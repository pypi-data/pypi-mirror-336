/* Copyright 2016 The TensorFlow Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

#ifndef TENSORFLOW_CORE_DISTRIBUTED_RUNTIME_BASE_RENDEZVOUS_MGR_H_
#define TENSORFLOW_CORE_DISTRIBUTED_RUNTIME_BASE_RENDEZVOUS_MGR_H_

#include <cstdint>
#include <memory>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <utility>

#include "absl/container/flat_hash_map.h"
#include "absl/container/flat_hash_set.h"
#include "tensorflow/core/common_runtime/eager/rendezvous_cache.h"
#include "tensorflow/core/distributed_runtime/rendezvous_mgr_interface.h"
#include "tensorflow/core/distributed_runtime/worker_env.h"
#include "tensorflow/core/distributed_runtime/worker_session.h"
#include "tensorflow/core/framework/cancellation.h"
#include "tensorflow/core/framework/control_flow.h"
#include "tensorflow/core/framework/local_rendezvous.h"
#include "tensorflow/core/framework/rendezvous.h"
#include "tensorflow/core/lib/core/status.h"
#include "tensorflow/core/lib/hash/hash.h"
#include "tensorflow/core/platform/macros.h"
#include "tensorflow/core/platform/mutex.h"
#include "tensorflow/core/platform/thread_annotations.h"
#include "tensorflow/core/platform/types.h"
#include "tensorflow/core/util/device_name_utils.h"
#include "tsl/platform/refcount.h"

namespace tensorflow {

class BaseRemoteRendezvous;
class BaseRecvTensorCall;

// RendezvousMgr keeps track of a set of local rendezvous instances.
// All tensors sent by this worker are buffered in a RendezvousMgr
// until the tensor is received.  Each global unique "step_id"
// corresponds to one local rendezvous instance managed by a
// RendezvousMgr.
// RendezvousMgr holds weak references to rendezvous. When a rendezvous is
// destructed, it will create a new instance to fulfill the Find.
//
// E.g.,
//   Rendezvous* rendez = worker_env->rendezvous_mgr->Find(0x8935);
//   fork execution of a graph executor using "rendez" on thread 1;
//   fork execution of another graph executor using "rendez" on thread 2;
//   ...
//   join threads 1 and 2;
//
// In the example above, execution in thread 1 and 2 communicates with
// each other by send/recv operations through `rendez`.
//
// Tensors sent and received through a rendezvous managed by this
// RendezvousMgr must have keys generated by Rendezvous::CreateKey().
class BaseRendezvousMgr : public RendezvousMgrInterface {
 public:
  explicit BaseRendezvousMgr(const WorkerEnv* worker_env);

  ~BaseRendezvousMgr() override;

  // Returns Rendezvous supporting send and recv among workers in the
  // "step_id".  The caller takes ownership of one reference on the
  // returned Rendezvous instance.
  //
  // Note: the caller must guarantee to eventually call Initialize on the
  // returned RemoteRendezvous
  tsl::core::RefCountPtr<RemoteRendezvous> Find(int64_t step_id) override;

  // Finds the local rendezvous instance for the "step_id".  Runs
  // "done" when the tensor for "key" is produced or an error occurs.
  //
  // This method is used by the rpc handler of RecvTensor.
  void RecvLocalAsync(int64_t step_id, const Rendezvous::ParsedKey& parsed,
                      Rendezvous::DoneCallback done) override;

  // Synchronous wrapper for RecvLocalAsync.
  absl::Status RecvLocal(int64_t step_id, const Rendezvous::ParsedKey& parsed,
                         Tensor* val, bool* is_dead) override;

  // Removes rendezvous for "step_id".
  void Cleanup(int64_t step_id) override { cache_->RemoveAndAbort(step_id); }

  // Remove all rendezvous instances owned by the rendezvous_mgr.
  void CleanupAll() override { cache_->RemoveAll(); }

 protected:
  virtual tsl::core::RefCountPtr<BaseRemoteRendezvous> Create(
      int64_t step_id, const WorkerEnv* worker_env) = 0;

 private:
  tsl::core::RefCountPtr<RendezvousCache<BaseRemoteRendezvous>> cache_;

  // Not owned.
  const WorkerEnv* const worker_env_;

  tsl::core::RefCountPtr<BaseRemoteRendezvous> FindOrCreate(int64_t step_id);

  BaseRendezvousMgr(const BaseRendezvousMgr&) = delete;
  void operator=(const BaseRendezvousMgr&) = delete;
};

// RemoteRendezvous is a Rendezvous which can handle either
// the producer or consumer being in a remote process.
//
// Buffering of Tensor values is delegated to a "local" Rendezvous
// obtained from NewLocalRendezvous().  This class just adds
// functionality to coordinate with remote workers.
class BaseRemoteRendezvous : public RemoteRendezvous {
 public:
  BaseRemoteRendezvous(const WorkerEnv* env, int64_t step_id);

  // Upgrades the BaseRemoteRendezvous to full initialization.
  absl::Status Initialize(WorkerSession* session) override;

  void SetRemoteEagerContextDefault() override {
    remote_eager_context_default_ = true;
  }
  bool IsRemoteEagerContextDefault() override {
    return remote_eager_context_default_;
  }

  // Forwards to local_, where the Tensor "val" will be buffered and
  // any waiting callback stored.
  absl::Status Send(const ParsedKey& key, const Rendezvous::Args& args,
                    const Tensor& val, bool is_dead) override;

  // This method is called only by the RecvOp.  It tests to see
  // whether the value will be produced by a local or remote device
  // and handles accordingly.  In the local case it forwards to
  // local_, in the remote case it initiates an RPC request.
  void RecvAsync(const ParsedKey& key, const Rendezvous::Args& args,
                 DoneCallback done) override;

  void StartAbort(const absl::Status& status) override;

  // This method is called only by the local Worker, forwarded through
  // the same method on RendezvousMgr.  This occurs when the Worker
  // has received a RecvTensor request, either locally or over the
  // network.  In either case it needs to retrieve a locally buffered
  // value from local_, and give it to its caller.
  //
  // Runs "done" as soon as the tensor for "parsed" is available or an error
  // is detected.
  //
  // REQUIRES: "parsed" is one that will be Saved into the local rendezvous.
  void RecvLocalAsync(const ParsedKey& parsed, DoneCallback done);

 protected:
  virtual void RecvFromRemoteAsync(const Rendezvous::ParsedKey& parsed,
                                   const Rendezvous::Args& args,
                                   DoneCallback done) = 0;

  // Returns true if "src" and "dst" are located in the same worker,
  // and hence may use a local rendezvous.
  virtual bool IsSameWorker(DeviceNameUtils::ParsedName src,
                            DeviceNameUtils::ParsedName dst);

  // If aborted, aborts "call". Otherwise, adds "call" into calls_.
  void RegisterCall(BaseRecvTensorCall* call, const Rendezvous::Args& args);

  // Removes "call" from calls_ if "call" is in calls_.
  void DeregisterCall(BaseRecvTensorCall* call, const Rendezvous::Args& args);

  WorkerSession* session();

  bool is_initialized();

  ~BaseRemoteRendezvous() override;

  const WorkerEnv* const env_;  // Not owned.
  const int64_t step_id_;

 private:
  int num_shards_;
  LocalRendezvous local_;
  // Indicates whether this remote rendezvous instance is used as the default
  // rendezvous for remote eager op-by-op execution. Errors in eager op-by-op
  // execution should not abort the rendezvous since it is a context-wide
  // instance and needs to be reused; instead, the errors are propagated through
  // eager executors.
  bool remote_eager_context_default_ = false;

  mutable mutex mu_;
  mutable mutex calls_mu_;

  // Status given by StartAbort() if any.
  absl::Status status_ TF_GUARDED_BY(mu_);

  WorkerSession* session_ TF_GUARDED_BY(mu_);  // Not owned.

  // Data structures to handle calls when partially initialized.
  struct DeferredCall {
    const ParsedKey parsed;
    DoneCallback done;

    // Keeps a reference to the rendezvous, to keep it alive.
    tsl::core::RefCountPtr<Rendezvous> rendezvous;

    DeferredCall(const ParsedKey& parsed, DoneCallback done,
                 tsl::core::RefCountPtr<Rendezvous> rendez);
  };
  std::vector<DeferredCall> deferred_calls_ TF_GUARDED_BY(mu_);

  struct CallBucket {
    mutex mu;

    absl::flat_hash_set<BaseRecvTensorCall*> calls TF_GUARDED_BY(mu);
  };

  struct PendingCalls {
    PendingCalls(CancellationToken token, int num_calls, int num_buckets,
                 tsl::core::RefCountPtr<Rendezvous> rendez)
        : token(token),
          num_calls(num_calls),
          buckets(num_buckets),
          rendezvous(std::move(rendez)) {}
    CancellationToken token = CancellationManager::kInvalidToken;
    std::atomic<int> num_calls = 0;
    std::vector<CallBucket> buckets;

    // Keeps a reference to the rendezvous, to keep it alive.
    tsl::core::RefCountPtr<Rendezvous> rendezvous;
  };

  // "CancellationToken" is stored here so that when there's no active
  // RecvTensorCalls, we can de-register the callback in the cancellation
  // manager. RecvTensorCalls are managed in multiple buckets since in large
  // scaled distributed training, lots of Send/Recv may be triggered
  // concurrently.
  //
  // Note: pointer to CancellationManager can be nullptr in certain use cases.
  absl::flat_hash_map<CancellationManager*, std::unique_ptr<PendingCalls>>
      calls_ TF_GUARDED_BY(calls_mu_);

  // Callback for CancellationManager.
  void CancelledByManager(CancellationManager* cm);

  bool is_initialized_locked() TF_SHARED_LOCKS_REQUIRED(mu_) {
    return session_ != nullptr;
  }

  // If "is_src" is true, checks that the rendezvous key "parsed"'s
  // source is in this process. If "is_src" is false, checks that the
  // rendezvous key "parsed"'s destination is in this process.
  absl::Status ValidateDevices(const Rendezvous::ParsedKey& parsed,
                               bool is_src);

  // Callback handling the case when a rendezvous has been
  // accomplished in local_ and the consumer is local to this process.
  // Tensor "in" will be copied into "out". The key "parsed" encodes
  // the src and dst devices.
  void SameWorkerRecvDone(const Rendezvous::ParsedKey& parsed,
                          const Rendezvous::Args& in_args,
                          const Rendezvous::Args& out_args, const Tensor& in,
                          Tensor* out, StatusCallback done);

  // Must be called only if fully initialized.
  void RecvLocalAsyncInternal(const ParsedKey& parsed, DoneCallback done);

  BaseRemoteRendezvous(const BaseRemoteRendezvous&) = delete;
  void operator=(const BaseRemoteRendezvous&) = delete;
};

class BaseRecvTensorCall {
 public:
  BaseRecvTensorCall() {}
  virtual ~BaseRecvTensorCall() {}

  virtual void Start(std::function<void()> recv_done) = 0;

  virtual void StartAbort(const absl::Status& s) = 0;

  virtual absl::Status status() const = 0;

 private:
  BaseRecvTensorCall(const BaseRecvTensorCall&) = delete;
  void operator=(const BaseRecvTensorCall&) = delete;
};

}  // end namespace tensorflow

#endif  // TENSORFLOW_CORE_DISTRIBUTED_RUNTIME_BASE_RENDEZVOUS_MGR_H_

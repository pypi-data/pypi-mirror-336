// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: tensorflow/core/protobuf/queue_runner.proto

#ifndef GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcore_2fprotobuf_2fqueue_5frunner_2eproto
#define GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcore_2fprotobuf_2fqueue_5frunner_2eproto

#include <limits>
#include <string>

#include <google/protobuf/port_def.inc>
#if PROTOBUF_VERSION < 3021000
#error This file was generated by a newer version of protoc which is
#error incompatible with your Protocol Buffer headers. Please update
#error your headers.
#endif
#if 3021009 < PROTOBUF_MIN_PROTOC_VERSION
#error This file was generated by an older version of protoc which is
#error incompatible with your Protocol Buffer headers. Please
#error regenerate this file with a newer version of protoc.
#endif

#include <google/protobuf/port_undef.inc>
#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/arena.h>
#include <google/protobuf/arenastring.h>
#include <google/protobuf/generated_message_util.h>
#include <google/protobuf/metadata_lite.h>
#include <google/protobuf/generated_message_reflection.h>
#include <google/protobuf/message.h>
#include <google/protobuf/repeated_field.h>  // IWYU pragma: export
#include <google/protobuf/extension_set.h>  // IWYU pragma: export
#include <google/protobuf/unknown_field_set.h>
#include "tensorflow/core/protobuf/error_codes.pb.h"
// @@protoc_insertion_point(includes)
#include <google/protobuf/port_def.inc>
#define PROTOBUF_INTERNAL_EXPORT_tensorflow_2fcore_2fprotobuf_2fqueue_5frunner_2eproto PROTOBUF_EXPORT
PROTOBUF_NAMESPACE_OPEN
namespace internal {
class AnyMetadata;
}  // namespace internal
PROTOBUF_NAMESPACE_CLOSE

// Internal implementation detail -- do not use these members.
struct PROTOBUF_EXPORT TableStruct_tensorflow_2fcore_2fprotobuf_2fqueue_5frunner_2eproto {
  static const uint32_t offsets[];
};
PROTOBUF_EXPORT extern const ::PROTOBUF_NAMESPACE_ID::internal::DescriptorTable descriptor_table_tensorflow_2fcore_2fprotobuf_2fqueue_5frunner_2eproto;
namespace tensorflow {
class QueueRunnerDef;
struct QueueRunnerDefDefaultTypeInternal;
PROTOBUF_EXPORT extern QueueRunnerDefDefaultTypeInternal _QueueRunnerDef_default_instance_;
}  // namespace tensorflow
PROTOBUF_NAMESPACE_OPEN
template<> PROTOBUF_EXPORT ::tensorflow::QueueRunnerDef* Arena::CreateMaybeMessage<::tensorflow::QueueRunnerDef>(Arena*);
PROTOBUF_NAMESPACE_CLOSE
namespace tensorflow {

// ===================================================================

class PROTOBUF_EXPORT QueueRunnerDef final :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:tensorflow.QueueRunnerDef) */ {
 public:
  inline QueueRunnerDef() : QueueRunnerDef(nullptr) {}
  ~QueueRunnerDef() override;
  explicit PROTOBUF_CONSTEXPR QueueRunnerDef(::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized);

  QueueRunnerDef(const QueueRunnerDef& from);
  QueueRunnerDef(QueueRunnerDef&& from) noexcept
    : QueueRunnerDef() {
    *this = ::std::move(from);
  }

  inline QueueRunnerDef& operator=(const QueueRunnerDef& from) {
    CopyFrom(from);
    return *this;
  }
  inline QueueRunnerDef& operator=(QueueRunnerDef&& from) noexcept {
    if (this == &from) return *this;
    if (GetOwningArena() == from.GetOwningArena()
  #ifdef PROTOBUF_FORCE_COPY_IN_MOVE
        && GetOwningArena() != nullptr
  #endif  // !PROTOBUF_FORCE_COPY_IN_MOVE
    ) {
      InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }

  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* descriptor() {
    return GetDescriptor();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* GetDescriptor() {
    return default_instance().GetMetadata().descriptor;
  }
  static const ::PROTOBUF_NAMESPACE_ID::Reflection* GetReflection() {
    return default_instance().GetMetadata().reflection;
  }
  static const QueueRunnerDef& default_instance() {
    return *internal_default_instance();
  }
  static inline const QueueRunnerDef* internal_default_instance() {
    return reinterpret_cast<const QueueRunnerDef*>(
               &_QueueRunnerDef_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    0;

  friend void swap(QueueRunnerDef& a, QueueRunnerDef& b) {
    a.Swap(&b);
  }
  inline void Swap(QueueRunnerDef* other) {
    if (other == this) return;
  #ifdef PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() != nullptr &&
        GetOwningArena() == other->GetOwningArena()) {
   #else  // PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() == other->GetOwningArena()) {
  #endif  // !PROTOBUF_FORCE_COPY_IN_SWAP
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(QueueRunnerDef* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetOwningArena() == other->GetOwningArena());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  QueueRunnerDef* New(::PROTOBUF_NAMESPACE_ID::Arena* arena = nullptr) const final {
    return CreateMaybeMessage<QueueRunnerDef>(arena);
  }
  using ::PROTOBUF_NAMESPACE_ID::Message::CopyFrom;
  void CopyFrom(const QueueRunnerDef& from);
  using ::PROTOBUF_NAMESPACE_ID::Message::MergeFrom;
  void MergeFrom( const QueueRunnerDef& from) {
    QueueRunnerDef::MergeImpl(*this, from);
  }
  private:
  static void MergeImpl(::PROTOBUF_NAMESPACE_ID::Message& to_msg, const ::PROTOBUF_NAMESPACE_ID::Message& from_msg);
  public:
  PROTOBUF_ATTRIBUTE_REINITIALIZES void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  const char* _InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) final;
  uint8_t* _InternalSerialize(
      uint8_t* target, ::PROTOBUF_NAMESPACE_ID::io::EpsCopyOutputStream* stream) const final;
  int GetCachedSize() const final { return _impl_._cached_size_.Get(); }

  private:
  void SharedCtor(::PROTOBUF_NAMESPACE_ID::Arena* arena, bool is_message_owned);
  void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(QueueRunnerDef* other);

  private:
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "tensorflow.QueueRunnerDef";
  }
  protected:
  explicit QueueRunnerDef(::PROTOBUF_NAMESPACE_ID::Arena* arena,
                       bool is_message_owned = false);
  public:

  static const ClassData _class_data_;
  const ::PROTOBUF_NAMESPACE_ID::Message::ClassData*GetClassData() const final;

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  enum : int {
    kEnqueueOpNameFieldNumber = 2,
    kQueueClosedExceptionTypesFieldNumber = 5,
    kQueueNameFieldNumber = 1,
    kCloseOpNameFieldNumber = 3,
    kCancelOpNameFieldNumber = 4,
  };
  // repeated string enqueue_op_name = 2;
  int enqueue_op_name_size() const;
  private:
  int _internal_enqueue_op_name_size() const;
  public:
  void clear_enqueue_op_name();
  const std::string& enqueue_op_name(int index) const;
  std::string* mutable_enqueue_op_name(int index);
  void set_enqueue_op_name(int index, const std::string& value);
  void set_enqueue_op_name(int index, std::string&& value);
  void set_enqueue_op_name(int index, const char* value);
  void set_enqueue_op_name(int index, const char* value, size_t size);
  std::string* add_enqueue_op_name();
  void add_enqueue_op_name(const std::string& value);
  void add_enqueue_op_name(std::string&& value);
  void add_enqueue_op_name(const char* value);
  void add_enqueue_op_name(const char* value, size_t size);
  const ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField<std::string>& enqueue_op_name() const;
  ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField<std::string>* mutable_enqueue_op_name();
  private:
  const std::string& _internal_enqueue_op_name(int index) const;
  std::string* _internal_add_enqueue_op_name();
  public:

  // repeated .tensorflow.error.Code queue_closed_exception_types = 5;
  int queue_closed_exception_types_size() const;
  private:
  int _internal_queue_closed_exception_types_size() const;
  public:
  void clear_queue_closed_exception_types();
  private:
  ::tensorflow::error::Code _internal_queue_closed_exception_types(int index) const;
  void _internal_add_queue_closed_exception_types(::tensorflow::error::Code value);
  ::PROTOBUF_NAMESPACE_ID::RepeatedField<int>* _internal_mutable_queue_closed_exception_types();
  public:
  ::tensorflow::error::Code queue_closed_exception_types(int index) const;
  void set_queue_closed_exception_types(int index, ::tensorflow::error::Code value);
  void add_queue_closed_exception_types(::tensorflow::error::Code value);
  const ::PROTOBUF_NAMESPACE_ID::RepeatedField<int>& queue_closed_exception_types() const;
  ::PROTOBUF_NAMESPACE_ID::RepeatedField<int>* mutable_queue_closed_exception_types();

  // string queue_name = 1;
  void clear_queue_name();
  const std::string& queue_name() const;
  template <typename ArgT0 = const std::string&, typename... ArgT>
  void set_queue_name(ArgT0&& arg0, ArgT... args);
  std::string* mutable_queue_name();
  PROTOBUF_NODISCARD std::string* release_queue_name();
  void set_allocated_queue_name(std::string* queue_name);
  private:
  const std::string& _internal_queue_name() const;
  inline PROTOBUF_ALWAYS_INLINE void _internal_set_queue_name(const std::string& value);
  std::string* _internal_mutable_queue_name();
  public:

  // string close_op_name = 3;
  void clear_close_op_name();
  const std::string& close_op_name() const;
  template <typename ArgT0 = const std::string&, typename... ArgT>
  void set_close_op_name(ArgT0&& arg0, ArgT... args);
  std::string* mutable_close_op_name();
  PROTOBUF_NODISCARD std::string* release_close_op_name();
  void set_allocated_close_op_name(std::string* close_op_name);
  private:
  const std::string& _internal_close_op_name() const;
  inline PROTOBUF_ALWAYS_INLINE void _internal_set_close_op_name(const std::string& value);
  std::string* _internal_mutable_close_op_name();
  public:

  // string cancel_op_name = 4;
  void clear_cancel_op_name();
  const std::string& cancel_op_name() const;
  template <typename ArgT0 = const std::string&, typename... ArgT>
  void set_cancel_op_name(ArgT0&& arg0, ArgT... args);
  std::string* mutable_cancel_op_name();
  PROTOBUF_NODISCARD std::string* release_cancel_op_name();
  void set_allocated_cancel_op_name(std::string* cancel_op_name);
  private:
  const std::string& _internal_cancel_op_name() const;
  inline PROTOBUF_ALWAYS_INLINE void _internal_set_cancel_op_name(const std::string& value);
  std::string* _internal_mutable_cancel_op_name();
  public:

  // @@protoc_insertion_point(class_scope:tensorflow.QueueRunnerDef)
 private:
  class _Internal;

  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  struct Impl_ {
    ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField<std::string> enqueue_op_name_;
    ::PROTOBUF_NAMESPACE_ID::RepeatedField<int> queue_closed_exception_types_;
    mutable std::atomic<int> _queue_closed_exception_types_cached_byte_size_;
    ::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr queue_name_;
    ::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr close_op_name_;
    ::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr cancel_op_name_;
    mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  };
  union { Impl_ _impl_; };
  friend struct ::TableStruct_tensorflow_2fcore_2fprotobuf_2fqueue_5frunner_2eproto;
};
// ===================================================================


// ===================================================================

#ifdef __GNUC__
  #pragma GCC diagnostic push
  #pragma GCC diagnostic ignored "-Wstrict-aliasing"
#endif  // __GNUC__
// QueueRunnerDef

// string queue_name = 1;
inline void QueueRunnerDef::clear_queue_name() {
  _impl_.queue_name_.ClearToEmpty();
}
inline const std::string& QueueRunnerDef::queue_name() const {
  // @@protoc_insertion_point(field_get:tensorflow.QueueRunnerDef.queue_name)
  return _internal_queue_name();
}
template <typename ArgT0, typename... ArgT>
inline PROTOBUF_ALWAYS_INLINE
void QueueRunnerDef::set_queue_name(ArgT0&& arg0, ArgT... args) {
 
 _impl_.queue_name_.Set(static_cast<ArgT0 &&>(arg0), args..., GetArenaForAllocation());
  // @@protoc_insertion_point(field_set:tensorflow.QueueRunnerDef.queue_name)
}
inline std::string* QueueRunnerDef::mutable_queue_name() {
  std::string* _s = _internal_mutable_queue_name();
  // @@protoc_insertion_point(field_mutable:tensorflow.QueueRunnerDef.queue_name)
  return _s;
}
inline const std::string& QueueRunnerDef::_internal_queue_name() const {
  return _impl_.queue_name_.Get();
}
inline void QueueRunnerDef::_internal_set_queue_name(const std::string& value) {
  
  _impl_.queue_name_.Set(value, GetArenaForAllocation());
}
inline std::string* QueueRunnerDef::_internal_mutable_queue_name() {
  
  return _impl_.queue_name_.Mutable(GetArenaForAllocation());
}
inline std::string* QueueRunnerDef::release_queue_name() {
  // @@protoc_insertion_point(field_release:tensorflow.QueueRunnerDef.queue_name)
  return _impl_.queue_name_.Release();
}
inline void QueueRunnerDef::set_allocated_queue_name(std::string* queue_name) {
  if (queue_name != nullptr) {
    
  } else {
    
  }
  _impl_.queue_name_.SetAllocated(queue_name, GetArenaForAllocation());
#ifdef PROTOBUF_FORCE_COPY_DEFAULT_STRING
  if (_impl_.queue_name_.IsDefault()) {
    _impl_.queue_name_.Set("", GetArenaForAllocation());
  }
#endif // PROTOBUF_FORCE_COPY_DEFAULT_STRING
  // @@protoc_insertion_point(field_set_allocated:tensorflow.QueueRunnerDef.queue_name)
}

// repeated string enqueue_op_name = 2;
inline int QueueRunnerDef::_internal_enqueue_op_name_size() const {
  return _impl_.enqueue_op_name_.size();
}
inline int QueueRunnerDef::enqueue_op_name_size() const {
  return _internal_enqueue_op_name_size();
}
inline void QueueRunnerDef::clear_enqueue_op_name() {
  _impl_.enqueue_op_name_.Clear();
}
inline std::string* QueueRunnerDef::add_enqueue_op_name() {
  std::string* _s = _internal_add_enqueue_op_name();
  // @@protoc_insertion_point(field_add_mutable:tensorflow.QueueRunnerDef.enqueue_op_name)
  return _s;
}
inline const std::string& QueueRunnerDef::_internal_enqueue_op_name(int index) const {
  return _impl_.enqueue_op_name_.Get(index);
}
inline const std::string& QueueRunnerDef::enqueue_op_name(int index) const {
  // @@protoc_insertion_point(field_get:tensorflow.QueueRunnerDef.enqueue_op_name)
  return _internal_enqueue_op_name(index);
}
inline std::string* QueueRunnerDef::mutable_enqueue_op_name(int index) {
  // @@protoc_insertion_point(field_mutable:tensorflow.QueueRunnerDef.enqueue_op_name)
  return _impl_.enqueue_op_name_.Mutable(index);
}
inline void QueueRunnerDef::set_enqueue_op_name(int index, const std::string& value) {
  _impl_.enqueue_op_name_.Mutable(index)->assign(value);
  // @@protoc_insertion_point(field_set:tensorflow.QueueRunnerDef.enqueue_op_name)
}
inline void QueueRunnerDef::set_enqueue_op_name(int index, std::string&& value) {
  _impl_.enqueue_op_name_.Mutable(index)->assign(std::move(value));
  // @@protoc_insertion_point(field_set:tensorflow.QueueRunnerDef.enqueue_op_name)
}
inline void QueueRunnerDef::set_enqueue_op_name(int index, const char* value) {
  GOOGLE_DCHECK(value != nullptr);
  _impl_.enqueue_op_name_.Mutable(index)->assign(value);
  // @@protoc_insertion_point(field_set_char:tensorflow.QueueRunnerDef.enqueue_op_name)
}
inline void QueueRunnerDef::set_enqueue_op_name(int index, const char* value, size_t size) {
  _impl_.enqueue_op_name_.Mutable(index)->assign(
    reinterpret_cast<const char*>(value), size);
  // @@protoc_insertion_point(field_set_pointer:tensorflow.QueueRunnerDef.enqueue_op_name)
}
inline std::string* QueueRunnerDef::_internal_add_enqueue_op_name() {
  return _impl_.enqueue_op_name_.Add();
}
inline void QueueRunnerDef::add_enqueue_op_name(const std::string& value) {
  _impl_.enqueue_op_name_.Add()->assign(value);
  // @@protoc_insertion_point(field_add:tensorflow.QueueRunnerDef.enqueue_op_name)
}
inline void QueueRunnerDef::add_enqueue_op_name(std::string&& value) {
  _impl_.enqueue_op_name_.Add(std::move(value));
  // @@protoc_insertion_point(field_add:tensorflow.QueueRunnerDef.enqueue_op_name)
}
inline void QueueRunnerDef::add_enqueue_op_name(const char* value) {
  GOOGLE_DCHECK(value != nullptr);
  _impl_.enqueue_op_name_.Add()->assign(value);
  // @@protoc_insertion_point(field_add_char:tensorflow.QueueRunnerDef.enqueue_op_name)
}
inline void QueueRunnerDef::add_enqueue_op_name(const char* value, size_t size) {
  _impl_.enqueue_op_name_.Add()->assign(reinterpret_cast<const char*>(value), size);
  // @@protoc_insertion_point(field_add_pointer:tensorflow.QueueRunnerDef.enqueue_op_name)
}
inline const ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField<std::string>&
QueueRunnerDef::enqueue_op_name() const {
  // @@protoc_insertion_point(field_list:tensorflow.QueueRunnerDef.enqueue_op_name)
  return _impl_.enqueue_op_name_;
}
inline ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField<std::string>*
QueueRunnerDef::mutable_enqueue_op_name() {
  // @@protoc_insertion_point(field_mutable_list:tensorflow.QueueRunnerDef.enqueue_op_name)
  return &_impl_.enqueue_op_name_;
}

// string close_op_name = 3;
inline void QueueRunnerDef::clear_close_op_name() {
  _impl_.close_op_name_.ClearToEmpty();
}
inline const std::string& QueueRunnerDef::close_op_name() const {
  // @@protoc_insertion_point(field_get:tensorflow.QueueRunnerDef.close_op_name)
  return _internal_close_op_name();
}
template <typename ArgT0, typename... ArgT>
inline PROTOBUF_ALWAYS_INLINE
void QueueRunnerDef::set_close_op_name(ArgT0&& arg0, ArgT... args) {
 
 _impl_.close_op_name_.Set(static_cast<ArgT0 &&>(arg0), args..., GetArenaForAllocation());
  // @@protoc_insertion_point(field_set:tensorflow.QueueRunnerDef.close_op_name)
}
inline std::string* QueueRunnerDef::mutable_close_op_name() {
  std::string* _s = _internal_mutable_close_op_name();
  // @@protoc_insertion_point(field_mutable:tensorflow.QueueRunnerDef.close_op_name)
  return _s;
}
inline const std::string& QueueRunnerDef::_internal_close_op_name() const {
  return _impl_.close_op_name_.Get();
}
inline void QueueRunnerDef::_internal_set_close_op_name(const std::string& value) {
  
  _impl_.close_op_name_.Set(value, GetArenaForAllocation());
}
inline std::string* QueueRunnerDef::_internal_mutable_close_op_name() {
  
  return _impl_.close_op_name_.Mutable(GetArenaForAllocation());
}
inline std::string* QueueRunnerDef::release_close_op_name() {
  // @@protoc_insertion_point(field_release:tensorflow.QueueRunnerDef.close_op_name)
  return _impl_.close_op_name_.Release();
}
inline void QueueRunnerDef::set_allocated_close_op_name(std::string* close_op_name) {
  if (close_op_name != nullptr) {
    
  } else {
    
  }
  _impl_.close_op_name_.SetAllocated(close_op_name, GetArenaForAllocation());
#ifdef PROTOBUF_FORCE_COPY_DEFAULT_STRING
  if (_impl_.close_op_name_.IsDefault()) {
    _impl_.close_op_name_.Set("", GetArenaForAllocation());
  }
#endif // PROTOBUF_FORCE_COPY_DEFAULT_STRING
  // @@protoc_insertion_point(field_set_allocated:tensorflow.QueueRunnerDef.close_op_name)
}

// string cancel_op_name = 4;
inline void QueueRunnerDef::clear_cancel_op_name() {
  _impl_.cancel_op_name_.ClearToEmpty();
}
inline const std::string& QueueRunnerDef::cancel_op_name() const {
  // @@protoc_insertion_point(field_get:tensorflow.QueueRunnerDef.cancel_op_name)
  return _internal_cancel_op_name();
}
template <typename ArgT0, typename... ArgT>
inline PROTOBUF_ALWAYS_INLINE
void QueueRunnerDef::set_cancel_op_name(ArgT0&& arg0, ArgT... args) {
 
 _impl_.cancel_op_name_.Set(static_cast<ArgT0 &&>(arg0), args..., GetArenaForAllocation());
  // @@protoc_insertion_point(field_set:tensorflow.QueueRunnerDef.cancel_op_name)
}
inline std::string* QueueRunnerDef::mutable_cancel_op_name() {
  std::string* _s = _internal_mutable_cancel_op_name();
  // @@protoc_insertion_point(field_mutable:tensorflow.QueueRunnerDef.cancel_op_name)
  return _s;
}
inline const std::string& QueueRunnerDef::_internal_cancel_op_name() const {
  return _impl_.cancel_op_name_.Get();
}
inline void QueueRunnerDef::_internal_set_cancel_op_name(const std::string& value) {
  
  _impl_.cancel_op_name_.Set(value, GetArenaForAllocation());
}
inline std::string* QueueRunnerDef::_internal_mutable_cancel_op_name() {
  
  return _impl_.cancel_op_name_.Mutable(GetArenaForAllocation());
}
inline std::string* QueueRunnerDef::release_cancel_op_name() {
  // @@protoc_insertion_point(field_release:tensorflow.QueueRunnerDef.cancel_op_name)
  return _impl_.cancel_op_name_.Release();
}
inline void QueueRunnerDef::set_allocated_cancel_op_name(std::string* cancel_op_name) {
  if (cancel_op_name != nullptr) {
    
  } else {
    
  }
  _impl_.cancel_op_name_.SetAllocated(cancel_op_name, GetArenaForAllocation());
#ifdef PROTOBUF_FORCE_COPY_DEFAULT_STRING
  if (_impl_.cancel_op_name_.IsDefault()) {
    _impl_.cancel_op_name_.Set("", GetArenaForAllocation());
  }
#endif // PROTOBUF_FORCE_COPY_DEFAULT_STRING
  // @@protoc_insertion_point(field_set_allocated:tensorflow.QueueRunnerDef.cancel_op_name)
}

// repeated .tensorflow.error.Code queue_closed_exception_types = 5;
inline int QueueRunnerDef::_internal_queue_closed_exception_types_size() const {
  return _impl_.queue_closed_exception_types_.size();
}
inline int QueueRunnerDef::queue_closed_exception_types_size() const {
  return _internal_queue_closed_exception_types_size();
}
inline void QueueRunnerDef::clear_queue_closed_exception_types() {
  _impl_.queue_closed_exception_types_.Clear();
}
inline ::tensorflow::error::Code QueueRunnerDef::_internal_queue_closed_exception_types(int index) const {
  return static_cast< ::tensorflow::error::Code >(_impl_.queue_closed_exception_types_.Get(index));
}
inline ::tensorflow::error::Code QueueRunnerDef::queue_closed_exception_types(int index) const {
  // @@protoc_insertion_point(field_get:tensorflow.QueueRunnerDef.queue_closed_exception_types)
  return _internal_queue_closed_exception_types(index);
}
inline void QueueRunnerDef::set_queue_closed_exception_types(int index, ::tensorflow::error::Code value) {
  _impl_.queue_closed_exception_types_.Set(index, value);
  // @@protoc_insertion_point(field_set:tensorflow.QueueRunnerDef.queue_closed_exception_types)
}
inline void QueueRunnerDef::_internal_add_queue_closed_exception_types(::tensorflow::error::Code value) {
  _impl_.queue_closed_exception_types_.Add(value);
}
inline void QueueRunnerDef::add_queue_closed_exception_types(::tensorflow::error::Code value) {
  _internal_add_queue_closed_exception_types(value);
  // @@protoc_insertion_point(field_add:tensorflow.QueueRunnerDef.queue_closed_exception_types)
}
inline const ::PROTOBUF_NAMESPACE_ID::RepeatedField<int>&
QueueRunnerDef::queue_closed_exception_types() const {
  // @@protoc_insertion_point(field_list:tensorflow.QueueRunnerDef.queue_closed_exception_types)
  return _impl_.queue_closed_exception_types_;
}
inline ::PROTOBUF_NAMESPACE_ID::RepeatedField<int>*
QueueRunnerDef::_internal_mutable_queue_closed_exception_types() {
  return &_impl_.queue_closed_exception_types_;
}
inline ::PROTOBUF_NAMESPACE_ID::RepeatedField<int>*
QueueRunnerDef::mutable_queue_closed_exception_types() {
  // @@protoc_insertion_point(field_mutable_list:tensorflow.QueueRunnerDef.queue_closed_exception_types)
  return _internal_mutable_queue_closed_exception_types();
}

#ifdef __GNUC__
  #pragma GCC diagnostic pop
#endif  // __GNUC__

// @@protoc_insertion_point(namespace_scope)

}  // namespace tensorflow

// @@protoc_insertion_point(global_scope)

#include <google/protobuf/port_undef.inc>
#endif  // GOOGLE_PROTOBUF_INCLUDED_GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcore_2fprotobuf_2fqueue_5frunner_2eproto

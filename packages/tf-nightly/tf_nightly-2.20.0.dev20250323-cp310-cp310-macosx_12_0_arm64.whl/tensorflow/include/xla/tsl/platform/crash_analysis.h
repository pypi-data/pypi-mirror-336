/* Copyright 2021 The TensorFlow Authors. All Rights Reserved.

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

#ifndef XLA_TSL_PLATFORM_CRASH_ANALYSIS_H_
#define XLA_TSL_PLATFORM_CRASH_ANALYSIS_H_

#include "tsl/platform/platform.h"

// Include appropriate platform-dependent implementations
#if defined(PLATFORM_GOOGLE)
#include "xla/tsl/platform/google/crash_analysis.h"  // IWYU pragma: export
#else
#include "xla/tsl/platform/default/crash_analysis.h"  // IWYU pragma: export
#endif

#endif  // XLA_TSL_PLATFORM_CRASH_ANALYSIS_H_

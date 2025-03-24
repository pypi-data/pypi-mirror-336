// SPDX-License-Identifier: MIT
// Copyright (c) 2018-2023, Advanced Micro Devices, Inc. All rights reserved.

#pragma once

#include "ck/utility/data_type.hpp"
#include "ck/utility/reduction_enums.hpp"

#include "ck/library/tensor_operation_instance/gpu/reduce/device_reduce_instance_threadwise.hpp"

namespace ck {
namespace tensor_operation {
namespace device {
namespace instance {

// clang-format off
// InDataType | AccDataType | OutDataType | Rank | NumReduceDim | ReduceOperation | InElementwiseOp | AccElementwiseOp | PropagateNan | UseIndex 
extern template void add_device_reduce_instance_threadwise<F16, F32, F16, 4, 3, ReduceAdd, UnarySquare, UnarySqrt, false, false>(std::vector<DeviceReducePtr<F16, F32, F16, 4, 3, ReduceAdd, UnarySquare, UnarySqrt, false, false>>&); 
extern template void add_device_reduce_instance_threadwise<F16, F32, F16, 4, 4, ReduceAdd, UnarySquare, UnarySqrt, false, false>(std::vector<DeviceReducePtr<F16, F32, F16, 4, 4, ReduceAdd, UnarySquare, UnarySqrt, false, false>>&); 
extern template void add_device_reduce_instance_threadwise<F16, F32, F16, 4, 1, ReduceAdd, UnarySquare, UnarySqrt, false, false>(std::vector<DeviceReducePtr<F16, F32, F16, 4, 1, ReduceAdd, UnarySquare, UnarySqrt, false, false>>&); 
extern template void add_device_reduce_instance_threadwise<F16, F32, F16, 2, 1, ReduceAdd, UnarySquare, UnarySqrt, false, false>(std::vector<DeviceReducePtr<F16, F32, F16, 2, 1, ReduceAdd, UnarySquare, UnarySqrt, false, false>>&);
// clang-format on

} // namespace instance
} // namespace device
} // namespace tensor_operation
} // namespace ck

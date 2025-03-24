// SPDX-License-Identifier: MIT
// Copyright (c) 2018-2023, Advanced Micro Devices, Inc. All rights reserved.

#include "ck/utility/reduction_enums.hpp"
#include "ck/library/tensor_operation_instance/gpu/reduce/device_reduce_instance_blockwise.hpp"

namespace ck {
namespace tensor_operation {
namespace device {
namespace instance {

// clang-format off
// InDataType | AccDataType | OutDataType | Rank | NumReduceDim | ReduceOperation | InElementwiseOp | AccElementwiseOp | PropagateNan | UseIndex 
template void add_device_reduce_instance_blockwise<F64, F64, F64, 4, 3, ReduceMax, PassThrough, PassThrough, false, false>(std::vector<DeviceReducePtr<F64, F64, F64, 4, 3, ReduceMax, PassThrough, PassThrough, false, false>>&);
template void add_device_reduce_instance_blockwise<F64, F64, F64, 4, 4, ReduceMax, PassThrough, PassThrough, false, false>(std::vector<DeviceReducePtr<F64, F64, F64, 4, 4, ReduceMax, PassThrough, PassThrough, false, false>>&);
template void add_device_reduce_instance_blockwise<F64, F64, F64, 4, 1, ReduceMax, PassThrough, PassThrough, false, false>(std::vector<DeviceReducePtr<F64, F64, F64, 4, 1, ReduceMax, PassThrough, PassThrough, false, false>>&);
template void add_device_reduce_instance_blockwise<F64, F64, F64, 2, 1, ReduceMax, PassThrough, PassThrough, false, false>(std::vector<DeviceReducePtr<F64, F64, F64, 2, 1, ReduceMax, PassThrough, PassThrough, false, false>>&);
template void add_device_reduce_instance_blockwise<F64, F64, F64, 4, 3, ReduceMax, PassThrough, PassThrough, false, true>(std::vector<DeviceReducePtr<F64, F64, F64, 4, 3, ReduceMax, PassThrough, PassThrough, false, true>>&);
template void add_device_reduce_instance_blockwise<F64, F64, F64, 4, 4, ReduceMax, PassThrough, PassThrough, false, true>(std::vector<DeviceReducePtr<F64, F64, F64, 4, 4, ReduceMax, PassThrough, PassThrough, false, true>>&);
template void add_device_reduce_instance_blockwise<F64, F64, F64, 4, 1, ReduceMax, PassThrough, PassThrough, false, true>(std::vector<DeviceReducePtr<F64, F64, F64, 4, 1, ReduceMax, PassThrough, PassThrough, false, true>>&);
template void add_device_reduce_instance_blockwise<F64, F64, F64, 2, 1, ReduceMax, PassThrough, PassThrough, false, true>(std::vector<DeviceReducePtr<F64, F64, F64, 2, 1, ReduceMax, PassThrough, PassThrough, false, true>>&);
// clang-format on

} // namespace instance
} // namespace device
} // namespace tensor_operation

} // namespace ck

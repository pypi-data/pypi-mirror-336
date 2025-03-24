// SPDX-License-Identifier: MIT
// Copyright (c) 2018-2023, Advanced Micro Devices, Inc. All rights reserved.

#include "device_conv2d_dl_int8_instance.hpp"

namespace ck {
namespace tensor_operation {
namespace device {
namespace instance {
void add_device_conv2d_dl_perlayer_quantization_int8_instances(
    std::vector<std::unique_ptr<DeviceGroupedConvFwdMultipleABD<NDimSpatial,
                                                                NHWGC,
                                                                GKYXC,
                                                                Empty_Tuple,
                                                                NHWGK,
                                                                int8_t,
                                                                int8_t,
                                                                Empty_Tuple,
                                                                int8_t,
                                                                PassThrough,
                                                                PassThrough,
                                                                Mul_Clamp>>>& instances)
{
    add_device_operation_instances(instances,
                                   device_grouped_conv2d_dl_int8_instances<NHWGC,
                                                                           GKYXC,
                                                                           Empty_Tuple,
                                                                           NHWGK,
                                                                           Empty_Tuple,
                                                                           Mul_Clamp,
                                                                           ConvFwdDefault,
                                                                           4>{});
    add_device_operation_instances(instances,
                                   device_grouped_conv2d_dl_int8_instances<NHWGC,
                                                                           GKYXC,
                                                                           Empty_Tuple,
                                                                           NHWGK,
                                                                           Empty_Tuple,
                                                                           Mul_Clamp,
                                                                           ConvFwd1x1P0,
                                                                           4>{});
    add_device_operation_instances(instances,
                                   device_grouped_conv2d_dl_int8_instances<NHWGC,
                                                                           GKYXC,
                                                                           Empty_Tuple,
                                                                           NHWGK,
                                                                           Empty_Tuple,
                                                                           Mul_Clamp,
                                                                           ConvFwd1x1S1P0,
                                                                           4>{});
}

void add_device_conv2d_dl_relu_perlayer_quantization_int8_instances(
    std::vector<std::unique_ptr<DeviceGroupedConvFwdMultipleABD<NDimSpatial,
                                                                NHWGC,
                                                                GKYXC,
                                                                Empty_Tuple,
                                                                NHWGK,
                                                                int8_t,
                                                                int8_t,
                                                                Empty_Tuple,
                                                                int8_t,
                                                                PassThrough,
                                                                PassThrough,
                                                                Relu_Mul_Clamp>>>& instances)
{
    add_device_operation_instances(instances,
                                   device_grouped_conv2d_dl_int8_instances<NHWGC,
                                                                           GKYXC,
                                                                           Empty_Tuple,
                                                                           NHWGK,
                                                                           Empty_Tuple,
                                                                           Relu_Mul_Clamp,
                                                                           ConvFwdDefault,
                                                                           4>{});
    add_device_operation_instances(instances,
                                   device_grouped_conv2d_dl_int8_instances<NHWGC,
                                                                           GKYXC,
                                                                           Empty_Tuple,
                                                                           NHWGK,
                                                                           Empty_Tuple,
                                                                           Relu_Mul_Clamp,
                                                                           ConvFwd1x1P0,
                                                                           4>{});
    add_device_operation_instances(instances,
                                   device_grouped_conv2d_dl_int8_instances<NHWGC,
                                                                           GKYXC,
                                                                           Empty_Tuple,
                                                                           NHWGK,
                                                                           Empty_Tuple,
                                                                           Relu_Mul_Clamp,
                                                                           ConvFwd1x1S1P0,
                                                                           4>{});
}
} // namespace instance
} // namespace device
} // namespace tensor_operation
} // namespace ck

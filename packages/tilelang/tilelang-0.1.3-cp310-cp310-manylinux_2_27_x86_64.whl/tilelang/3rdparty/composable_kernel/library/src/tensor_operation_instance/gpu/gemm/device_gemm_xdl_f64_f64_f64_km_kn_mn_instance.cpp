// SPDX-License-Identifier: MIT
// Copyright (c) 2018-2023, Advanced Micro Devices, Inc. All rights reserved.

#include <cstdlib>

#include "ck/ck.hpp"
#include "ck/tensor_operation/gpu/device/tensor_layout.hpp"
#include "ck/tensor_operation/gpu/device/gemm_specialization.hpp"
#include "ck/tensor_operation/gpu/device/impl/device_gemm_xdl.hpp"
#include "ck/library/tensor_operation_instance/add_device_operation_instance.hpp"

namespace ck {
namespace tensor_operation {
namespace device {
namespace instance {

using F64 = double;

using Row = ck::tensor_layout::gemm::RowMajor;
using Col = ck::tensor_layout::gemm::ColumnMajor;

template <ck::index_t... Is>
using S = ck::Sequence<Is...>;

using PassThrough = ck::tensor_operation::element_wise::PassThrough;

static constexpr auto GemmDefault = ck::tensor_operation::device::GemmSpecialization::Default;

// Compilation parameters for a[k, m] * b[k, n] = c[m, n]
using device_gemm_xdl_f64_f64_f64_km_kn_mn_instances =
    std::tuple<
        // clang-format off
        //##########| AData| BData| CData| AccData| ALayout| BLayout| CLayout|           A|           B|           C|          GEMM| Block|  MPer|  NPer| K0Per| K1| MPer| NPer| MXdl| NXdl|  ABlockTransfer| ABlockTransfer| ABlockTransfer| ABlockTransfer| ABlockTransfer| ABlockTransfer| ABlockLds|  BBlockTransfer| BBlockTransfer| BBlockTransfer| BlockTransfer| BBlockTransfer| BBlockTransfer| BBlockLds| CThreadTransfer| CThreadTransfer|
        //##########|  Type|  Type|  Type|    Type|        |        |        | Elementwise| Elementwise| Elementwise|Specialization|  Size| Block| Block| Block|   |  XDL|  XDL|  Per|  Per|   ThreadCluster|  ThreadCluster| SrcAccessOrder|   SrcVectorDim|      SrcScalar|      DstScalar| AddExtraM|   ThreadCluster|  ThreadCluster| SrcAccessOrder|  SrcVectorDim|      SrcScalar|      DstScalar| AddExtraN| SrcDstVectorDim|       DstScalar|
        //##########|      |      |      |        |        |        |        |   Operation|   Operation|   Operation|              |      |      |      |      |   |     |     | Wave| Wave| Lengths_K0_M_K1|   ArrangeOrder|               |               |      PerVector|   PerVector_K1|          | Lengths_K0_N_K1|   ArrangeOrder|               |              |      PerVector|   PerVector_K1|          |                |       PerVector|
        //##########|      |      |      |        |        |        |        |            |            |            |              |      |      |      |      |   |     |     |     |     |                |               |               |               |               |               |          |                |               |               |              |               |               |          |                |                |
        DeviceGemmXdl<  F64,   F64,   F64,     F64,     Col,     Row,     Row, PassThrough, PassThrough, PassThrough,   GemmDefault,   256,   128,   128,     4,  2,   16,   16,    4,    4,     S<4, 64, 1>,     S<0, 2, 1>,     S<0, 2, 1>,              1,              2,              2,      true,     S<4, 64, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              2,              2,      true,               7,               1>,
        DeviceGemmXdl<  F64,   F64,   F64,     F64,     Col,     Row,     Row, PassThrough, PassThrough, PassThrough,   GemmDefault,   128,   128,    64,     4,  2,   16,   16,    4,    4,     S<4, 32, 1>,     S<0, 2, 1>,     S<0, 2, 1>,              1,              4,              2,      true,     S<4, 32, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              2,              2,      true,               7,               1>,
        DeviceGemmXdl<  F64,   F64,   F64,     F64,     Col,     Row,     Row, PassThrough, PassThrough, PassThrough,   GemmDefault,   128,    64,   128,     4,  2,   16,   16,    4,    4,     S<4, 32, 1>,     S<0, 2, 1>,     S<0, 2, 1>,              1,              2,              2,      true,     S<4, 32, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              4,              2,      true,               7,               1>,
        DeviceGemmXdl<  F64,   F64,   F64,     F64,     Col,     Row,     Row, PassThrough, PassThrough, PassThrough,   GemmDefault,   256,   128,    64,     4,  2,   16,   16,    4,    2,     S<4, 64, 1>,     S<0, 2, 1>,     S<0, 2, 1>,              1,              2,              2,      true,     S<4, 64, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              1,              2,      true,               7,               1>,
        DeviceGemmXdl<  F64,   F64,   F64,     F64,     Col,     Row,     Row, PassThrough, PassThrough, PassThrough,   GemmDefault,   256,    64,   128,     4,  2,   16,   16,    2,    4,     S<4, 64, 1>,     S<0, 2, 1>,     S<0, 2, 1>,              1,              1,              2,      true,     S<4, 64, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              2,              2,      true,               7,               1>
        // clang-format on
        >;

void add_device_gemm_xdl_f64_f64_f64_km_kn_mn_instances(
    std::vector<std::unique_ptr<
        DeviceGemm<Col, Row, Row, F64, F64, F64, PassThrough, PassThrough, PassThrough>>>&
        instances)
{
    add_device_operation_instances(instances, device_gemm_xdl_f64_f64_f64_km_kn_mn_instances{});
}

} // namespace instance
} // namespace device
} // namespace tensor_operation
} // namespace ck

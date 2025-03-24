// SPDX-License-Identifier: MIT
// Copyright (c) 2018-2023, Advanced Micro Devices, Inc. All rights reserved.

#include <cstdlib>

#include "ck/ck.hpp"
#include "ck/tensor_operation/gpu/device/tensor_layout.hpp"
#include "ck/tensor_operation/gpu/device/gemm_specialization.hpp"
#include "ck/tensor_operation/gpu/device/device_batched_gemm_multi_d.hpp"
#include "ck/tensor_operation/gpu/device/impl/device_batched_gemm_multiple_d_dl.hpp"
#include "ck/library/tensor_operation_instance/add_device_operation_instance.hpp"

namespace ck {
namespace tensor_operation {
namespace device {
namespace instance {

using F16 = ck::half_t;
using F32 = float;

using Row = ck::tensor_layout::gemm::RowMajor;
using Col = ck::tensor_layout::gemm::ColumnMajor;

template <ck::index_t... Is>
using S = ck::Sequence<Is...>;

using PassThrough = ck::tensor_operation::element_wise::PassThrough;
using Empty_Tuple = ck::Tuple<>;

static constexpr auto GemmDefault = ck::tensor_operation::device::GemmSpecialization::Default;

// Compilation parameters for a[k, m] * b[k, n] = c[m, n]
using device_batched_gemm_multi_d_dl_f16_f16_f16_gkm_gkn_gmn_instances = std::tuple<
    // clang-format off
        // ##########################| ALayout| BLayout|    DsLayout| CLayout| AData| BData| AccData|      DsData| CData|           A|           B|           C|           GEMM| Block|  MPer|  NPer| K0Per| K1|      M1Per|      N1Per|   KPer|  M11N11Thread|  M11N11Thread|     ABlockTransfer|       ABlockTransfer| ABlockTransfer| ABlockTransfer|      ABlockTransfer|     ABlockTransfer|       ABlockTransfer|     BBlockTransfer|       BBlockTransfer| BBlockTransfer| BBlockTransfer|      BBlockTransfer|     BBlockTransfer|       BBlockTransfer|     CThreadTransfer|  CThreadTransfer|    CThreadTransfer|
        // ##########################|        |        |            |        |  Type|  Type|    Type|        Type|  Type| Elementwise| Elementwise| Elementwise| Specialization|  Size| Block| Block| Block|   | ThreadM111| ThreadN111| Thread| ClusterM110Xs| ClusterN110Xs| ThreadSliceLengths| ThreadClusterLengths|  ThreadCluster|      SrcAccess|     SrcVectorTensor|    SrcVectorTensor|      DstVectorTensor| ThreadSliceLengths| ThreadClusterLengths|  ThreadCluster|      SrcAccess|     SrcVectorTensor|    SrcVectorTensor|      DstVectorTensor|        SrcDstAccess|  SrcDstVectorDim| DstScalarPerVector|
        // ##########################|        |        |            |        |      |      |        |            |      |   Operation|   Operation|   Operation|               |      |      |      |      |   |           |           |       |              |              |        K0_M0_M1_K1|          K0_M0_M1_K1|   ArrangeOrder|          Order| Lengths_K0_M0_M1_K1| ContiguousDimOrder|  Lengths_K0_M0_M1_K1|        K0_M0_M1_K1|          K0_M0_M1_K1|   ArrangeOrder|          Order| Lengths_K0_M0_M1_K1| ContiguousDimOrder|  Lengths_K0_M0_M1_K1|               Order|                 |                   |
        // ##########################|        |        |            |        |      |      |        |            |      |            |            |            |               |      |      |      |      |   |           |           |       |              |              |                   |                     |               |               |                    |                   |                     |                   |                     |               |               |                    |                   |                     |                    |                 |                   |
        // MPerBlock=128, NPerBlock=128
        DeviceBatchedGemmMultipleD_Dl<     Col,     Row, Empty_Tuple,     Row,   F16,   F16,     F32, Empty_Tuple, F16, PassThrough, PassThrough, PassThrough,    GemmDefault,   256,   128,   128,    16,  2,          4,          4,      1,       S<8, 2>,       S<8, 2>,      S<2, 1, 4, 2>,       S<8, 1, 32, 1>,  S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>,      S<2, 1, 4, 2>,       S<8, 1, 32, 1>,  S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>, S<0, 1, 2, 3, 4, 5>,                5,                  4>,
        DeviceBatchedGemmMultipleD_Dl<     Col,     Row, Empty_Tuple,     Row,   F16,   F16,     F32, Empty_Tuple, F16, PassThrough, PassThrough, PassThrough,    GemmDefault,   256,   128,   128,    16,  2,          4,          4,      1,       S<4, 4>,       S<4, 4>,      S<2, 1, 4, 2>,       S<8, 1, 32, 1>,  S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>,      S<2, 1, 4, 2>,       S<8, 1, 32, 1>,  S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>, S<0, 1, 2, 3, 4, 5>,                5,                  4>,
        DeviceBatchedGemmMultipleD_Dl<     Col,     Row, Empty_Tuple,     Row,   F16,   F16,     F32, Empty_Tuple, F16, PassThrough, PassThrough, PassThrough,    GemmDefault,   256,   128,   128,    16,  2,          4,          4,      1,       S<2, 8>,       S<2, 8>,      S<2, 1, 4, 2>,       S<8, 1, 32, 1>,  S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>,      S<2, 1, 4, 2>,       S<8, 1, 32, 1>,  S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>, S<0, 1, 2, 3, 4, 5>,                5,                  4>,
        // MPerBlock=128, NPerBlock=64
        DeviceBatchedGemmMultipleD_Dl<     Col,     Row, Empty_Tuple,     Row,   F16,   F16,     F32, Empty_Tuple, F16, PassThrough, PassThrough, PassThrough,    GemmDefault,   128,   128,    64,    16,  2,          4,          4,      1,       S<8, 2>,       S<4, 2>,      S<2, 1, 8, 2>,       S<8, 1, 16, 1>,  S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>,      S<2, 1, 8, 2>,        S<8, 1, 8, 1>,  S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>, S<0, 1, 2, 3, 4, 5>,                5,                  4>,
        DeviceBatchedGemmMultipleD_Dl<     Col,     Row, Empty_Tuple,     Row,   F16,   F16,     F32, Empty_Tuple, F16, PassThrough, PassThrough, PassThrough,    GemmDefault,   128,   128,    64,    16,  2,          4,          4,      1,       S<2, 8>,       S<2, 4>,      S<2, 1, 8, 2>,       S<8, 1, 16, 1>,  S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>,      S<2, 1, 8, 2>,        S<8, 1, 8, 1>,  S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>, S<0, 1, 2, 3, 4, 5>,                5,                  4>,
        // MPerBlock=64, NPerBlock=128
        DeviceBatchedGemmMultipleD_Dl<     Col,     Row, Empty_Tuple,     Row,   F16,   F16,     F32, Empty_Tuple, F16, PassThrough, PassThrough, PassThrough,    GemmDefault,   128,    64,   128,    16,  2,          4,          4,      1,       S<4, 2>,       S<8, 2>,      S<2, 1, 8, 2>,        S<8, 1, 8, 1>,  S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>,      S<2, 1, 8, 2>,       S<8, 1, 16, 1>,  S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>, S<0, 1, 2, 3, 4, 5>,                5,                  4>,
        DeviceBatchedGemmMultipleD_Dl<     Col,     Row, Empty_Tuple,     Row,   F16,   F16,     F32, Empty_Tuple, F16, PassThrough, PassThrough, PassThrough,    GemmDefault,   128,    64,   128,    16,  2,          4,          4,      1,       S<2, 4>,       S<2, 8>,      S<2, 1, 8, 2>,        S<8, 1, 8, 1>,  S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>,      S<2, 1, 8, 2>,       S<8, 1, 16, 1>,  S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>, S<0, 1, 2, 3, 4, 5>,                5,                  4>,
        // MPerBlock=64, NPerBlock=64
        DeviceBatchedGemmMultipleD_Dl<     Col,     Row, Empty_Tuple,     Row,   F16,   F16,     F32, Empty_Tuple, F16, PassThrough, PassThrough, PassThrough,    GemmDefault,    64,    64,    64,     8,  2,          4,          4,      1,       S<4, 2>,       S<4, 2>,      S<2, 1, 4, 2>,       S<4, 1, 16, 1>,  S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>,      S<2, 1, 4, 2>,       S<4, 1, 16, 1>,  S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>, S<0, 1, 2, 3, 4, 5>,                5,                  4>,
        DeviceBatchedGemmMultipleD_Dl<     Col,     Row, Empty_Tuple,     Row,   F16,   F16,     F32, Empty_Tuple, F16, PassThrough, PassThrough, PassThrough,    GemmDefault,    64,    64,    64,     8,  2,          4,          4,      1,       S<2, 4>,       S<2, 4>,      S<2, 1, 4, 2>,       S<4, 1, 16, 1>,  S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>,      S<2, 1, 4, 2>,       S<4, 1, 16, 1>,  S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>, S<0, 1, 2, 3, 4, 5>,                5,                  4>,
        DeviceBatchedGemmMultipleD_Dl<     Col,     Row, Empty_Tuple,     Row,   F16,   F16,     F32, Empty_Tuple, F16, PassThrough, PassThrough, PassThrough,    GemmDefault,    64,    64,    64,     8,  2,          4,          4,      1,       S<8, 1>,       S<4, 2>,      S<2, 1, 4, 2>,       S<4, 1, 16, 1>,  S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>,      S<2, 1, 4, 2>,       S<4, 1, 16, 1>,  S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>, S<0, 1, 2, 3, 4, 5>,                5,                  4>,
        DeviceBatchedGemmMultipleD_Dl<     Col,     Row, Empty_Tuple,     Row,   F16,   F16,     F32, Empty_Tuple, F16, PassThrough, PassThrough, PassThrough,    GemmDefault,    64,    64,    64,     8,  2,          4,          4,      1,       S<4, 2>,       S<8, 1>,      S<2, 1, 4, 2>,       S<4, 1, 16, 1>,  S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>,      S<2, 1, 4, 2>,       S<4, 1, 16, 1>,  S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>, S<0, 1, 2, 3, 4, 5>,                5,                  4>,
        // MPerBlock=16, NPerBlock=64
        DeviceBatchedGemmMultipleD_Dl<     Col,     Row, Empty_Tuple,     Row,   F16,   F16,     F32, Empty_Tuple, F16, PassThrough, PassThrough, PassThrough,    GemmDefault,    64,    16,    64,    16,  2,          1,          4,      1,       S<4, 2>,       S<4, 2>,      S<1, 1, 4, 2>,       S<16, 1, 4, 1>,  S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>,     S<4, 1, 4, 2>,       S<4, 1, 16, 1>,   S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>, S<0, 1, 2, 3, 4, 5>,                5,                  4>,
        // MPerBlock=64, NPerBlock=16
        DeviceBatchedGemmMultipleD_Dl<     Col,     Row, Empty_Tuple,     Row,   F16,   F16,     F32, Empty_Tuple, F16, PassThrough, PassThrough, PassThrough,    GemmDefault,    64,    64,    16,    16,  2,          4,          1,      1,       S<4, 2>,       S<4, 2>,      S<4, 1, 4, 2>,       S<4, 1, 16, 1>,  S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>,     S<1, 1, 4, 2>,       S<16, 1, 4, 1>,   S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>, S<0, 1, 2, 3, 4, 5>,                5,                  1>,
        // MPerBlock=16, NPerBlock=16
        DeviceBatchedGemmMultipleD_Dl<     Col,     Row, Empty_Tuple,     Row,   F16,   F16,     F32, Empty_Tuple, F16, PassThrough, PassThrough, PassThrough,    GemmDefault,    16,    16,    16,    16,  2,          2,          2,      1,       S<2, 2>,       S<2, 2>,      S<4, 1, 4, 2>,        S<4, 1, 4, 1>,  S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>,     S<4, 1, 4, 2>,        S<4, 1, 4, 1>,   S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>, S<0, 1, 2, 3, 4, 5>,                5,                  2>,
        DeviceBatchedGemmMultipleD_Dl<     Col,     Row, Empty_Tuple,     Row,   F16,   F16,     F32, Empty_Tuple, F16, PassThrough, PassThrough, PassThrough,    GemmDefault,    16,    16,    16,    16,  2,          2,          2,      1,       S<1, 4>,       S<1, 4>,      S<4, 1, 4, 2>,        S<4, 1, 4, 1>,  S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>,     S<4, 1, 4, 2>,        S<4, 1, 4, 1>,   S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>, S<0, 1, 2, 3, 4, 5>,                5,                  2>,
        // MPerBlock=8, NPerBlock=64
        DeviceBatchedGemmMultipleD_Dl<     Col,     Row, Empty_Tuple,     Row,   F16,   F16,     F32, Empty_Tuple, F16, PassThrough, PassThrough, PassThrough,    GemmDefault,    64,     8,    64,    32,  2,          1,          2,      1,       S<4, 1>,       S<8, 2>,      S<1, 1, 4, 2>,       S<32, 1, 2, 1>,  S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>,     S<8, 1, 4, 2>,       S<4, 1, 16, 1>,   S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>, S<0, 1, 2, 3, 4, 5>,                5,                  2>,
        DeviceBatchedGemmMultipleD_Dl<     Col,     Row, Empty_Tuple,     Row,   F16,   F16,     F32, Empty_Tuple, F16, PassThrough, PassThrough, PassThrough,    GemmDefault,    64,     8,    64,    32,  2,          1,          2,      1,       S<2, 2>,       S<8, 2>,      S<1, 1, 4, 2>,       S<32, 1, 2, 1>,  S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>,     S<8, 1, 4, 2>,       S<4, 1, 16, 1>,   S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>, S<0, 1, 2, 3, 4, 5>,                5,                  2>,
        // MPerBlock=64, NPerBlock=8
        DeviceBatchedGemmMultipleD_Dl<     Col,     Row, Empty_Tuple,     Row,   F16,   F16,     F32, Empty_Tuple, F16, PassThrough, PassThrough, PassThrough,    GemmDefault,    64,    64,     8,    32,  2,          2,          1,      1,       S<8, 2>,       S<4, 1>,      S<8, 1, 4, 2>,       S<4, 1, 16, 1>,  S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>,     S<1, 1, 4, 2>,       S<32, 1, 2, 1>,   S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>, S<0, 1, 2, 3, 4, 5>,                5,                  1>,
        DeviceBatchedGemmMultipleD_Dl<     Col,     Row, Empty_Tuple,     Row,   F16,   F16,     F32, Empty_Tuple, F16, PassThrough, PassThrough, PassThrough,    GemmDefault,    64,    64,     8,    32,  2,          2,          1,      1,       S<8, 2>,       S<2, 2>,      S<8, 1, 4, 2>,       S<4, 1, 16, 1>,  S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>,     S<1, 1, 4, 2>,       S<32, 1, 2, 1>,   S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>, S<0, 1, 2, 3, 4, 5>,                5,                  1>,
        // MPerBlock=8, NPerBlock=8
        DeviceBatchedGemmMultipleD_Dl<     Col,     Row, Empty_Tuple,     Row,   F16,   F16,     F32, Empty_Tuple, F16, PassThrough, PassThrough, PassThrough,    GemmDefault,     8,     8,     8,     4,  2,          1,          2,      1,       S<4, 1>,       S<2, 1>,      S<1, 1, 4, 2>,        S<4, 1, 2, 1>,  S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>,     S<1, 1, 4, 2>,        S<4, 1, 2, 1>,   S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>, S<0, 1, 2, 3, 4, 5>,                5,                  2>,
        DeviceBatchedGemmMultipleD_Dl<     Col,     Row, Empty_Tuple,     Row,   F16,   F16,     F32, Empty_Tuple, F16, PassThrough, PassThrough, PassThrough,    GemmDefault,     8,     8,     8,     4,  2,          1,          2,      1,       S<1, 4>,       S<1, 2>,      S<1, 1, 4, 2>,        S<4, 1, 2, 1>,  S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>,     S<1, 1, 4, 2>,        S<4, 1, 2, 1>,   S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>, S<0, 1, 2, 3, 4, 5>,                5,                  2>,
        DeviceBatchedGemmMultipleD_Dl<     Col,     Row, Empty_Tuple,     Row,   F16,   F16,     F32, Empty_Tuple, F16, PassThrough, PassThrough, PassThrough,    GemmDefault,     8,     8,     8,     4,  2,          2,          1,      1,       S<2, 1>,       S<4, 1>,      S<1, 1, 4, 2>,        S<4, 1, 2, 1>,  S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>,     S<1, 1, 4, 2>,        S<4, 1, 2, 1>,   S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>, S<0, 1, 2, 3, 4, 5>,                5,                  1>,
        DeviceBatchedGemmMultipleD_Dl<     Col,     Row, Empty_Tuple,     Row,   F16,   F16,     F32, Empty_Tuple, F16, PassThrough, PassThrough, PassThrough,    GemmDefault,     8,     8,     8,     4,  2,          2,          1,      1,       S<1, 2>,       S<1, 4>,      S<1, 1, 4, 2>,        S<4, 1, 2, 1>,  S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>,     S<1, 1, 4, 2>,        S<4, 1, 2, 1>,   S<0, 3, 1, 2>,  S<0, 3, 1, 2>,       S<1, 1, 4, 1>,      S<0, 3, 1, 2>,        S<1, 1, 4, 2>, S<0, 1, 2, 3, 4, 5>,                5,                  1>
    // clang-format on
    >;

void add_device_batched_gemm_multi_d_dl_f16_f16_f16_gkm_gkn_gmn_instances(
    std::vector<std::unique_ptr<DeviceBatchedGemmMultiD<Col,
                                                        Row,
                                                        Empty_Tuple,
                                                        Row,
                                                        F16,
                                                        F16,
                                                        Empty_Tuple,
                                                        F16,
                                                        PassThrough,
                                                        PassThrough,
                                                        PassThrough>>>& instances)
{
    add_device_operation_instances(
        instances, device_batched_gemm_multi_d_dl_f16_f16_f16_gkm_gkn_gmn_instances{});
}

} // namespace instance
} // namespace device
} // namespace tensor_operation
} // namespace ck

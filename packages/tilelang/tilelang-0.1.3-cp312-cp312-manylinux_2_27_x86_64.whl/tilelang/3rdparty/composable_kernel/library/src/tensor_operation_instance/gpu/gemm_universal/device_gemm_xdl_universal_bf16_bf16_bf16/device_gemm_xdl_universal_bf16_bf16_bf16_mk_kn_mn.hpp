// SPDX-License-Identifier: MIT
// Copyright (c) 2018-2023, Advanced Micro Devices, Inc. All rights reserved.

#include "ck/ck.hpp"
#include "ck/tensor_operation/gpu/device/tensor_layout.hpp"
#include "ck/tensor_operation/gpu/device/gemm_specialization.hpp"
#include "ck/tensor_operation/gpu/device/impl/device_gemm_xdl_cshuffle_v3.hpp"

#include "ck/library/tensor_operation_instance/add_device_operation_instance.hpp"

namespace ck {
namespace tensor_operation {
namespace device {
namespace instance {

using BF16 = bhalf_t;
using F32  = float;

using Row = tensor_layout::gemm::RowMajor;
using Col = tensor_layout::gemm::ColumnMajor;

template <index_t... Is>
using S = Sequence<Is...>;

using PassThrough = element_wise::PassThrough;

static constexpr auto GemmDefault    = GemmSpecialization::Default;
static constexpr auto GemmKPadding   = GemmSpecialization::KPadding;
static constexpr auto GemmMPadding   = GemmSpecialization::MPadding;
static constexpr auto GemmMNPadding  = GemmSpecialization::MNPadding;
static constexpr auto GemmMKPadding  = GemmSpecialization::MKPadding;
static constexpr auto GemmMNKPadding = GemmSpecialization::MNKPadding;

static constexpr auto Intrawave = BlockGemmPipelineScheduler::Intrawave;
static constexpr auto Interwave = BlockGemmPipelineScheduler::Interwave;

template <GemmSpecialization GemmSpec>
using device_gemm_xdl_universal_bf16_bf16_bf16_mk_kn_mn_comp_instances = std::tuple<
    // clang-format off
        //#########################| ALayout| BLayout| CLayout|AData| BData| CData| AccData| Cshuffle|           A|           B|           C|          GEMM| Block|  MPer|  NPer|  KPer| AK1| BK1|MPer| NPer| MXdl| NXdl|  ABlockTransfer| ABlockTransfer| ABlockTransfer| ABlockTransfer| ABlockTransfer| ABlockTransfer| ABlockLds|  BBlockTransfer| BBlockTransfer| BBlockTransfer| BlockTransfer| BBlockTransfer| BBlockTransfer| BBlockLds|    CShuffle|    CShuffle|     CBlockTransferClusterLengths|  CBlockTransfer|                         Block-wiseGemm|               Block-wiseGemm|
        //#########################|        |        |        | Type|  Type|  Type|    Type|     Type| Elementwise| Elementwise| Elementwise|Specialization|  Size| Block| Block| Block|    |    | XDL|  XDL|  Per|  Per|   ThreadCluster|  ThreadCluster| SrcAccessOrder|   SrcVectorDim|      SrcScalar|      DstScalar| AddExtraM|   ThreadCluster|  ThreadCluster| SrcAccessOrder|  SrcVectorDim|      SrcScalar|      DstScalar| AddExtraN| MXdlPerWave| NXdlPerWave| _MBlock_MXdlPerWave_MWaveMPerXdl| ScalarPerVector|                               Pipeline|                     Pipeline|
        //#########################|        |        |        |     |      |      |        |         |   Operation|   Operation|   Operation|              |      |      |      |      |    |    |    |     | Wave| Wave| Lengths_K0_M_K1|   ArrangeOrder|               |               |      PerVector|   PerVector_K1|          | Lengths_K0_N_K1|   ArrangeOrder|               |              |      PerVector|   PerVector_K1|          |  PerShuffle|  PerShuffle| _NBlock_NXdlPerWave_NWaveNPerXdl|   _NWaveNPerXdl|                              Scheduler|                     Verision|
        //#########################|        |        |        |     |      |      |        |         |            |            |            |              |      |      |      |      |    |    |    |     |     |     |                |               |               |               |               |               |          |                |               |               |              |               |               |          |            |            |                                 |                |                                       |                             |
        
        DeviceGemm_Xdl_CShuffleV3<  Row,     Row,     Row,     BF16,   BF16,  BF16,   F32,     BF16,      PassThrough, PassThrough, PassThrough,       GemmSpec,   256,   256,   256,    32,   8,   4,  32,   32,    4,    4,     S<4, 64, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,              8,              8,          0,    S<8, 32, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              8,              4,          0,          1,           1,                   S<1, 16, 1, 16>,               4,  BlockGemmPipelineScheduler::Intrawave, BlockGemmPipelineVersion::v4>,
        DeviceGemm_Xdl_CShuffleV3<  Row,     Row,     Row,     BF16,   BF16,  BF16,   F32,     BF16,      PassThrough, PassThrough, PassThrough,       GemmSpec,   256,   256,   256,    32,   4,   4,  32,   32,    4,    4,     S<8, 32, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,              4,              4,          0,    S<8, 32, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              8,              4,          0,          1,           1,                   S<1, 16, 1, 16>,               4,  BlockGemmPipelineScheduler::Intrawave, BlockGemmPipelineVersion::v4>,
        DeviceGemm_Xdl_CShuffleV3<  Row,     Row,     Row,     BF16,   BF16,  BF16,   F32,     BF16,      PassThrough, PassThrough, PassThrough,       GemmSpec,   256,   256,   256,    32,   2,   2,  32,   32,    4,    4,     S<16,16, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,              2,              2,          0,    S<16,16, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              2,              2,          0,          1,           1,                   S<1, 16, 1, 16>,               4,  BlockGemmPipelineScheduler::Intrawave, BlockGemmPipelineVersion::v4>,
        DeviceGemm_Xdl_CShuffleV3<  Row,     Row,     Row,     BF16,   BF16,  BF16,   F32,     BF16,      PassThrough, PassThrough, PassThrough,       GemmSpec,   256,   128,   128,    64,   8,   4,  32,   32,    2,    2,     S<8, 32, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,              8,              8,          0,    S<16, 16, 1>,    S<0, 2, 1>,     S<0, 2, 1>,             1,              8,              4,          0,          1,           1,                   S<1, 16, 1, 16>,               4,  BlockGemmPipelineScheduler::Intrawave, BlockGemmPipelineVersion::v4>,
        DeviceGemm_Xdl_CShuffleV3<  Row,     Row,     Row,     BF16,   BF16,  BF16,   F32,     BF16,      PassThrough, PassThrough, PassThrough,       GemmSpec,   256,   256,   256,    32,   8,   4,  32,   32,    4,    4,     S<4, 64, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,              8,              8,          0,    S<8, 32, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              8,              4,          0,          1,           1,                   S<1, 16, 1, 16>,               4,  BlockGemmPipelineScheduler::Intrawave, BlockGemmPipelineVersion::v5>,
        DeviceGemm_Xdl_CShuffleV3<  Row,     Row,     Row,     BF16,   BF16,  BF16,   F32,     BF16,      PassThrough, PassThrough, PassThrough,       GemmSpec,   256,   256,   256,    32,   8,   4,  32,   32,    4,    4,     S<4, 64, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,              8,              8,          0,    S<8, 32, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              8,              4,          0,          1,           1,                   S<1, 16, 1, 16>,               4,  BlockGemmPipelineScheduler::Intrawave, BlockGemmPipelineVersion::v3>,
        DeviceGemm_Xdl_CShuffleV3<  Row,     Row,     Row,     BF16,   BF16,  BF16,   F32,     BF16,      PassThrough, PassThrough, PassThrough,       GemmSpec,   256,   224,   256,    64,   8,   8,  16,   16,    7,    8,     S<8, 32, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,              8,              8,          0,    S<8, 32, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              8,              8,          0,          1,           2,                   S<1, 16, 1, 16>,               4,  BlockGemmPipelineScheduler::Intrawave, BlockGemmPipelineVersion::v3>,
        DeviceGemm_Xdl_CShuffleV3<  Row,     Row,     Row,     BF16,   BF16,  BF16,   F32,     BF16,      PassThrough, PassThrough, PassThrough,       GemmSpec,   256,   128,   128,    64,   8,   4,  32,   32,    2,    2,     S<8, 32, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,              8,              8,          0,    S<16, 16, 1>,    S<0, 2, 1>,     S<0, 2, 1>,             1,              8,              4,          0,          1,           1,                   S<1, 16, 1, 16>,               4,  BlockGemmPipelineScheduler::Intrawave, BlockGemmPipelineVersion::v3>,
        DeviceGemm_Xdl_CShuffleV3<  Row,     Row,     Row,     BF16,   BF16,  BF16,   F32,     BF16,      PassThrough, PassThrough, PassThrough,       GemmSpec,   256,   128,   128,    64,   8,   4,  32,   32,    2,    2,     S<8, 32, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,              8,              8,          0,    S<16, 16, 1>,    S<0, 2, 1>,     S<0, 2, 1>,             1,              8,              4,          0,          1,           1,                   S<1, 16, 1, 16>,               4,  BlockGemmPipelineScheduler::Intrawave, BlockGemmPipelineVersion::v5>,
        DeviceGemm_Xdl_CShuffleV3<  Row,     Row,     Row,     BF16,   BF16,  BF16,   F32,     BF16,      PassThrough, PassThrough, PassThrough,       GemmSpec,   256,   128,   128,    64,   8,   4,  32,   32,    2,    2,     S<8, 32, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,              8,              8,          0,    S<16, 16, 1>,    S<0, 2, 1>,     S<0, 2, 1>,             1,              8,              4,          0,          1,           1,                   S<1, 16, 1, 16>,               4,  BlockGemmPipelineScheduler::Interwave, BlockGemmPipelineVersion::v1>
    // clang-format on
    >;

template <BlockGemmPipelineScheduler BlkGemmPipeSched, GemmSpecialization GemmSpec>
using device_gemm_xdl_universal_bf16_bf16_bf16_mk_kn_mn_mem_instances = std::tuple<
    // clang-format off
        //#########################| ALayout| BLayout| CLayout|AData| BData| CData| AccData| Cshuffle|           A|           B|           C|          GEMM| Block|  MPer|  NPer|  KPer| AK1| BK1|MPer| NPer| MXdl| NXdl|  ABlockTransfer| ABlockTransfer| ABlockTransfer| ABlockTransfer| ABlockTransfer| ABlockTransfer| ABlockLds|  BBlockTransfer| BBlockTransfer| BBlockTransfer| BlockTransfer| BBlockTransfer| BBlockTransfer| BBlockLds|    CShuffle|    CShuffle|     CBlockTransferClusterLengths|  CBlockTransfer|    Block-wiseGemm|               Block-wiseGemm|
        //#########################|        |        |        | Type|  Type|  Type|    Type|     Type| Elementwise| Elementwise| Elementwise|Specialization|  Size| Block| Block| Block|    |    | XDL|  XDL|  Per|  Per|   ThreadCluster|  ThreadCluster| SrcAccessOrder|   SrcVectorDim|      SrcScalar|      DstScalar| AddExtraM|   ThreadCluster|  ThreadCluster| SrcAccessOrder|  SrcVectorDim|      SrcScalar|      DstScalar| AddExtraN| MXdlPerWave| NXdlPerWave| _MBlock_MXdlPerWave_MWaveMPerXdl| ScalarPerVector|          Pipeline|                     Pipeline|
        //#########################|        |        |        |     |      |      |        |         |   Operation|   Operation|   Operation|              |      |      |      |      |    |    |    |     | Wave| Wave| Lengths_K0_M_K1|   ArrangeOrder|               |               |      PerVector|   PerVector_K1|          | Lengths_K0_N_K1|   ArrangeOrder|               |              |      PerVector|   PerVector_K1|          |  PerShuffle|  PerShuffle| _NBlock_NXdlPerWave_NWaveNPerXdl|   _NWaveNPerXdl|         Scheduler|                     Verision|
        //#########################|        |        |        |     |      |      |        |         |            |            |            |              |      |      |      |      |    |    |    |     |     |     |                |               |               |               |               |               |          |                |               |               |              |               |               |          |            |            |                                 |                |                  |                             |

        // Latency friendly
        DeviceGemm_Xdl_CShuffleV3<  Row,     Row,     Row,     BF16,   BF16,  BF16,   F32,     BF16,      PassThrough, PassThrough, PassThrough,       GemmSpec,   128,    32,   16,    64,   8,   4,  16,   16,    1,    1,     S<8, 16, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,              8,              8,          0,    S<16, 8, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              2,              4,          0,          1,           1,                   S<1, 16, 1, 8>,               2,  BlkGemmPipeSched, BlockGemmPipelineVersion::v1>,
        DeviceGemm_Xdl_CShuffleV3<  Row,     Row,     Row,     BF16,   BF16,  BF16,   F32,     BF16,      PassThrough, PassThrough, PassThrough,       GemmSpec,   128,    32,   16,    64,   4,   4,  16,   16,    1,    1,     S<16, 8, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,              4,              4,          0,    S<16, 8, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              2,              4,          0,          1,           1,                   S<1, 16, 1, 8>,               2,  BlkGemmPipeSched, BlockGemmPipelineVersion::v1>,
        DeviceGemm_Xdl_CShuffleV3<  Row,     Row,     Row,     BF16,   BF16,  BF16,   F32,     BF16,      PassThrough, PassThrough, PassThrough,       GemmSpec,   128,    32,   16,    64,   2,   2,  16,   16,    1,    1,     S<32, 4, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,              2,              2,          0,    S<32, 4, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              2,              2,          0,          1,           1,                   S<1, 16, 1, 8>,               2,  BlkGemmPipeSched, BlockGemmPipelineVersion::v1>,
        DeviceGemm_Xdl_CShuffleV3<  Row,     Row,     Row,     BF16,   BF16,  BF16,   F32,     BF16,      PassThrough, PassThrough, PassThrough,       GemmSpec,    64,    16,   16,    64,   8,   4,  16,   16,    1,    1,     S<8,  8, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,              8,              8,          0,    S<16, 4, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              4,              4,          0,          1,           1,                   S<1, 16, 1, 4>,               4,  BlkGemmPipeSched, BlockGemmPipelineVersion::v1>,
        DeviceGemm_Xdl_CShuffleV3<  Row,     Row,     Row,     BF16,   BF16,  BF16,   F32,     BF16,      PassThrough, PassThrough, PassThrough,       GemmSpec,   128,    16,   32,    64,   8,   4,  16,   16,    1,    1,     S<8, 16, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,              8,              8,          0,    S<16, 8, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              4,              4,          0,          1,           1,                   S<1, 16, 1, 8>,               4,  BlkGemmPipeSched, BlockGemmPipelineVersion::v1>,
        // Memory friendly
        DeviceGemm_Xdl_CShuffleV3<  Row,     Row,     Row,     BF16,   BF16,  BF16,   F32,     BF16,      PassThrough, PassThrough, PassThrough,       GemmSpec,   256,   256,   16,    64,   8,   2,  16,   16,    4,    1,     S<8, 32, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,              8,              8,          0,    S<32, 8, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              2,              2,          0,          1,           1,                   S<1, 32, 1, 8>,               2,  BlkGemmPipeSched, BlockGemmPipelineVersion::v2>,
        DeviceGemm_Xdl_CShuffleV3<  Row,     Row,     Row,     BF16,   BF16,  BF16,   F32,     BF16,      PassThrough, PassThrough, PassThrough,       GemmSpec,   256,   256,   16,    64,   2,   2,  16,   16,    4,    1,     S<32, 8, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,              2,              2,          0,    S<32, 8, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              2,              2,          0,          1,           1,                   S<1, 32, 1, 8>,               2,  BlkGemmPipeSched, BlockGemmPipelineVersion::v2>,
        DeviceGemm_Xdl_CShuffleV3<  Row,     Row,     Row,     BF16,   BF16,  BF16,   F32,     BF16,      PassThrough, PassThrough, PassThrough,       GemmSpec,   128,   128,   16,    64,   8,   4,  16,   16,    4,    1,     S<8, 16, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,              8,              8,          0,    S<16, 8, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              2,              4,          0,          1,           1,                   S<1, 16, 1, 8>,               2,  BlkGemmPipeSched, BlockGemmPipelineVersion::v2>,
        DeviceGemm_Xdl_CShuffleV3<  Row,     Row,     Row,     BF16,   BF16,  BF16,   F32,     BF16,      PassThrough, PassThrough, PassThrough,       GemmSpec,   128,    64,   16,    64,   8,   4,  16,   16,    2,    1,     S<8, 16, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,              8,              8,          0,    S<16, 8, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              2,              4,          0,          1,           1,                   S<1, 16, 1, 8>,               2,  BlkGemmPipeSched, BlockGemmPipelineVersion::v2>,
        DeviceGemm_Xdl_CShuffleV3<  Row,     Row,     Row,     BF16,   BF16,  BF16,   F32,     BF16,      PassThrough, PassThrough, PassThrough,       GemmSpec,   128,    32,   16,    64,   8,   4,  16,   16,    1,    1,     S<8, 16, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,              8,              8,          0,    S<16, 8, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              2,              4,          0,          1,           1,                   S<1, 16, 1, 8>,               2,  BlkGemmPipeSched, BlockGemmPipelineVersion::v2>,
        DeviceGemm_Xdl_CShuffleV3<  Row,     Row,     Row,     BF16,   BF16,  BF16,   F32,     BF16,      PassThrough, PassThrough, PassThrough,       GemmSpec,    64,    16,   16,    64,   8,   4,  16,   16,    1,    1,     S<8,  8, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,              8,              8,          0,    S<16, 4, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              4,              4,          0,          1,           1,                   S<1, 16, 1, 4>,               4,  BlkGemmPipeSched, BlockGemmPipelineVersion::v2>,
        DeviceGemm_Xdl_CShuffleV3<  Row,     Row,     Row,     BF16,   BF16,  BF16,   F32,     BF16,      PassThrough, PassThrough, PassThrough,       GemmSpec,    64,    16,   16,    64,   4,   4,  16,   16,    1,    1,     S<16, 4, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,              4,              4,          0,    S<16, 4, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              4,              4,          0,          1,           1,                   S<1, 16, 1, 4>,               4,  BlkGemmPipeSched, BlockGemmPipelineVersion::v2>,
        DeviceGemm_Xdl_CShuffleV3<  Row,     Row,     Row,     BF16,   BF16,  BF16,   F32,     BF16,      PassThrough, PassThrough, PassThrough,       GemmSpec,   128,    16,   32,    64,   8,   4,  16,   16,    1,    1,     S<8, 16, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,              8,              8,          0,    S<16, 8, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              4,              4,          0,          1,           1,                   S<1, 16, 1, 8>,               4,  BlkGemmPipeSched, BlockGemmPipelineVersion::v2>,
        DeviceGemm_Xdl_CShuffleV3<  Row,     Row,     Row,     BF16,   BF16,  BF16,   F32,     BF16,      PassThrough, PassThrough, PassThrough,       GemmSpec,   128,    16,   64,    64,   8,   4,  16,   16,    1,    2,     S<8, 16, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,              8,              8,          0,    S<16, 8, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              8,              4,          0,          1,           1,                   S<1, 16, 1, 8>,               4,  BlkGemmPipeSched, BlockGemmPipelineVersion::v2>,
        DeviceGemm_Xdl_CShuffleV3<  Row,     Row,     Row,     BF16,   BF16,  BF16,   F32,     BF16,      PassThrough, PassThrough, PassThrough,       GemmSpec,   128,    16,  128,    64,   8,   4,  16,   16,    1,    4,     S<8, 16, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,              8,              8,          0,    S<8, 16, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              8,              4,          0,          1,           1,                   S<1, 16, 1, 8>,               4,  BlkGemmPipeSched, BlockGemmPipelineVersion::v2>,
        DeviceGemm_Xdl_CShuffleV3<  Row,     Row,     Row,     BF16,   BF16,  BF16,   F32,     BF16,      PassThrough, PassThrough, PassThrough,       GemmSpec,   256,    16,  256,    64,   8,   4,  16,   16,    1,    4,     S<8, 16, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,              8,              8,          0,    S<8, 32, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              8,              4,          0,          1,           1,                   S<1, 16, 1, 16>,              4,  BlkGemmPipeSched, BlockGemmPipelineVersion::v2>
    // clang-format on
    >;
} // namespace instance
} // namespace device
} // namespace tensor_operation
} // namespace ck

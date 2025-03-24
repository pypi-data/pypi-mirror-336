// SPDX-License-Identifier: MIT
// Copyright (c) 2024, Advanced Micro Devices, Inc. All rights reserved.

#include "ck/ck.hpp"
#include "ck/tensor_operation/gpu/device/tensor_layout.hpp"
#include "ck/tensor_operation/gpu/device/gemm_specialization.hpp"
#include "ck/tensor_operation/gpu/device/impl/device_gemm_multiple_d_xdl_cshuffle_v3.hpp"

#include "ck/library/tensor_operation_instance/add_device_operation_instance.hpp"

namespace ck {
namespace tensor_operation {
namespace device {
namespace instance {

using I8   = int8_t;
using I32  = int;
using BF16 = bhalf_t;
using F32  = float;

using Row = tensor_layout::gemm::RowMajor;
using Col = tensor_layout::gemm::ColumnMajor;

template <index_t... Is>
using S = Sequence<Is...>;

using PassThrough      = element_wise::PassThrough;
using MultiplyMultiply = element_wise::MultiplyMultiply;

static constexpr auto GemmDefault    = GemmSpecialization::Default;
static constexpr auto GemmKPadding   = GemmSpecialization::KPadding;
static constexpr auto GemmMNPadding  = GemmSpecialization::MNPadding;
static constexpr auto GemmMNKPadding = GemmSpecialization::MNKPadding;

static constexpr auto Intrawave = BlockGemmPipelineScheduler::Intrawave;
static constexpr auto Interwave = BlockGemmPipelineScheduler::Interwave;

template <GemmSpecialization GemmSpec>
using device_gemm_multiply_multiply_xdl_i8_i8_bf16_mk_nk_mn_comp_instances = std::tuple<
    // clang-format off
        //################################| ALayout| BLayout|         DsLayout| ELayout|AData| BData|          DsData| EData| AccData| Cshuffle|           A|           B|              C|          GEMM| Block|  MPer|  NPer|  KPer| AK1| BK1|MPer| NPer| MXdl| NXdl|  ABlockTransfer| ABlockTransfer| ABlockTransfer| ABlockTransfer| ABlockTransfer| ABlockTransfer| ABlockLds|  BBlockTransfer| BBlockTransfer| BBlockTransfer| BlockTransfer| BBlockTransfer| BBlockTransfer| BBlockLds|    CShuffle|    CShuffle|     CBlockTransferClusterLengths|  CBlockTransfer|                         Block-wiseGemm|               Block-wiseGemm|
        //################################|        |        |                 |        | Type|  Type|            Type|  Type|    Type|     Type| Elementwise| Elementwise|    Elementwise|Specialization|  Size| Block| Block| Block|    |    | XDL|  XDL|  Per|  Per|   ThreadCluster|  ThreadCluster| SrcAccessOrder|   SrcVectorDim|      SrcScalar|      DstScalar| AddExtraM|   ThreadCluster|  ThreadCluster| SrcAccessOrder|  SrcVectorDim|      SrcScalar|      DstScalar| AddExtraN| MXdlPerWave| NXdlPerWave| _MBlock_MXdlPerWave_MWaveMPerXdl| ScalarPerVector|                               Pipeline|                     Pipeline|
        //################################|        |        |                 |        |     |      |                |      |        |         |   Operation|   Operation|      Operation|              |      |      |      |      |    |    |    |     | Wave| Wave| Lengths_K0_M_K1|   ArrangeOrder|               |               |      PerVector|   PerVector_K1|          | Lengths_K0_N_K1|   ArrangeOrder|               |              |      PerVector|   PerVector_K1|          |  PerShuffle|  PerShuffle| _NBlock_NXdlPerWave_NWaveNPerXdl|   _NWaveNPerXdl|                              Scheduler|                     Verision|
        //################################|        |        |                 |        |     |      |                |      |        |         |            |            |               |              |      |      |      |      |    |    |    |     |     |     |                |               |               |               |               |               |          |                |               |               |              |               |               |          |            |            |                                 |                |                                       |                             |
        
        // Compute friendly
        DeviceGemmMultiD_Xdl_CShuffle_V3<  Row,     Col,     Tuple<Row, Col>,  Row,    I8,    I8,    Tuple<F32, F32>, BF16,  I32,     I32,     PassThrough, PassThrough, MultiplyMultiply,    GemmSpec,   256,   256,   256,    64,  16,  16,  32,   32,    4,    4,     S<4, 64, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,    S<4, 64, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,          1,           1,                   S<1, 32, 1, 8>,     S<8, 8, 1>,  BlockGemmPipelineScheduler::Intrawave, BlockGemmPipelineVersion::v4, I8>,
        DeviceGemmMultiD_Xdl_CShuffle_V3<  Row,     Col,     Tuple<Row, Col>,  Row,    I8,    I8,    Tuple<F32, F32>, BF16,  I32,     I32,     PassThrough, PassThrough, MultiplyMultiply,    GemmSpec,   256,   128,   128,   128,  16,  16,  32,   32,    2,    2,     S<8, 32, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,    S<8, 32, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,          1,           1,                   S<1, 32, 1, 8>,     S<8, 8, 1>,  BlockGemmPipelineScheduler::Intrawave, BlockGemmPipelineVersion::v4, I8>,
        DeviceGemmMultiD_Xdl_CShuffle_V3<  Row,     Col,     Tuple<Row, Col>,  Row,    I8,    I8,    Tuple<F32, F32>, BF16,  I32,     I32,     PassThrough, PassThrough, MultiplyMultiply,    GemmSpec,   256,   128,   128,    64,  16,  16,  32,   32,    2,    2,     S<4, 64, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,    S<4, 64, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,          1,           1,                   S<1, 32, 1, 8>,     S<8, 8, 1>,  BlockGemmPipelineScheduler::Intrawave, BlockGemmPipelineVersion::v4, I8>,
        DeviceGemmMultiD_Xdl_CShuffle_V3<  Row,     Col,     Tuple<Row, Col>,  Row,    I8,    I8,    Tuple<F32, F32>, BF16,  I32,     I32,     PassThrough, PassThrough, MultiplyMultiply,    GemmSpec,   256,   256,   256,   128,  16,  16,  16,   16,    8,    8,     S<8, 32, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,    S<8, 32, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,          1,           2,                   S<1, 32, 1, 8>,     S<8, 8, 1>,  BlockGemmPipelineScheduler::Intrawave, BlockGemmPipelineVersion::v3, I8>,
        DeviceGemmMultiD_Xdl_CShuffle_V3<  Row,     Col,     Tuple<Row, Col>,  Row,    I8,    I8,    Tuple<F32, F32>, BF16,  I32,     I32,     PassThrough, PassThrough, MultiplyMultiply,    GemmSpec,   256,   256,   256,    64,  16,  16,  16,   16,    8,    8,     S<4, 64, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,    S<4, 64, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,          1,           2,                   S<1, 32, 1, 8>,     S<8, 8, 1>,  BlockGemmPipelineScheduler::Intrawave, BlockGemmPipelineVersion::v3, I8>,
        DeviceGemmMultiD_Xdl_CShuffle_V3<  Row,     Col,     Tuple<Row, Col>,  Row,    I8,    I8,    Tuple<F32, F32>, BF16,  I32,     I32,     PassThrough, PassThrough, MultiplyMultiply,    GemmSpec,   256,   224,   256,    128, 16,  16,  16,   16,    7,    8,     S<8, 32, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,    S<8, 32, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,          1,           2,                   S<1, 32, 1, 8>,     S<8, 8, 1>,  BlockGemmPipelineScheduler::Intrawave, BlockGemmPipelineVersion::v3, I8>,
        DeviceGemmMultiD_Xdl_CShuffle_V3<  Row,     Col,     Tuple<Row, Col>,  Row,    I8,    I8,    Tuple<F32, F32>, BF16,  I32,     I32,     PassThrough, PassThrough, MultiplyMultiply,    GemmSpec,   256,   256,   224,    128, 16,  16,  16,   16,    8,    7,     S<8, 32, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,    S<8, 32, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,          2,           1,                   S<1, 64, 1, 4>,     S<8, 8, 1>,  BlockGemmPipelineScheduler::Intrawave, BlockGemmPipelineVersion::v3, I8>,
        DeviceGemmMultiD_Xdl_CShuffle_V3<  Row,     Col,     Tuple<Row, Col>,  Row,    I8,    I8,    Tuple<F32, F32>, BF16,  I32,     I32,     PassThrough, PassThrough, MultiplyMultiply,    GemmSpec,   256,   128,   128,    128, 16,  16,  32,   32,    2,    2,     S<8, 32, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,    S<8, 32, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,          1,           1,                   S<1, 32, 1, 8>,     S<8, 8, 1>,  BlockGemmPipelineScheduler::Intrawave, BlockGemmPipelineVersion::v3, I8>,
        DeviceGemmMultiD_Xdl_CShuffle_V3<  Row,     Col,     Tuple<Row, Col>,  Row,    I8,    I8,    Tuple<F32, F32>, BF16,  I32,     I32,     PassThrough, PassThrough, MultiplyMultiply,    GemmSpec,   256,   128,   128,    128, 16,  16,  32,   32,    2,    2,     S<8, 32, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,    S<8, 32, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,          1,           1,                   S<1, 32, 1, 8>,     S<8, 8, 1>,  BlockGemmPipelineScheduler::Intrawave, BlockGemmPipelineVersion::v5, I8>,
        DeviceGemmMultiD_Xdl_CShuffle_V3<  Row,     Col,     Tuple<Row, Col>,  Row,    I8,    I8,    Tuple<F32, F32>, BF16,  I32,     I32,     PassThrough, PassThrough, MultiplyMultiply,    GemmSpec,   256,   128,   256,    64,  16,  16,  32,   32,    2,    4,     S<4, 64, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,    S<4, 64, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,          1,           1,                   S<1, 32, 1, 8>,     S<8, 8, 1>,  BlockGemmPipelineScheduler::Interwave, BlockGemmPipelineVersion::v1, I8>,
        DeviceGemmMultiD_Xdl_CShuffle_V3<  Row,     Col,     Tuple<Row, Col>,  Row,    I8,    I8,    Tuple<F32, F32>, BF16,  I32,     I32,     PassThrough, PassThrough, MultiplyMultiply,    GemmSpec,   256,   256,   128,    64,  16,  16,  32,   32,    4,    2,     S<4, 64, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,    S<4, 64, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,          1,           1,                   S<1, 32, 1, 8>,     S<8, 8, 1>,  BlockGemmPipelineScheduler::Interwave, BlockGemmPipelineVersion::v1, I8>,
        DeviceGemmMultiD_Xdl_CShuffle_V3<  Row,     Col,     Tuple<Row, Col>,  Row,    I8,    I8,    Tuple<F32, F32>, BF16,  I32,     I32,     PassThrough, PassThrough, MultiplyMultiply,    GemmSpec,   256,   128,   128,    128, 16,  16,  32,   32,    2,    2,     S<8, 32, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,    S<8, 32, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,          1,           1,                   S<1, 32, 1, 8>,     S<8, 8, 1>,  BlockGemmPipelineScheduler::Interwave, BlockGemmPipelineVersion::v1, I8>,
        DeviceGemmMultiD_Xdl_CShuffle_V3<  Row,     Col,     Tuple<Row, Col>,  Row,    I8,    I8,    Tuple<F32, F32>, BF16,  I32,     I32,     PassThrough, PassThrough, MultiplyMultiply,    GemmSpec,   256,   128,    64,    128, 16,  16,  32,   32,    2,    1,     S<8, 32, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,    S<8, 32, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,          1,           1,                   S<1, 32, 1, 8>,     S<8, 8, 1>,  BlockGemmPipelineScheduler::Intrawave, BlockGemmPipelineVersion::v3, I8>,
        DeviceGemmMultiD_Xdl_CShuffle_V3<  Row,     Col,     Tuple<Row, Col>,  Row,    I8,    I8,    Tuple<F32, F32>, BF16,  I32,     I32,     PassThrough, PassThrough, MultiplyMultiply,    GemmSpec,   256,    64,   128,    128, 16,  16,  32,   32,    1,    2,     S<8, 32, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,    S<8, 32, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,          1,           1,                   S<1, 32, 1, 8>,     S<8, 8, 1>,  BlockGemmPipelineScheduler::Intrawave, BlockGemmPipelineVersion::v3, I8>,
        DeviceGemmMultiD_Xdl_CShuffle_V3<  Row,     Col,     Tuple<Row, Col>,  Row,    I8,    I8,    Tuple<F32, F32>, BF16,  I32,     I32,     PassThrough, PassThrough, MultiplyMultiply,    GemmSpec,   256,    64,    64,    128, 16,  16,  32,   32,    1,    1,     S<8, 32, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,    S<8, 32, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,          1,           1,                   S<1, 32, 1, 8>,     S<8, 8, 1>,  BlockGemmPipelineScheduler::Intrawave, BlockGemmPipelineVersion::v3, I8>
    // clang-format oI
    >;

template <BlockGemmPipelineScheduler BlkGemmPipeSched, GemmSpecialization GemmSpec>
using device_gemm_multiply_multiply_xdl_i8_i8_bf16_mk_nk_mn_mem_instances = std::tuple<
    // clang-format off
        //################################| ALayout| BLayout|         DsLayout| ELayout|AData| BData|          DsData| EData| AccData| Cshuffle|           A|           B|               C|          GEMM| Block|  MPer|  NPer|  KPer| AK1| BK1|MPer| NPer| MXdl| NXdl|  ABlockTransfer| ABlockTransfer| ABlockTransfer| ABlockTransfer| ABlockTransfer| ABlockTransfer| ABlockLds|  BBlockTransfer| BBlockTransfer| BBlockTransfer| BlockTransfer| BBlockTransfer| BBlockTransfer| BBlockLds|    CShuffle|    CShuffle|     CBlockTransferClusterLengths|  CBlockTransfer|    Block-wiseGemm|               Block-wiseGemm|
        //################################|        |        |                 |        | Type|  Type|            Type|  Type|    Type|     Type| Elementwise| Elementwise|     Elementwise|Specialization|  Size| Block| Block| Block|    |    | XDL|  XDL|  Per|  Per|   ThreadCluster|  ThreadCluster| SrcAccessOrder|   SrcVectorDim|      SrcScalar|      DstScalar| AddExtraM|   ThreadCluster|  ThreadCluster| SrcAccessOrder|  SrcVectorDim|      SrcScalar|      DstScalar| AddExtraN| MXdlPerWave| NXdlPerWave| _MBlock_MXdlPerWave_MWaveMPerXdl| ScalarPerVector|          Pipeline|                     Pipeline|
        //################################|        |        |                 |        |     |      |                |      |        |         |   Operation|   Operation|       Operation|              |      |      |      |      |    |    |    |     | Wave| Wave| Lengths_K0_M_K1|   ArrangeOrder|               |               |      PerVector|   PerVector_K1|          | Lengths_K0_N_K1|   ArrangeOrder|               |              |      PerVector|   PerVector_K1|          |  PerShuffle|  PerShuffle| _NBlock_NXdlPerWave_NWaveNPerXdl|   _NWaveNPerXdl|         Scheduler|                     Verision|
        //################################|        |        |                 |        |     |      |                |      |        |         |            |            |                |              |      |      |      |      |    |    |    |     |     |     |                |               |               |               |               |               |          |                |               |               |              |               |               |          |            |            |                                 |                |                  |                             |

        // Latency friendly 
        DeviceGemmMultiD_Xdl_CShuffle_V3<  Row,     Col,     Tuple<Row, Col>, Row,     I8,     I8,    Tuple<F32, F32>, BF16,   I32,     I32,  PassThrough, PassThrough, MultiplyMultiply,     GemmSpec,   128,    32,   16,    128, 16,  16,  16,   16,    1,    1,     S<8, 16, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,    S<8, 16, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,          1,           1,                   S<1, 16, 1, 8>,      S<2, 2, 1>,  BlkGemmPipeSched, BlockGemmPipelineVersion::v1, I8>,
        DeviceGemmMultiD_Xdl_CShuffle_V3<  Row,     Col,     Tuple<Row, Col>, Row,     I8,     I8,    Tuple<F32, F32>, BF16,   I32,     I32,  PassThrough, PassThrough, MultiplyMultiply,     GemmSpec,    64,    16,   16,    128, 16,  16,  16,   16,    1,    1,     S<8,  8, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,    S<8,  8, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,          1,           1,                   S<1, 16, 1, 4>,      S<4, 4, 1>,  BlkGemmPipeSched, BlockGemmPipelineVersion::v1, I8>,
        DeviceGemmMultiD_Xdl_CShuffle_V3<  Row,     Col,     Tuple<Row, Col>, Row,     I8,     I8,    Tuple<F32, F32>, BF16,   I32,     I32,  PassThrough, PassThrough, MultiplyMultiply,     GemmSpec,   128,    16,   32,    128, 16,  16,  16,   16,    1,    1,     S<8, 16, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,    S<8, 16, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,          1,           1,                   S<1, 16, 1, 8>,      S<4, 4, 1>,  BlkGemmPipeSched, BlockGemmPipelineVersion::v1, I8>,
        // Memory friendly
        DeviceGemmMultiD_Xdl_CShuffle_V3<  Row,     Col,     Tuple<Row, Col>, Row,     I8,     I8,    Tuple<F32, F32>, BF16,   I32,     I32,  PassThrough, PassThrough, MultiplyMultiply,     GemmSpec,   256,   256,   32,    128, 16,  16,  32,   32,    2,    1,     S<8, 32, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,    S<8, 32, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,          1,           1,                   S<1, 32, 1, 8>,     S<4, 4, 1>,  BlkGemmPipeSched, BlockGemmPipelineVersion::v2, I8>,
        DeviceGemmMultiD_Xdl_CShuffle_V3<  Row,     Col,     Tuple<Row, Col>, Row,     I8,     I8,    Tuple<F32, F32>, BF16,   I32,     I32,  PassThrough, PassThrough, MultiplyMultiply,     GemmSpec,   256,   256,   16,    128, 16,  16,  16,   16,    4,    1,     S<8, 32, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,    S<8, 16, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,          1,           1,                   S<1, 32, 1, 8>,     S<2, 2, 1>,  BlkGemmPipeSched, BlockGemmPipelineVersion::v2, I8>,
        DeviceGemmMultiD_Xdl_CShuffle_V3<  Row,     Col,     Tuple<Row, Col>, Row,     I8,     I8,    Tuple<F32, F32>, BF16,   I32,     I32,  PassThrough, PassThrough, MultiplyMultiply,     GemmSpec,   128,   128,   32,    128, 16,  16,  32,   32,    2,    1,     S<8, 16, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,    S<8, 16, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,          1,           1,                   S<1, 16, 1, 8>,     S<4, 4, 1>,  BlkGemmPipeSched, BlockGemmPipelineVersion::v2, I8>,
        DeviceGemmMultiD_Xdl_CShuffle_V3<  Row,     Col,     Tuple<Row, Col>, Row,     I8,     I8,    Tuple<F32, F32>, BF16,   I32,     I32,  PassThrough, PassThrough, MultiplyMultiply,     GemmSpec,   128,   128,   16,    128, 16,  16,  16,   16,    4,    1,     S<8, 16, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,    S<8, 16, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,          1,           1,                   S<1, 16, 1, 8>,     S<2, 2, 1>,  BlkGemmPipeSched, BlockGemmPipelineVersion::v2, I8>,
        DeviceGemmMultiD_Xdl_CShuffle_V3<  Row,     Col,     Tuple<Row, Col>, Row,     I8,     I8,    Tuple<F32, F32>, BF16,   I32,     I32,  PassThrough, PassThrough, MultiplyMultiply,     GemmSpec,   128,    64,   32,    128, 16,  16,  32,   32,    1,    1,     S<8, 16, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,    S<8, 16, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,          1,           1,                   S<1, 16, 1, 8>,     S<4, 4, 1>,  BlkGemmPipeSched, BlockGemmPipelineVersion::v2, I8>,
        DeviceGemmMultiD_Xdl_CShuffle_V3<  Row,     Col,     Tuple<Row, Col>, Row,     I8,     I8,    Tuple<F32, F32>, BF16,   I32,     I32,  PassThrough, PassThrough, MultiplyMultiply,     GemmSpec,   128,    64,   16,    128, 16,  16,  16,   16,    2,    1,     S<8, 16, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,    S<8, 16, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,          1,           1,                   S<1, 16, 1, 8>,     S<2, 2, 1>,  BlkGemmPipeSched, BlockGemmPipelineVersion::v2, I8>,
        DeviceGemmMultiD_Xdl_CShuffle_V3<  Row,     Col,     Tuple<Row, Col>, Row,     I8,     I8,    Tuple<F32, F32>, BF16,   I32,     I32,  PassThrough, PassThrough, MultiplyMultiply,     GemmSpec,   128,    32,   16,    128, 16,  16,  16,   16,    1,    1,     S<8, 16, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,    S<8, 16, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,          1,           1,                   S<1, 16, 1, 8>,     S<2, 2, 1>,  BlkGemmPipeSched, BlockGemmPipelineVersion::v2, I8>,
        DeviceGemmMultiD_Xdl_CShuffle_V3<  Row,     Col,     Tuple<Row, Col>, Row,     I8,     I8,    Tuple<F32, F32>, BF16,   I32,     I32,  PassThrough, PassThrough, MultiplyMultiply,     GemmSpec,    64,    16,   16,     64, 16,  16,  16,   16,    1,    1,     S<4, 16, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,    S<4, 16, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,          1,           1,                   S<1, 16, 1, 4>,     S<4, 4, 1>,  BlkGemmPipeSched, BlockGemmPipelineVersion::v2, I8>,
        DeviceGemmMultiD_Xdl_CShuffle_V3<  Row,     Col,     Tuple<Row, Col>, Row,     I8,     I8,    Tuple<F32, F32>, BF16,   I32,     I32,  PassThrough, PassThrough, MultiplyMultiply,     GemmSpec,    64,    16,   16,    128, 16,  16,  16,   16,    1,    1,     S<8,  8, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,    S<8,  8, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,          1,           1,                   S<1, 16, 1, 4>,     S<4, 4, 1>,  BlkGemmPipeSched, BlockGemmPipelineVersion::v2, I8>,
        DeviceGemmMultiD_Xdl_CShuffle_V3<  Row,     Col,     Tuple<Row, Col>, Row,     I8,     I8,    Tuple<F32, F32>, BF16,   I32,     I32,  PassThrough, PassThrough, MultiplyMultiply,     GemmSpec,   128,    16,   32,    128, 16,  16,  16,   16,    1,    1,     S<8, 16, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,    S<8, 16, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,          1,           1,                   S<1, 16, 1, 8>,     S<4, 4, 1>,  BlkGemmPipeSched, BlockGemmPipelineVersion::v2, I8>,
        DeviceGemmMultiD_Xdl_CShuffle_V3<  Row,     Col,     Tuple<Row, Col>, Row,     I8,     I8,    Tuple<F32, F32>, BF16,   I32,     I32,  PassThrough, PassThrough, MultiplyMultiply,     GemmSpec,   128,    16,   64,    128, 16,  16,  16,   16,    1,    2,     S<8, 16, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,    S<8, 16, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,          1,           1,                   S<1, 16, 1, 8>,     S<4, 4, 1>,  BlkGemmPipeSched, BlockGemmPipelineVersion::v2, I8>,
        DeviceGemmMultiD_Xdl_CShuffle_V3<  Row,     Col,     Tuple<Row, Col>, Row,     I8,     I8,    Tuple<F32, F32>, BF16,   I32,     I32,  PassThrough, PassThrough, MultiplyMultiply,     GemmSpec,   128,    32,   64,    128, 16,  16,  32,   32,    1,    1,     S<8, 16, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,    S<8, 16, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,          1,           1,                   S<1, 16, 1, 8>,     S<8, 8, 1>,  BlkGemmPipeSched, BlockGemmPipelineVersion::v2, I8>,
        DeviceGemmMultiD_Xdl_CShuffle_V3<  Row,     Col,     Tuple<Row, Col>, Row,     I8,     I8,    Tuple<F32, F32>, BF16,   I32,     I32,  PassThrough, PassThrough, MultiplyMultiply,     GemmSpec,   128,    16,  128,    128, 16,  16,  16,   16,    1,    4,     S<8, 16, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,    S<8, 16, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,          1,           1,                   S<1, 16, 1, 8>,     S<4, 4, 1>,  BlkGemmPipeSched, BlockGemmPipelineVersion::v2, I8>,
        DeviceGemmMultiD_Xdl_CShuffle_V3<  Row,     Col,     Tuple<Row, Col>, Row,     I8,     I8,    Tuple<F32, F32>, BF16,   I32,     I32,  PassThrough, PassThrough, MultiplyMultiply,     GemmSpec,   128,    32,  128,    128, 16,  16,  32,   32,    1,    2,     S<8, 16, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,    S<8, 16, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,          1,           1,                   S<1, 16, 1, 8>,     S<8, 8, 1>,  BlkGemmPipeSched, BlockGemmPipelineVersion::v2, I8>,
        DeviceGemmMultiD_Xdl_CShuffle_V3<  Row,     Col,     Tuple<Row, Col>, Row,     I8,     I8,    Tuple<F32, F32>, BF16,   I32,     I32,  PassThrough, PassThrough, MultiplyMultiply,     GemmSpec,   256,    16,  256,    128, 16,  16,  16,   16,    1,    4,     S<8, 16, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,    S<8, 16, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,          1,           1,                   S<1, 16, 1, 16>,    S<4, 4, 1>,  BlkGemmPipeSched, BlockGemmPipelineVersion::v2, I8>,
        DeviceGemmMultiD_Xdl_CShuffle_V3<  Row,     Col,     Tuple<Row, Col>, Row,     I8,     I8,    Tuple<F32, F32>, BF16,   I32,     I32,  PassThrough, PassThrough, MultiplyMultiply,     GemmSpec,   256,    32,  256,    128, 16,  16,  32,   32,    1,    2,     S<8, 32, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,    S<8, 32, 1>,     S<1, 0, 2>,    S<1, 0, 2>,               2,             16,             16,          0,          1,           1,                   S<1, 16, 1, 16>,    S<8, 8, 1>,  BlkGemmPipeSched, BlockGemmPipelineVersion::v2, I8>
    // clang-format oI
    >;
} // namespace instance
} // namespace device
} // namespace tensor_operation
} // namespace ck

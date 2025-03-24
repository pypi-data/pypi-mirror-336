// SPDX-License-Identifier: MIT
// Copyright (c) 2018-2023, Advanced Micro Devices, Inc. All rights reserved.

#include <cstdlib>

#include "ck/ck.hpp"
#include "ck/tensor_operation/gpu/device/tensor_layout.hpp"
#include "ck/tensor_operation/gpu/device/gemm_specialization.hpp"
#include "ck/tensor_operation/gpu/device/impl/device_gemm_xdl_cshuffle.hpp"
#include "ck/tensor_operation/gpu/device/impl/device_gemm_xdl_cshuffle_v2.hpp"
#include "ck/tensor_operation/gpu/element/element_wise_operation.hpp"

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

static constexpr auto GemmDefault = ck::tensor_operation::device::GemmSpecialization::Default;

static constexpr auto MNPadding = ck::tensor_operation::device::GemmSpecialization::MNPadding;

static constexpr auto MNKPadding = ck::tensor_operation::device::GemmSpecialization::MNKPadding;

using device_gemm_xdl_c_shuffle_f16_f16_f16_mk_kn_mn_generic_instances = std::tuple<
    // clang-format off
        //#####################| ALayout| BLayout| CLayout| AData| BData| CData| AccData| CShuffle|           A|           B|           C|           GEMM| NumGemmK| Block|  MPer|  NPer|  KPer| AK1| BK1| MPer| NPer| MXdl| NXdl|  ABlockTransfer| ABlockTransfer| ABlockTransfer| ABlockTransfer| ABlockTransfer| ABlockTransfer| ABlockLds|  BBlockTransfer| BBlockTransfer| BBlockTransfer| BlockTransfer| BBlockTransfer| BBlockTransfer| BBlockLds|    CShuffle|    CShuffle| CBlockTransferClusterLengths|  CBlockTransfer|          LoopScheduler|                    Pipeline|
        //#####################|        |        |        |  Type|  Type|  Type|    Type| DataType| Elementwise| Elementwise| Elementwise| Specialization| Prefetch|  Size| Block| Block| Block|    |    |  XDL|  XDL|  Per|  Per|   ThreadCluster|  ThreadCluster| SrcAccessOrder|   SrcVectorDim|      SrcScalar|      DstScalar| AddExtraM|   ThreadCluster|  ThreadCluster| SrcAccessOrder|  SrcVectorDim|      SrcScalar|      DstScalar| AddExtraN| MXdlPerWave| NXdlPerWave|         _MBlock_MWaveMPerXdl| ScalarPerVector|                       |                            |
        //#####################|        |        |        |      |      |      |        |         |   Operation|   Operation|   Operation|               |    Stage|      |      |      |      |    |    |     |     | Wave| Wave| Lengths_K0_M_K1|   ArrangeOrder|               |               |      PerVector|   PerVector_K1|          | Lengths_K0_N_K1|   ArrangeOrder|               |              |      PerVector|   PerVector_K1|          |  PerShuffle|  PerShuffle|         _NBlock_NWaveNPerXdl|   _NWaveNPerXdl|                       |                            |
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,     MNKPadding,        1,   128,   128,   128,    32,   8,   8,   32,   32,    4,    2,     S<4, 32, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              1,              8,         1,     S<4, 32, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              1,              8,         1,           1,           1,               S<1, 16, 1, 8>,              1,  LoopScheduler::Default,        PipelineVersion::v1>
    // clang-format on
    >;

// Compilation parameters for a[m, k] * b[k, n] = c[m, n]
template <ck::tensor_operation::device::GemmSpecialization GemmSpec>
using device_gemm_xdl_c_shuffle_f16_f16_f16_mk_kn_mn_instances = std::tuple<
    // clang-format off
        //#####################| ALayout| BLayout| CLayout| AData| BData| CData| AccData| CShuffle|           A|           B|           C|           GEMM| NumGemmK| Block|  MPer|  NPer|  KPer| AK1| BK1| MPer| NPer| MXdl| NXdl|  ABlockTransfer| ABlockTransfer| ABlockTransfer| ABlockTransfer| ABlockTransfer| ABlockTransfer| ABlockLds|  BBlockTransfer| BBlockTransfer| BBlockTransfer| BlockTransfer| BBlockTransfer| BBlockTransfer| BBlockLds|    CShuffle|    CShuffle| CBlockTransferClusterLengths|  CBlockTransfer|          LoopScheduler|                    Pipeline|
        //#####################|        |        |        |  Type|  Type|  Type|    Type| DataType| Elementwise| Elementwise| Elementwise| Specialization| Prefetch|  Size| Block| Block| Block|    |    |  XDL|  XDL|  Per|  Per|   ThreadCluster|  ThreadCluster| SrcAccessOrder|   SrcVectorDim|      SrcScalar|      DstScalar| AddExtraM|   ThreadCluster|  ThreadCluster| SrcAccessOrder|  SrcVectorDim|      SrcScalar|      DstScalar| AddExtraN| MXdlPerWave| NXdlPerWave|         _MBlock_MWaveMPerXdl| ScalarPerVector|                       |                            |
        //#####################|        |        |        |      |      |      |        |         |   Operation|   Operation|   Operation|               |    Stage|      |      |      |      |    |    |     |     | Wave| Wave| Lengths_K0_M_K1|   ArrangeOrder|               |               |      PerVector|   PerVector_K1|          | Lengths_K0_N_K1|   ArrangeOrder|               |              |      PerVector|   PerVector_K1|          |  PerShuffle|  PerShuffle|         _NBlock_NWaveNPerXdl|   _NWaveNPerXdl|                       |                            |
        //#####################|        |        |        |      |      |      |        |         |            |            |            |               |         |      |      |      |      |    |    |     |     |     |     |                |               |               |               |               |               |          |                |               |               |              |               |               |          |            |            |                             |                |                       |                            |
        // pipeline v1, 1 wave
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   256,   256,   128,    32,   8,   2,   32,   32,    4,    2,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<8, 32, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              4,              2,         0,           1,           1,               S<1, 32, 1, 8>,              8,  LoopScheduler::Default,        PipelineVersion::v1>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   256,   256,   128,    32,   8,   8,   32,   32,    4,    2,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 64, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              2,              8,         1,           1,           1,               S<1, 32, 1, 8>,              8,  LoopScheduler::Default,        PipelineVersion::v1>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   256,   128,   256,    32,   8,   2,   32,   32,    2,    4,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 64, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              4,              2,         0,           1,           1,               S<1, 32, 1, 8>,              8,  LoopScheduler::Default,        PipelineVersion::v1>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   256,   128,   256,    32,   8,   8,   32,   32,    2,    4,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 64, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              4,              8,         1,           1,           1,               S<1, 32, 1, 8>,              8,  LoopScheduler::Default,        PipelineVersion::v1>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   128,   128,   128,    32,   8,   2,   32,   32,    4,    2,     S<4, 32, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 32, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              4,              2,         0,           1,           1,               S<1, 16, 1, 8>,              8,  LoopScheduler::Default,        PipelineVersion::v1>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   128,   128,   128,    32,   8,   8,   32,   32,    4,    2,     S<4, 32, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 32, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              4,              8,         1,           1,           1,               S<1, 16, 1, 8>,              8,  LoopScheduler::Default,        PipelineVersion::v1>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   256,   128,   128,    32,   8,   2,   32,   32,    2,    2,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<8, 32, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              4,              2,         0,           1,           1,               S<1, 32, 1, 8>,              8,  LoopScheduler::Default,        PipelineVersion::v1>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   256,   128,   128,    32,   8,   8,   32,   32,    2,    2,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 64, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              2,              8,         1,           1,           1,               S<1, 32, 1, 8>,              8,  LoopScheduler::Default,        PipelineVersion::v1>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   128,   128,    64,    32,   8,   2,   32,   32,    2,    2,     S<4, 32, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<8, 16, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              4,              2,         0,           1,           1,               S<1, 32, 1, 4>,              8,  LoopScheduler::Default,        PipelineVersion::v1>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   128,   128,    64,    32,   8,   8,   32,   32,    2,    2,     S<4, 32, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 32, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              2,              8,         1,           1,           1,               S<1, 32, 1, 4>,              8,  LoopScheduler::Default,        PipelineVersion::v1>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   128,    64,   128,    32,   8,   2,   32,   32,    2,    2,     S<4, 32, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 32, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              4,              2,         0,           1,           1,               S<1, 16, 1, 8>,              8,  LoopScheduler::Default,        PipelineVersion::v1>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   128,    64,   128,    32,   8,   8,   32,   32,    2,    2,     S<4, 32, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 32, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              4,              8,         1,           1,           1,               S<1, 16, 1, 8>,              8,  LoopScheduler::Default,        PipelineVersion::v1>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   256,   128,    64,    32,   8,   2,   32,   32,    2,    1,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<16,16, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              4,              2,         0,           1,           1,               S<1, 32, 1, 8>,              8,  LoopScheduler::Default,        PipelineVersion::v1>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   256,   128,    64,    32,   8,   8,   32,   32,    2,    1,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 64, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              1,              8,         1,           1,           1,               S<1, 32, 1, 8>,              8,  LoopScheduler::Default,        PipelineVersion::v1>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   256,    64,   128,    32,   8,   2,   32,   32,    1,    2,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<8, 32, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              4,              2,         0,           1,           1,               S<1, 32, 1, 8>,              8,  LoopScheduler::Default,        PipelineVersion::v1>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   256,    64,   128,    32,   8,   8,   32,   32,    1,    2,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 64, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              2,              8,         1,           1,           1,               S<1, 32, 1, 8>,              8,  LoopScheduler::Default,        PipelineVersion::v1>,
        DeviceGemm_Xdl_CShuffleV2<   Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        2,   256,   256,   256,    32,   8,   4,   32,   32,    4,    4,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         0,     S<8, 32, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              8,              4,         0,           1,           1,               S<1, 32, 1, 8>,              8,  LoopScheduler::Default,        PipelineVersion::v1>
#if CK_EXPERIMENTAL_INTER_WAVE_INSTANCES
        // pipeline v1, 2 waves
        ,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   256,   256,   128,    32,   8,   2,   32,   32,    4,    2,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<8, 32, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              4,              2,         0,           1,           1,               S<1, 32, 1, 8>,              8,  LoopScheduler::Interwave,      PipelineVersion::v1>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   256,   256,   128,    32,   8,   8,   32,   32,    4,    2,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 64, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              2,              8,         1,           1,           1,               S<1, 32, 1, 8>,              8,  LoopScheduler::Interwave,      PipelineVersion::v1>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   256,   128,   256,    32,   8,   2,   32,   32,    2,    4,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 64, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              4,              2,         0,           1,           1,               S<1, 32, 1, 8>,              8,  LoopScheduler::Interwave,      PipelineVersion::v1>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   256,   128,   256,    32,   8,   8,   32,   32,    2,    4,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 64, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              4,              8,         1,           1,           1,               S<1, 32, 1, 8>,              8,  LoopScheduler::Interwave,      PipelineVersion::v1>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   128,   128,   128,    32,   8,   2,   32,   32,    4,    2,     S<4, 32, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 32, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              4,              2,         0,           1,           1,               S<1, 16, 1, 8>,              8,  LoopScheduler::Interwave,      PipelineVersion::v1>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   128,   128,   128,    32,   8,   8,   32,   32,    4,    2,     S<4, 32, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 32, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              4,              8,         1,           1,           1,               S<1, 16, 1, 8>,              8,  LoopScheduler::Interwave,      PipelineVersion::v1>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   256,   128,   128,    32,   8,   2,   32,   32,    2,    2,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<8, 32, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              4,              2,         0,           1,           1,               S<1, 32, 1, 8>,              8,  LoopScheduler::Interwave,      PipelineVersion::v1>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   256,   128,   128,    32,   8,   8,   32,   32,    2,    2,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 64, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              2,              8,         1,           1,           1,               S<1, 32, 1, 8>,              8,  LoopScheduler::Interwave,      PipelineVersion::v1>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   128,   128,    64,    32,   8,   2,   32,   32,    2,    2,     S<4, 32, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<8, 16, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              4,              2,         0,           1,           1,               S<1, 32, 1, 4>,              8,  LoopScheduler::Interwave,      PipelineVersion::v1>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   128,   128,    64,    32,   8,   8,   32,   32,    2,    2,     S<4, 32, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 32, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              2,              8,         1,           1,           1,               S<1, 32, 1, 4>,              8,  LoopScheduler::Interwave,      PipelineVersion::v1>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   128,    64,   128,    32,   8,   2,   32,   32,    2,    2,     S<4, 32, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 32, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              4,              2,         0,           1,           1,               S<1, 16, 1, 8>,              8,  LoopScheduler::Interwave,      PipelineVersion::v1>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   128,    64,   128,    32,   8,   8,   32,   32,    2,    2,     S<4, 32, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 32, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              4,              8,         1,           1,           1,               S<1, 16, 1, 8>,              8,  LoopScheduler::Interwave,      PipelineVersion::v1>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   256,   128,    64,    32,   8,   2,   32,   32,    2,    1,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<16,16, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              4,              2,         0,           1,           1,               S<1, 32, 1, 8>,              8,  LoopScheduler::Interwave,      PipelineVersion::v1>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   256,   128,    64,    32,   8,   8,   32,   32,    2,    1,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 64, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              1,              8,         1,           1,           1,               S<1, 32, 1, 8>,              8,  LoopScheduler::Interwave,      PipelineVersion::v1>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   256,    64,   128,    32,   8,   2,   32,   32,    1,    2,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<8, 32, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              4,              2,         0,           1,           1,               S<1, 32, 1, 8>,              8,  LoopScheduler::Interwave,      PipelineVersion::v1>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   256,    64,   128,    32,   8,   8,   32,   32,    1,    2,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 64, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              2,              8,         1,           1,           1,               S<1, 32, 1, 8>,              8,  LoopScheduler::Interwave,      PipelineVersion::v1>
#endif
#if CK_EXPERIMENTAL_PIPELINE_V2_INSTANCES
        // pipeline v2, 1 wave
        ,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   256,   256,   128,    32,   8,   2,   32,   32,    4,    2,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<8, 32, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              4,              2,         0,           1,           1,               S<1, 32, 1, 8>,              8,  LoopScheduler::Default,        PipelineVersion::v2>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   256,   256,   128,    32,   8,   8,   32,   32,    4,    2,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 64, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              2,              8,         1,           1,           1,               S<1, 32, 1, 8>,              8,  LoopScheduler::Default,        PipelineVersion::v2>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   256,   128,   256,    32,   8,   2,   32,   32,    2,    4,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 64, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              4,              2,         0,           1,           1,               S<1, 32, 1, 8>,              8,  LoopScheduler::Default,        PipelineVersion::v2>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   256,   128,   256,    32,   8,   8,   32,   32,    2,    4,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 64, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              4,              8,         1,           1,           1,               S<1, 32, 1, 8>,              8,  LoopScheduler::Default,        PipelineVersion::v2>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   128,   128,   128,    32,   8,   2,   32,   32,    4,    2,     S<4, 32, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 32, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              4,              2,         0,           1,           1,               S<1, 16, 1, 8>,              8,  LoopScheduler::Default,        PipelineVersion::v2>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   128,   128,   128,    32,   8,   8,   32,   32,    4,    2,     S<4, 32, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 32, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              4,              8,         1,           1,           1,               S<1, 16, 1, 8>,              8,  LoopScheduler::Default,        PipelineVersion::v2>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   256,   128,   128,    32,   8,   2,   32,   32,    2,    2,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<8, 32, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              4,              2,         0,           1,           1,               S<1, 32, 1, 8>,              8,  LoopScheduler::Default,        PipelineVersion::v2>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   256,   128,   128,    32,   8,   8,   32,   32,    2,    2,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 64, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              2,              8,         1,           1,           1,               S<1, 32, 1, 8>,              8,  LoopScheduler::Default,        PipelineVersion::v2>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   128,   128,    64,    32,   8,   2,   32,   32,    2,    2,     S<4, 32, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<8, 16, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              4,              2,         0,           1,           1,               S<1, 32, 1, 4>,              8,  LoopScheduler::Default,        PipelineVersion::v2>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   128,   128,    64,    32,   8,   8,   32,   32,    2,    2,     S<4, 32, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 32, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              2,              8,         1,           1,           1,               S<1, 32, 1, 4>,              8,  LoopScheduler::Default,        PipelineVersion::v2>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   128,    64,   128,    32,   8,   2,   32,   32,    2,    2,     S<4, 32, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 32, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              4,              2,         0,           1,           1,               S<1, 16, 1, 8>,              8,  LoopScheduler::Default,        PipelineVersion::v2>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   128,    64,   128,    32,   8,   8,   32,   32,    2,    2,     S<4, 32, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 32, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              4,              8,         1,           1,           1,               S<1, 16, 1, 8>,              8,  LoopScheduler::Default,        PipelineVersion::v2>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   256,   128,    64,    32,   8,   2,   32,   32,    2,    1,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<16,16, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              4,              2,         0,           1,           1,               S<1, 32, 1, 8>,              8,  LoopScheduler::Default,        PipelineVersion::v2>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   256,   128,    64,    32,   8,   8,   32,   32,    2,    1,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 64, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              1,              8,         1,           1,           1,               S<1, 32, 1, 8>,              8,  LoopScheduler::Default,        PipelineVersion::v2>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   256,    64,   128,    32,   8,   2,   32,   32,    1,    2,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<8, 32, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              4,              2,         0,           1,           1,               S<1, 32, 1, 8>,              8,  LoopScheduler::Default,        PipelineVersion::v2>,
        DeviceGemm_Xdl_CShuffle<     Row,      Row,    Row,   F16,   F16,   F16,     F32,      F16, PassThrough, PassThrough, PassThrough,       GemmSpec,        1,   256,    64,   128,    32,   8,   8,   32,   32,    1,    2,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 64, 1>,     S<0, 2, 1>,     S<0, 2, 1>,             1,              2,              8,         1,           1,           1,               S<1, 32, 1, 8>,              8,  LoopScheduler::Default,        PipelineVersion::v2>
#endif
    // clang-format on
    >;

void add_device_gemm_xdl_c_shuffle_f16_f16_f16_mk_kn_mn_instances(
    std::vector<std::unique_ptr<
        DeviceGemm<Row, Row, Row, F16, F16, F16, PassThrough, PassThrough, PassThrough>>>&
        instances)
{
    add_device_operation_instances(
        instances, device_gemm_xdl_c_shuffle_f16_f16_f16_mk_kn_mn_generic_instances{});

    add_device_operation_instances(
        instances, device_gemm_xdl_c_shuffle_f16_f16_f16_mk_kn_mn_instances<GemmDefault>{});

    add_device_operation_instances(
        instances, device_gemm_xdl_c_shuffle_f16_f16_f16_mk_kn_mn_instances<MNPadding>{});

    add_device_operation_instances(
        instances, device_gemm_xdl_c_shuffle_f16_f16_f16_mk_kn_mn_instances<MNKPadding>{});
}

} // namespace instance
} // namespace device
} // namespace tensor_operation
} // namespace ck

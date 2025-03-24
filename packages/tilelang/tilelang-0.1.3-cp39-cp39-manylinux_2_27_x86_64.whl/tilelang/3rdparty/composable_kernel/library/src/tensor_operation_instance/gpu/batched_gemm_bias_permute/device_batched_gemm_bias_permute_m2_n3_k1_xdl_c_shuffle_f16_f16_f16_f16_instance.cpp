// SPDX-License-Identifier: MIT
// Copyright (c) 2018-2023, Advanced Micro Devices, Inc. All rights reserved.

// This (ifndef) is a hack to use customized behavior for buffer load rather than using default
// setting Don't use this hack unless absolutely necessary!
// FIXME: make the behavior of buffer load a configurable (template) parameter of each device op
#define CK_EXPERIMENTAL_USE_BUFFER_LOAD_OOB_CHECK_OFFSET_TRICK 1

#include <cstdlib>

#include "ck/ck.hpp"
#include "ck/tensor_operation/gpu/device/tensor_layout.hpp"
#include "ck/tensor_operation/gpu/device/gemm_specialization.hpp"
#include "ck/tensor_operation/gpu/device/impl/device_batched_contraction_multiple_d_xdl_cshuffle.hpp"
#include "ck/tensor_operation/gpu/element/element_wise_operation.hpp"

#include "ck/library/tensor_operation_instance/add_device_operation_instance.hpp"

namespace ck {
namespace tensor_operation {
namespace device {
namespace instance {

using F16       = ck::half_t;
using F32       = float;
using F16_Tuple = ck::Tuple<F16>;

template <ck::index_t... Is>
using S = ck::Sequence<Is...>;

using PassThrough = ck::tensor_operation::element_wise::PassThrough;
using Add         = ck::tensor_operation::element_wise::Add;

static constexpr auto GemmMNKPadding = ck::tensor_operation::device::GemmSpecialization::MNKPadding;
static constexpr auto ABSpec         = ck::tensor_operation::device::TensorSpecialization::Packed;
static constexpr auto DESpec         = ck::tensor_operation::device::TensorSpecialization::Default;

// A[g0, m0, m1, k0] * B[g0, n0, n1, n2, k0] + D[g0, m0, m1, n0, n1, n2] = E[g0, n0, m0, n0, n1, m1]
// m/n/n/n are the fast changing dimension for A/B/D/E
using device_batched_contraction_bias_permute_m2_n3_k1_xdl_c_shuffle_f16_f16_f16_f16_mnnm_instance =
    std::tuple<
        // clang-format off
        //############################################| NumDimG| NumDimM| NumDimN| NumDimK| AData| BData| AccData| CShuffle|    DsData| EData|            A|           B|         CDE|           GEMM|              A|              B|             DE| NumGemmK| Block|  MPer|  NPer|  KPer| AK1| BK1| MPer| NPer| MXdl| NXdl|  ABlockTransfer| ABlockTransfer| ABlockTransfer| ABlockTransfer| ABlockTransfer| ABlockTransfer| ABlockLds|  BBlockTransfer| BBlockTransfer| BBlockTransfer| BlockTransfer| BBlockTransfer| BBlockTransfer| BBlockLds|    CShuffle|    CShuffle| CBlockTransferClusterLengths|  CBlockTransfer|
        //############################################|        |        |        |        |  Type|  Type|    Type| DataType|      Type|  Type|  Elementwise| Elementwise| Elementwise| Specialization| Spacialization| Spacialization| Spacialization| Prefetch|  Size| Block| Block| Block|    |    |  XDL|  XDL|  Per|  Per|   ThreadCluster|  ThreadCluster| SrcAccessOrder|   SrcVectorDim|      SrcScalar|      DstScalar| AddExtraM|   ThreadCluster|  ThreadCluster| SrcAccessOrder|  SrcVectorDim|      SrcScalar|      DstScalar| AddExtraN| MXdlPerWave| NXdlPerWave|         _MBlock_MWaveMPerXdl| ScalarPerVector|
        //############################################|        |        |        |        |      |      |        |         |          |      |    Operation|   Operation|   Operation|               |               |               |               |    Stage|      |      |      |      |    |    |     |     | Wave| Wave| Lengths_K0_M_K1|   ArrangeOrder|               |               |      PerVector|   PerVector_K1|          | Lengths_K0_N_K1|   ArrangeOrder|               |              |      PerVector|   PerVector_K1|          |  PerShuffle|  PerShuffle|         _NBlock_NWaveNPerXdl|   _NWaveNPerXdl|
        //############################################|        |        |        |        |      |      |        |         |          |      |             |            |            |               |               |               |               |         |      |      |      |      |    |    |     |     |     |     |                |               |               |               |               |               |          |                |               |               |              |               |               |          |            |            |                             |                |
        DeviceBatchedContractionMultipleD_Xdl_CShuffle<       1,       2,       3,       1,   F16,   F16,     F32,      F16, F16_Tuple,   F16,  PassThrough, PassThrough,         Add, GemmMNKPadding,         ABSpec,         ABSpec,         DESpec,        1,   256,   256,   128,    32,   8,   8,   32,   32,    4,    2,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,             2,              8,              8,         1,           1,           1,               S<1, 32, 1, 8>,               1>,
        DeviceBatchedContractionMultipleD_Xdl_CShuffle<       1,       2,       3,       1,   F16,   F16,     F32,      F16, F16_Tuple,   F16,  PassThrough, PassThrough,         Add, GemmMNKPadding,         ABSpec,         ABSpec,         DESpec,        1,   256,   128,   256,    32,   8,   8,   32,   32,    2,    4,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,             2,              8,              8,         1,           1,           1,               S<1, 32, 1, 8>,               1>,
        DeviceBatchedContractionMultipleD_Xdl_CShuffle<       1,       2,       3,       1,   F16,   F16,     F32,      F16, F16_Tuple,   F16,  PassThrough, PassThrough,         Add, GemmMNKPadding,         ABSpec,         ABSpec,         DESpec,        1,   128,   128,   128,    32,   8,   8,   32,   32,    4,    2,     S<4, 32, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 32, 1>,     S<1, 0, 2>,     S<1, 0, 2>,             2,              8,              8,         1,           1,           1,               S<1, 16, 1, 8>,               1>,
        DeviceBatchedContractionMultipleD_Xdl_CShuffle<       1,       2,       3,       1,   F16,   F16,     F32,      F16, F16_Tuple,   F16,  PassThrough, PassThrough,         Add, GemmMNKPadding,         ABSpec,         ABSpec,         DESpec,        1,   256,   128,   128,    32,   8,   8,   32,   32,    2,    2,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,             2,              8,              8,         1,           1,           1,               S<1, 32, 1, 8>,               1>,
        DeviceBatchedContractionMultipleD_Xdl_CShuffle<       1,       2,       3,       1,   F16,   F16,     F32,      F16, F16_Tuple,   F16,  PassThrough, PassThrough,         Add, GemmMNKPadding,         ABSpec,         ABSpec,         DESpec,        1,   128,   128,    64,    32,   8,   8,   32,   32,    2,    2,     S<4, 32, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 32, 1>,     S<1, 0, 2>,     S<1, 0, 2>,             2,              8,              8,         1,           1,           1,               S<1, 32, 1, 4>,               1>,
        DeviceBatchedContractionMultipleD_Xdl_CShuffle<       1,       2,       3,       1,   F16,   F16,     F32,      F16, F16_Tuple,   F16,  PassThrough, PassThrough,         Add, GemmMNKPadding,         ABSpec,         ABSpec,         DESpec,        1,   128,    64,   128,    32,   8,   8,   32,   32,    2,    2,     S<4, 32, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 32, 1>,     S<1, 0, 2>,     S<1, 0, 2>,             2,              8,              8,         1,           1,           1,               S<1, 16, 1, 8>,               1>,
        DeviceBatchedContractionMultipleD_Xdl_CShuffle<       1,       2,       3,       1,   F16,   F16,     F32,      F16, F16_Tuple,   F16,  PassThrough, PassThrough,         Add, GemmMNKPadding,         ABSpec,         ABSpec,         DESpec,        1,    64,    64,    64,    32,   8,   8,   32,   32,    2,    2,     S<4, 16, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 16, 1>,     S<1, 0, 2>,     S<1, 0, 2>,             2,              8,              8,         1,           1,           1,               S<1, 16, 1, 4>,               1>,
        DeviceBatchedContractionMultipleD_Xdl_CShuffle<       1,       2,       3,       1,   F16,   F16,     F32,      F16, F16_Tuple,   F16,  PassThrough, PassThrough,         Add, GemmMNKPadding,         ABSpec,         ABSpec,         DESpec,        1,   256,   128,    64,    32,   8,   8,   32,   32,    2,    1,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,             2,              8,              8,         1,           1,           1,               S<1, 32, 1, 8>,               1>,
        DeviceBatchedContractionMultipleD_Xdl_CShuffle<       1,       2,       3,       1,   F16,   F16,     F32,      F16, F16_Tuple,   F16,  PassThrough, PassThrough,         Add, GemmMNKPadding,         ABSpec,         ABSpec,         DESpec,        1,   256,    64,   128,    32,   8,   8,   32,   32,    1,    2,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,             2,              8,              8,         1,           1,           1,               S<1, 32, 1, 8>,               1>,
        DeviceBatchedContractionMultipleD_Xdl_CShuffle<       1,       2,       3,       1,   F16,   F16,     F32,      F16, F16_Tuple,   F16,  PassThrough, PassThrough,         Add, GemmMNKPadding,         ABSpec,         ABSpec,         DESpec,        1,   128,   128,    32,    32,   8,   8,   32,   32,    2,    1,     S<4, 32, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 32, 1>,     S<1, 0, 2>,     S<1, 0, 2>,             2,              8,              8,         1,           1,           1,               S<1, 32, 1, 4>,               1>,
        DeviceBatchedContractionMultipleD_Xdl_CShuffle<       1,       2,       3,       1,   F16,   F16,     F32,      F16, F16_Tuple,   F16,  PassThrough, PassThrough,         Add, GemmMNKPadding,         ABSpec,         ABSpec,         DESpec,        1,   128,    32,   128,    32,   8,   8,   32,   32,    1,    2,     S<4, 32, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 32, 1>,     S<1, 0, 2>,     S<1, 0, 2>,             2,              8,              8,         1,           1,           1,               S<1, 16, 1, 8>,               1>,
        DeviceBatchedContractionMultipleD_Xdl_CShuffle<       1,       2,       3,       1,   F16,   F16,     F32,      F16, F16_Tuple,   F16,  PassThrough, PassThrough,         Add, GemmMNKPadding,         ABSpec,         ABSpec,         DESpec,        1,    64,    64,    32,    32,   8,   8,   32,   32,    2,    1,     S<4, 16, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 16, 1>,     S<1, 0, 2>,     S<1, 0, 2>,             2,              8,              8,         1,           1,           1,               S<1, 16, 1, 4>,               1>,
        DeviceBatchedContractionMultipleD_Xdl_CShuffle<       1,       2,       3,       1,   F16,   F16,     F32,      F16, F16_Tuple,   F16,  PassThrough, PassThrough,         Add, GemmMNKPadding,         ABSpec,         ABSpec,         DESpec,        1,    64,    32,    64,    32,   8,   8,   32,   32,    1,    2,     S<4, 16, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 16, 1>,     S<1, 0, 2>,     S<1, 0, 2>,             2,              8,              8,         1,           1,           1,               S<1, 16, 1, 4>,               1>,
        //M1 faster dim
        DeviceBatchedContractionMultipleD_Xdl_CShuffle<       1,       2,       3,       1,   F16,   F16,     F32,      F16, F16_Tuple,   F16,  PassThrough, PassThrough,         Add, GemmMNKPadding,         ABSpec,         ABSpec,         DESpec,        1,   256,   256,   128,    32,   8,   8,   32,   32,    4,    2,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,             2,              8,              8,         1,           1,           1,               S<1, 32, 1, 8>,               8>,
        DeviceBatchedContractionMultipleD_Xdl_CShuffle<       1,       2,       3,       1,   F16,   F16,     F32,      F16, F16_Tuple,   F16,  PassThrough, PassThrough,         Add, GemmMNKPadding,         ABSpec,         ABSpec,         DESpec,        1,   256,   128,   256,    32,   8,   8,   32,   32,    2,    4,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,             2,              8,              8,         1,           1,           1,               S<1, 32, 1, 8>,               8>,
        DeviceBatchedContractionMultipleD_Xdl_CShuffle<       1,       2,       3,       1,   F16,   F16,     F32,      F16, F16_Tuple,   F16,  PassThrough, PassThrough,         Add, GemmMNKPadding,         ABSpec,         ABSpec,         DESpec,        1,   128,   128,   128,    32,   8,   8,   32,   32,    4,    2,     S<4, 32, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 32, 1>,     S<1, 0, 2>,     S<1, 0, 2>,             2,              8,              8,         1,           1,           1,               S<1, 16, 1, 8>,               8>,
        DeviceBatchedContractionMultipleD_Xdl_CShuffle<       1,       2,       3,       1,   F16,   F16,     F32,      F16, F16_Tuple,   F16,  PassThrough, PassThrough,         Add, GemmMNKPadding,         ABSpec,         ABSpec,         DESpec,        1,   256,   128,   128,    32,   8,   8,   32,   32,    2,    2,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,             2,              8,              8,         1,           1,           1,               S<1, 32, 1, 8>,               8>,
        DeviceBatchedContractionMultipleD_Xdl_CShuffle<       1,       2,       3,       1,   F16,   F16,     F32,      F16, F16_Tuple,   F16,  PassThrough, PassThrough,         Add, GemmMNKPadding,         ABSpec,         ABSpec,         DESpec,        1,   128,   128,    64,    32,   8,   8,   32,   32,    2,    2,     S<4, 32, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 32, 1>,     S<1, 0, 2>,     S<1, 0, 2>,             2,              8,              8,         1,           1,           1,               S<1, 32, 1, 4>,               8>,
        DeviceBatchedContractionMultipleD_Xdl_CShuffle<       1,       2,       3,       1,   F16,   F16,     F32,      F16, F16_Tuple,   F16,  PassThrough, PassThrough,         Add, GemmMNKPadding,         ABSpec,         ABSpec,         DESpec,        1,   128,    64,   128,    32,   8,   8,   32,   32,    2,    2,     S<4, 32, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 32, 1>,     S<1, 0, 2>,     S<1, 0, 2>,             2,              8,              8,         1,           1,           1,               S<1, 16, 1, 8>,               8>,
        DeviceBatchedContractionMultipleD_Xdl_CShuffle<       1,       2,       3,       1,   F16,   F16,     F32,      F16, F16_Tuple,   F16,  PassThrough, PassThrough,         Add, GemmMNKPadding,         ABSpec,         ABSpec,         DESpec,        1,    64,    64,    64,    32,   8,   8,   32,   32,    2,    2,     S<4, 16, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 16, 1>,     S<1, 0, 2>,     S<1, 0, 2>,             2,              8,              8,         1,           1,           1,               S<1, 16, 1, 4>,               8>,
        DeviceBatchedContractionMultipleD_Xdl_CShuffle<       1,       2,       3,       1,   F16,   F16,     F32,      F16, F16_Tuple,   F16,  PassThrough, PassThrough,         Add, GemmMNKPadding,         ABSpec,         ABSpec,         DESpec,        1,   256,   128,    64,    32,   8,   8,   32,   32,    2,    1,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,             2,              8,              8,         1,           1,           1,               S<1, 32, 1, 8>,               8>,
        DeviceBatchedContractionMultipleD_Xdl_CShuffle<       1,       2,       3,       1,   F16,   F16,     F32,      F16, F16_Tuple,   F16,  PassThrough, PassThrough,         Add, GemmMNKPadding,         ABSpec,         ABSpec,         DESpec,        1,   256,    64,   128,    32,   8,   8,   32,   32,    1,    2,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 64, 1>,     S<1, 0, 2>,     S<1, 0, 2>,             2,              8,              8,         1,           1,           1,               S<1, 32, 1, 8>,               8>,
        DeviceBatchedContractionMultipleD_Xdl_CShuffle<       1,       2,       3,       1,   F16,   F16,     F32,      F16, F16_Tuple,   F16,  PassThrough, PassThrough,         Add, GemmMNKPadding,         ABSpec,         ABSpec,         DESpec,        1,   128,   128,    32,    32,   8,   8,   32,   32,    2,    1,     S<4, 32, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 32, 1>,     S<1, 0, 2>,     S<1, 0, 2>,             2,              8,              8,         1,           1,           1,               S<1, 32, 1, 4>,               8>,
        DeviceBatchedContractionMultipleD_Xdl_CShuffle<       1,       2,       3,       1,   F16,   F16,     F32,      F16, F16_Tuple,   F16,  PassThrough, PassThrough,         Add, GemmMNKPadding,         ABSpec,         ABSpec,         DESpec,        1,   128,    32,   128,    32,   8,   8,   32,   32,    1,    2,     S<4, 32, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 32, 1>,     S<1, 0, 2>,     S<1, 0, 2>,             2,              8,              8,         1,           1,           1,               S<1, 16, 1, 8>,               8>,
        DeviceBatchedContractionMultipleD_Xdl_CShuffle<       1,       2,       3,       1,   F16,   F16,     F32,      F16, F16_Tuple,   F16,  PassThrough, PassThrough,         Add, GemmMNKPadding,         ABSpec,         ABSpec,         DESpec,        1,    64,    64,    32,    32,   8,   8,   32,   32,    2,    1,     S<4, 16, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 16, 1>,     S<1, 0, 2>,     S<1, 0, 2>,             2,              8,              8,         1,           1,           1,               S<1, 16, 1, 4>,               8>,
        DeviceBatchedContractionMultipleD_Xdl_CShuffle<       1,       2,       3,       1,   F16,   F16,     F32,      F16, F16_Tuple,   F16,  PassThrough, PassThrough,         Add, GemmMNKPadding,         ABSpec,         ABSpec,         DESpec,        1,    64,    32,    64,    32,   8,   8,   32,   32,    1,    2,     S<4, 16, 1>,     S<1, 0, 2>,     S<1, 0, 2>,              2,              8,              8,         1,     S<4, 16, 1>,     S<1, 0, 2>,     S<1, 0, 2>,             2,              8,              8,         1,           1,           1,               S<1, 16, 1, 4>,               8>
        // clang-format on
        >;

void add_device_batched_contraction_bias_permute_m2_n3_k1_xdl_c_shuffle_f16_f16_f16_f16_mnnm_instance(
    std::vector<std::unique_ptr<DeviceBatchedContractionMultipleD<1,
                                                                  2,
                                                                  3,
                                                                  1,
                                                                  F16,
                                                                  F16,
                                                                  F16_Tuple,
                                                                  F16,
                                                                  PassThrough,
                                                                  PassThrough,
                                                                  Add>>>& instances)
{
    add_device_operation_instances(
        instances,
        device_batched_contraction_bias_permute_m2_n3_k1_xdl_c_shuffle_f16_f16_f16_f16_mnnm_instance{});
}

} // namespace instance
} // namespace device
} // namespace tensor_operation
} // namespace ck

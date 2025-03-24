/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

/*!
 * \file linear_algebra.h
 * \brief The functions to infer struct info for distributed linear algebra operator
 */

#ifndef TVM_RELAX_OP_DISTRIBUTED_LINEAR_ALGEBRA_H_
#define TVM_RELAX_OP_DISTRIBUTED_LINEAR_ALGEBRA_H_

#include "utils.h"
namespace tvm {
namespace relax {
namespace distributed {

StructInfo InferDistStructInfoMatmul(const Call& call, const BlockBuilder& ctx);

}  // namespace distributed
}  // namespace relax
}  // namespace tvm

#endif  // TVM_RELAX_OP_DISTRIBUTED_LINEAR_ALGEBRA_H_

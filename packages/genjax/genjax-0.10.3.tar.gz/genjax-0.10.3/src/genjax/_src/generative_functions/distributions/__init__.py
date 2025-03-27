# Copyright 2024 MIT Probabilistic Computing Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This module provides:

* Abstract base classes for declaring distributions as `GenerativeFunction` types. These classes are `Distribution` and `ExactDensity`. The latter assumes that the inheritor exposes _exact density evaluation_, while the former makes no such assumption.

* A number of distribution generative functions which implement `ExactDensity` by utilizing TensorFlow Probability distributions with the JAX backend.

* Custom distributions, including ones with exact posteriors (like discrete HMMs).
"""

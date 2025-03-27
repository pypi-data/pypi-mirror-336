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
"""A module containing a test suite for inference based on exact inference in hidden
Markov models (HMMs)."""

import jax
import jax.numpy as jnp

from genjax._src.core.generative import SelectionBuilder
from genjax._src.core.pytree import Pytree
from genjax._src.core.typing import FloatArray, IntArray, PRNGKey
from genjax._src.generative_functions.combinators.scan import (
    scan,
)
from genjax._src.generative_functions.distributions.custom.discrete_hmm import (
    DiscreteHMM,
    DiscreteHMMConfiguration,
)
from genjax._src.generative_functions.distributions.tensorflow_probability import (
    categorical,
)
from genjax._src.generative_functions.static import gen


@Pytree.dataclass
class DiscreteHMMInferenceProblem(Pytree):
    initial_state: IntArray
    log_posterior: FloatArray
    log_data_marginal: FloatArray
    latent_sequence: IntArray
    observation_sequence: IntArray


def build_test_against_exact_inference(
    max_length: int,
    state_space_size: IntArray,
    transition_distance_truncation: IntArray,
    observation_distance_truncation: IntArray,
    transition_variance: FloatArray,
    observation_variance: FloatArray,
):
    config = DiscreteHMMConfiguration(
        state_space_size,
        transition_distance_truncation,
        observation_distance_truncation,
        transition_variance,
        observation_variance,
    )

    @scan(n=max_length)
    @gen
    def markov_chain(state: IntArray, config: DiscreteHMMConfiguration):
        transition = config.transition_tensor()
        observation = config.observation_tensor()
        z = categorical(transition[state, :]) @ "z"
        _ = categorical(observation[z, :]) @ "x"
        return z, None

    def inference_test_generator(key: PRNGKey):
        key, sub_key = jax.random.split(key)
        initial_state = categorical.sample(sub_key, jnp.ones(config.linear_grid_dim))
        tr = markov_chain.simulate(sub_key, (max_length - 1, initial_state, config))
        z_sel = SelectionBuilder["z"]
        x_sel = SelectionBuilder["x"]
        latent_sequence = tr.get_choices().filter(z_sel)["z"]
        observation_sequence = tr.get_choices().filter(x_sel)["x"]
        log_data_marginal = DiscreteHMM.data_logpdf(config, observation_sequence)
        # This actually doesn't use any randomness.
        (log_posterior, _) = DiscreteHMM.estimate_logpdf(
            key, latent_sequence, config, observation_sequence
        )
        return DiscreteHMMInferenceProblem(
            initial_state,
            log_posterior,
            log_data_marginal,
            latent_sequence,
            observation_sequence,
        )

    return inference_test_generator

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
"""The `Vmap` is a generative function combinator which exposes vectorization
on the input arguments of a provided generative function callee.

This vectorization is implemented using `jax.vmap`, and the combinator expects the user to specify `in_axes` as part of the construction of an instance of this combinator.
"""

import jax
import jax.numpy as jnp
import jax.tree_util as jtu

from genjax._src.core.compiler.interpreters.incremental import Diff
from genjax._src.core.generative import (
    Argdiffs,
    ChoiceMap,
    EditRequest,
    GenerativeFunction,
    IndexRequest,
    R,
    Retdiff,
    Score,
    Trace,
    Update,
    Weight,
)
from genjax._src.core.generative.choice_map import (
    Address,
    Selection,
)
from genjax._src.core.pytree import Pytree
from genjax._src.core.typing import (
    Any,
    Callable,
    FloatArray,
    Generic,
    InAxes,
    IntArray,
    PRNGKey,
)


@Pytree.dataclass
class VmapTrace(Generic[R], Trace[R]):
    gen_fn: "Vmap[R]"
    inner: Trace[R]
    args: tuple[Any, ...]
    score: FloatArray
    chm: ChoiceMap

    # TODO is this really helpful? what if someone has inflated the dimension out from around us? How do we re-use this?
    dim_length: int = Pytree.static()

    @staticmethod
    def build(
        gen_fn: "Vmap[R]", tr: Trace[R], args: tuple[Any, ...], length: int
    ) -> "VmapTrace[R]":
        score = jnp.sum(jax.vmap(lambda tr: tr.get_score())(tr))
        # TODO make a note here about why we are jax.vmapping; we are library authors!! we should not depend on the user convenience here of get_choices() on a vectorized choicemap.
        if length == 0:
            chm = ChoiceMap.empty()
        else:
            chm = jax.vmap(lambda tr: tr.get_choices())(tr)
        return VmapTrace(gen_fn, tr, args, score, chm, length)

    def get_args(self) -> tuple[Any, ...]:
        return self.args

    def get_retval(self):
        # returns the vectorized retval from self.inner.
        return self.inner.get_retval()

    def get_gen_fn(self):
        return self.gen_fn

    def get_choices(self) -> ChoiceMap:
        return self.chm

    def get_score(self) -> Score:
        return self.score

    def get_inner_trace(self, address: Address):
        return self.inner.get_inner_trace(address)


@Pytree.dataclass
class Vmap(Generic[R], GenerativeFunction[R]):
    """`Vmap` is a generative function which lifts another generative function to support `vmap`-based patterns of parallel (and generative) computation.

    In contrast to the full set of options which [`jax.vmap`](https://jax.readthedocs.io/en/latest/_autosummary/jax.vmap.html), this combinator expects an `in_axes: tuple` configuration argument, which indicates how the underlying `vmap` patterns should be broadcast across the input arguments to the generative function.

    Attributes:
        gen_fn: A [`genjax.GenerativeFunction`][] to be vectorized.

        in_axes: A tuple specifying which input arguments (or indices into them) should be vectorized. `in_axes` must match (or prefix) the `Pytree` type of the argument tuple for the underlying `gen_fn`. Defaults to 0, i.e., the first argument. See [this link](https://jax/readthedocs.io/en/latest/pytrees.html#applying-optional-parameters-to-pytrees) for more detail.

    Examples:
        Create a `Vmap` using the [`genjax.vmap`][] decorator:
        ```python exec="yes" html="true" source="material-block" session="vmap"
        import jax, genjax
        import jax.numpy as jnp


        @genjax.vmap(in_axes=(0,))
        @genjax.gen
        def mapped(x):
            noise1 = genjax.normal(0.0, 1.0) @ "noise1"
            noise2 = genjax.normal(0.0, 1.0) @ "noise2"
            return x + noise1 + noise2


        key = jax.random.key(314159)
        arr = jnp.ones(100)

        tr = jax.jit(mapped.simulate)(key, (arr,))
        print(tr.render_html())
        ```

        Use the [`genjax.GenerativeFunction.vmap`][] method:
        ```python exec="yes" html="true" source="material-block" session="vmap"
        @genjax.gen
        def add_normal_noise(x):
            noise1 = genjax.normal(0.0, 1.0) @ "noise1"
            noise2 = genjax.normal(0.0, 1.0) @ "noise2"
            return x + noise1 + noise2


        mapped = add_normal_noise.vmap(in_axes=(0,))

        tr = jax.jit(mapped.simulate)(key, (arr,))
        print(tr.render_html())
        ```
    """

    gen_fn: GenerativeFunction[R]
    in_axes: InAxes = Pytree.static()

    def __abstract_call__(self, *args) -> Any:
        return jax.vmap(self.gen_fn.__abstract_call__, in_axes=self.in_axes)(*args)

    @staticmethod
    def _static_broadcast_dim_length(in_axes: InAxes, args: tuple[Any, ...]) -> int:
        # We start by triggering a vmap to force all JAX validations to run. If we get past this line we know we have compatible dimensions.
        jax.vmap(lambda *_: None, in_axes=in_axes)(*args)

        # perform the in_axes massaging that vmap performs internally:
        if isinstance(in_axes, int):
            in_axes = (in_axes,) * len(args)
        elif isinstance(in_axes, list):
            in_axes = tuple(in_axes)

        def find_axis_size(axis: int | None, x: Any) -> int | None:
            """Find the size of the axis specified by `axis` for the argument `x`."""
            if axis is not None:
                leaf = jax.tree_util.tree_leaves(x)[0]
                return leaf.shape[axis]

        # tree_map uses in_axes as a template. To have passed vmap validation, Any non-None entry
        # must bottom out in an array-shaped leaf, and all such leafs must have the same size for
        # the specified dimension. Fetching the first is sufficient.
        axis_sizes = jax.tree_util.tree_map(
            find_axis_size,
            in_axes,
            args,
            is_leaf=lambda x: x is None,
        )
        return jtu.tree_leaves(axis_sizes)[0]

    def simulate(
        self,
        key: PRNGKey,
        args: tuple[Any, ...],
    ) -> VmapTrace[R]:
        dim_length = self._static_broadcast_dim_length(self.in_axes, args)
        sub_keys = jax.random.split(key, dim_length)

        # vmapping over `gen_fn`'s `simulate` gives us a new trace with vector-shaped leaves.
        tr = jax.vmap(self.gen_fn.simulate, (0, self.in_axes))(sub_keys, args)

        return VmapTrace.build(self, tr, args, dim_length)

    def generate(
        self,
        key: PRNGKey,
        constraint: ChoiceMap,
        args: tuple[Any, ...],
    ) -> tuple[VmapTrace[R], Weight]:
        dim_length = self._static_broadcast_dim_length(self.in_axes, args)
        idx_array = jnp.arange(dim_length)
        sub_keys = jax.random.split(key, dim_length)

        def _inner(key, idx, args):
            # Here we have to vmap across indices and perform individual lookups because the user might only constrain a subset of all indices. This forces recomputation.
            submap = constraint.get_submap(idx)
            tr, w = self.gen_fn.generate(
                key,
                submap,
                args,
            )
            return tr, w

        tr, weight_v = jax.vmap(_inner, in_axes=(0, 0, self.in_axes))(
            sub_keys, idx_array, args
        )
        w = jnp.sum(weight_v)
        map_tr = VmapTrace.build(self, tr, args, dim_length)
        return map_tr, w

    def project(
        self,
        key: PRNGKey,
        trace: Trace[R],
        selection: Selection,
    ) -> Weight:
        assert isinstance(trace, VmapTrace)

        dim_length = trace.dim_length
        sub_keys = jax.random.split(key, dim_length)

        def _project(key, subtrace):
            return subtrace.project(key, selection)

        weights = jax.vmap(_project)(sub_keys, trace.inner)
        return jnp.sum(weights)

    def edit_choice_map(
        self,
        key: PRNGKey,
        trace: VmapTrace[R],
        constraint: ChoiceMap,
        argdiffs: Argdiffs,
    ) -> tuple[VmapTrace[R], Weight, Retdiff[R], EditRequest]:
        primals = Diff.tree_primal(argdiffs)

        # TODO for McCoy... what if someone has inflated the dimension out from around us? How do we re-use this?
        dim_length = trace.dim_length
        idx_array = jnp.arange(dim_length)
        sub_keys = jax.random.split(key, dim_length)

        def _edit(key, idx, subtrace, argdiffs):
            # Here we have to vmap across indices and perform individual lookups because the user might only constrain a subset of all indices. This forces recomputation.
            subconstraint = constraint(idx)

            new_subtrace, w, retdiff, bwd_request = self.gen_fn.edit(
                key,
                subtrace,
                Update(subconstraint),
                argdiffs,
            )
            assert isinstance(bwd_request, Update)
            inner_chm = bwd_request.constraint
            return (new_subtrace, w, retdiff, inner_chm)

        new_subtraces, w, retdiff, bwd_constraints = jax.vmap(
            _edit, in_axes=(0, 0, 0, self.in_axes)
        )(sub_keys, idx_array, trace.inner, argdiffs)
        w = jnp.sum(w)
        map_tr = VmapTrace.build(self, new_subtraces, primals, dim_length)
        return (
            map_tr,
            w,
            retdiff,
            Update(bwd_constraints),
        )

    def edit_index(
        self,
        key: PRNGKey,
        trace: VmapTrace[R],
        idx: IntArray,
        request: EditRequest,
        argdiffs: Argdiffs,
    ) -> tuple[VmapTrace[R], Weight, Retdiff[R], EditRequest]:
        # For now, we don't allow changes to the arguments for this type of edit.
        assert Diff.static_check_no_change(argdiffs)
        primals = Diff.tree_primal(argdiffs)
        dim_length = trace.dim_length

        trace_slice = jtu.tree_map(lambda v: v[idx], trace.inner)

        def slice_argdiffs(axis: int | None, x: Any) -> Any:
            """Helper function to slice argdiffs based on axis.

            Args:
                axis: The axis to slice along, or None if no slicing needed
                x: The value to slice

            Returns:
                The sliced value if axis is provided, otherwise returns x unchanged
            """
            if axis is None:
                return x
            else:
                return jtu.tree_map(lambda v: jnp.take(v, idx, axis=axis), x)

        # First get the primal. The shape of this is going to match the in_axes shape.
        primal_slice = jax.tree_util.tree_map(
            slice_argdiffs,
            self.in_axes,
            primals,
            is_leaf=lambda x: x is None,
        )
        argdiffs_slice = Diff.tree_diff(primal_slice, Diff.tree_tangent(argdiffs))

        new_trace_slice, w, _, bwd_request = self.gen_fn.edit(
            key,
            trace_slice,
            request,
            argdiffs_slice,
        )

        new_inner_trace = jtu.tree_map(
            lambda v, v_: v.at[idx].set(v_), trace.inner, new_trace_slice
        )

        map_tr = VmapTrace.build(self, new_inner_trace, primals, dim_length)

        # We always set the carried out value to be an unknown change, conservatively.
        retdiff = Diff.unknown_change(map_tr.get_retval())

        return (map_tr, w, retdiff, IndexRequest(idx, bwd_request))

    def edit(
        self,
        key: PRNGKey,
        trace: Trace[R],
        edit_request: EditRequest,
        argdiffs: Argdiffs,
    ) -> tuple[VmapTrace[R], Weight, Retdiff[R], EditRequest]:
        assert isinstance(trace, VmapTrace)

        match edit_request:
            case Update(constraint):
                constraint = edit_request.constraint
                return self.edit_choice_map(
                    key,
                    trace,
                    constraint,
                    argdiffs,
                )
            case IndexRequest(idx, subrequest):
                return self.edit_index(
                    key,
                    trace,
                    idx,
                    subrequest,
                    argdiffs,
                )
            case _:
                raise NotImplementedError

    def assess(
        self,
        sample: ChoiceMap,
        args: tuple[Any, ...],
    ) -> tuple[Score, R]:
        dim_length = self._static_broadcast_dim_length(self.in_axes, args)

        def _inner(idx, args):
            return self.gen_fn.assess(sample(idx), args)

        scores, retvals = jax.vmap(_inner, in_axes=(0, self.in_axes))(
            jnp.arange(dim_length), args
        )
        return jnp.sum(scores), retvals


#############
# Decorator #
#############


def vmap(*, in_axes: InAxes = 0) -> Callable[[GenerativeFunction[R]], Vmap[R]]:
    """
    Returns a decorator that wraps a [`GenerativeFunction`][genjax.GenerativeFunction] and returns a new `GenerativeFunction` that performs a vectorized map over the argument specified by `in_axes`. Traced values are nested under an index, and the retval is vectorized.

    Args:
        in_axes: Selector specifying which input arguments (or index into them) should be vectorized. `in_axes` must match (or prefix) the `Pytree` type of the argument tuple for the underlying `gen_fn`. Defaults to 0, i.e., the first argument. See [this link](https://jax.readthedocs.io/en/latest/pytrees.html#applying-optional-parameters-to-pytrees) for more detail.

    Returns:
        A decorator that converts a [`genjax.GenerativeFunction`][] into a new [`genjax.GenerativeFunction`][] that accepts an argument of one-higher dimension at the position specified by `in_axes`.

    Examples:
        ```python exec="yes" html="true" source="material-block" session="vmap"
        import jax, genjax
        import jax.numpy as jnp


        @genjax.vmap(in_axes=0)
        @genjax.gen
        def vmapped_model(x):
            v = genjax.normal(x, 1.0) @ "v"
            return genjax.normal(v, 0.01) @ "q"


        key = jax.random.key(314159)
        arr = jnp.ones(100)

        # `vmapped_model` accepts an array of numbers:
        tr = jax.jit(vmapped_model.simulate)(key, (arr,))

        print(tr.render_html())
        ```
    """

    def decorator(gen_fn: GenerativeFunction[R]) -> Vmap[R]:
        return Vmap(gen_fn, in_axes)

    return decorator

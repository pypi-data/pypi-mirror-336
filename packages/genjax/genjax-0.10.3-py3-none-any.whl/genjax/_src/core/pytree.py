# Copyright 2024 MIT Probabilistic Computing Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This module contains an abstract data class (called `Pytree`) for implementing JAX's [`Pytree` interface](https://jax.readthedocs.io/en/latest/pytrees.html) on derived classes.

The Pytree interface determines how data classes behave across JAX-transformed function boundaries - it provides a user with the freedom to declare subfields of a class as "static" (meaning, the value of the field cannot be a JAX traced value, it must be a Python literal, or a constant array - and the value is embedded in the `PyTreeDef` of any instance) or "dynamic" (meaning, the value may be a JAX traced value).
"""

from dataclasses import field
from typing import overload

import jax.numpy as jnp
import jax.tree_util as jtu
import penzai.pz as pz
import treescope
from treescope import formatting_util
from typing_extensions import dataclass_transform

from genjax._src.core.typing import (
    Any,
    Callable,
    Generic,
    TypeVar,
    static_check_is_concrete,
)

R = TypeVar("R")


class Pytree(pz.Struct):
    """`Pytree` is an abstract base class which registers a class with JAX's `Pytree`
    system. JAX's `Pytree` system tracks how data classes should behave across JAX-transformed function boundaries, like `jax.jit` or `jax.vmap`.

    Inheriting this class provides the implementor with the freedom to declare how the subfields of a class should behave:

    * `Pytree.static(...)`: the value of the field cannot be a JAX traced value, it must be a Python literal, or a constant). The values of static fields are embedded in the `PyTreeDef` of any instance of the class.
    * `Pytree.field(...)` or no annotation: the value may be a JAX traced value, and JAX will attempt to convert it to tracer values inside of its transformations.

    If a field _points to another `Pytree`_, it should not be declared as `Pytree.static()`, as the `Pytree` interface will automatically handle the `Pytree` fields as dynamic fields.

    """

    @staticmethod
    @overload
    def dataclass(
        incoming: None = None,
        /,
        **kwargs,
    ) -> Callable[[type[R]], type[R]]: ...

    @staticmethod
    @overload
    def dataclass(
        incoming: type[R],
        /,
        **kwargs,
    ) -> type[R]: ...

    @dataclass_transform(
        frozen_default=True,
    )
    @staticmethod
    def dataclass(
        incoming: type[R] | None = None,
        /,
        **kwargs,
    ) -> type[R] | Callable[[type[R]], type[R]]:
        """
        Denote that a class (which is inheriting `Pytree`) should be treated as a dataclass, meaning it can hold data in fields which are declared as part of the class.

        A dataclass is to be distinguished from a "methods only" `Pytree` class, which does not have fields, but may define methods.
        The latter cannot be instantiated, but can be inherited from, while the former can be instantiated:
        the `Pytree.dataclass` declaration informs the system _how to instantiate_ the class as a dataclass,
        and how to automatically define JAX's `Pytree` interfaces (`tree_flatten`, `tree_unflatten`, etc.) for the dataclass, based on the fields declared in the class, and possibly `Pytree.static(...)` or `Pytree.field(...)` annotations (or lack thereof, the default is that all fields are `Pytree.field(...)`).

        All `Pytree` dataclasses support pretty printing, as well as rendering to HTML.

        Examples:
            ```python exec="yes" html="true" source="material-block" session="core"
            from genjax import Pytree
            from genjax.typing import FloatArray
            import jax.numpy as jnp


            @Pytree.dataclass
            # Enforces type annotations on instantiation.
            class MyClass(Pytree):
                my_static_field: int = Pytree.static()
                my_dynamic_field: FloatArray


            print(MyClass(10, jnp.array(5.0)).render_html())
            ```
        """

        return pz.pytree_dataclass(
            incoming,
            overwrite_parent_init=True,
            **kwargs,
        )

    @staticmethod
    def static(**kwargs):
        """Declare a field of a `Pytree` dataclass to be static. Users can provide additional keyword argument options,
        like `default` or `default_factory`, to customize how the field is instantiated when an instance of
        the dataclass is instantiated.` Fields which are provided with default values must come after required fields in the dataclass declaration.

        Examples:
            ```python exec="yes" html="true" source="material-block" session="core"
            @Pytree.dataclass
            # Enforces type annotations on instantiation.
            class MyClass(Pytree):
                my_dynamic_field: FloatArray
                my_static_field: int = Pytree.static(default=0)


            print(MyClass(jnp.array(5.0)).render_html())
            ```

        """
        return field(metadata={"pytree_node": False}, **kwargs)

    @staticmethod
    def field(**kwargs):
        "Declare a field of a `Pytree` dataclass to be dynamic. Alternatively, one can leave the annotation off in the declaration."
        return field(**kwargs)

    ##############################
    # Utility class constructors #
    ##############################

    @staticmethod
    def const(v):
        # The value must be concrete!
        # It cannot be a JAX traced value.
        assert static_check_is_concrete(v)
        if isinstance(v, Const):
            return v
        else:
            return Const(v)

    # Safe: will not wrap a Const in another Const, and will not
    # wrap dynamic values.
    @staticmethod
    def tree_const(v):
        def _inner(v):
            if isinstance(v, Const):
                return v
            elif static_check_is_concrete(v):
                return Const(v)
            else:
                return v

        return jtu.tree_map(
            _inner,
            v,
            is_leaf=lambda v: isinstance(v, Const),
        )

    @staticmethod
    def tree_const_unwrap(v):
        def _inner(v):
            if isinstance(v, Const):
                return v.val
            else:
                return v

        return jtu.tree_map(
            _inner,
            v,
            is_leaf=lambda v: isinstance(v, Const),
        )

    @staticmethod
    def partial(*args) -> Callable[[Callable[..., R]], "Closure[R]"]:
        return lambda fn: Closure[R](args, fn)

    def treedef(self):
        return jtu.tree_structure(self)

    #################
    # Static checks #
    #################

    @staticmethod
    def static_check_tree_structure_equivalence(trees: list[Any]):
        if not trees:
            return True
        else:
            fst, *rest = trees
            treedef = jtu.tree_structure(fst)
            check = all(map(lambda v: treedef == jtu.tree_structure(v), rest))
            return check

    def treescope_color(self) -> str:
        """Computes a CSS color to display for this object in treescope.

        This function can be overridden to change the color for a particular object
        in treescope, without having to register a new handler.

        (note that we are overriding the Penzai base class's implementation so that ALL structs receive colors, not just classes with `__call__` implemented.)

        Returns:
          A CSS color string to use as a background/highlight color for this object.
          Alternatively, a tuple of (border, fill) CSS colors.
        """
        type_string = type(self).__module__ + "." + type(self).__qualname__
        return formatting_util.color_from_string(type_string)

    def render_html(self):
        return treescope.render_to_html(
            self,
            roundtrip_mode=False,
        )


##############################
# Associated utility classes #
##############################


# Wrapper for static values (can include callables).
@Pytree.dataclass
class Const(Generic[R], Pytree):
    """
    JAX-compatible way to tag a value as a constant. Valid constants include Python literals, strings, essentially anything **that won't hold JAX arrays** inside of a computation.

    Examples:
        Instances of `Const` can be created using a `Pytree` classmethod:
        ```python exec="yes" html="true" source="material-block" session="core"
        from genjax import Pytree

        c = Pytree.const(5)
        print(c.render_html())
        ```

        Constants can be freely used across [`jax.jit`](https://jax.readthedocs.io/en/latest/_autosummary/jax.jit.html) boundaries:
        ```python exec="yes" html="true" source="material-block" session="core"
        from genjax import Pytree


        def f(c):
            if c.unwrap() == 5:
                return 10.0
            else:
                return 5.0


        c = Pytree.const(5)
        r = jax.jit(f)(c)
        print(r)
        ```
    """

    val: R = Pytree.static()

    def __call__(self, *args):
        assert isinstance(self.val, Callable), (
            f"Wrapped `val` {self.val} is not Callable."
        )
        return self.val(*args)

    def unwrap(self: Any) -> R:
        """Unwrap a constant value from a `Const` instance.

        This method can be used as an instance method or as a static method. When used as a static method, it returns the input value unchanged if it is not a `Const` instance.

        Returns:
            R: The unwrapped value if self is a `Const`, otherwise returns self unchanged.

        Examples:
            ```python exec="yes" html="true" source="material-block" session="core"
            from genjax import Pytree, Const

            c = Pytree.const(5)
            val = c.unwrap()  # Returns 5

            # Can also be used as static method
            val = Const.unwrap(10)  # Returns 10 unchanged
            ```
        """
        if isinstance(self, Const):
            return self.val
        else:
            return self


# Construct for a type of closure which closes over dynamic values.
@Pytree.dataclass
class Closure(Generic[R], Pytree):
    """
    JAX-compatible closure type. It's a closure _as a [`Pytree`][genjax.core.Pytree]_ - meaning the static _source code_ / _callable_ is separated from dynamic data (which must be tracked by JAX).

    Examples:
        Instances of `Closure` can be created using `Pytree.partial` -- note the order of the "closed over" arguments:
        ```python exec="yes" html="true" source="material-block" session="core"
        from genjax import Pytree


        def g(y):
            @Pytree.partial(y)  # dynamic values come first
            def f(v, x):
                # v will be bound to the value of y
                return x * (v * 5.0)

            return f


        clos = jax.jit(g)(5.0)
        print(clos.render_html())
        ```

        Closures can be invoked / JIT compiled in other code:
        ```python exec="yes" html="true" source="material-block" session="core"
        r = jax.jit(lambda x: clos(x))(3.0)
        print(r)
        ```
    """

    dyn_args: tuple[Any, ...]
    fn: Callable[..., R] = Pytree.static()

    def __call__(self, *args, **kwargs) -> R:
        return self.fn(*self.dyn_args, *args, **kwargs)


def nth(x: Pytree, idx: int | slice | jnp.ndarray):
    """Returns a Pytree in which `[idx]` has been applied to every leaf."""
    return jtu.tree_map(lambda v: v[idx], x)


class PythonicPytree(Pytree):
    """
    A class that adds support for bracket indexing/slicing, sequence-like operations,
    and concatenation to make working with Pytrees more Pythonic. The base class is
    appropriate for Pytrees which have a unform shape over leaves (or at least each
    leaf's initial axis should have the same length).
    """

    def __getitem__(self, idx):
        """Return a pytree in which each leaf has been sliced by `idx`."""
        return nth(self, idx)

    def __len__(self):
        """Return the "length" of the Pytree. This should only be used on
        Pytrees which have a uniform shape over leaves; it operates by
        returning the length of the "first" leaf."""
        return len(jtu.tree_leaves(self)[0])

    def __iter__(self):
        """Returs an iterator which generates each self[i] in order"""
        return (self[i] for i in range(len(self)))

    def __add__(self, other):
        """Concatenates two pytrees, leaf-wise."""
        if not isinstance(other, type(self)):
            raise TypeError(f"Cannot add {type(self)} and {type(other)}")

        def concat_leaves(x, y):
            return jnp.concatenate([x, y])

        return jtu.tree_map(concat_leaves, self, other)

    def prepend(self, child):
        """Prepends a scalar element to the front of each leaf in a Pytree."""
        return jtu.tree_map(lambda x: x[jnp.newaxis], child) + self

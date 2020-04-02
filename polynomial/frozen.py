"""This module defines the Freezable interface and subclasses."""
from math import inf
from polynomial.core import Constant, Polynomial, extract_polynomial, FixedDegreePolynomial


class Freezable:
    """An interface for freezable objects."""

    def _freeze(self):
        """Prevent further modification of self."""
        if not self._is_frozen():
            self._frozen = True

    def _is_frozen(self):
        """Return true if self is frozen."""
        return getattr(self, "_frozen", False)

    def __setitem__(self, key, value):
        """Implement self[x] = y; disallows setting item if frozen."""
        if self._is_frozen():
            raise AttributeError("Can not modify items of frozen object.")
        super().__setitem__(key, value)

    def __setattr__(self, key, value):
        """Implement self.x; disallows setting attr if frozen."""
        if not self._is_frozen():
            object.__setattr__(self, key, value)
        else:
            raise AttributeError("Can not modify frozen object.")


class FrozenPolynomial(Freezable, Polynomial):
    """A polynomial which can not be directly modified."""

    def __init__(self, *args, **kwargs):
        """Create a polynomial from the args, and then freeze it."""
        Polynomial.__init__(self, *args, **kwargs)
        self._vector = tuple(self._vector)
        self._trim = self._no_op
        self._freeze()

    @classmethod
    def zero_instance(cls):
        """Return the zero FrozenPolynomial."""
        return FrozenPolynomial()

    @classmethod
    def from_polynomial(cls, polynomial):
        """Create a frozen copy of the polynomial."""
        return cls(polynomial)

    def _no_op(self):
        """Do nothing. Used as a dummy method."""

    def __repr__(self):
        """Return repr(self)."""
        return "Frozen" + super().__repr__()


class ZeroPolynomial(Freezable, Constant, FixedDegreePolynomial, valid_degrees=-inf):
    """The zero polynomial."""

    def __init__(self):
        """Equivalent to Polynomial()."""
        Constant.__init__(self, 0)
        self._vector = tuple(self._vector)
        self._freeze()

    @classmethod
    def zero_instance(cls):
        """Return an instance of the ZeroPolynomial."""
        return ZeroPolynomial()

    @property
    def const(self):
        """Return self.const, which is always 0."""
        return 0

    @extract_polynomial
    def __mul__(self, other):
        """Return self * other."""
        return other.zero_instance()

    @extract_polynomial
    def __rmul__(self, other):
        """Return other * self."""
        return other.zero_instance()

    def __ipow__(self, other):
        """Return self **= power.

        Does not mutate self.
        """
        if other == 0:
            return Constant(1)

        # This call simply enforces other >= 0 and is int.
        # Could be moved out into a decorator.
        super().__ipow__(other)
        return ZeroPolynomial()

    def __repr__(self):
        """Return repr(self)."""
        return "ZeroPolynomial()"

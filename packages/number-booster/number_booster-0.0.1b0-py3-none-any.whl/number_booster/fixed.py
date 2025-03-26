from .base import BaseBoosterStrategy, NumericType, T


class FixedBoosterStrategy(BaseBoosterStrategy):
    """
    Implementation of the BoosterStrategy interface that boosts the value
    by multiplying it by a fixed value.

    .. note::
        If the multiplier is between 1 and 2, and the value provided is an
        integer, the resulting value after boosting may remain the same.
        Specifically, if the multiplier is close to 1 (within this range),
        the boosted integer value may still round back to 1. In such cases,
        the boost will have no significant effect on the integer value.
    """

    def __init__(self, multiplier: NumericType) -> None:
        self._validate_multiplier(multiplier)

        self._multiplier = multiplier

    def boost(self, value: T) -> T:
        return self._apply_multiplier(value, multiplier=self._multiplier)

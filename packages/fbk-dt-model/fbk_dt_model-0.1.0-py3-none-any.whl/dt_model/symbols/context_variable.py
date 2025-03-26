from __future__ import annotations

import random

from scipy.stats import rv_continuous

from dt_model.symbols._base import SymbolExtender


class ContextVariable(SymbolExtender):
    """
    Class to represent a context variable.
    """

    def __init__(self, name: str) -> None:
        super().__init__(name)

    def support_size(self) -> int:
        pass

    def sample(self, nr: int = 1, *, subset: list | None = None, force_sample: bool = False) -> list:
        """
        Returns a list of tuples (probability, value)  from the support variable or provided
        subset.

        If the distribution discrete, or if a subset is provided, it may return the whole support/subset,
        if its size is not larger that the requested number of sample values.
        Flag force_sample can be used to disallow this behavior and to force the sampling.

        Parameters
        ----------
        nr: int (default 1)
            Number of values to sample.
        subset: list (default None)
            List of values to sample. The whole support is used if this list in None.
        force_sample: bool (default False)
            If True, forces the sampling of the support/subset, even if its size is smaller than nr.

        Returns
        -------
        list
            List of sampled values.
        """
        pass


class UniformCategoricalContextVariable(ContextVariable):
    """
    Class to represent a categorical context variable with uniform probability mass.

    All values returned in sample have the same probability value, even if all the support is returned.
    """

    def __init__(self, name: str, values: list) -> None:
        super().__init__(name)
        self.values = values
        self.size = len(self.values)

    def support_size(self) -> int:
        return self.size

    def sample(self, nr: int = 1, *, subset: list | None = None, force_sample: bool = False) -> list:
        # TODO: subset (if defined) should be a subset of the support (also: with repetitions?)

        (values, size) = (self.values, self.size) if subset is None else (subset, len(subset))

        if force_sample or nr < size:
            assert nr > 0
            return [(1 / nr, r) for r in random.choices(values, k=nr)]

        return [(1 / size, v) for v in values]


class CategoricalContextVariable(ContextVariable):
    """
    Class to represent a categorical context variable.
    """

    def __init__(self, name: str, distribution: dict) -> None:
        super().__init__(name)
        self.distribution = distribution
        self.values = list(self.distribution.keys())
        self.size = len(self.values)
        # TODO: check if distribution is, indeed, a distribution (sum = 1)

    def support_size(self) -> int:
        return self.size

    def sample(self, nr: int = 1, *, subset: list | None = None, force_sample: bool = False) -> list:
        (values, size) = (self.values, self.size) if subset is None else (subset, len(subset))

        if force_sample or nr < size:
            assert nr > 0
            return [(1 / nr, r) for r in random.choices(values, k=nr, weights=[self.distribution[v] for v in values])]

        if subset is None:
            return [(self.distribution[v], v) for v in values]

        subset_probability = [self.distribution[v] for v in values]
        subset_probability_sum = sum(subset_probability)
        return [(p / subset_probability_sum, v) for (p, v) in zip(subset_probability, subset)]


class ContinuousContextVariable(ContextVariable):
    """
    Class to represent a continuous context variable;
    the distribution is any scipy.stats continuous random variable.
    """

    def __init__(self, name: str, rvc: rv_continuous) -> None:
        super().__init__(name)
        self.rvc = rvc
        # TODO: check if distribution is, indeed, a distribution (sum = 1)

    def support_size(self) -> int:
        return -1  # TODO: do better

    def sample(self, nr: int = 1, *, subset: list | None = None, force_sample: bool = False) -> list:
        if force_sample or subset is None or nr < len(subset):
            assert nr > 0
            return [(1 / nr, r) for r in list(self.rvc.rvs(size=nr))]

        subset_probability = list(self.rvc.pdf(subset))
        subset_probability_sum = sum(subset_probability)
        return [(p / subset_probability_sum, v) for (p, v) in zip(subset_probability, subset)]

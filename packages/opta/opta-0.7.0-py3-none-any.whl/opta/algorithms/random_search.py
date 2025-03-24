from opta.algorithms.abstract_algorithm import OptimizationAlgorithm
from opta.tools.vectors import (
    bound_vector,
    generate_vector_in_area,
    generate_vector_in_sphere,
)


class RandomSearch(OptimizationAlgorithm):
    def __init__(self, radius):
        self.radius = radius

    def _initialize(self):
        self.x = generate_vector_in_area(self._search_area)
        self.f_x = self._f(self.x)

    def iterate(self):
        x_new = generate_vector_in_sphere(self.x, self.radius)
        x_new = bound_vector(x_new, self._search_area)
        f_x_new = self._f(x_new)
        if f_x_new < self.f_x:
            self.x = x_new
            self.f_x = f_x_new

    def terminate(self):
        return self.x


def RS(radius):
    return RandomSearch(radius)

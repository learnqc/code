from ch04.util import *

from math import sqrt, cos, sin, pi

import random


def generate_state(n, seed=555):
    # Choose a seed
    random.seed(seed)
    # Generate 4 random probabilities that add up to 1
    probs = [random.random() for _ in range(2 ** n)]
    total = sum(probs)
    probs = [p / total for p in probs]
    # Generate 4 random angles in radians
    angles = [random.uniform(0, 2 * pi) for _ in range(2 ** n)]
    # Build the quantum state array
    return [sqrt(p) * (cos(a) + 1j * sin(a)) for (p, a) in zip(probs, angles)]

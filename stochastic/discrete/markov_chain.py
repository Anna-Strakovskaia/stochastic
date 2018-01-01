"""Markov chain."""
import numpy as np


class MarkovChain(object):
    """Finite state Markov chain.

    A Markov Chain which changes between states according to the transition
    matrix.
    """

    def __init__(self,
                 transition=[[0.5, 0.5], [0.5, 0.5]],
                 initial=None
                 ):
        self.transition = transition
        if initial is None:
            self.initial = [1.0 / len(self.transition)
                            for t in self.transition]
        else:
            self.initial = initial
        self.num_states = len(self.initial)

    @property
    def transition(self):
        """Transition probabilities."""
        return self._transition

    @transition.setter
    def transition(self, values):
        values = np.array(values, copy=False)
        if values.ndim != 2 or values.shape[0] != values.shape[1]:
            raise ValueError("Transition matrix must be a square matrix.")
        for row in values:
            if sum(row) != 1:
                raise ValueError(
                    "Transition matrix is not a proper stochastic matrix.")
        self._transition = values

    @property
    def initial(self):
        """Get the initial state."""
        return self._initial

    @initial.setter
    def initial(self, values):
        values = np.array(values, copy=False)
        if values.ndim != 1 or len(values) != len(self.transition):
            raise ValueError(
                "Initial state probabilities must be one-to-one with states.")
        if sum(values) != 1:
            raise ValueError("Initial state probabilities must sum to 1.")
        self._initial = values

    def __str__(self):
        return "Markov chain with transition matrix = \n{t}".format(
            t=str(self.transition)) + \
            "and initial state probabilities = {p}".format(p=str(self.initial))

    def __repr__(self):
        return "MarkovChain(transition={t})"

    def sample(self, n):
        """Generate a realization of the Markov chain."""
        if not isinstance(n, int):
            raise TypeError("Sample length must be positive integer.")
        if n < 1:
            raise ValueError("Sample length must be at least 1.")

        states = range(self.num_states)

        markovchain = [np.random.choice(states, p=self.initial)]
        count = 1
        while count < n:
            current_transition = self.transition[markovchain[-1]]
            markovchain.append(
                np.random.choice(states, p=current_transition)
            )
            count += 1

        return np.array([self.states[num] for num in markovchain])

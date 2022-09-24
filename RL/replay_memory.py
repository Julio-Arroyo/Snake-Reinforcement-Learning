from collections import deque


class Transition:
    """
    Implements 4-tuple: (s_t, a_t, r_t, s_{t+1}).

    A state is given by the last four frames in the game.
        - s_t: State
        - a_t: action
        - r_t: reward
        - s_t1: next state
    """
    def __init__(self, s_t, a_t, r_t, s_t1):
        self.s_t = s_t
        self.a_t = a_t
        self.r_t = r_t
        self.s_t1 = s_t1

class ReplayMemory:
    """
    Implements the data structure used in Experience Replay.

        - D: deque with max_capacity. Stores Transition objects
    """

    def __init__(self, max_capacity):
        self.max_capacity = max_capacity
        self.experiences = deque(maxlen=self.max_capacity)
    
    def push(self, transition):
        self.experiences.append(transition)

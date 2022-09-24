from replay_memory import *
from dqn_model import *
from Game.Engine.Board import *


N = 1000000  # capacity of replay memory
M = 100  # number of episodes
EPSILON = 1
ACTION_SPACE = set([Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT])


# HELPER FUNCTIONS
def get_initial_state(environment):
    state = deque(maxlen=4)
    for _ in range(4):
        curr_board = environment.board
        state.append(curr_board)
        environment.update(Direction.RIGHT)
    return state


def select_action(Q, curr_state):
    x = random.random()
    if x <= EPSILON:
        return random.choice(ACTION_SPACE)
    else:
        rewards = Q(curr_state)
        return torch.argmax(rewards)


# CORE ALGORITHM
def deep_q_learning_with_experience_replay():
    D = ReplayMemory(N)
    Q = DQN()
    environment = Board()

    for ep_num in range(1, M):
        curr_frames = get_initial_state()
        while True:
            curr_state = torch.tensor(curr_frames)
            action = select_action(Q, curr_state)

            reward = environment.board.update(action)

            curr_frames.append(environment.board)
            next_state = torch.tensor(curr_frames)

            transition = Transition(curr_state, action, reward, next_state)
            D.push(transition)

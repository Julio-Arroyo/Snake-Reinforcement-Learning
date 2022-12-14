from replay_memory import *
from dqn_model import *
import matplotlib.pyplot as plt

import sys
sys.path.insert(0, '/media/julioarroyo/aspen/Snake-Reinforcement-Learning/Game/Engine')

from Board import Board
from direction import Direction


N = 1000000  # capacity of replay memory
M = 100  # number of episodes
EPSILON = 0.1
ACTION_SPACE = [Direction.UP,
                Direction.RIGHT,
                Direction.DOWN,
                Direction.LEFT]
DISCOUNT_FACTOR = 0.9  # gamma
ANNEALING_TIME_STEPS = 1000


# HELPER FUNCTIONS
def get_initial_state(environment):
    state = deque(maxlen=4)
    for _ in range(4):
        curr_board = environment.board
        state.append(curr_board)
        environment.update(Direction.RIGHT)
    return state


def select_action(Q, curr_state, curr_time_step):
    x = random.random()
    threshold = max((-0.9/ANNEALING_TIME_STEPS)*curr_time_step + 1, EPSILON)
    if x <= threshold:
        return random.choice(ACTION_SPACE)
    else:
        print(f"Not random!!!")
        rewards = Q(curr_state.unsqueeze(0).float())
        return torch.argmax(rewards)


def stack_tensors(mini_batch):
    """
    Takes in mini_batch (a list of Transition objects), returns stacked states, next_states, and rewards
    """
    states = torch.zeros((len(mini_batch), mini_batch[0].s_t.size()[0], mini_batch[0].s_t.size()[1], mini_batch[0].s_t.size()[2]))
    actions = torch.zeros((len(mini_batch), 1), dtype=int)
    next_states = torch.zeros((len(mini_batch), mini_batch[0].s_t.size()[0], mini_batch[0].s_t.size()[1], mini_batch[0].s_t.size()[2]))
    rewards = torch.zeros(len(mini_batch))
    for i in range(1, len(mini_batch)):
        curr_transition = mini_batch[i]
        actions[i, 0] = int(mini_batch[i].a_t)
        states[i] = curr_transition.s_t
        next_states[i] = curr_transition.s_t1
        rewards[i] = curr_transition.r_t
    return (states, actions, rewards, next_states)


def pick_best_actions(expected_rewards):
    """
    expected_rewards is a tensor with shape (batch_size, action_space_size).
    
    Returns a vector of dimension batch_size with the best action at every entry.
    """
    batch_size = expected_rewards.shape[0]
    best_expected_rewards = torch.zeros(batch_size)
    for i in range(batch_size):
        best_expected_rewards[i] = torch.max(best_expected_rewards[i])
    return best_expected_rewards


def get_final_states_mask(rewards):
    final_states_idx = []
    for i in range(rewards.size()[0]):
        if rewards[i] == -1:
            final_states_idx.append(i)
    return final_states_idx


# CORE ALGORITHM
def deep_q_learning_with_experience_replay():
    D = ReplayMemory(N)

    # Q represents our policy network, old_Q is the function approximator of the optimal action-value function
    Q = DQN()
    old_Q = DQN()
    old_Q.load_state_dict(Q.state_dict())
    optimizer = torch.optim.RMSprop(Q.parameters())
    curr_time_step = 0
    best_snake_size = 1
    best_time_alive = 0

    for ep_num in range(1, M):
        print(f"Episode #{ep_num}")
        environment = Board()
        curr_frames = get_initial_state(environment)
        time_alive = 0
        while True:
            curr_state = torch.tensor(curr_frames)
            action = select_action(Q, curr_state, curr_time_step)
            # print("BEFORE:")
            # print(f"Snake head: {environment.snake.head} tail: {environment.snake.tail}, size: {environment.snake.size}")
            # print(environment.board)
            reward = environment.update(action)
            # print(f"Current action: {action} led to reward: {reward} in ep: {ep_num} with time: {time_alive}.")
            # print()
            # print("AFTER:")
            # print(f"Snake head: {environment.snake.head} tail: {environment.snake.tail}, size: {environment.snake.size}")
            # print(environment.board)

            curr_frames.append(environment.board)
            next_state = torch.tensor(curr_frames)

            transition = Transition(curr_state, action, reward, next_state)
            D.push(transition)

            mini_batch = D.get_mini_batch()
            (mb_states, mb_actions, mb_rewards, mb_next_states) = stack_tensors(mini_batch)

            predictions = Q(mb_states).gather(1, mb_actions).squeeze()

            future_best_actions = pick_best_actions(old_Q(mb_next_states))
            future_best_actions[get_final_states_mask(mb_rewards)] = 0
            targets = mb_rewards + DISCOUNT_FACTOR*future_best_actions

            loss_func = torch.nn.MSELoss()
            loss = loss_func(predictions, targets)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            old_Q.load_state_dict(Q.state_dict())

            if reward == -1:
                print(f"Time alive: {time_alive}")
                break
            time_alive += 1
            curr_time_step += 1
        if time_alive > best_time_alive:
            best_time_alive = time_alive
        if environment.snake.size > best_snake_size:
            best_snake_size = environment.snake.size

    print(f"RESULTS: best size: {best_snake_size}, best time: {best_time_alive}")


if __name__ == "__main__":
    deep_q_learning_with_experience_replay()

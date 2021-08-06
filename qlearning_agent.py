import time
import joblib
import numpy as np
from game import Game

game_env = Game()

car_passed = []
crashed = []

LEARNING_RATE = 0.09
DISCOUNT = 0.95
EPISODES = 25000

DISCRETE_OSV_SIZE = [10] * len(game_env.state_HIGH)
discrete_osv_win_size = (game_env.state_HIGH -
                         game_env.state_LOW)/DISCRETE_OSV_SIZE

q_table = np.random.uniform(
    low=-2, high=0, size=(DISCRETE_OSV_SIZE+[len(game_env.action_set)]))


def get_discrete_state(state):
    discrete_state = (state - game_env.state_LOW)/discrete_osv_win_size
    return tuple(discrete_state.astype(np.int))


for eps in range(EPISODES):
    discrete_state = get_discrete_state(game_env.reset())
    done = False
    while not done:
        action = np.argmax(q_table[discrete_state])
        new_state, reward, done = game_env.game_play(action)
        new_discrete_state = get_discrete_state(new_state)
        if not done:
            max_future_q = np.max(q_table[new_discrete_state])
            current_q = q_table[discrete_state + (action,)]
            new_q = (1-LEARNING_RATE)*current_q+LEARNING_RATE * \
                (reward+DISCOUNT*max_future_q)
            q_table[discrete_state+(action,)] = new_q
        discrete_state = new_discrete_state

        print('Crashed : ', game_env.crashed)
        print('Episode : ', eps)
        time.sleep(0.001)

    crashed.append(game_env.crashed)
    car_passed.append(game_env.car_passed)

    # because it will take too much time to complete 25000 episodes,
    # just for testing purpose we are doing only 100 episodes.
    if eps == 100:
        break

joblib.dump(crashed, 'crashed.pkl')
joblib.dump(car_passed, 'car_passed.pkl')

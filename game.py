import os
import time
import random
import numpy as np


class Game:
    def __init__(self):
        self.screen_buf = []  # virtual screen buffer
        self.road_wl = ['||', '   ', '|', '   ', '||']   # road with line
        self.road_wol = ['  ', '   ', ' ', '   ', '  ']   # road without line

        # my cars part 1, here two backslash (\\) represent only one backslash (\)
        self.m_car_1 = '/^\\'
        self.m_car_2 = ']#['
        self.m_car_3 = '=-='

        self.o_car_3 = '=-='  # other's car part 3
        self.o_car_2 = '!#!'  # other's car part 2
        # other's car part 1, here two backslash (\\) represent only one backslash (\)
        self.o_car_1 = '\\_/'

        self.lcar = -1
        self.rcar = -1
        self.mcar = 1

        self.distance = 0

        self.state_LOW = np.array([-1, -1, 0])
        self.state_HIGH = np.array([15, 15, 2])
        self.action_set = np.array([0, 1])

        # load the screen cleaner for different OS
        if os.name == 'nt':
            self.clr_scr_cmd = 'cls'
        else:
            self.clr_scr_cmd = 'clear'
        os.system(self.clr_scr_cmd)

        self.car_passed = 0
        self.crashed = 0

    def reset(self):
        self.screen_buf = []

        self.lcar = -1
        self.rcar = -1
        self.mcar = 1

        self.distance = 0
        self.crashed = 0
        self.car_passed = 0

        return [self.lcar, self.rcar, self.mcar]

    def screen_1(self):
        for i in range(4):
            self.screen_buf.append(self.road_wl.copy())
            self.screen_buf.append(self.road_wol.copy())
            self.screen_buf.append(self.road_wol.copy())

    def screen_2(self):
        for i in range(4):
            self.screen_buf.append(self.road_wol.copy())
            self.screen_buf.append(self.road_wl.copy())
            self.screen_buf.append(self.road_wol.copy())

    def screen_3(self):
        for i in range(4):
            self.screen_buf.append(self.road_wol.copy())
            self.screen_buf.append(self.road_wol.copy())
            self.screen_buf.append(self.road_wl.copy())

    def render_screen_buf(self):
        os.system(self.clr_scr_cmd)
        for i in range(12):
            tmp_row = ''
            for j in self.screen_buf[i]:
                tmp_row += j
            self.screen_buf[i] = tmp_row

        print('-'*11)
        print('\n'.join(self.screen_buf))
        print('-'*11)

        self.screen_buf = []

    def game_play(self, action):
        self.mcar = action
        # becoming car from the left lane's probability is 1/10
        # check if the left lane is free or not and the random state
        # and also check if the differece between two car is greater than 6 unit or not
        if self.lcar == -1 and (self.rcar == -1 or abs(self.lcar-self.rcar) > 6) and random.randint(0, 10) == 10:
            self.lcar = 0
        # becoming car from the right lane's probability is 1/12
        # check if the right lane is free or not and the random state
        # and also check if the differece between two car is greater than 6 unit or not
        if self.rcar == -1 and (self.lcar == -1 or abs(self.lcar-self.rcar) > 6) and random.randint(0, 12) == 12:
            self.rcar = 0

        if self.distance % 3 == 0:
            self.screen_1()
        elif self.distance % 3 == 1:
            self.screen_2()
        else:
            self.screen_3()
        self.distance += 1

        # if any other car is on the screen then set it properly and update the state of that car
        if self.lcar > -1:
            if self.lcar < 12:
                self.screen_buf[self.lcar][1] = self.o_car_1
            if self.lcar > 0 and self.lcar < 12:
                self.screen_buf[self.lcar-1][1] = self.o_car_2
            if self.lcar > 1 and self.lcar < 12:
                self.screen_buf[self.lcar-2][1] = self.o_car_3
            self.lcar += 1

        if self.rcar > -1:
            if self.rcar < 12:
                self.screen_buf[self.rcar][3] = self.o_car_1
            if self.rcar > 0 and self.rcar < 12:
                self.screen_buf[self.rcar-1][3] = self.o_car_2
            if self.rcar > 1 and self.rcar < 12:
                self.screen_buf[self.rcar-2][3] = self.o_car_3
            self.rcar += 1

        if self.mcar == 0:
            self.screen_buf[9][1] = self.m_car_1
            self.screen_buf[10][1] = self.m_car_2
            self.screen_buf[11][1] = self.m_car_3
        elif self.mcar == 1:
            self.screen_buf[9][3] = self.m_car_1
            self.screen_buf[10][3] = self.m_car_2
            self.screen_buf[11][3] = self.m_car_3

        self.render_screen_buf()

        reward = 10
        if self.distance >= 1000:
            done = True
        else:
            done = False

        if self.lcar > 8 and self.mcar == 0:
            print('Car crashed!')
            self.crashed += 1
            reward = -999
        elif self.rcar > 8 and self.mcar == 1:
            print('Car crashed!')
            self.crashed += 1
            reward = -999

        if self.lcar > 8 and self.mcar == 1:
            reward = 30
        elif self.rcar > 8 and self.mcar == 0:
            reward = 30

        # if the other car goes out of the screen then the it reset the state of that car
        if self.lcar == 14:
            self.lcar = -1
            self.car_passed += 1
            reward = 50
        if self.rcar == 14:
            self.rcar = -1
            reward = 50
            self.car_passed += 1

        return ([self.lcar, self.rcar, self.mcar], reward, done)


# testing part only runs when we directly run this file, not after importing this file to another file
if __name__ == "__main__":
    # the main loop which run the game and call the qlearner in every cycle
    game = Game()
    for i in range(10):
        for j in range(1001):
            cur_state, reward, done = game.game_play(random.randint(0, 1))
            print("\t\t", cur_state, reward, done)
            if reward == -999:
                break
            # the delay is kept high to see that is really hapenning. because in high
            # frame per second we can't see what's actually hapenning.
            time.sleep(0.5)

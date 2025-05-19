from cube import Cube
from constants import *
from utility import *

import random
import random
import numpy as np


class Snake:
    body = []
    turns = {}



    def __init__(self, color, pos, file_name):
        self.color = color
        self.head = Cube(pos, color=color)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1
        self.episode_rewards = []          # this is for check reward
        self.lengh = []                    # this is for check lengh of snake
        self.win = 0                       # this is for check win snake
        
        
        try:
            # After we train our snake, we can save its Q_table and use the previous Q_table when we run our code again.
            self.q_table = np.load(file_name) 
            
        except:
            # first initialize a Q_table with empty np array
            # when the call update Q_table function, according bellman equation Q_table is updated
            # after converge Q_table , we can find the best policy
            self.q_table = np.zeros((66669,4))


        # in this 3 line code we setup learning rate , discount factor , epsilon for our train snake
        self.lr = 0.1 # Learning rate
        self.discount_factor = 0.9 # Discount factor
        self.epsilon = 0.00 # Epsilon



    # In this function, we come and tell the snake the best choice from the Q_table you have
    def get_optimal_policy(self, n_state):
        list_nstate = self.q_table[n_state]
        arg = np.argmax(self.q_table[n_state])
        
        ###  dar in ghesmat ma in mahdodiat ra migozarim ke mar nemitavaned dar khalaf jahati ke alan harkat mikonad harkat konad
        
        if (arg == 0) and (self.dirnx == 1) : # chap and sorat rast
            sorted_indices = np.argsort(list_nstate)
            arg = sorted_indices[-2]
            return arg
        
        elif (arg == 1) and (self.dirnx == -1) : # rast and sorat chap
            sorted_indices = np.argsort(list_nstate)
            arg = sorted_indices[-2]
            return arg
        
        elif (arg == 2) and (self.dirny == 1) : # up and sorat down
            sorted_indices = np.argsort(list_nstate)
            arg = sorted_indices[-2]
            return arg
        
        elif (arg == 3) and (self.dirny == -1) : # down and sorat up
            sorted_indices = np.argsort(list_nstate)
            arg = sorted_indices[-2]
            return arg
        
        return arg


    def make_action(self, n_state):
        chance = random.random()
        if chance < self.epsilon:
            action = random.randint(0, 3)
        else:
            action = self.get_optimal_policy(n_state)
        return action


    # in this function we update Q_table
    def update_q_table(self, n_state, action, n_next_state, reward):
        c_q_value = self.q_table[n_state][action]
        best_next_action = np.argmax(self.q_table[n_next_state])
        target = (1- self.lr) * c_q_value + (self.lr * (reward + (self.discount_factor * best_next_action)))
        self.q_table[n_state][action] = target


    def create_state(self , snack , other_snake):
        state = np.zeros((3 , 3))
        my_headSnake_x, my_headSnake_y = self.head.pos
        
        for i in range(-1, 2):
            for j in range(-1, 2):
                temp_x = my_headSnake_x + i
                temp_y = my_headSnake_y + j

                if temp_x <= 0 or temp_x >= 19 or temp_y <= 0 or temp_y >= 19:
                    state[i + 1, j + 1] = 1  # Wall
                elif (temp_x, temp_y) == self.head.pos:
                    state[i + 1, j + 1] = 2  # my Head
                elif (temp_x , temp_y) == other_snake.head.pos :
                    state[i + 1, j + 1] = 3 # other Head
                elif (temp_x, temp_y) in [cube.pos for cube in other_snake.body]:
                    state[i + 1, j + 1] = 4  # other Snake body
                elif (temp_x, temp_y) in [cube.pos for cube in self.body]:
                    state[i + 1, j + 1] = 5  # my Snake body
                elif (temp_x, temp_y) == snack.pos:
                    state[i + 1, j + 1] = 6  # Snack
                    
        if self.head.pos[0] < snack.pos[0] :
            if self.head.pos[1] < snack.pos[1] :
                t = 1
            elif self.head.pos[1] == snack.pos[1] :
                t = 2
            elif self.head.pos[1] > snack.pos[1] :
                t = 3
        elif self.head.pos[0] > snack.pos[0] :
            if self.head.pos[1] < snack.pos[1] :
                t = 4
            elif self.head.pos[1] == snack.pos[1] :
                t = 5
            elif self.head.pos[1] > snack.pos[1] :
                t = 6
        elif self.head.pos[0] == snack.pos[0] :
            if self.head.pos[1] < snack.pos[1] :
                t = 7
            elif self.head.pos[1] > snack.pos[1] :
                t = 8
            elif self.head.pos[1] == snack.pos[1] :
                t = 9
                
        n_state = int(t + state[0][1] * 10 + state[1][0] * 100 + state[1][2] * 1000 + state[2][1] * 10000)
        return n_state
    
    
    def move(self, snack, other_snake):
        n_state = self.create_state(snack , other_snake) # Create state
        action = self.make_action(n_state)

        if action == 0: # Left
            self.dirnx = -1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        elif action == 1: # Right
            self.dirnx = 1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        elif action == 2: # Up
            self.dirny = -1
            self.dirnx = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        elif action == 3: # Down
            self.dirny = 1
            self.dirnx = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                c.move(c.dirnx, c.dirny)

        # Create new state after moving and other needed values and return them
        n_new_state = self.create_state(snack , other_snake)
        self.lengh.append(len(self.body))
        return n_state , n_new_state , action
            
          
    def check_out_of_board(self):
        headPos = self.head.pos
        if headPos[0] >= ROWS - 1 or headPos[0] < 1 or headPos[1] >= ROWS - 1 or headPos[1] < 1:
            self.reset((random.randint(3, 18), random.randint(3, 18)))
            return True
        return False
    
    
    def calc_reward(self, snack, other_snake):
        reward = 0
        win_self, win_other = False, False
        
        down = tuple(np.array(self.head.pos) + np.array((0 , 1)))
        up = tuple(np.array(self.head.pos) - np.array((0 , 1)))
        left = tuple(np.array(self.head.pos) - np.array((1 , 0)))
        right = tuple(np.array(self.head.pos) + np.array((1 , 0)))

        if down == snack.pos:
            if self.dirny == -1 :
                reward -= 100
            elif self.dirny == 1 : ###########
                reward += 100
        elif down[1] > 18 :
            if self.dirny == +1 :
                reward -= 80
            else:
                reward += 40
        elif down == other_snake.head.pos :
            if self.dirny == +1 :
                reward -= 80
            else :
                reward += 40
        elif down in [cube.pos for cube in other_snake.body] :
            if self.dirny == +1 :
                reward -= 80
            else :
                reward += 40
        elif down in [cube.pos for cube in self.body] :
            if self.dirny == +1 :
                reward -= 80
            else :
                reward += 40
            
        if up == snack.pos:
            if self.dirny == +1:
                reward -= 100
            elif self.dirny == -1 :
                reward += 100
        elif up[1] < 1 :
            if self.dirny == -1 :
                reward -= 80
            else:
                reward += 40
        elif up == other_snake.head.pos :
            if self.dirny == -1 :
                reward -= 80
            else :
                reward += 40
        elif up in [cube.pos for cube in other_snake.body] :
            if self.dirny == -1 :
                reward -= 80
            else :
                reward += 40
        elif up in [cube.pos for cube in self.body] :
            if self.dirny == -1 :
                reward -= 80
            else :
                reward += 40
                
        if left == snack.pos:
            if self.dirnx == 1:
                reward -= 100
            elif self.dirnx == -1:
                reward += 100
        elif left[0] < 1 :
            if self.dirnx == -1:
                reward -= 80
            else :
                reward += 40
        elif left == other_snake.head.pos :
            if self.dirnx == -1:
                reward -= 80
            else :
                reward += 40
        elif left in [cube.pos for cube in other_snake.body] :
            if self.dirnx == -1:
                reward -= 80
            else :
                reward += 40
        elif left in [cube.pos for cube in self.body] :
            if self.dirnx == -1:
                reward -= 80
            else :
                reward += 40
        
        if right == snack.pos:
            if self.dirnx == -1:
                reward -= 100
            elif self.dirnx == 1 :
                reward += 100
        elif right[0] >= 19 :
            if self.dirnx == 1:
                reward -= 80
            else :
                reward += 40
        elif right == other_snake.head.pos :
            if self.dirnx == 1:
                reward -= 80
            else :
                reward += 40
        elif right in [cube.pos for cube in other_snake.body] :
            if self.dirnx == 1:
                reward -= 80
            else :
                reward += 40
        elif right in [cube.pos for cube in self.body] :
            if self.dirnx == 1:
                reward -= 80
            else :
                reward += 40
        
        if self.head.pos[0] >= 3 and self.head.pos[0] <= 16 and self.head.pos[1] >= 3 and self.head.pos[1] <= 16:
            reward += 20
        
        temp = np.array(snack.pos) - np.array(self.head.pos)
        sorat = np.array([self.dirnx , self.dirny])
        dot = np.dot(temp , sorat)
        if dot > 0 :
            reward += 60
        else :
            reward -= 60
        
        if self.check_out_of_board():
            # Punish the snake for getting out of the board
            reward -= 400 # 300
            win_other = True
            if win_other == True :
                self.reset((random.randint(1, 18), random.randint(1, 18)))
        
            
        if self.head.pos == snack.pos:
            self.addCube()
            snack = Cube(randomSnack(ROWS, self), color=(0, 255, 0))
            # Reward the snake for eating
            reward += 300
            
        if self.head.pos in list(map(lambda z: z.pos, self.body[1:])):
            # Punish the snake for hitting itself
            reward -= 400 ## 300
            win_other = True
            if win_other == True :
                self.reset((random.randint(1, 18), random.randint(1, 18)))
            
            
        if self.head.pos in list(map(lambda z: z.pos, other_snake.body)):
            
            if self.head.pos != other_snake.head.pos:
                # Punish the snake for hitting the other snake
                reward -= 400 ## 300
                win_other = True
            else:
                if len(self.body) > len(other_snake.body):
                    # Reward the snake for hitting the head of the other snake and being longer
                    reward += 20
                    win_self = True
                elif len(self.body) == len(other_snake.body):
                    # No winner
                    reward -= 400 ## 300
                else:
                    # Punish the snake for hitting the head of the other snake and being shorter
                    reward -= 400 ## 300
                    win_other = True
                    
            # reset(self, other_snake)
        if win_self == True :
            self.win += 1
            other_snake.reset((random.randint(1, 18), random.randint(1, 18)))
        elif win_other == True :
            other_snake.win += 1
            self.reset((random.randint(1, 18), random.randint(1, 18)))
                
        # if len(self.episode_rewards) != 0 :
        #     temp_reward = self.episode_rewards[-1]
        #     self.episode_rewards.append(temp_reward + reward)
        # else :
        #     self.episode_rewards.append(reward)
            
        self.episode_rewards.append(reward)
        return snack, reward, win_self, win_other
    
    
    def reset(self, pos):
        self.head = Cube(pos, color=self.color)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1


    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1]), color=self.color))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1]), color=self.color))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1), color=self.color))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1), color=self.color))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy



    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


    def save_q_table(self, file_name):
        np.save(file_name, self.q_table)

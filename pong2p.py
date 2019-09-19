import numpy as np
import random as rnd

class State:

    def __init__(self):
        # Down, up, stay
        #self.move_counts = np.zeros(3)
        self.move_counts = [0 for x in range(3)]
        # Goodness of each above move
        #self.move_qualities = np.zeros(3)
        self.move_qualities = [0 for x in range(3)]

class Pong:

    def __init__(self):
        self.ball_x = 0.5
        self.ball_y = 0.5
        self.velocity_x = 0.03
        self.velocity_y = 0.01
        self.paddle_height = 0.2
        self.paddle_y = 0.4
        self.paddle_x = 1
        self.state = [[[[[State() for a in range(12)] for b in range(12)] for c in range(3)] for d in range(2)] for e in range(12)]
        self.p2_paddle_y = 0.4
        self.p2_paddle_height = 0.2

def get_paddle_height(paddle_y):
    if paddle_y == 0.8:
        return 11
    else:
        return int((12*paddle_y) / 0.8)

def get_ball_x_dir(velocity_x):
    # Left
    if velocity_x < 0:
        return 0
    # Right
    else:
        return 1

def get_ball_y_dir(velocity_y):
    # Down
    if velocity_y > 0.015:
        return 0
    # Up
    elif velocity_y < -0.015:
        return 1
    # Horizontal
    else:
        return 2

def get_grid_col(ball_x):
    if ball_x < 0:
        return 0
    else:
        return min(int(ball_x*12), 11)

def get_grid_row(ball_y):
    return min(int(ball_y*12), 11)

def p2_decide_paddle_movement(paddle_y, velocity_y, ball_y):
    movement = ball_y + velocity_y
    # Down
    if movement > paddle_y + 0.2:
        return 0
    # Up
    elif movement < paddle_y:
        return 1
    # Stay
    else:
        return 2
    # # Down
    # if ball_y > paddle_y + 0.2:
    #     return 0
    # # Up
    # elif ball_y < paddle_y:
    #     return 1
    # else:
    #     return 0

def decide_paddle_movement(cur_state):
    # 3% chance to move paddle at random
    random_move = rnd.random()
    if random_move < 0.03:
        if random_move < 0.02:
            return 0
        elif random_move < 0.01:
            return 1
        else:
            return 2
    # Purposeful move
    # If a move has been done less than 100 times, do it
    lowest_freq_of_move = min(cur_state.move_counts)
    if lowest_freq_of_move < 100:
        move_to_do = cur_state.move_counts.index(lowest_freq_of_move)
    # If all moves done > 100 times, choose one with best Q value
    else:
        best_Q = max(cur_state.move_qualities)
        move_to_do = cur_state.move_qualities.index(best_Q)
    return move_to_do

def p2_move_paddle(action, paddle_y):
    # Down
    if action == 0:
        if paddle_y + 0.02 < 0.8:
            return paddle_y + 0.02
        else:
            return 0.8
    # Up
    elif action == 1:
        if paddle_y - 0.02 > 0:
            return paddle_y - 0.02
        else:
            return 0
    # Stay
    elif action == 2:
        return paddle_y

def move_paddle(action, paddle_y):
    # Down
    if action == 0:
        #if paddle_y + 0.04 < 1 - paddle_height:
        if paddle_y + 0.04 < 0.8:
            return paddle_y + 0.04
        else:
            #return 1 - paddle_height
            return 0.8
    # Up
    elif action == 1:
        if paddle_y - 0.04 > 0:
            return paddle_y - 0.04
        else:
            return 0
    # Stay
    elif action == 2:
        return paddle_y

def update_ball(ball_x, ball_y, velocity_x, velocity_y, paddle_y, p2_paddle_y):
    punish_reward = ""
    ball_x += velocity_x
    ball_y += velocity_y
    # Above top wall
    if ball_y < 0:
        ball_y = -ball_y
        velocity_y = -velocity_y
    # Below bottom wall
    elif ball_y > 1:
        ball_y = 2 - ball_y
        velocity_y = -velocity_y
    # Game over/bounce off P2 paddle
    if ball_x < 0:
        if ball_y >= p2_paddle_y and ball_y <= (p2_paddle_y + 0.2):
            punish_reward = "P2 Rebound"
            ball_x = 2 - ball_x
            U = rnd.uniform(-0.015, 0.015)
            V = rnd.uniform(-0.03, 0.03)
            velocity_x = -velocity_x + U
            velocity_y = velocity_y + V
            if velocity_x > -0.03 and velocity_x < 0.03:
                if velocity_x < 0:
                    velocity_x -= 0.03
                else:
                    velocity_x += 0.03
            # Checks in problem statements
            if abs(velocity_x) > 1:
                if velocity_x > 1:
                    velocity_x = 0.95
                else:
                    velocity_x = -0.95
            if abs(velocity_y) > 1:
                if velocity_y > 1:
                    velocity_y = 0.95
                else:
                    velocity_y = -0.95
        # Paddle misses ball
        else:
            punish_reward = "P2 Miss"
    # Game over/bounce off P1 paddle
    elif ball_x >= 1:
        if ball_y >= paddle_y and ball_y <= (paddle_y + 0.2):
            punish_reward = "P1 Rebound"
            ball_x = 2 - ball_x
            U = rnd.uniform(-0.015, 0.015)
            V = rnd.uniform(-0.03, 0.03)
            velocity_x = -velocity_x + U
            velocity_y = velocity_y + V
            if velocity_x > -0.03 and velocity_x < 0.03:
                if velocity_x < 0:
                    velocity_x -= 0.03
                else:
                    velocity_x += 0.03
            # Checks in problem statements
            if abs(velocity_x) > 1:
                if velocity_x > 1:
                    velocity_x = 0.95
                else:
                    velocity_x = -0.95
            if abs(velocity_y) > 1:
                if velocity_y > 1:
                    velocity_y = 0.95
                else:
                    velocity_y = -0.95
        # Paddle misses ball
        else:
            punish_reward = "P1 Miss"
    return ball_x, ball_y, velocity_x, velocity_y, punish_reward

def reset(pong):
    pong.ball_x = 0.5
    pong.ball_y = 0.5
    pong.velocity_x = 0.03
    pong.velocity_y = 0.01
    pong.paddle_height = 0.2
    pong.paddle_y = 0.4
    pong.pd_paddle_y = 0.4

def simulate():
    p = Pong()
    # Learning rate
    C = 50
    alpha = 1
    # Discount factor
    gamma = 0.9
    p1_rebound_test_count = 0
    p2_rebound_test_count = 0
    p1_wins = 0
    p2_wins = 0
    # Train 100,000 times, test 1000 times
    for i in range(51001):
        if i%10000 == 0:
            print(i)
        reset(p)
        while(1):
            if i < 50000:
                p.p2_paddle_height = 1
            else:
                p.p2_paddle_height = 0.2
            #print(p.paddle_y)
            # 0. Get current state
            paddle_y = get_paddle_height(p.paddle_y)
            ball_v_x = get_ball_x_dir(p.velocity_x)
            ball_v_y = get_ball_y_dir(p.velocity_y)
            ball_x = get_grid_col(p.ball_x)
            ball_y = get_grid_row(p.ball_y)
            #print(paddle_y, ball_v_x, ball_v_y, ball_x, ball_y)
            #print(len(p.state), len(p.state[0]), len(p.state[0][0]), len(p.state[0][0][0]), len(p.state[0][0][0][0]))
            cur_state = p.state[paddle_y][ball_v_x][ball_v_y][ball_x][ball_y]
            # 1. Choose paddle movement
            paddle_move = decide_paddle_movement(cur_state)
            p2_paddle_move = p2_decide_paddle_movement(p.p2_paddle_y, p.velocity_y, p.ball_y)
            # Move paddle
            new_paddle_y = move_paddle(paddle_move, p.paddle_y)
            p.paddle_y = new_paddle_y
            p2_new_paddle_y = p2_move_paddle(p2_paddle_move, p.p2_paddle_y)
            #p.p2_paddle_y = p2_new_paddle_y ##
            # Update state move count
            cur_state.move_counts[paddle_move] += 1
            # 2. Move ball
            p.ball_x, p.ball_y, p.velocity_x, p.velocity_y, punish_reward = \
            update_ball(p.ball_x, p.ball_y, p.velocity_x, p.velocity_y, p.paddle_y, p.p2_paddle_y)
            # Punish move if didn't hit paddle/reward if it did
            R = 0
            if punish_reward != "":
                if punish_reward == "P1 Rebound":
                    R = 1
                elif punish_reward == "P1 Miss":
                    R = -1
            # 3. Get new state
            new_paddle_y = get_paddle_height(p.paddle_y)
            new_ball_v_x = get_ball_x_dir(p.velocity_x)
            new_ball_v_y = get_ball_y_dir(p.velocity_y)
            new_ball_x = get_grid_col(p.ball_x)
            new_ball_y = get_grid_row(p.ball_y)
            #print(new_paddle_y, new_ball_v_x, new_ball_v_y, new_ball_x, new_ball_y)
            next_state = p.state[new_paddle_y][new_ball_v_x][new_ball_v_y][new_ball_x][new_ball_y]
            # 4. Update "goodness" of move  - Q function
            alpha = C/(C + cur_state.move_counts[paddle_move])
            cur_state.move_qualities[paddle_move] += alpha*(R + gamma*max(next_state.move_qualities) - cur_state.move_qualities[paddle_move])
            if i >= 50000:
                if punish_reward == 'P1 Rebound':
                    p1_rebound_test_count += 1
                elif punish_reward == 'P2 Rebound':
                    p2_rebound_test_count += 1
                elif punish_reward == 'P1 Miss':
                    p2_wins += 1
                    break
                elif punish_reward == 'P2 Miss':
                    p1_wins += 1
                    break
            if R == -1:
                break

    print('P1 Rebound Test Rate =', p1_rebound_test_count/1000, 'per trial')
    print('P2 Rebound Test Rate =', p2_rebound_test_count/1000, 'per trial')
    print('P1 Wins =', p1_wins, 'P2 Wins =', p2_wins)
    print('AI Win Rate =', p1_wins/1000)

simulate()
# AI Win Rate = 0.977

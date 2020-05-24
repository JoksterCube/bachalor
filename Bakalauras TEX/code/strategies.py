import warnings
warnings.filterwarnings('ignore')

import argparse, os, sys
import numpy as np
import gym, gym_sokoban
from gym_sokoban.envs import SokobanEnv
from stable_baselines import A2C, ACER, PPO2
from stable_baselines.common.cmd_util import make_vec_env
from stable_baselines.common.policies import CnnPolicy, CnnLstmPolicy, CnnLnLstmPolicy
from my_wrappers import ActionWrapper

steps = int(1e7)
room_dimensions = (7, 7)
box_number = 1
max_steps_in_env = 200
n_envs = 64

def main(name, algorithm, policy):
    save_file_name = f"{name}_sokoban_10M"
    tensorboard = f"./{name}_sokoban_tensorboard"

    sokoban_env = SokobanEnv(dim_room=room_dimensions, max_steps=max_steps_in_env, num_boxes=box_number)
    create_env_fn = lambda: ActionWrapper(sokoban_env, new_action_space=5)
    env = make_vec_env(create_env_fn, n_envs=n_envs)

    model = algorithm(policy, env, verbose=1, tensorboard_log=tensorboard)
    print(f'Starting {name} model')

    model.learn(total_timesteps=steps, reset_num_timesteps=False)
    model.save(save_file_name)
    print(f"Training done, model saved:", save_file_name)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Training algorithms")
    parser.add_argument('--algorithm', type=str, default=None)
    parser.add_argument('--policy', type=str, default=None)
    args = parser.parse_args()
    algorithm = args.algorithm.upper()
    policy = args.policy.upper()
    
    if algorithm == 'A2C':
        algorithm_fn = A2C
    elif algorithm == 'ACER':
        algorithm_fn = ACER
    elif algorithm== 'PPO2':
        algorithm_fn = PPO2
    else:
        algorithm_fn = None   
        
    if policy == 'CNN':
        policy_fn = CnnPolicy
    elif policy == 'CNNLSTM':
        policy_fn = CnnLstmPolicy
    elif policy == 'CNNLNLSTM':
        policy_fn = CnnLnLstmPolicy
    else:
        policy_fn = None    
        
    if algorithm_fn is not None and policy_fn is not None:
        main(algorithm, algorithm_fn, policy_fn)
    else:
        print("No or incorrect algorithm or policy name given.")
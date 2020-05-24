import warnings
warnings.filterwarnings('ignore')
from distutils.util import strtobool
import argparse, os, sys
import numpy as np
import tensorflow as tf
from typing import Optional
from collections import deque
import gym, gym_sokoban
from gym_sokoban.envs import SokobanEnv
from stable_baselines import A2C, ACER, PPO2
from stable_baselines.common.vec_env import SubprocVecEnv, DummyVecEnv
from stable_baselines.common.cmd_util import make_vec_env
from stable_baselines.common.policies import CnnLnLstmPolicy
from stable_baselines.common.callbacks import BaseCallback, CallbackList, CheckpointCallback, EveryNTimesteps, EventCallback
from my_wrappers import ActionWrapper, ExposeCompletedEnvironments, CombinedWrappers
verbose=1
save_dir = "./saves/"
tensorboard_path = "./tensorboard"
max_amount_of_steps_per_iteration = int(1e8)
iteration_steps = int(1e6)
iteration_count_before_progressing = 5
min_iteration_solverate_to_progress = 0.5
min_abs_solverate_and_avg_difference_to_progress = .01
ignore_avg_treshold_to_progress = .9
room_dimensions = (10, 10)
max_steps_in_env = 100
initial_box_number = 1
max_box_number = 2
n_envs = 16
def create_current_env(num_boxes, vec_env_cls=SubprocVecEnv):
    env_kwargs = {'dim_room':room_dimensions,  'max_steps':max_steps_in_env, 'num_boxes':num_boxes}
    wrapper = lambda env: CombinedWrappers(env, wrappers=[ActionWrapper, ExposeCompletedEnvironments], new_action_space=5, done_info_keyword=("all_boxes_on_target"))
    env = make_vec_env(SokobanEnv, n_envs=n_envs, env_kwargs=env_kwargs, wrapper_class=wrapper, vec_env_cls=vec_env_cls)
    return env
def copy_and_replace_model(create_fn, model, env, tensorboard_full_path):
    new_model = create_fn(CnnLnLstmPolicy, env=env, verbose=verbose, tensorboard_log=tensorboard_full_path)
    print("New model created")
    model_parameters = model.get_parameters()
    new_model.load_parameters(model_parameters)
    print("Parameters copied")
    return new_model 
class TensorboardCompletionTrackingCallback(BaseCallback):
    def __init__(self, verbose=0):
        super(TensorboardCompletionTrackingCallback, self).__init__(verbose)
    def _on_step(self) -> bool:
        dones = self.training_env.get_attr('env_done')
        completes = self.training_env.get_attr('env_completed')
        for done, complete in zip(dones, completes):
            if done:
                writer = self.locals['writer']
                if writer is not None:
                    value = int(complete)
                    summary = tf.Summary(value=[tf.Summary.Value(tag='completions', simple_value=value)])
                    self.locals['writer'].add_summary(summary, self.num_timesteps) 
        return True
class CompletionEvaluationCallback(BaseCallback):
    def __init__(self, box_number = 1, verbose=1):
        super(CompletionEvaluationCallback, self).__init__(verbose)
        self.current_solverate_queue = deque(maxlen=iteration_count_before_progressing)
        self.current_local_iteration = 0
        self.box_number = box_number
    def _on_step(self) -> bool:       
        # Track current iteration
        self.current_local_iteration += 1
        # Get each environment complete ratio 
        env_ratios = [fn() for fn in self.training_env.get_attr('completed_ratio')]
        env_ratios_cleaned = [0 if np.isnan(x) else x for x in env_ratios]
        # Reset totals for next iteration
        for reset_totals_fn in self.training_env.get_attr('reset_totals'):
            reset_totals_fn()
        # Calculate total solverate from all of the environements
        solverate = np.mean(env_ratios_cleaned)            
        self.current_solverate_queue.append(solverate)
        if self.verbose > 0:
            print(f"Model's current solverate is '{solverate}'.")
        # Progress if minimum amount of iterations have passed
        if self.current_local_iteration < iteration_count_before_progressing:
            if self.verbose > 0:
                print(f"Current iteration number {self.current_local_iteration} is below minimum before progressing iteration number {iteration_count_before_progressing}.")
            return True
        if self.verbose > 0:
            print(f"Current iteration number {self.current_local_iteration} is sufficient to progress.")
        # Pass if solverate is above the minimum expected solvrate for progression
        if solverate < min_iteration_solverate_to_progress:
            if self.verbose > 0:
                print(f"Current iteration solverate {solverate} is not sufficient to progress. Min required: {min_iteration_solverate_to_progress}.")
            return True
        if self.verbose > 0:
            print(f"Current iteration solverate {solverate} is sufficient to progress.")
        avg_solverate = np.mean(self.current_solverate_queue)
        abs_diff = abs(solverate - avg_solverate)
        # Pass for progress with difficulty if abs diff of average over last few and current is less then expected
        # Ignore above condition if solverate is above the ignore treshold, ignore this if this is the last run
        if (abs_diff > min_abs_solverate_and_avg_difference_to_progress and 
            (self.box_number >= max_box_number or 
             solverate < ignore_avg_treshold_to_progress)):
            if self.verbose > 0:
                print(f"Current iteration solverate {solverate} and last {iteration_count_before_progressing} iteration average solvareate {avg_solverate} absolute differacnce {abs_diff} is not sufficient to progress.")
            return True
        if self.verbose > 0:
            print(f"Current iteration solverate {solverate} and last {iteration_count_before_progressing} iteration average solvareate {avg_solverate} absolute differacnce {abs_diff} is sufficient to progress.")
        self.current_local_iteration = 0
        return False       
def main(name, create_fn, load_fn=None, load_filename = None, starting_block = None, copy=False, save_path=None):
    # Create initial environment
    current_box_number = initial_box_number if starting_block is None else starting_block
    env = create_current_env(current_box_number)
    # Create model
    print(f"Creating {name} model")
    tensorboard_full_path = os.path.join(tensorboard_path, name)
    if load_filename is None:
        model = create_fn(CnnLnLstmPolicy, env=env, verbose=verbose, tensorboard_log=tensorboard_full_path)
        print(f"{name} model created")
    else:
        load_path = os.path.join(save_dir, name, load_filename)
        model = load_fn(load_path, env=env, verbose=verbose, tensorboard_log=tensorboard_full_path)
        print(f"{name} model loaded")
        if copy:
            model = copy_and_replace_model(create_fn, model, env, tensorboard_full_path)
    # Save path
    full_save_path = os.path.join(save_dir, name)
    if save_path is not None:
        full_save_path = os.path.join(full_save_path, save_path)
    # Create callbacks
    tensorboard_callback = TensorboardCompletionTrackingCallback()
    checkpoint_callback = CheckpointCallback(save_freq=1, save_path=full_save_path)
    iteration_test_callback = CompletionEvaluationCallback(box_number=current_box_number)
    iteration_callback_list = CallbackList([checkpoint_callback, iteration_test_callback])
    iteration_callback = EveryNTimesteps(n_steps=iteration_steps, callback=iteration_callback_list)
    callbacks = CallbackList([tensorboard_callback, iteration_callback])
    # Start Curriculum learning
    while True:
        if verbose > 0:
            print(f"Starting training with {current_box_number} boxes")  
        # Create unique name for each iteration and different box numbers
        log_name = f"{name}_box_{current_box_number}_v2"
        # Train model for this iteration
        model.learn(total_timesteps=max_amount_of_steps_per_iteration, tb_log_name=log_name, reset_num_timesteps=False, callback=callbacks)
        # Save final run of the current difficulty
        save_name = f'{name}_box_{current_box_number}_final'
        final_save_path = os.path.join(save_dir, name)
        if save_path is not None:
            final_save_path = os.path.join(final_save_path, save_path)
        final_save_path = os.path.join(final_save_path, save_name)
        model.save(final_save_path)
        current_box_number += 1
        if current_box_number <= max_box_number:
            if verbose > 0:
                print(f"Increasing difficutly to {current_box_number} boxes")  
            # Close previous environment to save resources
            model.get_env().close()
            new_env = create_current_env(current_box_number)
            if copy:
                model = copy_model(create_fn, model, new_env, tensorboard_full_path)
            else:
                model.set_env(new_env)
        else:
            break
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Training algorithms")
    parser.add_argument('--algorithm', type=str, default=None)
    parser.add_argument('--load', type=str, default=None)
    parser.add_argument('--starting', type=int, default=None)
    parser.add_argument('--copy', type=lambda b: bool(strtobool(b)), default=False)
    parser.add_argument('--save', type=str, default=None)
    args = parser.parse_args()
    algorithm = args.algorithm.upper()
    load_filename = args.load
    starting_block = None  if args.starting is not None and args.starting > max_box_number else args.starting
    copy =  args.copy
    save_path =  args.save
    if algorithm == 'A2C':
        create_fn = A2C
        load_fn = A2C.load
    elif algorithm == 'ACER':
        create_fn = ACER
        load_fn = ACER.load
    elif algorithm == 'PPO2':
        create_fn = PPO2
        load_fn = PPO2.load
    else:
        create_fn = None
        load_fn = None
    if create_fn is not None:
        main(algorithm, create_fn, load_fn, load_filename, starting_block, copy, save_path)
    else:
        print("No or incorrect algorithm name given.")
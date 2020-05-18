import gym
import numpy as np

class ActionWrapper(gym.Wrapper):
    def __init__(self, env, new_action_space=None, **kvars):
        super(ActionWrapper, self).__init__(env)
        from gym.spaces.discrete import Discrete
        if new_action_space is not None:
            self.env.action_space = Discrete(new_action_space)     
           
class ExposeCompletedEnvironments(gym.Wrapper):
    def __init__(self, env, done_info_keyword=None, **kvars):
        super(ExposeCompletedEnvironments, self).__init__(env)
        self.done_info_keyword = done_info_keyword
        self.env_done = False
        self.env_completed = False
        self.cleaned = True
        
        self.reset_totals()
    
    def reset(self, **kwargs):
        observation = super(ExposeCompletedEnvironments, self).reset(**kwargs)
        self.cleaned = True
        return observation
    
    def step(self, action):
        observation, reward, done, info = super(ExposeCompletedEnvironments, self).step(action)
        if self.cleaned:
            self._clean_env()
        if done:
            self.env_done = True
            if self.done_info_keyword in info:
                self.env_completed = info[self.done_info_keyword]
            else:
                self.env_completed = False; 
            info['puzzle_completed'] = self.env_completed
            
            self.total_completed_num += int(self.env_completed)
            self.total_done_num += 1
        return observation, reward, done, info
    
    def completed_ratio(self):
        if self.total_done_num > 0:
            return self.total_completed_num / self.total_done_num
        return np.nan
    
    def _clean_env(self):
        self.env_done = False
        self.env_completed = False
        self.cleaned = False 
    
    def reset_totals(self):
        self.total_completed_num = 0
        self.total_done_num = 0
        
    def __getattr__(self, name):
        if name is "completed_ratio":
            return self.completed_ratio
        elif name is "reset_totals":
            return self.reset_totals
        elif name is "env_done":
            return self.env_done
        elif name is "env_completed":
            return self.env_completed
        attr = super(ExposeCompletedEnvironments, self).__getattr__(name)
        if attr is not None:
            return attr
            
class CombinedWrappers(gym.Wrapper):
    def __init__(self, env, wrappers=[], **kvars):
        for wrapper in wrappers:
            env = wrapper(env, **kvars)
        super(CombinedWrappers, self).__init__(env)
            
            
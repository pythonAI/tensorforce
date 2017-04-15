# Copyright 2017 reinforce.io. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""
Deep Q-learning from demonstration. This agent pre-trains from demonstration data.
 
Original paper: 'Learning from Demonstrations for Real World Reinforcement Learning'

https://arxiv.org/abs/1704.03732
"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from six.moves import xrange
from tensorforce.config import create_config
from tensorforce.replay_memories import ReplayMemory
from tensorforce.agents import RLAgent


#TODO Michael: should probably inherit from memory_agent
class DQFDAgent(RLAgent):

    model = None

    default_config = {
        'batch_size': 32,
        'update_rate': 0.25,
        'target_network_update_rate': 0.0001,
        'min_replay_size': 5e4,
        'deterministic_mode': False,
        'use_target_network': False,
        'update_repeat': 1
    }

    def __init__(self, config, scope='dqfd_agent'):
        """
        
        :param config: 
        :param scope: 
        """
        self.config = create_config(config, default=self.default_config)
        self.model = None

        # This is the online memory
        self.replay_memory = ReplayMemory(**self.config)

        # This is the demonstration memory that we will fill with observations before starting
        # the main training loop
        self.demo_memory = ReplayMemory(**self.config)

        self.step_count = 0

        # Called p in paper, controls
        self.expert_sampling_ratio = self.config.expert_sampling_ratio

        self.update_repeat = self.config.update_repeat
        self.batch_size = self.config.batch_size
        self.update_steps = int(round(1 / self.config.update_rate))
        self.use_target_network = self.config.use_target_network

        if self.use_target_network:
            self.target_update_steps = int(round(1 / self.config.target_network_update_rate))

        self.min_replay_size = self.config.min_replay_size

        if self.__class__.model:
            self.model = self.__class__.model(self.config, scope)

    def add_demo_observation(self, state, action, reward, terminal):
        """
        Adds observations to demo memory. 

        """
        self.demo_memory.add_experience(state, action, reward, terminal)

    def pretrain(self, steps=1):
        """
        
        :param steps: Number of pre-train gradient updates.
        
        """

    def add_observation(self, state, action, reward, terminal):
        """
        Adds observations, updates via sampling from memories according to update rate.
        In the DQFD case, we sample from the online replay memory and the demo memory with
        the fractions controlled by a hyperparameter p called 'expert sampling ratio.
        
        :param state: 
        :param action: 
        :param reward: 
        :param terminal: 
        :return: 
        """
        pass

    def get_action(self, *args, **kwargs):
        """
        Get action from model, as in DQN.
        
        :param state: 
        """

        action = self.model.get_action(*args, **kwargs)

        return action

    def save_model(self, path):
        self.model.save_model(path)

    def load_model(self, path):
        self.model.load_model(path)

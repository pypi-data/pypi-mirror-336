import numpy as np 
import matplotlib.pyplot as plt


class GenericMDP:

    def __init__(self, 
                 states, 
                 actions, 
                 probabilities, 
                 rewards, 
                 discount_rate, 
                 max_iterations,
                 tolerance = 1e-6, 
                 len_x = None, 
                 len_y = None, 
                 reward_list = None, 
                 reward_values = None, 
                 problem_type = 'generic'):

        self.tolerance = tolerance
        self.states = states
        self.actions = actions
        self.probabilities = probabilities
        self.discount_rate = discount_rate
        self.max_iter = max_iterations
        self.rewards_dict = rewards
        self.problem_type = problem_type

        if self.problem_type == 'gridworld':
            self.len_x = len_x
            self.len_y = len_y
            self.rewards_list = reward_list
            self.rewards_list = reward_list
            self.reward_values = reward_values



    def _bellmans_eq(self, state, values_dict:dict, extract_policy = False):
        '''
        This will be a generic bellmans which takes in the probabilities, rewards and states
        
        intentionally sparse for the time being to avoid wasted computation
        '''

        action_space = len(self.actions)
        V_k = np.zeros(action_space) 

        for action in range(action_space):
            # this must be one scary looking summation
            V_k[action] = sum(self.probabilities[state][action][s_prime] * \
                              (self.rewards_dict.get(state, {}).get(action, {}).get(s_prime,0) + \
                              self.discount_rate * values_dict.get(s_prime, 0)) \
                              for s_prime in self.probabilities[state][action])
        if extract_policy == False:
            return max(V_k)
        else:
            return np.where(V_k == max(V_k))

    def _value_iteration(self):
        '''
        value iteration function which we have to 
        
        soon, this will need termination conditions
        '''

        V_k = {}   
        k = 0
        while k < self.max_iter:
            V_k_minus_1 = V_k.copy()
            for state in self.states:
                V_k[state] = self._bellmans_eq(state = state, values_dict = V_k_minus_1)
            k += 1
            # lets see if we have reached tolerance, only after doing multiple iterations through incase of a slow start 
            if k > 10:
                value_change = sum(abs(V_k[k] - V_k_minus_1[k]) for k in V_k)
                if value_change/ len(V_k) < self.tolerance:
                    print(f'Tolerance of {self.tolerance} was met after {k} iterations. Terminating now.')
                    return V_k
        print(f'Tolerance of {self.tolerance} was not met after {self.max_iter} iterations. Terminating now.')
        return V_k
    
    def _extract_policy_gridworld(self):
        '''
        Description: 
            We will only do this once as to reduce computational load on the solver
        Inputs: 
            Value function
        Returns: 
            Policy
        '''
        Values = self.values
        policy = {}
        for state in self.states:
            policy[state] = self._bellmans_eq(state = state, values_dict = Values, extract_policy=True)
        return policy
    
    def _extract_policy_generic(self):
        '''
        Description: 
            We will only do this once as to reduce computational load on the solver
        Inputs: 
            Value function
        Returns: 
            Policy
        '''
        Values = self.values
        policy = {}
        for state in self.states:
            policy[state] = self._bellmans_eq(state = state, values_dict = Values, extract_policy=True)
            print(f'If in state: {state}, the optimal action is: {self.actions[int(policy[state][0][0])]}')
        return policy

    def _policy_plotter(self):
        arrow_map = {
            0: (0,  1),   # Up
            1: (0, -1),   # Down
            2: (1,  0),   # Right
            3: (-1, 0),   # Left
        }
        # unpack array of actions
        array = np.zeros((self.len_x, self.len_y), dtype=int)
        for (i, j), chosen_action in self.policy.items():
            array[i, j] = chosen_action[0][0]

        rows, cols = array.shape
        X, Y = np.meshgrid(np.arange(cols), np.arange(rows))

        U = np.zeros_like(array, dtype=float)
        V = np.zeros_like(array, dtype=float)

        for i in range(rows):
            for j in range(cols):
                if (i, j) in self.rewards_list:
                    plt.text(
                        i, 
                        j, 
                        f'{self.reward_values[self.rewards_list.index((i, j))]}',
                        ha='center', va='center', fontsize=12, fontweight='bold', color='red'
                    )
                else:
                    dx, dy = arrow_map[array[i, j]]
                    U[i, j] = dx
                    V[i, j] = dy   

        plt.quiver(Y, X, V, U, pivot='middle', scale=1, scale_units='xy', angles='xy')

        #plt.gca().invert_yaxis() 
        plt.xticks(np.arange(rows))
        plt.yticks(np.arange(cols))
        plt.grid(True)
        plt.title("Policy Visualisation")
        plt.show()
 


    def __call__(self):
        '''call funciton'''
        self.values = self._value_iteration()
        if self.problem_type == 'gridworld':
            self.policy = self._extract_policy_gridworld()
            self._policy_plotter()
        else:
            self.policy = self._extract_policy_generic()

        return self.policy, self.values

class Gridworld_Constructor:
    '''here we can contain all of the helper functions which will allow us to make the transition matricies we need'''
    def __init__(self, 
                 reward_states, 
                 reward_values, 
                 probability_of_intended_move, 
                 len_x, 
                 len_y, 
                 border_penalty,
                 ):
        self.border_penalty = border_penalty
        self.reward_states = reward_states
        self.reward_values = reward_values
        self.accuracy = probability_of_intended_move
        self.len_x = len_x
        self.len_y = len_y
        self.states = [(i, j) for i in range(self.len_x) for j in range(self.len_y)]
        self.corners =[(0, 0), (0, self.len_y - 1), (self.len_x - 1, 0), (self.len_x - 1, self.len_y - 1)]
        self.actions =[(1,  0),    # right
                       (-1, 0),   # left
                       (0,  1),    # up
                       (0, -1)]   # down


    def _populate_probabilities_rewards(self, state):
        sub_dirs = {}
        for index, _ in enumerate(self.actions):
            sub_dirs[index] = {}
            for corner in self.corners:
                sub_dirs[index][(corner)] = 0.25
        return sub_dirs

    def _populate_probabilities_usual(self, state):
        sub_dirs = {}
        for index, intended_move in enumerate(self.actions):
            sub_dirs[index] = {}
            for actual_move in self.actions:
                value = 0.7 if intended_move == actual_move else 0.1
                sub_dirs[index][(state[0] + actual_move[0], state[1] + actual_move[1])] = value
        return sub_dirs

    def _populate_probabilities_edge(self, state):
        sub_dirs = {}

        for index, intended_move in enumerate(self.actions):
            sub_dirs[index] = {}

            for actual_move in self.actions:
                new_row = state[0] + actual_move[0]
                new_col = state[1] + actual_move[1]

                # Check if out of bounds
                if (new_row < 0 or new_row >= self.len_x or
                    new_col < 0 or new_col >= self.len_y):
                    # Remain in the same cell 
                    new_state = state
                else:
                    new_state = (new_row, new_col)

                value = 0.7 if intended_move == actual_move else 0.1
                sub_dirs[index][new_state] = value

        return sub_dirs

    def _populate_positive_rewards(self, state, reward_value):
        sub_dirs = {}
        for index, _ in enumerate(self.actions):
            sub_dirs[index] = {}
            for corner in self.corners:
                sub_dirs[index][(corner)] = reward_value
        return sub_dirs

    def _populate_negative_rewards(self, state, reward_value):
        sub_dirs = {}
        for index, _ in enumerate(self.actions):
            sub_dirs[index] = {}
            for actual_move in self.actions:
                sub_dirs[index][(state[0] + actual_move[0], state[1] + actual_move[1])] = reward_value
        return sub_dirs


    def _populate_edge_penalties(self, state):
        sub_dirs = {}

        for index, _ in enumerate(self.actions):
            sub_dirs[index] = {}

            for actual_move in self.actions:
                new_row = state[0] + actual_move[0]
                new_col = state[1] + actual_move[1]

                # Check if out of bounds
                if (new_row < 0 or new_row >= self.len_x or
                    new_col < 0 or new_col >= self.len_y):
                    # Remain in the same cell 
                    new_state = state
                else:
                    new_state = (new_row, new_col)

                value = self.border_penalty if new_state == state else 0
                sub_dirs[index][new_state] = value

        return sub_dirs

    def _fit_rewards_and_probabilities(self):
        probabilities = {}
        for state in self.states:
            i, j = state
            if state in self.reward_states and self.reward_values[self.reward_states.index(state)] > 0:
                # teleportation step
                probabilities[state] = self._populate_probabilities_rewards(state)
            elif 0 < i < self.len_x-1 and 0 < j < self.len_y-1:
                # we are in standard operating conditions, make usual sub directories
                probabilities[state] = self._populate_probabilities_usual(state)
            else: # we must be at an edge
                probabilities[state] = self._populate_probabilities_edge(state)


        rewards = {}
        for state in self.states:
            i, j = state
            if state in self.reward_states and self.reward_values[self.reward_states.index(state)] > 0:
                # we are about to teleport
                rewards[state] = self._populate_positive_rewards(state, self.reward_values[self.reward_states.index(state)])
            elif state in self.reward_states and self.reward_values[self.reward_states.index(state)] < 0:
                # we get a reward but do not teleport
                rewards[state] = self._populate_negative_rewards(state, self.reward_values[self.reward_states.index(state)])
            elif i in [0, self.len_x-1] or j in [0, self.len_y-1]:
                rewards[state] = self._populate_edge_penalties(state)

        return probabilities, rewards

    def __call__(self):
        self.probabilities, self.rewards = self._fit_rewards_and_probabilities()
        return self.probabilities, self.rewards
import ast

from .Gridworld_Constructor import Gridworld_Constructor
from .MDP import GenericMDP



def Value_Iteration():
    print("\n")
    print("Welcome to the MDP Solver! Is this a GridWorld problem?", flush=True)
    problem_type_validity = False
    
    while not problem_type_validity:
        problem_type = input("Enter 'Gridworld', or 'Other' (no quotation marks):  ").strip()
        if problem_type.lower() == "gridworld":
            problem_type_validity = True
            gridworld_helper_func()
        elif problem_type.lower() == 'other':
            problem_type_validity = True
            generic_helper_func()
        else:
            print("Please check spelling of problem type.")

def gridworld_helper_func():
    """CLI for collecting all inputs required to specify a GridWorld."""
    
    # Get grid dimensions
    dimension_type_validity = False
    while not dimension_type_validity:
        print("\nConfigure Gridworld dimensions and rewards")
        dimensions = input("Enter GridWorld dimensions as [len_x, len_y]: ").strip()
        try:
            dimensions = dimensions.strip("[]")
            dimensions = [int(x.strip()) for x in dimensions.split(",")]
            if len(dimensions) == 2 and all(x > 0 for x in dimensions):
                dimension_type_validity = True
            else:
                print("Ensure both dimensions are positive integers.")
        except ValueError:
            print("Invalid input. Enter dimensions as [x, y] with positive integers.")

    len_x, len_y = dimensions
    print(f"Gridworld dimensions set to: {len_x} x {len_y}")

    # Get reward cells (list of tuples)
    reward_cells_validity = False
    while not reward_cells_validity:
        reward_cells = input(f"Enter reward cell coordinates as [(x1, y1), (x2, y2), ...]. Grid size is {len_x}x{len_y}. Use zero indexing: ").strip()
        try:
            reward_cells = eval(reward_cells)  # Convert to list of tuples

            if (
                isinstance(reward_cells, list)
                and all(isinstance(t, tuple) and len(t) == 2 for t in reward_cells)
                and all(0 <= t[0] < len_x and 0 <= t[1] < len_y for t in reward_cells)  # ✅ Check bounds
            ):
                reward_cells_validity = True
            else:
                print(f"Invalid coordinates. Ensure tuples are within (0 ≤ x < {len_x-1}, 0 ≤ y < {len_y-1}).")
        
        except (SyntaxError, ValueError, TypeError):
            print("Invalid input. Enter coordinates as [(x1, y1), (x2, y2), ...].")

    print(f"Reward cells set to: {reward_cells}")

    # Get reward values (list of numbers, same length as reward cells)
    reward_values_validity = False
    while not reward_values_validity:
        reward_values = input(f"Enter reward values as a list [{len(reward_cells)} values]: ").strip()
        try:
            reward_values = eval(reward_values)  # Convert to list
            if isinstance(reward_values, list) and len(reward_values) == len(reward_cells) and all(isinstance(x, (int, float)) for x in reward_values):
                reward_values_validity = True
            else:
                print(f"Invalid format. Enter {len(reward_cells)} numbers in a list, e.g., [5, -10, 3].")
        except (SyntaxError, ValueError, TypeError):
            print(f"Invalid input. Enter a list of {len(reward_cells)} numeric values.")

    print(f"Reward values set to: {reward_values}")

    # Get edge penalty (negative number)
    edge_penalty_validity = False
    while not edge_penalty_validity:
        print("\nEdge penalties and probability of missstep")
        edge_penalty = input("Enter the edge penalty (negative number): ").strip()
        try:
            edge_penalty = float(edge_penalty)
            if edge_penalty < 0:
                edge_penalty_validity = True
            else:
                print("Edge penalty must be a negative number.")
        except ValueError:
            print("Invalid input. Enter a negative number.")

    print(f"Edge penalty set to: {edge_penalty}")

    # Get probability of misstep (0 < p < 1)
    probability_of_misstep_validity = False
    while not probability_of_misstep_validity:
        probability_of_misstep = input("Enter probability of misstep (0 < p < 1): ").strip()
        try:
            probability_of_misstep = float(probability_of_misstep)
            if 0 < probability_of_misstep < 1:
                probability_of_misstep_validity = True
            else:
                print("Probability must be greater than 0 and less than 1.")
        except ValueError:
            print("Invalid input. Enter a number between 0 and 1.")

    print(f"Probability of misstep set to: {probability_of_misstep}")

    # Get max iterations (positive integer)
    max_iterations_validity = False
    while not max_iterations_validity:
        print("\nInput solver parameters")
        max_iterations = input("Enter the maximum number of iterations (positive integer): ").strip()
        try:
            max_iterations = int(max_iterations)
            if max_iterations > 0:
                max_iterations_validity = True
            else:
                print("Must be a positive integer.")
        except ValueError:
            print("Invalid input. Enter a positive integer.")

    # Get tolerance (small positive float)
    tolerance_validity = False
    while not tolerance_validity:
        tolerance = input("Enter the solver tolerance (e.g., 1e-6): ").strip()
        try:
            tolerance = float(tolerance)
            if tolerance > 0:
                tolerance_validity = True
            else:
                print("Tolerance must be a positive number.")
        except ValueError:
            print("Invalid input. Enter a small positive float (e.g., 0.00001 or 1e-5).")

    # Get discount rate
    discount_rate_validity = False
    while not discount_rate_validity:
        discount_rate = input("Enter the discount rate (0 ≤ γ < 1): ").strip()
        try:
            discount_rate = float(discount_rate)
            if 0 <= discount_rate < 1:
                discount_rate_validity = True
            else:
                print("Discount rate must be in the range [0, 1).")
        except ValueError:
            print("Invalid input. Enter a float between 0 and 1 (e.g., 0.9).")

    # Create GridWorld instance
    gridworld = Gridworld_Constructor(
        reward_states=reward_cells, 
        reward_values=reward_values, 
        probability_of_intended_move = 1 - probability_of_misstep, 
        len_x=len_x, 
        len_y=len_y, 
        border_penalty=edge_penalty
    ) 
    probabilities, rewards = gridworld()

    print("\nGridWorld successfully created! Initialising solver")

    solver = GenericMDP(states = [(i, j) for i in range(len_x) for j in range(len_y)], 
                        actions = [(1, 0),    # right
                                   (-1, 0),   # left
                                   (0, 1),    # up
                                   (0, -1)], 
                        probabilities = probabilities, 
                        rewards = rewards, 
                        discount_rate = discount_rate, 
                        max_iterations = max_iterations,
                        tolerance=tolerance, 
                        len_x = dimensions[0], 
                        len_y = dimensions[1], 
                        reward_list = reward_cells, 
                        reward_values = reward_values, 
                        problem_type = 'gridworld')()





def generic_helper_func():
    """CLI for collecting all inputs required to specify a general mdp"""

    # Get state space
    while True:
        print("\nDefine States and Actions")
        states = input("Name available states as ['state_1', 'state_2', ...]: ").strip()
        try:
            states = ast.literal_eval(states)
            if isinstance(states, list) and all(isinstance(x, str) for x in states):
                break
            else:
                print("Ensure your input is a list of strings, e.g. ['Healthy', 'Sick', ...]")
        except (ValueError, SyntaxError):
            print("Invalid input. Use the format ['Healthy', 'Sick']")

    # Get action space
    while True:
        actions = input("Name available actions as ['action_1', 'action_2']: ").strip()
        try:
            actions = ast.literal_eval(actions)
            if isinstance(actions, list) and all(isinstance(x, str) for x in actions):
                break
            else:
                print("Ensure your input is a list of strings, e.g. ['Run', 'Walk']")
        except (ValueError, SyntaxError):
            print("Invalid input. Use the format ['Run', 'Walk']")

    print("States:", states)
    print("Actions:", actions)

    probabilities = {}
    print("\nNow define transition probabilties")
    if len(states) == 2:
        for s in states: 
            temp = {}
            for index, action in enumerate(actions):
                while True:
                    try:
                        probability = input(
                            f"If in state={s} and you take action={action}, "
                            f"what is the probability of entering state={states[0]}? "
                        ).strip()

                        p_float = float(probability)
                        
                        # Probability must be in [0, 1]
                        if not (0 <= p_float <= 1):
                            raise ValueError("Probability must be between 0 and 1.")

                        # The sum for 2 states is forced to 1
                        # state[1] = 1 - p_float
                        p_complement = round(1.0 - p_float, 4)
                        if not (0 <= p_complement <= 1):
                            raise ValueError(
                                "Calculated complement is not between 0 and 1, "
                                "check your value."
                            )
                        print(f"Probability for transition from state {s} to {states[1]} following action {action} defaulted to {p_complement}")
                        # If all checks pass, store the result
                        temp2 = {
                            states[0]: round(p_float, 4),
                            states[1]: round(p_complement, 4),
                        }
                        temp[index] = temp2
                        break  # exit the while loop
                    except ValueError as e:
                        print(f"Invalid input: {e}")
                
            probabilities[s] = temp

    else:
        for s in states:
            temp = {}
            for index, action in enumerate(actions):
                while True:
                    # gather probabilities for all next-states in a loop
                    temp2 = {}
                    valid = True
                    total_probability = 0.0

                    for s_prime in states:
                        prob_input = input(
                            f"If in state={s} and you take action={action}, "
                            f"what is the probability of entering state={s_prime}? "
                        ).strip()

                        try:
                            p_float = float(prob_input)
                            if not (0 <= p_float <= 1):
                                raise ValueError("Probability must be between 0 and 1.")
                            temp2[s_prime] = p_float
                            total_probability += p_float
                        except ValueError as e:
                            print(f"Invalid input for transition to {s_prime}: {e}")
                            valid = False
                            break  # break out of the s_prime loop

                    if not valid:
                        print("Retry entering probabilities for this action.\n")
                        continue

                    # Now check if sum of probabilities is 1
                    # (we allow a small tolerance, e.g. 1e-5)
                    if abs(total_probability - 1.0) > 1e-5:
                        print(
                            f"The sum of the probabilities you entered is "
                            f"{total_probability:.5f}, which does not equal 1. "
                            "Please re-enter.\n"
                        )
                        continue

                    # If we get here, everything is valid (i hope)
                    temp[index] = temp2
                    break  # break from the while loop for this action

            probabilities[s] = temp

    print("Final Probabilities Dictionary:\n", probabilities)
    rewards = {}

    print("\nNow define rewards")
    for s in states:
        temp = {}
        for index, action in enumerate(actions):
            while True:
                reward_str = input(
                    f"If in state = {s} and you take action = {action}, what is the reward? "
                ).strip()
                try:
                    reward_val = float(reward_str)
                except ValueError:
                    print("Invalid input. Please enter a valid float.")
                    continue  # prompt again
                
                # If we get here, parsing succeeded
                temp2 = {}
                # set these for all values further down the tree: 
                for i in range(len(states)):
                    temp2[states[i]] = reward_val

                # Store it in the dictionary for this (state, action)
                temp[index] = temp2
                break  # break the while loop, move to the next action

        # Finally, store the dictionary for this state
        rewards[s] = temp

    print("Final Rewards Dictionary:")
    print(rewards)
    # Get max iterations (positive integer)
    max_iterations_validity = False
    print("\nInput solver parameters")

    while not max_iterations_validity:
        max_iterations = input("Enter the maximum number of iterations (positive integer): ").strip()
        try:
            max_iterations = int(max_iterations)
            if max_iterations > 0:
                max_iterations_validity = True
            else:
                print("Must be a positive integer.")
        except ValueError:
            print("Invalid input. Enter a positive integer.")

    # Get tolerance (small positive float)
    tolerance_validity = False
    while not tolerance_validity:
        tolerance = input("Enter the solver tolerance (e.g., 1e-6): ").strip()
        try:
            tolerance = float(tolerance)
            if tolerance > 0:
                tolerance_validity = True
            else:
                print("Tolerance must be a positive number.")
        except ValueError:
            print("Invalid input. Enter a small positive float (e.g., 0.00001 or 1e-5).")

    # Get discount rate
    discount_rate_validity = False
    while not discount_rate_validity:
        discount_rate = input("Enter the discount rate (0 ≤ γ < 1): ").strip()
        try:
            discount_rate = float(discount_rate)
            if 0 <= discount_rate < 1:
                discount_rate_validity = True
            else:
                print("Discount rate must be in the range [0, 1).")
        except ValueError:
            print("Invalid input. Enter a float between 0 and 1 (e.g., 0.9).")
    print('\nMDP Successfully initialised, solving in progess')

    solver = GenericMDP(states = states, 
                        actions = actions, 
                        probabilities = probabilities, 
                        rewards = rewards, 
                        discount_rate = discount_rate, 
                        max_iterations = max_iterations, 
                        tolerance = tolerance)()


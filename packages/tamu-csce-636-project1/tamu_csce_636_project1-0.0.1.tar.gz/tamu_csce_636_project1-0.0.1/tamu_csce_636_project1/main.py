import numpy as np
import math
from math import e 
from collections import defaultdict

real_print = print

n_k_m_pairs = [
    (9, 4, 2), 
    (9, 4, 3), 
    (9, 4, 4), 
    (9, 4, 5), 
    (9, 5, 2), 
    (9, 5, 3), 
    (9, 5, 4), 
    (9, 6, 2), 
    (9, 6, 3), 
    (10, 4, 2), 
    (10, 4, 3), 
    (10, 4, 4), 
    (10, 4, 5),
    (10, 4, 6),
    (10, 5, 2),
    (10, 5, 3),
    (10, 5, 4),
    (10, 5, 5),
    (10, 6, 2),
    (10, 6, 3),
    (10, 6, 4),
]
p = [
    [ 0.4759809,  0.9938236, 0.819425 ],
    [-0.8960798, -0.7442706, 0.3345122],
]

def calculate_score(person_index, list_of_loss_per_parameter_set):
    """
    NOTE: this function is not guarenteed to be correct. It is just an inital pass at implementing the algorithm from the instructions pdf
    Example:
        n = 9;k = 4;m = 2
        parameter_set1 = (n, k, m)
        parameter_set2 = (n, k, m+1)
        parameter_set3 = (n, k, m+2)
        
        person_1 = {
            parameter_set1: 0.3,
            parameter_set2: 0.8,
            parameter_set3: 0.5,
        }
        person_2 = {
            parameter_set1: 0.9,
            parameter_set2: 0.6,
            parameter_set3: 0.7,
        }
        
        list_of_loss_per_parameter_set = [
            person_1,
            person_2,
        ]
        
        calculate_score(0, list_of_loss_per_parameter_set)
    """
    alpha, theta = calculate_score_part1_alphas_and_thetas(list_of_loss_per_parameter_set)
    loss_per_parameter_set = list_of_loss_per_parameter_set[person_index]
    score_per_parameter_set = calculate_score_part2_beta_scores(loss_per_parameter_set, alpha, theta)
    score = calculate_score_part3(score_per_parameter_set)
    return score

# helper 
def calculate_score_part1_alphas_and_thetas(list_of_loss_per_parameter_set):
    """
    Example:
        n = 9;k = 4;m = 2
        parameter_set1 = (n, k, m)
        parameter_set2 = (n, k, m+1)
        parameter_set3 = (n, k, m+2)
        
        
        person_1 = {
            parameter_set1: 0.3,
            parameter_set2: 0.8,
            parameter_set3: 0.5,
        }
        person_2 = {
            parameter_set1: 0.9,
            parameter_set2: 0.6,
            parameter_set3: 0.7,
        }
        
        list_of_loss_per_parameter_set = [
            person_1,
            person_2,
        ]
        alpha_per_parameter_set, theta_per_parameter_set = calculate_score_part1_alphas_and_thetas(list_of_loss_per_parameter_set)
        print(alpha_per_parameter_set)
        print(theta_per_parameter_set)
    
    Parameters:
        scores (list of dictionaries, with keys that are (n, k, m) and values of score (float))
    """
    # 
    # validate input
    # 
    if 1:
        all_keys = []
        for each_submission in list_of_loss_per_parameter_set:
            all_keys.append(
                sorted(list(each_submission.keys()))
            )
        if len(all_keys) == 0:
            raise ValueError("No parameter sets found.")
        
        # make sure all submissions have same parameter sets (or at least same quantity)
        num_of_parameter_sets = len(all_keys[0])
        for index, each in enumerate(all_keys):
            if len(each) != num_of_parameter_sets:
                raise ValueError(f"Number of parameter sets differs. i=1, has keys: {all_keys[0]}, i={index}, has keys: {each}")
            
    # 
    # organize data
    # 
    if 1:
        losses_per_parameter_set = defaultdict(lambda *args: [])
        for each_submission in list_of_loss_per_parameter_set:
            for each_parameter_set, score in each_submission.items():
                losses_per_parameter_set[each_parameter_set].append(score)
    
    #
    # get alpha
    #
    alpha_per_parameter_set = defaultdict(lambda *args: 0)
    theta_per_parameter_set = defaultdict(lambda *args: 0)
    for parameter_set, scores in losses_per_parameter_set.items():
        sorted_scores = sorted(scores)
        scores_array = np.array(sorted_scores)
        median_score = np.percentile(scores_array, 50)
        median_index = (len(scores) + 1) // 2  # This is equivalent to ceil(M/2)
        quarter_score = np.percentile(scores_array, 25)
        alpha_per_parameter_set[parameter_set] = math.log(3) / (median_score - quarter_score)
        theta_per_parameter_set[parameter_set] = sorted_scores[median_index - 1]
    
    return alpha_per_parameter_set, theta_per_parameter_set

# helper
def calculate_score_part2_beta_scores(loss_per_parameter_set, alpha, theta):
    alpha, theta = calculate_score_part1_alphas_and_thetas(list_of_loss_per_parameter_set)
    score_per_parameter_set = defaultdict(lambda *args: 0)
    for n,k,m in alpha.keys():
        # this part is just an S curve between 0 and 100
        part1 = 100 * (e**( alpha[n,k,m] * (loss_per_parameter_set[n,k,m] - theta[n,k,m]) + 1)** -1)
        part2 = 100 * (e**(-alpha[n,k,m] * theta[n,k,m]                                   + 1)** -1)
        score_per_parameter_set[n,k,m] = part1 + 100 - part2
    
    # these are beta_scores
    return score_per_parameter_set

# helper
def calculate_score_part3(beta_scores):
    """
    Parameters:
        beta_scores (dict): A dictionary where keys are tuples representing (n, k, m)
        and values are the corresponding β_{n,k,m} scores.

    Returns:
        float: The average score SCORE_model for the model, ranging from 0 to 100.
    """
    num_configurations = len(beta_scores)
    total_score = sum(beta_scores.values())
    score = total_score / num_configurations if num_configurations > 0 else 0
    score = min(100, max(0, score))
    return score

class Evaluator:
    def __init__(
        self,
        print=True,
        input_output_pairs=[
            # n, k, m, p
            ((5, 2, 0, p), 1),
            ((5, 2, 2, p), 1.9242387),
        ]
    ):
        self.should_print = print
        self.input_output_pairs = input_output_pairs
    
    def cost_function(self, real_value, guess):
        return (math.log2(real_value) - math.log2(guess)) ** 2

    def eval(self, func):
        """
        Parameters:
            print (bool): Whether to print the output
            func (function): A function that takes in k (int), n (int), m (int), and p (numpy matrix) and returns the m-height value
        Returns:
            dict: A dictionary of scores per parameter set
        """
        losses_per_parameter_set = defaultdict(lambda *args: [])
        for index, ((n, k, m, p), correct_m_height) in enumerate(self.input_output_pairs):
            given_m_height = 1
            try:
                given_m_height = func(n, k, m, p)
            except Exception as error:
                if self.should_print:
                    print(f"Error at index={index}\nargs: k={k}, n={n}, m={m}, p={p}\nerror={error}")
            
            iter_loss = self.cost_function(correct_m_height, given_m_height)
            losses_per_parameter_set[n, k, m].append(iter_loss)
        
        # get average scores
        loss_per_parameter_set = defaultdict(lambda *args: 0)
        for each_parameter_set, each_set_of_scores in losses_per_parameter_set.items():
            loss_per_parameter_set[each_parameter_set] = sum(each_set_of_scores) / len(each_set_of_scores)
        
        if self.should_print:
            print(f"loss_per_parameter_set = {{")
            print(f'''    # n, k, m''')
            for each_key, each_value in loss_per_parameter_set.items():
                print(f'''    {each_key}: {each_value},''')
            print("}")
        
        return loss_per_parameter_set
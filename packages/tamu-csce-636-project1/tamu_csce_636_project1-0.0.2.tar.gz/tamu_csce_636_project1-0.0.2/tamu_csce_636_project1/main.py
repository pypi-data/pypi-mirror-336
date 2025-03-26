import numpy as np
import math
from math import e 
from collections import defaultdict

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

def is_iterable(thing):
    # https://stackoverflow.com/questions/1952464/in-python-how-do-i-determine-if-an-object-is-iterable
    try:
        iter(thing)
    except TypeError:
        return False
    else:
        return True
        
def to_pure(an_object, recursion_help=None):
    # 
    # infinte recursion prevention
    # 
    top_level = False
    if recursion_help is None:
        top_level = True
        recursion_help = {}
    class PlaceHolder:
        def __init__(self, id):
            self.id = id
        def eval(self):
            return recursion_help[key]
    object_id = id(an_object)
    # if we've see this object before
    if object_id in recursion_help:
        # if this value is a placeholder, then it means we found a child that is equal to a parent (or equal to other ancestor/grandparent)
        if isinstance(recursion_help[object_id], PlaceHolder):
            return recursion_help[object_id]
        else:
            # if its not a placeholder, then we already have cached the output
            return recursion_help[object_id]
    # if we havent seen the object before, give it a placeholder while it is being computed
    else:
        recursion_help[object_id] = PlaceHolder(object_id)
    
    parents_of_placeholders = set()
    
    # 
    # optional torch tensor converter
    # 
    if hasattr(an_object, "__class__") and hasattr(an_object.__class__, "__name__"):
        if an_object.__class__.__name__ == "Tensor":
            try:
                import torch
                if isinstance(an_object, torch.Tensor):
                    an_object = an_object.detach().cpu()
            except Exception as error:
                pass
    # 
    # main compute
    # 
    return_value = None
    # base case 1 (iterable but treated like a primitive)
    if isinstance(an_object, str):
        return_value = an_object
    # base case 2 (exists because of scalar numpy/pytorch/tensorflow objects)
    elif hasattr(an_object, "tolist"):
        return_value = an_object.tolist()
    else:
        # base case 3
        if not is_iterable(an_object):
            return_value = an_object
        else:
            if isinstance(an_object, dict):
                return_value = {
                    to_pure(each_key, recursion_help) : to_pure(each_value, recursion_help)
                        for each_key, each_value in an_object.items()
                }
            else:
                return_value = [ to_pure(each, recursion_help) for each in an_object ]
    
    # convert iterables to tuples so they are hashable
    if is_iterable(return_value) and not isinstance(return_value, dict) and not isinstance(return_value, str):
        return_value = tuple(return_value)
    
    # update the cache/log with the real value
    recursion_help[object_id] = return_value
    #
    # handle placeholders
    #
    if is_iterable(return_value):
        # check if this value has any placeholder children
        children = return_value if not isinstance(return_value, dict) else [ *return_value.keys(), *return_value.values() ]
        for each in children:
            if isinstance(each, PlaceHolder):
                parents_of_placeholders.add(return_value)
                break
        # convert all the placeholders into their final values
        if top_level == True:
            for each_parent in parents_of_placeholders:
                iterator = enumerate(each_parent) if not isinstance(each_parent, dict) else each_parent.items()
                for each_key, each_value in iterator:
                    if isinstance(each_parent[each_key], PlaceHolder):
                        each_parent[each_key] = each_parent[each_key].eval()
                    # if the key is a placeholder
                    if isinstance(each_key, PlaceHolder):
                        value = each_parent[each_key]
                        del each_parent[each_key]
                        each_parent[each_key.eval()] = value
    
    # finally return the value
    return return_value

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
        for (index, ((n, k, m, p), correct_val)) in enumerate(self.input_output_pairs):
            # make sure the matrix is pure, so that student's code isn't surprised when tested on pure data structures
            self.input_output_pairs[index] = ((n, k, m, to_pure(p)), correct_val)
    
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
        had_errors = False
        for index, ((n, k, m, p), correct_m_height) in enumerate(self.input_output_pairs):
            given_m_height = 1
            try:
                given_m_height = func(n, k, m, p)
                if type(given_m_height) != float and type(given_m_height) != int:
                    raise ValueError(f"the return value of the function given to .eval() is not a float. given_m_height={given_m_height}")
            except Exception as error:
                had_errors = True
                if self.should_print:
                    print(f"Error at index={index}\n    args: k={k}, n={n}, m={m}, p={p}\n    error={error}")
                else:
                    raise error
            
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
        
            if had_errors:
                raise ValueError("There were errors in the evaluation. See the output for more details.")
        
        return loss_per_parameter_set
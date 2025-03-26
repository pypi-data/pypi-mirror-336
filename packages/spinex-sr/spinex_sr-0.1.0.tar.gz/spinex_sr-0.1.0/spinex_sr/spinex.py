import logging
from termcolor import colored

class Logger:
    def __init__(self, log_file='Feynman_medium_units.log', verbose=True, log_config=None, enable_file_logging=False):
        self.verbose = verbose
        self.enable_file_logging = enable_file_logging
        self.log_file = log_file
        # Default configuration if none provided
        default_config = {
            'DEBUG': {'enabled': True, 'interval': 1},
            'INFO': {'enabled': True, 'interval': 1},
            'WARNING': {'enabled': True, 'interval': 1},
            'ERROR': {'enabled': True, 'interval': 1},
            'SUCCESS': {'enabled': True, 'interval': 1}
        }
        self.log_config = log_config if log_config else default_config
        self.counters = {
            level: 0 for level, config in self.log_config.items() if config.get('enabled', False)
        }
        self.logger = logging.getLogger('SPINEX_SymbolicRegression')
        self.logger.setLevel(logging.DEBUG)
        if not self.logger.handlers:
            if self.enable_file_logging:
                self._add_file_handler()
        self.logger.propagate = False
        if not hasattr(logging, 'SUCCESS'):
            logging.SUCCESS = logging.INFO + 5
            logging.addLevelName(logging.SUCCESS, 'SUCCESS')

    def _add_file_handler(self):
        fh = logging.FileHandler(self.log_file)
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def _should_print(self, level):
        config = self.log_config.get(level, {})
        if not config.get('enabled', False):
            return False
        self.counters[level] += 1
        interval = config.get('interval', 1)
        return self.counters[level] % interval == 0

    def info(self, message):
        if self.enable_file_logging:
            self.logger.info(message)
        if self.verbose and self._should_print('INFO'):
            print(colored(f"[INFO] {message}", "cyan"))

    def warning(self, message):
        if self.enable_file_logging:
            self.logger.warning(message)
        if self.verbose and self._should_print('WARNING'):
            print(colored(f"[WARNING] {message}", "yellow"))

    def error(self, message):
        if self.enable_file_logging:
            self.logger.error(message)
        if self.verbose and self._should_print('ERROR'):
            print(colored(f"[ERROR] {message}", "red", attrs=["bold"]))

    def success(self, message):
        if self.enable_file_logging:
            self.logger.log(logging.SUCCESS, message)
        if self.verbose and self._should_print('SUCCESS'):
            print(colored(f"[SUCCESS] {message}", "green", attrs=["bold"]))

    def debug(self, message):
        if self.enable_file_logging:
            self.logger.debug(message)
        if self.verbose and self._should_print('DEBUG'):
            print(colored(f"[DEBUG] {message}", "magenta"))

    def set_file_logging(self, enable):
        self.enable_file_logging = enable
        if enable and not self.logger.handlers:
            self._add_file_handler()
        elif not enable and self.logger.handlers:
            self.logger.handlers = []

    def set_log_file(self, new_log_file):
        self.log_file = new_log_file
        if self.enable_file_logging:
            self.logger.handlers = []
            self._add_file_handler()


import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from joblib import Parallel, delayed, parallel_backend
from sympy.printing.numpy import NumPyPrinter
from sympy.utilities.lambdify import lambdify
import sympy as sp
import warnings
from scipy.stats import pearsonr, spearmanr
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import cosine, euclidean
import random
import threading
import time
import logging
import concurrent.futures
from functools import lru_cache
from sklearn.feature_selection import mutual_info_regression
import threading

class TimeoutMixin:
    def check_timeout(self):
        if hasattr(self, 'start_time') and hasattr(self, 'max_time'):
            if self.max_time is not None:
                elapsed = time.time() - self.start_time
                if elapsed > self.max_time:
                    raise TimeoutException(f"Maximum time of {self.max_time} seconds exceeded")

class TimeoutException(Exception):
    pass

def timeout_handler(timeout_duration, function, *args, **kwargs):
    result = [TimeoutException("Expression evaluation timed out")]
    def target():
        try:
            result[0] = function(*args, **kwargs)
        except Exception as e:
            result[0] = e
    thread = threading.Thread(target=target)
    thread.start()
    thread.join(timeout_duration)
    if thread.is_alive():
        thread.join()
        raise TimeoutException("Expression evaluation timed out")
    if isinstance(result[0], Exception):
        raise result[0]
    return result[0]

def set_seed(seed_value=42):
    np.random.seed(seed_value)
    random.seed(seed_value)

# Set seed at the start
set_seed(42)

# Ignore overflow warnings
warnings.filterwarnings('ignore', category=RuntimeWarning)

@lru_cache(maxsize=5000)  # Set maxsize to limit the cache
def cached_get_expression_depth_helper(expr):
    if isinstance(expr, (sp.Symbol, sp.Number)):
        return 1
    elif isinstance(expr, sp.Basic):
        if not expr.args:
            return 1
        return 1 + max(cached_get_expression_depth_helper(arg) for arg in expr.args)
    else:
        return 1

# Define the function to clear the cache
def clear_all_lru_caches():
    cached_get_expression_depth_helper.cache_clear()

class SPINEX_SymbolicRegression(TimeoutMixin):
    def __init__(self, data, target, actual_function, user_expression=None, max_depth=None, population_size=50,
                generations=50, similarity_threshold=0.7, dynamic_similarity_threshold=True, n_jobs=1,
                explainability_level='none', plot_results=True, early_stopping_metric=None, early_stopping_value=None,
                patience=0, force_all_variables=False, variable_inclusion_strategy='guided', logger=None,
                last_resort=False, elite_percentage=0.05, dynamic_elite=True, max_time=None, relevance_metric='both'):
        self.max_time = max_time
        self.start_time = time.time()
        self._expression_depth_cache = {}
        self._evaluate_expression_cache = {}
        self._subexpressions_cache = {}
        self._tree_edit_distance_cache = {}
        self.tree_edit_distance_cache_lock = threading.Lock()
        self.similarity_cache = {}
        self.similarity_cache_lock = threading.Lock()
        self.lambdified_cache = {}
        self.data = data
        self.target = target
        self.actual_function = actual_function
        self.force_all_variables = force_all_variables
        self.variable_inclusion_strategy = variable_inclusion_strategy
        self.variables = {str(var): sp.Symbol(var) for var in list(data.columns)}
        if logger is None:
            self.logger = Logger()
        else:
            self.logger = logger
        base_depth = 2
        if max_depth is None:
            self.max_depth = base_depth + (len(self.variables) if self.force_all_variables else 2)
            self.logger.debug(f"max_depth set to {self.max_depth} based on {'all variables' if self.force_all_variables else 'base depth + 2'}")
        else:
            min_depth = base_depth + (len(self.variables) if self.force_all_variables else 2)
            if max_depth < min_depth:
                self.logger.warning(f"Provided max_depth={max_depth} is too low. Setting to minimum required: {min_depth}.")
                self.max_depth = min_depth
            else:
                self.max_depth = max_depth
                self.logger.debug(f"max_depth provided: {self.max_depth}")
        self.initial_max_depth = self.max_depth
        self.logger.debug(f"initial_max_depth set to {self.initial_max_depth}")
        self.relevance_metric = relevance_metric
        self.relevance_scores = self.assess_variable_relevance(relevance_metric=self.relevance_metric)
        self.sorted_vars = sorted(
            self.variables.values(),
            key=lambda var: self.relevance_scores.get(var, 0),
            reverse=True
        )
        self.logger.debug(f"Variables sorted by relevance: {self.sorted_vars}")
        self.user_expression = user_expression
        if self.user_expression:
            try:
                self.user_expression_sym = sp.sympify(self.user_expression)
                if self.get_expression_depth(self.user_expression_sym) > self.max_depth:
                    self.logger.warning("User expression exceeds max_depth. It will be truncated or modified.")
                    self.user_expression_sym = self.truncate_expression(self.user_expression_sym)
                allowed_symbols = set(self.variables.values())
                if not self.user_expression_sym.free_symbols.issubset(allowed_symbols):
                    self.logger.warning("User expression contains variables not present in the data. They will be removed.")
                    self.user_expression_sym = self.user_expression_sym.subs(
                        {var: 0 for var in self.user_expression_sym.free_symbols if var not in allowed_symbols}
                    )
            except Exception as e:
                self.logger.error(f"Invalid user_expression provided: {e}")
                self.user_expression_sym = None
        else:
            self.user_expression_sym = None
        self.population_size = population_size
        self.generations = generations
        self.similarity_threshold = similarity_threshold
        self.initial_similarity_threshold = similarity_threshold
        self.dynamic_similarity_threshold = dynamic_similarity_threshold
        self.elite_percentage = elite_percentage
        self.dynamic_elite = dynamic_elite
        if not (0 < self.elite_percentage <= 1):
            raise ValueError("elite_percentage must be a float between 0 and 1")
        self.n_jobs = n_jobs
        self.explainability_level = explainability_level
        self.plot_results = plot_results

        self.early_stopping_metric = early_stopping_metric
        valid_metrics = ['fitness', 'r2', 'mse']
        if self.early_stopping_metric is not None:
            self.early_stopping_metric = self.early_stopping_metric.lower()
            if self.early_stopping_metric not in valid_metrics:
                raise ValueError(f"Invalid early_stopping_metric: {early_stopping_metric}. Choose from {valid_metrics}.")
            if early_stopping_value is None:
                raise ValueError("early_stopping_value must be provided when early_stopping_metric is set.")
        self.early_stopping_value = early_stopping_value

        self.patience = patience
        self.fitness_tolerance = 1e-6
        self.epsilon = 1e-10
        self.lambdified_cache = {}
        self.population = []
        self.best_expression = None
        self.baseline_mse = mean_squared_error(self.target, np.mean(self.target) * np.ones_like(self.target))
        self.expression_cache = {}
        self.max_cache_size = 1000  # Adjust based on available memory
        self.diversity_weight = 0.3  # Weight for balancing similarity and fitness
        self.mutation_types = ['replace', 'add', 'remove']
        valid_explain_levels = ['none', 'basic', 'advanced']
        if self.explainability_level.lower() not in valid_explain_levels:
            raise ValueError(f"Invalid explainability_level: {self.explainability_level}. "
                            f"Choose from {valid_explain_levels}.")
        self.unary_operators = [
            sp.sin, sp.cos,
            self.safe_exp, self.safe_log,
            self.safe_sqrt, self.safe_atan,
#            self.safe_acos, self.safe_asin,
#            self.safe_sinh, self.safe_cosh,
            self.safe_tanh
        ]
        self.binary_operators = [
            sp.Add,
            lambda x, y: x - y,
            sp.Mul,
            self.safe_div,
#            self.safe_max,
#            self.safe_min,
            self.safe_pow
        ]

        self.constant_choices = [sp.Integer(i) for i in range(-10, 11)] + \
                                [sp.pi, sp.E, sp.Rational(1, 2), sp.Rational(1, 3),
                                sp.Rational(1, 4), sp.Rational(1, 5), sp.sqrt(2), sp.sqrt(3)]
        self.variable_values = list(self.variables.values())
        self.variable_and_constant_choices = self.variable_values + self.constant_choices
        self.all_variables_set = set(self.variables.values())
        self.lambdify_modules = ['numpy', {
            'Max': np.maximum,
            'Min': np.minimum,
            'sin': np.sin,
            'cos': np.cos,
            'tan': np.tan,
            'asin': np.arcsin,
            'acos': np.arccos,
            'atan': np.arctan,
            'sinh': np.sinh,
            'cosh': np.cosh,
            'tanh': np.tanh,
            'exp': np.exp,
            'sqrt': np.sqrt,
            'Abs': np.abs,
            'ceiling': np.ceil,
            'floor': np.floor
        }]
        self.unit_array = np.array([1.0])
        self.num_variables = len(self.variables)
        self.sample_value_arrays = [self.unit_array] * self.num_variables
        self.last_resort = last_resort
        self.last_resort_activated = False
        self.logger.info("SPINEX_SymbolicRegression initialized with parameters:")
        self.logger.info(f"max_depth={max_depth}, population_size={population_size}, generations={generations}, "
                         f"similarity_threshold={similarity_threshold}, n_jobs={n_jobs}, "
                         f"explainability_level={explainability_level}, plot_results={plot_results}, "
                         f"early_stopping_fitness={early_stopping_value}, patience={patience}, "
                         f"force_all_variables={force_all_variables}, variable_inclusion_strategy={variable_inclusion_strategy}")

    def time_exceeded(self):
        if self.max_time is not None:
            elapsed_time = time.time() - self.start_time
            return elapsed_time > self.max_time
        else:
            return False

    def get_expression_depth_cached(self, expr):
        if expr in self._expression_depth_cache:
            return self._expression_depth_cache[expr]
        depth = cached_get_expression_depth_helper(expr)
        self._expression_depth_cache[expr] = depth
        return depth

    def get_expression_depth(self, expr):
        return self.get_expression_depth_cached(expr)

    def clip_sympy(self, x, lower, upper):
        return sp.Piecewise(
            (lower, x < lower),
            (upper, x > upper),
            (x, True)
        )

    def safe_log(self, x):
        is_sympy = isinstance(x, sp.Basic)
        if is_sympy:
            return sp.log(sp.Abs(x) + self.epsilon)
        else:
            x_array = np.asarray(x)
            return np.log(np.abs(x_array) + self.epsilon)

    def safe_sqrt(self, x):
        is_sympy = isinstance(x, sp.Basic)
        if is_sympy:
            return sp.sqrt(sp.Abs(x))
        else:
            x_array = np.asarray(x)
            return np.sqrt(np.abs(x_array))

    def safe_div(self, x, y):
        is_sympy = isinstance(x, sp.Basic) or isinstance(y, sp.Basic)
        small_value = 1e-12
        if is_sympy:
            return x / (y + small_value)
        else:
            y_array = np.asarray(y)
            y_array = np.where(np.abs(y_array) < small_value, small_value, y_array)
            return np.divide(x, y_array)

    def safe_max(self, x, y):
        is_sympy = isinstance(x, sp.Basic) or isinstance(y, sp.Basic)
        if is_sympy:
            return sp.Max(x, y)
        else:
            x_array = np.asarray(x)
            y_array = np.asarray(y)
            return np.maximum(x_array, y_array)

    def safe_min(self, x, y):
        is_sympy = isinstance(x, sp.Basic) or isinstance(y, sp.Basic)
        if is_sympy:
            return sp.Min(x, y)
        else:
            x_array = np.asarray(x)
            y_array = np.asarray(y)
            return np.minimum(x_array, y_array)

    def safe_pow(self, x, y):
        is_sympy = isinstance(x, sp.Basic) or isinstance(y, sp.Basic)
        if is_sympy:
            return sp.Pow(sp.Abs(x), y)
        else:
            x_array = np.abs(np.asarray(x))
            return np.power(x_array, y)

    def safe_asin(self, x):
        is_sympy = isinstance(x, sp.Basic)
        if is_sympy:
            return sp.asin(self.clip_sympy(x, -1, 1))
        else:
            x_array = np.asarray(x)
            return np.arcsin(np.clip(x_array, -1, 1))

    def safe_acos(self, x):
        is_sympy = isinstance(x, sp.Basic)
        if is_sympy:
            return sp.acos(self.clip_sympy(x, -1, 1))
        else:
            x_array = np.asarray(x)
            return np.arccos(np.clip(x_array, -1, 1))

    def safe_atan(self, x):
        is_sympy = isinstance(x, sp.Basic)
        if is_sympy:
            return sp.atan(x)
        else:
            x_array = np.asarray(x)
            return np.arctan(x_array)

    def safe_sinh(self, x):
        is_sympy = isinstance(x, sp.Basic)
        if is_sympy:
            return sp.sinh(self.clip_sympy(x, -100, 100))
        else:
            x_array = np.asarray(x)
            return np.sinh(np.clip(x_array, -100, 100))

    def safe_cosh(self, x):
        is_sympy = isinstance(x, sp.Basic)
        if is_sympy:
            return sp.cosh(self.clip_sympy(x, -100, 100))
        else:
            x_array = np.asarray(x)
            return np.cosh(np.clip(x_array, -100, 100))

    def safe_tanh(self, x):
        is_sympy = isinstance(x, sp.Basic)
        if is_sympy:
            return sp.tanh(x)
        else:
            x_array = np.asarray(x)
            return np.tanh(x_array)

    def safe_exp(self, x):
        is_sympy = isinstance(x, sp.Basic)
        if is_sympy:
            abs_x = sp.Abs(x)
            return sp.exp(abs_x / (abs_x + 1))
        else:
            x_array = np.abs(np.asarray(x))
            return np.exp(x_array / (x_array + 1))

    def assess_variable_relevance(self, relevance_metric='correlation'):
        relevance_scores = {}
        if relevance_metric not in ['correlation', 'mutual_information', 'both']:
            raise ValueError("relevance_metric must be 'correlation', 'mutual_information', or 'both'.")

        # Precompute mutual information if needed
        if relevance_metric in ['mutual_information', 'both']:
            try:
                mi_scores = mutual_info_regression(
                    self.data.values,
                    self.target,
                    discrete_features=False,
                    random_state=42  # For reproducibility
                )
                mi_dict = dict(zip(self.variables.keys(), mi_scores))
            except Exception as e:
                self.logger.error(f"Error computing mutual information: {e}")
                mi_dict = {var: 0 for var in self.variables}
        else:
            mi_dict = {var: 0 for var in self.variables}

        for var in self.variables:
            try:
                var_values = self.data[var].values
                if relevance_metric in ['correlation', 'both']:
                    # Compute Pearson correlation
                    pearson_corr, _ = pearsonr(var_values, self.target)
                    pearson_corr = abs(pearson_corr)
                else:
                    pearson_corr = 0

                if relevance_metric in ['mutual_information', 'both']:
                    mi = mi_dict[var]
                else:
                    mi = 0

                # Combine metrics into a relevance score
                if relevance_metric == 'both':
                    # You can adjust the weights as needed
                    relevance_score = 0.5 * pearson_corr + 0.5 * mi
                elif relevance_metric == 'correlation':
                    relevance_score = pearson_corr
                elif relevance_metric == 'mutual_information':
                    relevance_score = mi

                relevance_scores[self.variables[var]] = relevance_score

            except Exception as e:
                self.logger.error(f"Error assessing relevance for variable {var}: {e}")
                relevance_scores[self.variables[var]] = 0

        return relevance_scores

    def initialize_population(self):
        self.check_timeout()  # Add timeout check

        # EDIT: Replace exception raising with graceful handling
        if self.time_exceeded():
            self.logger.warning("Maximum time exceeded during population initialization. Returning with current population.")
            return  # EDIT: Previously raised TimeoutException

        self.logger.info("Initializing population...")
        self.population = []
        num_generated = self.population_size - int(self.user_expression_sym is not None)
        expr_types = np.random.choice(['simple', 'unary', 'binary', 'complex'], size=num_generated)
        for expr_type in expr_types:
            # EDIT: Replace exception raising with graceful handling
            if self.time_exceeded():
                self.logger.warning("Maximum time exceeded during population initialization loop. Stopping population initialization.")
                break  # EDIT: Previously raised TimeoutException

            if expr_type == 'simple':
                expr = self.generate_leaf()
            elif expr_type == 'unary':
                expr = np.random.choice(self.unary_operators)(self.generate_leaf())
            elif expr_type == 'binary':
                expr = np.random.choice(self.binary_operators)(self.generate_leaf(), self.generate_leaf())
            else:
                expr = self.generate_random_expression()

            # EDIT: Handle cases where expression generation fails
            if expr is None:
                self.logger.warning("Generated expression is None. Skipping this expression.")
                continue  # EDIT: Skip adding None expressions

            if self.force_all_variables:
                if self.variable_inclusion_strategy == 'guided':
                    missing_vars = set(self.variables.values()) - expr.free_symbols
                    for var in self.sorted_vars:
                        if var in missing_vars:
                            potential_expr = sp.Add(expr, var)
                            if self.get_expression_depth(potential_expr) <= self.max_depth:
                                expr = potential_expr
                                missing_vars.remove(var)
                elif self.variable_inclusion_strategy == 'probabilistic':
                    missing_vars = set(self.variables.values()) - expr.free_symbols
                    for var in missing_vars:
                        if np.random.random() < 0.5:
                            potential_expr = sp.Add(expr, var)
                            if self.get_expression_depth(potential_expr) <= self.max_depth:
                                expr = potential_expr
            self.population.append(expr)

        if self.user_expression_sym:
            self.population.append(self.user_expression_sym)
            self.logger.info(f"User-provided expression added to population: {self.user_expression_sym}")

        self.logger.success(f"Population initialized with {len(self.population)} expressions.")

        if self.force_all_variables:
            self.logger.info(f"Variable inclusion strategy: {self.variable_inclusion_strategy}")


    def generate_random_expression(self, depth=0, used_vars=None):
        self.check_timeout()  # Add timeout check

        # EDIT: Replace exception raising with graceful handling
        if self.time_exceeded():
            self.logger.warning("Maximum time exceeded during random expression generation. Returning fallback expression.")
            return sp.Integer(1)  # EDIT: Return a fallback expression instead of raising an exception

        if used_vars is None:
            used_vars = set()
        if depth == self.max_depth or (depth > 0 and np.random.random() < 0.3):
            if np.random.random() < 0.9:
                available_vars = list(set(self.variables.values()) - used_vars)
                if available_vars:
                    expr = np.random.choice(available_vars)
                else:
                    expr = np.random.choice(self.variable_values)
                used_vars.add(expr)
            else:
                expr = np.random.choice(self.constant_choices)
            if self.force_all_variables:
                missing_vars = self.all_variables_set - used_vars
                for extra_var in missing_vars:
                    potential_expr = sp.Add(expr, extra_var)
                    if self.get_expression_depth(potential_expr) <= self.max_depth:
                        expr = potential_expr
                        used_vars.add(extra_var)
                    else:
                        self.logger.debug(f"Cannot add variable {extra_var} to expression {expr} without exceeding max_depth.")
            return expr
        op_type = np.random.choice(['unary', 'binary'], p=[0.5, 0.5])
        max_attempts = 5
        for attempt in range(max_attempts):
            # EDIT: Replace exception raising with graceful handling
            if self.time_exceeded():
                self.logger.warning("Maximum time exceeded during random expression generation loop. Returning fallback expression.")
                return sp.Integer(1)  # EDIT: Return a fallback expression instead of raising an exception

            try:
                if op_type == 'unary':
                    op = np.random.choice(self.unary_operators)
                    new_subexpr = self.generate_random_expression(depth + 1, used_vars)
                    # EDIT: Handle None sub-expressions
                    if new_subexpr is None:
                        self.logger.debug("Generated sub-expression is None. Skipping this attempt.")
                        continue  # EDIT: Skip if sub-expression is None
                    # EDIT END
                    if depth + self.get_expression_depth(new_subexpr) > self.max_depth:
                        continue
                    expr = op(new_subexpr)
                else:
                    op = np.random.choice(self.binary_operators)
                    left_expr = self.generate_random_expression(depth + 1, used_vars)
                    right_expr = self.generate_random_expression(depth + 1, used_vars)
                    # EDIT: Handle None sub-expressions
                    if left_expr is None or right_expr is None:
                        self.logger.debug("One of the generated sub-expressions is None. Skipping this attempt.")
                        continue  # EDIT: Skip if any sub-expression is None
                    # EDIT END
                    combined_depth = max(self.get_expression_depth(left_expr), self.get_expression_depth(right_expr)) + 1
                    if combined_depth > self.max_depth:
                        continue
                    expr = op(left_expr, right_expr)
                    used_vars.update(expr.free_symbols)
                if self.is_valid_expression(expr):
                    used_vars.update(expr.free_symbols)
                    if self.user_expression_sym and np.random.random() < 0.1:
                        expr = self.insert_user_expression_subtree(expr)
                    return expr
            except Exception as e:
                # EDIT: Log the exception instead of propagating it
                self.logger.error(f"Exception during expression generation attempt {attempt + 1}: {e}")
                continue  # EDIT: Continue to next attempt without propagating the exception

        # EDIT: Replace exception raising with fallback expression
        fallback_expr = np.random.choice(self.variable_and_constant_choices)
        if self.force_all_variables:
            missing_vars = set(self.variables.values()) - {fallback_expr}
            for extra_var in missing_vars:
                potential_expr = sp.Add(fallback_expr, extra_var)
                if self.get_expression_depth(potential_expr) <= self.max_depth:
                    fallback_expr = potential_expr
                else:
                    self.logger.debug(f"Cannot add variable {extra_var} to fallback expression {fallback_expr} without exceeding max_depth.")
        return fallback_expr  # EDIT END



    def generate_leaf(self):
        return np.random.choice(list(self.variables.values()) +
                                [sp.Integer(i) for i in range(-10, 11)] +
                                [sp.pi, sp.E, sp.Rational(1, 2), sp.Rational(1, 3),
                                sp.Rational(1, 4), sp.Rational(1, 5), sp.sqrt(2), sp.sqrt(3)])

    def is_valid_expression(self, expr):
        self.check_timeout()  # Add timeout check

        try:
            if expr in self.expression_cache:
                return True
            func = self.get_lambdified_function(expr)
            if func is None:
                return False
            predictions = func(*self.sample_value_arrays)
            result = predictions[0]
            is_valid = (not np.iscomplex(result) and
                        not np.isnan(result) and
                        not np.isinf(result))
            return is_valid
        except Exception as e:
            return False

    def dynamic_complexity_penalty(self, complexity, generation, best_fitness):
        if self.last_resort_activated:
            final_penalty = 1.0
        else:
            progress = generation / self.generations
            base_penalty = 0.01 * (1 + np.tanh(2 * progress - 1))
            fitness_factor = np.clip(1.5 - (best_fitness * 1.5), 0.5, 1.5)
            complexity_scale = np.log1p(complexity) / np.log1p(self.max_depth)
            unique_exprs = len(set(str(expr) for expr in self.population))
            diversity = unique_exprs / len(self.population)
            diversity_factor = 1 + np.tanh(5 * (diversity - 0.5))
            final_penalty = np.exp(-base_penalty * fitness_factor * complexity_scale * diversity_factor)
            final_penalty = np.clip(final_penalty, 0.1, 1.0)
        return final_penalty

    def evaluate_expression(self, expression, timeout=5):
        self.check_timeout()  # Add timeout check

        try:
            if isinstance(expression, str):
                expression = sp.sympify(expression)
            if (expression.has(sp.zoo) or
                expression.has(sp.oo) or
                expression.has(sp.S.NegativeInfinity) or
                expression.has(sp.nan)):
                raise ValueError(f"Invalid expression contains infinity or NaN: {expression}")
            func = self.get_lambdified_function(expression)
            if func is None:
                raise ValueError(f"Could not lambdify expression: {expression}")

            def evaluation_function():
                return func(*[self.data[str(var)].values for var in self.variables])
            predictions = timeout_handler(timeout, evaluation_function)
            if np.isscalar(predictions):
                predictions = np.full_like(self.target, predictions)
            if np.isnan(predictions).any() or np.isinf(predictions).any():
                return 0, np.inf, np.inf, -1, -1, -1, -1, -1, -1
            mse = mean_squared_error(self.target, predictions)
            r2 = r2_score(self.target, predictions)
            correlation, _ = pearsonr(self.target, predictions)
            spearman, _ = spearmanr(self.target, predictions)
            scaler = StandardScaler()
            target_normalized = scaler.fit_transform(self.target.reshape(-1, 1)).flatten()
            predictions_normalized = scaler.transform(predictions.reshape(-1, 1)).flatten()
            cosine_sim = 1 - cosine(target_normalized, predictions_normalized)
            euclidean_dist = euclidean(target_normalized, predictions_normalized)
            max_euclidean = np.sqrt(len(self.target))
            euclidean_sim = 1 - (euclidean_dist / max_euclidean)
            complexity = expression.count_ops()
            relative_improvement = max(0, (self.baseline_mse - mse) / self.baseline_mse)
            accuracy_score = (0.2 * r2 +
                            0.2 * relative_improvement +
                            0.2 * cosine_sim +
                            0.2 * euclidean_sim +
                            0.1 * abs(correlation) +
                            0.1 * abs(spearman))
            complexity_penalty = self.dynamic_complexity_penalty(complexity, self.current_generation, self.best_fitness_overall)
            fitness = accuracy_score * complexity_penalty
            return fitness, mse, complexity, correlation, spearman, cosine_sim, euclidean_sim, r2, relative_improvement
        except TimeoutException:
            self.logger.error(f"Evaluation of expression {expression} timed out after {timeout} seconds")
            return 0, np.inf, np.inf, -1, -1, -1, -1, -1, -1
        except Exception as e:
            self.logger.error(f"Error evaluating expression: {expression} - {str(e)}")
            return 0, np.inf, np.inf, -1, -1, -1, -1, -1, -1

    def insert_user_expression_subtree(self, expr):

        if not self.user_expression_sym:
            return expr
        try:
            subexpr = self.get_random_subexpression(expr)
            new_expr = expr.subs(subexpr, self.user_expression_sym)
            if self.get_expression_depth(new_expr) <= self.max_depth:
                return new_expr
            else:
                self.logger.debug(f"Replacing with user expression exceeds max_depth. Skipping.")
                return expr
        except Exception as e:
            self.logger.debug(f"Error inserting user expression subtree: {e}")
            return expr

    def truncate_expression(self, expr):

        if self.get_expression_depth(expr) <= self.max_depth:
            return expr
        if isinstance(expr, sp.Basic):
            truncated_args = []
            for arg in expr.args:
                truncated_arg = self.truncate_expression(arg)
                truncated_args.append(truncated_arg)
                if self.get_expression_depth(sp.Function(expr.func, *truncated_args)) > self.max_depth:
                    break
            return expr.func(*truncated_args)
        return expr

    def cached_evaluate_expression(self, expression_str, timeout=5):
        if expression_str in self._evaluate_expression_cache:
            return self._evaluate_expression_cache[expression_str]
        expression = sp.sympify(expression_str)
        result = self.evaluate_expression(expression, timeout)
        self._evaluate_expression_cache[expression_str] = result
        return result

    def prune_population(self):
        self.check_timeout()  # Add timeout check

        self.population = [expr for expr in self.population if self.is_valid_expression(expr)]
        unique_exprs = {}
        for expr in self.population:
            expr_str = str(expr)
            if expr_str not in unique_exprs:
                unique_exprs[expr_str] = expr
        self.population = list(unique_exprs.values())
        if self.force_all_variables:
            self.population = [
                expr for expr in self.population
                if set(self.variables.values()).issubset(expr.free_symbols)
            ]
        if len(self.population) > self.population_size:
            with parallel_backend('threading', n_jobs=self.n_jobs):
                fitness_scores = Parallel()(delayed(self.cached_evaluate_expression)(str(expr), timeout=5) for expr in self.population)
            combined = list(zip(self.population, fitness_scores))
            sorted_population = sorted(combined, key=lambda x: x[1][0], reverse=True)
            self.population = [expr for expr, _ in sorted_population[:self.population_size]]
        if len(self.expression_cache) > self.max_cache_size:
            sorted_cache = sorted(self.expression_cache.items(), key=lambda x: x[1][0], reverse=True)
            self.expression_cache = dict(sorted_cache[:self.max_cache_size])

    def select_diverse_expression(self, population):
        if len(population) <= 1:
            return population[0][0]
        similarities = Parallel(n_jobs=self.n_jobs)(
            delayed(self.calculate_similarity)(expr1, expr2)
            for expr1, _ in population
            for expr2, _ in population
            if expr1 != expr2
        )
        avg_similarities = np.array(similarities).reshape(len(population), -1).mean(axis=1)
        diversity_scores = 1 - avg_similarities
        fitness_scores = np.array([score[0] for _, score in population])
        combined_scores = (1 - self.diversity_weight) * fitness_scores + self.diversity_weight * diversity_scores
        combined_scores /= combined_scores.sum()
        selected_index = np.random.choice(len(population), p=combined_scores)
        return population[selected_index][0]

    def select_similar_expression(self, target_expr, population):
        similarities = [
            (expr, self.calculate_similarity(target_expr, expr))
            for expr, _ in population if expr != target_expr
        ]
        similar_exprs = [expr for expr, sim in similarities if sim >= self.similarity_threshold]
        if similar_exprs:
            return np.random.choice(similar_exprs)
        else:
            return np.random.choice([expr for expr, _ in population if expr != target_expr])

    def mutate_expression(self, expression):
        self.check_timeout()  # Add timeout check

        if self.time_exceeded():
            raise TimeoutException("Maximum time exceeded during mutation.")
        if not isinstance(expression, sp.Basic):
            expr = sp.sympify(expression)
        else:
            expr = expression
        expr_depth = self.get_expression_depth(expr)
        mutation_type = np.random.choice(['replace', 'add', 'remove'])
        mutated_expr = None
        max_attempts = 5
        for attempt in range(max_attempts):
            if self.time_exceeded():
                raise TimeoutException("Maximum time exceeded during mutation.")
            try:
                if mutation_type == 'replace':
                    subexpr = self.get_random_subexpression(expr)
                    new_subexpr = self.generate_random_expression()
                    potential_depth = expr_depth - self.get_expression_depth(subexpr) + self.get_expression_depth(new_subexpr)
                    if potential_depth > self.max_depth:
                        continue
                    mutated_expr = expr.subs(subexpr, new_subexpr)
                elif mutation_type == 'add':
                    new_expr = self.generate_random_expression()
                    combined_depth = max(expr_depth, self.get_expression_depth(new_expr)) + 1
                    if combined_depth > self.max_depth:
                        continue
                    op = np.random.choice(self.binary_operators)
                    mutated_expr = op(expr, new_expr)
                elif mutation_type == 'remove':
                    if len(expr.args) > 1 or isinstance(expr.func, (sp.Add, sp.Mul)):
                        args = list(expr.args)
                        args.pop(np.random.randint(len(args)))
                        if isinstance(expr.func, sp.Pow) and len(args) < 2:
                            continue
                        temp_expr = expr.func(*args)
                        temp_expr_depth = self.get_expression_depth(temp_expr)
                        if temp_expr_depth > self.max_depth:
                            continue
                        mutated_expr = temp_expr
                    else:
                        continue
                else:
                    continue
                if mutated_expr != expr:
                    similarity = self.calculate_similarity(expr, mutated_expr)
                    if similarity < 0.9:
                        if self.force_all_variables:
                            missing_vars = set(self.variables.values()) - mutated_expr.free_symbols
                            if self.variable_inclusion_strategy == 'guided':
                                for var in self.sorted_vars:
                                    if var in missing_vars and np.random.random() < 0.5:
                                        potential_expr = sp.Add(mutated_expr, var)
                                        if self.get_expression_depth(potential_expr) <= self.max_depth:
                                            mutated_expr = potential_expr
                                            missing_vars.remove(var)
                            elif self.variable_inclusion_strategy == 'probabilistic':
                                for var in missing_vars:
                                    if np.random.random() < 0.5:
                                        potential_expr = sp.Add(mutated_expr, var)
                                        if self.get_expression_depth(potential_expr) <= self.max_depth:
                                            mutated_expr = potential_expr
                        return mutated_expr
            except Exception as e:
                continue
        return self.generate_random_expression()

    def crossover_expressions(self, expr1, expr2):
        self.check_timeout()  # Add timeout check

        if self.time_exceeded():
            raise TimeoutException("Maximum time exceeded during crossover.")
        tree1 = sp.sympify(expr1)
        tree2 = sp.sympify(expr2)
        max_attempts = 5
        new_expr = None

        for attempt in range(max_attempts):
            if self.time_exceeded():
                raise TimeoutException("Maximum time exceeded during crossover.")

            try:
                subtree1 = self.get_random_subexpression(tree1)
                subtree2 = self.get_random_subexpression(tree2)
                depth1 = self.get_expression_depth(subtree1)
                depth2 = self.get_expression_depth(subtree2)
                expr1_depth = self.get_expression_depth(tree1)
                expr2_depth = self.get_expression_depth(tree2)
                new_depth1 = expr1_depth - depth1 + depth2
                new_depth2 = expr2_depth - depth2 + depth1
                if new_depth1 > self.max_depth or new_depth2 > self.max_depth:
                    continue
                new_tree1 = tree1.subs(subtree1, subtree2)
                new_tree2 = tree2.subs(subtree2, subtree1)
                new_expr = np.random.choice([new_tree1, new_tree2])
                if new_expr != tree1 and new_expr != tree2 and self.calculate_similarity(tree1, new_expr) < 0.9:
                    if self.force_all_variables:
                        missing_vars = set(self.variables.values()) - new_expr.free_symbols
                        if self.variable_inclusion_strategy == 'guided':
                            for var in self.sorted_vars:
                                if var in missing_vars and np.random.random() < 0.5:
                                    potential_expr = sp.Add(new_expr, var)
                                    if self.get_expression_depth(potential_expr) <= self.max_depth:
                                        new_expr = potential_expr
                                        missing_vars.remove(var)
                        elif self.variable_inclusion_strategy == 'probabilistic':
                            for var in missing_vars:
                                if np.random.random() < 0.5:
                                    potential_expr = sp.Add(new_expr, var)
                                    if self.get_expression_depth(potential_expr) <= self.max_depth:
                                        new_expr = potential_expr
                    return new_expr
            except Exception as e:
                continue
        return self.generate_random_expression()

    def get_all_subexpressions_cached(self, expr_str):
        if expr_str in self._subexpressions_cache:
            return self._subexpressions_cache[expr_str]
        expr = sp.sympify(expr_str)
        subexprs = self.get_all_subexpressions_helper(expr)
        self._subexpressions_cache[expr_str] = subexprs
        return subexprs

    def get_all_subexpressions_helper(self, expr):
        if isinstance(expr, (sp.Symbol, sp.Number)):
            return [expr]
        subexprs = [expr]
        for arg in expr.args:
            subexprs.extend(self.get_all_subexpressions_helper(arg))
        return subexprs

    def get_random_subexpression(self, expr):
        expr_str = str(expr)
        subexprs = self.get_all_subexpressions_cached(expr_str)
        return np.random.choice(subexprs)

    def get_lambdified_function(self, expression):

        try:
            if expression in self.lambdified_cache:
                return self.lambdified_cache[expression]
            func = sp.lambdify(
                self.variable_values,
                expression,
                modules=self.lambdify_modules
            )
            self.lambdified_cache[expression] = func
            return func
        except Exception as e:
            self.logger.error(f"Error in get_lambdified_function: {e}")
            return None

    def update_similarity_threshold(self):
        unique_expressions = set(str(expr) for expr in self.population)
        diversity = len(unique_expressions) / len(self.population)
        self.diversity = diversity
        if not self.dynamic_similarity_threshold:
            return
        self.similarity_threshold = max(0.1, min(0.9, self.initial_similarity_threshold * (1 - diversity)))
        self.logger.info(f"Updated similarity_threshold to {self.similarity_threshold:.2f} based on diversity {diversity:.2f}")

    def update_elite_percentage(self):
        if not self.dynamic_elite:
            return
        diversity = self.diversity
        progress = self.current_generation / self.generations
        base_elite = 0.05
        max_elite = 0.2
        self.elite_percentage = min(max_elite, base_elite + (progress * (1 - diversity) * (max_elite - base_elite)))
        self.elite_percentage = max(base_elite, self.elite_percentage)
        self.logger.info(f"Updated elite_percentage to {self.elite_percentage:.4f} based on diversity {diversity:.4f} and progress {progress:.4f}")

    def evolve(self):
        self.check_timeout()  # Add timeout check

        self.start_time = time.time()
        self._expression_depth_cache.clear()
        self._evaluate_expression_cache.clear()
        self._subexpressions_cache.clear()
        self._tree_edit_distance_cache.clear()
        self.similarity_cache.clear()
        self.lambdified_cache.clear()
        set_seed(42)
        self.logger.info("Starting evolution process...")
        self.best_fitness_overall = float('-inf')
        self.best_r2_overall = float('-inf')
        self.best_mse_overall = float('inf')
        best_expression_overall = None
        stagnant_generations = 0
        reinitialization_attempts = 0
        max_reinitializations = int(0.9 * self.generations)
        self.current_generation = -1
        MAX_ALLOWED_DEPTH = 2 * self.initial_max_depth
        self.logger.info(f"Set MAX_ALLOWED_DEPTH to {MAX_ALLOWED_DEPTH} (twice the initial max_depth).")
        self.early_stopping_counter = 0  

        for generation in range(self.generations):
            elapsed_time = time.time() - self.start_time
            if self.max_time is not None and elapsed_time > self.max_time:
                self.logger.warning(f"Maximum time of {self.max_time} seconds exceeded at generation {generation}. Terminating evolution early.")
                if best_expression_overall is not None:
                    self.best_expression = best_expression_overall
                    self.logger.info(f"Returning best expression found so far: {self.best_expression}")
                else:
                    self.logger.warning(f"Evolution completed at generation {generation} without an expression. Returning a constant fallback expression. Please consider updating your search settings.")
                    self.best_expression = sp.Integer(1)
                self.logger.success(
                    f"Evolution terminated due to timeout at generation {generation}. "
                    f"Best Expression: {self.best_expression}, "
                    f"R²: {self.best_r2_overall:.3g}, "
                    f"MSE: {self.best_mse_overall:.3g}, "
                    f"Fitness: {self.best_fitness_overall:.3g}"
                )
                return self.best_expression

            self.current_generation = generation
            max_depth_exceeded = False
            if (self.last_resort and not self.last_resort_activated and
                generation >= int(0.9 * self.generations) and
                self.best_fitness_overall < 0.85):
                self.activate_last_resort_mode()
            self.logger.info(f"--- Generation {generation} ---")
            try:
                with parallel_backend('threading', n_jobs=self.n_jobs):
                    fitness_scores = Parallel()(
                        delayed(self.cached_evaluate_expression)(str(expr), timeout=5) for expr in self.population
                    )
            except Exception as e:
                self.logger.error(f"Error during parallel fitness evaluation at generation {generation}: {e}")
                continue  
            valid_population = [
                (expr, score) for expr, score in zip(self.population, fitness_scores) if score[0] > 1e-10
            ]
            if not valid_population:
                self.logger.warning(f"Generation {generation}: No valid expressions found. Reinitializing population.")
                reinitialization_attempts += 1
                if reinitialization_attempts > max_reinitializations:
                    self.logger.error(f"Max reinitializations reached. Terminating evolution after {reinitialization_attempts} attempts.")
                    break
                self.initialize_population()
                continue
            reinitialization_attempts = 0
            if self.force_all_variables:
                sorted_population = sorted(
                    valid_population,
                    key=lambda x: (set(self.variables.values()).issubset(x[0].free_symbols), x[1][0]),
                    reverse=True
                )
            else:
                sorted_population = sorted(valid_population, key=lambda x: x[1][0], reverse=True)
            current_best_expression = sorted_population[0][0]
            current_best_fitness = sorted_population[0][1][0]
            current_best_mse = sorted_population[0][1][1]
            current_best_r2 = sorted_population[0][1][7]
            if current_best_fitness > self.best_fitness_overall:
                self.best_fitness_overall = current_best_fitness
                best_expression_overall = current_best_expression
                self.best_r2_overall = current_best_r2
                self.best_mse_overall = current_best_mse
                stagnant_generations = 0
                self.logger.info(f"New best fitness: {self.best_fitness_overall:.3g} with expression: {best_expression_overall}")
            else:
                stagnant_generations += 1
                self.logger.info(f"No improvement in fitness. Stagnant generations: {stagnant_generations}")
            self.logger.info(f"Generation {generation}: Best Fitness = {self.best_fitness_overall:.3g}: Best Expression: {best_expression_overall}")



            if self.early_stopping_metric is not None and self.early_stopping_value is not None:
                metric_name = self.early_stopping_metric.lower()
                metric_value = None
                comparison = False

                if metric_name == 'fitness':
                    metric_value = current_best_fitness
                    target_value = self.early_stopping_value
                    comparison = metric_value >= target_value - self.fitness_tolerance
                elif metric_name == 'r2':
                    metric_value = current_best_r2
                    target_value = self.early_stopping_value
                    comparison = metric_value >= target_value
                elif metric_name == 'mse':
                    metric_value = current_best_mse
                    target_value = self.early_stopping_value
                    comparison = metric_value <= target_value
                else:
                    raise ValueError(f"Invalid early_stopping_metric: {self.early_stopping_metric}")

                if comparison:
                    self.early_stopping_counter += 1
                    if self.early_stopping_counter >= self.patience:
                        self.logger.info(
                            f"Early stopping at generation {generation} as {metric_name} "
                            f"has reached the target value of {target_value} for {self.patience} consecutive generations."
                        )
                        break
                else:
                    self.early_stopping_counter = 0
            else:
                # Early stopping not used; reset counter
                self.early_stopping_counter = 0


            if stagnant_generations > 5:
                self.logger.warning("Stagnation detected, resetting population.")
                self.initialize_population()
                stagnant_generations = 0
                continue
            if self.last_resort_activated:
                mutation_rate = self.mutation_rate
            else:
                mutation_rate = 0.2 if stagnant_generations < 5 else 0.7
            self.logger.info(f"Mutation rate set to {mutation_rate} for generation {generation}.")
            self.update_similarity_threshold()
            self.update_elite_percentage()
            elite_count = max(1, int(self.elite_percentage * self.population_size))
            self.logger.info(f"Elitism: Carrying forward top {elite_count} expressions "
                            f"({self.elite_percentage * 100:.1f}% of population).")
            new_population = [item[0] for item in sorted_population[:elite_count]]
            max_generation_attempts = 10
            generation_attempts = 0
            while len(new_population) < self.population_size:
                generation_attempts += 1
                self.logger.debug(f"Generation attempts: {generation_attempts}")
                if generation_attempts > max_generation_attempts:
                    self.logger.warning(f"Max generation attempts reached. Generating random expressions to complete population.")
                    remaining_slots = self.population_size - len(new_population)
                    max_final_attempts = remaining_slots * 2
                    final_attempts = 0
                    exceeded_depth_count = 0
                    while len(new_population) < self.population_size and final_attempts < max_final_attempts:
                        expr = self.generate_random_expression()
                        if expr is None:
                            self.logger.warning("Generated expression is None during final attempts. Skipping.")
                            final_attempts += 1
                            continue  
                        expr_depth = self.get_expression_depth(expr)
                        if expr_depth <= self.max_depth:
                            new_population.append(expr)
                            self.logger.debug(f"Added new expression within max_depth: {expr}")
                        else:
                            exceeded_depth_count += 1
                            self.logger.debug(f"Random expression {expr} exceeds max_depth ({expr_depth} > {self.max_depth}). Skipping.")
                        final_attempts += 1
                    exceed_threshold = 0.5
                    if final_attempts > 0 and (exceeded_depth_count / final_attempts) > exceed_threshold:
                        self.max_depth += 1
                        self.logger.warning(f"More than {exceed_threshold*100}% of expressions exceeded max_depth. Incrementing max_depth to {self.max_depth}.")
                        if self.max_depth > MAX_ALLOWED_DEPTH:
                            self.logger.error(f"Max depth exceeded the allowed limit of {MAX_ALLOWED_DEPTH}. Terminating evolution.")
                            max_depth_exceeded = True
                            break
                    if max_depth_exceeded:
                        break
                    if len(new_population) < self.population_size:
                        self.logger.warning(f"Only {len(new_population)} expressions were added after {final_attempts} attempts.")
                    break
                if np.random.random() < mutation_rate:
                    parent = np.random.choice([expr for expr, _ in sorted_population])
                    child = self.mutate_expression(parent)
                    if child is None:
                        self.logger.warning("Mutated child is None. Skipping.")
                        continue  
                    self.logger.debug(f"Mutated expression: {child}")
                else:
                    parent = np.random.choice([expr for expr, _ in sorted_population])
                    similar_expressions = self.find_similar_expressions(parent)
                    if similar_expressions and np.random.random() > 0.5:
                        partner = np.random.choice(similar_expressions)
                        child = self.crossover_expressions(parent, partner)
                        if child is None:
                            self.logger.warning("Crossover resulted in None expression. Skipping.")
                            continue  
                        self.logger.debug(f"Crossover between {parent} and {partner} resulted in {child}")
                    else:
                        child = self.generate_random_expression()
                        if child is None:
                            self.logger.warning("Generated child is None during crossover/generation. Skipping.")
                            continue  
                        self.logger.debug(f"Generated random expression: {child}")
                if self.force_all_variables:
                    missing_vars = set(self.variables.values()) - child.free_symbols
                    if self.variable_inclusion_strategy == 'guided':
                        for var in self.sorted_vars:
                            if var in missing_vars and np.random.random() < 0.5:
                                potential_expr = sp.Add(child, var)
                                if self.get_expression_depth(potential_expr) <= self.max_depth:
                                    child = potential_expr
                                    missing_vars.remove(var)
                    elif self.variable_inclusion_strategy == 'probabilistic':
                        for var in missing_vars:
                            if np.random.random() < 0.5:
                                potential_expr = sp.Add(child, var)
                                if self.get_expression_depth(potential_expr) <= self.max_depth:
                                    child = potential_expr
                if self.force_all_variables:
                    missing_vars = set(self.variables.values()) - child.free_symbols
                    for extra_var in missing_vars:
                        child = sp.Add(child, extra_var)
                if self.get_expression_depth(child) > self.max_depth:
                    self.logger.debug(f"Child expression {child} exceeds max_depth. Skipping.")
                    continue
                new_population.append(child)
            self.population = new_population
            self.logger.info(f"Population updated for generation {generation}.")
            if max_depth_exceeded:
                self.logger.error(f"Terminating evolution due to max_depth exceeding {MAX_ALLOWED_DEPTH}.")
                break
            self.prune_population()
            self.check_diversity()
        if best_expression_overall is None:
            self.logger.warning(f"Evolution completed at generation {self.current_generation} without an expression. "
                "Returning a constant fallback expression. Please consider updating your search settings.")
            best_expression_overall = sp.Integer(1)
        self.best_expression = best_expression_overall
        if self.force_all_variables:
            missing_vars = set(self.variables.values()) - self.best_expression.free_symbols
            if missing_vars:
                causes = self.determine_missing_variables_cause(missing_vars)
                self.logger.warning(
                    f"Best expression is missing variables: {missing_vars}. "
                    f"Possible cause(s): {causes}. "
                    "The algorithm will still return this expression, but you may want to adjust your settings."
                )
        elapsed_time = time.time() - self.start_time
        self.logger.success(
            f"Evolution completed at generation {self.current_generation}. "
            f"Time taken: {elapsed_time:.2f} seconds. "
            f"Best Expression: {self.best_expression}, "
            f"R²: {self.best_r2_overall:.3g}, "
            f"MSE: {self.best_mse_overall:.3g}, "
            f"Fitness: {self.best_fitness_overall:.3g}"
        )
        return self.best_expression

    def determine_missing_variables_cause(self, missing_vars):
        causes = []
        if self.get_expression_depth(self.best_expression) >= self.max_depth:
            causes.append(f"Expression reached max depth ({self.max_depth})")
        if self.variable_inclusion_strategy == 'probabilistic':
            causes.append("Probabilistic inclusion strategy may have excluded variables")
        if len(self.population) < self.population_size:
            causes.append("Population size decreased during evolution")
        if self.last_resort_activated:
            causes.append("Last resort mode was activated")
        if not causes:
            causes.append("Unknown - consider increasing generations or adjusting other parameters")
        return ", ".join(causes)

    def check_diversity(self):
        unique_expressions = set(str(expr) for expr in self.population)
        diversity = len(unique_expressions) / len(self.population)
        if diversity < 0.5:
            self.logger.warning("Low diversity detected, introducing new random expressions.")
            num_new = int(self.population_size * 0.2)
            new_expressions = Parallel(n_jobs=self.n_jobs)(
                delayed(self.generate_random_expression)() for _ in range(num_new)
            )
            self.population = self.population[:-num_new] + new_expressions

#    @lru_cache(maxsize=None)
    def calculate_similarity(self, expr1, expr2):

        key = tuple(sorted([expr1, expr2], key=lambda x: x.sort_key()))
        similarity = self.tree_edit_distance(expr1, expr2)
        similarity = max(0.0, min(1.0, similarity))
        return similarity

    def tree_edit_distance(self, tree1_str, tree2_str, depth=0):
        self.check_timeout()  # Add timeout check at the start

        key = (tree1_str, tree2_str)
        with self.tree_edit_distance_cache_lock:
            if key in self._tree_edit_distance_cache:
                return self._tree_edit_distance_cache[key]
        tree1 = sp.sympify(tree1_str)
        tree2 = sp.sympify(tree2_str)
        if depth > self.max_depth:
            similarity = 1
        else:
            def _size(tree):
                if isinstance(tree, (sp.Symbol, sp.Number)):
                    return 1
                return 1 + sum(_size(arg) for arg in tree.args)

            def _distance(t1, t2, depth):
                self.check_timeout()  # Add timeout check in each recursive call
                if t1 == t2:
                    return 0
                if isinstance(t1, (sp.Symbol, sp.Number)) and isinstance(t2, (sp.Symbol, sp.Number)):
                    return 1
                if isinstance(t1, (sp.Symbol, sp.Number)) or isinstance(t2, (sp.Symbol, sp.Number)):
                    return max(_size(t1), _size(t2))
                if t1.func != t2.func:
                    return 1 + max(_size(t1), _size(t2))
                return 1 + sum(_distance(a1, a2, depth + 1) for a1, a2 in zip(t1.args, t2.args))

            max_size = max(_size(tree1), _size(tree2))
            distance = _distance(tree1, tree2, depth)
            similarity = 1 - (distance / max_size)
            similarity = max(0.0, min(1.0, similarity))

        with self.tree_edit_distance_cache_lock:
            self._tree_edit_distance_cache[key] = similarity
        return similarity

    def find_similar_expressions(self, expression):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            similarities = list(executor.map(lambda expr: self.calculate_similarity(expression, expr), self.population))
        return [expr for expr, sim in zip(self.population, similarities) if sim >= self.similarity_threshold]

    def merge_expressions(self, expr1, expr2):
        tree1 = sp.sympify(expr1)
        tree2 = sp.sympify(expr2)
        operators = [sp.Add, sp.Mul]
        chosen_op = np.random.choice(operators)
        try:
            merged = chosen_op(tree1, tree2)
            merged_expr = sp.sympify(merged)
            if self.get_expression_depth(merged_expr) > self.max_depth:
                return self.generate_random_expression()
            if self.force_all_variables:
                missing_vars = set(self.variables.values()) - merged_expr.free_symbols
                for extra_var in missing_vars:
                    merged_expr = sp.Add(merged_expr, extra_var)
            return merged_expr
        except Exception as e:
            self.logger.debug(f"Error merging expressions {expr1} and {expr2}: {e}")
            return self.generate_random_expression()

    def activate_last_resort_mode(self):
        self.logger.warning("Activating Last Resort Mode: Increasing complexity and depth.")
        self.max_depth += 5
        self.mutation_rate = 0.85
        self.diversity_weight = 0.1
        self.last_resort_activated = True

    def find_similar_neighbors(self, expression, n_neighbors=5):
        similarities = []
        for expr in self.population:
            if expr != expression:
                similarity = self.calculate_similarity(expression, expr)
                similarities.append((expr, similarity))
        return sorted(similarities, key=lambda x: x[1], reverse=True)[:n_neighbors]

    def analyze_neighbors(self, expression, neighbors):
        analysis = []
        for neighbor, similarity in neighbors:
            neighbor_fitness, *_ = self.evaluate_expression(neighbor)
            analysis.append({
                'expression': str(neighbor),
                'similarity': similarity,
                'fitness': neighbor_fitness
            })
        return analysis

    def explain(self):
        if self.explainability_level == 'basic':
            self.basic_explanation()
        elif self.explainability_level == 'advanced':
            self.advanced_explanation()
        elif self.explainability_level.lower() == 'none':
            if self.plot_results:
                self.plot_expression()
        else:
            self.logger.warning(f"Unknown explainability level: {self.explainability_level}. No explanation will be provided.")

    def basic_explanation(self):
        print("\nBasic Explanation:")
        print(f"Best Expression: {self.best_expression}")
        fitness, mse, complexity, correlation, spearman, cosine_sim, euclidean_sim, r2, relative_improvement = self.evaluate_expression(self.best_expression)
        print(f"Fitness: {fitness}")
        print(f"Mean Squared Error: {mse}")
        print(f"R-squared: {r2}")
        print(f"Relative Improvement: {relative_improvement}")
        print(f"Expression Complexity: {complexity}")
        print(f"Correlation: {correlation}")
        print(f"Spearman Correlation: {spearman}")
        print(f"Cosine Similarity: {cosine_sim}")
        print(f"Euclidean Similarity: {euclidean_sim}")
        self.plot_expression()

    def advanced_explanation(self):
        self.basic_explanation()
        print("\nAdvanced Explanation:")
        expr = sp.sympify(self.best_expression)
        print("Expression Breakdown:")
        for term in expr.args:
            term_expr = str(term)
            if isinstance(term, sp.Number):
                print(f"Term: {term_expr}")
                print(f"  Contribution: Constant term")
            else:
                term_fitness, term_mse, term_complexity, term_corr, term_spearman, term_cosine, term_euclidean, term_r2, term_rel_imp = self.evaluate_expression(term_expr)
                print(f"Term: {term_expr}")
                print(f"  Fitness: {term_fitness:.4f}")
                print(f"  MSE Contribution: {term_mse:.4f}")
                print(f"  Complexity: {term_complexity}")
                print(f"  Correlation: {term_corr:.4f}")
                print(f"  Spearman Correlation: {term_spearman:.4f}")
                print(f"  Cosine Similarity: {term_cosine:.4f}")
                print(f"  Euclidean Similarity: {term_euclidean:.4f}")
                print(f"  R-squared: {term_r2:.4f}")
                print(f"  Relative Improvement: {term_rel_imp:.4f}")
        print("\nNeighbor Similarity Analysis:")
        similar_neighbors = self.find_similar_neighbors(self.best_expression)
        neighbor_analysis = self.analyze_neighbors(self.best_expression, similar_neighbors)
        for i, neighbor in enumerate(neighbor_analysis, 1):
            print(f"Neighbor {i}:")
            print(f"  Expression: {neighbor['expression']}")
            print(f"  Similarity: {neighbor['similarity']:.4f}")
            print(f"  Fitness: {neighbor['fitness']:.4f}")
        avg_neighbor_fitness = sum(n['fitness'] for n in neighbor_analysis) / len(neighbor_analysis) if neighbor_analysis else 0
        best_fitness = self.evaluate_expression(self.best_expression)[0]
        print("\nInsights:")
        print(f"Average Neighbor Fitness: {avg_neighbor_fitness:.4f}")
        print(f"Best Expression Fitness: {best_fitness:.4f}")
        if best_fitness > avg_neighbor_fitness:
            print("The best expression outperforms its neighbors, suggesting it's a local optimum.")
        else:
            print("The best expression has similar performance to its neighbors, suggesting potential for further optimization.")
        self.plot_expression()

    def plot_expression(self):
        if not self.plot_results:
            return None
        try:
            expr = sp.sympify(self.best_expression)
            func = sp.lambdify(list(self.variables.values()), expr, modules=["numpy", {
                'cosh': self.safe_cosh, 'sinh': self.safe_sinh, 'sqrt': self.safe_sqrt,
                'Max': self.safe_max, 'Min': self.safe_min, 'Abs': np.abs,
                'ceiling': np.ceil, 'floor': np.floor
            }])
            data_values = [self.data[var].values for var in self.variables]
            predictions = func(*data_values)
            predictions = np.asarray(predictions)

            if predictions.ndim == 0:
                predictions = np.full_like(self.target, predictions)
            elif predictions.ndim > 1:
                predictions = np.squeeze(predictions)
                print(f"Squeezed predictions shape: {predictions.shape}")

            if np.isnan(predictions).any() or np.isinf(predictions).any():
                print(f"Invalid predictions generated for expression: {self.best_expression}")
                return None

            # Check if all predictions are 1
            if np.all(predictions == 1):
                mse_str = "N/A"
                rmse_str = "N/A"
                r2_str = "N/A"
            else:
                mse = mean_squared_error(self.target, predictions)
                rmse = np.sqrt(mse)
                r2 = r2_score(self.target, predictions)
                mse_str = f"{mse:.2f}"
                rmse_str = f"{rmse:.2f}"
                r2_str = f"{r2:.2f}"

            fig, ax = plt.subplots(figsize=(10, 6))
            ax.scatter(self.target, predictions, alpha=0.5, label='Predicted vs Actual')
            ax.plot([self.target.min(), self.target.max()], [self.target.min(), self.target.max()], 'r--', label='Ideal Fit')

            actual_func = self.actual_function
            predicted_func = sp.pretty(expr)

            # Update legend with conditional metrics
            ax.legend(title=f"Actual: {actual_func}\n"
                            f"Predicted: {predicted_func}\n"
                            f"MSE: {mse_str}, RMSE: {rmse_str}, R²: {r2_str}")

            ax.set_xlabel("Actual Values")
            ax.set_ylabel("Predicted Values")
            ax.set_title("Actual vs Predicted Values for Expression")
            plt.show()
            return fig
        except Exception as e:
            print(f"Error plotting expression: {self.best_expression}. Error: {str(e)}")
            return None

    def clear_caches(self):
        self._expression_depth_cache.clear()
        self._evaluate_expression_cache.clear()
        self._subexpressions_cache.clear()
        self._tree_edit_distance_cache.clear()
        self.similarity_cache.clear()
        self.lambdified_cache.clear()

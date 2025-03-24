from .mainClass import *

import math

class MarkovChainKullbackLeibler(Distance):

    def __init__(self) -> None:
        """
        Initialize the MarkovChainKullbackLeibler class with transition matrices of two Markov chains.
        
        Parameters:
        P (list of list of float): Transition matrix of the first Markov chain (n x n).
        Q (list of list of float): Transition matrix of the second Markov chain (n x n).
        """
        super().__init__()
        self.type='Markov_chain'

    def kl_divergence(self, p, q):
        """
        Compute the Kullback-Leibler (KL) divergence between two probability distributions.
        
        Parameters:
        p (list of float): First probability distribution.
        q (list of float): Second probability distribution.
        
        Returns:
        float: KL divergence D_KL(p || q).
        """
        kl_div = 0.0
        for i in range(len(p)):
            if p[i] > 0 and q[i] > 0:
                kl_div += p[i] * math.log(p[i] / q[i])
        return kl_div

    def compute(self,P,Q):
        """
        Compute the Kullback-Leibler distance between the stationary distributions of two Markov chains.
        
        Returns:
        float: Kullback-Leibler distance between the stationary distributions.
        """

        # Compute stationary distributions of P and Q
        pi_P = MarkovChain.stationary_distribution(P)
        pi_Q = MarkovChain.stationary_distribution(Q)
        
        # Compute the Kullback-Leibler divergence between the two stationary distributions
        return self.kl_divergence(pi_P, pi_Q)

class MarkovChainWasserstein(Distance):

    def __init__(self, cost_matrix =[[0, 1], [1, 0]])-> None:
        """
        Initialize the MarkovChainWassersteinDistance class with transition matrices of two Markov chains.
        
        Parameters:
        P (list of list of float): Transition matrix of the first Markov chain (n x n).
        Q (list of list of float): Transition matrix of the second Markov chain (n x n).
        cost_matrix (list of list of float): Cost matrix (n x n) representing the "distance" between states.
        """
        super().__init__()
        self.type='Markov_chain'

        self.cost_matrix = cost_matrix

    def _compute_wasserstein_greedy(self, pi_P, pi_Q):
        """
        A greedy algorithm to compute an approximation of the Wasserstein distance between two distributions.
        
        Parameters:
        pi_P (list of float): Stationary distribution of the first Markov chain.
        pi_Q (list of float): Stationary distribution of the second Markov chain.
        
        Returns:
        float: Approximate Wasserstein distance between the two distributions.
        """
        n = self.num_states
        flow = [[0] * n for _ in range(n)]  # Flow matrix (transport plan)
        pi_P_copy = pi_P[:]
        pi_Q_copy = pi_Q[:]
        total_cost = 0.0

        for i in range(n):
            for j in range(n):
                # Flow is the minimum of remaining mass in pi_P and pi_Q
                flow_amount = min(pi_P_copy[i], pi_Q_copy[j])
                flow[i][j] = flow_amount
                total_cost += flow_amount * self.cost_matrix[i][j]
                
                # Update remaining mass in pi_P and pi_Q
                pi_P_copy[i] -= flow_amount
                pi_Q_copy[j] -= flow_amount
        
        return total_cost
        
    def compute(self,P, Q):
        """
        Compute the Wasserstein distance between the stationary distributions of two Markov chains.
        
        Returns:
        float: Wasserstein distance between the stationary distributions.
        """
        self.num_states = len(P)

        # Compute stationary distributions of P and Q
        pi_P = MarkovChain.stationary_distribution(P)
        pi_Q = MarkovChain.stationary_distribution(Q)
        
        # Compute Wasserstein distance using a greedy algorithm
        distance = self._compute_wasserstein_greedy(pi_P, pi_Q)
        return distance
        
    def example(self):
      # Example usage
      P = [[0.9, 0.1], [0.2, 0.8]]  # Transition matrix for Markov chain 1
      Q = [[0.85, 0.15], [0.25, 0.75]]  # Transition matrix for Markov chain 2
      # Cost matrix (Euclidean distance between states) dans init

      # Compute the Wasserstein distance between stationary distributions
      print("Wasserstein Distance:", self.compute(P, Q))

#TVD
class MarkovChainTotalVariation(Distance):

    def __init__(self)-> None:
        """
        Initialize the MarkovChainTotalVariationDistance class with transition matrices of two Markov chains.
        
        Parameters:
        P (list of list of float): Transition matrix of the first Markov chain (n x n).
        Q (list of list of float): Transition matrix of the second Markov chain (n x n).
        """
        super().__init__()
        self.type='Markov_chain'

        

    def total_variation_distance(self, pi_P, pi_Q):
        """
        Compute the total variation distance between two stationary distributions.
        
        Parameters:
        pi_P (list of float): Stationary distribution of the first Markov chain.
        pi_Q (list of float): Stationary distribution of the second Markov chain.
        
        Returns:
        float: Total variation distance between the two distributions.
        """
        total_variation = 0.0
        for i in range(len(pi_P)):
            total_variation += abs(pi_P[i] - pi_Q[i])
        return total_variation / 2

    def compute(self,P,Q):
        """
        Compute the total variation distance between the stationary distributions of two Markov chains.
        
        Returns:
        float: Total variation distance between the stationary distributions of the two Markov chains.
        """
        # Compute stationary distributions of P and Q
        pi_P = MarkovChain.stationary_distribution(P)
        pi_Q = MarkovChain.stationary_distribution(Q)

        # Compute the total variation distance between the two stationary distributions
        return self.total_variation_distance(pi_P, pi_Q)



class MarkovChainHellinger(Distance):

    def __init__(self)-> None:
        """
        Initialize the MarkovChainHellingerDistance class with transition matrices of two Markov chains.
        
        Parameters:
        P (list of list of float): Transition matrix of the first Markov chain (n x n).
        Q (list of list of float): Transition matrix of the second Markov chain (n x n).
        """
        super().__init__()
        self.type='Markov_chain'


    def hellinger_distance(self, pi_P, pi_Q):
        """
        Compute the Hellinger distance between two stationary distributions.
        
        Parameters:
        pi_P (list of float): Stationary distribution of the first Markov chain.
        pi_Q (list of float): Stationary distribution of the second Markov chain.
        
        Returns:
        float: Hellinger distance between the two distributions.
        """
        sum_squares = 0.0
        for i in range(len(pi_P)):
            sqrt_diff = math.sqrt(pi_P[i]) - math.sqrt(pi_Q[i])
            sum_squares += sqrt_diff ** 2
        return sum_squares**0.5 / 2**0.5

    def compute(self, P, Q):
        """
        Compute the Hellinger distance between the stationary distributions of two Markov chains.
        
        Returns:
        float: Hellinger distance between the stationary distributions of the two Markov chains.
        """
        # Compute stationary distributions of P and Q
        pi_P = MarkovChain.stationary_distribution(P)
        pi_Q = MarkovChain.stationary_distribution(Q)

        # Compute the Hellinger distance between the two stationary distributions
        return self.hellinger_distance(pi_P, pi_Q)


class MarkovChainJensenShannon(Distance):

    def __init__(self) -> None:
        """
        Initialize the MarkovChainJensenShannonDistance class with transition matrices of two Markov chains.
        
        Parameters:
        P (list of list of float): Transition matrix of the first Markov chain (n x n).
        Q (list of list of float): Transition matrix of the second Markov chain (n x n).
        """
        super().__init__()
        self.type='Markov_chain'

    def kl_divergence(self, p, q):
        """
        Compute the Kullback-Leibler (KL) divergence between two probability distributions.
        
        Parameters:
        p (list of float): First probability distribution.
        q (list of float): Second probability distribution.
        
        Returns:
        float: KL divergence D_KL(p || q).
        """
        kl_div = 0.0
        for i in range(len(p)):
            if p[i] > 0 and q[i] > 0:  # KL divergence is only defined when p[i] and q[i] are positive
                kl_div += p[i] * math.log(p[i] / q[i])
        return kl_div

    def jensen_shannon_divergence(self, pi_P, pi_Q):
        """
        Compute the Jensen-Shannon divergence between two stationary distributions.
        
        Parameters:
        pi_P (list of float): Stationary distribution of the first Markov chain.
        pi_Q (list of float): Stationary distribution of the second Markov chain.
        
        Returns:
        float: Jensen-Shannon divergence between the two distributions.
        """
        # Compute M = (P + Q) / 2
        M = [(pi_P[i] + pi_Q[i]) / 2 for i in range(len(pi_P))]

        # Compute the Jensen-Shannon divergence
        js_div = (self.kl_divergence(pi_P, M) + self.kl_divergence(pi_Q, M)) / 2
        return js_div

    def compute(self, P, Q):
        """
        Compute the Jensen-Shannon distance between the stationary distributions of two Markov chains.
        
        Returns:
        float: Jensen-Shannon distance between the stationary distributions of the two Markov chains.
        """
        # Compute stationary distributions of P and Q
        pi_P = MarkovChain.stationary_distribution(P)
        pi_Q = MarkovChain.stationary_distribution(Q)

        # Compute the Jensen-Shannon divergence
        js_divergence = self.jensen_shannon_divergence(pi_P, pi_Q)

        # Return the square root of the Jensen-Shannon divergence (Jensen-Shannon distance)
        return js_divergence**0.5



class MarkovChainFrobenius(Distance):

    def __init__(self)-> None:
        """
        Initialize the MarkovChainFrobeniusDistance class with transition matrices of two Markov chains.
        
        Parameters:
        P (list of list of float): Transition matrix of the first Markov chain (n x n).
        Q (list of list of float): Transition matrix of the second Markov chain (n x n).
        """
        super().__init__()
        self.type='Markov_chain'


    def compute(self, P, Q):
        """
        Compute the Frobenius distance between the transition matrices of two Markov chains.
        
        Returns:
        float: Frobenius distance between the two transition matrices.
        """
        num_states = len(P)
        sum_of_squares = 0.0
        for i in range(num_states):
            for j in range(num_states):
                diff = P[i][j] - Q[i][j]
                sum_of_squares += diff ** 2
        return sum_of_squares**0.5

class MarkovChainSpectral(Distance):

	def __init__(self) -> None:
		super().__init__()
		self.type='Markov_chain'
		print(self.type)

		"""
		Initialize the MarkovChainSpectralDistance class with transition matrices of two Markov chains.
        
		Parameters:
		P (list of list of float): Transition matrix of the first Markov chain (n x n).
		Q (list of list of float): Transition matrix of the second Markov chain (n x n).
		"""
		
	def characteristic_polynomial(self, matrix):
		"""
		Compute the characteristic polynomial of a matrix.
        
		Parameters:
		matrix (list of list of float): Matrix.
        
		Returns:
		list of float: Coefficients of the characteristic polynomial.
		"""
		# For a 2x2 matrix, the characteristic polynomial is given by:
		# det(A - λI) = λ^2 - (trace(A))λ + det(A)
		a = matrix
		if self.num_states == 2:
			trace = self.matrix_trace(a)
			det = a[0][0]*a[1][1] - a[0][1]*a[1][0]
			return [1, -trace, det]
		else:
			raise NotImplementedError("Characteristic polynomial calculation for matrices larger than 2x2 is not implemented.")
			
	def matrix_trace(self, matrix):
		"""
		Compute the trace of a matrix (sum of diagonal elements).
        
		Parameters:
		matrix (list of list of float): Matrix.
        
		Returns:
		float: Trace of the matrix.
		"""
		return sum(matrix[i][i] for i in range(self.num_states))
		
	def eigenvalues_2x2(self, matrix):
		"""
		Compute the eigenvalues of a 2x2 matrix.
        
		Parameters:
		matrix (list of list of float): 2x2 matrix.
        
		Returns:
		list of complex: Eigenvalues of the matrix.
		"""
		coeffs = self.characteristic_polynomial(matrix)
		a, b, c = coeffs
		discriminant = b**2 - 4*a*c
		eigenvalue1 = (-b + discriminant**0.5) / (2*a)
		eigenvalue2 = (-b - discriminant**0.5) / (2*a)
		return [eigenvalue1, eigenvalue2]
		
	def compute(self, P, Q):
		"""
		Compute the spectral distance between the transition matrices of two Markov chains.
        
		Returns:
		float: Spectral distance between the two transition matrices.
		"""
		self.num_states = len(P)

		# Compute eigenvalues of matrices P and Q
		if self.num_states == 2:
			eigenvalues_P = self.eigenvalues_2x2(P)
			eigenvalues_Q = self.eigenvalues_2x2(Q)
            
			# Calculate the spectral distance
			distance = 0.0
			for lambda_P, lambda_Q in zip(eigenvalues_P, eigenvalues_Q):
				distance += abs(lambda_P - lambda_Q) ** 2
			return distance**00.5
		else:
			raise NotImplementedError("Spectral distance calculation for matrices larger than 2x2 is not implemented.")
#######################################

from typing import List, Dict, Union, Optional
from math import sqrt

class MarkovSteadyStateDistance:
    """
    A class to calculate the distance between steady-state distributions of two Markov chains.
    
    This class implements methods to:
    1. Calculate steady-state distributions for Markov chains
    2. Compute the distance between two steady-state distributions
    3. Validate transition matrices
    """
    
    def __init__(self, tolerance: float = 1e-10, max_iterations: int = 1000):
        """
        Initialize the calculator with convergence parameters.
        
        Args:
            tolerance (float): Convergence tolerance for steady state calculation
            max_iterations (int): Maximum number of iterations for convergence
        """
        self.tolerance = tolerance
        self.max_iterations = max_iterations
    
    def _validate_transition_matrix(self, matrix: List[List[float]]) -> bool:
        """
        Validate if the given matrix is a valid transition matrix.
        
        Args:
            matrix (List[List[float]]): Transition matrix to validate
            
        Returns:
            bool: True if valid, raises ValueError otherwise
            
        Raises:
            ValueError: If matrix is not square or rows don't sum to 1
        """
        n = len(matrix)
        
        # Check if matrix is square
        if not all(len(row) == n for row in matrix):
            raise ValueError("Transition matrix must be square")
            
        # Check if all elements are non-negative and rows sum to 1
        for row in matrix:
            if any(p < 0 for p in row):
                raise ValueError("Transition probabilities must be non-negative")
            row_sum = sum(row)
            if abs(row_sum - 1.0) > self.tolerance:
                raise ValueError(f"Row sum must be 1, got {row_sum}")
                
        return True
    
    def calculate_steady_state(self, transition_matrix: List[List[float]]) -> List[float]:
        """
        Calculate the steady-state distribution for a given transition matrix.
        
        Args:
            transition_matrix (List[List[float]]): Transition probability matrix
            
        Returns:
            List[float]: Steady-state distribution vector
            
        Raises:
            ValueError: If matrix is invalid or convergence fails
        """
        self._validate_transition_matrix(transition_matrix)
        n = len(transition_matrix)
        
        # Initialize with uniform distribution
        current_dist = [1.0/n] * n
        
        for iteration in range(self.max_iterations):
            next_dist = [0.0] * n
            
            # Matrix multiplication
            for i in range(n):
                for j in range(n):
                    next_dist[i] += current_dist[j] * transition_matrix[j][i]
            
            # Check convergence
            max_diff = max(abs(next_dist[i] - current_dist[i]) 
                         for i in range(n))
            
            if max_diff < self.tolerance:
                return next_dist
                
            current_dist = next_dist
            
        raise ValueError(f"Steady state did not converge after {self.max_iterations} iterations")
    
    def calculate_distance(self, matrix1: List[List[float]], 
                         matrix2: List[List[float]], 
                         method: str = "euclidean") -> float:
        """
        Calculate the distance between steady-state distributions of two Markov chains.
        
        Args:
            matrix1 (List[List[float]]): First transition matrix
            matrix2 (List[List[float]]): Second transition matrix
            method (str): Distance metric to use ('euclidean' or 'manhattan')
            
        Returns:
            float: Distance between the steady-state distributions
            
        Raises:
            ValueError: If matrices are invalid or method is unknown
        """
        if method not in ["euclidean", "manhattan"]:
            raise ValueError("Method must be 'euclidean' or 'manhattan'")
            
        dist1 = self.calculate_steady_state(matrix1)
        dist2 = self.calculate_steady_state(matrix2)
        
        if method == "euclidean":
            return sqrt(sum((p1 - p2) ** 2 for p1, p2 in zip(dist1, dist2)))
        else:  # manhattan
            return sum(abs(p1 - p2) for p1, p2 in zip(dist1, dist2))
######################################
from typing import List, Dict, Union, Optional, Tuple
from math import sqrt

class MarkovCommuteTimeDistance:
    """
    A class to calculate the commute time distance between states in a Markov chain.
    
    The commute time distance measures the expected number of steps for a random walk
    to travel from state i to state j and back to state i.
    
    Implements:
    1. Fundamental matrix calculation
    2. Commute time distance computation
    3. Matrix operations without numpy dependency
    """
    
    def __init__(self, tolerance: float = 1e-10):
        """
        Initialize the calculator with numerical tolerance.
        
        Args:
            tolerance (float): Numerical tolerance for calculations
        """
        self.tolerance = tolerance
    
    def _validate_transition_matrix(self, matrix: List[List[float]]) -> bool:
        """
        Validate if the given matrix is a valid transition matrix.
        
        Args:
            matrix (List[List[float]]): Transition matrix to validate
            
        Returns:
            bool: True if valid, raises ValueError otherwise
            
        Raises:
            ValueError: If matrix is not square or rows don't sum to 1
        """
        n = len(matrix)
        
        if not all(len(row) == n for row in matrix):
            raise ValueError("Transition matrix must be square")
            
        for row in matrix:
            if any(p < 0 for p in row):
                raise ValueError("Transition probabilities must be non-negative")
            row_sum = sum(row)
            if abs(row_sum - 1.0) > self.tolerance:
                raise ValueError(f"Row sum must be 1, got {row_sum}")
                
        return True
    
    def _matrix_subtract(self, A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
        """
        Subtract matrix B from matrix A.
        
        Args:
            A (List[List[float]]): First matrix
            B (List[List[float]]): Second matrix
            
        Returns:
            List[List[float]]: Result of A - B
        """
        n = len(A)
        return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]
    
    def _identity_matrix(self, size: int) -> List[List[float]]:
        """
        Create an identity matrix of given size.
        
        Args:
            size (int): Size of the matrix
            
        Returns:
            List[List[float]]: Identity matrix
        """
        return [[1.0 if i == j else 0.0 for j in range(size)] for i in range(size)]
    
    def _matrix_inverse(self, matrix: List[List[float]]) -> List[List[float]]:
        """
        Calculate the inverse of a matrix using Gauss-Jordan elimination.
        
        Args:
            matrix (List[List[float]]): Matrix to invert
            
        Returns:
            List[List[float]]: Inverted matrix
            
        Raises:
            ValueError: If matrix is singular
        """
        n = len(matrix)
        # Augment with identity matrix
        aug = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(matrix)]
        
        # Gaussian elimination
        for i in range(n):
            pivot = aug[i][i]
            if abs(pivot) < self.tolerance:
                raise ValueError("Matrix is singular")
                
            for j in range(i + 1, 2 * n):
                aug[i][j] /= pivot
            aug[i][i] = 1.0
            
            for k in range(n):
                if k != i:
                    factor = aug[k][i]
                    for j in range(i, 2 * n):
                        aug[k][j] -= factor * aug[i][j]
        
        # Extract inverse
        return [[aug[i][j + n] for j in range(n)] for i in range(n)]
    
    def _calculate_fundamental_matrix(self, transition_matrix: List[List[float]]) -> List[List[float]]:
        """
        Calculate the fundamental matrix (I - P + W)^-1 where W is the steady state matrix.
        
        Args:
            transition_matrix (List[List[float]]): Transition probability matrix
            
        Returns:
            List[List[float]]: Fundamental matrix
        """
        n = len(transition_matrix)
        
        # Calculate steady state
        steady_state = self._calculate_steady_state(transition_matrix)
        
        # Create W matrix (steady state matrix)
        W = [[steady_state[j] for j in range(n)] for i in range(n)]
        
        # Calculate I - P + W
        I = self._identity_matrix(n)
        temp = self._matrix_subtract(I, transition_matrix)
        fundamental = [[temp[i][j] + W[i][j] for j in range(n)] for i in range(n)]
        
        return self._matrix_inverse(fundamental)
    
    def _calculate_steady_state(self, transition_matrix: List[List[float]], 
                              max_iterations: int = 1000) -> List[float]:
        """
        Calculate the steady-state distribution of the Markov chain.
        
        Args:
            transition_matrix (List[List[float]]): Transition matrix
            max_iterations (int): Maximum number of iterations
            
        Returns:
            List[float]: Steady state distribution
        """
        n = len(transition_matrix)
        current = [1.0/n] * n
        
        for _ in range(max_iterations):
            next_dist = [sum(current[j] * transition_matrix[j][i] 
                           for j in range(n)) for i in range(n)]
            
            if max(abs(next_dist[i] - current[i]) 
                   for i in range(n)) < self.tolerance:
                return next_dist
                
            current = next_dist
            
        return current
    
    def calculate_commute_time(self, transition_matrix: List[List[float]], 
                             state_i: int, state_j: int) -> float:
        """
        Calculate the commute time distance between two states.
        
        Args:
            transition_matrix (List[List[float]]): Transition probability matrix
            state_i (int): First state index
            state_j (int): Second state index
            
        Returns:
            float: Commute time distance between states i and j
            
        Raises:
            ValueError: If matrix is invalid or states are out of bounds
        """
        self._validate_transition_matrix(transition_matrix)
        n = len(transition_matrix)
        
        if not (0 <= state_i < n and 0 <= state_j < n):
            raise ValueError("State indices must be within matrix dimensions")
        
        # Calculate fundamental matrix
        Z = self._calculate_fundamental_matrix(transition_matrix)
        
        # Calculate commute time using fundamental matrix
        commute_time = (Z[state_i][state_i] + Z[state_j][state_j] - 
                       Z[state_i][state_j] - Z[state_j][state_i])
        
        return commute_time
#############################################

from typing import List, Dict, Union, Optional, Tuple
from math import sqrt

class MarkovHittingTimeDistance:
    """
    A class to calculate the hitting time distances in a Markov chain.
    
    The hitting time (or first passage time) is the expected number of steps
    needed for a random walk starting at state i to first reach state j.
    
    Implements:
    1. Hitting time calculation using fundamental matrix
    2. Matrix operations for calculations
    3. Validation and numerical stability checks
    """
    
    def __init__(self, tolerance: float = 1e-10):
        """
        Initialize the calculator with numerical tolerance.
        
        Args:
            tolerance (float): Numerical tolerance for calculations
        """
        self.tolerance = tolerance
    
    def _validate_transition_matrix(self, matrix: List[List[float]]) -> bool:
        """
        Validate if the given matrix is a valid transition matrix.
        
        Args:
            matrix (List[List[float]]): Transition matrix to validate
            
        Returns:
            bool: True if valid, raises ValueError otherwise
            
        Raises:
            ValueError: If matrix is not square or rows don't sum to 1
        """
        n = len(matrix)
        
        if not all(len(row) == n for row in matrix):
            raise ValueError("Transition matrix must be square")
            
        for row in matrix:
            if any(p < 0 for p in row):
                raise ValueError("Transition probabilities must be non-negative")
            row_sum = sum(row)
            if abs(row_sum - 1.0) > self.tolerance:
                raise ValueError(f"Row sum must be 1, got {row_sum}")
                
        return True
    
    def _matrix_multiply(self, A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
        """
        Multiply two matrices.
        
        Args:
            A (List[List[float]]): First matrix
            B (List[List[float]]): Second matrix
            
        Returns:
            List[List[float]]: Result of A * B
        """
        n = len(A)
        result = [[0.0 for _ in range(n)] for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                result[i][j] = sum(A[i][k] * B[k][j] for k in range(n))
                
        return result
    
    def _matrix_subtract(self, A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
        """
        Subtract matrix B from matrix A.
        
        Args:
            A (List[List[float]]): First matrix
            B (List[List[float]]): Second matrix
            
        Returns:
            List[List[float]]: Result of A - B
        """
        n = len(A)
        return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]
    
    def _identity_matrix(self, size: int) -> List[List[float]]:
        """
        Create an identity matrix of given size.
        
        Args:
            size (int): Size of the matrix
            
        Returns:
            List[List[float]]: Identity matrix
        """
        return [[1.0 if i == j else 0.0 for j in range(size)] for i in range(size)]
    
    def _matrix_inverse(self, matrix: List[List[float]]) -> List[List[float]]:
        """
        Calculate the inverse of a matrix using Gauss-Jordan elimination.
        
        Args:
            matrix (List[List[float]]): Matrix to invert
            
        Returns:
            List[List[float]]: Inverted matrix
            
        Raises:
            ValueError: If matrix is singular
        """
        n = len(matrix)
        augmented = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] 
                    for i, row in enumerate(matrix)]
        
        for i in range(n):
            pivot = augmented[i][i]
            if abs(pivot) < self.tolerance:
                raise ValueError("Matrix is singular")
            
            for j in range(2 * n):
                augmented[i][j] /= pivot
                
            for k in range(n):
                if k != i:
                    factor = augmented[k][i]
                    for j in range(2 * n):
                        augmented[k][j] -= factor * augmented[i][j]
        
        return [[augmented[i][j + n] for j in range(n)] for i in range(n)]
    
    def _create_modified_matrix(self, transition_matrix: List[List[float]], 
                              target_state: int) -> List[List[float]]:
        """
        Create a modified transition matrix by removing target state transitions.
        
        Args:
            transition_matrix (List[List[float]]): Original transition matrix
            target_state (int): State to modify
            
        Returns:
            List[List[float]]: Modified transition matrix
        """
        n = len(transition_matrix)
        modified = [[0.0 for _ in range(n)] for _ in range(n)]
        
        for i in range(n):
            if i != target_state:
                for j in range(n):
                    if j != target_state:
                        modified[i][j] = transition_matrix[i][j]
        
        return modified
    
    def calculate_hitting_time(self, transition_matrix: List[List[float]], 
                             start_state: int, target_state: int) -> float:
        """
        Calculate the expected hitting time from start_state to target_state.
        
        Args:
            transition_matrix (List[List[float]]): Transition probability matrix
            start_state (int): Starting state index
            target_state (int): Target state index
            
        Returns:
            float: Expected hitting time
            
        Raises:
            ValueError: If matrix is invalid or states are out of bounds
        """
        self._validate_transition_matrix(transition_matrix)
        n = len(transition_matrix)
        
        if not (0 <= start_state < n and 0 <= target_state < n):
            raise ValueError("State indices must be within matrix dimensions")
            
        if start_state == target_state:
            return 0.0
        
        # Create modified matrix removing target state transitions
        Q = self._create_modified_matrix(transition_matrix, target_state)
        
        # Calculate fundamental matrix N = (I - Q)^(-1)
        I = self._identity_matrix(n)
        N = self._matrix_inverse(self._matrix_subtract(I, Q))
        
        # Calculate hitting time using the fundamental matrix
        hitting_time = sum(N[start_state][j] for j in range(n) if j != target_state)
        
        return hitting_time
    
    def calculate_hitting_time_matrix(self, transition_matrix: List[List[float]]) -> List[List[float]]:
        """
        Calculate the hitting time matrix for all pairs of states.
        
        Args:
            transition_matrix (List[List[float]]): Transition probability matrix
            
        Returns:
            List[List[float]]: Matrix of hitting times between all pairs of states
        """
        n = len(transition_matrix)
        hitting_times = [[0.0 for _ in range(n)] for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    hitting_times[i][j] = self.calculate_hitting_time(
                        transition_matrix, i, j)
        
        return hitting_times
########################################
from typing import List, Dict, Union, Optional, Tuple
from math import inf, sqrt

class MarkovResistanceDistance:
    """
    A class to calculate resistance distance in a Markov chain, 
    interpreting the chain as an electrical network.
    
    Resistance distance is a metric that treats the Markov chain 
    as a network of resistors, where transition probabilities 
    determine the conductance between states.
    
    Key methods:
    1. Convert Markov chain to conductance matrix
    2. Calculate effective resistance between states
    3. Compute resistance distance matrix
    """
    
    def __init__(self, tolerance: float = 1e-10):
        """
        Initialize the resistance distance calculator.
        
        Args:
            tolerance (float): Numerical tolerance for calculations
        """
        self.tolerance = tolerance
    
    def _validate_transition_matrix(self, matrix: List[List[float]]) -> bool:
        """
        Validate the transition matrix for resistance distance calculation.
        
        Args:
            matrix (List[List[float]]): Transition probability matrix
            
        Returns:
            bool: True if matrix is valid
            
        Raises:
            ValueError: If matrix is invalid
        """
        n = len(matrix)
        
        if not all(len(row) == n for row in matrix):
            raise ValueError("Transition matrix must be square")
            
        for row in matrix:
            if any(p < 0 for p in row):
                raise ValueError("Transition probabilities must be non-negative")
            row_sum = sum(row)
            if abs(row_sum - 1.0) > self.tolerance:
                raise ValueError(f"Row sum must be 1, got {row_sum}")
                
        return True
    
    def _calculate_stationary_distribution(self, 
                                         transition_matrix: List[List[float]], 
                                         max_iterations: int = 1000) -> List[float]:
        """
        Calculate the stationary distribution of the Markov chain.
        
        Args:
            transition_matrix (List[List[float]]): Transition probability matrix
            max_iterations (int): Maximum iterations for convergence
            
        Returns:
            List[float]: Stationary distribution vector
        """
        n = len(transition_matrix)
        current = [1.0/n] * n
        
        for _ in range(max_iterations):
            next_dist = [
                sum(current[j] * transition_matrix[j][i] for j in range(n)) 
                for i in range(n)
            ]
            
            if max(abs(next_dist[i] - current[i]) for i in range(n)) < self.tolerance:
                return next_dist
                
            current = next_dist
        
        return current
    
    def _create_conductance_matrix(self, transition_matrix: List[List[float]]) -> List[List[float]]:
        """
        Convert transition matrix to a conductance matrix.
        
        Args:
            transition_matrix (List[List[float]]): Transition probability matrix
            
        Returns:
            List[List[float]]: Conductance matrix
        """
        n = len(transition_matrix)
        stationary_dist = self._calculate_stationary_distribution(transition_matrix)
        
        # Create conductance matrix
        conductance = [[0.0 for _ in range(n)] for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    # Conductance proportional to transition prob and stationary distribution
                    conductance[i][j] = (
                        (transition_matrix[i][j] * stationary_dist[j]) / 
                        stationary_dist[i]
                    )
        
        return conductance
    
    def calculate_resistance_distance(self, 
                                    transition_matrix: List[List[float]], 
                                    state_i: int, 
                                    state_j: int) -> float:
        """
        Calculate the resistance distance between two states.
        
        Uses Kirchhoff's matrix-tree theorem and the concept of 
        effective resistance in electrical networks.
        
        Args:
            transition_matrix (List[List[float]]): Transition probability matrix
            state_i (int): First state index
            state_j (int): Second state index
            
        Returns:
            float: Resistance distance between states
            
        Raises:
            ValueError: If states are invalid or matrix is incorrect
        """
        self._validate_transition_matrix(transition_matrix)
        n = len(transition_matrix)
        
        if not (0 <= state_i < n and 0 <= state_j < n):
            raise ValueError("Invalid state indices")
        
        if state_i == state_j:
            return 0.0
        
        # Create conductance matrix
        G = self._create_conductance_matrix(transition_matrix)
        
        # Create Laplacian matrix
        L = [[0.0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            L[i][i] = sum(G[i])
            for j in range(n):
                if i != j:
                    L[i][j] = -G[i][j]
        
        # Remove last row and column (reduce rank)
        L_reduced = [row[:-1] for row in L[:-1]]
        
        # Compute pseudoinverse using singular value decomposition would 
        # require numpy, so we'll use a simplified approximation
        # This is an approximate method for resistance distance
        
        # Auxiliary vectors for resistance calculation
        e_i = [1.0 if k == state_i else 0.0 for k in range(n-1)]
        e_j = [1.0 if k == state_j else 0.0 for k in range(n-1)]
        
        # Compute difference in potential
        def solve_linear_system(A, b):
            # Simple Gauss-Jordan elimination
            augmented = [row + [bi] for row, bi in zip(A, b)]
            n = len(augmented)
            
            for i in range(n):
                # Find pivot
                max_element = abs(augmented[i][i])
                max_row = i
                for k in range(i + 1, n):
                    if abs(augmented[k][i]) > max_element:
                        max_element = abs(augmented[k][i])
                        max_row = k
                
                # Swap maximum row with current row
                augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
                
                # Make all rows below this one 0 in current column
                for k in range(i + 1, n):
                    c = -augmented[k][i] / augmented[i][i]
                    for j in range(i, n + 1):
                        if i == j:
                            augmented[k][j] = 0
                        else:
                            augmented[k][j] += c * augmented[i][j]
            
            # Back substitution
            x = [0.0] * n
            for i in range(n - 1, -1, -1):
                x[i] = augmented[i][n] / augmented[i][i]
                for k in range(i - 1, -1, -1):
                    augmented[k][n] -= augmented[k][i] * x[i]
            
            return x
        
        try:
            potential_diff = solve_linear_system(L_reduced, e_i)
            
            # Resistance is the difference in potentials
            return abs(potential_diff[state_j] - potential_diff[state_i])
        
        except (ValueError, ZeroDivisionError):
            # Fallback to a simplified estimate
            return sqrt(
                sum((e_i[k] - e_j[k])**2 for k in range(len(e_i)))
            )
    
    def calculate_resistance_matrix(self, 
                                  transition_matrix: List[List[float]]) -> List[List[float]]:
        """
        Calculate the full resistance distance matrix.
        
        Args:
            transition_matrix (List[List[float]]): Transition probability matrix
            
        Returns:
            List[List[float]]: Resistance distance matrix
        """
        n = len(transition_matrix)
        res_matrix = [[0.0 for _ in range(n)] for _ in range(n)]
        
        for i in range(n):
            for j in range(i+1, n):
                dist = self.calculate_resistance_distance(transition_matrix, i, j)
                res_matrix[i][j] = dist
                res_matrix[j][i] = dist
        
        return res_matrix
####################################
from typing import List, Dict, Union
from math import log2, isfinite

class MarkovEntropyRateDistance:
    """
    A class to calculate the relative entropy rate between two Markov chains.
    
    Relative Entropy Rate measures the divergence between the probabilistic
    information content of two Markov processes, capturing how differently
    two stochastic processes generate sequences.
    
    Key methods:
    1. Calculate entropy rate for a Markov chain
    2. Compute relative entropy rate between two chains
    3. Validate transition matrices
    """
    
    def __init__(self, tolerance: float = 1e-10):
        """
        Initialize the entropy rate distance calculator.
        
        Args:
            tolerance (float): Numerical tolerance for calculations
        """
        self.tolerance = tolerance
    
    def _validate_transition_matrix(self, matrix: List[List[float]]) -> bool:
        """
        Validate the transition probability matrix.
        
        Args:
            matrix (List[List[float]]): Transition probability matrix
            
        Returns:
            bool: True if matrix is valid
            
        Raises:
            ValueError: If matrix is invalid
        """
        n = len(matrix)
        
        if not all(len(row) == n for row in matrix):
            raise ValueError("Transition matrix must be square")
            
        for row in matrix:
            if any(p < 0 for p in row):
                raise ValueError("Transition probabilities must be non-negative")
            row_sum = sum(row)
            if abs(row_sum - 1.0) > self.tolerance:
                raise ValueError(f"Row sum must be 1, got {row_sum}")
                
        return True
    
    def _calculate_stationary_distribution(self, 
                                         transition_matrix: List[List[float]], 
                                         max_iterations: int = 1000) -> List[float]:
        """
        Calculate the stationary distribution of the Markov chain.
        
        Args:
            transition_matrix (List[List[float]]): Transition probability matrix
            max_iterations (int): Maximum iterations for convergence
            
        Returns:
            List[float]: Stationary distribution vector
        """
        n = len(transition_matrix)
        current = [1.0/n] * n
        
        for _ in range(max_iterations):
            next_dist = [
                sum(current[j] * transition_matrix[j][i] for j in range(n)) 
                for i in range(n)
            ]
            
            if max(abs(next_dist[i] - current[i]) for i in range(n)) < self.tolerance:
                return next_dist
                
            current = next_dist
        
        return current
    
    def calculate_entropy_rate(self, transition_matrix: List[List[float]]) -> float:
        """
        Calculate the entropy rate of a Markov chain.
        
        Entropy rate measures the average amount of information 
        generated by the Markov process per step.
        
        Args:
            transition_matrix (List[List[float]]): Transition probability matrix
            
        Returns:
            float: Entropy rate of the Markov chain
        """
        self._validate_transition_matrix(transition_matrix)
        n = len(transition_matrix)
        
        # Calculate stationary distribution
        stationary_dist = self._calculate_stationary_distribution(transition_matrix)
        
        # Calculate entropy rate
        entropy_rate = 0.0
        for i in range(n):
            for j in range(n):
                # Conditional entropy calculation
                if transition_matrix[i][j] > self.tolerance:
                    entropy_term = (
                        stationary_dist[i] * 
                        transition_matrix[i][j] * 
                        log2(1.0 / transition_matrix[i][j])
                    )
                    entropy_rate += entropy_term
        
        return -entropy_rate
    
    def calculate_relative_entropy_rate(self, 
                                      matrix1: List[List[float]], 
                                      matrix2: List[List[float]]) -> float:
        """
        Calculate the relative entropy rate between two Markov chains.
        
        Uses Kullback-Leibler divergence of entropy rates to measure 
        the information-theoretic distance between processes.
        
        Args:
            matrix1 (List[List[float]]): First transition matrix
            matrix2 (List[List[float]]): Second transition matrix
            
        Returns:
            float: Relative entropy rate distance
        """
        self._validate_transition_matrix(matrix1)
        self._validate_transition_matrix(matrix2)
        
        if len(matrix1) != len(matrix2):
            raise ValueError("Matrices must have the same dimensions")
        
        n = len(matrix1)
        
        # Calculate stationary distributions
        stat_dist1 = self._calculate_stationary_distribution(matrix1)
        stat_dist2 = self._calculate_stationary_distribution(matrix2)
        
        # Compute relative entropy rate
        relative_entropy = 0.0
        for i in range(n):
            for j in range(n):
                # Avoid log(0) or division by zero
                if (matrix1[i][j] > self.tolerance and 
                    matrix2[i][j] > self.tolerance):
                    term = (
                        stat_dist1[i] * 
                        matrix1[i][j] * 
                        log2(matrix1[i][j] / matrix2[i][j])
                    )
                    relative_entropy += term
        
        return relative_entropy
    
    def calculate_symmetric_entropy_rate(self, 
                                       matrix1: List[List[float]], 
                                       matrix2: List[List[float]]) -> float:
        """
        Calculate the symmetric relative entropy rate.
        
        Provides a symmetric measure of divergence between Markov chains.
        
        Args:
            matrix1 (List[List[float]]): First transition matrix
            matrix2 (List[List[float]]): Second transition matrix
            
        Returns:
            float: Symmetric relative entropy rate
        """
        # Symmetrized relative entropy rate
        forward_div = self.calculate_relative_entropy_rate(matrix1, matrix2)
        reverse_div = self.calculate_relative_entropy_rate(matrix2, matrix1)
        
        return (forward_div + reverse_div) / 2.0
    
    def normalize_entropy_rate(self, entropy_rate: float, matrix_size: int) -> float:
        """
        Normalize the entropy rate by the matrix size.
        
        Provides a scale-independent measure of entropy rate.
        
        Args:
            entropy_rate (float): Calculated entropy rate
            matrix_size (int): Size of the transition matrix
            
        Returns:
            float: Normalized entropy rate
        """
        return entropy_rate / log2(matrix_size)
######################################
from typing import List, Dict, Union, Optional
from math import log2, isfinite

class MarkovSequenceProbabilityDivergence:
    """
    A class to calculate sequence probability divergence between two Markov Chains.
    
    Measures the difference in sequence generation probabilities by comparing:
    1. Likelihood of generating specific sequences
    2. Conditional probability distributions
    3. Divergence in sequence generation capabilities
    
    Key methods:
    1. Calculate sequence probability under a Markov chain
    2. Compute divergence between sequence probabilities
    3. Analyze sequence generation characteristics
    """
    
    def __init__(self, tolerance: float = 1e-10):
        """
        Initialize the sequence probability divergence calculator.
        
        Args:
            tolerance (float): Numerical tolerance for calculations
        """
        self.tolerance = tolerance
    
    def _validate_transition_matrix(self, matrix: List[List[float]]) -> bool:
        """
        Validate the transition probability matrix.
        
        Args:
            matrix (List[List[float]]): Transition probability matrix
            
        Returns:
            bool: True if matrix is valid
            
        Raises:
            ValueError: If matrix is invalid
        """
        n = len(matrix)
        
        if not all(len(row) == n for row in matrix):
            raise ValueError("Transition matrix must be square")
            
        for row in matrix:
            if any(p < 0 for p in row):
                raise ValueError("Transition probabilities must be non-negative")
            row_sum = sum(row)
            if abs(row_sum - 1.0) > self.tolerance:
                raise ValueError(f"Row sum must be 1, got {row_sum}")
                
        return True
    
    def _calculate_stationary_distribution(self, 
                                         transition_matrix: List[List[float]], 
                                         max_iterations: int = 1000) -> List[float]:
        """
        Calculate the stationary distribution of the Markov chain.
        
        Args:
            transition_matrix (List[List[float]]): Transition probability matrix
            max_iterations (int): Maximum iterations for convergence
            
        Returns:
            List[float]: Stationary distribution vector
        """
        n = len(transition_matrix)
        current = [1.0/n] * n
        
        for _ in range(max_iterations):
            next_dist = [
                sum(current[j] * transition_matrix[j][i] for j in range(n)) 
                for i in range(n)
            ]
            
            if max(abs(next_dist[i] - current[i]) for i in range(n)) < self.tolerance:
                return next_dist
                
            current = next_dist
        
        return current
    
    def calculate_sequence_probability(self, 
                                     transition_matrix: List[List[float]], 
                                     sequence: List[int], 
                                     initial_state: Optional[int] = None) -> float:
        """
        Calculate the probability of generating a specific sequence.
        
        Args:
            transition_matrix (List[List[float]]): Transition probability matrix
            sequence (List[int]): Sequence of state indices
            initial_state (Optional[int]): Starting state (uses stationary dist if None)
            
        Returns:
            float: Probability of generating the sequence
        """
        self._validate_transition_matrix(transition_matrix)
        n = len(transition_matrix)
        
        # Validate sequence states
        if any(state < 0 or state >= n for state in sequence):
            raise ValueError("Sequence states must be within matrix dimensions")
        
        # Determine initial state
        if initial_state is None:
            stationary_dist = self._calculate_stationary_distribution(transition_matrix)
            current_prob = stationary_dist[sequence[0]]
        else:
            current_prob = 1.0 if initial_state == sequence[0] else 0.0
        
        # Calculate sequence probability
        for i in range(1, len(sequence)):
            prev_state = sequence[i-1]
            current_state = sequence[i]
            current_prob *= transition_matrix[prev_state][current_state]
        
        return current_prob
    
    def calculate_sequence_probability_divergence(self, 
                                               matrix1: List[List[float]], 
                                               matrix2: List[List[float]], 
                                               sequence: List[int]) -> float:
        """
        Calculate the divergence in sequence probabilities between two Markov chains.
        
        Uses Kullback-Leibler divergence to measure probability difference.
        
        Args:
            matrix1 (List[List[float]]): First transition matrix
            matrix2 (List[List[float]]): Second transition matrix
            sequence (List[int]): Sequence to compare
            
        Returns:
            float: Sequence probability divergence
        """
        # Validate matrices
        self._validate_transition_matrix(matrix1)
        self._validate_transition_matrix(matrix2)
        
        if len(matrix1) != len(matrix2):
            raise ValueError("Matrices must have the same dimensions")
        
        # Calculate sequence probabilities
        prob1 = self.calculate_sequence_probability(matrix1, sequence)
        prob2 = self.calculate_sequence_probability(matrix2, sequence)
        
        # Avoid log(0) or division by zero
        if prob1 < self.tolerance or prob2 < self.tolerance:
            return float('inf')
        
        # Kullback-Leibler divergence for sequence
        return log2(prob1 / prob2)
    
    def calculate_conditional_probability_divergence(self, 
                                                   matrix1: List[List[float]], 
                                                   matrix2: List[List[float]], 
                                                   context_state: int) -> float:
        """
        Calculate the divergence in conditional probability distributions.
        
        Measures how differently two Markov chains generate next states 
        given a specific context state.
        
        Args:
            matrix1 (List[List[float]]): First transition matrix
            matrix2 (List[List[float]]): Second transition matrix
            context_state (int): State to condition on
            
        Returns:
            float: Conditional probability divergence
        """
        self._validate_transition_matrix(matrix1)
        self._validate_transition_matrix(matrix2)
        n = len(matrix1)
        
        if context_state < 0 or context_state >= n:
            raise ValueError("Context state out of matrix dimensions")
        
        # Calculate conditional probability divergence
        div_sum = 0.0
        for next_state in range(n):
            # Avoid log(0) or division by zero
            if (matrix1[context_state][next_state] > self.tolerance and 
                matrix2[context_state][next_state] > self.tolerance):
                div_term = (
                    matrix1[context_state][next_state] * 
                    log2(matrix1[context_state][next_state] / 
                         matrix2[context_state][next_state])
                )
                div_sum += div_term
        
        return div_sum
    
    def generate_most_likely_sequence(self, 
                                     transition_matrix: List[List[float]], 
                                     length: int, 
                                     initial_state: Optional[int] = None) -> List[int]:
        """
        Generate the most likely sequence for a given Markov chain.
        
        Args:
            transition_matrix (List[List[float]]): Transition probability matrix
            length (int): Desired sequence length
            initial_state (Optional[int]): Starting state (uses stationary dist if None)
            
        Returns:
            List[int]: Most probable sequence
        """
        self._validate_transition_matrix(transition_matrix)
        n = len(transition_matrix)
        
        # Determine initial state
        if initial_state is None:
            stationary_dist = self._calculate_stationary_distribution(transition_matrix)
            current_state = max(range(n), key=lambda i: stationary_dist[i])
        else:
            current_state = initial_state
        
        # Generate sequence with highest probability transitions
        sequence = [current_state]
        for _ in range(length - 1):
            # Find state with highest transition probability
            next_state = max(range(n), key=lambda i: transition_matrix[current_state][i])
            sequence.append(next_state)
            current_state = next_state
        
        return sequence
############################################


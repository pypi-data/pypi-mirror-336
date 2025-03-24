from .mainClass import *
from .tools     import Matrix
from .vectorDistance     import Euclidean,Vector

class matrixDistance(Distance,Matrix):

  def __init__(self)-> None:
        super().__init__()
        self.type='matrix_float'
  def example(self):
      if self.type=='matrix_float':
        self.obj1_example=Matrix()  .generate(4,4)
        self.obj2_example=Matrix()  .generate(4,4)
      super().example()

from typing import List, Tuple, Union, Optional
import math

class CanonicalCorrelation(matrixDistance):
    """
    A class that implements Canonical Correlation Analysis (CCA) to measure similarity
    between two matrices by finding the maximum correlation between their linear combinations.
    
    This implementation uses simplified matrix operations and a power iteration method
    for eigenvalue computation instead of relying on external linear algebra libraries.
    
    Methods
    -------
    compute(matrix1, matrix2):
        Computes the canonical correlations between two matrices
    center_matrix(matrix):
        Centers a matrix by subtracting its mean
    covariance_matrix(matrix1, matrix2):
        Computes the covariance matrix between two matrices
    power_iteration(matrix, num_iterations=100):
        Computes the dominant eigenvalue and eigenvector using power iteration
    """
    
    def __init__(self, tolerance=1e-10, max_iterations=100):
        """
        Initialize the CanonicalCorrelation calculator.
        
        Parameters
        ----------
        tolerance : float
            Numerical tolerance for convergence
        max_iterations : int
            Maximum number of iterations for power method
        """
        super().__init__()
        
        self.tolerance = tolerance
        self.max_iterations = max_iterations
    
    @staticmethod
    def validate_matrices(matrix1, matrix2):
        """
        Validates input matrices.
        
        Parameters
        ----------
        matrix1, matrix2 : list of lists
            Input matrices to compare
            
        Raises
        ------
        ValueError
            If matrices are invalid or empty
        """
        if not matrix1 or not matrix2:
            raise ValueError("Matrices cannot be empty")
            
        if not all(isinstance(row, list) for row in matrix1) or \
           not all(isinstance(row, list) for row in matrix2):
            raise TypeError("Inputs must be lists of lists")
            
        if len(matrix1) != len(matrix2):
            raise ValueError("Matrices must have the same number of rows")
            
        if not all(len(row) == len(matrix1[0]) for row in matrix1) or \
           not all(len(row) == len(matrix2[0]) for row in matrix2):
            raise ValueError("All rows must have the same length within each matrix")

    def center_matrix(self, matrix):
        """
        Centers a matrix by subtracting the mean of each column.
        
        Parameters
        ----------
        matrix : list of lists
            Input matrix
            
        Returns
        -------
        list of lists
            Centered matrix
        """
        n_rows, n_cols = len(matrix), len(matrix[0])
        
        # Compute column means
        col_means = [sum(matrix[i][j] for i in range(n_rows)) / n_rows 
                    for j in range(n_cols)]
        
        # Center the matrix
        centered = [[matrix[i][j] - col_means[j] 
                    for j in range(n_cols)]
                   for i in range(n_rows)]
        
        return centered

    def matrix_multiply(self, matrix1, matrix2):
        """
        Multiplies two matrices.
        
        Parameters
        ----------
        matrix1, matrix2 : list of lists
            Input matrices
            
        Returns
        -------
        list of lists
            Product matrix
        """
        n, m = len(matrix1), len(matrix1[0])
        p = len(matrix2[0]) if matrix2 else 0
        
        result = [[0] * p for _ in range(n)]
        for i in range(n):
            for j in range(p):
                result[i][j] = sum(matrix1[i][k] * matrix2[k][j] 
                                 for k in range(m))
        return result

    def matrix_transpose(self, matrix):
        """
        Computes matrix transpose.
        
        Parameters
        ----------
        matrix : list of lists
            Input matrix
            
        Returns
        -------
        list of lists
            Transposed matrix
        """
        if not matrix or not matrix[0]:
            return []
        return [[matrix[j][i] for j in range(len(matrix))]
                for i in range(len(matrix[0]))]

    def covariance_matrix(self, matrix1, matrix2):
        """
        Computes the covariance matrix between two matrices.
        
        Parameters
        ----------
        matrix1, matrix2 : list of lists
            Input matrices
            
        Returns
        -------
        list of lists
            Covariance matrix
        """
        n_rows = len(matrix1)
        
        # Center the matrices
        centered1 = self.center_matrix(matrix1)
        centered2 = self.center_matrix(matrix2)
        
        # Compute covariance
        transposed1 = self.matrix_transpose(centered1)
        covariance = self.matrix_multiply(transposed1, centered2)
        
        # Scale by n-1
        scale = 1.0 / (n_rows - 1)
        return [[cell * scale for cell in row] for row in covariance]

    def power_iteration(self, matrix, num_iterations=100):
        """
        Computes the dominant eigenvalue and eigenvector using power iteration.
        
        Parameters
        ----------
        matrix : list of lists
            Input matrix
        num_iterations : int
            Number of iterations
            
        Returns
        -------
        tuple
            (eigenvalue, eigenvector)
        """
        n = len(matrix)
        # Initialize random vector
        vector = [1.0/n**0.5] * n
        
        for _ in range(num_iterations):
            # Multiply matrix by vector
            new_vector = [sum(matrix[i][j] * vector[j] 
                            for j in range(n))
                        for i in range(n)]
            
            # Normalize
            norm = sum(x*x for x in new_vector) ** 0.5
            if norm < self.tolerance:
                break
                
            vector = [x/norm for x in new_vector]
            
        # Compute Rayleigh quotient
        eigenvalue = sum(sum(matrix[i][j] * vector[i] * vector[j]
                           for j in range(n))
                       for i in range(n))
        
        return eigenvalue, vector

    def compute(self, matrix1, matrix2):
        """
        Computes the canonical correlations between two matrices.
        
        Parameters
        ----------
        matrix1, matrix2 : list of lists
            Input matrices
            
        Returns
        -------
        tuple
            (correlations, canonical_vectors_1, canonical_vectors_2)
            
        Examples
        --------
        >>> m1 = [[1, 2], [3, 4], [5, 6]]
        >>> m2 = [[7, 8], [9, 10], [11, 12]]
        >>> cca = CanonicalCorrelation()
        >>> correlations, vectors1, vectors2 = cca.compute(m1, m2)
        """
        # Validate inputs
        self.validate_matrices(matrix1, matrix2)
        
        # Compute covariance matrices
        C11 = self.covariance_matrix(matrix1, matrix1)
        C22 = self.covariance_matrix(matrix2, matrix2)
        C12 = self.covariance_matrix(matrix1, matrix2)
        C21 = self.matrix_transpose(C12)
        
        # Compute matrices for eigenvalue problem
        # This is a simplified version of the actual CCA computation
        eigenvalue, eigenvector = self.power_iteration(C12)
        correlation = eigenvalue / (len(matrix1) - 1)
        
        # Get canonical vectors
        vectors1 = eigenvector
        vectors2 = self.matrix_multiply(C21, [[x] for x in eigenvector])
        vectors2 = [x[0] for x in vectors2]
        
        return correlation
        #return correlation, vectors1, vectors2


from typing import List, TypeVar, Union
from math import sqrt

T = TypeVar('T', int, float)

class CycleMatrixDistance(matrixDistance):
    """
    A class to calculate distance between matrices based on cycle detection.
    
    The distance is computed by analyzing the cyclic patterns in matrix transformations.
    Supports integer and float matrix elements.
    """
    
    def __init__(self,tolerance: float = 1e-6):
        """
        Initialize the distance calculator with two matrices.
        
        Args:
            matrix1 (List[List[T]]): First input matrix 
            matrix2 (List[List[T]]): Second input matrix
        
        Raises:
            ValueError: If matrices have different dimensions
        """
        super().__init__()
        
        self.tolerance=tolerance
        
    
    def _validate_matrices(self, matrix1: List[List[T]], matrix2: List[List[T]]) -> None:
        """
        Validate that both matrices have the same dimensions.
        
        Args:
            matrix1 (List[List[T]]): First matrix to validate
            matrix2 (List[List[T]]): Second matrix to validate
        
        Raises:
            ValueError: If matrices have different dimensions
        """
        if len(matrix1) != len(matrix2):
            raise ValueError("Matrices must have the same number of rows")
        
        if len(matrix1[0]) != len(matrix2[0]):
            raise ValueError("Matrices must have the same number of columns")
    
    def _detect_local_cycles(self,matrix1: List[List[T]], matrix2: List[List[T]]) -> List[List[int]]:
        """
        Detect local cyclic patterns between corresponding matrix elements.
        
        Args:
            tolerance (float): Precision threshold for cycle detection
        
        Returns:
            List[List[int]]: Cycle lengths for each matrix element
        """
        rows = len(matrix1)
        cols = len(matrix1[0])
        cycle_map: List[List[int]] = [[0 for _ in range(cols)] for _ in range(rows)]
        
        for i in range(rows):
            for j in range(cols):
                # Compare elements and detect cycle length
                current = matrix1[i][j]
                target = matrix2[i][j]
                
                if abs(current - target) <= self.tolerance:
                    cycle_map[i][j] = 0
                else:
                    # Estimate cycle length based on element differences
                    cycle_length = int(abs(target - current) * 100)
                    cycle_map[i][j] = max(1, cycle_length)
        
        return cycle_map
    
    def compute(self, matrix1: List[List[T]], matrix2: List[List[T]]) -> float:
        """
        Compute the distance between matrices based on cycle detection.
        
        Args:
            tolerance (float): Precision threshold for cycle detection
        
        Returns:
            float: Calculated distance representing cyclic transformation complexity
        """
        cycle_map = self._detect_local_cycles(matrix1,matrix2)
        
        # Compute total cycle complexity
        total_cycle_complexity = sum(
            sum(row) for row in cycle_map
        )
        
        # Normalize distance using root mean square
        matrix_size = self.rows * self.cols
        normalized_distance = sqrt(total_cycle_complexity / matrix_size)
        
        return normalized_distance
    
    def __str__(self) -> str:
        """
        Provide a string representation of the distance calculation.
        
        Returns:
            str: Descriptive string of cycle matrix distance
        """
        distance = self.compute()
        return f"Cycle Matrix Distance: {distance:.4f}"
               
class Mahalanobis(matrixDistance):
    """
    A class that calculates the Mahalanobis distance between a point and a set of points.
    The Mahalanobis distance takes into account the correlations between variables
    in the matrices by using the inverse of the covariance matrix.
    
    This implementation is pure Python without numpy dependency.
    """
    
    data: List[List[float]]
    n_samples: int
    n_features: int
    mean: List[float]
    covariance_matrix: List[List[float]]
    inv_covariance_matrix: List[List[float]]
    
    def __init__(self, regularization: float = 1e-5):
        """
        Initialize the MahalanobisDistance calculator with a dataset.
        
        Args:
            data: A list of lists where each inner list represents a data point
                 and each element represents a feature value.
            regularization: A small value added to the diagonal of the covariance matrix
                           to ensure it is invertible. Default is 1e-5.
        """
        super().__init__()

        self.regularization: float = regularization
       
    
    def _calculate_mean(self) -> List[float]:
        """
        Calculate the mean vector of the dataset.
        
        Returns:
            A list containing the mean value for each feature.
        """
        mean: List[float] = [0.0] * self.n_features
        
        for point in self.data:
            for i in range(self.n_features):
                mean[i] += point[i]
        
        # Divide by number of samples
        for i in range(self.n_features):
            mean[i] /= self.n_samples
            
        return mean
    
    def _calculate_covariance_matrix(self) -> List[List[float]]:
        """
        Calculate the covariance matrix of the dataset with regularization.
        
        Returns:
            A list of lists representing the covariance matrix.
        """
        # Initialize covariance matrix with zeros
        cov_matrix: List[List[float]] = [[0.0 for _ in range(self.n_features)] for _ in range(self.n_features)]
        
        # Calculate covariance matrix
        for point in self.data:
            for i in range(self.n_features):
                for j in range(self.n_features):
                    cov_matrix[i][j] += (point[i] - self.mean[i]) * (point[j] - self.mean[j])
        
        # Divide by n_samples - 1 for unbiased estimation
        for i in range(self.n_features):
            for j in range(self.n_features):
                cov_matrix[i][j] /= (self.n_samples - 1)
        
        # Add small regularization term to diagonal to ensure invertibility
        for i in range(self.n_features):
            cov_matrix[i][i] += self.regularization
        
        return cov_matrix
    
    def _matrix_determinant(self, matrix: List[List[float]]) -> float:
        """
        Calculate the determinant of a matrix using cofactor expansion.
        Only implemented for 2x2 and 3x3 matrices for simplicity.
        
        Args:
            matrix: A square matrix represented as a list of lists.
            
        Returns:
            The determinant of the matrix.
            
        Raises:
            NotImplementedError: If matrix dimension is greater than 3.
        """
        n: int = len(matrix)
        
        if n == 1:
            return matrix[0][0]
        elif n == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        elif n == 3:
            det: float = 0
            for j in range(3):
                det += matrix[0][j] * (matrix[1][(j+1)%3] * matrix[2][(j+2)%3] - 
                                       matrix[1][(j+2)%3] * matrix[2][(j+1)%3])
            return det
        else:
            raise NotImplementedError("Determinant calculation is only implemented for matrices up to 3x3")
    
    def _matrix_minor(self, matrix: List[List[float]], i: int, j: int) -> List[List[float]]:
        """
        Calculate the minor of matrix by removing row i and column j.
        
        Args:
            matrix: A square matrix represented as a list of lists.
            i: Row index to remove.
            j: Column index to remove.
            
        Returns:
            A new matrix with row i and column j removed.
        """
        return [[matrix[row][col] for col in range(len(matrix[0])) if col != j]
                for row in range(len(matrix)) if row != i]
    
    def _matrix_adjoint(self, matrix: List[List[float]]) -> List[List[float]]:
        """
        Calculate the adjoint (adjugate) of a matrix.
        
        Args:
            matrix: A square matrix represented as a list of lists.
            
        Returns:
            The adjoint matrix.
        """
        n: int = len(matrix)
        adjoint: List[List[float]] = [[0.0 for _ in range(n)] for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                minor = self._matrix_minor(matrix, i, j)
                sign: int = (-1) ** (i + j)
                adjoint[j][i] = sign * self._matrix_determinant(minor)  # Note the transpose: [j][i]
        
        return adjoint
    
    def _invert_matrix(self, matrix: List[List[float]]) -> List[List[float]]:
        """
        Calculate the inverse of a matrix.
        
        Args:
            matrix: A square matrix represented as a list of lists.
            
        Returns:
            The inverse of the matrix.
            
        Raises:
            ValueError: If the matrix is singular (determinant is zero).
        """
        det: float = self._matrix_determinant(matrix)
        
        if abs(det) < 1e-10:
            raise ValueError("Matrix is singular, cannot calculate inverse")
        
        adjoint = self._matrix_adjoint(matrix)
        inverse: List[List[float]] = [[adjoint[i][j] / det for j in range(len(matrix))] for i in range(len(matrix))]
        
        return inverse
    
    def _matrix_vector_multiply(self, matrix: List[List[float]], vector: List[float]) -> List[float]:
        """
        Multiply a matrix by a vector.
        
        Args:
            matrix: A matrix represented as a list of lists.
            vector: A vector represented as a list.
            
        Returns:
            The result of matrix-vector multiplication as a list.
        """
        result: List[float] = [0.0] * len(matrix)
        
        for i in range(len(matrix)):
            for j in range(len(vector)):
                result[i] += matrix[i][j] * vector[j]
                
        return result
    
    def _vector_vector_multiply(self, vector1: List[float], vector2: List[float]) -> float:
        """
        Calculate the dot product of two vectors.
        
        Args:
            vector1: First vector as a list.
            vector2: Second vector as a list.
            
        Returns:
            The dot product as a float.
        """
        if len(vector1) != len(vector2):
            raise ValueError("Vectors must have the same length")
            
        result: float = 0.0
        for i in range(len(vector1)):
            result += vector1[i] * vector2[i]
            
        return result
    
    def compute(self,data: List[List[float]], point: List[float]) -> float:
        """
        Calculate the Mahalanobis distance between the given point and the dataset.
        
        Args:
            point: A list representing a single data point.
            
        Returns:
            The Mahalanobis distance as a float.
            
        Raises:
            ValueError: If the point does not have the same number of features as the dataset.
        """
        self.data=data
        
        self.n_samples = len(data)
        
        self.n_features = len(data[0])
        # Check if all points have the same dimension
        for point in data:
            if len(point) != self.n_features:
                raise ValueError("All points must have the same number of features")
        
        # Calculate mean vector
        self.mean = self._calculate_mean()
        
        # Calculate covariance matrix
        self.covariance_matrix = self._calculate_covariance_matrix()
        
        # Calculate inverse of covariance matrix
        self.inv_covariance_matrix = self._invert_matrix(self.covariance_matrix)
        
        if len(point) != self.n_features:
            raise ValueError(f"Point must have {self.n_features} features, got {len(point)}")
        
        # Calculate point - mean
        diff: List[float] = [point[i] - self.mean[i] for i in range(self.n_features)]
        
        # Calculate (point - mean)^T * inv_covariance_matrix * (point - mean)
        temp: List[float] = self._matrix_vector_multiply(self.inv_covariance_matrix, diff)
        mahalanobis_squared: float = self._vector_vector_multiply(diff, temp)
        
        # Return square root of the result
        return math.sqrt(mahalanobis_squared)
        
    def example(self):
      data = [
       [1.0, 5.0, 3.0],
       [2.0, 4.0, 1.0],
       [3.0, 6.0, 2.0],
       [4.0, 3.0, 4.0],
       [2.5, 5.5, 2.5],
       [3.5, 4.5, 3.5]
      ]
      point = [2.5, 4.5, 2.0]
      distance = self.compute(data,point)
      print(f"Mahalanobis distance: {distance}")


class MahalanobisTaguchi(matrixDistance):
	
    def __init__(self)-> None:
        """
        Initialize the MahalanobisTaguchi class with a reference group.
        
        :param reference_group: A list of lists where each inner list is a data point in the reference group.
        """
        super().__init__()
        self.type='vec_float'

    def calculate_mean_vector(self):
        """
        Calculate the mean vector of the reference group.

        :return: A list representing the mean vector.
        """
        num_points = len(self.reference_group)
        num_dimensions = len(self.reference_group[0])

        mean_vector = [0] * num_dimensions

        for point in self.reference_group:
            for i in range(num_dimensions):
                mean_vector[i] += point[i]

        mean_vector = [x / num_points for x in mean_vector]
        return mean_vector

    def compute(self,reference_group :list[list], data_point)-> float:
        """
        Calculate the Mahalanobis-Taguchi distance for a given data point.

        :param data_point: A list representing the data point to be evaluated.
        :return: The Mahalanobis-Taguchi distance as a float.
        """
        self.reference_group = reference_group
        self.mean_vector = self.calculate_mean_vector()
        self.covariance_matrix = Matrix.covariance(reference_group)
        self.inverse_covariance_matrix = Matrix.invert(self.covariance_matrix)
        
        diff_vector = [data_point[i] - self.mean_vector[i] for i in range(len(self.mean_vector))]
        
        # Matrix multiplication with the inverse covariance matrix
        temp_vector = [0] * len(diff_vector)
        for i in range(len(diff_vector)):
            for j in range(len(diff_vector)):
                temp_vector[i] += diff_vector[j] * self.inverse_covariance_matrix[j][i]

        # Final dot product to get the Mahalanobis-Taguchi distance
        distance_squared = sum(temp_vector[i] * diff_vector[i] for i in range(len(diff_vector)))
        return distance_squared ** 0.5
        
    def example(self):
        # Example reference group data (2D array where each row is a data point)
        reference_group = [
    [1.0, 5.0, 3.0],
    [2.0, 4.0, 1.0],
    [3.0, 6.0, 2.0],
    [4.0, 3.0, 4.0],
    [2.5, 5.5, 2.5],
    [3.5, 4.5, 3.5]
]
        # Example test data (data point to be evaluated against the reference group)
        test_data = [1.3, 2.3, 3.3]

        # Calculate the Mahalanobis-Taguchi distance for the test data
        distance = self.compute(reference_group,test_data)

        # Print the result
        print(f"Mahalanobis-Taguchi distance for the test data {test_data} is: {distance}")

from typing import List, Tuple
import math

class MatrixSpectral(matrixDistance):
	
    def __init__(self)-> None:
        """
        Initialize the MahalanobisTaguchi class with a reference group.
        
        :param reference_group: A list of lists where each inner list is a data point in the reference group.
        """
        super().__init__()

        self.reset()

    def reset(self) -> None:
        """
        Reset all computed values
        """
        self.spectrum1: List[float] = []
        self.spectrum2: List[float] = []
        self.distance: float = 0.0

    def compute_spectrum(self, matrix: List[List[float]], max_iter: int = 100, tol: float = 1e-6) -> List[float]:
        """
        Compute eigenvalues using power iteration with deflation
        
        Args:
            matrix: Input matrix
            max_iter: Maximum iterations for convergence
            tol: Convergence tolerance
            
        Returns:
            List[float]: Sorted eigenvalues
        """
        n = len(matrix)
        spectrum = []
        working_matrix = [row[:] for row in matrix]  # Copy matrix

        for _ in range(n):
            # Initialize random vector
            vector = [1.0] * n
            vector, _ = Vector.normalize(vector)
            
            # Power iteration
            eigenvalue = 0.0
            for _ in range(max_iter):
                # Compute new vector
                new_vector = Matrix.multiply_vector(working_matrix, vector)
                new_vector, new_norm = Vector.normalize(new_vector)
                
                # Update eigenvalue estimate
                new_eigenvalue = sum(v1 * v2 for v1, v2 in zip(vector, Matrix.multiply_vector(working_matrix, vector)))
                
                # Check convergence
                if abs(new_eigenvalue - eigenvalue) < tol:
                    eigenvalue = new_eigenvalue
                    break
                    
                vector = new_vector
                eigenvalue = new_eigenvalue
            
            spectrum.append(eigenvalue)
            
            # Deflation
            for i in range(n):
                for j in range(n):
                    working_matrix[i][j] -= eigenvalue * vector[i] * vector[j]

        return sorted(spectrum, reverse=True)

    def compute(self, matrix1: List[List[float]], matrix2: List[List[float]]) -> float:
        """
        Compute spectral distance between two matrices
        
        Args:
            matrix1: First matrix
            matrix2: Second matrix
            
        Returns:
            float: Spectral distance between matrices
            
        Raises:
            ValueError: If matrices have different dimensions
        """
        # Validate matrices
        n1, n2 = len(matrix1), len(matrix2)
        if n1 != n2 or any(len(row) != n1 for row in matrix1) or any(len(row) != n2 for row in matrix2):
            raise ValueError("Matrices must be square and have the same dimensions")

        # Reset previous computations
        self.reset()

        # Compute spectra
        self.spectrum1 = self.compute_spectrum(matrix1)
        self.spectrum2 = self.compute_spectrum(matrix2)

        # Compute Euclidean distance between spectra
        #self.distance = math.sqrt(sum((s1 - s2) ** 2 for s1, s2 in zip(self.spectrum1, self.spectrum2)))
        self.distance = Euclidean().compute(self.spectrum1, self.spectrum2)
        
        return self.distance

    def get_spectra(self) -> Tuple[List[float], List[float]]:
        """
        Get computed spectra of both matrices
        
        Returns:
            Tuple[List[float], List[float]]: Spectra of both matrices
        """
        return self.spectrum1, self.spectrum2

from typing import List, Tuple
import math

class NormalizedSpectral(matrixDistance):
	
    def __init__(self)-> None:
        """
        Initialize the MahalanobisTaguchi class with a reference group.
        
        :param reference_group: A list of lists where each inner list is a data point in the reference group.
        """
        super().__init__()

        self.reset()

    def reset(self) -> None:
        """
        Reset all computed values
        """
        self.spectrum1: List[float] = []
        self.spectrum2: List[float] = []
        self.normalized_spectrum1: List[float] = []
        self.normalized_spectrum2: List[float] = []
        self.distance: float = 0.0

    def _frobenius_norm(self, matrix: List[List[float]]) -> float:
        """
        Compute the Frobenius norm of a matrix
        
        Args:
            matrix: Input matrix
            
        Returns:
            float: Frobenius norm
        """
        return math.sqrt(sum(sum(x*x for x in row) for row in matrix))

    def compute_spectrum(self, matrix: List[List[float]], max_iter: int = 100, tol: float = 1e-6) -> List[float]:
        """
        Compute eigenvalues using power iteration with deflation
        
        Args:
            matrix: Input matrix
            max_iter: Maximum iterations for convergence
            tol: Convergence tolerance
            
        Returns:
            List[float]: Sorted eigenvalues
        """
        n = len(matrix)
        spectrum = []
        working_matrix = [row[:] for row in matrix]

        for _ in range(n):
            # Initialize random vector
            vector = [1.0] * n
            vector, _ = Vector.normalize(vector)
            
            # Power iteration
            eigenvalue = 0.0
            for _ in range(max_iter):
                new_vector = Matrix.multiply_vector(working_matrix, vector)
                new_vector, new_norm = Vector.normalize(new_vector)
                
                # Rayleigh quotient for eigenvalue estimation
                new_eigenvalue = sum(v1 * v2 for v1, v2 in zip(vector, Matrix.multiply_vector(working_matrix, vector)))
                
                if abs(new_eigenvalue - eigenvalue) < tol:
                    eigenvalue = new_eigenvalue
                    break
                    
                vector = new_vector
                eigenvalue = new_eigenvalue
            
            spectrum.append(eigenvalue)
            
            # Deflation
            for i in range(n):
                for j in range(n):
                    working_matrix[i][j] -= eigenvalue * vector[i] * vector[j]

        return sorted(spectrum, reverse=True)

    def normalize_spectrum(self, spectrum: List[float], norm_factor: float) -> List[float]:
        """
        Normalize spectrum by dividing by norm factor
        
        Args:
            spectrum: List of eigenvalues
            norm_factor: Normalization factor
            
        Returns:
            List[float]: Normalized spectrum
        """
        if norm_factor < 1e-10:  # Avoid division by zero
            return spectrum
        return [val/norm_factor for val in spectrum]

    def compute(self, matrix1: List[List[float]], matrix2: List[List[float]], 
                        normalization: str = 'frobenius') -> float:
        """
        Compute normalized spectral distance between two matrices
        
        Args:
            matrix1: First matrix
            matrix2: Second matrix
            normalization: Normalization method ('frobenius' or 'spectral')
            
        Returns:
            float: Normalized spectral distance
            
        Raises:
            ValueError: If matrices have different dimensions or invalid normalization method
        """
        # Validate matrices
        n1, n2 = len(matrix1), len(matrix2)
        if n1 != n2 or any(len(row) != n1 for row in matrix1) or any(len(row) != n2 for row in matrix2):
            raise ValueError("Matrices must be square and have the same dimensions")
            
        if normalization not in ['frobenius', 'spectral']:
            raise ValueError("Normalization must be either 'frobenius' or 'spectral'")

        # Reset previous computations
        self.reset()

        # Compute spectra
        self.spectrum1 = self.compute_spectrum(matrix1)
        self.spectrum2 = self.compute_spectrum(matrix2)

        # Compute normalization factors
        if normalization == 'frobenius':
            norm1 = self._frobenius_norm(matrix1)
            norm2 = self._frobenius_norm(matrix2)
        else:  # spectral normalization
            norm1 = max(abs(val) for val in self.spectrum1)
            norm2 = max(abs(val) for val in self.spectrum2)

        # Normalize spectra
        self.normalized_spectrum1 = self.normalize_spectrum(self.spectrum1, norm1)
        self.normalized_spectrum2 = self.normalize_spectrum(self.spectrum2, norm2)

        # Compute normalized distance
        self.distance = math.sqrt(sum((s1 - s2) ** 2 
                                for s1, s2 in zip(self.normalized_spectrum1, 
                                                 self.normalized_spectrum2)))
        
        return self.distance

    def get_spectra(self) -> Tuple[List[float], List[float]]:
        """
        Get original computed spectra
        
        Returns:
            Tuple[List[float], List[float]]: Original spectra of both matrices
        """
        return self.spectrum1, self.spectrum2

    def get_normalized_spectra(self) -> Tuple[List[float], List[float]]:
        """
        Get normalized spectra
        
        Returns:
            Tuple[List[float], List[float]]: Normalized spectra of both matrices
        """
        return self.normalized_spectrum1, self.normalized_spectrum2

from typing import List, Tuple, Optional
from dataclasses import dataclass
import math


class SpectralResistanceDistance(matrixDistance):
    """
    A class to compute the spectral resistance distance between two matrices.
    
    The spectral resistance distance is defined as the Euclidean norm of the
    difference between the pseudo-inverses of the Laplacian matrices.
    """
    
    def __init__(self, tolerance: float = 1e-10):
        """
        Initialize the SpectralResistanceDistance calculator.
        
        Args:
            tolerance: Numerical tolerance for singular value decomposition
        """
        super().__init__()
        
        self.tolerance = tolerance

    def _compute_laplacian(self, adjacency: Matrix) -> Matrix:
        """
        Compute the Laplacian matrix from an adjacency matrix.
        L = D - A where D is the degree matrix and A is the adjacency matrix.
        
        Args:
            adjacency: Adjacency matrix of the graph
            
        Returns:
            The Laplacian matrix
        """
        n = adjacency.rows
        # Compute degree matrix (diagonal matrix of row sums)
        degrees = [sum(adjacency.data[i]) for i in range(n)]
        
        # Initialize Laplacian matrix
        laplacian = Matrix.zeros(n, n)
        
        # Fill Laplacian matrix
        for i in range(n):
            for j in range(n):
                if i == j:
                    laplacian.data[i][j] = degrees[i]
                else:
                    laplacian.data[i][j] = -adjacency.data[i][j]
        
        return laplacian

    def _svd(self, matrix: Matrix) -> Tuple[Matrix, List[float], Matrix]:
        """
        Compute the Singular Value Decomposition (SVD) of a matrix using power iteration.
        
        Args:
            matrix: Input matrix for SVD
            
        Returns:
            Tuple of (U, singular values, V^T)
        """
        max_iter = 100
        n = matrix.rows
        m = matrix.cols
        
        # Initialize matrices
        U = Matrix.zeros(n, min(n, m))
        V = Matrix.zeros(m, min(n, m))
        singular_values: List[float] = []
        
        # Compute SVD using power iteration
        remaining = Matrix(n, m, [[x for x in row] for row in matrix.data])
        
        for k in range(min(n, m)):
            # Initialize random vector
            v = [1.0 if i == 0 else 0.0 for i in range(m)]
            
            # Power iteration
            for _ in range(max_iter):
                # Compute matrix-vector product
                u = [sum(remaining.data[i][j] * v[j] for j in range(m)) 
                     for i in range(n)]
                
                # Normalize u
                norm_u = math.sqrt(sum(x * x for x in u))
                if norm_u > self.tolerance:
                    u = [x / norm_u for x in u]
                
                # Compute matrix^T-vector product
                v_new = [sum(remaining.data[i][j] * u[i] for i in range(n)) 
                        for j in range(m)]
                
                # Normalize v
                norm_v = math.sqrt(sum(x * x for x in v_new))
                if norm_v > self.tolerance:
                    v_new = [x / norm_v for x in v_new]
                
                # Check convergence
                if all(abs(v_new[i] - v[i]) < self.tolerance for i in range(m)):
                    break
                v = v_new
            
            # Compute singular value
            sigma = sum(u[i] * sum(remaining.data[i][j] * v[j] 
                                 for j in range(m)) for i in range(n))
            
            if abs(sigma) > self.tolerance:
                singular_values.append(sigma)
                
                # Update U and V matrices
                for i in range(n):
                    U.data[i][k] = u[i]
                for i in range(m):
                    V.data[i][k] = v[i]
                
                # Deflate the matrix
                for i in range(n):
                    for j in range(m):
                        remaining.data[i][j] -= sigma * u[i] * v[j]
        
        return U, singular_values, V

    def _pseudo_inverse(self, matrix: Matrix) -> Matrix:
        """
        Compute the Moore-Penrose pseudo-inverse of a matrix using SVD.
        
        Args:
            matrix: Input matrix
            
        Returns:
            Pseudo-inverse of the input matrix
        """
        # Compute SVD
        U, s, V = self._svd(matrix)
        
        # Compute pseudo-inverse of singular values
        s_inv = [1/x if abs(x) > self.tolerance else 0.0 for x in s]
        
        # Compute pseudo-inverse
        result = Matrix.zeros(matrix.cols, matrix.rows)
        for i in range(result.rows):
            for j in range(result.cols):
                result.data[i][j] = sum(V.data[i][k] * s_inv[k] * U.data[j][k] 
                                      for k in range(len(s)))
        
        return result

    def compute(self, matrix1: Matrix, matrix2: Matrix) -> float:
        """
        Compute the spectral resistance distance between two matrices.
        
        Args:
            matrix1: First adjacency matrix
            matrix2: Second adjacency matrix
            
        Returns:
            The spectral resistance distance between the two matrices
            
        Raises:
            ValueError: If matrices have different dimensions
        """
        #if (matrix1.rows != matrix1.cols or 
        #    matrix2.rows != matrix2.cols or 
        #    matrix1.rows != matrix2.rows):
        #   raise ValueError("Matrices must be square and of same dimension")
        
        # Compute Laplacian matrices
        laplacian1 = self._compute_laplacian(matrix1)
        laplacian2 = self._compute_laplacian(matrix2)
        
        # Compute pseudo-inverses
        pinv1 = self._pseudo_inverse(laplacian1)
        pinv2 = self._pseudo_inverse(laplacian2)
        
        # Compute Frobenius norm of difference
        diff_norm = 0.0
        for i in range(pinv1.rows):
            for j in range(pinv1.cols):
                diff = pinv1.data[i][j] - pinv2.data[i][j]
                diff_norm += diff * diff
                
        return math.sqrt(diff_norm)

      
from typing import List, Tuple, Optional
import math
from copy import deepcopy

class PureDiffusion(matrixDistance):
    """
    A class to compute the diffusion distance between two matrices using pure Python.
    Implements matrix operations and eigenvalue decomposition without external libraries.
    
    Attributes:
        time_param (float): Time parameter for the diffusion process
        n_eigenvalues (int): Number of eigenvalues to use in computation
        epsilon (float): Small value for numerical stability
        max_iterations (int): Maximum iterations for power method
        tolerance (float): Convergence tolerance for eigenvalue computation
    """
    
    def __init__(self, 
                 time_param: float = 1.0, 
                 n_eigenvalues: Optional[int] = None,
                 epsilon: float = 1e-10,
                 max_iterations: int = 1000,
                 tolerance: float = 1e-6) -> None:
        """
        Initialize the DiffusionDistance calculator.
        
        Args:
            time_param: Time parameter for diffusion process
            n_eigenvalues: Number of eigenvalues to use
            epsilon: Numerical stability parameter
            max_iterations: Maximum iterations for eigenvalue computation
            tolerance: Convergence tolerance
        """
        super().__init__()
        
        self.time_param = time_param
        self.n_eigenvalues = n_eigenvalues
        self.epsilon = epsilon
        self.max_iterations = max_iterations
        self.tolerance = tolerance
        
    def _power_iteration(self, 
                        matrix: List[List[float]], 
                        num_vectors: int) -> Tuple[List[float], List[List[float]]]:
        """
        Compute eigenvalues and eigenvectors using power iteration method.
        
        Args:
            matrix: Input matrix
            num_vectors: Number of eigenvectors to compute
            
        Returns:
            Tuple[List[float], List[List[float]]]: Eigenvalues and eigenvectors
        """
        n = len(matrix)
        eigenvalues = []
        eigenvectors = []
        
        # Deep copy of matrix for deflation
        working_matrix = deepcopy(matrix)
        
        for _ in range(min(num_vectors, n)):
            # Initialize random vector
            vector = [1.0 / math.sqrt(n) for _ in range(n)]
            
            # Power iteration
            for _ in range(self.max_iterations):
                new_vector = [0.0 for _ in range(n)]
                
                # Matrix-vector multiplication
                for i in range(n):
                    for j in range(n):
                        new_vector[i] += working_matrix[i][j] * vector[j]
                
                # Normalize
                norm = math.sqrt(sum(x * x for x in new_vector))
                if norm < self.epsilon:
                    break
                
                vector = [x / norm for x in new_vector]
                
                # Compute Rayleigh quotient (eigenvalue estimate)
                eigenvalue = sum(working_matrix[i][j] * vector[i] * vector[j] 
                               for i in range(n) for j in range(n))
                
            eigenvalues.append(eigenvalue)
            eigenvectors.append(vector)
            
            # Matrix deflation
            for i in range(n):
                for j in range(n):
                    working_matrix[i][j] -= eigenvalue * vector[i] * vector[j]
        
        return eigenvalues, Matrix.transpose(eigenvectors)
    
    def compute(self, 
                        matrix1: List[List[float]], 
                        matrix2: List[List[float]],
                        normalized: bool = False) -> float:
        """
        Compute diffusion distance between two matrices.
        
        Args:
            matrix1: First input matrix
            matrix2: Second input matrix
            normalized: Whether to normalize the distance
            
        Returns:
            float: Diffusion distance between matrices
            
        Raises:
            ValueError: If matrices have different dimensions
        """
        if len(matrix1) != len(matrix2) or len(matrix1[0]) != len(matrix2[0]):
            raise ValueError("Matrices must have the same dimensions")
            
        n = len(matrix1)
        n_eigvals = self.n_eigenvalues if self.n_eigenvalues else n
        
        # Compute eigendecompositions
        evals1, evecs1 = self._power_iteration(Matrix.normalize(matrix1), n_eigvals)
        evals2, evecs2 = self._power_iteration(Matrix.normalize(matrix2), n_eigvals)
        
        # Compute diffusion matrices
        diff1 = [[0.0 for _ in range(n)] for _ in range(n)]
        diff2 = [[0.0 for _ in range(n)] for _ in range(n)]
        
        for k in range(len(evals1)):
            scale1 = math.exp(-self.time_param * (1 - evals1[k]))
            scale2 = math.exp(-self.time_param * (1 - evals2[k]))
            
            for i in range(n):
                for j in range(n):
                    diff1[i][j] += scale1 * evecs1[i][k] * evecs1[j][k]
                    diff2[i][j] += scale2 * evecs2[i][k] * evecs2[j][k]
        
        # Compute Frobenius norm of difference
        distance = 0.0
        for i in range(n):
            for j in range(n):
                diff = diff1[i][j] - diff2[i][j]
                distance += diff * diff
        distance = math.sqrt(distance)
        
        if normalized:
            # Compute norms of individual matrices
            norm1 = math.sqrt(sum(diff1[i][j] * diff1[i][j] 
                                for i in range(n) for j in range(n)))
            norm2 = math.sqrt(sum(diff2[i][j] * diff2[i][j] 
                                for i in range(n) for j in range(n)))
            distance = distance / (norm1 + norm2 + self.epsilon)
            
        return distance
    
    def get_diffusion_coordinates(self, 
                                matrix: List[List[float]], 
                                dim: int = 2) -> List[List[float]]:
        """
        Compute diffusion coordinates for dimensionality reduction.
        
        Args:
            matrix: Input matrix
            dim: Number of dimensions for the embedding
            
        Returns:
            List[List[float]]: Diffusion coordinates
            
        Raises:
            ValueError: If dim is larger than matrix dimension
        """
        if dim > len(matrix):
            raise ValueError(f"Requested dimensions {dim} larger than matrix dimension {len(matrix)}")
            
        eigenvalues, eigenvectors = self._power_iteration(Matrix.normalize(matrix), dim)
        n = len(matrix)
        coordinates = [[0.0 for _ in range(dim)] for _ in range(n)]
        
        for i in range(n):
            for j in range(dim):
                coordinates[i][j] = eigenvectors[i][j] * math.exp(
                    -self.time_param * (1 - eigenvalues[j]))
                
        return coordinates
from typing import List, Tuple, Optional
import math
from copy import deepcopy

class RandomWalk(matrixDistance):
    """
    A class to compute the random walk distance between two matrices.
    The random walk distance measures the difference between transition probabilities
    of random walks on the graphs represented by the matrices.
    
    Attributes:
        alpha (float): Damping factor for random walk (between 0 and 1)
        max_iter (int): Maximum number of iterations for convergence
        tolerance (float): Convergence tolerance for matrix operations
        epsilon (float): Small value for numerical stability
    """
    
    def __init__(self, 
                 alpha: float = 0.85,
                 max_iter: int = 100,
                 tolerance: float = 1e-6,
                 epsilon: float = 1e-10) -> None:
        """
        Initialize the RandomWalkDistance calculator.
        
        Args:
            alpha: Damping factor (default: 0.85)
            max_iter: Maximum iterations for convergence (default: 100)
            tolerance: Convergence tolerance (default: 1e-6)
            epsilon: Numerical stability parameter (default: 1e-10)
            
        Raises:
            ValueError: If alpha is not between 0 and 1
        """
        super().__init__()
        
        if not 0 <= alpha <= 1:
            raise ValueError("Alpha must be between 0 and 1")
            
        self.alpha = alpha
        self.max_iter = max_iter
        self.tolerance = tolerance
        self.epsilon = epsilon
    
    
    def _normalize_matrix(self, matrix: List[List[float]]) -> List[List[float]]:
        """
        Normalize matrix to create transition probability matrix.
        
        Args:
            matrix: Input adjacency matrix
            
        Returns:
            List[List[float]]: Normalized transition matrix
        """
        n = len(matrix)
        normalized = [[0.0 for _ in range(n)] for _ in range(n)]
        
        # Compute out-degrees
        for i in range(n):
            out_degree = sum(max(0.0, matrix[i][j]) for j in range(n))
            # Handle isolated nodes
            if out_degree > self.epsilon:
                for j in range(n):
                    normalized[i][j] = max(0.0, matrix[i][j]) / out_degree
            else:
                # Uniform distribution for isolated nodes
                for j in range(n):
                    normalized[i][j] = 1.0 / n
                    
        return normalized
    
    def _compute_stationary_distribution(self, 
                                       transition_matrix: List[List[float]]
                                       ) -> List[float]:
        """
        Compute the stationary distribution of a Markov chain.
        
        Args:
            transition_matrix: Normalized transition matrix
            
        Returns:
            List[float]: Stationary distribution vector
        """
        n = len(transition_matrix)
        
        # Initialize uniform distribution
        distribution = [1.0 / n for _ in range(n)]
        
        for _ in range(self.max_iter):
            new_distribution = [0.0 for _ in range(n)]
            
            # Power iteration
            for i in range(n):
                for j in range(n):
                    new_distribution[i] += distribution[j] * transition_matrix[j][i]
                    
            # Check convergence
            max_diff = max(abs(new_distribution[i] - distribution[i]) 
                         for i in range(n))
            
            distribution = new_distribution
            
            if max_diff < self.tolerance:
                break
                
        return distribution
    
    def compute(self, 
                        matrix1: List[List[float]], 
                        matrix2: List[List[float]],
                        normalized: bool = False) -> float:
        """
        Compute random walk distance between two matrices.
        
        Args:
            matrix1: First input matrix
            matrix2: Second input matrix
            normalized: Whether to normalize the distance
            
        Returns:
            float: Random walk distance between matrices
            
        Raises:
            ValueError: If matrices have different dimensions
        """
        if len(matrix1) != len(matrix2) or len(matrix1[0]) != len(matrix2[0]):
            raise ValueError("Matrices must have the same dimensions")
        
        n = len(matrix1)
        
        # Normalize matrices to get transition probabilities
        P1 = self._normalize_matrix(matrix1)
        P2 = self._normalize_matrix(matrix2)
        
        # Compute stationary distributions
        pi1 = self._compute_stationary_distribution(P1)
        pi2 = self._compute_stationary_distribution(P2)
        
        # Compute fundamental matrices
        # Z = (I - αP)^(-1)
        Z1 = [[0.0 for _ in range(n)] for _ in range(n)]
        Z2 = [[0.0 for _ in range(n)] for _ in range(n)]
        
        # Initialize with identity matrix
        for i in range(n):
            for j in range(n):
                Z1[i][j] = 1.0 if i == j else 0.0
                Z2[i][j] = 1.0 if i == j else 0.0
        
        # Compute fundamental matrices using power series
        for _ in range(self.max_iter):
            Z1_new = Matrix.multiply(P1, Z1)
            Z2_new = Matrix.multiply(P2, Z2)
            
            # Scale by alpha
            for i in range(n):
                for j in range(n):
                    Z1[i][j] = (1 - self.alpha) * (1.0 if i == j else 0.0) + self.alpha * Z1_new[i][j]
                    Z2[i][j] = (1 - self.alpha) * (1.0 if i == j else 0.0) + self.alpha * Z2_new[i][j]
        
        # Compute distance
        distance = 0.0
        for i in range(n):
            for j in range(n):
                diff = Z1[i][j] - Z2[i][j]
                # Weight by stationary distributions
                distance += abs(diff) * pi1[i] * pi2[j]
        
        if normalized:
            # Compute individual norms
            norm1 = sum(abs(Z1[i][j]) * pi1[i] * pi1[j] 
                       for i in range(n) for j in range(n))
            norm2 = sum(abs(Z2[i][j]) * pi2[i] * pi2[j] 
                       for i in range(n) for j in range(n))
            distance = distance / (math.sqrt(norm1 * norm2) + self.epsilon)
        
        return distance
    
    def get_node_distances(self, 
                          matrix: List[List[float]]
                          ) -> List[List[float]]:
        """
        Compute pairwise random walk distances between nodes.
        
        Args:
            matrix: Input adjacency matrix
            
        Returns:
            List[List[float]]: Matrix of pairwise node distances
        """
        n = len(matrix)
        P = self._normalize_matrix(matrix)
        pi = self._compute_stationary_distribution(P)
        
        # Initialize distance matrix
        distances = [[0.0 for _ in range(n)] for _ in range(n)]
        
        # Compute fundamental matrix
        Z = [[0.0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            Z[i][i] = 1.0
            
        for _ in range(self.max_iter):
            Z_new = Matrix.multiply(P, Z)
            for i in range(n):
                for j in range(n):
                    Z[i][j] = (1 - self.alpha) * (1.0 if i == j else 0.0) + self.alpha * Z_new[i][j]
        
        # Compute pairwise distances
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    distances[i][j] += abs(Z[i][k] - Z[j][k]) * pi[k]
                    
        return distances
        
from typing import List, Union
from math import exp

class HeatKernel(matrixDistance):
    """
    A class to compute the Heat Kernel distance between two matrices.
    The Heat Kernel distance is a measure that captures both the direct and indirect
    relationships between matrices by considering paths of all lengths.
    
    The distance is calculated as: d(A,B) = ||exp(-t*A) - exp(-t*B)||
    where:
    - t is the time parameter (controls the scale of the diffusion)
    - exp is the matrix exponential
    - ||.|| is the Frobenius norm
    """

    def __init__(self, time_parameter: float = 1.0):
        """
        Initialize the HeatKernelDistance calculator.
        
        Args:
            time_parameter (float): The time parameter t for the heat kernel.
                                  Controls how far the heat diffusion spreads.
                                  Larger values give more weight to indirect connections.
        """
        super().__init__()
        
        self.time_parameter = time_parameter

    def compute(self, A: List[List[float]], B: List[List[float]]) -> float:
        """
        Compute the Heat Kernel distance between two matrices.
        
        Args:
            A (List[List[float]]): First matrix
            B (List[List[float]]): Second matrix
            
        Returns:
            float: Heat Kernel distance between A and B
        """
        exp_A = Matrix(0,0).exp(A,self.time_parameter)
        exp_B = Matrix(0,0).exp(B,self.time_parameter)
        diff = Matrix.subtraction(exp_A, exp_B)
        return Matrix.frobenius_norm(diff)

from typing import List, Tuple, Optional
from math import sqrt

class GraphEditMatrix(matrixDistance):
    """
    Implements Graph Edit Distance (GED) calculation between two matrices.
    Graph Edit Distance measures the minimum cost of transforming one graph into another
    through edit operations like node/edge insertion, deletion, and substitution.
    """
    
    def __init__(self, node_cost: float = 1.0, edge_cost: float = 1.0):
        """
        Initialize the Graph Edit Distance calculator with configurable costs.
        
        Args:
            node_cost (float): Cost of node-level edit operations. Default is 1.0.
            edge_cost (float): Cost of edge-level edit operations. Default is 1.0.
        """
        super().__init__()
        
        self.node_cost = node_cost
        self.edge_cost = edge_cost
    
    def compute(self, matrix1: List[List[float]], matrix2: List[List[float]]) -> float:
        """
        Calculate the Graph Edit Distance between two adjacency matrices.
        
        Args:
            matrix1 (List[List[float]]): First graph's adjacency matrix
            matrix2 (List[List[float]]): Second graph's adjacency matrix
        
        Returns:
            float: Computed edit distance between the two graphs
        
        Raises:
            ValueError: If input matrices are invalid (non-square or different sizes)
        """
        # Validate input matrices
        if not self._validate_matrices(matrix1, matrix2):
            raise ValueError("Input matrices must be square and of equal dimensions")
        
        n1, n2 = len(matrix1), len(matrix2)
        total_cost: float = 0.0
        
        # Node edit operations cost
        total_cost += abs(n1 - n2) * self.node_cost
        
        # Edge edit operations cost
        min_size = min(n1, n2)
        for i in range(min_size):
            for j in range(i + 1, min_size):  # Upper triangular matrix
                # Compute edge difference
                edge_diff = abs(matrix1[i][j] - matrix2[i][j])
                total_cost += edge_diff * self.edge_cost
        
        return total_cost
    
    def similarity_score(self, matrix1: List[List[float]], matrix2: List[List[float]]) -> float:
        """
        Compute a normalized similarity score between two graph matrices.
        
        Args:
            matrix1 (List[List[float]]): First graph's adjacency matrix
            matrix2 (List[List[float]]): Second graph's adjacency matrix
        
        Returns:
            float: Similarity score between 0 and 1 (1 = identical, 0 = maximally different)
        """
        distance = self.compute(matrix1, matrix2)
        max_distance = self._calculate_max_possible_distance(matrix1, matrix2)
        
        # Normalize the distance
        return 1.0 - (distance / max_distance) if max_distance > 0 else 1.0
    
    def _validate_matrices(self, matrix1: List[List[float]], matrix2: List[List[float]]) -> bool:
        """
        Validate that input matrices are square and have consistent dimensions.
        
        Args:
            matrix1 (List[List[float]]): First matrix to validate
            matrix2 (List[List[float]]): Second matrix to validate
        
        Returns:
            bool: True if matrices are valid, False otherwise
        """
        return (
            all(len(row) == len(matrix1) for row in matrix1) and
            all(len(row) == len(matrix2) for row in matrix2) and
            len(matrix1) == len(matrix2)
        )
    
    def _calculate_max_possible_distance(self, matrix1: List[List[float]], matrix2: List[List[float]]) -> float:
        """
        Calculate the maximum possible edit distance between two matrices.
        
        Args:
            matrix1 (List[List[float]]): First matrix
            matrix2 (List[List[float]]): Second matrix
        
        Returns:
            float: Maximum possible edit distance
        """
        n1, n2 = len(matrix1), len(matrix2)
        
        # Maximum node edit cost
        max_node_cost = abs(n1 - n2) * self.node_cost
        
        # Maximum edge edit cost (complete graph)
        max_edge_count = (max(n1, n2) * (max(n1, n2) - 1)) // 2
        max_edge_cost = max_edge_count * self.edge_cost
        
        return max_node_cost + max_edge_cost


    
from typing import List, Dict, Set, Tuple, Union
from collections import defaultdict
from hashlib import sha256

class WeisfeilerLehman(matrixDistance):
    """
    A class to compute the Weisfeiler-Lehman distance between two matrices.
    This implementation treats matrices as adjacency matrices of graphs and compares their
    structural similarities using the Weisfeiler-Lehman graph kernel algorithm.
    
    The WL algorithm works by iteratively:
    1. Aggregating neighborhood information for each node
    2. Hashing the aggregated information to create new labels
    3. Comparing the resulting label distributions
    """

    def __init__(self, num_iterations: int = 3):
        """
        Initialize the Weisfeiler-Lehman Distance calculator.
        
        Args:
            num_iterations (int): Number of WL iterations to perform.
                                Higher values capture more global structure.
        """
        super().__init__()
        
        self.num_iterations = num_iterations

    def _matrix_to_adjacency_list(self, matrix: List[List[float]]) -> Dict[int, Set[int]]:
        """
        Convert a matrix to an adjacency list representation.
        
        Args:
            matrix (List[List[float]]): Input matrix
            
        Returns:
            Dict[int, Set[int]]: Adjacency list representation
        """
        adj_list = defaultdict(set)
        n = len(matrix)
        for i in range(n):
            for j in range(n):
                if matrix[i][j] != 0:
                    adj_list[i].add(j)
        return adj_list

    def _hash_label(self, label: str) -> str:
        """
        Create a compressed hash of a label string.
        
        Args:
            label (str): Input label
            
        Returns:
            str: Hashed label
        """
        return sha256(label.encode()).hexdigest()[:8]

    def _get_neighborhood_label(self, 
                              node: int, 
                              adj_list: Dict[int, Set[int]], 
                              labels: Dict[int, str]) -> str:
        """
        Compute the neighborhood label for a node.
        
        Args:
            node (int): Target node
            adj_list (Dict[int, Set[int]]): Adjacency list of the graph
            labels (Dict[int, str]): Current node labels
            
        Returns:
            str: Combined neighborhood label
        """
        neighbor_labels = sorted([labels[neighbor] for neighbor in adj_list[node]])
        return f"{labels[node]}_{'_'.join(neighbor_labels)}"

    def _wl_iteration(self, 
                     adj_list: Dict[int, Set[int]], 
                     labels: Dict[int, str]) -> Dict[int, str]:
        """
        Perform one iteration of the WL algorithm.
        
        Args:
            adj_list (Dict[int, Set[int]]): Adjacency list of the graph
            labels (Dict[int, str]): Current node labels
            
        Returns:
            Dict[int, str]: Updated node labels
        """
        new_labels = {}
        for node in adj_list:
            neighborhood_label = self._get_neighborhood_label(node, adj_list, labels)
            new_labels[node] = self._hash_label(neighborhood_label)
        return new_labels

    def _get_label_distribution(self, labels: Dict[int, str]) -> Dict[str, int]:
        """
        Compute the distribution of labels in the graph.
        
        Args:
            labels (Dict[int, str]): Node labels
            
        Returns:
            Dict[str, int]: Frequency of each label
        """
        distribution = defaultdict(int)
        for label in labels.values():
            distribution[label] += 1
        return distribution

    def _compare_distributions(self, 
                             dist1: Dict[str, int], 
                             dist2: Dict[str, int]) -> float:
        """
        Compare two label distributions using L1 distance.
        
        Args:
            dist1 (Dict[str, int]): First label distribution
            dist2 (Dict[str, int]): Second label distribution
            
        Returns:
            float: Distance between distributions
        """
        all_labels = set(dist1.keys()) | set(dist2.keys())
        return sum(abs(dist1.get(label, 0) - dist2.get(label, 0)) for label in all_labels)

    def compute(self, A: List[List[float]], B: List[List[float]]) -> float:
        """
        Compute the Weisfeiler-Lehman distance between two matrices.
        
        Args:
            A (List[List[float]]): First matrix
            B (List[List[float]]): Second matrix
            
        Returns:
            float: Weisfeiler-Lehman distance between A and B
        """
        # Convert matrices to adjacency lists
        adj_list_A = self._matrix_to_adjacency_list(A)
        adj_list_B = self._matrix_to_adjacency_list(B)
        
        # Initialize labels with degree information
        labels_A = {node: str(len(neighbors)) for node, neighbors in adj_list_A.items()}
        labels_B = {node: str(len(neighbors)) for node, neighbors in adj_list_B.items()}
        
        total_distance = 0.0
        
        # Perform WL iterations
        for _ in range(self.num_iterations):
            # Update labels
            labels_A = self._wl_iteration(adj_list_A, labels_A)
            labels_B = self._wl_iteration(adj_list_B, labels_B)
            
            # Compare label distributions
            dist_A = self._get_label_distribution(labels_A)
            dist_B = self._get_label_distribution(labels_B)
            
            # Accumulate distances
            iteration_distance = self._compare_distributions(dist_A, dist_B)
            total_distance += iteration_distance
        
        # Normalize by number of iterations
        return total_distance / self.num_iterations


from typing import List, Dict, Set, Tuple
from collections import defaultdict
from statistics import mean, median
from math import sqrt

class NetSimile(matrixDistance):
    """
    Implementation of NetSimile distance measure for graphs/networks represented as matrices.
    NetSimile computes the similarity between networks based on local structural features:
    - Node degree
    - Clustering coefficient
    - Average neighbor degree
    - Number of edges in ego network
    - Average clustering of neighbors
    
    For each feature, it computes 7 aggregated values:
    - Median
    - Mean
    - Standard deviation
    - Skewness
    - Kurtosis
    - 90th percentile
    - Number of non-zero values
    """

    def __init__(self):
        """Initialize the NetSimile distance calculator."""
        super().__init__()

    def _matrix_to_adjacency_list(self, matrix: List[List[float]]) -> Dict[int, Set[int]]:
        """
        Convert an adjacency matrix to an adjacency list.
        
        Args:
            matrix (List[List[float]]): Input adjacency matrix
            
        Returns:
            Dict[int, Set[int]]: Adjacency list representation
        """
        adj_list = defaultdict(set)
        n = len(matrix)
        for i in range(n):
            for j in range(n):
                if matrix[i][j] != 0:
                    adj_list[i].add(j)
        return adj_list

    def _get_node_degree(self, node: int, adj_list: Dict[int, Set[int]]) -> int:
        """
        Calculate the degree of a node.
        
        Args:
            node (int): Target node
            adj_list (Dict[int, Set[int]]): Adjacency list
            
        Returns:
            int: Node degree
        """
        return len(adj_list[node])

    def _get_clustering_coefficient(self, node: int, adj_list: Dict[int, Set[int]]) -> float:
        """
        Calculate the clustering coefficient of a node.
        
        Args:
            node (int): Target node
            adj_list (Dict[int, Set[int]]): Adjacency list
            
        Returns:
            float: Clustering coefficient
        """
        neighbors = adj_list[node]
        if len(neighbors) < 2:
            return 0.0
        
        possible_edges = len(neighbors) * (len(neighbors) - 1) / 2
        actual_edges = 0
        
        for neighbor1 in neighbors:
            for neighbor2 in neighbors:
                if neighbor1 < neighbor2 and neighbor2 in adj_list[neighbor1]:
                    actual_edges += 1
        
        return actual_edges / possible_edges if possible_edges > 0 else 0.0

    def _get_average_neighbor_degree(self, node: int, adj_list: Dict[int, Set[int]]) -> float:
        """
        Calculate the average degree of node's neighbors.
        
        Args:
            node (int): Target node
            adj_list (Dict[int, Set[int]]): Adjacency list
            
        Returns:
            float: Average neighbor degree
        """
        neighbors = adj_list[node]
        if not neighbors:
            return 0.0
        
        neighbor_degrees = [len(adj_list[neighbor]) for neighbor in neighbors]
        return sum(neighbor_degrees) / len(neighbor_degrees)

    def _get_ego_net_edges(self, node: int, adj_list: Dict[int, Set[int]]) -> int:
        """
        Calculate the number of edges in node's ego network.
        
        Args:
            node (int): Target node
            adj_list (Dict[int, Set[int]]): Adjacency list
            
        Returns:
            int: Number of edges in ego network
        """
        ego_net = {node} | adj_list[node]
        edge_count = 0
        
        for v in ego_net:
            for u in adj_list[v]:
                if u in ego_net and v < u:  # Count each edge only once
                    edge_count += 1
        
        return edge_count

    def _compute_statistics(self, values: List[float]) -> List[float]:
        """
        Compute the seven statistical measures for a feature.
        
        Args:
            values (List[float]): List of feature values
            
        Returns:
            List[float]: Seven statistical measures
        """
        if not values:
            return [0.0] * 7
        
        n = len(values)
        mean_val = mean(values)
        
        # Standard deviation
        variance = sum((x - mean_val) ** 2 for x in values) / n
        std_dev = sqrt(variance)
        
        # Skewness
        if std_dev == 0:
            skewness = 0
        else:
            skewness = sum((x - mean_val) ** 3 for x in values) / (n * std_dev ** 3)
        
        # Kurtosis
        if std_dev == 0:
            kurtosis = 0
        else:
            kurtosis = sum((x - mean_val) ** 4 for x in values) / (n * std_dev ** 4)
        
        # 90th percentile
        sorted_values = sorted(values)
        idx_90 = int(0.9 * (n - 1))
        percentile_90 = sorted_values[idx_90]
        
        # Number of non-zero values
        non_zero = sum(1 for x in values if x != 0)
        
        return [
            median(values),
            mean_val,
            std_dev,
            skewness,
            kurtosis,
            percentile_90,
            non_zero
        ]

    def _extract_features(self, adj_list: Dict[int, Set[int]]) -> List[List[float]]:
        """
        Extract all features for all nodes.
        
        Args:
            adj_list (Dict[int, Set[int]]): Adjacency list
            
        Returns:
            List[List[float]]: Feature matrix
        """
        features = []
        for node in adj_list:
            node_features = []
            
            # Degree
            degree = self._get_node_degree(node, adj_list)
            node_features.append(degree)
            
            # Clustering coefficient
            clustering = self._get_clustering_coefficient(node, adj_list)
            node_features.append(clustering)
            
            # Average neighbor degree
            avg_neighbor_degree = self._get_average_neighbor_degree(node, adj_list)
            node_features.append(avg_neighbor_degree)
            
            # Ego network edges
            ego_edges = self._get_ego_net_edges(node, adj_list)
            node_features.append(ego_edges)
            
            features.append(node_features)
        
        return features

    def _compute_signature(self, features: List[List[float]]) -> List[float]:
        """
        Compute the NetSimile signature from features.
        
        Args:
            features (List[List[float]]): Feature matrix
            
        Returns:
            List[float]: Network signature
        """
        signature = []
        n_features = len(features[0])
        
        # For each feature
        for i in range(n_features):
            feature_values = [node[i] for node in features]
            # Compute statistics and extend signature
            signature.extend(self._compute_statistics(feature_values))
        
        return signature

    def _canberra_distance(self, signature1: List[float], signature2: List[float]) -> float:
        """
        Compute Canberra distance between two signatures.
        
        Args:
            signature1 (List[float]): First signature
            signature2 (List[float]): Second signature
            
        Returns:
            float: Canberra distance
        """
        distance = 0.0
        for x, y in zip(signature1, signature2):
            if x == 0 and y == 0:
                continue
            distance += abs(x - y) / (abs(x) + abs(y))
        return distance

    def compute(self, A: List[List[float]], B: List[List[float]]) -> float:
        """
        Compute the NetSimile distance between two networks represented as matrices.
        
        Args:
            A (List[List[float]]): First adjacency matrix
            B (List[List[float]]): Second adjacency matrix
            
        Returns:
            float: NetSimile distance between the networks
        """
        # Convert matrices to adjacency lists
        adj_list_A = self._matrix_to_adjacency_list(A)
        adj_list_B = self._matrix_to_adjacency_list(B)
        
        # Extract features
        features_A = self._extract_features(adj_list_A)
        features_B = self._extract_features(adj_list_B)
        
        # Compute signatures
        signature_A = self._compute_signature(features_A)
        signature_B = self._compute_signature(features_B)
        
        # Calculate distance between signatures
        return self._canberra_distance(signature_A, signature_B)


from typing import List, Set, Dict, Tuple
from collections import defaultdict

class PatternBased(matrixDistance):
    """
    Implementation of Pattern-based distance measure for matrices.
    This measure identifies and compares local structural patterns between matrices.
    It focuses on:
    - Structural motifs (repeating patterns)
    - Local connectivity patterns
    - Submatrix patterns
    - Pattern frequency distributions
    
    The algorithm works by:
    1. Extracting local patterns of specified size
    2. Computing pattern frequencies
    3. Comparing pattern distributions
    """

    def __init__(self, pattern_size: int = 2):
        """
        Initialize the Pattern-based distance calculator.
        
        Args:
            pattern_size (int): Size of local patterns to extract (default: 2)
        """
        super().__init__()
        
        self.pattern_size = pattern_size

    def _extract_pattern(self, 
                        matrix: List[List[float]], 
                        row: int, 
                        col: int) -> Tuple[Tuple[float, ...], ...]:
        """
        Extract a local pattern from the matrix starting at given position.
        
        Args:
            matrix (List[List[float]]): Input matrix
            row (int): Starting row
            col (int): Starting column
            
        Returns:
            Tuple[Tuple[float, ...]]: Pattern as a tuple of tuples for hashability
        """
        pattern = []
        n = len(matrix)
        m = len(matrix[0])
        
        for i in range(self.pattern_size):
            if row + i >= n:
                return tuple()
            
            row_pattern = []
            for j in range(self.pattern_size):
                if col + j >= m:
                    return tuple()
                row_pattern.append(matrix[row + i][col + j])
            pattern.append(tuple(row_pattern))
            
        return tuple(pattern)

    def _get_pattern_signature(self, pattern: Tuple[Tuple[float, ...], ...]) -> str:
        """
        Convert a pattern to a canonical string representation.
        This helps identify equivalent patterns regardless of exact values.
        
        Args:
            pattern (Tuple[Tuple[float, ...]]): Input pattern
            
        Returns:
            str: Pattern signature
        """
        if not pattern:
            return ""
            
        # Create value mapping for normalization
        value_map = {}
        next_value = 0
        signature_parts = []
        
        for row in pattern:
            row_sig = []
            for val in row:
                if val not in value_map:
                    value_map[val] = str(next_value)
                    next_value += 1
                row_sig.append(value_map[val])
            signature_parts.append('_'.join(row_sig))
        
        return '|'.join(signature_parts)

    def _extract_all_patterns(self, matrix: List[List[float]]) -> Dict[str, int]:
        """
        Extract all patterns from the matrix and count their frequencies.
        
        Args:
            matrix (List[List[float]]): Input matrix
            
        Returns:
            Dict[str, int]: Pattern frequency distribution
        """
        pattern_counts = defaultdict(int)
        n = len(matrix)
        m = len(matrix[0])
        
        for i in range(n - self.pattern_size + 1):
            for j in range(m - self.pattern_size + 1):
                pattern = self._extract_pattern(matrix, i, j)
                if pattern:
                    signature = self._get_pattern_signature(pattern)
                    pattern_counts[signature] += 1
                    
        return pattern_counts

    def _normalize_distribution(self, distribution: Dict[str, int]) -> Dict[str, float]:
        """
        Normalize pattern frequency distribution.
        
        Args:
            distribution (Dict[str, int]): Pattern frequency counts
            
        Returns:
            Dict[str, float]: Normalized distribution
        """
        total = sum(distribution.values())
        if total == 0:
            return {}
        
        return {k: v / total for k, v in distribution.items()}

    def _compute_correlation_distance(self, 
                                   dist1: Dict[str, float], 
                                   dist2: Dict[str, float]) -> float:
        """
        Compute correlation-based distance between pattern distributions.
        
        Args:
            dist1 (Dict[str, float]): First distribution
            dist2 (Dict[str, float]): Second distribution
            
        Returns:
            float: Distance between distributions
        """
        # Get all patterns
        all_patterns = set(dist1.keys()) | set(dist2.keys())
        
        # Convert to vectors
        vec1 = [dist1.get(p, 0.0) for p in all_patterns]
        vec2 = [dist2.get(p, 0.0) for p in all_patterns]
        
        # Compute correlation coefficient
        n = len(vec1)
        if n == 0:
            return 1.0
            
        mean1 = sum(vec1) / n
        mean2 = sum(vec2) / n
        
        numerator = sum((x - mean1) * (y - mean2) for x, y in zip(vec1, vec2))
        denom1 = sum((x - mean1) ** 2 for x in vec1)
        denom2 = sum((y - mean2) ** 2 for y in vec2)
        
        if denom1 == 0 or denom2 == 0:
            return 1.0
            
        correlation = numerator / ((denom1 * denom2) ** 0.5)
        
        # Convert correlation to distance (1 - correlation) / 2
        # This ensures distance is between 0 and 1
        return (1 - correlation) / 2

    def _compute_jaccard_distance(self, 
                                dist1: Dict[str, float], 
                                dist2: Dict[str, float]) -> float:
        """
        Compute Jaccard distance between pattern sets.
        
        Args:
            dist1 (Dict[str, float]): First distribution
            dist2 (Dict[str, float]): Second distribution
            
        Returns:
            float: Jaccard distance
        """
        patterns1 = set(dist1.keys())
        patterns2 = set(dist2.keys())
        
        intersection = len(patterns1 & patterns2)
        union = len(patterns1 | patterns2)
        
        if union == 0:
            return 0.0
            
        return 1 - (intersection / union)

    def compute(self, 
                        A: List[List[float]], 
                        B: List[List[float]], 
                        method: str = "correlation") -> float:
        """
        Compute the Pattern-based distance between two matrices.
        
        Args:
            A (List[List[float]]): First matrix
            B (List[List[float]]): Second matrix
            method (str): Distance method - "correlation" or "jaccard"
            
        Returns:
            float: Pattern-based distance between matrices
        """
        # Extract patterns and their frequencies
        patterns_A = self._extract_all_patterns(A)
        patterns_B = self._extract_all_patterns(B)
        
        # Normalize distributions
        norm_dist_A = self._normalize_distribution(patterns_A)
        norm_dist_B = self._normalize_distribution(patterns_B)
        
        # Compute distance based on selected method
        if method == "jaccard":
            return self._compute_jaccard_distance(norm_dist_A, norm_dist_B)
        else:  # correlation
            return self._compute_correlation_distance(norm_dist_A, norm_dist_B)
from typing import List, Set, Dict, Tuple
from itertools import combinations

class CliqueBasedGraph(matrixDistance):
    """
    Calculates graph distance using clique-based structural comparison.
    
    Focuses on analyzing maximal cliques and their overlap between graphs.
    """
    
    def __init__(self, node_weight: float = 1.0, clique_weight: float = 2.0):
        """
        Initialize the Clique-Based Graph Distance calculator.
        
        Args:
            node_weight (float): Weight for node differences. Defaults to 1.0
            clique_weight (float): Weight for clique structure differences. Defaults to 2.0
        """
        super().__init__()
        
        self.node_weight = node_weight
        self.clique_weight = clique_weight
    
    def compute(self, graph1: List[List[float]], graph2: List[List[float]]) -> float:
        """
        Compute graph distance based on clique structure.
        
        Args:
            graph1 (List[List[float]]): First graph adjacency matrix
            graph2 (List[List[float]]): Second graph adjacency matrix
        
        Returns:
            float: Calculated graph distance
        """
        self._validate_matrices(graph1, graph2)
        
        # Find maximal cliques in both graphs
        cliques1 = self._find_maximal_cliques(graph1)
        cliques2 = self._find_maximal_cliques(graph2)
        
        # Calculate distance components
        node_distance = self._compute_node_distance(graph1, graph2)
        clique_distance = self._compute_clique_distance(cliques1, cliques2)
        
        return node_distance + clique_distance
    
    def _validate_matrices(self, graph1: List[List[float]], graph2: List[List[float]]) -> None:
        """
        Validate input graph matrices.
        
        Args:
            graph1 (List[List[float]]): First graph matrix
            graph2 (List[List[float]]): Second graph matrix
        
        Raises:
            ValueError: If matrices are invalid
        """
        if not (
            all(len(row) == len(graph1) for row in graph1) and
            all(len(row) == len(graph2) for row in graph2)
        ):
            raise ValueError("Input matrices must be square")
    
    def _find_maximal_cliques(self, graph: List[List[float]]) -> List[Set[int]]:
        """
        Find all maximal cliques in the graph using Bron-Kerbosch algorithm.
        
        Args:
            graph (List[List[float]]): Graph adjacency matrix
        
        Returns:
            List[Set[int]]: List of maximal cliques
        """
        def is_clique(nodes: Set[int]) -> bool:
            """Check if given nodes form a complete subgraph."""
            return all(
                graph[u][v] > 0 
                for u, v in combinations(nodes, 2)
                if u != v
            )
        
        def bron_kerbosch(r: Set[int], p: Set[int], x: Set[int]) -> None:
            """
            Recursive Bron-Kerbosch algorithm for finding maximal cliques.
            
            Args:
                r (Set[int]): Current clique being built
                p (Set[int]): Potential nodes to add
                x (Set[int]): Excluded nodes
            """
            if not p and not x:
                if is_clique(r):
                    maximal_cliques.append(r)
                return
            
            for v in list(p):
                new_r = r.union({v})
                new_p = p.intersection(set(
                    u for u in range(len(graph)) 
                    if graph[v][u] > 0 and u in p
                ))
                new_x = x.intersection(set(
                    u for u in range(len(graph)) 
                    if graph[v][u] > 0 and u in x
                ))
                
                bron_kerbosch(new_r, new_p, new_x)
                p.remove(v)
                x.add(v)
        
        # Initialize variables
        maximal_cliques: List[Set[int]] = []
        nodes = set(range(len(graph)))
        
        # Run Bron-Kerbosch algorithm
        bron_kerbosch(set(), nodes, set())
        
        return maximal_cliques
    
    def _compute_node_distance(self, 
                                graph1: List[List[float]], 
                                graph2: List[List[float]]) -> float:
        """
        Calculate distance based on node differences.
        
        Args:
            graph1 (List[List[float]]): First graph matrix
            graph2 (List[List[float]]): Second graph matrix
        
        Returns:
            float: Node-based distance
        """
        n1, n2 = len(graph1), len(graph2)
        return abs(n1 - n2) * self.node_weight
    
    def _compute_clique_distance(self, 
                                  cliques1: List[Set[int]], 
                                  cliques2: List[Set[int]]) -> float:
        """
        Calculate distance based on clique structure differences.
        
        Args:
            cliques1 (List[Set[int]]): Maximal cliques of first graph
            cliques2 (List[Set[int]]): Maximal cliques of second graph
        
        Returns:
            float: Clique structure distance
        """
        # Compute clique matching and differences
        matched_cliques = 0
        total_cliques = len(cliques1) + len(cliques2)
        
        for c1 in cliques1:
            for c2 in cliques2:
                # Compute clique similarity
                overlap = len(c1.intersection(c2)) / max(len(c1), len(c2))
                if overlap > 0.5:  # Threshold for matching
                    matched_cliques += 1
                    break
        
        # Calculate clique distance
        unmatched_cliques = total_cliques - (2 * matched_cliques)
        return unmatched_cliques * self.clique_weight
    
    def similarity_score(self, graph1: List[List[float]], graph2: List[List[float]]) -> float:
        """
        Compute a similarity score between 0 and 1.
        
        Args:
            graph1 (List[List[float]]): First graph adjacency matrix
            graph2 (List[List[float]]): Second graph adjacency matrix
        
        Returns:
            float: Similarity score (1 = identical, 0 = completely different)
        """
        distance = self.compute(graph1, graph2)
        max_distance = self._compute_max_distance(graph1, graph2)
        
        return 1.0 - (distance / max_distance) if max_distance > 0 else 1.0
    
    def _compute_max_distance(self, 
                               graph1: List[List[float]], 
                               graph2: List[List[float]]) -> float:
        """
        Calculate maximum possible distance between graphs.
        
        Args:
            graph1 (List[List[float]]): First graph matrix
            graph2 (List[List[float]]): Second graph matrix
        
        Returns:
            float: Maximum possible distance
        """
        n1, n2 = len(graph1), len(graph2)
        max_node_diff = abs(n1 - n2)
        max_clique_count = max(len(self._find_maximal_cliques(graph1)), 
                               len(self._find_maximal_cliques(graph2)))
        
        return (max_node_diff * self.node_weight + 
                max_clique_count * self.clique_weight)


from typing import List, TypeVar, Union
from math import sqrt, acos, pi

T = TypeVar('T', int, float)

class TriangleMatrixDistance(matrixDistance):
    """
    A class to calculate distance between matrices based on triangular transformations.
    
    The distance is computed by analyzing triangular patterns and angle variations
    between corresponding matrix elements.
    """
    
    def __init__(self, window_size: int = 3, tolerance: float = 1e-6):
        """
        Initialize the distance calculator with two matrices.
        
        Args:
            matrix1 (List[List[T]]): First input matrix 
            matrix2 (List[List[T]]): Second input matrix
        
        Raises:
            ValueError: If matrices have different dimensions
        """
        super().__init__()
        self.window_size=window_size
        self.tolerance=tolerance
    
    def _validate_matrices(self, matrix1: List[List[T]], matrix2: List[List[T]]) -> None:
        """
        Validate that both matrices have the same dimensions.
        
        Args:
            matrix1 (List[List[T]]): First matrix to validate
            matrix2 (List[List[T]]): Second matrix to validate
        
        Raises:
            ValueError: If matrices have different dimensions
        """
        if len(matrix1) != len(matrix2):
            raise ValueError("Matrices must have the same number of rows")
        
        if len(matrix1[0]) != len(matrix2[0]):
            raise ValueError("Matrices must have the same number of columns")
    
    def _compute_triangle_angle(self, a: T, b: T, c: T) -> float:
        """
        Compute the angle of a triangle formed by three matrix elements.
        
        Args:
            a (T): First element
            b (T): Second element
            c (T): Third element
        
        Returns:
            float: Angle in radians between the triangle's sides
        """
        # Prevent division by zero and handle very small values
        a, b, c = abs(float(a)), abs(float(b)), abs(float(c))
        
        # Avoid invalid triangle configurations
        if a + b <= c or a + c <= b or b + c <= a:
            return 0.0
        
        # Compute the cosine of the angle using the law of cosines
        cos_angle = (a**2 + b**2 - c**2) / (2 * a * b)
        
        # Ensure cos_angle is within valid range [-1, 1]
        cos_angle = max(min(cos_angle, 1), -1)
        
        return acos(cos_angle)
    
    def compute(self, matrix1: List[List[T]], matrix2: List[List[T]]) -> float:
        """
        Compute the distance between matrices based on triangular patterns.
        
        Args:
            window_size (int): Size of the sliding window for triangle computation
            tolerance (float): Precision threshold for comparisons
        
        Returns:
            float: Calculated distance representing triangular transformation complexity
        """
        rows = len(matrix1)
        cols = len(matrix1[0])
        
        if self.window_size < 3:
            raise ValueError("Window size must be at least 3")
        
        total_triangle_angles = 0.0
        total_windows = 0
        
        # Slide the window across the matrix
        for i in range(rows - self.window_size + 1):
            for j in range(cols - self.window_size + 1):
                # Compute triangle angles for corresponding windows
                window1_angles = self._compute_window_angles(
                    matrix1, i, j, self.window_size
                )
                window2_angles = self._compute_window_angles(
                    matrix2, i, j, self.window_size
                )
                
                # Compare window angles
                window_distance = self._compare_window_angles(
                    window1_angles, window2_angles)
                
                total_triangle_angles += window_distance
                total_windows += 1
        
        # Normalize the distance
        return sqrt(total_triangle_angles / total_windows) if total_windows > 0 else 0.0
    
    def _compute_window_angles(self, matrix: List[List[T]], row: int, col: int, 
                                window_size: int) -> List[float]:
        """
        Compute triangle angles for a specific matrix window.
        
        Args:
            matrix (List[List[T]]): Source matrix
            row (int): Starting row of the window
            col (int): Starting column of the window
            window_size (int): Size of the sliding window
        
        Returns:
            List[float]: Angles of triangles within the window
        """
        angles = []
        
        # Compute all possible triangle angles within the window
        for i in range(window_size):
            for j in range(i + 1, window_size):
                for k in range(j + 1, window_size):
                    a = matrix[row + i][col + j]
                    b = matrix[row + i][col + k]
                    c = matrix[row + j][col + k]
                    
                    angle = self._compute_triangle_angle(a, b, c)
                    angles.append(angle)
        
        return angles
    
    def _compare_window_angles(self, angles1: List[float], 
                                angles2: List[float]) -> float:
        """
        Compare triangle angles between two matrix windows.
        
        Args:
            angles1 (List[float]): Angles from first matrix window
            angles2 (List[float]): Angles from second matrix window
            tolerance (float): Precision threshold for comparisons
        
        Returns:
            float: Distance between window angle configurations
        """
        if len(angles1) != len(angles2):
            return float('inf')
        
        # Compute angle differences
        angle_differences = [
            abs(a1 - a2) for a1, a2 in zip(sorted(angles1), sorted(angles2))
        ]
        
        # Compute root mean square of angle differences
        return sqrt(
            sum(diff**2 for diff in angle_differences) / len(angle_differences)
        )
    

from typing import List, TypeVar, Dict, Set, Tuple
from math import sqrt, log

T = TypeVar('T', int, float)

class GraphletMatrixDistance(matrixDistance):
    """
    A class to calculate distance between matrices based on graphlet distribution.
    
    Computes matrix similarity by analyzing the distribution of local graph structures
    (graphlets) within the matrix as an adjacency representation.
    """
    
    def __init__(self, normalize: bool = True):
        """
        Initialize the distance calculator with two matrices.
        
        Args:
            matrix1 (List[List[T]]): First input matrix as adjacency matrix
            matrix2 (List[List[T]]): Second input matrix as adjacency matrix
        
        Raises:
            ValueError: If matrices are not square or have different dimensions
        """
        super().__init__()
        self.normalize=normalize
        
    
    def _validate_matrices(self, matrix1: List[List[T]], matrix2: List[List[T]]) -> None:
        """
        Validate matrix properties: square matrices of same size.
        
        Args:
            matrix1 (List[List[T]]): First matrix to validate
            matrix2 (List[List[T]]): Second matrix to validate
        
        Raises:
            ValueError: If matrices are invalid
        """
        if not all(len(row) == len(matrix1) for row in matrix1):
            raise ValueError("Matrix 1 must be square")
        
        if not all(len(row) == len(matrix2) for row in matrix2):
            raise ValueError("Matrix 2 must be square")
        
        if len(matrix1) != len(matrix2):
            raise ValueError("Matrices must have the same dimensions")
    
    def _count_graphlets(self, matrix: List[List[T]]) -> Dict[str, int]:
        """
        Count different types of local graph structures (graphlets).
        
        Args:
            matrix (List[List[T]]): Adjacency matrix to analyze
        
        Returns:
            Dict[str, int]: Counts of different graphlet types
        """
        graphlets: Dict[str, int] = {
            'isolated_node': 0,   # 0-node
            'single_edge': 0,     # 1-edge 
            'triangle': 0,         # 3-node complete
            'star': 0,             # Star-like structure
            'path': 0              # Linear path
        }
        
        # Find total graph structures
        size = len(matrix)

        for i in range(size):
            # Isolated node check
            if sum(1 for j in range(size) if matrix[i][j] != 0) == 0:
                graphlets['isolated_node'] += 1
            
            for j in range(i+1, size):
                # Check for edges
                if matrix[i][j] != 0:
                    graphlets['single_edge'] += 1
                    
                    # Path and star detection
                    for k in range(j+1, size):
                        if matrix[j][k] != 0:
                            graphlets['path'] += 1
                        
                        # Triangle detection
                        if matrix[i][k] != 0:
                            graphlets['triangle'] += 1
                            
                        # Star detection
                        if matrix[i][k] != 0 and matrix[j][k] != 0:
                            graphlets['star'] += 1
        
        return graphlets
    
    def compute(self, matrix1: List[List[T]], matrix2: List[List[T]]) -> float:
        """
        Compute the distance between matrices based on graphlet distribution.
        
        Args:
            normalize (bool): Whether to normalize the distance
        
        Returns:
            float: Calculated distance representing graphlet distribution difference
        """
        # Count graphlets for both matrices
        graphlets1 = self._count_graphlets(matrix1)
        graphlets2 = self._count_graphlets(matrix2)
        
        # Compute Jensen-Shannon divergence between graphlet distributions
        js_divergence = self._jensen_shannon_divergence(graphlets1, graphlets2)
        
        return sqrt(js_divergence) if self.normalize else js_divergence
    
    def _jensen_shannon_divergence(self, 
                                    dist1: Dict[str, int], 
                                    dist2: Dict[str, int]) -> float:
        """
        Compute Jensen-Shannon divergence between two graphlet distributions.
        
        Args:
            dist1 (Dict[str, int]): First graphlet distribution
            dist2 (Dict[str, int]): Second graphlet distribution
        
        Returns:
            float: Jensen-Shannon divergence value
        """
        # Total counts for normalization
        total1 = sum(dist1.values())
        total2 = sum(dist2.values())
        
        # Compute probability distributions
        prob1 = {k: v/total1 for k, v in dist1.items()}
        prob2 = {k: v/total2 for k, v in dist2.items()}
        
        # Merge keys from both distributions
        all_keys = set(prob1.keys()) | set(prob2.keys())
        
        # Compute divergence
        js_div = 0.0
        for key in all_keys:
            p1 = prob1.get(key, 0.0)
            p2 = prob2.get(key, 0.0)
            
            # Average probability
            avg_prob = 0.5 * (p1 + p2)
            
            # Compute KL divergence components
            if p1 > 0:
                js_div += p1 * log(p1 / avg_prob)
            if p2 > 0:
                js_div += p2 * log(p2 / avg_prob)
        
        return js_div
    
    def __str__(self) -> str:
        """
        Provide a string representation of the distance calculation.
        
        Returns:
            str: Descriptive string of graphlet matrix distance
        """
        distance = self.compute()
        return f"Graphlet Matrix Distance: {distance:.4f}"
    
    def detailed_graphlet_analysis(self, matrix1: List[List[T]], matrix2: List[List[T]]) -> Dict[str, Tuple[int, int]]:
        """
        Provide detailed graphlet distribution comparison.
        
        Returns:
            Dict[str, Tuple[int, int]]: Graphlet counts for both matrices
        """
        graphlets1 = self._count_graphlets(matrix1)
        graphlets2 = self._count_graphlets(matrix2)
        
        return {
            graphlet: (count1, graphlets2.get(graphlet, 0))
            for graphlet, count1 in graphlets1.items()
        }
        
from typing import List, TypeVar, Optional
from math import sqrt

T = TypeVar('T', int, float)

class OptimizedMaxFlowMatrixDistance(matrixDistance):
    """
    Optimized matrix distance calculation using maximum flow analysis.
    """
    
    def __init__(self, normalize: bool = True):
        """
        Initialize distance calculator with improved performance.
        """
        super().__init__()
        self.normalize=normalize
        
    
    def _validate_matrices(self, matrix1: List[List[T]], matrix2: List[List[T]]) -> None:
        """
        Quickly validate matrix dimensions.
        """
        if len(matrix1) != len(matrix2) or len(matrix1[0]) != len(matrix2[0]):
            raise ValueError("Matrices must have identical dimensions")
    
    def _dinic_max_flow(self, graph: List[List[float]]) -> float:
        """
        Dinic's algorithm for maximum flow - significantly faster
        """
        def bfs() -> bool:
            # Reset levels and queue
            level[:] = [-1] * len(graph)
            level[source] = 0
            queue = [source]
            
            while queue:
                v = queue.pop(0)
                for u in range(len(graph)):
                    if level[u] == -1 and graph[v][u] > 0:
                        level[u] = level[v] + 1
                        queue.append(u)
            
            return level[sink] != -1
        
        def dfs(v: int, flow: float) -> float:
            if v == sink:
                return flow
            
            for u in range(len(graph)):
                residual = graph[v][u]
                if level[u] == level[v] + 1 and residual > 0:
                    curr_flow = dfs(u, min(flow, residual))
                    if curr_flow > 0:
                        graph[v][u] -= curr_flow
                        graph[u][v] += curr_flow
                        return curr_flow
            
            return 0.0
        
        # Graph size and source/sink
        n = self.rows * self.cols + 2
        source, sink = 0, n - 1
        
        # Maximum flow
        max_flow = 0.0
        
        # Level tracking for Dinic's algorithm
        level = [0] * n
        
        while bfs():
            while True:
                path_flow = dfs(source, float('inf'))
                if path_flow == 0:
                    break
                max_flow += path_flow
        
        return max_flow
    
    def _build_fast_flow_network(self, matrix: List[List[T]]) -> List[List[float]]:
        """
        Optimized flow network construction with fixed-size matrix
        """
        rows = len(matrix)
        cols = len(matrix[0])
        
        n = rows * cols + 2
        graph = [[0.0] * n for _ in range(n)]
        source, sink = 0, n - 1
        
        # Optimized network construction
        for i in range(rows):
            for j in range(cols):
                node = i * cols + j + 1
                flow_value = abs(float(matrix[i][j]))
                
                # Simplified source and sink connections
                if i == 0:
                    graph[source][node] = flow_value
                if i == self.rows - 1:
                    graph[node][sink] = flow_value
                
                # Layer connections
                if i < rows - 1:
                    next_layer_node = (i + 1) * cols + j + 1
                    graph[node][next_layer_node] = flow_value
        
        return graph
    
    def compute(self, matrix1: List[List[T]], matrix2: List[List[T]]) -> float:
        """
        Compute matrix distance using optimized max flow calculation
        """
        
        
        network1 = self._build_fast_flow_network(matrix1)
        network2 = self._build_fast_flow_network(matrix2)
        
        max_flow1 = self._dinic_max_flow(network1)
        max_flow2 = self._dinic_max_flow(network2.copy())
        
        flow_distance = abs(max_flow1 - max_flow2)
        return sqrt(flow_distance) if self.normalize else flow_distance

from typing import List, Optional, Tuple

class MinimumCutDistanceCalculator(matrixDistance):
    """
    A class to calculate the minimum cut distance between two matrices.
    
    This implementation provides a method to compute the minimum number of 
    elements that need to be removed to disconnect two matrices.
    """
    
    def __init__(self):
        """
        Initialize the calculator with two input matrices.
        
        Args:
            matrix1 (List[List[int]]): First input matrix
            matrix2 (List[List[int]]): Second input matrix
        """
        super().__init__() 
    
    def _validate_matrices(self, matrix1: List[List[int]], matrix2: List[List[int]]) -> None:
        """
        Validate that the input matrices have the same dimensions.
        
        Raises:
            ValueError: If matrices have different dimensions or are empty
        """
        if not matrix1 or not matrix2:
            raise ValueError("Matrices cannot be empty")
        
        if len(matrix1) != len(matrix2) or len(matrix1[0]) != len(matrix2[0]):
            raise ValueError("Matrices must have the same dimensions")
    
    def compute(self, matrix1: List[List[int]], matrix2: List[List[int]]) -> int:
        """
        Calculate the minimum cut distance between two matrices.
        
        The minimum cut distance is the minimum number of elements 
        that must be changed to transform matrix1 into matrix2.
        
        Returns:
            int: The minimum number of elements that need to be changed
        """
        rows = len(matrix1)
        cols = len(matrix1[0])
        
        cut_distance = 0
        for i in range(rows):
            for j in range(cols):
                if matrix1[i][j] != matrix2[i][j]:
                    cut_distance += 1
        
        return cut_distance
    
    def get_cut_positions(self, matrix1: List[List[int]], matrix2: List[List[int]]) -> List[Tuple[int, int]]:
        """
        Get the positions of elements that need to be changed.
        
        Returns:
            List[Tuple[int, int]]: List of (row, col) positions where 
            matrices differ
        """
        cut_positions = []
        for i in range(self.rows):
            for j in range(self.cols):
                if matrix1[i][j] != matrix2[i][j]:
                    cut_positions.append((i, j))
        
        return cut_positions
    
    def get_detailed_difference(self, matrix1: List[List[int]], matrix2: List[List[int]]) -> Optional[dict]:
        """
        Provide a detailed breakdown of the differences between matrices.
        
        Returns:
            Optional[dict]: A dictionary with detailed difference information
        """
        if self.compute(matrix1,matrix2) == 0:
            return None
        
        return {
            "total_cut_distance": self.compute(matrix1,matrix2),
            "cut_positions": self.get_cut_positions(matrix1,matrix2),
            "matrix1_values": [matrix1[pos[0]][pos[1]] for pos in self.get_cut_positions(matrix1,matrix2)],
            "matrix2_values": [matrix2[pos[0]][pos[1]] for pos in self.get_cut_positions(matrix1,matrix2)]
        }
from typing import List, Tuple, Set
from enum import Enum
from collections import deque

class PercolationType(Enum):
    """
    Enum to represent different types of percolation connectivity.
    """
    HORIZONTAL = 1
    VERTICAL = 2
    DIAGONAL = 3

class Percolation(matrixDistance):
    """
    A class to calculate the percolation distance between two matrices.
    
    Percolation distance measures the minimum number of changes required 
    to create a connected path through the matrix.
    """
    
    def __init__(self, percolation_type: PercolationType = PercolationType.HORIZONTAL):
        """
        Initialize the percolation distance calculator.
        
        Args:
            matrix1 (List[List[int]]): First input matrix
            matrix2 (List[List[int]]): Second input matrix
            percolation_type (PercolationType): Type of percolation connectivity
        """
        super().__init__()
        

        self.percolation_type = percolation_type
    
    def _validate_matrices(self, matrix1: List[List[int]], matrix2: List[List[int]]) -> None:
        """
        Validate input matrices dimensions.
        
        Raises:
            ValueError: If matrices have different dimensions or are empty
        """
        if not matrix1 or not matrix2:
            raise ValueError("Matrices cannot be empty")
        
        if len(matrix1) != len(matrix2) or len(matrix1[0]) != len(matrix2[0]):
            raise ValueError("Matrices must have the same dimensions")
    
    def _get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """
        Get neighboring cells based on percolation type.
        
        Args:
            x (int): Row index
            y (int): Column index
        
        Returns:
            List[Tuple[int, int]]: List of neighboring cell coordinates
        """
        neighbors = []
        directions = []
        
        if self.percolation_type == PercolationType.HORIZONTAL:
            directions = [(0, 1), (0, -1)]
        elif self.percolation_type == PercolationType.VERTICAL:
            directions = [(1, 0), (-1, 0)]
        elif self.percolation_type == PercolationType.DIAGONAL:
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0), 
                          (1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.rows and 0 <= ny < self.cols:
                neighbors.append((nx, ny))
        
        return neighbors
    
    def compute(self, matrix1: List[List[int]], matrix2: List[List[int]]) -> int:
        """
        Calculate the percolation distance between two matrices.
        
        Returns:
            int: Minimum number of changes to create a percolation path
        """
        rows = len(matrix1)
        cols = len(matrix1[0])
        changes = []
        for i in range(self.rows):
            for j in range(self.cols):
                if matrix1[i][j] != matrix2[i][j]:
                    changes.append((i, j))
        
        return self._find_minimum_percolation_path(changes,matrix1,matrix2)
    
    def _find_minimum_percolation_path(self, changes: List[Tuple[int, int]],matrix1,matrix2) -> int:
        """
        Find the minimum number of changes to create a percolation path.
        
        Args:
            changes (List[Tuple[int, int]]): Positions of different cells
        
        Returns:
            int: Minimum number of changes for percolation
        """
        if not changes:
            return 0
        
        # Try all possible minimal subsets of changes
        min_changes = len(changes)
        
        for k in range(1, len(changes) + 1):
            for subset in self._generate_combinations(changes, k):
                if self._check_percolation_path(subset,matrix1,matrix2):
                    min_changes = min(min_changes, k)
                    break
        
        return min_changes
    
    def _check_percolation_path(self, changes: List[Tuple[int, int]],matrix1,matrix2) -> bool:
        """
        Check if a given set of changes creates a percolation path.
        
        Args:
            changes (List[Tuple[int, int]]): Positions to change
        
        Returns:
            bool: True if a percolation path exists, False otherwise
        """
        # Create a modified matrix
        modified_matrix = [row.copy() for row in matrix1]
        for x, y in changes:
            modified_matrix[x][y] = matrix2[x][y]
        
        # Check for percolation path
        if self.percolation_type == PercolationType.HORIZONTAL:
            return self._check_horizontal_percolation(modified_matrix)
        elif self.percolation_type == PercolationType.VERTICAL:
            return self._check_vertical_percolation(modified_matrix)
        elif self.percolation_type == PercolationType.DIAGONAL:
            return self._check_diagonal_percolation(modified_matrix)
    
    def _check_horizontal_percolation(self, matrix: List[List[int]]) -> bool:
        """
        Check if a horizontal percolation path exists.
        
        Args:
            matrix (List[List[int]]): Modified matrix
        
        Returns:
            bool: True if a horizontal path exists
        """
        for row in matrix:
            if len(set(row)) == 1:
                return True
        return False
    
    def _check_vertical_percolation(self, matrix: List[List[int]]) -> bool:
        """
        Check if a vertical percolation path exists.
        
        Args:
            matrix (List[List[int]]): Modified matrix
        
        Returns:
            bool: True if a vertical path exists
        """
        for j in range(self.cols):
            column = [matrix[i][j] for i in range(self.rows)]
            if len(set(column)) == 1:
                return True
        return False
    
    def _check_diagonal_percolation(self, matrix: List[List[int]]) -> bool:
        """
        Check if a diagonal percolation path exists.
        
        Args:
            matrix (List[List[int]]): Modified matrix
        
        Returns:
            bool: True if a diagonal path exists
        """
        # Check diagonals and anti-diagonals
        for start_row in range(self.rows):
            diagonal1 = [matrix[start_row + i][i] for i in range(min(self.rows - start_row, self.cols))]
            if len(set(diagonal1)) == 1:
                return True
        
        for start_col in range(self.cols):
            diagonal2 = [matrix[i][start_col + i] for i in range(min(self.rows, self.cols - start_col))]
            if len(set(diagonal2)) == 1:
                return True
        
        return False
    
    def _generate_combinations(self, items: List[Tuple[int, int]], k: int) -> List[List[Tuple[int, int]]]:
        """
        Generate all combinations of k items from the list.
        
        Args:
            items (List[Tuple[int, int]]): List of items
            k (int): Number of items to select
        
        Returns:
            List[List[Tuple[int, int]]]: All possible combinations
        """
        def backtrack(start: int, current: List[Tuple[int, int]]):
            if len(current) == k:
                result.append(current.copy())
                return
            
            for i in range(start, len(items)):
                current.append(items[i])
                backtrack(i + 1, current)
                current.pop()
        
        result: List[List[Tuple[int, int]]] = []
        backtrack(0, [])
        return result


from typing import List, Union
from numbers import Number

class VonNeumann(matrixDistance):
    """
    Calculate the Von Neumann distance (Manhattan/L1 distance) between two matrices
    using pure Python lists.
    
    Args:
        matrix1 (List[List[Number]]): First input matrix as list of lists
        matrix2 (List[List[Number]]): Second input matrix as list of lists
    
    Returns:
        float: The Von Neumann distance between the matrices
        
    Raises:
        ValueError: If matrices have different dimensions or are empty
        TypeError: If matrices contain non-numeric values
        
    Examples:
        >>> m1 = [[1, 2], [3, 4]]
        >>> m2 = [[2, 3], [4, 5]]
        >>> von_neumann_distance(m1, m2)
        4.0  # |1-2| + |2-3| + |3-4| + |4-5| = 1 + 1 + 1 + 1 = 4
    """
    
    def __init__(self):
        """
        Initialize the percolation distance calculator.
        
        Args:
            matrix1 (List[List[int]]): First input matrix
            matrix2 (List[List[int]]): Second input matrix
            percolation_type (PercolationType): Type of percolation connectivity
        """
        super().__init__()

    @staticmethod
    def validate(matrix1: List[List[float]], matrix2: List[List[float]]) -> None:
      # Validate matrices dimensions
      if not matrix1 or not matrix2:
        raise ValueError("Matrices cannot be empty")
    
      if len(matrix1) != len(matrix2):
        raise ValueError("Matrices must have the same number of rows")
    
      if len(matrix1[0]) != len(matrix2[0]):
        raise ValueError("Matrices must have the same number of columns")
      # Validate that all rows have the same length
      
      for row1, row2 in zip(matrix1, matrix2):
        if len(row1) != len(matrix1[0]) or len(row2) != len(matrix2[0]):
            raise ValueError("All rows must have the same length")
        
        # Validate that all elements are numeric
        if not all(isinstance(x, float) for x in row1 + row2):
            raise TypeError("All matrix elements must be numeric")

    def compute(self,matrix1: List[List[float]],matrix2: List[List[float]]) -> float:
      # Calculate Von Neumann distance
      distance: float = 0.0
      for i in range(len(matrix1)):
        for j in range(len(matrix1[0])):
            distance += abs(matrix1[i][j] - matrix2[i][j])
      return distance


from typing import List, Union, Tuple
from numbers import Number
import math

class GraphEntropyDistance(matrixDistance):
    """
    A class to compute the entropy distance between two graphs represented as adjacency matrices.
    The entropy is calculated using graph spectra and Von Neumann entropy.
    """
    
    def __init__(self, epsilon: float = 1e-10, max_iterations: int = 50):
        """
        Initialize the GraphEntropyDistance calculator.
        
        Args:
            epsilon (float): Small value to avoid log(0) in calculations
            max_iterations (int): Maximum iterations for eigenvalue calculations
        """
        super().__init__()
        
        self._epsilon = epsilon
        self._max_iterations = max_iterations
    
    @staticmethod
    def validate_matrices(matrix1: List[List[Number]], 
                         matrix2: List[List[Number]]) -> None:
        """Validate input matrices format and values."""
        if not matrix1 or not matrix2:
            raise ValueError("Matrices cannot be empty")
        
        if len(matrix1) != len(matrix2):
            raise ValueError("Matrices must have the same dimensions")
        
        for row1, row2 in zip(matrix1, matrix2):
            if len(row1) != len(matrix1) or len(row2) != len(matrix2):
                raise ValueError("Matrices must be square")
            if not all(isinstance(x, Number) for x in row1 + row2):
                raise TypeError("All matrix elements must be numeric")
    
    def _get_degree_matrix(self, matrix: List[List[Number]]) -> List[List[float]]:
        """
        Calculate the degree matrix of a graph.
        
        Args:
            matrix: Input adjacency matrix
            
        Returns:
            Degree matrix
        """
        n = len(matrix)
        degree_matrix = [[0.0] * n for _ in range(n)]
        
        for i in range(n):
            degree = sum(float(matrix[i][j]) for j in range(n))
            degree_matrix[i][i] = degree if degree > self._epsilon else self._epsilon
            
        return degree_matrix
    
    def _get_laplacian(self, matrix: List[List[Number]]) -> List[List[float]]:
        """
        Calculate the normalized Laplacian matrix.
        L = D^(-1/2) (D - A) D^(-1/2)
        where D is degree matrix and A is adjacency matrix.
        """
        n = len(matrix)
        degree_matrix = self._get_degree_matrix(matrix)
        
        # Calculate D^(-1/2)
        d_inv_sqrt = [[0.0] * n for _ in range(n)]
        for i in range(n):
            d_inv_sqrt[i][i] = 1.0 / math.sqrt(degree_matrix[i][i])
        
        # Calculate normalized Laplacian
        laplacian = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    laplacian[i][j] = 1.0
                elif matrix[i][j] != 0:
                    laplacian[i][j] = -matrix[i][j] / math.sqrt(
                        degree_matrix[i][i] * degree_matrix[j][j]
                    )
        
        return laplacian
    
    def _matrix_vector_multiply(self, matrix: List[List[float]], 
                              vector: List[float]) -> List[float]:
        """Matrix-vector multiplication."""
        n = len(matrix)
        result = [0.0] * n
        for i in range(n):
            for j in range(n):
                result[i] += matrix[i][j] * vector[j]
        return result
    
    def _normalize_vector(self, vector: List[float]) -> List[float]:
        """Normalize a vector to unit length."""
        magnitude = math.sqrt(sum(x*x for x in vector))
        if magnitude < self._epsilon:
            return [0.0] * len(vector)
        return [x/magnitude for x in vector]
    
    def _calculate_eigenvalues(self, matrix: List[List[float]]) -> List[float]:
        """
        Calculate eigenvalues using power iteration and deflation.
        Returns approximate eigenvalues sorted in descending order.
        """
        n = len(matrix)
        eigenvalues: List[float] = []
        current_matrix = [row[:] for row in matrix]
        
        for _ in range(n):
            # Find current largest eigenvalue
            vector = self._normalize_vector([1.0] * n)
            for _ in range(self._max_iterations):
                new_vector = self._matrix_vector_multiply(current_matrix, vector)
                vector = self._normalize_vector(new_vector)
            
            # Calculate Rayleigh quotient
            Av = self._matrix_vector_multiply(current_matrix, vector)
            lambda_value = sum(v * av for v, av in zip(vector, Av))
            eigenvalues.append(lambda_value)
            
            # Deflate matrix
            for i in range(n):
                for j in range(n):
                    current_matrix[i][j] -= lambda_value * vector[i] * vector[j]
        
        return sorted(eigenvalues, reverse=True)
    
    def _calculate_entropy(self, matrix: List[List[Number]]) -> float:
        """
        Calculate the von Neumann entropy using the normalized Laplacian spectrum.
        """
        laplacian = self._get_laplacian(matrix)
        eigenvalues = self._calculate_eigenvalues(laplacian)
        
        entropy = 0.0
        n = len(matrix)
        for eigenvalue in eigenvalues:
            if self._epsilon < eigenvalue < 1.0 - self._epsilon:
                p = eigenvalue / n
                entropy -= p * math.log2(p)
        
        return entropy
    
    def compute(self, matrix1: List[List[Number]], 
                         matrix2: List[List[Number]]) -> float:
        """
        Calculate the graph entropy distance between two matrices.
        
        Args:
            matrix1: First input matrix
            matrix2: Second input matrix
            
        Returns:
            Graph entropy distance between the matrices
        """
        self.validate_matrices(matrix1, matrix2)
        entropy1 = self._calculate_entropy(matrix1)
        entropy2 = self._calculate_entropy(matrix2)
        return abs(entropy1 - entropy2)
    
    @staticmethod
    def display_matrix(matrix: List[List[Number]]) -> None:
        """Display a matrix in a readable format."""
        for row in matrix:
            print([f"{x:>5.2f}" for x in row])
            
#a terminer dans les 3 examples c'est un calcul de norme!!!!!!!!!!!!!!!!!
class NuclearNormCalculator(matrixDistance):
    """
    A class to compute the Nuclear Norm of a matrix.
    The Nuclear Norm is the sum of the singular values of the matrix.
    It is often used in applications involving low-rank matrix approximations.
    """

    def __init__(self, matrix):
        """
        Initialize the calculator with the given matrix.

        :param matrix: A 2D list representing the matrix.
        """
        super().__init__()
        
        self.matrix = matrix
        self.rows = len(matrix)
        self.cols = len(matrix[0]) if matrix else 0

    def transpose(self):
        """
        Compute the transpose of the matrix.

        :return: A 2D list representing the transpose of the matrix.
        """
        return [[self.matrix[j][i] for j in range(self.rows)] for i in range(self.cols)]

    def multiply(self, mat1, mat2):
        """
        Multiply two matrices.

        :param mat1: The first matrix (2D list).
        :param mat2: The second matrix (2D list).
        :return: The product of mat1 and mat2 as a 2D list.
        """
        result = [[0] * len(mat2[0]) for _ in range(len(mat1))]
        for i in range(len(mat1)):
            for j in range(len(mat2[0])):
                for k in range(len(mat2)):
                    result[i][j] += mat1[i][k] * mat2[k][j]
        return result

    def power_iteration(self, mat, num_simulations=10):
        """
        Estimate the largest singular value of the matrix using the power iteration method.

        :param mat: The input square matrix (2D list).
        :param num_simulations: Number of iterations for the power method.
        :return: The largest singular value.
        """
        b_k = [1] * len(mat)  # Start with an initial vector
        for _ in range(num_simulations):
            # Multiply by the matrix
            b_k1 = [sum(mat[i][j] * b_k[j] for j in range(len(mat))) for i in range(len(mat))]
            # Normalize the result
            norm = sum(x**2 for x in b_k1) ** 0.5
            b_k = [x / norm for x in b_k1]
        return sum(b_k1[i] * b_k[i] for i in range(len(b_k)))

    def singular_values(self):
        """
        Compute all singular values of the matrix using SVD-like decomposition.

        :return: A list of singular values of the matrix.
        """
        mat_t = self.transpose()
        mat_ata = self.multiply(mat_t, self.matrix)  # A^T * A

        singular_values = []
        for _ in range(min(self.rows, self.cols)):
            largest_singular_value = self.power_iteration(mat_ata)
            singular_values.append(largest_singular_value ** 0.5)
            # Deflate the matrix (remove the influence of the largest singular value)
            u = [sum(self.matrix[i][j] * mat_t[j][i] for j in range(self.cols)) for i in range(self.rows)]
            u_norm = sum(x**2 for x in u) ** 0.5
            u = [x / u_norm for x in u]  # Normalize
            for i in range(self.rows):
                for j in range(self.cols):
                    self.matrix[i][j] -= largest_singular_value * u[i] * u[j]

        return singular_values

    def nuclear_norm(self):
        """
        Compute the nuclear norm of the matrix.

        :return: The nuclear norm (sum of the singular values).
        """
        return sum(self.singular_values())


class OperatorNormCalculator(matrixDistance):
    """
    A class to compute the Operator Norm (Spectral Norm) of the difference between two matrices.
    The Operator Norm is based on the largest singular value of the matrix.
    """

    def __init__(self):
        """
        Initialize the calculator with two matrices.

        :param matrix_a: The first matrix (2D list).
        :param matrix_b: The second matrix (2D list).
        """
        super().__init__()


    def validate_dimensions(self):
        """
        Ensure the matrices have the same dimensions.

        :raises ValueError: If the dimensions of the two matrices are not the same.
        """
        if len(self.matrix_a) != len(self.matrix_b) or len(self.matrix_a[0]) != len(self.matrix_b[0]):
            raise ValueError("Both matrices must have the same dimensions.")

    def matrix_difference(self,matrix_a, matrix_b):
        """
        Compute the difference between the two matrices (A - B).

        :return: A 2D list representing the matrix difference.
        """
        return [
            [
                matrix_a[i][j] - matrix_b[i][j]
                for j in range(len(matrix_a[0]))
            ]
            for i in range(len(matrix_a))
        ]

    def transpose(self, matrix):
        """
        Compute the transpose of a matrix.

        :param matrix: A 2D list representing the matrix.
        :return: A 2D list representing the transpose of the matrix.
        """
        return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

    def multiply(self, mat1, mat2):
        """
        Multiply two matrices.

        :param mat1: The first matrix (2D list).
        :param mat2: The second matrix (2D list).
        :return: The product of mat1 and mat2 as a 2D list.
        """
        result = [[0] * len(mat2[0]) for _ in range(len(mat1))]
        for i in range(len(mat1)):
            for j in range(len(mat2[0])):
                for k in range(len(mat2)):
                    result[i][j] += mat1[i][k] * mat2[k][j]
        return result

    def power_iteration(self, matrix, num_iterations=10):
        """
        Estimate the largest singular value of the matrix using the power iteration method.

        :param matrix: A square matrix (2D list).
        :param num_iterations: Number of iterations for the power method.
        :return: The largest singular value.
        """
        # Start with an initial vector (non-zero)
        b_k = [1] * len(matrix)
        for _ in range(num_iterations):
            # Multiply the matrix by the vector
            b_k1 = [sum(matrix[i][j] * b_k[j] for j in range(len(matrix))) for i in range(len(matrix))]
            # Normalize the result
            norm = sum(x**2 for x in b_k1) ** 0.5
            b_k = [x / norm for x in b_k1]
        # Compute the Rayleigh quotient to approximate the largest singular value
        return sum(b_k1[i] * b_k[i] for i in range(len(b_k)))

    def compute(self, matrix_a, matrix_b):
        """
        Compute the Operator Norm (Spectral Norm) of the difference between the two matrices.

        :return: The operator norm of the difference matrix.
        """
        difference = self.matrix_difference(matrix_a, matrix_b)
        difference_t = self.transpose(difference)
        # Compute A^T * A (difference_t * difference)
        ata = self.multiply(difference_t, difference)
        # Largest singular value is the square root of the largest eigenvalue of A^T * A
        largest_singular_value = self.power_iteration(ata)
        return largest_singular_value ** 0.5


class MaxNorm(matrixDistance):
    """
    A class to compute the maximum norm (also known as Chebyshev norm or L∞ norm) between two matrices.
    The max norm is defined as the largest absolute difference between corresponding elements.
    
    Methods
    -------
    compute(matrix1, matrix2):
        Computes the max norm between two matrices.
    validate_matrices(matrix1, matrix2):
        Validates that the input matrices have the same dimensions and are valid.
    """
    def __init__(self):
        super().__init__()
        
    @staticmethod
    def validate_matrices(matrix1, matrix2):
        """
        Validates that both input matrices have the same dimensions and are valid.
        
        Parameters
        ----------
        matrix1 : list of lists
            First input matrix
        matrix2 : list of lists
            Second input matrix
            
        Raises
        ------
        ValueError
            If matrices have different dimensions or are empty
        TypeError
            If inputs are not valid matrices (lists of lists)
        """
        # Check if inputs are lists
        if not isinstance(matrix1, list) or not isinstance(matrix2, list):
            raise TypeError("Both inputs must be lists")
            
        # Check if matrices are empty
        if not matrix1 or not matrix2:
            raise ValueError("Matrices cannot be empty")
            
        # Check if all rows are lists
        if not all(isinstance(row, list) for row in matrix1) or \
           not all(isinstance(row, list) for row in matrix2):
            raise TypeError("All rows must be lists")
            
        # Get dimensions
        rows1, cols1 = len(matrix1), len(matrix1[0])
        rows2, cols2 = len(matrix2), len(matrix2[0])
        
        # Check if dimensions match
        if rows1 != rows2 or cols1 != cols2:
            raise ValueError(f"Matrices must have same dimensions. Got {rows1}x{cols1} and {rows2}x{cols2}")
            
        # Check if all rows have same length
        if not all(len(row) == cols1 for row in matrix1) or \
           not all(len(row) == cols2 for row in matrix2):
            raise ValueError("All rows must have the same length")
    
    def compute(self, matrix1, matrix2):
        """
        Computes the max norm between two matrices.
        The max norm is the largest absolute difference between corresponding elements.
        
        Parameters
        ----------
        matrix1 : list of lists
            First input matrix
        matrix2 : list of lists
            Second input matrix
            
        Returns
        -------
        float
            The max norm between the two matrices
            
        Examples
        --------
        >>> m1 = [[1, 2], [3, 4]]
        >>> m2 = [[1, 3], [2, 5]]
        >>> max_norm = MaxNorm()
        >>> max_norm.compute(m1, m2)
        1.0  # The largest difference is |4-5| = 1
        """
        # Validate input matrices
        self.validate_matrices(matrix1, matrix2)
        
        # Initialize max difference
        max_diff = float('-inf')
        
        # Compare each element
        for i in range(len(matrix1)):
            for j in range(len(matrix1[0])):
                diff = abs(matrix1[i][j] - matrix2[i][j])
                max_diff = max(max_diff, diff)
                
        return max_diff

import math

class GaussianKernel(matrixDistance):
    """
    A class that implements the Gaussian (RBF) kernel to measure similarity between matrices.
    The Gaussian kernel is defined as: k(x,y) = exp(-||x-y||²/(2*sigma²))
    where sigma is the kernel bandwidth parameter.
    
    Attributes
    ----------
    sigma : float
        The bandwidth parameter that controls the width of the Gaussian kernel.
        Larger values make the kernel more tolerant to differences.
    
    Methods
    -------
    compute(matrix1, matrix2):
        Computes the Gaussian kernel similarity between two matrices.
    validate_matrices(matrix1, matrix2):
        Validates that the input matrices have the same dimensions and are valid.
    """
    
    def __init__(self, sigma=1.0):
        """
        Initialize the GaussianKernel with a bandwidth parameter.
        
        Parameters
        ----------
        sigma : float, optional
            The bandwidth parameter (default is 1.0)
            Must be positive
        
        Raises
        ------
        ValueError
            If sigma is not positive
        """
        super().__init__()
        
        if sigma <= 0:
            raise ValueError("Sigma must be positive")
        self.sigma = sigma
    
    @staticmethod
    def validate_matrices(matrix1, matrix2):
        """
        Validates that both input matrices have the same dimensions and are valid.
        
        Parameters
        ----------
        matrix1 : list of lists
            First input matrix
        matrix2 : list of lists
            Second input matrix
            
        Raises
        ------
        ValueError
            If matrices have different dimensions or are empty
        TypeError
            If inputs are not valid matrices (lists of lists)
        """
        if not isinstance(matrix1, list) or not isinstance(matrix2, list):
            raise TypeError("Both inputs must be lists")
            
        if not matrix1 or not matrix2:
            raise ValueError("Matrices cannot be empty")
            
        if not all(isinstance(row, list) for row in matrix1) or \
           not all(isinstance(row, list) for row in matrix2):
            raise TypeError("All rows must be lists")
            
        rows1, cols1 = len(matrix1), len(matrix1[0])
        rows2, cols2 = len(matrix2), len(matrix2[0])
        
        if rows1 != rows2 or cols1 != cols2:
            raise ValueError(f"Matrices must have same dimensions. Got {rows1}x{cols1} and {rows2}x{cols2}")
            
        if not all(len(row) == cols1 for row in matrix1) or \
           not all(len(row) == cols2 for row in matrix2):
            raise ValueError("All rows must have the same length")
    
    def compute(self, matrix1, matrix2):
        """
        Computes the Gaussian kernel similarity between two matrices.
        
        Parameters
        ----------
        matrix1 : list of lists
            First input matrix
        matrix2 : list of lists
            Second input matrix
            
        Returns
        -------
        float
            The Gaussian kernel similarity value between the two matrices.
            Values are in the range (0, 1], where:
            - 1.0 means the matrices are identical
            - Values close to 0 mean the matrices are very different
            
        Examples
        --------
        >>> m1 = [[1, 2], [3, 4]]
        >>> m2 = [[1, 2], [3, 4]]
        >>> kernel = GaussianKernel(sigma=1.0)
        >>> kernel.compute(m1, m2)
        1.0  # Matrices are identical
        
        >>> m3 = [[2, 3], [4, 5]]
        >>> kernel.compute(m1, m3)
        0.6065306597126334  # Matrices are somewhat different
        """
        # Validate input matrices
        self.validate_matrices(matrix1, matrix2)
        
        # Calculate squared Euclidean distance between matrices
        squared_diff_sum = 0
        for i in range(len(matrix1)):
            for j in range(len(matrix1[0])):
                diff = matrix1[i][j] - matrix2[i][j]
                squared_diff_sum += diff * diff
                
        # Apply Gaussian kernel formula
        return math.exp(-squared_diff_sum / (2 * self.sigma * self.sigma))

class PolynomialKernel(matrixDistance):
    """
    A class that implements the Polynomial kernel to measure similarity between matrices.
    The Polynomial kernel is defined as: k(x,y) = (scale * <x,y> + offset)^degree
    where <x,y> is the dot product between x and y.
    
    Attributes
    ----------
    degree : int
        The degree of the polynomial kernel (must be positive)
    scale : float
        The scaling factor for the dot product (must be positive)
    offset : float
        The offset term added to the scaled dot product
    
    Methods
    -------
    compute(matrix1, matrix2):
        Computes the polynomial kernel similarity between two matrices
    validate_matrices(matrix1, matrix2):
        Validates that the input matrices have the same dimensions and are valid
    """
    
    def __init__(self, degree=2, scale=1.0, offset=1.0):
        """
        Initialize the PolynomialKernel with degree, scale, and offset parameters.
        
        Parameters
        ----------
        degree : int, optional
            The degree of the polynomial (default is 2)
            Must be positive
        scale : float, optional
            The scaling factor (default is 1.0)
            Must be positive
        offset : float, optional
            The offset term (default is 1.0)
        
        Raises
        ------
        ValueError
            If degree is not positive or scale is not positive
        """
        super().__init__()
        
        if degree <= 0:
            raise ValueError("Degree must be positive")
        if scale <= 0:
            raise ValueError("Scale must be positive")
            
        self.degree = degree
        self.scale = scale
        self.offset = offset
    
    @staticmethod
    def validate_matrices(matrix1, matrix2):
        """
        Validates that both input matrices have the same dimensions and are valid.
        
        Parameters
        ----------
        matrix1 : list of lists
            First input matrix
        matrix2 : list of lists
            Second input matrix
            
        Raises
        ------
        ValueError
            If matrices have different dimensions or are empty
        TypeError
            If inputs are not valid matrices (lists of lists)
        """
        if not isinstance(matrix1, list) or not isinstance(matrix2, list):
            raise TypeError("Both inputs must be lists")
            
        if not matrix1 or not matrix2:
            raise ValueError("Matrices cannot be empty")
            
        if not all(isinstance(row, list) for row in matrix1) or \
           not all(isinstance(row, list) for row in matrix2):
            raise TypeError("All rows must be lists")
            
        rows1, cols1 = len(matrix1), len(matrix1[0])
        rows2, cols2 = len(matrix2), len(matrix2[0])
        
        if rows1 != rows2 or cols1 != cols2:
            raise ValueError(f"Matrices must have same dimensions. Got {rows1}x{cols1} and {rows2}x{cols2}")
            
        if not all(len(row) == cols1 for row in matrix1) or \
           not all(len(row) == cols2 for row in matrix2):
            raise ValueError("All rows must have the same length")
    
    def compute_dot_product(self, matrix1, matrix2):
        """
        Computes the dot product between two matrices element-wise.
        
        Parameters
        ----------
        matrix1 : list of lists
            First input matrix
        matrix2 : list of lists
            Second input matrix
            
        Returns
        -------
        float
            The dot product sum of corresponding elements
        """
        dot_product = 0
        for i in range(len(matrix1)):
            for j in range(len(matrix1[0])):
                dot_product += matrix1[i][j] * matrix2[i][j]
        return dot_product
    
    def compute(self, matrix1, matrix2):
        """
        Computes the polynomial kernel similarity between two matrices.
        
        Parameters
        ----------
        matrix1 : list of lists
            First input matrix
        matrix2 : list of lists
            Second input matrix
            
        Returns
        -------
        float
            The polynomial kernel similarity value between the two matrices
            
        Examples
        --------
        >>> m1 = [[1, 2], [3, 4]]
        >>> m2 = [[1, 2], [3, 4]]
        >>> kernel = PolynomialKernel(degree=2, scale=1.0, offset=1.0)
        >>> kernel.compute(m1, m2)
        441.0  # For identical matrices with degree=2
        """
        # Validate input matrices
        self.validate_matrices(matrix1, matrix2)
        
        # Compute dot product
        dot_product = self.compute_dot_product(matrix1, matrix2)
        
        # Apply polynomial kernel formula: (scale * <x,y> + offset)^degree
        return pow(self.scale * dot_product + self.offset, self.degree)

import math

class RBFKernel(matrixDistance):
    """
    A class that implements the Radial Basis Function (RBF) kernel to measure similarity between matrices.
    The RBF kernel is defined as: k(x,y) = exp(-gamma * ||x-y||²)
    where ||x-y||² is the squared Euclidean distance between matrices x and y.
    
    This kernel is also known as the Gaussian kernel, and it transforms the distance
    measure into a similarity score between 0 and 1.
    
    Attributes
    ----------
    gamma : float
        The kernel parameter that controls the similarity decay rate.
        Larger values make the kernel more sensitive to differences.
    
    Methods
    -------
    compute(matrix1, matrix2):
        Computes the RBF kernel similarity between two matrices.
    validate_matrices(matrix1, matrix2):
        Validates that the input matrices have the same dimensions and are valid.
    """
    
    def __init__(self, gamma=1.0):
        """
        Initialize the RBFKernel with a gamma parameter.
        
        Parameters
        ----------
        gamma : float, optional
            The kernel width parameter (default is 1.0)
            Must be positive
            - Larger values make the kernel more sensitive to differences
            - Smaller values make it more tolerant
        
        Raises
        ------
        ValueError
            If gamma is not positive
        """
        super().__init__()
        self.type='matrix_float'
        
        if gamma <= 0:
            raise ValueError("Gamma must be positive")
        self.gamma = gamma

    @staticmethod
    def validate_matrices(matrix1, matrix2):
        """
        Validates that both input matrices have the same dimensions and are valid.
        
        Parameters
        ----------
        matrix1 : list of lists
            First input matrix
        matrix2 : list of lists
            Second input matrix
            
        Raises
        ------
        ValueError
            If matrices have different dimensions or are empty
        TypeError
            If inputs are not valid matrices (lists of lists)
        """
        if not isinstance(matrix1, list) or not isinstance(matrix2, list):
            raise TypeError("Both inputs must be lists")
            
        if not matrix1 or not matrix2:
            raise ValueError("Matrices cannot be empty")
            
        if not all(isinstance(row, list) for row in matrix1) or \
           not all(isinstance(row, list) for row in matrix2):
            raise TypeError("All rows must be lists")
            
        rows1, cols1 = len(matrix1), len(matrix1[0])
        rows2, cols2 = len(matrix2), len(matrix2[0])
        
        if rows1 != rows2 or cols1 != cols2:
            raise ValueError(f"Matrices must have same dimensions. Got {rows1}x{cols1} and {rows2}x{cols2}")
            
        if not all(len(row) == cols1 for row in matrix1) or \
           not all(len(row) == cols2 for row in matrix2):
            raise ValueError("All rows must have the same length")
    
    def compute_squared_euclidean_distance(self, matrix1, matrix2):
        """
        Computes the squared Euclidean distance between two matrices.
        
        Parameters
        ----------
        matrix1 : list of lists
            First input matrix
        matrix2 : list of lists
            Second input matrix
            
        Returns
        -------
        float
            The squared Euclidean distance between the matrices
        """
        squared_distance = 0.0
        for i in range(len(matrix1)):
            for j in range(len(matrix1[0])):
                diff = matrix1[i][j] - matrix2[i][j]
                squared_distance += diff * diff
        return squared_distance
    
    def compute(self, matrix1, matrix2):
        """
        Computes the RBF kernel similarity between two matrices.
        
        Parameters
        ----------
        matrix1 : list of lists
            First input matrix
        matrix2 : list of lists
            Second input matrix
            
        Returns
        -------
        float
            The RBF kernel similarity value between the two matrices.
            Values are in the range (0, 1], where:
            - 1.0 means the matrices are identical
            - Values close to 0 mean the matrices are very different
            
        Examples
        --------
        >>> m1 = [[1, 2], [3, 4]]
        >>> m2 = [[1, 2], [3, 4]]
        >>> kernel = RBFKernel(gamma=0.5)
        >>> kernel.compute(m1, m2)
        1.0  # Matrices are identical
        
        >>> m3 = [[2, 3], [4, 5]]
        >>> kernel.compute(m1, m3)
        0.135335283236613  # Matrices are quite different
        """
        # Validate input matrices
        self.validate_matrices(matrix1, matrix2)
        
        # Compute squared Euclidean distance
        squared_distance = self.compute_squared_euclidean_distance(matrix1, matrix2)
        
        # Apply RBF formula: exp(-gamma * ||x-y||²)
        return math.exp(-self.gamma * squared_distance)

class ProcrustesDistance(matrixDistance):
    """
    A class that implements the Procrustes distance to measure similarity between matrices
    by finding the optimal transformation (rotation, scaling, and translation).
    
    The Procrustes analysis minimizes the sum of squared differences between two matrices
    by applying a series of transformations while preserving their shape properties.
    
    Methods
    -------
    compute(matrix1, matrix2):
        Computes the Procrustes distance between two matrices.
    center_matrix(matrix):
        Centers a matrix by subtracting its mean.
    compute_scale_factor(matrix):
        Computes the Frobenius norm of a matrix.
    normalize_matrix(matrix):
        Normalizes a matrix to have unit Frobenius norm.
    compute_rotation_matrix(matrix1, matrix2):
        Computes the optimal rotation matrix using SVD.
    """
    def __init__(self):
        super().__init__()
        
    @staticmethod
    def validate_matrices(matrix1, matrix2):
        """
        Validates that both input matrices have the same dimensions and are valid.
        
        Parameters
        ----------
        matrix1 : list of lists
            First input matrix
        matrix2 : list of lists
            Second input matrix
            
        Raises
        ------
        ValueError
            If matrices have different dimensions or are empty
        TypeError
            If inputs are not valid matrices
        """
        if not isinstance(matrix1, list) or not isinstance(matrix2, list):
            raise TypeError("Both inputs must be lists")
            
        if not matrix1 or not matrix2:
            raise ValueError("Matrices cannot be empty")
            
        rows1, cols1 = len(matrix1), len(matrix1[0])
        rows2, cols2 = len(matrix2), len(matrix2[0])
        
        if rows1 != rows2 or cols1 != cols2:
            raise ValueError(f"Matrices must have same dimensions. Got {rows1}x{cols1} and {rows2}x{cols2}")

    def center_matrix(self, matrix):
        """
        Centers a matrix by subtracting its mean.
        
        Parameters
        ----------
        matrix : list of lists
            Input matrix
            
        Returns
        -------
        list of lists
            Centered matrix
        float
            Mean of the original matrix elements
        """
        rows, cols = len(matrix), len(matrix[0])
        total_sum = sum(sum(row) for row in matrix)
        mean = total_sum / (rows * cols)
        
        centered = [[matrix[i][j] - mean for j in range(cols)] 
                   for i in range(rows)]
        return centered, mean

    def compute_scale_factor(self, matrix):
        """
        Computes the Frobenius norm of a matrix.
        
        Parameters
        ----------
        matrix : list of lists
            Input matrix
            
        Returns
        -------
        float
            Frobenius norm of the matrix
        """
        return sum(sum(x * x for x in row) for row in matrix) ** 0.5

    def normalize_matrix(self, matrix):
        """
        Normalizes a matrix to have unit Frobenius norm.
        
        Parameters
        ----------
        matrix : list of lists
            Input matrix
            
        Returns
        -------
        list of lists
            Normalized matrix
        float
            Scale factor used for normalization
        """
        scale = self.compute_scale_factor(matrix)
        if scale == 0:
            raise ValueError("Cannot normalize zero matrix")
            
        rows, cols = len(matrix), len(matrix[0])
        normalized = [[matrix[i][j] / scale for j in range(cols)]
                     for i in range(rows)]
        return normalized, scale

    def compute_rotation_matrix(self, matrix1, matrix2):
        """
        Computes the optimal rotation matrix using a simplified approach.
        Note: This is a simplified version without full SVD implementation.
        
        Parameters
        ----------
        matrix1, matrix2 : list of lists
            Input matrices
            
        Returns
        -------
        list of lists
            Approximate rotation matrix
        """
        # Compute cross-covariance matrix
        rows, cols = len(matrix1), len(matrix1[0])
        covariance = [[sum(matrix1[i][k] * matrix2[j][k] for k in range(cols))
                      for j in range(rows)]
                     for i in range(rows)]
        
        # Simple approximation of rotation
        # In practice, you would use SVD here
        rotation = [[1 if i == j else 0 for j in range(rows)]
                   for i in range(rows)]
        return rotation

    def compute(self, matrix1, matrix2):
        """
        Computes the Procrustes distance between two matrices.
        
        Parameters
        ----------
        matrix1, matrix2 : list of lists
            Input matrices to compare
            
        Returns
        -------
        float
            Procrustes distance between the matrices
        dict
            Transformation parameters used
            
        Examples
        --------
        >>> m1 = [[1, 2], [3, 4]]
        >>> m2 = [[2, 3], [4, 5]]
        >>> procrustes = ProcrustesDistance()
        >>> distance, params = procrustes.compute(m1, m2)
        """
        # Validate inputs
        self.validate_matrices(matrix1, matrix2)
        
        # Step 1: Center both matrices
        centered1, translation1 = self.center_matrix(matrix1)
        centered2, translation2 = self.center_matrix(matrix2)
        
        # Step 2: Normalize to unit scale
        normalized1, scale1 = self.normalize_matrix(centered1)
        normalized2, scale2 = self.normalize_matrix(centered2)
        
        # Step 3: Compute optimal rotation
        rotation = self.compute_rotation_matrix(normalized1, normalized2)
        
        # Step 4: Apply transformation and compute distance
        rows, cols = len(matrix1), len(matrix1[0])
        transformed = [[sum(rotation[i][k] * normalized1[k][j] for k in range(rows))
                       for j in range(cols)]
                      for i in range(rows)]
        
        # Compute squared differences
        squared_diff = sum(sum((transformed[i][j] - normalized2[i][j]) ** 2
                             for j in range(cols))
                         for i in range(rows))
        
        distance = squared_diff ** 0.5
        
        # Return distance and transformation parameters
        params = {
            'translation1': translation1,
            'translation2': translation2,
            'scale1': scale1,
            'scale2': scale2,
            'rotation': rotation
        }
        
        return distance#, params
import math

class SubspaceDistance(matrixDistance):
    """
    A class that implements subspace distance computation between matrices.
    The subspace distance measures how similar the vector spaces spanned by two matrices are.
    This implementation uses a simplified approach to SVD for pedagogical purposes.
    
    Methods
    -------
    compute(matrix1, matrix2):
        Computes the subspace distance between two matrices
    gram_schmidt(matrix):
        Performs Gram-Schmidt orthogonalization
    matrix_multiply(matrix1, matrix2):
        Multiplies two matrices
    matrix_transpose(matrix):
        Computes the transpose of a matrix
    """
    
    def __init__(self, tolerance=1e-10):
        """
        Initialize the SubspaceDistance calculator.
        
        Parameters
        ----------
        tolerance : float
            Numerical tolerance for zero comparisons
        """
        super().__init__()
        
        self.tolerance = tolerance
    
    @staticmethod
    def validate_matrices(matrix1, matrix2):
        """
        Validates input matrices.
        
        Parameters
        ----------
        matrix1, matrix2 : list of lists
            Input matrices to compare
            
        Raises
        ------
        ValueError
            If matrices are invalid or empty
        """
        if not matrix1 or not matrix2:
            raise ValueError("Matrices cannot be empty")
            
        if not all(isinstance(row, list) for row in matrix1) or \
           not all(isinstance(row, list) for row in matrix2):
            raise TypeError("Inputs must be lists of lists")
            
        if not all(len(row) == len(matrix1[0]) for row in matrix1) or \
           not all(len(row) == len(matrix2[0]) for row in matrix2):
            raise ValueError("All rows must have the same length within each matrix")

    def vector_dot_product(self, vec1, vec2):
        """
        Computes dot product of two vectors.
        
        Parameters
        ----------
        vec1, vec2 : list
            Input vectors
            
        Returns
        -------
        float
            Dot product
        """
        return sum(a * b for a, b in zip(vec1, vec2))

    def vector_scale(self, vector, scalar):
        """
        Scales a vector by a scalar.
        
        Parameters
        ----------
        vector : list
            Input vector
        scalar : float
            Scaling factor
            
        Returns
        -------
        list
            Scaled vector
        """
        return [scalar * x for x in vector]

    def vector_subtract(self, vec1, vec2):
        """
        Subtracts two vectors.
        
        Parameters
        ----------
        vec1, vec2 : list
            Input vectors
            
        Returns
        -------
        list
            Result of vec1 - vec2
        """
        return [a - b for a, b in zip(vec1, vec2)]

    def vector_norm(self, vector):
        """
        Computes the Euclidean norm of a vector.
        
        Parameters
        ----------
        vector : list
            Input vector
            
        Returns
        -------
        float
            Euclidean norm
        """
        return math.sqrt(sum(x * x for x in vector))

    def gram_schmidt(self, matrix):
        """
        Performs Gram-Schmidt orthogonalization.
        
        Parameters
        ----------
        matrix : list of lists
            Input matrix
            
        Returns
        -------
        list of lists
            Orthonormalized matrix
        """
        vectors = [row[:] for row in matrix]  # Copy input matrix
        orthogonal = []
        
        for i, vector in enumerate(vectors):
            for basis in orthogonal:
                # Project vector onto basis and subtract
                projection = self.vector_scale(
                    basis,
                    self.vector_dot_product(vector, basis)
                )
                vector = self.vector_subtract(vector, projection)
            
            # Normalize if vector is not zero
            norm = self.vector_norm(vector)
            if norm > self.tolerance:
                orthogonal.append([x / norm for x in vector])
        
        return orthogonal

    def matrix_multiply(self, matrix1, matrix2):
        """
        Multiplies two matrices.
        
        Parameters
        ----------
        matrix1, matrix2 : list of lists
            Input matrices
            
        Returns
        -------
        list of lists
            Product matrix
        """
        if not matrix1 or not matrix2 or not matrix1[0]:
            return []
            
        n, m = len(matrix1), len(matrix1[0])
        p = len(matrix2[0]) if matrix2 else 0
        
        result = [[0] * p for _ in range(n)]
        for i in range(n):
            for j in range(p):
                result[i][j] = sum(matrix1[i][k] * matrix2[k][j] 
                                 for k in range(m))
        return result

    def matrix_transpose(self, matrix):
        """
        Computes matrix transpose.
        
        Parameters
        ----------
        matrix : list of lists
            Input matrix
            
        Returns
        -------
        list of lists
            Transposed matrix
        """
        if not matrix or not matrix[0]:
            return []
        return [[matrix[j][i] for j in range(len(matrix))]
                for i in range(len(matrix[0]))]

    def compute(self, matrix1, matrix2):
        """
        Computes the subspace distance between two matrices.
        
        Parameters
        ----------
        matrix1, matrix2 : list of lists
            Input matrices
            
        Returns
        -------
        float
            Subspace distance between the matrices
        dict
            Additional information about the computation
            
        Examples
        --------
        >>> m1 = [[1, 0], [0, 1]]
        >>> m2 = [[0.707, -0.707], [0.707, 0.707]]
        >>> subspace = SubspaceDistance()
        >>> distance, info = subspace.compute(m1, m2)
        """
        # Validate inputs
        self.validate_matrices(matrix1, matrix2)
        
        # Orthonormalize both matrices
        Q1 = self.gram_schmidt(matrix1)
        Q2 = self.gram_schmidt(matrix2)
        
        # Compute projection matrices
        P1 = self.matrix_multiply(Q1, self.matrix_transpose(Q1))
        P2 = self.matrix_multiply(Q2, self.matrix_transpose(Q2))
        
        # Compute difference of projections
        diff_matrix = [[P1[i][j] - P2[i][j] 
                       for j in range(len(P1[0]))]
                      for i in range(len(P1))]
        
        # Compute Frobenius norm of difference
        squared_sum = sum(sum(x * x for x in row)
                         for row in diff_matrix)
        distance = math.sqrt(squared_sum) / 2  # Divide by 2 for normalization
        
        info = {
            'Q1': Q1,
            'Q2': Q2,
            'P1': P1,
            'P2': P2,
            'diff_matrix': diff_matrix
        }
        
        return distance#, info
        

        
class LogDetDivergence(matrixDistance):
    """
    A class to compute the Log-Determinant Divergence between two positive semi-definite matrices.
    
    The Log-Determinant Divergence (also known as Stein's loss) between two positive
    semi-definite matrices P and Q is defined as:
    D(P||Q) = tr(PQ^(-1)) - log(det(PQ^(-1))) - n
    
    where:
    - tr() is the trace of a matrix
    - det() is the determinant
    - n is the dimension of the matrices
    """
    
    def __init__(self):
        """Initialize the LogDetDivergence calculator."""
        super().__init__()
        self.type='matrix_float'
    
    def _check_matrix_validity(self, matrix):
        """
        Check if the input matrix is valid (square and symmetric).
        
        Args:
            matrix (list of lists): Input matrix to check
            
        Returns:
            bool: True if matrix is valid, False otherwise
        
        Raises:
            ValueError: If matrix is not square or symmetric
        """
        if not matrix or not matrix[0]:
            raise ValueError("Empty matrix provided")
            
        n = len(matrix)
        if not all(len(row) == n for row in matrix):
            raise ValueError("Matrix must be square")
            
        # Check symmetry
        for i in range(n):
            for j in range(i + 1, n):
                if abs(matrix[i][j] - matrix[j][i]) > 1e-10:
                    raise ValueError("Matrix must be symmetric")
        
        return True
    
    def _compute_determinant(self, matrix):
        """
        Compute the determinant of a matrix using LU decomposition.
        
        Args:
            matrix (list of lists): Input matrix
            
        Returns:
            float: Determinant of the matrix
        """
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
            
        # Create a copy of the matrix to avoid modifying the original
        mat = [row[:] for row in matrix]
        det = 1.0
        
        for i in range(n):
            # Find pivot
            pivot = mat[i][i]
            if abs(pivot) < 1e-10:
                raise ValueError("Matrix is singular or not positive definite")
            
            det *= pivot
            
            # Eliminate entries below pivot
            for j in range(i + 1, n):
                factor = mat[j][i] / pivot
                for k in range(i, n):
                    mat[j][k] -= factor * mat[i][k]
        
        return det
    
    def _compute_inverse(self, matrix):
        """
        Compute the inverse of a matrix using Gauss-Jordan elimination.
        
        Args:
            matrix (list of lists): Input matrix
            
        Returns:
            list of lists: Inverse of the input matrix
        """
        n = len(matrix)
        # Augment matrix with identity matrix
        aug = [row[:] + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)]
        
        # Forward elimination
        for i in range(n):
            pivot = aug[i][i]
            if abs(pivot) < 1e-10:
                raise ValueError("Matrix is singular or not positive definite")
            
            for j in range(i, 2*n):
                aug[i][j] /= pivot
                
            for j in range(n):
                if i != j:
                    factor = aug[j][i]
                    for k in range(i, 2*n):
                        aug[j][k] -= factor * aug[i][k]
        
        # Extract inverse from augmented matrix
        inverse = [row[n:] for row in aug]
        return inverse
    
    def _compute_trace(self, matrix):
        """
        Compute the trace of a matrix (sum of diagonal elements).
        
        Args:
            matrix (list of lists): Input matrix
            
        Returns:
            float: Trace of the matrix
        """
        return sum(matrix[i][i] for i in range(len(matrix)))
    
    def _matrix_multiply(self, A, B):
        """
        Multiply two matrices.
        
        Args:
            A (list of lists): First matrix
            B (list of lists): Second matrix
            
        Returns:
            list of lists: Result of matrix multiplication
        """
        n = len(A)
        result = [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
        return result
    
    def compute(self, P, Q):
        """
        Compute the Log-Determinant Divergence between matrices P and Q.
        
        Args:
            P (list of lists): First positive semi-definite matrix
            Q (list of lists): Second positive semi-definite matrix
            
        Returns:
            float: Log-Determinant Divergence between P and Q
            
        Raises:
            ValueError: If matrices are not valid or not positive semi-definite
        """
        # Validate inputs
        self._check_matrix_validity(P)
        self._check_matrix_validity(Q)
        
        n = len(P)
        
        # Compute Q inverse
        Q_inv = self._compute_inverse(Q)
        
        # Compute PQ^(-1)
        PQ_inv = self._matrix_multiply(P, Q_inv)
        
        # Compute trace(PQ^(-1))
        trace_term = self._compute_trace(PQ_inv)
        
        # Compute log(det(PQ^(-1)))
        det_P = self._compute_determinant(P)
        det_Q = self._compute_determinant(Q)
        log_det_term = abs(det_P / det_Q)
        
        if log_det_term <= 0:
            raise ValueError("Matrices must be positive definite")
            
        log_det_term = math.log(log_det_term)
        
        # Compute final divergence
        divergence = trace_term - log_det_term - n
        
        return divergence
        
class EnergyDistanceMatrix(matrixDistance):#nom rajouter matrix car classe energiedistance existe dans sound distance
    """
    A class to compute the Energy Distance between two matrices.
    
    The Energy Distance is a statistical distance between two probability distributions.
    For matrices A and B with same dimensions m×n, it is defined as:
    
    D(A,B) = (2/m^2) * sum(||A_i - B_j||) - (1/m^2) * sum(||A_i - A_j||) 
             - (1/m^2) * sum(||B_i - B_j||)
             
    where:
    - ||.|| denotes the Euclidean norm
    - A_i, B_j are rows of matrices A and B respectively
    - Both matrices must have the same number of rows (m) and columns (n)
    """
    def __init__(self):
        super().__init__()
        
    def _vector_energy(self, vector):
        """
        Compute the energy of a vector.
        
        Args:
            vector (list): Input vector
            
        Returns:
            float: Energy of the vector
        """
        return sum(x * x for x in vector)  # Sum of squared components
    
    def _euclidean_norm(self, vector1, vector2):
        """
        Compute the Euclidean norm between two vectors.
        
        Args:
            vector1 (list): First vector
            vector2 (list): Second vector
            
        Returns:
            float: Euclidean distance between the vectors
            
        Raises:
            ValueError: If vectors have different dimensions
        """
        if len(vector1) != len(vector2):
            raise ValueError("Vectors must have the same dimension")
            
        return sum((a - b) ** 2 for a, b in zip(vector1, vector2)) ** 0.5
    
    def _validate_matrices(self, A, B):
        """
        Validate that input matrices have the same dimensions.
        
        Args:
            A (list of lists): First matrix
            B (list of lists): Second matrix
            
        Returns:
            tuple: Number of rows (m) and columns (n)
            
        Raises:
            ValueError: If matrices are empty or have different dimensions
        """
        if not A or not B or not A[0] or not B[0]:
            raise ValueError("Empty matrix provided")
            
        m1, m2 = len(A), len(B)
        n1, n2 = len(A[0]), len(B[0])
        
        if m1 != m2:
            raise ValueError("Matrices must have the same number of rows")
            
        if n1 != n2:
            raise ValueError("Matrices must have the same number of columns")
            
        if not all(len(row) == n1 for row in A):
            raise ValueError("Inconsistent row lengths in first matrix")
            
        if not all(len(row) == n2 for row in B):
            raise ValueError("Inconsistent row lengths in second matrix")
            
        return m1, n1
    
    def _compute_pairwise_distances(self, X):
        """
        Compute all pairwise distances within a matrix.
        
        Args:
            X (list of lists): Input matrix
            
        Returns:
            list: List of all pairwise distances
        """
        distances = []
        n = len(X)
        
        for i in range(n):
            for j in range(i + 1, n):
                distances.append(self._euclidean_norm(X[i], X[j]))
                
        return distances
    
    def _compute_between_distances(self, A, B):
        """
        Compute all pairwise distances between two matrices.
        
        Args:
            A (list of lists): First matrix
            B (list of lists): Second matrix
            
        Returns:
            list: List of all pairwise distances between A and B
        """
        distances = []
        
        for row_a in A:
            for row_b in B:
                distances.append(self._euclidean_norm(row_a, row_b))
                
        return distances
    
    def compute(self, A, B):
        """
        Compute the Energy Distance between matrices A and B.
        
        Args:
            A (list of lists): First matrix
            B (list of lists): Second matrix
            
        Returns:
            float: Energy Distance between A and B
            
        Raises:
            ValueError: If matrices have different dimensions
        """
        # Validate inputs
        m, n = self._validate_matrices(A, B)
        
        # Compute between-matrices distances
        between_distances = self._compute_between_distances(A, B)
        between_term = 2 * sum(between_distances) / (m * m)
        
        # Compute within-matrix distances for A
        within_A_distances = self._compute_pairwise_distances(A)
        within_A_term = sum(within_A_distances) * 2 / (m * m)  # multiply by 2 because we only computed upper triangle
        
        # Compute within-matrix distances for B
        within_B_distances = self._compute_pairwise_distances(B)
        within_B_term = sum(within_B_distances) * 2 / (m * m)  # multiply by 2 because we only computed upper triangle
        
        # Compute final energy distance
        energy_distance = between_term - within_A_term - within_B_term
        
        return abs(energy_distance)  # Return absolute value as distance should be non-negative
    
    def compute_matrix_energy(self, X):
        """
        Compute the total energy of a matrix.
        
        Args:
            X (list of lists): Input matrix
            
        Returns:
            float: Total energy of the matrix
        """
        return sum(self._vector_energy(row) for row in X)

    def normalize(self, distance, A, B):
        """
        Normalize the Energy Distance by the dimensions of the matrices.
        
        Args:
            distance (float): Computed Energy Distance
            A (list of lists): First matrix
            B (list of lists): Second matrix
            
        Returns:
            float: Normalized Energy Distance
        """
        m, _ = self._validate_matrices(A, B)
        energy_A = self.compute_matrix_energy(A)
        energy_B = self.compute_matrix_energy(B)
        normalization_factor = (energy_A * energy_B) ** 0.5
        return distance / (normalization_factor if normalization_factor > 0 else 1.0)

class NMFComparator(matrixDistance):
    """
    A class to compare matrices using Non-negative Matrix Factorization (NMF).
    NMF decomposes a matrix V into two matrices W and H where V ≈ WH,
    with the constraint that all elements in W and H are non-negative.
    
    The comparison is based on the reconstruction error and the learned features
    between two matrices after their respective factorizations.
    """
    
    def __init__(self, n_components=2, max_iter=200, tolerance=1e-4):
        """
        Initialize NMF comparator.
        
        Args:
            n_components (int): Number of components for factorization
            max_iter (int): Maximum number of iterations for optimization
            tolerance (float): Convergence tolerance
        """
        super().__init__()
        
        self.n_components = n_components
        self.max_iter = max_iter
        self.tolerance = tolerance
    
    def _validate_non_negative(self, matrix, name="Matrix"):
        """
        Validate that a matrix contains only non-negative values.
        
        Args:
            matrix (list of lists): Input matrix
            name (str): Name of matrix for error message
            
        Raises:
            ValueError: If matrix contains negative values
        """
        if any(any(x < 0 for x in row) for row in matrix):
            raise ValueError(f"{name} must contain only non-negative values")
    
    def _initialize_factors(self, n_rows, n_cols):
        """
        Initialize W and H matrices with random values.
        
        Args:
            n_rows (int): Number of rows in the input matrix
            n_cols (int): Number of columns in the input matrix
            
        Returns:
            tuple: (W, H) initialized matrices
        """
        import random
        random.seed(42)  # For reproducibility
        
        W = [[random.random() for _ in range(self.n_components)] 
             for _ in range(n_rows)]
        
        H = [[random.random() for _ in range(n_cols)] 
             for _ in range(self.n_components)]
        
        return W, H
    
    def _multiply_matrices(self, A, B):
        """
        Multiply two matrices.
        
        Args:
            A (list of lists): First matrix
            B (list of lists): Second matrix
            
        Returns:
            list of lists: Result of matrix multiplication
        """
        n_rows = len(A)
        n_cols = len(B[0])
        n_inner = len(B)
        
        result = [[0 for _ in range(n_cols)] for _ in range(n_rows)]
        
        for i in range(n_rows):
            for j in range(n_cols):
                result[i][j] = sum(A[i][k] * B[k][j] for k in range(n_inner))
                
        return result
    
    def _frobenius_norm(self, matrix):
        """
        Compute the Frobenius norm of a matrix.
        
        Args:
            matrix (list of lists): Input matrix
            
        Returns:
            float: Frobenius norm
        """
        return sum(sum(x * x for x in row) for row in matrix) ** 0.5
    
    def _subtract_matrices(self, A, B):
        """
        Subtract matrix B from matrix A.
        
        Args:
            A (list of lists): First matrix
            B (list of lists): Second matrix
            
        Returns:
            list of lists: Result of A - B
        """
        return [[A[i][j] - B[i][j] 
                for j in range(len(A[0]))] 
                for i in range(len(A))]
    
    def _update_W(self, V, W, H):
        """
        Update matrix W using multiplicative update rules.
        
        Args:
            V (list of lists): Target matrix
            W (list of lists): Current W matrix
            H (list of lists): Current H matrix
            
        Returns:
            list of lists: Updated W matrix
        """
        numerator = self._multiply_matrices(V, [list(x) for x in zip(*H)])
        denominator = self._multiply_matrices(
            self._multiply_matrices(W, H), 
            [list(x) for x in zip(*H)]
        )
        
        return [[W[i][j] * numerator[i][j] / (denominator[i][j] + 1e-10)
                for j in range(len(W[0]))]
                for i in range(len(W))]
    
    def _update_H(self, V, W, H):
        """
        Update matrix H using multiplicative update rules.
        
        Args:
            V (list of lists): Target matrix
            W (list of lists): Current W matrix
            H (list of lists): Current H matrix
            
        Returns:
            list of lists: Updated H matrix
        """
        W_transpose = [list(x) for x in zip(*W)]
        numerator = self._multiply_matrices(W_transpose, V)
        denominator = self._multiply_matrices(
            W_transpose,
            self._multiply_matrices(W, H)
        )
        
        return [[H[i][j] * numerator[i][j] / (denominator[i][j] + 1e-10)
                for j in range(len(H[0]))]
                for i in range(len(H))]
    
    def factorize(self, V):
        """
        Perform NMF on input matrix V.
        
        Args:
            V (list of lists): Input matrix to factorize
            
        Returns:
            tuple: (W, H) factorized matrices and final reconstruction error
        """
        self._validate_non_negative(V)
        
        n_rows, n_cols = len(V), len(V[0])
        W, H = self._initialize_factors(n_rows, n_cols)
        
        prev_error = float('inf')
        
        for _ in range(self.max_iter):
            # Update W and H matrices
            W = self._update_W(V, W, H)
            H = self._update_H(V, W, H)
            
            # Compute reconstruction error
            reconstruction = self._multiply_matrices(W, H)
            error = self._frobenius_norm(
                self._subtract_matrices(V, reconstruction)
            )
            
            # Check convergence
            if abs(prev_error - error) < self.tolerance:
                break
                
            prev_error = error
        
        return W, H, error
    
    def compute(self, matrix1, matrix2):
        """
        Compare two matrices using their NMF decompositions.
        
        Args:
            matrix1 (list of lists): First matrix
            matrix2 (list of lists): Second matrix
            
        Returns:
            dict: Comparison metrics including reconstruction errors and similarity
        """
        # Perform NMF on both matrices
        W1, H1, error1 = self.factorize(matrix1)
        W2, H2, error2 = self.factorize(matrix2)
        
        # Compute feature similarity between W matrices
        W1_norm = self._frobenius_norm(W1)
        W2_norm = self._frobenius_norm(W2)
        
        # Normalize and compare feature matrices
        feature_similarity = 1.0 - (
            self._frobenius_norm(self._subtract_matrices(W1, W2)) /
            (W1_norm + W2_norm + 1e-10)
        )
        return feature_similarity
        '''ok but juste float 
        return {
            'reconstruction_error_1': error1,
            'reconstruction_error_2': error2,
            'feature_similarity': feature_similarity,
            'factors_1': (W1, H1),
            'factors_2': (W2, H2)
        }'''
        
class PCAComparator(matrixDistance):
    """
    A class to compare matrices using Principal Component Analysis (PCA).
    
    This comparator transforms matrices into their principal components and
    measures the distance between them in the reduced space. The comparison
    takes into account both the eigenvalues (explained variance) and
    eigenvectors (principal directions).
    """
    
    def __init__(self, n_components=None, tolerance=1e-10, max_iter=100):
        """
        Initialize the PCA comparator.
        
        Args:
            n_components (int): Number of principal components to use
            tolerance (float): Convergence tolerance for eigenvalue computation
            max_iter (int): Maximum iterations for power iteration method
        """
        super().__init__()
        
        self.n_components = n_components
        self.tolerance = tolerance
        self.max_iter = max_iter
    
    def _center_matrix(self, matrix):
        """
        Center the matrix by subtracting the mean of each column.
        
        Args:
            matrix (list of lists): Input matrix
            
        Returns:
            tuple: (centered matrix, column means)
        """
        n_rows = len(matrix)
        n_cols = len(matrix[0])
        
        # Compute column means
        col_means = [sum(matrix[i][j] for i in range(n_rows)) / n_rows 
                    for j in range(n_cols)]
        
        # Center the matrix
        centered = [[matrix[i][j] - col_means[j] 
                    for j in range(n_cols)] 
                    for i in range(n_rows)]
        
        return centered, col_means
    
    def _matrix_multiply(self, A, B):
        """
        Multiply two matrices.
        
        Args:
            A (list of lists): First matrix
            B (list of lists): Second matrix
            
        Returns:
            list of lists: Result of matrix multiplication
        """
        n_rows_A = len(A)
        n_cols_B = len(B[0])
        n_inner = len(B)
        
        result = [[sum(A[i][k] * B[k][j] 
                      for k in range(n_inner))
                  for j in range(n_cols_B)]
                  for i in range(n_rows_A)]
        
        return result
    
    def _transpose(self, matrix):
        """
        Transpose a matrix.
        
        Args:
            matrix (list of lists): Input matrix
            
        Returns:
            list of lists: Transposed matrix
        """
        return [list(row) for row in zip(*matrix)]
    
    def _covariance_matrix(self, matrix):
        """
        Compute the covariance matrix.
        
        Args:
            matrix (list of lists): Input centered matrix
            
        Returns:
            list of lists: Covariance matrix
        """
        n_rows = len(matrix)
        matrix_t = self._transpose(matrix)
        
        # Compute covariance matrix
        cov = self._matrix_multiply(matrix_t, matrix)
        
        # Normalize by (n-1)
        for i in range(len(cov)):
            for j in range(len(cov)):
                cov[i][j] /= (n_rows - 1)
        
        return cov
    
    def _normalize_vector(self, vector):
        """
        Normalize a vector to unit length.
        
        Args:
            vector (list): Input vector
            
        Returns:
            list: Normalized vector
        """
        norm = sum(x * x for x in vector) ** 0.5
        return [x / norm if norm > self.tolerance else 0 for x in vector]
    
    def _power_iteration(self, matrix):
        """
        Compute the dominant eigenvalue and eigenvector using power iteration.
        
        Args:
            matrix (list of lists): Input matrix
            
        Returns:
            tuple: (eigenvalue, eigenvector)
        """
        n = len(matrix)
        vector = self._normalize_vector([1 if i == 0 else 0 for i in range(n)])
        
        for _ in range(self.max_iter):
            # Multiply matrix by vector
            new_vector = [sum(matrix[i][j] * vector[j] 
                            for j in range(n))
                        for i in range(n)]
            
            # Normalize
            new_vector = self._normalize_vector(new_vector)
            
            # Check convergence
            if all(abs(v1 - v2) < self.tolerance 
                   for v1, v2 in zip(vector, new_vector)):
                break
                
            vector = new_vector
        
        # Compute eigenvalue (Rayleigh quotient)
        eigenvalue = sum(sum(vector[i] * matrix[i][j] * vector[j]
                           for j in range(n))
                       for i in range(n))
        
        return eigenvalue, vector
    
    def _deflate_matrix(self, matrix, eigenvalue, eigenvector):
        """
        Deflate matrix by removing the contribution of an eigenvector.
        
        Args:
            matrix (list of lists): Input matrix
            eigenvalue (float): Eigenvalue
            eigenvector (list): Eigenvector
            
        Returns:
            list of lists: Deflated matrix
        """
        n = len(matrix)
        deflated = [[matrix[i][j] - eigenvalue * eigenvector[i] * eigenvector[j]
                    for j in range(n)]
                    for i in range(n)]
        return deflated
    
    def compute_pca(self, matrix):
        """
        Compute PCA of a matrix.
        
        Args:
            matrix (list of lists): Input matrix
            
        Returns:
            tuple: (eigenvalues, eigenvectors, centered_matrix)
        """
        # Center the matrix
        centered, _ = self._center_matrix(matrix)
        
        # Compute covariance matrix
        cov_matrix = self._covariance_matrix(centered)
        
        # Initialize results
        n_comp = self.n_components or len(cov_matrix)
        eigenvalues = []
        eigenvectors = []
        
        # Compute eigenvalues and eigenvectors
        current_matrix = [row[:] for row in cov_matrix]
        
        for _ in range(n_comp):
            eigenvalue, eigenvector = self._power_iteration(current_matrix)
            
            if eigenvalue < self.tolerance:
                break
                
            eigenvalues.append(eigenvalue)
            eigenvectors.append(eigenvector)
            
            # Deflate matrix
            current_matrix = self._deflate_matrix(
                current_matrix, eigenvalue, eigenvector
            )
        
        return eigenvalues, eigenvectors, centered
    
    def compute(self, matrix1, matrix2):
        """
        Compare two matrices using their principal components.
        
        Args:
            matrix1 (list of lists): First matrix
            matrix2 (list of lists): Second matrix
            
        Returns:
            dict: Comparison metrics including:
                - eigenvalue_distances
                - eigenvector_similarities
                - total_distance
        """
        # Compute PCA for both matrices
        evals1, evecs1, _ = self.compute_pca(matrix1)
        evals2, evecs2, _ = self.compute_pca(matrix2)
        
        # Match components by similarity
        n_comp = min(len(evals1), len(evals2))
        
        # Compute eigenvalue distances
        eval_distances = [abs(ev1 - ev2) / (ev1 + ev2 + self.tolerance)
                        for ev1, ev2 in zip(evals1[:n_comp], evals2[:n_comp])]
        
        # Compute eigenvector similarities (absolute cosine similarity)
        evec_similarities = []
        for i in range(n_comp):
            dot_product = abs(sum(v1 * v2 for v1, v2 
                                in zip(evecs1[i], evecs2[i])))
            evec_similarities.append(dot_product)
        
        # Compute total distance as weighted sum
        total_distance = sum(d * (1 - s) 
                           for d, s in zip(eval_distances, evec_similarities))
        return total_distance
        '''ok but juste distance return {
            'eigenvalue_distances': eval_distances,
            'eigenvector_similarities': evec_similarities,
            'total_distance': total_distance,
            'n_components_compared': n_comp
        }'''

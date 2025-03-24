import cython
from .mainClass import Distance
from .vectorDistance  import Euclidean

cdef class DynamicTimeWarping(Distance):
    # Attributs de classe
    cdef object _dtw_distance
    cdef object _distance_matrix
    cdef object _series_b
    cdef object _series_a
    cdef object _type

    def __init__(self, *args, **kwargs):
        '
		Compute the Dynamic Time Warping (DTW) distance between two time series.
    
		DTW is a measure of similarity between two temporal sequences that may vary in speed.
		This class allows the computation of the DTW distance and the optimal alignment path between the sequences.
    
		Attributes:
		series_a (list or array): First time series.
		series_b (list or array): Second time series.
		distance_matrix (2D list): The accumulated cost matrix used to compute the DTW distance.
		dtw_distance (float): The computed DTW distance between series_a and series_b.
		'
        super().__init__()
        self._type = 'vec_float'

    def compute(self, series_a, series_b):
        '
		Compute the DTW distance between the two time series.
        
		Returns:
			float: The DTW distance.
		'
        self._series_a = series_a
        self._series_b = series_b
        self._distance_matrix = None
        self._dtw_distance = None
        n = len(self._series_a)
        m = len(self._series_b)
        self._distance_matrix = [([float('inf')] * m) for _ in range(n)]
        self._distance_matrix[0][0] = 0
        for i in range(1, n):
            for j in range(1, m):
                cost = abs((self._series_a[i] - self._series_b[j]))
                self._distance_matrix[i][j] = (cost + min(self._distance_matrix[(i - 1)][j], self._distance_matrix[i][(j - 1)], self._distance_matrix[(i - 1)][(j - 1)]))
        self._dtw_distance = self._distance_matrix[(- 1)][(- 1)]
        return self._dtw_distance

    def get_optimal_path(self):
        '
		Retrieve the optimal path that aligns the two time series with the minimum cost.
        
		Returns:
			list of tuples: The optimal path as a list of index pairs (i, j).
		'
        (i, j) = ((len(self._series_a) - 1), (len(self._series_b) - 1))
        path = [(i, j)]
        while ((i > 0) and (j > 0)):
            if (i == 0):
                j -= 1
            elif (j == 0):
                i -= 1
            else:
                step = min(self._distance_matrix[(i - 1)][j], self._distance_matrix[i][(j - 1)], self._distance_matrix[(i - 1)][(j - 1)])
                if (step == self._distance_matrix[(i - 1)][(j - 1)]):
                    i -= 1
                    j -= 1
                elif (step == self._distance_matrix[(i - 1)][j]):
                    i -= 1
                else:
                    j -= 1
                path.append((i, j))
        path.reverse()
        return path


    # Propriétés pour accéder aux attributs depuis Python
    @property
    def dtw_distance(self):
        return self._dtw_distance
    @dtw_distance.setter
    def dtw_distance(self, value):
        self._dtw_distance = value
    @property
    def distance_matrix(self):
        return self._distance_matrix
    @distance_matrix.setter
    def distance_matrix(self, value):
        self._distance_matrix = value
    @property
    def series_b(self):
        return self._series_b
    @series_b.setter
    def series_b(self, value):
        self._series_b = value
    @property
    def series_a(self):
        return self._series_a
    @series_a.setter
    def series_a(self, value):
        self._series_a = value
    @property
    def type(self):
        return self._type
    @type.setter
    def type(self, value):
        self._type = value
	def __init__(self)-> None:
		"""
		Compute the Dynamic Time Warping (DTW) distance between two time series.
    
		DTW is a measure of similarity between two temporal sequences that may vary in speed.
		This class allows the computation of the DTW distance and the optimal alignment path between the sequences.
    
		Attributes:
		series_a (list or array): First time series.
		series_b (list or array): Second time series.
		distance_matrix (2D list): The accumulated cost matrix used to compute the DTW distance.
		dtw_distance (float): The computed DTW distance between series_a and series_b.
		"""
		super().__init__()
		self.type='vec_float'

	def compute(self, series_a, series_b):
		"""
		Compute the DTW distance between the two time series.
        
		Returns:
			float: The DTW distance.
		"""
		self.series_a = series_a
		self.series_b = series_b
		self.distance_matrix = None
		self.dtw_distance = None
        
		n = len(self.series_a)
		m = len(self.series_b)
		self.distance_matrix = [[float('inf')] * m for _ in range(n)]
		self.distance_matrix[0][0] = 0
        
		for i in range(1, n):
			for j in range(1, m):
				cost = abs(self.series_a[i] - self.series_b[j])
				self.distance_matrix[i][j] = cost + min(self.distance_matrix[i-1][j],    # Insertion
						self.distance_matrix[i][j-1],    # Deletion
						self.distance_matrix[i-1][j-1])  # Match

		self.dtw_distance = self.distance_matrix[-1][-1]
		return self.dtw_distance

	def get_optimal_path(self):
		"""
		Retrieve the optimal path that aligns the two time series with the minimum cost.
        
		Returns:
			list of tuples: The optimal path as a list of index pairs (i, j).
		"""
		i, j = len(self.series_a) - 1, len(self.series_b) - 1
		path = [(i, j)]
        
		while i > 0 and j > 0:
			if i == 0:
				j -= 1
			elif j == 0:
				i -= 1
			else:
				step = min(self.distance_matrix[i-1][j], self.distance_matrix[i][j-1], self.distance_matrix[i-1][j-1])
                
				if step == self.distance_matrix[i-1][j-1]:
					i -= 1
					j -= 1
				elif step == self.distance_matrix[i-1][j]:
					i -= 1
				else:
					j -= 1
            
				path.append((i, j))
        
		path.reverse()
		return path

from typing import List

##########################
cdef class LongestCommonSubsequence(Distance):
    # Attributs de classe
    cdef object _compute
    cdef object ___class__
    cdef object _obj1_exemple
    cdef object __backtrack_lcs
    cdef object _type
    cdef object __lcs_matrix
    cdef object _obj2_exemple

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._type = 'vec_str'
        '
		A class to compute the Longest Common Subsequence (LCS) between two text files.
		'

    def _lcs_matrix(self, text1: str, text2: str) -> List[List[int]]:
        '
		Constructs the LCS matrix for two input texts.
        
		:param text1: The first text as a string.
		:param text2: The second text as a string.
		:return: A 2D list (matrix) containing the lengths of LCS for substrings of text1 and text2.
		'
        len1: int = len(text1)
        len2: int = len(text2)
        lcs_matrix: List[List[int]] = [([0] * (len2 + 1)) for _ in range((len1 + 1))]
        for i in range(1, (len1 + 1)):
            for j in range(1, (len2 + 1)):
                if (text1[(i - 1)] == text2[(j - 1)]):
                    lcs_matrix[i][j] = (lcs_matrix[(i - 1)][(j - 1)] + 1)
                else:
                    lcs_matrix[i][j] = max(lcs_matrix[(i - 1)][j], lcs_matrix[i][(j - 1)])
        return lcs_matrix

    def _backtrack_lcs(self, lcs_matrix: List[List[int]], text1: str, text2: str) -> str:
        '
		Backtracks through the LCS matrix to reconstruct the longest common subsequence.
        
		:param lcs_matrix: A 2D list (matrix) containing the lengths of LCS for substrings of text1 and text2.
		:param text1: The first text as a string.
		:param text2: The second text as a string.
		:return: The longest common subsequence as a string.
		'
        i: int = len(text1)
        j: int = len(text2)
        lcs: List[str] = []
        while ((i > 0) and (j > 0)):
            if (text1[(i - 1)] == text2[(j - 1)]):
                lcs.append(text1[(i - 1)])
                i -= 1
                j -= 1
            elif (lcs_matrix[(i - 1)][j] >= lcs_matrix[i][(j - 1)]):
                i -= 1
            else:
                j -= 1
        return ''.join(reversed(lcs))

    def compute(self, text1: str, text2: str) -> str:
        '
		Computes the Longest Common Subsequence (LCS) between two texts.
        
		:param text1: The first text as a string.
		:param text2: The second text as a string.
		:return: The longest common subsequence as a string.
		'
        lcs_matrix: List[List[int]] = self._lcs_matrix(text1, text2)
        lcs: str = self._backtrack_lcs(lcs_matrix, text1, text2)
        return lcs

    def example(self):
        self._obj1_exemple = 'AGGTAB'
        self._obj2_exemple = 'GXTXAYB'
        sequence = self.compute(self._obj1_exemple, self._obj2_exemple)
        print(f'{self.___class__.__name__} distance between {self._obj1_exemple} and {self._obj2_exemple} is {sequence}')


    # Propriétés pour accéder aux attributs depuis Python
    @property
    def __class__(self):
        return self.___class__
    @__class__.setter
    def __class__(self, value):
        self.___class__ = value
    @property
    def obj1_exemple(self):
        return self._obj1_exemple
    @obj1_exemple.setter
    def obj1_exemple(self, value):
        self._obj1_exemple = value
    @property
    def obj2_exemple(self):
        return self._obj2_exemple
    @obj2_exemple.setter
    def obj2_exemple(self, value):
        self._obj2_exemple = value
    @property
    def _backtrack_lcs(self):
        return self.__backtrack_lcs
    @_backtrack_lcs.setter
    def _backtrack_lcs(self, value):
        self.__backtrack_lcs = value
    @property
    def type(self):
        return self._type
    @type.setter
    def type(self, value):
        self._type = value
    @property
    def _lcs_matrix(self):
        return self.__lcs_matrix
    @_lcs_matrix.setter
    def _lcs_matrix(self, value):
        self.__lcs_matrix = value
    @property
    def compute(self):
        return self._compute
    @compute.setter
    def compute(self, value):
        self._compute = value

	def __init__(self) -> None:
		super().__init__()
		self.type='vec_str'

		"""
		A class to compute the Longest Common Subsequence (LCS) between two text files.
		"""

	def _lcs_matrix(self, text1: str, text2: str) -> List[List[int]]:
		"""
		Constructs the LCS matrix for two input texts.
        
		:param text1: The first text as a string.
		:param text2: The second text as a string.
		:return: A 2D list (matrix) containing the lengths of LCS for substrings of text1 and text2.
		"""
		len1: int = len(text1)
		len2: int = len(text2)
        
		# Create a 2D matrix initialized with 0
		lcs_matrix: List[List[int]] = [[0] * (len2 + 1) for _ in range(len1 + 1)]

		for i in range(1, len1 + 1):
			for j in range(1, len2 + 1):
				if text1[i - 1] == text2[j - 1]:
					lcs_matrix[i][j] = lcs_matrix[i - 1][j - 1] + 1
				else:
					lcs_matrix[i][j] = max(lcs_matrix[i - 1][j], lcs_matrix[i][j - 1])

		return lcs_matrix

	def _backtrack_lcs(self, lcs_matrix: List[List[int]], text1: str, text2: str) -> str:
		"""
		Backtracks through the LCS matrix to reconstruct the longest common subsequence.
        
		:param lcs_matrix: A 2D list (matrix) containing the lengths of LCS for substrings of text1 and text2.
		:param text1: The first text as a string.
		:param text2: The second text as a string.
		:return: The longest common subsequence as a string.
		"""
		i: int = len(text1)
		j: int = len(text2)
		lcs: List[str] = []

		while i > 0 and j > 0:
			if text1[i - 1] == text2[j - 1]:
				lcs.append(text1[i - 1])
				i -= 1
				j -= 1
			elif lcs_matrix[i - 1][j] >= lcs_matrix[i][j - 1]:
				i -= 1
			else:
				j -= 1

		return ''.join(reversed(lcs))

	def compute(self, text1: str, text2: str) -> str:
		"""
		Computes the Longest Common Subsequence (LCS) between two texts.
        
		:param text1: The first text as a string.
		:param text2: The second text as a string.
		:return: The longest common subsequence as a string.
		"""
		# Compute the LCS matrix
		lcs_matrix: List[List[int]] = self._lcs_matrix(text1, text2)

		# Backtrack to find the actual LCS
		lcs: str = self._backtrack_lcs(lcs_matrix, text1, text2)

		return lcs
		
	def example(self):
		self.obj1_exemple = "AGGTAB"
		self.obj2_exemple = "GXTXAYB"
		sequence=self.compute(self.obj1_exemple,self.obj2_exemple)
		
		print(f"{self.__class__.__name__} distance between {self.obj1_exemple} and {self.obj2_exemple} is {sequence}")

cdef class LCSS(LongestCommonSubsequence):
    # Attributs de classe
    pass

  pass
  
cdef class Frechet(Distance):
    # Attributs de classe
    cdef object ___class__
    cdef object _curve_b
    cdef object _curve_a
    cdef object _ca
    cdef object _obj1_example
    cdef object _obj2_example
    cdef object _type
    cdef object _compute
    cdef object __c

    def __init__(self, *args, **kwargs):
        '
		Initialize the FrechetDistance with two curves.

		:param curve_a: First curve, a list of tuples representing points (e.g., [(x1, y1), (x2, y2), ...])
		:param curve_b: Second curve, a list of tuples representing points (e.g., [(x1, y1), (x2, y2), ...])
		'
        super().__init__()
        self._type = 'vec_tuple_float'

    def _c(self, i, j):
        '
		Internal method to compute the discrete Fréchet distance using dynamic programming.

		:param i: Index in curve_a
		:param j: Index in curve_b
		:return: Fréchet distance between curve_a[0..i] and curve_b[0..j]
		'
        if (self._ca[i][j] > (- 1)):
            return self._ca[i][j]
        elif ((i == 0) and (j == 0)):
            self._ca[i][j] = Euclidean().calculate(self._curve_a[0], self._curve_b[0])
        elif ((i > 0) and (j == 0)):
            self._ca[i][j] = max(self._c((i - 1), 0), Euclidean().calculate(self._curve_a[i], self._curve_b[0]))
        elif ((i == 0) and (j > 0)):
            self._ca[i][j] = max(self._c(0, (j - 1)), Euclidean().calculate(self._curve_a[0], self._curve_b[j]))
        elif ((i > 0) and (j > 0)):
            self._ca[i][j] = max(min(self._c((i - 1), j), self._c((i - 1), (j - 1)), self._c(i, (j - 1))), Euclidean().calculate(self._curve_a[i], self._curve_b[j]))
        else:
            self._ca[i][j] = float('inf')
        return self._ca[i][j]

    def compute(self, curve_a, curve_b):
        '
		Compute the Fréchet distance between the two curves.

		:return: The Fréchet distance between curve_a and curve_b
		'
        self._curve_a = curve_a
        self._curve_b = curve_b
        self._ca = [[(- 1) for _ in range(len(curve_b))] for _ in range(len(curve_a))]
        return self._c((len(self._curve_a) - 1), (len(self._curve_b) - 1))

    def example(self):
        self._obj1_example = [(0, 0), (1, 1), (2, 2)]
        self._obj2_example = [(0, 0), (1, 2), (2, 3)]
        distance = self.compute(self._obj1_example, self._obj2_example)
        print(f'{self.___class__.__name__} distance between {self._obj1_example} and {self._obj2_example} is {distance:.2f}')


    # Propriétés pour accéder aux attributs depuis Python
    @property
    def __class__(self):
        return self.___class__
    @__class__.setter
    def __class__(self, value):
        self.___class__ = value
    @property
    def curve_b(self):
        return self._curve_b
    @curve_b.setter
    def curve_b(self, value):
        self._curve_b = value
    @property
    def curve_a(self):
        return self._curve_a
    @curve_a.setter
    def curve_a(self, value):
        self._curve_a = value
    @property
    def ca(self):
        return self._ca
    @ca.setter
    def ca(self, value):
        self._ca = value
    @property
    def type(self):
        return self._type
    @type.setter
    def type(self, value):
        self._type = value
    @property
    def obj2_example(self):
        return self._obj2_example
    @obj2_example.setter
    def obj2_example(self, value):
        self._obj2_example = value
    @property
    def obj1_example(self):
        return self._obj1_example
    @obj1_example.setter
    def obj1_example(self, value):
        self._obj1_example = value
    @property
    def compute(self):
        return self._compute
    @compute.setter
    def compute(self, value):
        self._compute = value
    @property
    def _c(self):
        return self.__c
    @_c.setter
    def _c(self, value):
        self.__c = value

	def __init__(self)-> None:
		"""
		Initialize the FrechetDistance with two curves.

		:param curve_a: First curve, a list of tuples representing points (e.g., [(x1, y1), (x2, y2), ...])
		:param curve_b: Second curve, a list of tuples representing points (e.g., [(x1, y1), (x2, y2), ...])
		"""
		super().__init__()
		self.type='vec_tuple_float'


	def _c(self, i, j):
		"""
		Internal method to compute the discrete Fréchet distance using dynamic programming.

		:param i: Index in curve_a
		:param j: Index in curve_b
		:return: Fréchet distance between curve_a[0..i] and curve_b[0..j]
		"""
		if self.ca[i][j] > -1:
			return self.ca[i][j]
		elif i == 0 and j == 0:
			self.ca[i][j] = Euclidean().calculate(self.curve_a[0], self.curve_b[0])
		elif i > 0 and j == 0:
			self.ca[i][j] = max(self._c(i - 1, 0), Euclidean().calculate(self.curve_a[i], self.curve_b[0]))
		elif i == 0 and j > 0:
			self.ca[i][j] = max(self._c(0, j - 1), Euclidean().calculate(self.curve_a[0], self.curve_b[j]))
		elif i > 0 and j > 0:
			self.ca[i][j] = max(
				min(self._c(i - 1, j), self._c(i - 1, j - 1), self._c(i, j - 1)),
				Euclidean().calculate(self.curve_a[i], self.curve_b[j])
				)
		else:
			self.ca[i][j] = float('inf')
		return self.ca[i][j]

	def compute(self, curve_a, curve_b):
		"""
		Compute the Fréchet distance between the two curves.

		:return: The Fréchet distance between curve_a and curve_b
		"""
		self.curve_a = curve_a
		self.curve_b = curve_b
		self.ca = [[-1 for _ in range(len(curve_b))] for _ in range(len(curve_a))]
        
		return self._c(len(self.curve_a) - 1, len(self.curve_b) - 1)
	
	def example(self):
		self.obj1_example = [(0, 0), (1, 1), (2, 2)]
		self.obj2_example = [(0, 0), (1, 2), (2, 3)]
		distance=self.compute(self.obj1_example,self.obj2_example)
		print(f"{self.__class__.__name__} distance between {self.obj1_example} and {self.obj2_example} is {distance:.2f}")
######################################
# atester

cdef class ERPDistance(Distance):
    # Attributs de classe
    cdef object _type
    cdef object __compute_element_distance
    cdef object _compute
    cdef object _gap_penalty
    '
    A class to compute the Edit Distance with Real Penalty (ERP) between two sequences.
    ERP is a metric that combines the properties of edit distance and Lp-norms.
    
    The ERP distance uses a constant gap penalty and considers numerical values
    when computing the distance between elements.
    
    Attributes:
        gap_penalty (float): The penalty value for gaps in the sequences
    '

    def __init__(self, *args, **kwargs):
        '
        Initialize the ERP distance calculator.
        
        Args:
            gap_penalty (float): The penalty value for gaps. Default is 1.0
        '
        super().__init__()
        self._type = 'vec_float'
        self._gap_penalty = gap_penalty

    def _compute_element_distance(self, x, y):
        '
        Compute the distance between two elements.
        
        Args:
            x (float): First element
            y (float): Second element
            
        Returns:
            float: Absolute difference between the elements
        '
        return abs((x - y))

    def compute(self, seq1, seq2):
        '
        Compute the ERP distance between two sequences.
        
        Args:
            seq1 (list): First sequence of numerical values
            seq2 (list): Second sequence of numerical values
            
        Returns:
            float: The ERP distance between the sequences
            
        Raises:
            ValueError: If sequences are empty
        '
        if ((not seq1) or (not seq2)):
            raise ValueError('Sequences cannot be empty')
        (n, m) = (len(seq1), len(seq2))
        dp = [([0.0] * (m + 1)) for _ in range((n + 1))]
        for i in range(1, (n + 1)):
            dp[i][0] = (dp[(i - 1)][0] + self._gap_penalty)
        for j in range(1, (m + 1)):
            dp[0][j] = (dp[0][(j - 1)] + self._gap_penalty)
        for i in range(1, (n + 1)):
            for j in range(1, (m + 1)):
                substitute = (dp[(i - 1)][(j - 1)] + self._compute_element_distance(seq1[(i - 1)], seq2[(j - 1)]))
                delete = (dp[(i - 1)][j] + self._gap_penalty)
                insert = (dp[i][(j - 1)] + self._gap_penalty)
                dp[i][j] = min(substitute, delete, insert)
        return dp[n][m]

    def compute_normalized(self, seq1, seq2):
        '
        Compute the normalized ERP distance between two sequences.
        The normalization is done by dividing the ERP distance by the length 
        of the longer sequence.
        
        Args:
            seq1 (list): First sequence of numerical values
            seq2 (list): Second sequence of numerical values
            
        Returns:
            float: The normalized ERP distance between the sequences
        '
        erp_distance = self.compute(seq1, seq2)
        max_length = max(len(seq1), len(seq2))
        return (erp_distance / max_length)


    # Propriétés pour accéder aux attributs depuis Python
    @property
    def type(self):
        return self._type
    @type.setter
    def type(self, value):
        self._type = value
    @property
    def _compute_element_distance(self):
        return self.__compute_element_distance
    @_compute_element_distance.setter
    def _compute_element_distance(self, value):
        self.__compute_element_distance = value
    @property
    def compute(self):
        return self._compute
    @compute.setter
    def compute(self, value):
        self._compute = value
    @property
    def gap_penalty(self):
        return self._gap_penalty
    @gap_penalty.setter
    def gap_penalty(self, value):
        self._gap_penalty = value

    """
    A class to compute the Edit Distance with Real Penalty (ERP) between two sequences.
    ERP is a metric that combines the properties of edit distance and Lp-norms.
    
    The ERP distance uses a constant gap penalty and considers numerical values
    when computing the distance between elements.
    
    Attributes:
        gap_penalty (float): The penalty value for gaps in the sequences
    """
    
    def __init__(self, gap_penalty=1.0)-> None:
        """
        Initialize the ERP distance calculator.
        
        Args:
            gap_penalty (float): The penalty value for gaps. Default is 1.0
        """
        super().__init__()
        self.type='vec_float'

        self.gap_penalty = gap_penalty
    
    def _compute_element_distance(self, x, y):
        """
        Compute the distance between two elements.
        
        Args:
            x (float): First element
            y (float): Second element
            
        Returns:
            float: Absolute difference between the elements
        """
        return abs(x - y)
    
    def compute(self, seq1, seq2):
        """
        Compute the ERP distance between two sequences.
        
        Args:
            seq1 (list): First sequence of numerical values
            seq2 (list): Second sequence of numerical values
            
        Returns:
            float: The ERP distance between the sequences
            
        Raises:
            ValueError: If sequences are empty
        """
        if not seq1 or not seq2:
            raise ValueError("Sequences cannot be empty")
            
        n, m = len(seq1), len(seq2)
        
        # Initialize the dynamic programming matrix
        dp = [[0.0] * (m + 1) for _ in range(n + 1)]
        
        # Initialize first row and column with gap penalties
        for i in range(1, n + 1):
            dp[i][0] = dp[i-1][0] + self.gap_penalty
        for j in range(1, m + 1):
            dp[0][j] = dp[0][j-1] + self.gap_penalty
            
        # Fill the DP matrix
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                # Cost of substitution
                substitute = dp[i-1][j-1] + self._compute_element_distance(seq1[i-1], seq2[j-1])
                # Cost of deletion (gap in second sequence)
                delete = dp[i-1][j] + self.gap_penalty
                # Cost of insertion (gap in first sequence)
                insert = dp[i][j-1] + self.gap_penalty
                
                # Take the minimum of the three operations
                dp[i][j] = min(substitute, delete, insert)
                
        return dp[n][m]
    
    def compute_normalized(self, seq1, seq2):
        """
        Compute the normalized ERP distance between two sequences.
        The normalization is done by dividing the ERP distance by the length 
        of the longer sequence.
        
        Args:
            seq1 (list): First sequence of numerical values
            seq2 (list): Second sequence of numerical values
            
        Returns:
            float: The normalized ERP distance between the sequences
        """
        erp_distance = self.compute(seq1, seq2)
        max_length = max(len(seq1), len(seq2))
        return erp_distance / max_length

cdef class EDRDistance(Distance):
    # Attributs de classe
    cdef object __is_match
    cdef object _epsilon
    cdef object _compute_normalized
    cdef object _type
    cdef object _compute
    '
    A class to compute the Edit Distance on Real Sequences (EDR) between two time series.
    EDR is designed to be robust to noise by considering two elements as a match
    if their difference falls within a user-specified threshold (epsilon).
    
    Attributes:
        epsilon (float): Threshold for considering two elements as matching
    '

    def __init__(self, *args, **kwargs):
        '
        Initialize the EDR distance calculator.
        
        Args:
            epsilon (float): Tolerance threshold for matching elements.
                           Two elements are considered matching if their
                           absolute difference is less than epsilon.
                           Default is 0.1
        '
        super().__init__()
        self._type = 'vec_float'
        self._epsilon = epsilon

    def _is_match(self, x, y):
        '
        Check if two elements match within the epsilon threshold.
        
        Args:
            x (float): First element
            y (float): Second element
            
        Returns:
            bool: True if the elements match within epsilon, False otherwise
        '
        return (abs((x - y)) <= self._epsilon)

    def compute(self, seq1, seq2):
        '
        Compute the EDR distance between two sequences.
        
        Args:
            seq1 (list): First sequence of numerical values
            seq2 (list): Second sequence of numerical values
            
        Returns:
            float: The EDR distance between the sequences
            
        Raises:
            ValueError: If sequences are empty
        '
        if ((not seq1) or (not seq2)):
            raise ValueError('Sequences cannot be empty')
        (n, m) = (len(seq1), len(seq2))
        dp = [([0] * (m + 1)) for _ in range((n + 1))]
        for i in range((n + 1)):
            dp[i][0] = i
        for j in range((m + 1)):
            dp[0][j] = j
        for i in range(1, (n + 1)):
            for j in range(1, (m + 1)):
                subcost = (0 if self._is_match(seq1[(i - 1)], seq2[(j - 1)]) else 1)
                dp[i][j] = min((dp[(i - 1)][(j - 1)] + subcost), (dp[(i - 1)][j] + 1), (dp[i][(j - 1)] + 1))
        return dp[n][m]

    def compute_normalized(self, seq1, seq2):
        '
        Compute the normalized EDR distance between two sequences.
        The normalization is done by dividing the EDR distance by the length
        of the longer sequence.
        
        Args:
            seq1 (list): First sequence of numerical values
            seq2 (list): Second sequence of numerical values
            
        Returns:
            float: The normalized EDR distance between the sequences (between 0 and 1)
        '
        edr_distance = self.compute(seq1, seq2)
        max_length = max(len(seq1), len(seq2))
        return (edr_distance / max_length)

    def similarity(self, seq1, seq2):
        '
        Compute the EDR similarity between two sequences.
        The similarity is defined as (1 - normalized_distance).
        
        Args:
            seq1 (list): First sequence of numerical values
            seq2 (list): Second sequence of numerical values
            
        Returns:
            float: The EDR similarity between the sequences (between 0 and 1)
        '
        return (1 - self.compute_normalized(seq1, seq2))


    # Propriétés pour accéder aux attributs depuis Python
    @property
    def _is_match(self):
        return self.__is_match
    @_is_match.setter
    def _is_match(self, value):
        self.__is_match = value
    @property
    def epsilon(self):
        return self._epsilon
    @epsilon.setter
    def epsilon(self, value):
        self._epsilon = value
    @property
    def compute_normalized(self):
        return self._compute_normalized
    @compute_normalized.setter
    def compute_normalized(self, value):
        self._compute_normalized = value
    @property
    def type(self):
        return self._type
    @type.setter
    def type(self, value):
        self._type = value
    @property
    def compute(self):
        return self._compute
    @compute.setter
    def compute(self, value):
        self._compute = value

    """
    A class to compute the Edit Distance on Real Sequences (EDR) between two time series.
    EDR is designed to be robust to noise by considering two elements as a match
    if their difference falls within a user-specified threshold (epsilon).
    
    Attributes:
        epsilon (float): Threshold for considering two elements as matching
    """
    
    def __init__(self, epsilon=0.1)-> None:
        """
        Initialize the EDR distance calculator.
        
        Args:
            epsilon (float): Tolerance threshold for matching elements.
                           Two elements are considered matching if their
                           absolute difference is less than epsilon.
                           Default is 0.1
        """
        super().__init__()
        self.type='vec_float'
        
        self.epsilon = epsilon
    
    def _is_match(self, x, y):
        """
        Check if two elements match within the epsilon threshold.
        
        Args:
            x (float): First element
            y (float): Second element
            
        Returns:
            bool: True if the elements match within epsilon, False otherwise
        """
        return abs(x - y) <= self.epsilon
    
    def compute(self, seq1, seq2):
        """
        Compute the EDR distance between two sequences.
        
        Args:
            seq1 (list): First sequence of numerical values
            seq2 (list): Second sequence of numerical values
            
        Returns:
            float: The EDR distance between the sequences
            
        Raises:
            ValueError: If sequences are empty
        """
        if not seq1 or not seq2:
            raise ValueError("Sequences cannot be empty")
            
        n, m = len(seq1), len(seq2)
        
        # Initialize the dynamic programming matrix
        # Adding 1 to dimensions for base cases
        dp = [[0] * (m + 1) for _ in range(n + 1)]
        
        # Initialize first row and column
        for i in range(n + 1):
            dp[i][0] = i
        for j in range(m + 1):
            dp[0][j] = j
            
        # Fill the DP matrix
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                # Cost is 0 if elements match within epsilon, 1 otherwise
                subcost = 0 if self._is_match(seq1[i-1], seq2[j-1]) else 1
                
                dp[i][j] = min(
                    dp[i-1][j-1] + subcost,  # substitution
                    dp[i-1][j] + 1,          # deletion
                    dp[i][j-1] + 1           # insertion
                )
                
        return dp[n][m]
    
    def compute_normalized(self, seq1, seq2):
        """
        Compute the normalized EDR distance between two sequences.
        The normalization is done by dividing the EDR distance by the length
        of the longer sequence.
        
        Args:
            seq1 (list): First sequence of numerical values
            seq2 (list): Second sequence of numerical values
            
        Returns:
            float: The normalized EDR distance between the sequences (between 0 and 1)
        """
        edr_distance = self.compute(seq1, seq2)
        max_length = max(len(seq1), len(seq2))
        return edr_distance / max_length
    
    def similarity(self, seq1, seq2):
        """
        Compute the EDR similarity between two sequences.
        The similarity is defined as (1 - normalized_distance).
        
        Args:
            seq1 (list): First sequence of numerical values
            seq2 (list): Second sequence of numerical values
            
        Returns:
            float: The EDR similarity between the sequences (between 0 and 1)
        """
        return 1 - self.compute_normalized(seq1, seq2)
        
cdef class TWEDDistance(Distance):
    # Attributs de classe
    cdef object __distance_between_points
    cdef object __time_difference_penalty
    cdef object _nu
    cdef object _lambda_
    cdef object _type
    cdef object _compute
    '
    A class to compute the Time Warp Edit Distance (TWED) between two time series.
    TWED combines the flexibility of edit distance with time awareness, making it
    suitable for comparing time series of different lengths while considering
    temporal relationships.
    
    Attributes:
        lambda_ (float): The gap penalty parameter
        nu (float): The time stamp penalty parameter
    '

    def __init__(self, *args, **kwargs):
        '
        Initialize the TWED calculator.
        
        Args:
            lambda_ (float): Gap penalty parameter. Controls the cost of deletion/insertion
                           operations. Default is 1.0
            nu (float): Time stamp penalty parameter. Controls the importance of
                      temporal differences. Default is 0.001
        '
        super().__init__()
        self._type = 'vec_float'
        self._lambda_ = lambda_
        self._nu = nu

    def _distance_between_points(self, x1, x2):
        '
        Compute the distance between two points in the time series.
        
        Args:
            x1 (float): First point
            x2 (float): Second point
            
        Returns:
            float: Absolute difference between the points
        '
        return abs((x1 - x2))

    def _time_difference_penalty(self, t1, t2):
        '
        Compute the time difference penalty between two timestamps.
        
        Args:
            t1 (float): First timestamp
            t2 (float): Second timestamp
            
        Returns:
            float: Time difference penalty
        '
        return (self._nu * abs((t1 - t2)))

    def compute(self, series1, times1, series2, times2):
        "
        Compute the TWED distance between two time series.
        
        Args:
            series1 (list): First time series values
            times1 (list): Timestamps for first series
            series2 (list): Second time series values
            times2 (list): Timestamps for second series
            
        Returns:
            float: The TWED distance between the time series
            
        Raises:
            ValueError: If input series are empty or lengths don't match their timestamps
        "
        if ((not series1) or (not series2)):
            raise ValueError('Time series cannot be empty')
        if ((len(series1) != len(times1)) or (len(series2) != len(times2))):
            raise ValueError('Series values and timestamps must have matching lengths')
        (n, m) = (len(series1), len(series2))
        dp = [([float('inf')] * (m + 1)) for _ in range((n + 1))]
        dp[0][0] = 0
        for i in range(1, (n + 1)):
            dp[i][0] = (((dp[(i - 1)][0] + self._distance_between_points(series1[(i - 1)], 0)) + self._time_difference_penalty(times1[(i - 1)], 0)) + self._lambda_)
        for j in range(1, (m + 1)):
            dp[0][j] = (((dp[0][(j - 1)] + self._distance_between_points(series2[(j - 1)], 0)) + self._time_difference_penalty(times2[(j - 1)], 0)) + self._lambda_)
        for i in range(1, (n + 1)):
            for j in range(1, (m + 1)):
                match_cost = self._distance_between_points(series1[(i - 1)], series2[(j - 1)])
                if ((i > 1) and (j > 1)):
                    time_penalty1 = self._time_difference_penalty(times1[(i - 1)], times1[(i - 2)])
                    time_penalty2 = self._time_difference_penalty(times2[(j - 1)], times2[(j - 2)])
                else:
                    time_penalty1 = time_penalty2 = 0
                match = (((dp[(i - 1)][(j - 1)] + match_cost) + time_penalty1) + time_penalty2)
                delete = (((dp[(i - 1)][j] + self._distance_between_points(series1[(i - 1)], 0)) + self._time_difference_penalty(times1[(i - 1)], 0)) + self._lambda_)
                insert = (((dp[i][(j - 1)] + self._distance_between_points(series2[(j - 1)], 0)) + self._time_difference_penalty(times2[(j - 1)], 0)) + self._lambda_)
                dp[i][j] = min(match, delete, insert)
        return dp[n][m]

    def compute_normalized(self, series1, times1, series2, times2):
        '
        Compute the normalized TWED distance between two time series.
        
        Args:
            series1 (list): First time series values
            times1 (list): Timestamps for first series
            series2 (list): Second time series values
            times2 (list): Timestamps for second series
            
        Returns:
            float: The normalized TWED distance
        '
        twed_distance = self.compute(series1, times1, series2, times2)
        max_length = max(len(series1), len(series2))
        max_time_diff = abs((max(max(times1), max(times2)) - min(min(times1), min(times2))))
        normalization_factor = (max_length * ((1 + self._lambda_) + (self._nu * max_time_diff)))
        return (twed_distance / normalization_factor)


    # Propriétés pour accéder aux attributs depuis Python
    @property
    def _distance_between_points(self):
        return self.__distance_between_points
    @_distance_between_points.setter
    def _distance_between_points(self, value):
        self.__distance_between_points = value
    @property
    def _time_difference_penalty(self):
        return self.__time_difference_penalty
    @_time_difference_penalty.setter
    def _time_difference_penalty(self, value):
        self.__time_difference_penalty = value
    @property
    def nu(self):
        return self._nu
    @nu.setter
    def nu(self, value):
        self._nu = value
    @property
    def lambda_(self):
        return self._lambda_
    @lambda_.setter
    def lambda_(self, value):
        self._lambda_ = value
    @property
    def type(self):
        return self._type
    @type.setter
    def type(self, value):
        self._type = value
    @property
    def compute(self):
        return self._compute
    @compute.setter
    def compute(self, value):
        self._compute = value

    """
    A class to compute the Time Warp Edit Distance (TWED) between two time series.
    TWED combines the flexibility of edit distance with time awareness, making it
    suitable for comparing time series of different lengths while considering
    temporal relationships.
    
    Attributes:
        lambda_ (float): The gap penalty parameter
        nu (float): The time stamp penalty parameter
    """
    
    def __init__(self, lambda_=1.0, nu=0.001)-> None:
        """
        Initialize the TWED calculator.
        
        Args:
            lambda_ (float): Gap penalty parameter. Controls the cost of deletion/insertion
                           operations. Default is 1.0
            nu (float): Time stamp penalty parameter. Controls the importance of
                      temporal differences. Default is 0.001
        """
        super().__init__()
        self.type='vec_float'
        
        self.lambda_ = lambda_
        self.nu = nu
    
    def _distance_between_points(self, x1, x2):
        """
        Compute the distance between two points in the time series.
        
        Args:
            x1 (float): First point
            x2 (float): Second point
            
        Returns:
            float: Absolute difference between the points
        """
        return abs(x1 - x2)
    
    def _time_difference_penalty(self, t1, t2):
        """
        Compute the time difference penalty between two timestamps.
        
        Args:
            t1 (float): First timestamp
            t2 (float): Second timestamp
            
        Returns:
            float: Time difference penalty
        """
        return self.nu * abs(t1 - t2)
    
    def compute(self, series1, times1, series2, times2):
        """
        Compute the TWED distance between two time series.
        
        Args:
            series1 (list): First time series values
            times1 (list): Timestamps for first series
            series2 (list): Second time series values
            times2 (list): Timestamps for second series
            
        Returns:
            float: The TWED distance between the time series
            
        Raises:
            ValueError: If input series are empty or lengths don't match their timestamps
        """
        # Validate inputs
        if not series1 or not series2:
            raise ValueError("Time series cannot be empty")
        if len(series1) != len(times1) or len(series2) != len(times2):
            raise ValueError("Series values and timestamps must have matching lengths")
            
        n, m = len(series1), len(series2)
        
        # Initialize the dynamic programming matrix
        dp = [[float('inf')] * (m + 1) for _ in range(n + 1)]
        dp[0][0] = 0
        
        # Initialize first row and column with deletion/insertion costs
        for i in range(1, n + 1):
            dp[i][0] = dp[i-1][0] + self._distance_between_points(series1[i-1], 0) + \
                      self._time_difference_penalty(times1[i-1], 0) + self.lambda_
                      
        for j in range(1, m + 1):
            dp[0][j] = dp[0][j-1] + self._distance_between_points(series2[j-1], 0) + \
                      self._time_difference_penalty(times2[j-1], 0) + self.lambda_
        
        # Fill the DP matrix
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                # Cost of matching current points
                match_cost = self._distance_between_points(series1[i-1], series2[j-1])
                
                # Time penalties
                if i > 1 and j > 1:
                    time_penalty1 = self._time_difference_penalty(times1[i-1], times1[i-2])
                    time_penalty2 = self._time_difference_penalty(times2[j-1], times2[j-2])
                else:
                    time_penalty1 = time_penalty2 = 0
                
                # Calculate the three possible operations
                match = dp[i-1][j-1] + match_cost + time_penalty1 + time_penalty2
                
                delete = dp[i-1][j] + self._distance_between_points(series1[i-1], 0) + \
                        self._time_difference_penalty(times1[i-1], 0) + self.lambda_
                        
                insert = dp[i][j-1] + self._distance_between_points(series2[j-1], 0) + \
                        self._time_difference_penalty(times2[j-1], 0) + self.lambda_
                
                dp[i][j] = min(match, delete, insert)
        
        return dp[n][m]
    
    def compute_normalized(self, series1, times1, series2, times2):
        """
        Compute the normalized TWED distance between two time series.
        
        Args:
            series1 (list): First time series values
            times1 (list): Timestamps for first series
            series2 (list): Second time series values
            times2 (list): Timestamps for second series
            
        Returns:
            float: The normalized TWED distance
        """
        twed_distance = self.compute(series1, times1, series2, times2)
        max_length = max(len(series1), len(series2))
        # Normalize by the maximum possible cost (assuming worst case)
        max_time_diff = abs(max(max(times1), max(times2)) - min(min(times1), min(times2)))
        normalization_factor = max_length * (1 + self.lambda_ + self.nu * max_time_diff)
        return twed_distance / normalization_factor
        
cdef class SBDDistance(Distance):
    # Attributs de classe
    cdef object _similarity
    cdef object __cross_correlation
    cdef object __normalize_series
    cdef object __pad_series
    cdef object _type
    cdef object _compute
    '
    A class to compute the Shape-Based Distance (SBD) between two time series.
    SBD uses normalized cross-correlation (NCC) to compare the shapes of time series,
    making it invariant to scaling and offset.
    
    The distance is calculated as: SBD = 1 - NCC_max,
    where NCC_max is the maximum of the normalized cross-correlation.
    '

    def __init__(self, *args, **kwargs):
        'Initialize the SBD calculator.'
        super().__init__()
        self._type = 'vec_float'

    def _normalize_series(self, series):
        '
        Normalize a time series by subtracting the mean and dividing by standard deviation.
        
        Args:
            series (list): Input time series
            
        Returns:
            list: Normalized time series
            
        Raises:
            ValueError: If the series has zero standard deviation
        '
        n = len(series)
        if (n == 0):
            raise ValueError('Series cannot be empty')
        mean = (sum(series) / n)
        squared_diff_sum = sum((((x - mean) ** 2) for x in series))
        std = ((squared_diff_sum / n) ** 0.5)
        if (std == 0):
            raise ValueError('Series has zero standard deviation')
        return [((x - mean) / std) for x in series]

    def _pad_series(self, series1, series2):
        '
        Pad the shorter series with zeros to match the length of the longer series.
        
        Args:
            series1 (list): First time series
            series2 (list): Second time series
            
        Returns:
            tuple: Padded versions of both series
        '
        (n1, n2) = (len(series1), len(series2))
        if (n1 > n2):
            return (series1, (series2 + ([0] * (n1 - n2))))
        elif (n2 > n1):
            return ((series1 + ([0] * (n2 - n1))), series2)
        return (series1, series2)

    def _cross_correlation(self, series1, series2):
        '
        Compute the normalized cross-correlation between two series.
        
        Args:
            series1 (list): First normalized time series
            series2 (list): Second normalized time series
            
        Returns:
            list: Cross-correlation values for different lags
        '
        n = len(series1)
        max_lag = (n - 1)
        cc = []
        for lag in range((- max_lag), (max_lag + 1)):
            correlation = 0
            count = 0
            for i in range(n):
                j = (i + lag)
                if (0 <= j < n):
                    correlation += (series1[i] * series2[j])
                    count += 1
            if (count > 0):
                cc.append((correlation / count))
            else:
                cc.append(0)
        return cc

    def compute(self, series1, series2):
        '
        Compute the Shape-Based Distance between two time series.
        
        Args:
            series1 (list): First time series
            series2 (list): Second time series
            
        Returns:
            float: The SBD distance (between 0 and 2)
            
        Raises:
            ValueError: If either series is empty
        '
        if ((not series1) or (not series2)):
            raise ValueError('Time series cannot be empty')
        norm_series1 = self._normalize_series(series1)
        norm_series2 = self._normalize_series(series2)
        (padded_series1, padded_series2) = self._pad_series(norm_series1, norm_series2)
        cc = self._cross_correlation(padded_series1, padded_series2)
        ncc_max = max(cc)
        return (1 - ncc_max)

    def similarity(self, series1, series2):
        '
        Compute the shape-based similarity between two time series.
        
        Args:
            series1 (list): First time series
            series2 (list): Second time series
            
        Returns:
            float: The similarity score (between 0 and 1)
        '
        return (1 - (self.compute(series1, series2) / 2))

    def is_similar(self, series1, series2, threshold=0.8):
        '
        Determine if two time series are similar based on a threshold.
        
        Args:
            series1 (list): First time series
            series2 (list): Second time series
            threshold (float): Similarity threshold (between 0 and 1)
            
        Returns:
            bool: True if similarity is above threshold, False otherwise
        '
        return (self.similarity(series1, series2) >= threshold)


    # Propriétés pour accéder aux attributs depuis Python
    @property
    def similarity(self):
        return self._similarity
    @similarity.setter
    def similarity(self, value):
        self._similarity = value
    @property
    def _normalize_series(self):
        return self.__normalize_series
    @_normalize_series.setter
    def _normalize_series(self, value):
        self.__normalize_series = value
    @property
    def _cross_correlation(self):
        return self.__cross_correlation
    @_cross_correlation.setter
    def _cross_correlation(self, value):
        self.__cross_correlation = value
    @property
    def _pad_series(self):
        return self.__pad_series
    @_pad_series.setter
    def _pad_series(self, value):
        self.__pad_series = value
    @property
    def type(self):
        return self._type
    @type.setter
    def type(self, value):
        self._type = value
    @property
    def compute(self):
        return self._compute
    @compute.setter
    def compute(self, value):
        self._compute = value
 

    """
    A class to compute the Shape-Based Distance (SBD) between two time series.
    SBD uses normalized cross-correlation (NCC) to compare the shapes of time series,
    making it invariant to scaling and offset.
    
    The distance is calculated as: SBD = 1 - NCC_max,
    where NCC_max is the maximum of the normalized cross-correlation.
    """
    
    def __init__(self)-> None:
        """Initialize the SBD calculator."""
        super().__init__()
        self.type='vec_float'
    
    def _normalize_series(self, series):
        """
        Normalize a time series by subtracting the mean and dividing by standard deviation.
        
        Args:
            series (list): Input time series
            
        Returns:
            list: Normalized time series
            
        Raises:
            ValueError: If the series has zero standard deviation
        """
        n = len(series)
        if n == 0:
            raise ValueError("Series cannot be empty")
            
        # Calculate mean
        mean = sum(series) / n
        
        # Calculate standard deviation
        squared_diff_sum = sum((x - mean) ** 2 for x in series)
        std = (squared_diff_sum / n) ** 0.5
        
        if std == 0:
            raise ValueError("Series has zero standard deviation")
            
        # Normalize series
        return [(x - mean) / std for x in series]
    
    def _pad_series(self, series1, series2):
        """
        Pad the shorter series with zeros to match the length of the longer series.
        
        Args:
            series1 (list): First time series
            series2 (list): Second time series
            
        Returns:
            tuple: Padded versions of both series
        """
        n1, n2 = len(series1), len(series2)
        if n1 > n2:
            # Pad series2 with zeros
            return series1, series2 + [0] * (n1 - n2)
        elif n2 > n1:
            # Pad series1 with zeros
            return series1 + [0] * (n2 - n1), series2
        return series1, series2
    
    def _cross_correlation(self, series1, series2):
        """
        Compute the normalized cross-correlation between two series.
        
        Args:
            series1 (list): First normalized time series
            series2 (list): Second normalized time series
            
        Returns:
            list: Cross-correlation values for different lags
        """
        n = len(series1)
        max_lag = n - 1
        cc = []
        
        # Calculate cross-correlation for different lags
        for lag in range(-max_lag, max_lag + 1):
            correlation = 0
            count = 0
            
            for i in range(n):
                j = i + lag
                if 0 <= j < n:
                    correlation += series1[i] * series2[j]
                    count += 1
            
            if count > 0:
                cc.append(correlation / count)
            else:
                cc.append(0)
                
        return cc
    
    def compute(self, series1, series2):
        """
        Compute the Shape-Based Distance between two time series.
        
        Args:
            series1 (list): First time series
            series2 (list): Second time series
            
        Returns:
            float: The SBD distance (between 0 and 2)
            
        Raises:
            ValueError: If either series is empty
        """
        if not series1 or not series2:
            raise ValueError("Time series cannot be empty")
        
        # Normalize both series
        norm_series1 = self._normalize_series(series1)
        norm_series2 = self._normalize_series(series2)
        
        # Pad series to equal length
        padded_series1, padded_series2 = self._pad_series(norm_series1, norm_series2)
        
        # Compute cross-correlation
        cc = self._cross_correlation(padded_series1, padded_series2)
        
        # Find maximum correlation
        ncc_max = max(cc)
        
        # Convert to distance
        return 1 - ncc_max
    
    def similarity(self, series1, series2):
        """
        Compute the shape-based similarity between two time series.
        
        Args:
            series1 (list): First time series
            series2 (list): Second time series
            
        Returns:
            float: The similarity score (between 0 and 1)
        """
        return 1 - (self.compute(series1, series2) / 2)
    
    def is_similar(self, series1, series2, threshold=0.8):
        """
        Determine if two time series are similar based on a threshold.
        
        Args:
            series1 (list): First time series
            series2 (list): Second time series
            threshold (float): Similarity threshold (between 0 and 1)
            
        Returns:
            bool: True if similarity is above threshold, False otherwise
        """
        return self.similarity(series1, series2) >= threshold
        
cdef class DDTWDistance(Distance):
    # Attributs de classe
    cdef object __calculate_distance_matrix
    cdef object __estimate_derivative
    cdef object _window_size
    cdef object __find_warp_path
    cdef object _type
    cdef object _compute
    '
    A class to compute the Derivative Dynamic Time Warping (DDTW) distance between two time series.
    DDTW extends the classical DTW algorithm by comparing the derivatives (rates of change)
    rather than the raw values, making it more sensitive to shape similarities.
    '

    def __init__(self, *args, **kwargs):
        '
        Initialize the DDTW calculator.
        
        Args:
            window_size (int, optional): Size of the warping window.
                                       If None, no window constraint is applied.
                                       If int, restricts the warping path to a window
                                       around the diagonal.
        '
        super().__init__()
        self._type = 'vec_float'
        self._window_size = window_size

    def _estimate_derivative(self, series):
        '
        Estimate the first derivative of a time series using a basic
        symmetric difference quotient method.
        
        For a point x[i], the derivative is estimated as:
        d[i] = ((x[i] - x[i-1]) + (x[i+1] - x[i-1])/2) / 2
        
        Args:
            series (list): Input time series
            
        Returns:
            list: Estimated derivatives for the time series
        '
        n = len(series)
        derivatives = []
        for i in range(n):
            if (i == 0):
                d = (series[1] - series[0])
            elif (i == (n - 1)):
                d = (series[(n - 1)] - series[(n - 2)])
            else:
                d = (((series[i] - series[(i - 1)]) + ((series[(i + 1)] - series[(i - 1)]) / 2)) / 2)
            derivatives.append(d)
        return derivatives

    def _calculate_distance_matrix(self, deriv1, deriv2):
        '
        Calculate the local cost matrix between two derivative series.
        
        Args:
            deriv1 (list): First derivative series
            deriv2 (list): Second derivative series
            
        Returns:
            list: 2D distance matrix
        '
        (n, m) = (len(deriv1), len(deriv2))
        distances = [([0] * m) for _ in range(n)]
        for i in range(n):
            for j in range(m):
                if ((self._window_size is None) or (abs((i - j)) <= self._window_size)):
                    distances[i][j] = ((deriv1[i] - deriv2[j]) ** 2)
                else:
                    distances[i][j] = float('inf')
        return distances

    def _find_warp_path(self, distances):
        '
        Find the optimal warping path through the distance matrix.
        
        Args:
            distances (list): 2D distance matrix
            
        Returns:
            float: The cumulative distance along the optimal path
        '
        (n, m) = (len(distances), len(distances[0]))
        accumulated = [([float('inf')] * m) for _ in range(n)]
        accumulated[0][0] = distances[0][0]
        for i in range(1, n):
            accumulated[i][0] = (distances[i][0] + accumulated[(i - 1)][0])
        for j in range(1, m):
            accumulated[0][j] = (distances[0][j] + accumulated[0][(j - 1)])
        for i in range(1, n):
            for j in range(1, m):
                if (distances[i][j] != float('inf')):
                    accumulated[i][j] = (distances[i][j] + min(accumulated[(i - 1)][j], accumulated[i][(j - 1)], accumulated[(i - 1)][(j - 1)]))
        return accumulated[(n - 1)][(m - 1)]

    def compute(self, series1, series2):
        '
        Compute the DDTW distance between two time series.
        
        Args:
            series1 (list): First time series
            series2 (list): Second time series
            
        Returns:
            float: The DDTW distance between the series
            
        Raises:
            ValueError: If either series is too short or empty
        '
        if ((len(series1) < 2) or (len(series2) < 2)):
            raise ValueError('Series must have at least 2 points for derivative estimation')
        deriv1 = self._estimate_derivative(series1)
        deriv2 = self._estimate_derivative(series2)
        distances = self._calculate_distance_matrix(deriv1, deriv2)
        ddtw_distance = self._find_warp_path(distances)
        return ddtw_distance

    def compute_normalized(self, series1, series2):
        '
        Compute the normalized DDTW distance between two time series.
        
        Args:
            series1 (list): First time series
            series2 (list): Second time series
            
        Returns:
            float: The normalized DDTW distance
        '
        ddtw_distance = self.compute(series1, series2)
        path_length = (len(series1) + len(series2))
        return (ddtw_distance / path_length)


    # Propriétés pour accéder aux attributs depuis Python
    @property
    def _calculate_distance_matrix(self):
        return self.__calculate_distance_matrix
    @_calculate_distance_matrix.setter
    def _calculate_distance_matrix(self, value):
        self.__calculate_distance_matrix = value
    @property
    def _estimate_derivative(self):
        return self.__estimate_derivative
    @_estimate_derivative.setter
    def _estimate_derivative(self, value):
        self.__estimate_derivative = value
    @property
    def type(self):
        return self._type
    @type.setter
    def type(self, value):
        self._type = value
    @property
    def _find_warp_path(self):
        return self.__find_warp_path
    @_find_warp_path.setter
    def _find_warp_path(self, value):
        self.__find_warp_path = value
    @property
    def window_size(self):
        return self._window_size
    @window_size.setter
    def window_size(self, value):
        self._window_size = value
    @property
    def compute(self):
        return self._compute
    @compute.setter
    def compute(self, value):
        self._compute = value
    """
    A class to compute the Derivative Dynamic Time Warping (DDTW) distance between two time series.
    DDTW extends the classical DTW algorithm by comparing the derivatives (rates of change)
    rather than the raw values, making it more sensitive to shape similarities.
    """
    
    def __init__(self, window_size=None)-> None:
        """
        Initialize the DDTW calculator.
        
        Args:
            window_size (int, optional): Size of the warping window.
                                       If None, no window constraint is applied.
                                       If int, restricts the warping path to a window
                                       around the diagonal.
        """
        super().__init__()
        self.type='vec_float'
        
        self.window_size = window_size
    
    def _estimate_derivative(self, series):
        """
        Estimate the first derivative of a time series using a basic
        symmetric difference quotient method.
        
        For a point x[i], the derivative is estimated as:
        d[i] = ((x[i] - x[i-1]) + (x[i+1] - x[i-1])/2) / 2
        
        Args:
            series (list): Input time series
            
        Returns:
            list: Estimated derivatives for the time series
        """
        n = len(series)
        derivatives = []
        
        for i in range(n):
            if i == 0:  # First point
                d = series[1] - series[0]
            elif i == n-1:  # Last point
                d = series[n-1] - series[n-2]
            else:  # Middle points
                d = ((series[i] - series[i-1]) + 
                     (series[i+1] - series[i-1]) / 2) / 2
            derivatives.append(d)
            
        return derivatives
    
    def _calculate_distance_matrix(self, deriv1, deriv2):
        """
        Calculate the local cost matrix between two derivative series.
        
        Args:
            deriv1 (list): First derivative series
            deriv2 (list): Second derivative series
            
        Returns:
            list: 2D distance matrix
        """
        n, m = len(deriv1), len(deriv2)
        distances = [[0] * m for _ in range(n)]
        
        for i in range(n):
            for j in range(m):
                if self.window_size is None or \
                   abs(i - j) <= self.window_size:
                    distances[i][j] = (deriv1[i] - deriv2[j]) ** 2
                else:
                    distances[i][j] = float('inf')
                    
        return distances
    
    def _find_warp_path(self, distances):
        """
        Find the optimal warping path through the distance matrix.
        
        Args:
            distances (list): 2D distance matrix
            
        Returns:
            float: The cumulative distance along the optimal path
        """
        n, m = len(distances), len(distances[0])
        accumulated = [[float('inf')] * m for _ in range(n)]
        
        # Initialize first cell
        accumulated[0][0] = distances[0][0]
        
        # Fill first column and row
        for i in range(1, n):
            accumulated[i][0] = distances[i][0] + accumulated[i-1][0]
        for j in range(1, m):
            accumulated[0][j] = distances[0][j] + accumulated[0][j-1]
        
        # Fill the rest of the matrix
        for i in range(1, n):
            for j in range(1, m):
                if distances[i][j] != float('inf'):
                    accumulated[i][j] = distances[i][j] + min(
                        accumulated[i-1][j],    # vertical
                        accumulated[i][j-1],    # horizontal
                        accumulated[i-1][j-1]   # diagonal
                    )
        
        return accumulated[n-1][m-1]
    
    def compute(self, series1, series2):
        """
        Compute the DDTW distance between two time series.
        
        Args:
            series1 (list): First time series
            series2 (list): Second time series
            
        Returns:
            float: The DDTW distance between the series
            
        Raises:
            ValueError: If either series is too short or empty
        """
        if len(series1) < 2 or len(series2) < 2:
            raise ValueError("Series must have at least 2 points for derivative estimation")
            
        # Estimate derivatives
        deriv1 = self._estimate_derivative(series1)
        deriv2 = self._estimate_derivative(series2)
        
        # Calculate distance matrix
        distances = self._calculate_distance_matrix(deriv1, deriv2)
        
        # Find optimal warping path
        ddtw_distance = self._find_warp_path(distances)
        
        return ddtw_distance
    
    def compute_normalized(self, series1, series2):
        """
        Compute the normalized DDTW distance between two time series.
        
        Args:
            series1 (list): First time series
            series2 (list): Second time series
            
        Returns:
            float: The normalized DDTW distance
        """
        ddtw_distance = self.compute(series1, series2)
        path_length = len(series1) + len(series2)  # Approximate path length
        return ddtw_distance / path_length

cdef class PAADistance(Distance):
    # Attributs de classe
    cdef object __euclidean_distance
    cdef object __normalize_series
    cdef object __compute_paa
    cdef object _type
    cdef object _compute
    cdef object _segments
    '
    A class to compute the Piecewise Aggregate Approximation (PAA) distance between two time series.
    PAA reduces the dimensionality of time series by dividing them into equal-sized segments
    and representing each segment by its mean value. This allows for faster distance computation
    while preserving the overall shape characteristics.
    '

    def __init__(self, *args, **kwargs):
        '
        Initialize the PAA distance calculator.
        
        Args:
            segments (int): Number of segments to divide the time series into.
                          Must be positive and smaller than the series length.
        '
        super().__init__()
        self._type = 'vec_float'
        if (segments < 1):
            raise ValueError('Number of segments must be positive')
        self._segments = segments

    def _compute_paa(self, series):
        '
        Convert a time series to its PAA representation.
        
        Args:
            series (list): Input time series
            
        Returns:
            list: PAA representation of the series (reduced dimension)
            
        Raises:
            ValueError: If series is empty or shorter than number of segments
        '
        if (not series):
            raise ValueError('Series cannot be empty')
        n = len(series)
        if (n < self._segments):
            raise ValueError('Series length must be >= number of segments')
        segment_size = (n / self._segments)
        paa_result = []
        for i in range(self._segments):
            start_idx = int((i * segment_size))
            end_idx = int(((i + 1) * segment_size))
            if (i == (self._segments - 1)):
                end_idx = n
            segment = series[start_idx:end_idx]
            segment_mean = (sum(segment) / len(segment))
            paa_result.append(segment_mean)
        return paa_result

    def _normalize_series(self, series):
        '
        Normalize a time series using z-score normalization.
        
        Args:
            series (list): Input time series
            
        Returns:
            list: Normalized time series
            
        Raises:
            ValueError: If series has zero standard deviation
        '
        n = len(series)
        mean = (sum(series) / n)
        squared_diff_sum = sum((((x - mean) ** 2) for x in series))
        std = ((squared_diff_sum / n) ** 0.5)
        if (std == 0):
            raise ValueError('Series has zero standard deviation')
        return [((x - mean) / std) for x in series]

    def _euclidean_distance(self, series1, series2):
        '
        Compute Euclidean distance between two series of equal length.
        
        Args:
            series1 (list): First series
            series2 (list): Second series
            
        Returns:
            float: Euclidean distance between the series
        '
        return (sum((((a - b) ** 2) for (a, b) in zip(series1, series2))) ** 0.5)

    def compute(self, series1, series2, normalize=True):
        '
        Compute the PAA distance between two time series.
        
        Args:
            series1 (list): First time series
            series2 (list): Second time series
            normalize (bool): Whether to normalize the series before PAA
                            Default is True
            
        Returns:
            float: The PAA distance between the series
            
        Raises:
            ValueError: If either series is invalid
        '
        if normalize:
            series1 = self._normalize_series(series1)
            series2 = self._normalize_series(series2)
        paa1 = self._compute_paa(series1)
        paa2 = self._compute_paa(series2)
        return self._euclidean_distance(paa1, paa2)

    def get_paa_representation(self, series, normalize=True):
        '
        Get the PAA representation of a time series.
        
        Args:
            series (list): Input time series
            normalize (bool): Whether to normalize before PAA
            
        Returns:
            list: PAA representation of the series
        '
        if normalize:
            series = self._normalize_series(series)
        return self._compute_paa(series)

    def compare_multiple_series(self, series_list, normalize=True):
        '
        Compute pairwise PAA distances between multiple time series.
        
        Args:
            series_list (list): List of time series to compare
            normalize (bool): Whether to normalize series
            
        Returns:
            list: Matrix of pairwise distances
        '
        n = len(series_list)
        distances = [([0] * n) for _ in range(n)]
        for i in range(n):
            for j in range((i + 1), n):
                dist = self.compute(series_list[i], series_list[j], normalize)
                distances[i][j] = distances[j][i] = dist
        return distances


    # Propriétés pour accéder aux attributs depuis Python
    @property
    def _euclidean_distance(self):
        return self.__euclidean_distance
    @_euclidean_distance.setter
    def _euclidean_distance(self, value):
        self.__euclidean_distance = value
    @property
    def _normalize_series(self):
        return self.__normalize_series
    @_normalize_series.setter
    def _normalize_series(self, value):
        self.__normalize_series = value
    @property
    def _compute_paa(self):
        return self.__compute_paa
    @_compute_paa.setter
    def _compute_paa(self, value):
        self.__compute_paa = value
    @property
    def type(self):
        return self._type
    @type.setter
    def type(self, value):
        self._type = value
    @property
    def compute(self):
        return self._compute
    @compute.setter
    def compute(self, value):
        self._compute = value
    @property
    def segments(self):
        return self._segments
    @segments.setter
    def segments(self, value):
        self._segments = value
    """
    A class to compute the Piecewise Aggregate Approximation (PAA) distance between two time series.
    PAA reduces the dimensionality of time series by dividing them into equal-sized segments
    and representing each segment by its mean value. This allows for faster distance computation
    while preserving the overall shape characteristics.
    """
    
    def __init__(self, segments=8)-> None:
        """
        Initialize the PAA distance calculator.
        
        Args:
            segments (int): Number of segments to divide the time series into.
                          Must be positive and smaller than the series length.
        """
        super().__init__()
        self.type='vec_float'
        
        if segments < 1:
            raise ValueError("Number of segments must be positive")
        self.segments = segments
    
    def _compute_paa(self, series):
        """
        Convert a time series to its PAA representation.
        
        Args:
            series (list): Input time series
            
        Returns:
            list: PAA representation of the series (reduced dimension)
            
        Raises:
            ValueError: If series is empty or shorter than number of segments
        """
        if not series:
            raise ValueError("Series cannot be empty")
            
        n = len(series)
        if n < self.segments:
            raise ValueError("Series length must be >= number of segments")
        
        # Calculate segment size (can be floating point)
        segment_size = n / self.segments
        
        paa_result = []
        for i in range(self.segments):
            # Calculate segment boundaries
            start_idx = int(i * segment_size)
            end_idx = int((i + 1) * segment_size)
            
            # Handle the case where end_idx exactly equals the series length
            if i == self.segments - 1:
                end_idx = n
            
            # Extract segment and calculate mean
            segment = series[start_idx:end_idx]
            segment_mean = sum(segment) / len(segment)
            paa_result.append(segment_mean)
            
        return paa_result
    
    def _normalize_series(self, series):
        """
        Normalize a time series using z-score normalization.
        
        Args:
            series (list): Input time series
            
        Returns:
            list: Normalized time series
            
        Raises:
            ValueError: If series has zero standard deviation
        """
        n = len(series)
        mean = sum(series) / n
        
        # Calculate standard deviation
        squared_diff_sum = sum((x - mean) ** 2 for x in series)
        std = (squared_diff_sum / n) ** 0.5
        
        if std == 0:
            raise ValueError("Series has zero standard deviation")
            
        return [(x - mean) / std for x in series]
    
    def _euclidean_distance(self, series1, series2):
        """
        Compute Euclidean distance between two series of equal length.
        
        Args:
            series1 (list): First series
            series2 (list): Second series
            
        Returns:
            float: Euclidean distance between the series
        """
        return sum((a - b) ** 2 for a, b in zip(series1, series2)) ** 0.5
    
    def compute(self, series1, series2, normalize=True):
        """
        Compute the PAA distance between two time series.
        
        Args:
            series1 (list): First time series
            series2 (list): Second time series
            normalize (bool): Whether to normalize the series before PAA
                            Default is True
            
        Returns:
            float: The PAA distance between the series
            
        Raises:
            ValueError: If either series is invalid
        """
        # Optionally normalize the series
        if normalize:
            series1 = self._normalize_series(series1)
            series2 = self._normalize_series(series2)
        
        # Convert to PAA representation
        paa1 = self._compute_paa(series1)
        paa2 = self._compute_paa(series2)
        
        # Compute Euclidean distance between PAA representations
        return self._euclidean_distance(paa1, paa2)
    
    def get_paa_representation(self, series, normalize=True):
        """
        Get the PAA representation of a time series.
        
        Args:
            series (list): Input time series
            normalize (bool): Whether to normalize before PAA
            
        Returns:
            list: PAA representation of the series
        """
        if normalize:
            series = self._normalize_series(series)
        return self._compute_paa(series)
    
    def compare_multiple_series(self, series_list, normalize=True):
        """
        Compute pairwise PAA distances between multiple time series.
        
        Args:
            series_list (list): List of time series to compare
            normalize (bool): Whether to normalize series
            
        Returns:
            list: Matrix of pairwise distances
        """
        n = len(series_list)
        distances = [[0] * n for _ in range(n)]
        
        for i in range(n):
            for j in range(i + 1, n):
                dist = self.compute(series_list[i], series_list[j], normalize)
                distances[i][j] = distances[j][i] = dist
                
        return distances
        
cdef class SAXDistance(Distance):
    # Attributs de classe
    cdef object __paa_transform
    cdef object __normalize_series
    cdef object _alphabet_size
    cdef object _word_length
    cdef object _transform
    cdef object _breakpoints
    cdef object _type
    cdef object __mindist
    cdef object __convert_to_sax
    '
    A class to compute the Symbolic Aggregate Approximation (SAX) distance between two time series.
    SAX first reduces the dimensionality using PAA, then converts the numerical series into
    a symbolic string representation using breakpoints that produce equal-sized areas under
    a Gaussian curve.
    '

    def __init__(self, *args, **kwargs):
        '
        Initialize the SAX distance calculator.
        
        Args:
            word_length (int): Length of the symbolic representation (number of segments)
            alphabet_size (int): Size of the alphabet for symbolic representation
                               Must be between 2 and 10
        '
        super().__init__()
        self._type = 'vec_float'
        if (not (2 <= alphabet_size <= 10)):
            raise ValueError('Alphabet size must be between 2 and 10')
        self._word_length = word_length
        self._alphabet_size = alphabet_size
        self._breakpoints = {2: [(- float('inf')), 0.0, float('inf')], 3: [(- float('inf')), (- 0.43), 0.43, float('inf')], 4: [(- float('inf')), (- 0.67), 0.0, 0.67, float('inf')], 5: [(- float('inf')), (- 0.84), (- 0.25), 0.25, 0.84, float('inf')], 6: [(- float('inf')), (- 0.97), (- 0.43), 0.0, 0.43, 0.97, float('inf')], 7: [(- float('inf')), (- 1.07), (- 0.57), (- 0.18), 0.18, 0.57, 1.07, float('inf')], 8: [(- float('inf')), (- 1.15), (- 0.67), (- 0.32), 0.0, 0.32, 0.67, 1.15, float('inf')], 9: [(- float('inf')), (- 1.22), (- 0.76), (- 0.43), (- 0.14), 0.14, 0.43, 0.76, 1.22, float('inf')], 10: [(- float('inf')), (- 1.28), (- 0.84), (- 0.52), (- 0.25), 0.0, 0.25, 0.52, 0.84, 1.28, float('inf')]}

    def _normalize_series(self, series):
        '
        Normalize a time series using z-score normalization.
        
        Args:
            series (list): Input time series
            
        Returns:
            list: Normalized time series
        '
        n = len(series)
        mean = (sum(series) / n)
        squared_diff_sum = sum((((x - mean) ** 2) for x in series))
        std = ((squared_diff_sum / n) ** 0.5)
        if (std == 0):
            raise ValueError('Series has zero standard deviation')
        return [((x - mean) / std) for x in series]

    def _paa_transform(self, series):
        '
        Transform time series using Piecewise Aggregate Approximation.
        
        Args:
            series (list): Input time series
            
        Returns:
            list: PAA representation
        '
        n = len(series)
        segment_size = (n / self._word_length)
        paa_result = []
        for i in range(self._word_length):
            start_idx = int((i * segment_size))
            end_idx = int(((i + 1) * segment_size))
            if (i == (self._word_length - 1)):
                end_idx = n
            segment = series[start_idx:end_idx]
            paa_result.append((sum(segment) / len(segment)))
        return paa_result

    def _convert_to_sax(self, paa_series):
        '
        Convert PAA series to SAX symbols.
        
        Args:
            paa_series (list): PAA representation of time series
            
        Returns:
            str: SAX symbolic representation
        '
        breakpoints = self._breakpoints[self._alphabet_size]
        symbols = 'abcdefghij'[:self._alphabet_size]
        sax_string = ''
        for value in paa_series:
            for i in range((len(breakpoints) - 1)):
                if (breakpoints[i] <= value < breakpoints[(i + 1)]):
                    sax_string += symbols[i]
                    break
        return sax_string

    def _mindist(self, sax1, sax2):
        '
        Compute the minimum distance between two SAX representations.
        
        Args:
            sax1 (str): First SAX string
            sax2 (str): Second SAX string
            
        Returns:
            float: MINDIST value between the strings
        '
        if (len(sax1) != len(sax2)):
            raise ValueError('SAX strings must have equal length')
        breakpoints = self._breakpoints[self._alphabet_size]
        symbols = 'abcdefghij'[:self._alphabet_size]
        dist = 0
        for (c1, c2) in zip(sax1, sax2):
            i1 = symbols.index(c1)
            i2 = symbols.index(c2)
            if (abs((i1 - i2)) > 1):
                cell_dist = (breakpoints[max(i1, i2)] - breakpoints[(min(i1, i2) + 1)])
                dist += (cell_dist * cell_dist)
        return ((len(sax1) / self._word_length) * (dist ** 0.5))

    def transform(self, series):
        '
        Transform a time series to its SAX representation.
        
        Args:
            series (list): Input time series
            
        Returns:
            tuple: (PAA representation, SAX string)
        '
        normalized = self._normalize_series(series)
        paa = self._paa_transform(normalized)
        sax = self._convert_to_sax(paa)
        return (paa, sax)

    def compute(self, series1, series2):
        '
        Compute the SAX distance between two time series.
        
        Args:
            series1 (list): First time series
            series2 (list): Second time series
            
        Returns:
            tuple: (SAX strings, MINDIST value)
        '
        (_, sax1) = self.transform(series1)
        (_, sax2) = self.transform(series2)
        distance = self._mindist(sax1, sax2)
        return ((sax1, sax2), distance)


    # Propriétés pour accéder aux attributs depuis Python
    @property
    def _paa_transform(self):
        return self.__paa_transform
    @_paa_transform.setter
    def _paa_transform(self, value):
        self.__paa_transform = value
    @property
    def _normalize_series(self):
        return self.__normalize_series
    @_normalize_series.setter
    def _normalize_series(self, value):
        self.__normalize_series = value
    @property
    def alphabet_size(self):
        return self._alphabet_size
    @alphabet_size.setter
    def alphabet_size(self, value):
        self._alphabet_size = value
    @property
    def word_length(self):
        return self._word_length
    @word_length.setter
    def word_length(self, value):
        self._word_length = value
    @property
    def transform(self):
        return self._transform
    @transform.setter
    def transform(self, value):
        self._transform = value
    @property
    def breakpoints(self):
        return self._breakpoints
    @breakpoints.setter
    def breakpoints(self, value):
        self._breakpoints = value
    @property
    def type(self):
        return self._type
    @type.setter
    def type(self, value):
        self._type = value
    @property
    def _mindist(self):
        return self.__mindist
    @_mindist.setter
    def _mindist(self, value):
        self.__mindist = value
    @property
    def _convert_to_sax(self):
        return self.__convert_to_sax
    @_convert_to_sax.setter
    def _convert_to_sax(self, value):
        self.__convert_to_sax = value
    """
    A class to compute the Symbolic Aggregate Approximation (SAX) distance between two time series.
    SAX first reduces the dimensionality using PAA, then converts the numerical series into
    a symbolic string representation using breakpoints that produce equal-sized areas under
    a Gaussian curve.
    """
    
    def __init__(self, word_length=8, alphabet_size=4)-> None:
        """
        Initialize the SAX distance calculator.
        
        Args:
            word_length (int): Length of the symbolic representation (number of segments)
            alphabet_size (int): Size of the alphabet for symbolic representation
                               Must be between 2 and 10
        """
        super().__init__()
        self.type='vec_float'
        
        if not 2 <= alphabet_size <= 10:
            raise ValueError("Alphabet size must be between 2 and 10")
        
        self.word_length = word_length
        self.alphabet_size = alphabet_size
        # Breakpoints table for standard normal distribution
        # Pre-computed for alphabet sizes 2-10
        self.breakpoints = {
            2: [-float('inf'), 0.00, float('inf')],
            3: [-float('inf'), -0.43, 0.43, float('inf')],
            4: [-float('inf'), -0.67, 0.00, 0.67, float('inf')],
            5: [-float('inf'), -0.84, -0.25, 0.25, 0.84, float('inf')],
            6: [-float('inf'), -0.97, -0.43, 0.00, 0.43, 0.97, float('inf')],
            7: [-float('inf'), -1.07, -0.57, -0.18, 0.18, 0.57, 1.07, float('inf')],
            8: [-float('inf'), -1.15, -0.67, -0.32, 0.00, 0.32, 0.67, 1.15, float('inf')],
            9: [-float('inf'), -1.22, -0.76, -0.43, -0.14, 0.14, 0.43, 0.76, 1.22, float('inf')],
            10: [-float('inf'), -1.28, -0.84, -0.52, -0.25, 0.00, 0.25, 0.52, 0.84, 1.28, float('inf')]
        }
    
    def _normalize_series(self, series):
        """
        Normalize a time series using z-score normalization.
        
        Args:
            series (list): Input time series
            
        Returns:
            list: Normalized time series
        """
        n = len(series)
        mean = sum(series) / n
        squared_diff_sum = sum((x - mean) ** 2 for x in series)
        std = (squared_diff_sum / n) ** 0.5
        
        if std == 0:
            raise ValueError("Series has zero standard deviation")
            
        return [(x - mean) / std for x in series]
    
    def _paa_transform(self, series):
        """
        Transform time series using Piecewise Aggregate Approximation.
        
        Args:
            series (list): Input time series
            
        Returns:
            list: PAA representation
        """
        n = len(series)
        segment_size = n / self.word_length
        paa_result = []
        
        for i in range(self.word_length):
            start_idx = int(i * segment_size)
            end_idx = int((i + 1) * segment_size)
            if i == self.word_length - 1:
                end_idx = n
                
            segment = series[start_idx:end_idx]
            paa_result.append(sum(segment) / len(segment))
            
        return paa_result
    
    def _convert_to_sax(self, paa_series):
        """
        Convert PAA series to SAX symbols.
        
        Args:
            paa_series (list): PAA representation of time series
            
        Returns:
            str: SAX symbolic representation
        """
        breakpoints = self.breakpoints[self.alphabet_size]
        symbols = 'abcdefghij'[:self.alphabet_size]  # Use first alphabet_size letters
        
        sax_string = ''
        for value in paa_series:
            # Find the symbol corresponding to the value's position
            for i in range(len(breakpoints) - 1):
                if breakpoints[i] <= value < breakpoints[i + 1]:
                    sax_string += symbols[i]
                    break
                    
        return sax_string
    
    def _mindist(self, sax1, sax2):
        """
        Compute the minimum distance between two SAX representations.
        
        Args:
            sax1 (str): First SAX string
            sax2 (str): Second SAX string
            
        Returns:
            float: MINDIST value between the strings
        """
        if len(sax1) != len(sax2):
            raise ValueError("SAX strings must have equal length")
            
        breakpoints = self.breakpoints[self.alphabet_size]
        symbols = 'abcdefghij'[:self.alphabet_size]
        
        dist = 0
        for c1, c2 in zip(sax1, sax2):
            # Get indices of symbols
            i1 = symbols.index(c1)
            i2 = symbols.index(c2)
            
            # If indices differ by more than 1, add to distance
            if abs(i1 - i2) > 1:
                # Use pre-computed breakpoints to calculate distance
                cell_dist = breakpoints[max(i1, i2)] - breakpoints[min(i1, i2) + 1]
                dist += cell_dist * cell_dist
                
        return (len(sax1) / self.word_length) * (dist ** 0.5)
    
    def transform(self, series):
        """
        Transform a time series to its SAX representation.
        
        Args:
            series (list): Input time series
            
        Returns:
            tuple: (PAA representation, SAX string)
        """
        normalized = self._normalize_series(series)
        paa = self._paa_transform(normalized)
        sax = self._convert_to_sax(paa)
        return paa, sax
    
    def compute(self, series1, series2):
        """
        Compute the SAX distance between two time series.
        
        Args:
            series1 (list): First time series
            series2 (list): Second time series
            
        Returns:
            tuple: (SAX strings, MINDIST value)
        """
        # Transform both series
        _, sax1 = self.transform(series1)
        _, sax2 = self.transform(series2)
        
        # Compute MINDIST
        distance = self._mindist(sax1, sax2)
        
        return (sax1, sax2), distance
import math   
cdef class SoftDTWDistance(Distance):
    # Attributs de classe
    cdef object __normalize_series
    cdef object __soft_min
    cdef object __squared_euclidean
    cdef object _gamma
    cdef object __compute_accumulated_cost_matrix
    cdef object _type
    cdef object __compute_cost_matrix
    '
    A class to compute the Soft Dynamic Time Warping (Soft-DTW) distance between two time series.
    Soft-DTW is a differentiable version of DTW that replaces the min operator with a
    soft minimum, making it suitable for gradient-based optimization.
    
    The soft minimum is computed using the log-sum-exp trick for numerical stability.
    '

    def __init__(self, *args, **kwargs):
        '
        Initialize the Soft-DTW calculator.
        
        Args:
            gamma (float): Smoothing parameter. Controls the smoothness of the soft minimum.
                         Lower values make it closer to regular DTW.
                         Must be positive. Default is 1.0.
        '
        super().__init__()
        self._type = 'vec_float'
        if (gamma <= 0):
            raise ValueError('Gamma must be positive')
        self._gamma = gamma

    def _soft_min(self, values):
        '
        Compute the soft minimum of a list of values using the log-sum-exp trick.
        
        Args:
            values (list): List of values to compute soft minimum
            
        Returns:
            float: Soft minimum value
        '
        min_val = min(values)
        exp_sum = sum((math.exp(((- (val - min_val)) / self._gamma)) for val in values))
        return (((- self._gamma) * math.log(exp_sum)) + min_val)

    def _squared_euclidean(self, x, y):
        '
        Compute squared Euclidean distance between two points.
        
        Args:
            x (float): First point
            y (float): Second point
            
        Returns:
            float: Squared distance between points
        '
        return ((x - y) ** 2)

    def _compute_cost_matrix(self, series1, series2):
        '
        Compute the cost matrix between two series using squared Euclidean distance.
        
        Args:
            series1 (list): First time series
            series2 (list): Second time series
            
        Returns:
            list: 2D cost matrix
        '
        (n, m) = (len(series1), len(series2))
        cost_matrix = [([0] * m) for _ in range(n)]
        for i in range(n):
            for j in range(m):
                cost_matrix[i][j] = self._squared_euclidean(series1[i], series2[j])
        return cost_matrix

    def _compute_accumulated_cost_matrix(self, cost_matrix):
        '
        Compute the accumulated cost matrix using soft minimum.
        
        Args:
            cost_matrix (list): Cost matrix between two series
            
        Returns:
            list: Accumulated cost matrix
        '
        (n, m) = (len(cost_matrix), len(cost_matrix[0]))
        D = [([float('inf')] * (m + 1)) for _ in range((n + 1))]
        D[0][0] = 0
        for i in range(1, (n + 1)):
            D[i][0] = float('inf')
        for j in range(1, (m + 1)):
            D[0][j] = float('inf')
        for i in range(1, (n + 1)):
            for j in range(1, (m + 1)):
                cost = cost_matrix[(i - 1)][(j - 1)]
                D[i][j] = (cost + self._soft_min([D[(i - 1)][j], D[i][(j - 1)], D[(i - 1)][(j - 1)]]))
        return D

    def _normalize_series(self, series):
        '
        Normalize a time series using z-score normalization.
        
        Args:
            series (list): Input time series
            
        Returns:
            list: Normalized time series
        '
        n = len(series)
        mean = (sum(series) / n)
        squared_diff_sum = sum((((x - mean) ** 2) for x in series))
        std = ((squared_diff_sum / n) ** 0.5)
        if (std == 0):
            raise ValueError('Series has zero standard deviation')
        return [((x - mean) / std) for x in series]

    def compute(self, series1, series2, normalize=True):
        '
        Compute the Soft-DTW distance between two time series.
        
        Args:
            series1 (list): First time series
            series2 (list): Second time series
            normalize (bool): Whether to normalize the series. Default is True
            
        Returns:
            float: The Soft-DTW distance between the series
        '
        if normalize:
            series1 = self._normalize_series(series1)
            series2 = self._normalize_series(series2)
        cost_matrix = self._compute_cost_matrix(series1, series2)
        D = self._compute_accumulated_cost_matrix(cost_matrix)
        return D[(- 1)][(- 1)]

    def compute_gradient(self, series1, series2, normalize=True):
        '
        Compute the gradient of Soft-DTW with respect to the first series.
        
        Args:
            series1 (list): First time series
            series2 (list): Second time series
            normalize (bool): Whether to normalize the series
            
        Returns:
            list: Gradient of Soft-DTW with respect to series1
        '
        if normalize:
            series1 = self._normalize_series(series1)
            series2 = self._normalize_series(series2)
        (n, m) = (len(series1), len(series2))
        cost_matrix = self._compute_cost_matrix(series1, series2)
        D = self._compute_accumulated_cost_matrix(cost_matrix)
        gradient = ([0] * n)
        for i in range(n):
            partial_sum = 0
            for j in range(m):
                if (D[(i + 1)][(j + 1)] < float('inf')):
                    partial_sum += (2 * (series1[i] - series2[j]))
            gradient[i] = partial_sum
        return gradient


    # Propriétés pour accéder aux attributs depuis Python
    @property
    def _normalize_series(self):
        return self.__normalize_series
    @_normalize_series.setter
    def _normalize_series(self, value):
        self.__normalize_series = value
    @property
    def _soft_min(self):
        return self.__soft_min
    @_soft_min.setter
    def _soft_min(self, value):
        self.__soft_min = value
    @property
    def _squared_euclidean(self):
        return self.__squared_euclidean
    @_squared_euclidean.setter
    def _squared_euclidean(self, value):
        self.__squared_euclidean = value
    @property
    def gamma(self):
        return self._gamma
    @gamma.setter
    def gamma(self, value):
        self._gamma = value
    @property
    def _compute_accumulated_cost_matrix(self):
        return self.__compute_accumulated_cost_matrix
    @_compute_accumulated_cost_matrix.setter
    def _compute_accumulated_cost_matrix(self, value):
        self.__compute_accumulated_cost_matrix = value
    @property
    def type(self):
        return self._type
    @type.setter
    def type(self, value):
        self._type = value
    @property
    def _compute_cost_matrix(self):
        return self.__compute_cost_matrix
    @_compute_cost_matrix.setter
    def _compute_cost_matrix(self, value):
        self.__compute_cost_matrix = value
    """
    A class to compute the Soft Dynamic Time Warping (Soft-DTW) distance between two time series.
    Soft-DTW is a differentiable version of DTW that replaces the min operator with a
    soft minimum, making it suitable for gradient-based optimization.
    
    The soft minimum is computed using the log-sum-exp trick for numerical stability.
    """
    
    def __init__(self, gamma=1.0)-> None:
        """
        Initialize the Soft-DTW calculator.
        
        Args:
            gamma (float): Smoothing parameter. Controls the smoothness of the soft minimum.
                         Lower values make it closer to regular DTW.
                         Must be positive. Default is 1.0.
        """
        super().__init__()
        self.type='vec_float'
        
        if gamma <= 0:
            raise ValueError("Gamma must be positive")
        self.gamma = gamma
    
    def _soft_min(self, values):
        """
        Compute the soft minimum of a list of values using the log-sum-exp trick.
        
        Args:
            values (list): List of values to compute soft minimum
            
        Returns:
            float: Soft minimum value
        """
        min_val = min(values)
        exp_sum = sum(
            math.exp(-(val - min_val) / self.gamma) 
            for val in values
        )
        return -self.gamma * math.log(exp_sum) + min_val
    
    def _squared_euclidean(self, x, y):
        """
        Compute squared Euclidean distance between two points.
        
        Args:
            x (float): First point
            y (float): Second point
            
        Returns:
            float: Squared distance between points
        """
        return (x - y) ** 2
    
    def _compute_cost_matrix(self, series1, series2):
        """
        Compute the cost matrix between two series using squared Euclidean distance.
        
        Args:
            series1 (list): First time series
            series2 (list): Second time series
            
        Returns:
            list: 2D cost matrix
        """
        n, m = len(series1), len(series2)
        cost_matrix = [[0] * m for _ in range(n)]
        
        for i in range(n):
            for j in range(m):
                cost_matrix[i][j] = self._squared_euclidean(series1[i], series2[j])
                
        return cost_matrix
    
    def _compute_accumulated_cost_matrix(self, cost_matrix):
        """
        Compute the accumulated cost matrix using soft minimum.
        
        Args:
            cost_matrix (list): Cost matrix between two series
            
        Returns:
            list: Accumulated cost matrix
        """
        n, m = len(cost_matrix), len(cost_matrix[0])
        D = [[float('inf')] * (m + 1) for _ in range(n + 1)]
        
        # Initialize first row and column
        D[0][0] = 0
        for i in range(1, n + 1):
            D[i][0] = float('inf')
        for j in range(1, m + 1):
            D[0][j] = float('inf')
        
        # Fill the matrix using soft minimum
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                cost = cost_matrix[i-1][j-1]
                D[i][j] = cost + self._soft_min([
                    D[i-1][j],     # insertion
                    D[i][j-1],     # deletion
                    D[i-1][j-1]    # match
                ])
                
        return D
    
    def _normalize_series(self, series):
        """
        Normalize a time series using z-score normalization.
        
        Args:
            series (list): Input time series
            
        Returns:
            list: Normalized time series
        """
        n = len(series)
        mean = sum(series) / n
        squared_diff_sum = sum((x - mean) ** 2 for x in series)
        std = (squared_diff_sum / n) ** 0.5
        
        if std == 0:
            raise ValueError("Series has zero standard deviation")
            
        return [(x - mean) / std for x in series]
    
    def compute(self, series1, series2, normalize=True):
        """
        Compute the Soft-DTW distance between two time series.
        
        Args:
            series1 (list): First time series
            series2 (list): Second time series
            normalize (bool): Whether to normalize the series. Default is True
            
        Returns:
            float: The Soft-DTW distance between the series
        """
        if normalize:
            series1 = self._normalize_series(series1)
            series2 = self._normalize_series(series2)
            
        cost_matrix = self._compute_cost_matrix(series1, series2)
        D = self._compute_accumulated_cost_matrix(cost_matrix)
        
        return D[-1][-1]
    
    def compute_gradient(self, series1, series2, normalize=True):
        """
        Compute the gradient of Soft-DTW with respect to the first series.
        
        Args:
            series1 (list): First time series
            series2 (list): Second time series
            normalize (bool): Whether to normalize the series
            
        Returns:
            list: Gradient of Soft-DTW with respect to series1
        """
        if normalize:
            series1 = self._normalize_series(series1)
            series2 = self._normalize_series(series2)
            
        n, m = len(series1), len(series2)
        cost_matrix = self._compute_cost_matrix(series1, series2)
        D = self._compute_accumulated_cost_matrix(cost_matrix)
        
        # Compute gradient using backpropagation
        gradient = [0] * n
        for i in range(n):
            partial_sum = 0
            for j in range(m):
                if D[i+1][j+1] < float('inf'):
                    # Contribution to gradient from each path
                    partial_sum += 2 * (series1[i] - series2[j])
            gradient[i] = partial_sum
            
        return gradient
        


import math
from typing import List, Union
import warnings

cdef class GlobalAlignmentKernel(Distance):
    # Attributs de classe
    cdef object _triangular
    cdef object _sigma
    cdef object __local_kernel
    cdef object _type
    cdef object _compute
    '
    Implementation of the Global Alignment Kernel (GAK) for time series similarity computation.
    GAK combines Dynamic Time Warping alignment with a kernel-based similarity measure.
    
    References:
    Cuturi, M., Vert, J. P., Birkenes, O., & Matsui, T. (2007). 
    A Kernel for Time Series Based on Global Alignments.
    '

    def __init__(self, *args, **kwargs):
        '
        Initialize the GAK calculator.
        
        Args:
            sigma: The bandwidth parameter for the Gaussian kernel
            triangular: Whether to use the triangular local kernel (True) or 
                       Gaussian kernel (False, default)
        '
        super().__init__()
        self._type = 'vec_float'
        self._sigma = sigma
        self._triangular = triangular

    def _local_kernel(self, x: float, y: float) -> float:
        '
        Compute the local kernel between two scalar values.
        
        Args:
            x: First scalar value
            y: Second scalar value
            
        Returns:
            float: Local kernel value
        '
        if self._triangular:
            return max(0, (1 - (abs((x - y)) / self._sigma)))
        else:
            return math.exp(((- ((x - y) ** 2)) / (2 * (self._sigma ** 2))))

    def compute(self, x: List[float], y: List[float]) -> float:
        '
        Compute the Global Alignment Kernel between two time series.
        
        Args:
            x: First time series (list of float values)
            y: Second time series (list of float values)
            
        Returns:
            float: GAK similarity value between the two series
        
        Example:
            >>> gak = GlobalAlignmentKernel(sigma=1.0)
            >>> ts1 = [1.0, 2.0, 3.0, 2.0, 1.0]
            >>> ts2 = [1.0, 2.0, 2.5, 2.0, 1.0]
            >>> similarity = gak.compute(ts1, ts2)
        '
        (n, m) = (len(x), len(y))
        dp = [([0.0] * (m + 1)) for _ in range((n + 1))]
        for i in range((n + 1)):
            dp[i][0] = 0.0
        for j in range((m + 1)):
            dp[0][j] = 0.0
        dp[0][0] = 1.0
        for i in range(1, (n + 1)):
            for j in range(1, (m + 1)):
                local_sim = self._local_kernel(x[(i - 1)], y[(j - 1)])
                dp[i][j] = (local_sim * ((dp[(i - 1)][(j - 1)] + dp[(i - 1)][j]) + dp[i][(j - 1)]))
        return dp[n][m]

    def normalized_compute(self, x: List[float], y: List[float]) -> float:
        '
        Compute the normalized Global Alignment Kernel between two time series.
        Normalization helps make the kernel values more comparable across different time series.
        
        Args:
            x: First time series (list of float values)
            y: Second time series (list of float values)
            
        Returns:
            float: Normalized GAK similarity value between the two series
        '
        gak_xx = self.compute(x, x)
        gak_yy = self.compute(y, y)
        gak_xy = self.compute(x, y)
        if ((gak_xx * gak_yy) <= 0):
            warnings.warn('Zero or negative self-similarity detected. Check your data and sigma parameter.')
            return 0.0
        return (gak_xy / math.sqrt((gak_xx * gak_yy)))


    # Propriétés pour accéder aux attributs depuis Python
    @property
    def triangular(self):
        return self._triangular
    @triangular.setter
    def triangular(self, value):
        self._triangular = value
    @property
    def sigma(self):
        return self._sigma
    @sigma.setter
    def sigma(self, value):
        self._sigma = value
    @property
    def _local_kernel(self):
        return self.__local_kernel
    @_local_kernel.setter
    def _local_kernel(self, value):
        self.__local_kernel = value
    @property
    def type(self):
        return self._type
    @type.setter
    def type(self, value):
        self._type = value
    @property
    def compute(self):
        return self._compute
    @compute.setter
    def compute(self, value):
        self._compute = value
    """
    Implementation of the Global Alignment Kernel (GAK) for time series similarity computation.
    GAK combines Dynamic Time Warping alignment with a kernel-based similarity measure.
    
    References:
    Cuturi, M., Vert, J. P., Birkenes, O., & Matsui, T. (2007). 
    A Kernel for Time Series Based on Global Alignments.
    """
    
    def __init__(self, sigma: float = 1.0, triangular: bool = False)-> None:
        """
        Initialize the GAK calculator.
        
        Args:
            sigma: The bandwidth parameter for the Gaussian kernel
            triangular: Whether to use the triangular local kernel (True) or 
                       Gaussian kernel (False, default)
        """
        super().__init__()
        self.type='vec_float'
        
        self.sigma = sigma
        self.triangular = triangular
    
    def _local_kernel(self, x: float, y: float) -> float:
        """
        Compute the local kernel between two scalar values.
        
        Args:
            x: First scalar value
            y: Second scalar value
            
        Returns:
            float: Local kernel value
        """
        if self.triangular:
            return max(0, 1 - abs(x - y) / self.sigma)
        else:
            return math.exp(-((x - y) ** 2) / (2 * self.sigma ** 2))
    
    def compute(self, x: List[float], y: List[float]) -> float:
        """
        Compute the Global Alignment Kernel between two time series.
        
        Args:
            x: First time series (list of float values)
            y: Second time series (list of float values)
            
        Returns:
            float: GAK similarity value between the two series
        
        Example:
            >>> gak = GlobalAlignmentKernel(sigma=1.0)
            >>> ts1 = [1.0, 2.0, 3.0, 2.0, 1.0]
            >>> ts2 = [1.0, 2.0, 2.5, 2.0, 1.0]
            >>> similarity = gak.compute(ts1, ts2)
        """
        n, m = len(x), len(y)
        
        # Initialize the dynamic programming matrix
        dp = [[0.0] * (m + 1) for _ in range(n + 1)]
        
        # Base cases
        for i in range(n + 1):
            dp[i][0] = 0.0
        for j in range(m + 1):
            dp[0][j] = 0.0
        dp[0][0] = 1.0
        
        # Fill the dynamic programming matrix
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                local_sim = self._local_kernel(x[i-1], y[j-1])
                
                dp[i][j] = local_sim * (
                    dp[i-1][j-1] +  # diagonal
                    dp[i-1][j] +    # vertical
                    dp[i][j-1]      # horizontal
                )
        
        # The final GAK value is in the bottom-right corner
        return dp[n][m]
    
    def normalized_compute(self, x: List[float], y: List[float]) -> float:
        """
        Compute the normalized Global Alignment Kernel between two time series.
        Normalization helps make the kernel values more comparable across different time series.
        
        Args:
            x: First time series (list of float values)
            y: Second time series (list of float values)
            
        Returns:
            float: Normalized GAK similarity value between the two series
        """
        gak_xx = self.compute(x, x)
        gak_yy = self.compute(y, y)
        gak_xy = self.compute(x, y)
        
        # Avoid numerical issues with very small values
        if gak_xx * gak_yy <= 0:
            warnings.warn("Zero or negative self-similarity detected. Check your data and sigma parameter.")
            return 0.0
            
        return gak_xy / math.sqrt(gak_xx * gak_yy)
        
from typing import List, Union
from math import inf

cdef class MSMDistance(Distance):
    # Attributs de classe
    cdef object _type
    cdef object _c
    cdef object __cost_split_merge
    cdef object _compute
    '
    Implementation of Move-Split-Merge (MSM) distance for time series comparison.
    MSM is an elastic distance measure that allows three operations:
    - Move: Change a value to another value (cost = |x - y|)
    - Split: Split one value into two values (cost = c)
    - Merge: Merge two values into one value (cost = c)
    
    The cost parameter c controls the relative cost of split/merge operations
    compared to move operations.
    
    Reference:
    Stefan, A., Athitsos, V., & Das, G. (2013). The move-split-merge metric for time series.
    IEEE Transactions on Knowledge and Data Engineering, 25(6), 1425-1438.
    '

    def __init__(self, *args, **kwargs):
        '
        Initialize the MSM distance calculator.
        
        Args:
            c: Cost parameter for split and merge operations.
               Higher values make split/merge operations more expensive.
        '
        super().__init__()
        self._type = 'vec_float'
        self._c = c

    def _cost_split_merge(self, x: float, y1: float, y2: float) -> float:
        '
        Calculate the minimum cost of splitting x to match y1,y2 or
        merging y1,y2 to match x.
        
        Args:
            x: Single value potentially being split or merged to
            y1: First value of the pair
            y2: Second value of the pair
            
        Returns:
            float: Minimum cost between split and merge operations
        '
        cost_split = (self._c + abs((x - y1)))
        cost_merge = (self._c + abs((y2 - x)))
        return min(cost_split, cost_merge)

    def compute(self, x: List[float], y: List[float]) -> float:
        '
        Compute the MSM distance between two time series.
        
        Args:
            x: First time series (list of float values)
            y: Second time series (list of float values)
            
        Returns:
            float: MSM distance between the two series
            
        Example:
            >>> msm = MSMDistance(c=0.5)
            >>> ts1 = [1.0, 2.0, 3.0, 2.0, 1.0]
            >>> ts2 = [1.0, 2.0, 2.5, 2.0, 1.0]
            >>> distance = msm.compute(ts1, ts2)
        '
        (n, m) = (len(x), len(y))
        dp = [([inf] * (m + 1)) for _ in range((n + 1))]
        dp[0][0] = 0
        for i in range(1, (n + 1)):
            dp[i][0] = (dp[(i - 1)][0] + self._c)
        for j in range(1, (m + 1)):
            dp[0][j] = (dp[0][(j - 1)] + self._c)
        for i in range(1, (n + 1)):
            for j in range(1, (m + 1)):
                cost_move = (dp[(i - 1)][(j - 1)] + abs((x[(i - 1)] - y[(j - 1)])))
                cost_split_merge = inf
                if (i > 1):
                    cost_split_merge = min(cost_split_merge, (dp[(i - 2)][(j - 1)] + self._cost_split_merge(y[(j - 1)], x[(i - 2)], x[(i - 1)])))
                if (j > 1):
                    cost_split_merge = min(cost_split_merge, (dp[(i - 1)][(j - 2)] + self._cost_split_merge(x[(i - 1)], y[(j - 2)], y[(j - 1)])))
                dp[i][j] = min(cost_move, cost_split_merge)
        return dp[n][m]

    def normalized_compute(self, x: List[float], y: List[float]) -> float:
        '
        Compute the normalized MSM distance between two time series.
        Normalization is done by dividing by the length of the longer series.
        
        Args:
            x: First time series (list of float values)
            y: Second time series (list of float values)
            
        Returns:
            float: Normalized MSM distance between the two series
        '
        raw_distance = self.compute(x, y)
        normalization_factor = max(len(x), len(y))
        return ((raw_distance / normalization_factor) if (normalization_factor > 0) else 0.0)


    # Propriétés pour accéder aux attributs depuis Python
    @property
    def type(self):
        return self._type
    @type.setter
    def type(self, value):
        self._type = value
    @property
    def c(self):
        return self._c
    @c.setter
    def c(self, value):
        self._c = value
    @property
    def _cost_split_merge(self):
        return self.__cost_split_merge
    @_cost_split_merge.setter
    def _cost_split_merge(self, value):
        self.__cost_split_merge = value
    @property
    def compute(self):
        return self._compute
    @compute.setter
    def compute(self, value):
        self._compute = value
    """
    Implementation of Move-Split-Merge (MSM) distance for time series comparison.
    MSM is an elastic distance measure that allows three operations:
    - Move: Change a value to another value (cost = |x - y|)
    - Split: Split one value into two values (cost = c)
    - Merge: Merge two values into one value (cost = c)
    
    The cost parameter c controls the relative cost of split/merge operations
    compared to move operations.
    
    Reference:
    Stefan, A., Athitsos, V., & Das, G. (2013). The move-split-merge metric for time series.
    IEEE Transactions on Knowledge and Data Engineering, 25(6), 1425-1438.
    """
    
    def __init__(self, c: float = 1.0)-> None:
        """
        Initialize the MSM distance calculator.
        
        Args:
            c: Cost parameter for split and merge operations.
               Higher values make split/merge operations more expensive.
        """
        super().__init__()
        self.type='vec_float'
        
        self.c = c
    
    def _cost_split_merge(self, x: float, y1: float, y2: float) -> float:
        """
        Calculate the minimum cost of splitting x to match y1,y2 or
        merging y1,y2 to match x.
        
        Args:
            x: Single value potentially being split or merged to
            y1: First value of the pair
            y2: Second value of the pair
            
        Returns:
            float: Minimum cost between split and merge operations
        """
        # Cost of splitting x into y1,y2
        cost_split = self.c + abs(x - y1)
        # Cost of merging y1,y2 into x
        cost_merge = self.c + abs(y2 - x)
        return min(cost_split, cost_merge)
    
    def compute(self, x: List[float], y: List[float]) -> float:
        """
        Compute the MSM distance between two time series.
        
        Args:
            x: First time series (list of float values)
            y: Second time series (list of float values)
            
        Returns:
            float: MSM distance between the two series
            
        Example:
            >>> msm = MSMDistance(c=0.5)
            >>> ts1 = [1.0, 2.0, 3.0, 2.0, 1.0]
            >>> ts2 = [1.0, 2.0, 2.5, 2.0, 1.0]
            >>> distance = msm.compute(ts1, ts2)
        """
        n, m = len(x), len(y)
        
        # Initialize dynamic programming matrix with infinity
        dp = [[inf] * (m + 1) for _ in range(n + 1)]
        
        # Base cases
        dp[0][0] = 0
        
        # Initialize first row and column
        for i in range(1, n + 1):
            dp[i][0] = dp[i-1][0] + self.c
        for j in range(1, m + 1):
            dp[0][j] = dp[0][j-1] + self.c
        
        # Fill the dynamic programming matrix
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                # Case 1: Move operation
                cost_move = dp[i-1][j-1] + abs(x[i-1] - y[j-1])
                
                # Case 2: Split or merge with previous elements
                cost_split_merge = inf
                if i > 1:
                    cost_split_merge = min(cost_split_merge,
                                         dp[i-2][j-1] + self._cost_split_merge(y[j-1], x[i-2], x[i-1]))
                if j > 1:
                    cost_split_merge = min(cost_split_merge,
                                         dp[i-1][j-2] + self._cost_split_merge(x[i-1], y[j-2], y[j-1]))
                
                dp[i][j] = min(cost_move, cost_split_merge)
        
        return dp[n][m]
    
    def normalized_compute(self, x: List[float], y: List[float]) -> float:
        """
        Compute the normalized MSM distance between two time series.
        Normalization is done by dividing by the length of the longer series.
        
        Args:
            x: First time series (list of float values)
            y: Second time series (list of float values)
            
        Returns:
            float: Normalized MSM distance between the two series
        """
        raw_distance = self.compute(x, y)
        normalization_factor = max(len(x), len(y))
        return raw_distance / normalization_factor if normalization_factor > 0 else 0.0
        
from typing import List, Dict, Tuple
import math
from itertools import permutations

cdef class PermutationEntropyDistance(Distance):
    # Attributs de classe
    cdef object _patterns
    cdef object __entropy
    cdef object __get_pattern
    cdef object _order
    cdef object __get_pattern_distribution
    cdef object _delay
    cdef object __jensen_shannon_distance
    cdef object _type
    '
    Implementation of Permutation Entropy Distance for time series comparison.
    This measure compares time series based on their complexity and patterns
    using symbolic permutations of consecutive values.
    
    The algorithm works by:
    1. Converting subsequences into ordinal patterns
    2. Computing the probability distribution of these patterns
    3. Calculating the entropy of the distributions
    4. Computing distance between entropy distributions
    
    Reference:
    Bandt, C., & Pompe, B. (2002). Permutation entropy: a natural complexity 
    measure for time series. Physical review letters, 88(17), 174102.
    '

    def __init__(self, *args, **kwargs):
        '
        Initialize the Permutation Entropy Distance calculator.
        
        Args:
            order: Length of the ordinal patterns (embedding dimension)
            delay: Time delay between values in the patterns (time lag)
        '
        super().__init__()
        self._type = 'vec_float'
        self._order = order
        self._delay = delay
        self._patterns = list(permutations(range(order)))

    def _get_pattern(self, values: List[float]) -> Tuple[int]:
        '
        Convert a subsequence of values into its ordinal pattern.
        
        Args:
            values: List of values to convert into pattern
            
        Returns:
            tuple: Ordinal pattern representing the relative ordering of values
        '
        indices = list(range(len(values)))
        indices.sort(key=(lambda i: values[i]))
        rank_order = ([0] * len(values))
        for (i, idx) in enumerate(indices):
            rank_order[idx] = i
        return tuple(rank_order)

    def _get_pattern_distribution(self, series: List[float]) -> Dict[(Tuple[int], float)]:
        '
        Compute the probability distribution of ordinal patterns in the time series.
        
        Args:
            series: Input time series
            
        Returns:
            dict: Mapping from patterns to their probabilities
        '
        pattern_counts = {pattern: 0 for pattern in self._patterns}
        total_patterns = 0
        for i in range((len(series) - ((self._order - 1) * self._delay))):
            subsequence = [series[(i + (j * self._delay))] for j in range(self._order)]
            pattern = self._get_pattern(subsequence)
            pattern_counts[pattern] += 1
            total_patterns += 1
        if (total_patterns > 0):
            pattern_dist = {pattern: (count / total_patterns) for (pattern, count) in pattern_counts.items()}
        else:
            pattern_dist = {pattern: 0 for pattern in self._patterns}
        return pattern_dist

    def _entropy(self, distribution: Dict[(Tuple[int], float)]) -> float:
        '
        Calculate the Shannon entropy of a probability distribution.
        
        Args:
            distribution: Probability distribution of patterns
            
        Returns:
            float: Shannon entropy value
        '
        entropy = 0.0
        for prob in distribution.values():
            if (prob > 0):
                entropy -= (prob * math.log2(prob))
        return entropy

    def _jensen_shannon_distance(self, dist1: Dict[(Tuple[int], float)], dist2: Dict[(Tuple[int], float)]) -> float:
        '
        Compute Jensen-Shannon distance between two probability distributions.
        
        Args:
            dist1: First probability distribution
            dist2: Second probability distribution
            
        Returns:
            float: Jensen-Shannon distance value
        '
        avg_dist = {}
        for pattern in self._patterns:
            avg_dist[pattern] = ((dist1[pattern] + dist2[pattern]) / 2)
        entropy_avg = self._entropy(avg_dist)
        entropy1 = self._entropy(dist1)
        entropy2 = self._entropy(dist2)
        jsd = (entropy_avg - ((entropy1 + entropy2) / 2))
        return math.sqrt(abs(jsd))

    def compute(self, x: List[float], y: List[float]) -> float:
        '
        Compute the Permutation Entropy Distance between two time series.
        
        Args:
            x: First time series (list of float values)
            y: Second time series (list of float values)
            
        Returns:
            float: Permutation Entropy Distance between the two series
            
        Example:
            >>> ped = PermutationEntropyDistance(order=3, delay=1)
            >>> ts1 = [1.0, 2.0, 3.0, 2.0, 1.0]
            >>> ts2 = [1.0, 2.0, 2.5, 2.0, 1.0]
            >>> distance = ped.compute(ts1, ts2)
        '
        min_length = (((self._order - 1) * self._delay) + 1)
        if ((len(x) < min_length) or (len(y) < min_length)):
            raise ValueError(f'Time series must have length >= {min_length} for order={self._order} and delay={self._delay}')
        dist_x = self._get_pattern_distribution(x)
        dist_y = self._get_pattern_distribution(y)
        return self._jensen_shannon_distance(dist_x, dist_y)

    def compute_entropy(self, x: List[float]) -> float:
        '
        Compute the Permutation Entropy of a single time series.
        
        Args:
            x: Input time series
            
        Returns:
            float: Permutation Entropy value
        '
        dist = self._get_pattern_distribution(x)
        return self._entropy(dist)


    # Propriétés pour accéder aux attributs depuis Python
    @property
    def patterns(self):
        return self._patterns
    @patterns.setter
    def patterns(self, value):
        self._patterns = value
    @property
    def _entropy(self):
        return self.__entropy
    @_entropy.setter
    def _entropy(self, value):
        self.__entropy = value
    @property
    def _get_pattern(self):
        return self.__get_pattern
    @_get_pattern.setter
    def _get_pattern(self, value):
        self.__get_pattern = value
    @property
    def order(self):
        return self._order
    @order.setter
    def order(self, value):
        self._order = value
    @property
    def _get_pattern_distribution(self):
        return self.__get_pattern_distribution
    @_get_pattern_distribution.setter
    def _get_pattern_distribution(self, value):
        self.__get_pattern_distribution = value
    @property
    def delay(self):
        return self._delay
    @delay.setter
    def delay(self, value):
        self._delay = value
    @property
    def _jensen_shannon_distance(self):
        return self.__jensen_shannon_distance
    @_jensen_shannon_distance.setter
    def _jensen_shannon_distance(self, value):
        self.__jensen_shannon_distance = value
    @property
    def type(self):
        return self._type
    @type.setter
    def type(self, value):
        self._type = value
    """
    Implementation of Permutation Entropy Distance for time series comparison.
    This measure compares time series based on their complexity and patterns
    using symbolic permutations of consecutive values.
    
    The algorithm works by:
    1. Converting subsequences into ordinal patterns
    2. Computing the probability distribution of these patterns
    3. Calculating the entropy of the distributions
    4. Computing distance between entropy distributions
    
    Reference:
    Bandt, C., & Pompe, B. (2002). Permutation entropy: a natural complexity 
    measure for time series. Physical review letters, 88(17), 174102.
    """
    
    def __init__(self, order: int = 3, delay: int = 1)-> None:
        """
        Initialize the Permutation Entropy Distance calculator.
        
        Args:
            order: Length of the ordinal patterns (embedding dimension)
            delay: Time delay between values in the patterns (time lag)
        """
        super().__init__()
        self.type='vec_float'
        
        self.order = order
        self.delay = delay
        # Generate all possible permutations for the given order
        self.patterns = list(permutations(range(order)))
        
    def _get_pattern(self, values: List[float]) -> Tuple[int]:
        """
        Convert a subsequence of values into its ordinal pattern.
        
        Args:
            values: List of values to convert into pattern
            
        Returns:
            tuple: Ordinal pattern representing the relative ordering of values
        """
        # Get the indices that would sort the values
        indices = list(range(len(values)))
        indices.sort(key=lambda i: values[i])
        
        # Convert to rank order
        rank_order = [0] * len(values)
        for i, idx in enumerate(indices):
            rank_order[idx] = i
            
        return tuple(rank_order)
    
    def _get_pattern_distribution(self, series: List[float]) -> Dict[Tuple[int], float]:
        """
        Compute the probability distribution of ordinal patterns in the time series.
        
        Args:
            series: Input time series
            
        Returns:
            dict: Mapping from patterns to their probabilities
        """
        pattern_counts = {pattern: 0 for pattern in self.patterns}
        total_patterns = 0
        
        # Sliding window through the time series
        for i in range(len(series) - (self.order - 1) * self.delay):
            # Extract subsequence
            subsequence = [series[i + j * self.delay] for j in range(self.order)]
            pattern = self._get_pattern(subsequence)
            pattern_counts[pattern] += 1
            total_patterns += 1
            
        # Convert counts to probabilities
        if total_patterns > 0:
            pattern_dist = {pattern: count / total_patterns 
                          for pattern, count in pattern_counts.items()}
        else:
            pattern_dist = {pattern: 0 for pattern in self.patterns}
            
        return pattern_dist
    
    def _entropy(self, distribution: Dict[Tuple[int], float]) -> float:
        """
        Calculate the Shannon entropy of a probability distribution.
        
        Args:
            distribution: Probability distribution of patterns
            
        Returns:
            float: Shannon entropy value
        """
        entropy = 0.0
        for prob in distribution.values():
            if prob > 0:  # Avoid log(0)
                entropy -= prob * math.log2(prob)
        return entropy
    
    def _jensen_shannon_distance(self, dist1: Dict[Tuple[int], float], 
                               dist2: Dict[Tuple[int], float]) -> float:
        """
        Compute Jensen-Shannon distance between two probability distributions.
        
        Args:
            dist1: First probability distribution
            dist2: Second probability distribution
            
        Returns:
            float: Jensen-Shannon distance value
        """
        # Calculate the average distribution
        avg_dist = {}
        for pattern in self.patterns:
            avg_dist[pattern] = (dist1[pattern] + dist2[pattern]) / 2
            
        # Calculate Jensen-Shannon divergence
        entropy_avg = self._entropy(avg_dist)
        entropy1 = self._entropy(dist1)
        entropy2 = self._entropy(dist2)
        
        jsd = entropy_avg - (entropy1 + entropy2) / 2
        
        # Convert divergence to distance by taking square root
        return math.sqrt(abs(jsd))  # abs to handle numerical errors
    
    def compute(self, x: List[float], y: List[float]) -> float:
        """
        Compute the Permutation Entropy Distance between two time series.
        
        Args:
            x: First time series (list of float values)
            y: Second time series (list of float values)
            
        Returns:
            float: Permutation Entropy Distance between the two series
            
        Example:
            >>> ped = PermutationEntropyDistance(order=3, delay=1)
            >>> ts1 = [1.0, 2.0, 3.0, 2.0, 1.0]
            >>> ts2 = [1.0, 2.0, 2.5, 2.0, 1.0]
            >>> distance = ped.compute(ts1, ts2)
        """
        # Check if series are long enough
        min_length = (self.order - 1) * self.delay + 1
        if len(x) < min_length or len(y) < min_length:
            raise ValueError(f"Time series must have length >= {min_length} "
                           f"for order={self.order} and delay={self.delay}")
        
        # Get pattern distributions
        dist_x = self._get_pattern_distribution(x)
        dist_y = self._get_pattern_distribution(y)
        
        # Calculate distance between distributions
        return self._jensen_shannon_distance(dist_x, dist_y)
    
    def compute_entropy(self, x: List[float]) -> float:
        """
        Compute the Permutation Entropy of a single time series.
        
        Args:
            x: Input time series
            
        Returns:
            float: Permutation Entropy value
        """
        dist = self._get_pattern_distribution(x)
        return self._entropy(dist)

from typing import List, Tuple
import math
import random

cdef class SOMDistance(Distance):
    # Attributs de classe
    cdef object __get_windows
    cdef object _n_iterations
    cdef object __euclidean_distance
    cdef object _grid
    cdef object _sigma
    cdef object __get_best_matching_unit
    cdef object _window_size
    cdef object __get_embedding
    cdef object __get_neighborhood
    cdef object __train_som
    cdef object _initialized
    cdef object __normalize_window
    cdef object _type
    cdef object _learning_rate
    cdef object _map_size
    '
    Implementation of Self-Organizing Map (SOM) based distance for time series comparison.
    This approach uses a SOM to create a lower-dimensional representation of time series,
    then computes distances between their embeddings.
    
    The algorithm:
    1. Trains a SOM on sliding windows from the time series
    2. Creates embeddings by mapping windows to their best matching units
    3. Computes distance between the resulting embeddings
    
    Reference:
    Kohonen, T. (1990). The self-organizing map. 
    Proceedings of the IEEE, 78(9), 1464-1480.
    '

    def __init__(self, *args, **kwargs):
        '
        Initialize the SOM Distance calculator.
        
        Args:
            map_size: Tuple of (width, height) for the SOM grid
            window_size: Size of sliding windows for time series
            learning_rate: Initial learning rate for SOM training
            sigma: Initial neighborhood radius
            n_iterations: Number of training iterations
        '
        super().__init__()
        self._type = 'vec_float'
        self._map_size = map_size
        self._window_size = window_size
        self._learning_rate = learning_rate
        self._sigma = sigma
        self._n_iterations = n_iterations
        self._initialized = False
        self._grid = [[[random.uniform((- 1), 1) for _ in range(window_size)] for _ in range(map_size[1])] for _ in range(map_size[0])]

    def _euclidean_distance(self, x: List[float], y: List[float]) -> float:
        '
        Compute Euclidean distance between two vectors.
        
        Args:
            x: First vector
            y: Second vector
            
        Returns:
            float: Euclidean distance
        '
        return math.sqrt(sum((((a - b) ** 2) for (a, b) in zip(x, y))))

    def _normalize_window(self, window: List[float]) -> List[float]:
        '
        Normalize a window of values to zero mean and unit variance.
        
        Args:
            window: List of values to normalize
            
        Returns:
            list: Normalized values
        '
        if (not window):
            return window
        mean = (sum(window) / len(window))
        variance = (sum((((x - mean) ** 2) for x in window)) / len(window))
        std = (math.sqrt(variance) if (variance > 0) else 1.0)
        return [((x - mean) / std) for x in window]

    def _get_best_matching_unit(self, window: List[float]) -> Tuple[(int, int)]:
        '
        Find the best matching unit (BMU) for a window in the SOM.
        
        Args:
            window: Input window to find BMU for
            
        Returns:
            tuple: (x, y) coordinates of the BMU
        '
        min_dist = float('inf')
        bmu = (0, 0)
        for i in range(self._map_size[0]):
            for j in range(self._map_size[1]):
                dist = self._euclidean_distance(window, self._grid[i][j])
                if (dist < min_dist):
                    min_dist = dist
                    bmu = (i, j)
        return bmu

    def _get_neighborhood(self, center: Tuple[(int, int)], sigma: float) -> List[Tuple[(Tuple[(int, int)], float)]]:
        '
        Get neighborhood weights for all nodes based on distance from center.
        
        Args:
            center: (x, y) coordinates of the center node
            sigma: Current neighborhood radius
            
        Returns:
            list: List of ((x, y), weight) pairs for all nodes
        '
        neighborhood = []
        for i in range(self._map_size[0]):
            for j in range(self._map_size[1]):
                dist = math.sqrt((((center[0] - i) ** 2) + ((center[1] - j) ** 2)))
                weight = math.exp(((- (dist ** 2)) / (2 * (sigma ** 2))))
                neighborhood.append(((i, j), weight))
        return neighborhood

    def _train_som(self, windows: List[List[float]]) -> None:
        '
        Train the SOM using the given windows.
        
        Args:
            windows: List of sliding windows from time series
        '
        current_learning_rate = self._learning_rate
        current_sigma = self._sigma
        for iteration in range(self._n_iterations):
            progress = (iteration / self._n_iterations)
            current_learning_rate = (self._learning_rate * (1 - progress))
            current_sigma = (self._sigma * (1 - progress))
            for window in windows:
                bmu = self._get_best_matching_unit(window)
                neighborhood = self._get_neighborhood(bmu, current_sigma)
                for ((i, j), weight) in neighborhood:
                    for k in range(self._window_size):
                        self._grid[i][j][k] += ((current_learning_rate * weight) * (window[k] - self._grid[i][j][k]))

    def _get_windows(self, series: List[float]) -> List[List[float]]:
        '
        Extract normalized sliding windows from a time series.
        
        Args:
            series: Input time series
            
        Returns:
            list: List of normalized windows
        '
        windows = []
        for i in range(((len(series) - self._window_size) + 1)):
            window = series[i:(i + self._window_size)]
            windows.append(self._normalize_window(window))
        return windows

    def _get_embedding(self, series: List[float]) -> List[Tuple[(int, int)]]:
        '
        Create SOM embedding for a time series by mapping its windows to BMUs.
        
        Args:
            series: Input time series
            
        Returns:
            list: List of BMU coordinates for each window
        '
        windows = self._get_windows(series)
        return [self._get_best_matching_unit(window) for window in windows]

    def compute(self, x: List[float], y: List[float]) -> float:
        '
        Compute the SOM-based distance between two time series.
        
        Args:
            x: First time series
            y: Second time series
            
        Returns:
            float: SOM-based distance between the series
            
        Example:
            >>> som = SOMDistance(map_size=(5, 5), window_size=3)
            >>> ts1 = [1.0, 2.0, 3.0, 2.0, 1.0]
            >>> ts2 = [1.0, 2.0, 2.5, 2.0, 1.0]
            >>> distance = som.compute(ts1, ts2)
        '
        if ((len(x) < self._window_size) or (len(y) < self._window_size)):
            raise ValueError(f'Time series must have length >= {self._window_size}')
        windows_x = self._get_windows(x)
        windows_y = self._get_windows(y)
        all_windows = (windows_x + windows_y)
        if (not self._initialized):
            self._train_som(all_windows)
            self._initialized = True
        embedding_x = self._get_embedding(x)
        embedding_y = self._get_embedding(y)
        dist_sum = 0
        min_len = min(len(embedding_x), len(embedding_y))
        for (bmu_x, bmu_y) in zip(embedding_x[:min_len], embedding_y[:min_len]):
            dist_sum += math.sqrt((((bmu_x[0] - bmu_y[0]) ** 2) + ((bmu_x[1] - bmu_y[1]) ** 2)))
        return (dist_sum / min_len)


    # Propriétés pour accéder aux attributs depuis Python
    @property
    def _get_windows(self):
        return self.__get_windows
    @_get_windows.setter
    def _get_windows(self, value):
        self.__get_windows = value
    @property
    def _euclidean_distance(self):
        return self.__euclidean_distance
    @_euclidean_distance.setter
    def _euclidean_distance(self, value):
        self.__euclidean_distance = value
    @property
    def grid(self):
        return self._grid
    @grid.setter
    def grid(self, value):
        self._grid = value
    @property
    def sigma(self):
        return self._sigma
    @sigma.setter
    def sigma(self, value):
        self._sigma = value
    @property
    def _get_best_matching_unit(self):
        return self.__get_best_matching_unit
    @_get_best_matching_unit.setter
    def _get_best_matching_unit(self, value):
        self.__get_best_matching_unit = value
    @property
    def window_size(self):
        return self._window_size
    @window_size.setter
    def window_size(self, value):
        self._window_size = value
    @property
    def _get_embedding(self):
        return self.__get_embedding
    @_get_embedding.setter
    def _get_embedding(self, value):
        self.__get_embedding = value
    @property
    def _get_neighborhood(self):
        return self.__get_neighborhood
    @_get_neighborhood.setter
    def _get_neighborhood(self, value):
        self.__get_neighborhood = value
    @property
    def _train_som(self):
        return self.__train_som
    @_train_som.setter
    def _train_som(self, value):
        self.__train_som = value
    @property
    def initialized(self):
        return self._initialized
    @initialized.setter
    def initialized(self, value):
        self._initialized = value
    @property
    def type(self):
        return self._type
    @type.setter
    def type(self, value):
        self._type = value
    @property
    def _normalize_window(self):
        return self.__normalize_window
    @_normalize_window.setter
    def _normalize_window(self, value):
        self.__normalize_window = value
    @property
    def n_iterations(self):
        return self._n_iterations
    @n_iterations.setter
    def n_iterations(self, value):
        self._n_iterations = value
    @property
    def learning_rate(self):
        return self._learning_rate
    @learning_rate.setter
    def learning_rate(self, value):
        self._learning_rate = value
    @property
    def map_size(self):
        return self._map_size
    @map_size.setter
    def map_size(self, value):
        self._map_size = value
    """
    Implementation of Self-Organizing Map (SOM) based distance for time series comparison.
    This approach uses a SOM to create a lower-dimensional representation of time series,
    then computes distances between their embeddings.
    
    The algorithm:
    1. Trains a SOM on sliding windows from the time series
    2. Creates embeddings by mapping windows to their best matching units
    3. Computes distance between the resulting embeddings
    
    Reference:
    Kohonen, T. (1990). The self-organizing map. 
    Proceedings of the IEEE, 78(9), 1464-1480.
    """
    
    def __init__(self, 
                 map_size: Tuple[int, int] = (10, 10),
                 window_size: int = 3,
                 learning_rate: float = 0.1,
                 sigma: float = 1.0,
                 n_iterations: int = 1000)-> None:
        """
        Initialize the SOM Distance calculator.
        
        Args:
            map_size: Tuple of (width, height) for the SOM grid
            window_size: Size of sliding windows for time series
            learning_rate: Initial learning rate for SOM training
            sigma: Initial neighborhood radius
            n_iterations: Number of training iterations
        """
        super().__init__()
        self.type='vec_float'
        
        self.map_size = map_size
        self.window_size = window_size
        self.learning_rate = learning_rate
        self.sigma = sigma
        self.n_iterations = n_iterations
        self.initialized = False
        
        # Initialize SOM grid randomly
        self.grid = [
            [
                [random.uniform(-1, 1) for _ in range(window_size)]
                for _ in range(map_size[1])
            ]
            for _ in range(map_size[0])
        ]
    
    def _euclidean_distance(self, x: List[float], y: List[float]) -> float:
        """
        Compute Euclidean distance between two vectors.
        
        Args:
            x: First vector
            y: Second vector
            
        Returns:
            float: Euclidean distance
        """
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(x, y)))
    
    def _normalize_window(self, window: List[float]) -> List[float]:
        """
        Normalize a window of values to zero mean and unit variance.
        
        Args:
            window: List of values to normalize
            
        Returns:
            list: Normalized values
        """
        if not window:
            return window
        
        mean = sum(window) / len(window)
        variance = sum((x - mean) ** 2 for x in window) / len(window)
        std = math.sqrt(variance) if variance > 0 else 1.0
        
        return [(x - mean) / std for x in window]
    
    def _get_best_matching_unit(self, window: List[float]) -> Tuple[int, int]:
        """
        Find the best matching unit (BMU) for a window in the SOM.
        
        Args:
            window: Input window to find BMU for
            
        Returns:
            tuple: (x, y) coordinates of the BMU
        """
        min_dist = float('inf')
        bmu = (0, 0)
        
        for i in range(self.map_size[0]):
            for j in range(self.map_size[1]):
                dist = self._euclidean_distance(window, self.grid[i][j])
                if dist < min_dist:
                    min_dist = dist
                    bmu = (i, j)
                    
        return bmu
    
    def _get_neighborhood(self, center: Tuple[int, int], 
                         sigma: float) -> List[Tuple[Tuple[int, int], float]]:
        """
        Get neighborhood weights for all nodes based on distance from center.
        
        Args:
            center: (x, y) coordinates of the center node
            sigma: Current neighborhood radius
            
        Returns:
            list: List of ((x, y), weight) pairs for all nodes
        """
        neighborhood = []
        for i in range(self.map_size[0]):
            for j in range(self.map_size[1]):
                dist = math.sqrt((center[0] - i) ** 2 + (center[1] - j) ** 2)
                weight = math.exp(-(dist ** 2) / (2 * sigma ** 2))
                neighborhood.append(((i, j), weight))
        return neighborhood
    
    def _train_som(self, windows: List[List[float]]) -> None:
        """
        Train the SOM using the given windows.
        
        Args:
            windows: List of sliding windows from time series
        """
        current_learning_rate = self.learning_rate
        current_sigma = self.sigma
        
        for iteration in range(self.n_iterations):
            # Update learning parameters
            progress = iteration / self.n_iterations
            current_learning_rate = self.learning_rate * (1 - progress)
            current_sigma = self.sigma * (1 - progress)
            
            # Train on each window
            for window in windows:
                bmu = self._get_best_matching_unit(window)
                neighborhood = self._get_neighborhood(bmu, current_sigma)
                
                # Update weights
                for (i, j), weight in neighborhood:
                    for k in range(self.window_size):
                        self.grid[i][j][k] += (
                            current_learning_rate * weight * 
                            (window[k] - self.grid[i][j][k])
                        )
    
    def _get_windows(self, series: List[float]) -> List[List[float]]:
        """
        Extract normalized sliding windows from a time series.
        
        Args:
            series: Input time series
            
        Returns:
            list: List of normalized windows
        """
        windows = []
        for i in range(len(series) - self.window_size + 1):
            window = series[i:i + self.window_size]
            windows.append(self._normalize_window(window))
        return windows
    
    def _get_embedding(self, series: List[float]) -> List[Tuple[int, int]]:
        """
        Create SOM embedding for a time series by mapping its windows to BMUs.
        
        Args:
            series: Input time series
            
        Returns:
            list: List of BMU coordinates for each window
        """
        windows = self._get_windows(series)
        return [self._get_best_matching_unit(window) for window in windows]
    
    def compute(self, x: List[float], y: List[float]) -> float:
        """
        Compute the SOM-based distance between two time series.
        
        Args:
            x: First time series
            y: Second time series
            
        Returns:
            float: SOM-based distance between the series
            
        Example:
            >>> som = SOMDistance(map_size=(5, 5), window_size=3)
            >>> ts1 = [1.0, 2.0, 3.0, 2.0, 1.0]
            >>> ts2 = [1.0, 2.0, 2.5, 2.0, 1.0]
            >>> distance = som.compute(ts1, ts2)
        """
        # Check if series are long enough
        if len(x) < self.window_size or len(y) < self.window_size:
            raise ValueError(f"Time series must have length >= {self.window_size}")
        
        # Get all windows from both series
        windows_x = self._get_windows(x)
        windows_y = self._get_windows(y)
        all_windows = windows_x + windows_y
        
        # Train SOM if not already trained
        if not self.initialized:
            self._train_som(all_windows)
            self.initialized = True
        
        # Get embeddings
        embedding_x = self._get_embedding(x)
        embedding_y = self._get_embedding(y)
        
        # Compute distance between embeddings using Euclidean distance
        # between successive BMU coordinates
        dist_sum = 0
        min_len = min(len(embedding_x), len(embedding_y))
        
        for bmu_x, bmu_y in zip(embedding_x[:min_len], embedding_y[:min_len]):
            dist_sum += math.sqrt(
                (bmu_x[0] - bmu_y[0]) ** 2 + 
                (bmu_x[1] - bmu_y[1]) ** 2
            )
            
        return dist_sum / min_len
from typing import List, Tuple, Optional
import random
import math

cdef class IsolationForestDistance(Distance):
    # Attributs de classe
    cdef object _max_depth
    cdef object __get_windows
    cdef object _split_value
    cdef object _n_trees
    cdef object __build_forest
    cdef object _right
    cdef object _is_leaf
    cdef object _left
    cdef object _window_size
    cdef object _split_feature
    cdef object _size
    cdef object _depth
    cdef object __normalize_window
    cdef object _type
    cdef object __average_path_length
    cdef object _subsample_size
    cdef object _IsolationTree
    '
    Implementation of Isolation Forest-based distance for time series comparison.
    This approach uses Isolation Forest concepts to measure similarity between
    time series based on their anomaly patterns and structural characteristics.
    '

    cdef class IsolationTree():
    # Attributs de classe
    cdef object _max_depth
    cdef object _split_value
    cdef object _right
    cdef object _is_leaf
    cdef object _left
    cdef object _split_feature
    cdef object _depth
    cdef object _size
    '
        Internal class representing a single isolation tree.
        '

    def __init__(self, *args, **kwargs):
        self._max_depth = max_depth
        self._split_feature = None
        self._split_value = None
        self._size = 0
        self._depth = 0
        self._left = None
        self._right = None
        self._is_leaf = False

    def fit(self, X: List[List[float]], depth: int) -> None:
        '
            Recursively build the isolation tree.
            
            Args:
                X: List of windows (each window is a list of values)
                depth: Current depth in the tree
            '
        self._depth = depth
        self._size = len(X)
        if ((depth >= self._max_depth) or (len(X) <= 1)):
            self._is_leaf = True
            return
        if ((not X) or (not X[0])):
            self._is_leaf = True
            return
        self._split_feature = random.randint(0, (len(X[0]) - 1))
        feature_values = [x[self._split_feature] for x in X]
        min_val = min(feature_values)
        max_val = max(feature_values)
        if (min_val == max_val):
            self._is_leaf = True
            return
        self._split_value = random.uniform(min_val, max_val)
        X_left = []
        X_right = []
        for x in X:
            if (x[self._split_feature] < self._split_value):
                X_left.append(x)
            else:
                X_right.append(x)
        if X_left:
            self._left = IsolationForestDistance.IsolationTree(self._max_depth)
            self._left.fit(X_left, (depth + 1))
        if X_right:
            self._right = IsolationForestDistance.IsolationTree(self._max_depth)
            self._right.fit(X_right, (depth + 1))

    def path_length(self, window: List[float]) -> int:
        '
            Compute the path length for a window.
            
            Args:
                window: Input window to compute path length for
                
            Returns:
                int: Length of path traversed
            '
        if (self._is_leaf or (self._split_feature is None)):
            return self._depth
        try:
            if (window[self._split_feature] < self._split_value):
                if (self._left is None):
                    return self._depth
                return self._left.path_length(window)
            else:
                if (self._right is None):
                    return self._depth
                return self._right.path_length(window)
        except (IndexError, TypeError):
            return self._depth


    # Propriétés pour accéder aux attributs depuis Python
    @property
    def max_depth(self):
        return self._max_depth
    @max_depth.setter
    def max_depth(self, value):
        self._max_depth = value
    @property
    def split_value(self):
        return self._split_value
    @split_value.setter
    def split_value(self, value):
        self._split_value = value
    @property
    def right(self):
        return self._right
    @right.setter
    def right(self, value):
        self._right = value
    @property
    def is_leaf(self):
        return self._is_leaf
    @is_leaf.setter
    def is_leaf(self, value):
        self._is_leaf = value
    @property
    def left(self):
        return self._left
    @left.setter
    def left(self, value):
        self._left = value
    @property
    def split_feature(self):
        return self._split_feature
    @split_feature.setter
    def split_feature(self, value):
        self._split_feature = value
    @property
    def depth(self):
        return self._depth
    @depth.setter
    def depth(self, value):
        self._depth = value
    @property
    def size(self):
        return self._size
    @size.setter
    def size(self, value):
        self._size = value
        '
        Internal class representing a single isolation tree.
        '

        def __init__(self, max_depth: int):
            self.max_depth = max_depth
            self.split_feature = None
            self.split_value = None
            self.size = 0
            self.depth = 0
            self.left = None
            self.right = None
            self.is_leaf = False

        def fit(self, X: List[List[float]], depth: int) -> None:
            '
            Recursively build the isolation tree.
            
            Args:
                X: List of windows (each window is a list of values)
                depth: Current depth in the tree
            '
            self.depth = depth
            self.size = len(X)
            if ((depth >= self.max_depth) or (len(X) <= 1)):
                self.is_leaf = True
                return
            if ((not X) or (not X[0])):
                self.is_leaf = True
                return
            self.split_feature = random.randint(0, (len(X[0]) - 1))
            feature_values = [x[self.split_feature] for x in X]
            min_val = min(feature_values)
            max_val = max(feature_values)
            if (min_val == max_val):
                self.is_leaf = True
                return
            self.split_value = random.uniform(min_val, max_val)
            X_left = []
            X_right = []
            for x in X:
                if (x[self.split_feature] < self.split_value):
                    X_left.append(x)
                else:
                    X_right.append(x)
            if X_left:
                self.left = IsolationForestDistance.IsolationTree(self.max_depth)
                self.left.fit(X_left, (depth + 1))
            if X_right:
                self.right = IsolationForestDistance.IsolationTree(self.max_depth)
                self.right.fit(X_right, (depth + 1))

        def path_length(self, window: List[float]) -> int:
            '
            Compute the path length for a window.
            
            Args:
                window: Input window to compute path length for
                
            Returns:
                int: Length of path traversed
            '
            if (self.is_leaf or (self.split_feature is None)):
                return self.depth
            try:
                if (window[self.split_feature] < self.split_value):
                    if (self.left is None):
                        return self.depth
                    return self.left.path_length(window)
                else:
                    if (self.right is None):
                        return self.depth
                    return self.right.path_length(window)
            except (IndexError, TypeError):
                return self.depth

    def __init__(self, *args, **kwargs):
        '
        Initialize the Isolation Forest Distance calculator.
        
        Args:
            n_trees: Number of isolation trees to build
            window_size: Size of sliding windows for time series
            subsample_size: Maximum number of samples to use per tree
            max_depth: Maximum depth of trees (if None, use log2(subsample_size))
        '
        super().__init__()
        self._type = 'vec_float'
        self._n_trees = max(10, n_trees)
        self._window_size = max(2, window_size)
        self._subsample_size = max(10, min(subsample_size, 1000))
        self._max_depth = (max_depth or int(math.log2(self._subsample_size)))

    def _normalize_window(self, window: List[float]) -> List[float]:
        '
        Normalize a window of values to zero mean and unit variance.
        '
        if (not window):
            return window
        try:
            mean = (sum(window) / len(window))
            variance = (sum((((x - mean) ** 2) for x in window)) / len(window))
            std = (math.sqrt(variance) if (variance > 0) else 1.0)
            return [((x - mean) / std) for x in window]
        except (TypeError, ZeroDivisionError):
            return window

    def _get_windows(self, series: List[float]) -> List[List[float]]:
        '
        Extract normalized sliding windows from a time series.
        '
        if ((not series) or (len(series) < self._window_size)):
            return []
        windows = []
        for i in range(((len(series) - self._window_size) + 1)):
            window = series[i:(i + self._window_size)]
            if all((isinstance(x, (int, float)) for x in window)):
                windows.append(self._normalize_window(window))
        return windows

    def _build_forest(self, windows: List[List[float]]) -> List[IsolationTree]:
        '
        Build an isolation forest from the given windows.
        '
        if (not windows):
            return []
        forest = []
        for _ in range(self._n_trees):
            if (len(windows) > self._subsample_size):
                sample = random.sample(windows, self._subsample_size)
            else:
                sample = windows.copy()
            tree = self.IsolationTree(self._max_depth)
            tree.fit(sample, 0)
            forest.append(tree)
        return forest

    def _average_path_length(self, window: List[float], forest: List[IsolationTree]) -> float:
        '
        Compute average path length for a window across all trees.
        '
        if (not forest):
            return 0.0
        total_length = sum((tree.path_length(window) for tree in forest))
        return (total_length / len(forest))

    def compute(self, x: List[float], y: List[float]) -> float:
        '
        Compute the Isolation Forest-based distance between two time series.
        
        Example:
            >>> ifd = IsolationForestDistance(n_trees=100, window_size=3)
            >>> ts1 = [1.0, 2.0, 3.0, 2.0, 1.0]
            >>> ts2 = [1.0, 2.0, 2.5, 2.0, 1.0]
            >>> distance = ifd.compute(ts1, ts2)
        '
        if ((not isinstance(x, list)) or (not isinstance(y, list))):
            raise TypeError('Input sequences must be lists')
        if ((len(x) < self._window_size) or (len(y) < self._window_size)):
            raise ValueError(f'Time series must have length >= {self._window_size}')
        if (not all((isinstance(val, (int, float)) for val in (x + y)))):
            raise TypeError('All values must be numeric')
        windows_x = self._get_windows(x)
        windows_y = self._get_windows(y)
        if ((not windows_x) or (not windows_y)):
            return float('inf')
        forest_x = self._build_forest(windows_x)
        forest_y = self._build_forest(windows_y)
        if ((not forest_x) or (not forest_y)):
            return float('inf')
        paths_x_in_x = [self._average_path_length(w, forest_x) for w in windows_x]
        paths_x_in_y = [self._average_path_length(w, forest_y) for w in windows_x]
        paths_y_in_x = [self._average_path_length(w, forest_x) for w in windows_y]
        paths_y_in_y = [self._average_path_length(w, forest_y) for w in windows_y]
        diff_x = sum((((px - py) ** 2) for (px, py) in zip(paths_x_in_x, paths_x_in_y)))
        diff_y = sum((((px - py) ** 2) for (px, py) in zip(paths_y_in_x, paths_y_in_y)))
        try:
            distance = math.sqrt(((diff_x + diff_y) / (len(windows_x) + len(windows_y))))
            return distance
        except (ValueError, ZeroDivisionError):
            return float('inf')


    # Propriétés pour accéder aux attributs depuis Python
    @property
    def max_depth(self):
        return self._max_depth
    @max_depth.setter
    def max_depth(self, value):
        self._max_depth = value
    @property
    def _get_windows(self):
        return self.__get_windows
    @_get_windows.setter
    def _get_windows(self, value):
        self.__get_windows = value
    @property
    def split_value(self):
        return self._split_value
    @split_value.setter
    def split_value(self, value):
        self._split_value = value
    @property
    def n_trees(self):
        return self._n_trees
    @n_trees.setter
    def n_trees(self, value):
        self._n_trees = value
    @property
    def _build_forest(self):
        return self.__build_forest
    @_build_forest.setter
    def _build_forest(self, value):
        self.__build_forest = value
    @property
    def right(self):
        return self._right
    @right.setter
    def right(self, value):
        self._right = value
    @property
    def is_leaf(self):
        return self._is_leaf
    @is_leaf.setter
    def is_leaf(self, value):
        self._is_leaf = value
    @property
    def left(self):
        return self._left
    @left.setter
    def left(self, value):
        self._left = value
    @property
    def size(self):
        return self._size
    @size.setter
    def size(self, value):
        self._size = value
    @property
    def split_feature(self):
        return self._split_feature
    @split_feature.setter
    def split_feature(self, value):
        self._split_feature = value
    @property
    def type(self):
        return self._type
    @type.setter
    def type(self, value):
        self._type = value
    @property
    def depth(self):
        return self._depth
    @depth.setter
    def depth(self, value):
        self._depth = value
    @property
    def _normalize_window(self):
        return self.__normalize_window
    @_normalize_window.setter
    def _normalize_window(self, value):
        self.__normalize_window = value
    @property
    def window_size(self):
        return self._window_size
    @window_size.setter
    def window_size(self, value):
        self._window_size = value
    @property
    def _average_path_length(self):
        return self.__average_path_length
    @_average_path_length.setter
    def _average_path_length(self, value):
        self.__average_path_length = value
    @property
    def subsample_size(self):
        return self._subsample_size
    @subsample_size.setter
    def subsample_size(self, value):
        self._subsample_size = value
    @property
    def IsolationTree(self):
        return self._IsolationTree
    @IsolationTree.setter
    def IsolationTree(self, value):
        self._IsolationTree = value
    """
    Implementation of Isolation Forest-based distance for time series comparison.
    This approach uses Isolation Forest concepts to measure similarity between
    time series based on their anomaly patterns and structural characteristics.
    """
    
    class IsolationTree:
        """
        Internal class representing a single isolation tree.
        """
        def __init__(self, max_depth: int):
            self.max_depth = max_depth
            self.split_feature = None
            self.split_value = None
            self.size = 0
            self.depth = 0
            self.left = None
            self.right = None
            self.is_leaf = False
            
        def fit(self, X: List[List[float]], depth: int) -> None:
            """
            Recursively build the isolation tree.
            
            Args:
                X: List of windows (each window is a list of values)
                depth: Current depth in the tree
            """
            self.depth = depth
            self.size = len(X)
            
            # Check termination conditions
            if depth >= self.max_depth or len(X) <= 1:
                self.is_leaf = True
                return
            
            # Randomly select split feature
            if not X or not X[0]:  # Check if X is empty or contains empty windows
                self.is_leaf = True
                return
                
            self.split_feature = random.randint(0, len(X[0]) - 1)
            
            # Get feature values and check if they're all the same
            feature_values = [x[self.split_feature] for x in X]
            min_val = min(feature_values)
            max_val = max(feature_values)
            
            if min_val == max_val:
                self.is_leaf = True
                return
            
            # Set split value and partition data
            self.split_value = random.uniform(min_val, max_val)
            
            X_left = []
            X_right = []
            
            for x in X:
                if x[self.split_feature] < self.split_value:
                    X_left.append(x)
                else:
                    X_right.append(x)
            
            # Create child nodes if partitions are non-empty
            if X_left:
                self.left = IsolationForestDistance.IsolationTree(self.max_depth)
                self.left.fit(X_left, depth + 1)
            
            if X_right:
                self.right = IsolationForestDistance.IsolationTree(self.max_depth)
                self.right.fit(X_right, depth + 1)
                
        def path_length(self, window: List[float]) -> int:
            """
            Compute the path length for a window.
            
            Args:
                window: Input window to compute path length for
                
            Returns:
                int: Length of path traversed
            """
            if self.is_leaf or self.split_feature is None:
                return self.depth
            
            try:
                if window[self.split_feature] < self.split_value:
                    if self.left is None:
                        return self.depth
                    return self.left.path_length(window)
                else:
                    if self.right is None:
                        return self.depth
                    return self.right.path_length(window)
            except (IndexError, TypeError):
                return self.depth
    
    def __init__(self, 
                 n_trees: int = 100,
                 window_size: int = 3,
                 subsample_size: int = 256,
                 max_depth: Optional[int] = None)-> None:
        """
        Initialize the Isolation Forest Distance calculator.
        
        Args:
            n_trees: Number of isolation trees to build
            window_size: Size of sliding windows for time series
            subsample_size: Maximum number of samples to use per tree
            max_depth: Maximum depth of trees (if None, use log2(subsample_size))
        """
        super().__init__()
        self.type='vec_float'
        
        self.n_trees = max(10, n_trees)  # Ensure minimum number of trees
        self.window_size = max(2, window_size)  # Ensure minimum window size
        self.subsample_size = max(10, min(subsample_size, 1000))  # Bound subsample size
        self.max_depth = max_depth or int(math.log2(self.subsample_size))
    
    def _normalize_window(self, window: List[float]) -> List[float]:
        """
        Normalize a window of values to zero mean and unit variance.
        """
        if not window:
            return window
            
        try:
            mean = sum(window) / len(window)
            variance = sum((x - mean) ** 2 for x in window) / len(window)
            std = math.sqrt(variance) if variance > 0 else 1.0
            return [(x - mean) / std for x in window]
        except (TypeError, ZeroDivisionError):
            return window
    
    def _get_windows(self, series: List[float]) -> List[List[float]]:
        """
        Extract normalized sliding windows from a time series.
        """
        if not series or len(series) < self.window_size:
            return []
            
        windows = []
        for i in range(len(series) - self.window_size + 1):
            window = series[i:i + self.window_size]
            if all(isinstance(x, (int, float)) for x in window):
                windows.append(self._normalize_window(window))
        return windows
    
    def _build_forest(self, windows: List[List[float]]) -> List[IsolationTree]:
        """
        Build an isolation forest from the given windows.
        """
        if not windows:
            return []
            
        forest = []
        for _ in range(self.n_trees):
            # Subsample windows if necessary
            if len(windows) > self.subsample_size:
                sample = random.sample(windows, self.subsample_size)
            else:
                sample = windows.copy()
                
            tree = self.IsolationTree(self.max_depth)
            tree.fit(sample, 0)
            forest.append(tree)
            
        return forest
    
    def _average_path_length(self, window: List[float], 
                           forest: List[IsolationTree]) -> float:
        """
        Compute average path length for a window across all trees.
        """
        if not forest:
            return 0.0
            
        total_length = sum(tree.path_length(window) for tree in forest)
        return total_length / len(forest)
    
    def compute(self, x: List[float], y: List[float]) -> float:
        """
        Compute the Isolation Forest-based distance between two time series.
        
        Example:
            >>> ifd = IsolationForestDistance(n_trees=100, window_size=3)
            >>> ts1 = [1.0, 2.0, 3.0, 2.0, 1.0]
            >>> ts2 = [1.0, 2.0, 2.5, 2.0, 1.0]
            >>> distance = ifd.compute(ts1, ts2)
        """
        # Validate input
        if not isinstance(x, list) or not isinstance(y, list):
            raise TypeError("Input sequences must be lists")
            
        if len(x) < self.window_size or len(y) < self.window_size:
            raise ValueError(f"Time series must have length >= {self.window_size}")
            
        if not all(isinstance(val, (int, float)) for val in x + y):
            raise TypeError("All values must be numeric")
        
        # Get windows from both series
        windows_x = self._get_windows(x)
        windows_y = self._get_windows(y)
        
        if not windows_x or not windows_y:
            return float('inf')
        
        # Build forests for both series
        forest_x = self._build_forest(windows_x)
        forest_y = self._build_forest(windows_y)
        
        if not forest_x or not forest_y:
            return float('inf')
        
        # Compute average path lengths
        paths_x_in_x = [self._average_path_length(w, forest_x) for w in windows_x]
        paths_x_in_y = [self._average_path_length(w, forest_y) for w in windows_x]
        paths_y_in_x = [self._average_path_length(w, forest_x) for w in windows_y]
        paths_y_in_y = [self._average_path_length(w, forest_y) for w in windows_y]
        
        # Compute distance based on difference in isolation patterns
        diff_x = sum((px - py) ** 2 for px, py in zip(paths_x_in_x, paths_x_in_y))
        diff_y = sum((px - py) ** 2 for px, py in zip(paths_y_in_x, paths_y_in_y))
        
        try:
            distance = math.sqrt((diff_x + diff_y) / (len(windows_x) + len(windows_y)))
            return distance
        except (ValueError, ZeroDivisionError):
            return float('inf')
        
from typing import List, Dict, Set
import random
import math

cdef class ClusterMembershipDistance(Distance):
    # Attributs de classe
    cdef object __get_windows
    cdef object _max_iter
    cdef object __euclidean_distance
    cdef object _n_init
    cdef object _window_size
    cdef object _n_clusters
    cdef object __kmeans_clustering
    cdef object __get_cluster_sets
    cdef object __normalize_window
    cdef object _type
    '
    Implementation of Cluster Membership Distance for time series comparison.
    This approach measures similarity between time series based on how often
    their subsequences are assigned to the same clusters.
    
    The algorithm:
    1. Extracts sliding windows from both time series
    2. Clusters the windows using k-means
    3. Computes distance based on shared cluster assignments
    
    Features:
    - Uses multiple random initializations for robust clustering
    - Normalizes windows to handle scaling differences
    - Supports weighted cluster assignments
    '

    def __init__(self, *args, **kwargs):
        '
        Initialize the Cluster Membership Distance calculator.
        
        Args:
            n_clusters: Number of clusters to use
            window_size: Size of sliding windows
            max_iter: Maximum number of k-means iterations
            n_init: Number of random initializations for k-means
        '
        super().__init__()
        self._type = 'vec_float'
        self._n_clusters = n_clusters
        self._window_size = window_size
        self._max_iter = max_iter
        self._n_init = n_init

    def _normalize_window(self, window: List[float]) -> List[float]:
        '
        Normalize a window to zero mean and unit variance.
        
        Args:
            window: List of values to normalize
            
        Returns:
            list: Normalized values
        '
        if (not window):
            return window
        mean = (sum(window) / len(window))
        variance = (sum((((x - mean) ** 2) for x in window)) / len(window))
        std = (math.sqrt(variance) if (variance > 0) else 1.0)
        return [((x - mean) / std) for x in window]

    def _euclidean_distance(self, x: List[float], y: List[float]) -> float:
        '
        Compute Euclidean distance between two vectors.
        
        Args:
            x: First vector
            y: Second vector
            
        Returns:
            float: Euclidean distance
        '
        return math.sqrt(sum((((a - b) ** 2) for (a, b) in zip(x, y))))

    def _kmeans_clustering(self, windows: List[List[float]]) -> List[int]:
        '
        Perform k-means clustering on the windows.
        
        Args:
            windows: List of windows to cluster
            
        Returns:
            list: Cluster assignments for each window
        '
        best_inertia = float('inf')
        best_assignments = None
        for _ in range(self._n_init):
            centroids = random.sample(windows, self._n_clusters)
            prev_centroids = None
            assignments = ([0] * len(windows))
            for _ in range(self._max_iter):
                for (i, window) in enumerate(windows):
                    min_dist = float('inf')
                    for (c_idx, centroid) in enumerate(centroids):
                        dist = self._euclidean_distance(window, centroid)
                        if (dist < min_dist):
                            min_dist = dist
                            assignments[i] = c_idx
                new_centroids = []
                for c_idx in range(self._n_clusters):
                    cluster_points = [windows[i] for i in range(len(windows)) if (assignments[i] == c_idx)]
                    if cluster_points:
                        centroid = [(sum(x) / len(cluster_points)) for x in zip(*cluster_points)]
                        new_centroids.append(centroid)
                    else:
                        new_centroids.append(random.choice(windows))
                if (prev_centroids == new_centroids):
                    break
                prev_centroids = new_centroids
                centroids = new_centroids
            inertia = sum(((self._euclidean_distance(windows[i], centroids[assignments[i]]) ** 2) for i in range(len(windows))))
            if (inertia < best_inertia):
                best_inertia = inertia
                best_assignments = assignments
        return best_assignments

    def _get_windows(self, series: List[float]) -> List[List[float]]:
        '
        Extract normalized sliding windows from a time series.
        
        Args:
            series: Input time series
            
        Returns:
            list: List of normalized windows
        '
        windows = []
        for i in range(((len(series) - self._window_size) + 1)):
            window = series[i:(i + self._window_size)]
            windows.append(self._normalize_window(window))
        return windows

    def _get_cluster_sets(self, assignments: List[int], n_windows: int) -> List[Set[int]]:
        '
        Convert cluster assignments to sets of window indices per cluster.
        
        Args:
            assignments: List of cluster assignments
            n_windows: Total number of windows
            
        Returns:
            list: List of sets containing window indices for each cluster
        '
        cluster_sets = [set() for _ in range(self._n_clusters)]
        for i in range(n_windows):
            cluster_sets[assignments[i]].add(i)
        return cluster_sets

    def compute(self, x: List[float], y: List[float]) -> float:
        '
        Compute the Cluster Membership Distance between two time series.
        
        Args:
            x: First time series
            y: Second time series
            
        Returns:
            float: Cluster Membership Distance between the series
            
        Example:
            >>> cmd = ClusterMembershipDistance(n_clusters=3, window_size=3)
            >>> ts1 = [1.0, 2.0, 3.0, 2.0, 1.0]
            >>> ts2 = [1.0, 2.0, 2.5, 2.0, 1.0]
            >>> distance = cmd.compute(ts1, ts2)
        '
        if ((len(x) < self._window_size) or (len(y) < self._window_size)):
            raise ValueError(f'Time series must have length >= {self._window_size}')
        windows_x = self._get_windows(x)
        windows_y = self._get_windows(y)
        all_windows = (windows_x + windows_y)
        assignments = self._kmeans_clustering(all_windows)
        n_windows_x = len(windows_x)
        assignments_x = assignments[:n_windows_x]
        assignments_y = assignments[n_windows_x:]
        cluster_sets_x = self._get_cluster_sets(assignments_x, n_windows_x)
        cluster_sets_y = self._get_cluster_sets(assignments_y, len(windows_y))
        total_distance = 0
        for (set_x, set_y) in zip(cluster_sets_x, cluster_sets_y):
            if (set_x or set_y):
                intersection = len((set_x & set_y))
                union = len((set_x | set_y))
                jaccard_dist = (1 - (intersection / union))
                total_distance += jaccard_dist
        return (total_distance / self._n_clusters)


    # Propriétés pour accéder aux attributs depuis Python
    @property
    def _get_windows(self):
        return self.__get_windows
    @_get_windows.setter
    def _get_windows(self, value):
        self.__get_windows = value
    @property
    def max_iter(self):
        return self._max_iter
    @max_iter.setter
    def max_iter(self, value):
        self._max_iter = value
    @property
    def _euclidean_distance(self):
        return self.__euclidean_distance
    @_euclidean_distance.setter
    def _euclidean_distance(self, value):
        self.__euclidean_distance = value
    @property
    def n_init(self):
        return self._n_init
    @n_init.setter
    def n_init(self, value):
        self._n_init = value
    @property
    def n_clusters(self):
        return self._n_clusters
    @n_clusters.setter
    def n_clusters(self, value):
        self._n_clusters = value
    @property
    def _kmeans_clustering(self):
        return self.__kmeans_clustering
    @_kmeans_clustering.setter
    def _kmeans_clustering(self, value):
        self.__kmeans_clustering = value
    @property
    def type(self):
        return self._type
    @type.setter
    def type(self, value):
        self._type = value
    @property
    def _get_cluster_sets(self):
        return self.__get_cluster_sets
    @_get_cluster_sets.setter
    def _get_cluster_sets(self, value):
        self.__get_cluster_sets = value
    @property
    def _normalize_window(self):
        return self.__normalize_window
    @_normalize_window.setter
    def _normalize_window(self, value):
        self.__normalize_window = value
    @property
    def window_size(self):
        return self._window_size
    @window_size.setter
    def window_size(self, value):
        self._window_size = value
    """
    Implementation of Cluster Membership Distance for time series comparison.
    This approach measures similarity between time series based on how often
    their subsequences are assigned to the same clusters.
    
    The algorithm:
    1. Extracts sliding windows from both time series
    2. Clusters the windows using k-means
    3. Computes distance based on shared cluster assignments
    
    Features:
    - Uses multiple random initializations for robust clustering
    - Normalizes windows to handle scaling differences
    - Supports weighted cluster assignments
    """
    
    def __init__(self, 
                 n_clusters: int = 5,
                 window_size: int = 3,
                 max_iter: int = 100,
                 n_init: int = 10)-> None:
        """
        Initialize the Cluster Membership Distance calculator.
        
        Args:
            n_clusters: Number of clusters to use
            window_size: Size of sliding windows
            max_iter: Maximum number of k-means iterations
            n_init: Number of random initializations for k-means
        """
        super().__init__()
        self.type='vec_float'
        
        self.n_clusters = n_clusters
        self.window_size = window_size
        self.max_iter = max_iter
        self.n_init = n_init
        
    def _normalize_window(self, window: List[float]) -> List[float]:
        """
        Normalize a window to zero mean and unit variance.
        
        Args:
            window: List of values to normalize
            
        Returns:
            list: Normalized values
        """
        if not window:
            return window
            
        mean = sum(window) / len(window)
        variance = sum((x - mean) ** 2 for x in window) / len(window)
        std = math.sqrt(variance) if variance > 0 else 1.0
        
        return [(x - mean) / std for x in window]
    
    def _euclidean_distance(self, x: List[float], y: List[float]) -> float:
        """
        Compute Euclidean distance between two vectors.
        
        Args:
            x: First vector
            y: Second vector
            
        Returns:
            float: Euclidean distance
        """
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(x, y)))
    
    def _kmeans_clustering(self, windows: List[List[float]]) -> List[int]:
        """
        Perform k-means clustering on the windows.
        
        Args:
            windows: List of windows to cluster
            
        Returns:
            list: Cluster assignments for each window
        """
        best_inertia = float('inf')
        best_assignments = None
        
        for _ in range(self.n_init):
            # Initialize centroids randomly
            centroids = random.sample(windows, self.n_clusters)
            prev_centroids = None
            assignments = [0] * len(windows)
            
            # Iterate until convergence or max_iter
            for _ in range(self.max_iter):
                # Assign points to nearest centroid
                for i, window in enumerate(windows):
                    min_dist = float('inf')
                    for c_idx, centroid in enumerate(centroids):
                        dist = self._euclidean_distance(window, centroid)
                        if dist < min_dist:
                            min_dist = dist
                            assignments[i] = c_idx
                
                # Update centroids
                new_centroids = []
                for c_idx in range(self.n_clusters):
                    cluster_points = [windows[i] for i in range(len(windows)) 
                                   if assignments[i] == c_idx]
                    if cluster_points:
                        centroid = [sum(x)/len(cluster_points) for x in zip(*cluster_points)]
                        new_centroids.append(centroid)
                    else:
                        # If empty cluster, reinitialize randomly
                        new_centroids.append(random.choice(windows))
                
                # Check convergence
                if prev_centroids == new_centroids:
                    break
                prev_centroids = new_centroids
                centroids = new_centroids
            
            # Calculate inertia (sum of squared distances to centroids)
            inertia = sum(self._euclidean_distance(windows[i], centroids[assignments[i]]) ** 2 
                         for i in range(len(windows)))
            
            if inertia < best_inertia:
                best_inertia = inertia
                best_assignments = assignments
        
        return best_assignments
    
    def _get_windows(self, series: List[float]) -> List[List[float]]:
        """
        Extract normalized sliding windows from a time series.
        
        Args:
            series: Input time series
            
        Returns:
            list: List of normalized windows
        """
        windows = []
        for i in range(len(series) - self.window_size + 1):
            window = series[i:i + self.window_size]
            windows.append(self._normalize_window(window))
        return windows
    
    def _get_cluster_sets(self, assignments: List[int], n_windows: int) -> List[Set[int]]:
        """
        Convert cluster assignments to sets of window indices per cluster.
        
        Args:
            assignments: List of cluster assignments
            n_windows: Total number of windows
            
        Returns:
            list: List of sets containing window indices for each cluster
        """
        cluster_sets = [set() for _ in range(self.n_clusters)]
        for i in range(n_windows):
            cluster_sets[assignments[i]].add(i)
        return cluster_sets
    
    def compute(self, x: List[float], y: List[float]) -> float:
        """
        Compute the Cluster Membership Distance between two time series.
        
        Args:
            x: First time series
            y: Second time series
            
        Returns:
            float: Cluster Membership Distance between the series
            
        Example:
            >>> cmd = ClusterMembershipDistance(n_clusters=3, window_size=3)
            >>> ts1 = [1.0, 2.0, 3.0, 2.0, 1.0]
            >>> ts2 = [1.0, 2.0, 2.5, 2.0, 1.0]
            >>> distance = cmd.compute(ts1, ts2)
        """
        # Check if series are long enough
        if len(x) < self.window_size or len(y) < self.window_size:
            raise ValueError(f"Time series must have length >= {self.window_size}")
        
        # Extract windows
        windows_x = self._get_windows(x)
        windows_y = self._get_windows(y)
        all_windows = windows_x + windows_y
        
        # Perform clustering
        assignments = self._kmeans_clustering(all_windows)
        
        # Get cluster sets for both series
        n_windows_x = len(windows_x)
        assignments_x = assignments[:n_windows_x]
        assignments_y = assignments[n_windows_x:]
        
        cluster_sets_x = self._get_cluster_sets(assignments_x, n_windows_x)
        cluster_sets_y = self._get_cluster_sets(assignments_y, len(windows_y))
        
        # Calculate Jaccard distances between cluster assignments
        total_distance = 0
        for set_x, set_y in zip(cluster_sets_x, cluster_sets_y):
            if set_x or set_y:  # Avoid division by zero
                intersection = len(set_x & set_y)
                union = len(set_x | set_y)
                jaccard_dist = 1 - (intersection / union)
                total_distance += jaccard_dist
        
        # Normalize by number of clusters
        return total_distance / self.n_clusters


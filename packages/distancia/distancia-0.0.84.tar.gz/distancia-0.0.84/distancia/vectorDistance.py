
from .mainClass import Distance
from .tools     import Generation,degrees_to_radians,sin,cos,atan2,log,spearman_correlation

from typing import List, Union,Tuple,Optional

from itertools import zip_longest
import math

class vectorDistance(Distance):

    def __init__(self)-> None:
        super().__init__()
        self.type='vec_float'
        
    def check_data_dimension(self,data1,data2):
      c_name=self.__class__.__name__
      str_raise=f'In {c_name} class, '   
      if c_name=='Euclidean'or c_name=='L2'or c_name=='Manhattan'or  c_name=='L1'or  c_name=='Minkowski'or  c_name=='RussellRao' or  c_name=='Chebyshev'or  c_name=='KendallTau'or  c_name=='Canberra' or  c_name=='BrayCurtis'or  c_name=='Matching'or  c_name=='Kulsinski'or  c_name=='Yule' or  c_name=='Bhattacharyya'or  c_name=='Gower'or  c_name=='Hellinger' or  c_name=='CzekanowskiDice' or  c_name=='Wasserstein' :
        if len(data1) != len(data2):
          raise ValueError(str_raise+'points must have the same dimensions')  
        else: return True
          
    def check_data_type(self,data_list):
        print(self.type)
        tv=TypeValidate()
        if self.type=='vec_float':
          return tv._list(data_list,float)
        if self.type=='vec_int':
          return tv._list(data_list,int)
        if self.type=='vec_proba':
          return tv._list(data_list,proba)
        if self.type=='vec_nn':
          return tv._list(data_list,bin)
        if self.type=='vec_str':
          return tv._list(data_list,'letter')
        if self.type=='vec_bool':
          return tv._list(data_list,bool)      
           
    def example(self):
		
      if self.type=='vec_float':
        self.obj1_example=Vector()  .generate(4)
        self.obj2_example=Vector()  .generate(4)
      if self.type=='vec_proba':
        self.obj1_example=Vector()  .generate(4,form='proba')
        self.obj2_example=Vector()  .generate(4,form='proba')
      if self.type=='vec_nn':
        self.obj1_example=Vector()  .generate(4,form='bin')
        self.obj2_example=Vector()  .generate(4,form='proba')
      if self.type=='vec_str':
        self.obj1_example = Vector().generate(4,form='letter')
        self.obj2_example = Vector().generate(4,form='letter')   
      if self.type=='vec_int':
        self.obj1_example=Vector()  .generate(4,form='int')
        self.obj2_example=Vector()  .generate(4,form='int')
      if self.type=='vec_bin':
        self.obj1_example=Vector()  .generate(4,form='bin')
        self.obj2_example=Vector()  .generate(4,form='bin')
      if self.type=='vec_bool':
       self.obj1_example=Vector()   .generate(4,form='bool')
       self.obj2_example=Vector()   .generate(4,form='bool')
      super().example()
##########################################################
from typing import List, Any, Type, TypeVar, Union, Optional, cast, Callable, Dict
import numbers
from decimal import Decimal

T = TypeVar('T')

class TypeValidate:
    """
    Utility class for enforcing strict type checking on standard Python lists.
    Provides functions to verify and ensure type consistency for any list.
    """
    @staticmethod
    def _value(value: Any, target_type: Type[T]) -> T:
        """
        Strictly validate a value against a target type.
        
        Args:
            value: The value to validate
            target_type: The target type to validate against
            
        Returns:
            True or False
            
        """
        if isinstance(value, target_type):
          return True
        else:
          return False
                
    @staticmethod
    def _list(data_list: List[Any], element_type: Type[T]) -> List[T]:
        """
        Validate all elements in a list are of the specified type.
                
        Args:
            data_list: The list to validate type on
            element_type: The required type for all elements
            
        Returns:
            True or False
            
        """
        v:bool  = True
        i:int   = 0
        while v and i < len(data_list):
            if not TypeValidate._value(data_list[i], element_type):
              v=False
            i=i+1
        return v
                              
    @staticmethod
    def ensure_type(value: Any, target_type: Type[T]) -> T:
        """
        Strictly validate a value against a target type.
        
        Args:
            value: The value to validate
            target_type: The target type to validate against
            
        Returns:
            The validated value, guaranteed to be of the target type
            
        Raises:
            TypeError: If the value cannot be exactly converted to the target type
        """
        # Special handling for numeric types
        if target_type is int:
            # Accept only exact integers or values that can be converted without loss
            if isinstance(value, int):
                return cast(T, value)
            elif isinstance(value, float):
                # Only accept floats that are exact integers
                if value.is_integer():
                    return cast(T, int(value))
                raise TypeError(f"Value {value} is a float with fractional part, cannot convert to int")
            elif isinstance(value, (str, Decimal)):
                try:
                    # Try to convert and ensure no information is lost
                    float_val = float(value)
                    if float_val.is_integer():
                        return cast(T, int(float_val))
                    raise TypeError(f"Value {value} has a fractional part, cannot convert to int")
                except ValueError:
                    raise TypeError(f"Value '{value}' cannot be converted to int")
        
        elif target_type is float:
            # Accept float, int, or values that can be exactly converted
            if isinstance(value, float):
                return cast(T, value)
            elif isinstance(value, int):
                return cast(T, float(value))
            elif isinstance(value, (str, Decimal)):
                try:
                    return cast(T, float(value))
                except ValueError:
                    raise TypeError(f"Value '{value}' cannot be converted to float")
        
        # For other types, use direct instance checking
        elif isinstance(value, target_type):
            return cast(T, value)
        
        # For string types, attempt conversion for specific target types
        elif isinstance(value, str):
            # Add specific string conversion logic for other types if needed
            pass
        
        # If we get here, the value is not compatible
        raise TypeError(f"Value {value} of type {type(value).__name__} is not compatible "
                      f"with target type {target_type.__name__}")

    @staticmethod
    def ensure_list(data_list: List[Any], element_type: Type[T]) -> List[T]:
        """
        Ensure all elements in a list are of the specified type.
        Modifies the list in place and returns the modified list.
        
        Args:
            data_list: The list to enforce type on
            element_type: The required type for all elements
            
        Returns:
            The modified list with all elements validated and converted
            
        Raises:
            TypeError: If any element cannot be converted to the required type
        """
        for i in range(len(data_list)):
            data_list[i] = TypeValidate.ensure_type(data_list[i], element_type)
        return data_list
        
    def autodetect(data_list: List[Any]) -> list:
        """
        List of type in data_list.
        
        Args:
            data_list: The list to enforce type on
            
        Returns:
            The type list
            
        Raises:
        """
        element_type=[type(data_list[0])]
        for d in data_list:
          if type(d) not in element_type:
            element_type.append(type(d))
        return element_type
##########################################################
class Vector(Generation):
	
	@staticmethod
	def display(vector: List[float]) -> None:
		"""
		Display a Vector in a readable format.
    
		Args:
			Vector (List[Number]): Vatrix to display
		"""
		print([f"{x:>5.2f}" for x in vector])
		
	@staticmethod
	def norm(vec) -> float:
		"""
		Calculate the norm (magnitude) of a vector.
    
		:param vec: Input vector
		:return: Norm of the vector
		"""
		return (sum(x * x for x in vec))**0.5
		
	@staticmethod
	def normalize(vector: List[float]) -> Tuple[List[float], float]:
		"""
		Normalize a vector and return its norm
        
		Args:
			vector: Input vector
            
		Returns:
			Tuple[List[float], float]: Normalized vector and its norm
		"""
		norm = math.sqrt(sum(x*x for x in vector))
		if norm < 1e-10:  # Avoid division by zero
			return vector, 0.0
		return [x/norm for x in vector], norm
        
	@staticmethod
	def dot_product(vec1, vec2) -> float:
		"""
		Calculate the dot product between two vectors.
    
		:param vec1: First vector
		:param vec2: Second vector
		:return: Dot product of vec1 and vec2
		"""
		return sum(x * y for x, y in zip(vec1, vec2))
		
	def generate(self, cols: int, form:str='float'):
		return self.generate_vector(cols,form)
###########################################################
class Euclidean(vectorDistance):

    def __init__(self)-> None:
        super().__init__()
        self.type='vec_float'

    @staticmethod
    def vector_distance(v1: List[float], v2: List[float]) -> float:
        """
        Calculate the Euclidean distance between two vectors.

        Args:
            v1: First vector (list of floats)
            v2: Second vector (list of floats)

        Returns:
            The Euclidean distance between v1 and v2

        Raises:
            ValueError: If vectors have different lengths
        """
        if len(v1) != len(v2):
            raise ValueError("Vectors must have the same length")

        return math.dist(v1,v2)

    @staticmethod
    def matrix_distance(m1: List[List[float]], m2: List[List[float]]) -> List[List[float]]:
        """
        Calculate the Euclidean distance between each point in two matrices.

        Args:
            m1: First matrix (list of lists of floats)
            m2: Second matrix (list of lists of floats)

        Returns:
            A matrix of Euclidean distances

        Raises:
            ValueError: If matrices have different dimensions or if rows have different lengths
        """
        if len(m1) != len(m2) or any(len(row1) != len(row2) for row1, row2 in zip(m1, m2)):
            raise ValueError("Matrices must have the same dimensions")
        v1 = list(chain.from_iterable(m1))
        v2 = list(chain.from_iterable(m2))

        return math.dist(v1,v2)

    @classmethod
    def compute(cls, a: Union[List[float], List[List[float]]], b: Union[List[float], List[List[float]]]) -> Union[float, List[List[float]]]:
        """
        Calculate the Euclidean distance between two vectors or matrices.

        This method automatically detects whether the inputs are vectors or matrices
        and calls the appropriate distance calculation method.

        Args:
            a: First vector or matrix
            b: Second vector or matrix

        Returns:
            The Euclidean distance (float for vectors, matrix for matrices)

        Raises:
            ValueError: If inputs are not of the same type or have incompatible dimensions
        """
        if isinstance(a[0], (int, float)) and isinstance(b[0], (int, float)):
            return cls.vector_distance(a, b)
        elif isinstance(a[0], list) and isinstance(b[0], list):
            return cls.matrix_distance(a, b)
        else:
            raise ValueError("Inputs must be either two vectors or two matrices")
            
class L2(Euclidean):
	def __init__(self):
		super().__init__()

class Manhattan(vectorDistance):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='vec_float'

	def compute(self,point1:list, point2:list) -> int:
		"""
		Calculate the Manhattan distance, taxicab or L1 between two points.
    
		:param point1: First point as a list of coordinates
		:param point2: Second point as a list of coordinates
		:return: Manhattan distance between point1 and point2
		:raises ValueError: If the points are not of the same dimension
		"""  
		distance = sum(abs(p1 - p2) for p1, p2 in zip(point1, point2))
		return distance
		
class L1(Manhattan):
	def __init__(self)-> None:
		super().__init__()

class InverseTanimoto(vectorDistance):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='vec_str'

	def compute(self, list_a:list, list_b:list) -> float:
		"""
		Calculate the Inverse Tanimoto coefficient between two sets.

		Parameters:
		- set_a: First set of elements.
		- set_b: Second set of elements.

		Returns:
		- Inverse Tanimoto coefficient: A float value representing the dissimilarity between the two sets.
		"""
		set_a=set(list_a)
		set_b=set(list_b)
		# Calculate the intersection and union of the two sets
		intersection = set(set_a).intersection(set(set_b))
		union = set_a.union(set_b)

		# Handle the edge case where the union is empty
		if not union:
			return 0.0

		# Calculate the Inverse Tanimoto coefficient
		inverse_tanimoto = (len(union) - len(intersection)) / len(union)

		return inverse_tanimoto




class Minkowski(vectorDistance):
	
	def __init__(self, p=3)-> None:
		super().__init__()
		self.p=p
		
	def compute(self,point1:list, point2:list) -> float:
		"""
		Calculate the Minkowski distance between two points.
    
		:param point1: First point as a list of coordinates
		:param point2: Second point as a list of coordinates
		:param p: The order of the Minkowski distance
		:return: Minkowski distance between point1 and point2
		:raises ValueError: If the points are not of the same dimension
		"""
		distance = sum(abs(p1 - p2) ** self.p for p1, p2 in zip(point1, point2)) ** (1 / self.p)
		return distance
		
	def exemple(self):
		self.obj3_exemple = self.p
		super().exemple()

class RussellRao(vectorDistance):
    def __init__(self )-> None:
        """
        Initialize the Russell-Rao class with two binary vectors.

        :param vector1: First binary vector for comparison.
        :param vector2: Second binary vector for comparison.
        """
        super().__init__()

        
    def compute(self,vector1 :list, vector2 :list) -> float:
        """
        Calculate the Russell-Rao distance between the two binary vectors.

        :return: The Russell-Rao distance as a float.
        """
        # Calculate the number of matching features (both present)
        a = sum(v1 and v2 for v1, v2 in zip(vector1, vector2))

        # Calculate the total number of features
        n = len(vector1)

        # Calculate the Russell-Rao distance
        distance = a / n

        return distance
        
class Chebyshev(vectorDistance):
	
	def __init__(self)-> None:
		super().__init__()

	def compute(self,point1 :list, point2 :list) -> float:

		"""
		Calculate the Chebyshev distance between two points.
    
		:param point1: A list of coordinates for the first point
		:param point2: A list of coordinates for the second point
		:return: Chebyshev distance between the two points
		:raises ValueError: If the points do not have the same dimensions
		"""
    
		return max(abs(a - b) for a, b in zip(point1, point2))


class Hausdorff(vectorDistance):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='tuple_float'


	def compute(self,set1 :tuple, set2 :tuple) -> float:
		"""
		Calculate the Hausdorff distance between two sets of points.
    
		:param set1: The first set of points, each point represented as a tuple (x, y)
		:param set2: The second set of points, each point represented as a tuple (x, y)
		:return: Hausdorff distance between the two sets of points
		"""
		def max_min_distance(set_a, set_b):
			"""
			Helper function to find the maximum of the minimum distances from each point in set_a to the closest point in set_b.
        
			:param set_a: The first set of points
			:param set_b: The second set of points
			:return: Maximum of the minimum distances
			"""
			max_min_dist = 0
			for point_a in set_a:
				min_dist = float('inf')
				for point_b in set_b:
					dist = Euclidean().calculate(point_a, point_b)
					if dist < min_dist:
						min_dist = dist
				if min_dist > max_min_dist:
					max_min_dist = min_dist
			return max_min_dist

		return max(max_min_distance(set1, set2), max_min_distance(set2, set1))
		
	def example(self):
		self.obj1_example = [(0, 0), (0, 1), (1, 0), (1, 1)]
		self.obj2_example = [(2, 2), (2, 3), (3, 2), (3, 3)]
		distance=self.compute(self.obj1_example,self.obj2_example)
		print(f"{self.__class__.__name__} distance between {self.obj1_example} and {self.obj2_example} is {distance:.2f}")


class KendallTau(vectorDistance):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='vec_int'

	def compute(self,permutation1 :list[int], permutation2 :list[int]) -> int:
		"""
		Calculate the Kendall Tau distance between two permutations.
    
		:param permutation1: The first permutation (a list of integers)
		:param permutation2: The second permutation (a list of integers)
		:return: Kendall Tau distance between the two permutations
		"""    
		n = len(permutation1)
		pairs = [(permutation1[i], permutation2[i]) for i in range(n)]
    
		def count_inversions(pairs :list):
			"""
			Helper function to count inversions in a list of pairs.
        
			:param pairs: List of pairs
			:return: Number of inversions
			"""
			inversions = 0
			for i in range(len(pairs)):
				for j in range(i + 1, len(pairs)):
					if (pairs[i][0] > pairs[j][0] and pairs[i][1] < pairs[j][1]) or (pairs[i][0] < pairs[j][0] and pairs[i][1] > pairs[j][1]):
						inversions += 1
			return inversions

		return count_inversions(pairs)

class Haversine(vectorDistance):
	
	def __init__(self)-> None:
		super().__init__()

	def compute(self,p1 :list,p2 :list ) -> float:
		"""
		Calculate the Haversine distance between two points on the Earth's surface.
    
		:param lat1: Latitude of the first point in decimal degrees
		:param lon1: Longitude of the first point in decimal degrees
		:param lat2: Latitude of the second point in decimal degrees
		:param lon2: Longitude of the second point in decimal degrees
		:return: Haversine distance between the two points in kilometers
		"""
		lat1, lon1=p1[0],p1[1]
		lat2, lon2=p2[0],p2[1]
		# Radius of the Earth in kilometers
		R = 6371.0
    
		# Convert latitude and longitude from degrees to radians
		lat1_rad = degrees_to_radians(lat1)
		lon1_rad = degrees_to_radians(lon1)
		lat2_rad = degrees_to_radians(lat2)
		lon2_rad = degrees_to_radians(lon2)
    
		# Differences in coordinates
		dlat = lat2_rad - lat1_rad
		dlon = lon2_rad - lon1_rad
    
		# Haversine formula
		a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
		c = 2 * atan2(a**0.5, (1 - a)**0.5)
    
		# Distance in kilometers
		distance = R * c
    
		return distance
		
	def example(self):
		self.obj1_exemple = (48.8566, 2.3522)# Paris coordinates
		self.obj2_exemple = (51.5074, -0.1278)# London coordinates
		super().example()

class Canberra(vectorDistance):
	
	def __init__(self)-> None:
		super().__init__()

	def compute(self,point1 :list, point2 :list) -> float:
		"""
		Calculate the Canberra distance between two points.
    
		:param point1: The first point (a list of numerical values)
		:param point2: The second point (a list of numerical values)
		:return: Canberra distance between the two points
		"""    
		distance = 0
		for x1, x2 in zip(point1, point2):
			numerator = abs(x1 - x2)
			denominator = abs(x1) + abs(x2)
			if denominator != 0:
				distance += numerator / denominator
    
		return distance

class BrayCurtis(vectorDistance):
	
	def __init__(self)-> None:
		super().__init__()

	def compute(self,point1 :list, point2 :list) -> float:
		"""
		Calculate the Bray-Curtis distance between two points.
    
		:param point1: The first point (a list of numerical values)
		:param point2: The second point (a list of numerical values)
		:return: Bray-Curtis distance between the two points
		"""
    
		sum_diff = 0
		sum_sum = 0
    
		for x1, x2 in zip(point1, point2):
			sum_diff += abs(x1 - x2)
			sum_sum += abs(x1 + x2)
    
		if sum_sum == 0:
			return 0  # To handle the case when both points are zeros
    
		distance = sum_diff / sum_sum
		return distance

#claude ai
from typing import List, Union

class Hamming(vectorDistance):

    def __init__(self)-> None:
      super().__init__()
      self.type='vec_int'
      
    @staticmethod
    def compute(v1: Union[str, List[int]], v2: Union[str, List[int]]) -> int:
        """
        Calculate the Hamming distance between two strings or two lists of integers.
        
        Args:
            v1: First string or list of integers
            v2: Second string or list of integers
        
        Returns:
            The Hamming distance between v1 and v2
        
        Raises:
            ValueError: If inputs are not of the same type or have different lengths
        """
        if isinstance(v1, str) and isinstance(v2, str):
            if len(v1) != len(v2):
                raise ValueError("Strings must have the same length")
            return sum(c1 != c2 for c1, c2 in zip(v1, v2))
        
        elif isinstance(v1, list) and isinstance(v2, list):
            if len(v1) != len(v2):
                raise ValueError("Lists must have the same length")
            return sum(i1 != i2 for i1, i2 in zip(v1, v2))
        
        else:
            raise ValueError("Inputs must be either two strings or two lists of integers")

    @classmethod
    def normalized_distance(cls, v1: Union[str, List[int]], v2: Union[str, List[int]]) -> float:
        """
        Calculate the normalized Hamming distance between two strings or two lists of integers.
        
        The normalized distance is the Hamming distance divided by the length of the inputs.
        This gives a value between 0 and 1, where 0 means the inputs are identical,
        and 1 means they are completely different.
        
        Args:
            v1: First string or list of integers
            v2: Second string or list of integers
        
        Returns:
            The normalized Hamming distance between v1 and v2
        """
        distance = cls.compute(v1, v2)
        return distance / len(v1)  # len(v1) is safe to use as we've checked they're equal in distance()

    def similarity(self, document1: str, document2: str) -> float:
        """
        Computes the similarity between two documents based on their SimHash values.

        :param document1: The first document as a string.
        :param document2: The second document as a string.
        :return: A similarity score between 0 (completely different) and 1 (identical).
        """
        simhash1: int = self.compute(document1)
        simhash2: int = self.compute(document2)

        # Calculate Hamming distance
        hamming_dist: int = self.hamming_distance(simhash1, simhash2)
        max_bits: int = 64

        # Compute similarity as the fraction of matching bits
        similarity_score: float = (max_bits - hamming_dist) / max_bits
        return similarity_score


class Matching(Hamming):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='vec_bin'

class Kulsinski(vectorDistance):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='vec_bin'

	def compute(self,set1 :set, set2 :set) -> float:
		"""
		Calculate the Kulsinski distance between two sets or binary vectors.
    
		:param set1: The first set (a set of elements or a list of binary values)
		:param set2: The second set (a set of elements or a list of binary values)
		:return: Kulsinski distance between the two sets or binary vectors
		"""
		if isinstance(set1, set) and isinstance(set2, set):
			# Calculate for sets
			intersection = len(set1.intersection(set2))
			union = len(set1.union(set2))
			a = intersection
			b = len(set1) - intersection
			c = len(set2) - intersection
			d = union - a - b - c
		elif isinstance(set1, list) and isinstance(set2, list):
			# Calculate for binary vectors
			a = sum(1 for x, y in zip(set1, set2) if x == 1 and y == 1)
			b = sum(1 for x, y in zip(set1, set2) if x == 1 and y == 0)
			c = sum(1 for x, y in zip(set1, set2) if x == 0 and y == 1)
			d = sum(1 for x, y in zip(set1, set2) if x == 0 and y == 0)

		n = a + b + c + d
		if b + c + n !=0:
			return (b + c - a + n) / (b + c + n)
		return 0
		

class Yule(vectorDistance):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='vec_bin'

	def compute(self,binary_vector1 :list[int], binary_vector2 :list[int]) -> float:
		"""
		Calcule la distance de Yule entre deux vecteurs binaires.
    
		:param binary_vector1: Premier vecteur binaire (liste de 0 et 1)
		:param binary_vector2: Deuxième vecteur binaire (liste de 0 et 1)
		:return: Distance de Yule
		"""
    
		# Calcul des variables a, b, c, d
		a = b = c = d = 0
    
		for bit1, bit2 in zip(binary_vector1, binary_vector2):
			if bit1 == 1 and bit2 == 1:
				a += 1
			elif bit1 == 1 and bit2 == 0:
				b += 1
			elif bit1 == 0 and bit2 == 1:
				c += 1
			elif bit1 == 0 and bit2 == 0:
				d += 1
    
		# Calcul de l'indice de dissimilarité de Yule Q
		if (a * d + b * c) == 0:
			return 0.0  # Si le dénominateur est 0, la dissimilarité est 0 (vecteurs identiques)
    
		Q = 2 * b * c / (a * d + b * c)
        
		return Q / (Q + 2 * a * d)
		
	#def exemple(self):
	#	self.obj1_exemple =  [1, 0, 1, 1, 0, 1, 0, 0, 1, 1]
	#	self.obj2_exemple = [0, 1, 1, 0, 0, 1, 0, 1, 1, 0]
	#	super().exemple()

class Bhattacharyya(vectorDistance):
	
	def __init__(self)-> None:
		super().__init__()

	def compute(self,P :list[float], Q :list[float]) -> float:
		"""
		Calcule la distance de Bhattacharyya entre deux distributions de probabilité discrètes.
    
		:param P: Première distribution de probabilité (liste de probabilités)
		:param Q: Deuxième distribution de probabilité (liste de probabilités)
		:return: Distance de Bhattacharyya
		"""
    
		# Calcul du coefficient de Bhattacharyya
		bc = 0.0
		for p, q in zip(P, Q):
			bc += (p * q)**0.5
    
		# Calcul de la distance de Bhattacharyya
		distance = -log(bc)
    
		return distance


class Gower(vectorDistance):
	
	def __init__(self,ranges=None)-> None:
		super().__init__()

		self.ranges=ranges
		
	def compute(self, vec1 :list, vec2 :list) -> float:
		"""
		Calculate the Gower similarity between two vectors.

		Parameters:
		- vec1: List of values for the first entity (can include both numerical and categorical).
		- vec2: List of values for the second entity (can include both numerical and categorical).
		- ranges: List of ranges for numerical variables. Use `None` for categorical variables.

		Returns:
		- distance: Gower distance between vec1 and vec2.
		"""

		total_similarity = 0
		num_variables = len(vec1)

		for i in range(num_variables):
			if self.ranges[i] is None:
				# Categorical variable
				if vec1[i] == vec2[i]:
					similarity = 1
				else:
				    similarity = 0
			else:
				# Numerical variable
				if vec1[i] == vec2[i]:
					similarity = 1
				else:
					range_value = self.ranges[i]
					if range_value == 0:
						similarity = 0
					else:
						similarity = 1 - abs(vec1[i] - vec2[i]) / range_value

			total_similarity += similarity

		# Normalize by the number of variables
		return 1 - total_similarity / num_variables
		
	def example(self):
		self.ranges=[None, 5.0, 10]
		vec1=["Red", 3.2, 5]
		vec2=["Blue", 4.1, 3]
		distance = self.compute(vec1, vec2)
		print(f"Gower dustance between {vec1} and {vec2}: {distance:.4f}")


class Hellinger(vectorDistance):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='vec_proba'


	def compute(self,p :list[float], q :list[float]) -> float:
		"""
		Calcule la distance de Hellinger entre deux distributions de probabilités.
    
		:param p: Première distribution de probabilités (sous forme de liste ou d'array).
		:param q: Deuxième distribution de probabilités (sous forme de liste ou d'array).
		:return: Distance de Hellinger entre p et q.
		"""
    
		# Calculer la distance de Hellinger
		sum_of_squares = sum(((p_i)**0.5 - (q_i)**0.5 ) ** 2 for p_i, q_i in zip(p, q))
    
		return (1 / 2**0.5 ) * sum_of_squares**0.5

class CzekanowskiDice(vectorDistance):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='vec_int'

	def compute(self,x :list, y :list) -> float:
		"""
		Calcule la distance Czekanowski-Dice entre deux vecteurs.
    
		:param x: Premier vecteur (sous forme de liste ou d'array).
		:param y: Deuxième vecteur (sous forme de liste ou d'array).
		:return: Distance Czekanowski-Dice entre x et y.
		"""
    
		min_sum = sum(min(x_i, y_i) for x_i, y_i in zip(x, y))
		sum_x = sum(x)
		sum_y = sum(y)
    
		if sum_x + sum_y == 0:
			return 0.0  # Pour éviter la division par zéro
    
		dice_similarity = (2 * min_sum) / (sum_x + sum_y)
    
		return 1 - dice_similarity

class Wasserstein(vectorDistance) :
	
    def __init__(self)-> None:
        """
        Initialize the Wasserstein class with two probability distributions.

        :param distribution1: First probability distribution (list of floats).
        :param distribution2: Second probability distribution (list of floats).
        """
        super().__init__()
        self.type='vec_proba'


    def compute(self, distribution1 :list, distribution2 :list)-> float:
        """
        Calculate the Wasserstein distance between the two distributions.

        :return: The Wasserstein distance as a float.
        """
    
        # Cumulative distribution functions (CDF) of both distributions
        cdf1 = self._cumulative_distribution(distribution1)
        cdf2 = self._cumulative_distribution(distribution2)

        # Wasserstein distance is the area between the CDFs
        distance = sum(abs(c1 - c2) for c1, c2 in zip(cdf1, cdf2))

        return distance

    def _cumulative_distribution(self, distribution :list[float]):
        """
        Calculate the cumulative distribution for a given distribution.

        :param distribution: A probability distribution (list of floats).
        :return: The cumulative distribution (list of floats).
        """
        cdf = []
        cumulative_sum = 0.0
        for prob in distribution:
            cumulative_sum += prob
            cdf.append(cumulative_sum)
        return cdf


#claude ai
from typing import List, TypeVar, Set, Union
T = TypeVar('T')

class Jaccard(vectorDistance):
    def __init__(self)-> None:
        super().__init__()
        self.type='vec_str'
        
    @staticmethod
    def compute(set1: List[T], set2: List[T]) -> float:
        """
        Calculate the Jaccard distance between two lists of objects.
        
        The Jaccard distance is complementary to the Jaccard index:
        distance = 1 - index
        
        Args:
            set1: First list of objects
            set2: Second list of objects
        
        Returns:
            The Jaccard distance between set1 and set2
        """
        set1_set: Set[T] = set(set1)
        set2_set: Set[T] = set(set2)
        
        intersection_size: int = len(set1_set.intersection(set2_set))
        union_size: int = len(set1_set.union(set2_set))
        
        if union_size == 0:
            return 0.0  # Both sets are empty, consider them identical
        
        jaccard_index: float = intersection_size / union_size
        return 1 - jaccard_index

    @classmethod
    def similarity(cls, set1: List[T], set2: List[T]) -> float:
        """
        Calculate the Jaccard similarity (index) between two lists of objects.
        
        Args:
            set1: First list of objects
            set2: Second list of objects
        
        Returns:
            The Jaccard similarity between set1 and set2
        """
        return 1 - cls.compute(set1, set2)

# Example for jaccard custom class to demonstrate usage with user-defined objects
class CustomObject:
    def __init__(self, value: Union[str, int]):
        self.value = value
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CustomObject):
            return NotImplemented
        return self.value == other.value
    
    def __hash__(self) -> int:
        return hash(self.value)
    
    def __repr__(self) -> str:
        return f"CustomObject({self.value})"

class Tanimoto(Jaccard):
	
	def __init__(self)-> None:
		super().__init__()
		
class GeneralizedJaccard(vectorDistance):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='vec_int'

	def compute(self,x :list, y :list)-> float:
		"""
		Calcule la distance de Jaccard généralisée entre deux vecteurs.
    
		:param x: Premier vecteur (sous forme de liste ou d'array).
		:param y: Deuxième vecteur (sous forme de liste ou d'array).
		:return: Distance de Jaccard généralisée entre x et y.
		"""
		if len(x) != len(y):
			raise ValueError("Les vecteurs doivent avoir la même longueur.")
    
		min_sum = sum(min(x_i, y_i) for x_i, y_i in zip(x, y))
		max_sum = sum(max(x_i, y_i) for x_i, y_i in zip(x, y))
    
		if max_sum == 0:
			return 0.0  # Pour éviter la division par zéro
        
		return 1 - (min_sum / max_sum)
		
	def example(self):
		#self.obj1_example = {1, 2, 3, 4}
		#self.obj2_example = {3, 4, 5, 6}
		super().example()

  
class Pearson(vectorDistance):
	
	def __init__(self)-> None:
		super().__init__()

	def compute(self,x :list[float], y :list[float])-> float:
		"""
		Calcule le coefficient de corrélation de Pearson entre deux listes de données.

		:param x: Liste des valeurs de la première variable.
		:param y: Liste des valeurs de la seconde variable.
		:return: Coefficient de corrélation de Pearson entre x et y.
		"""
		if len(x) != len(y):
			raise ValueError("Les listes x et y doivent avoir la même longueur.")
    
		n = len(x)
    
		# Calcul des moyennes
		mean_x = sum(x) / n
		mean_y = sum(y) / n
    
		# Calcul des covariances et des variances
		cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
		var_x = sum((x[i] - mean_x) ** 2 for i in range(n))
		var_y = sum((y[i] - mean_y) ** 2 for i in range(n))
    
		# Calcul du coefficient de corrélation de Pearson
		if var_x == 0 or var_y == 0:
			raise ValueError("L'écart-type ne peut pas être nul.")
    
		pearson_corr = cov_xy / (var_x ** 0.5 * var_y ** 0.5)
    
		return 1 - pearson_corr
		
	def exemple(self):
		self.obj1_exemple = [1, 1, 3, 4, 5]
		self.obj2_exemple = [2, 3, 4, 5, 6]
		super().exemple()


class Spearman(vectorDistance):
	
	def __init__(self)-> None:
		super().__init__()

	def compute(self,x :list[float], y :list[float])-> float:
		"""
		Calcule la distance de Spearman entre deux listes de données.
    
		:param x: Liste des valeurs de la première variable.
		:param y: Liste des valeurs de la seconde variable.
		:return: Distance de Spearman entre x et y.
		"""
		spearman_corr = spearman_correlation(x, y)
		# La distance de Spearman est 1 moins le coefficient de corrélation de Spearman
		distance = 1 - spearman_corr
    
		return distance
		
	def exemple(self):
		self.obj1_exemple = [1, 2, 3, 4, 5]
		self.obj2_exemple = [5, 6, 7, 8, 7]
		super().exemple()
		

#claude ai
from typing import Union, Set, List, TypeVar
from collections.abc import Iterable
T = TypeVar('T')

class Ochiai(vectorDistance):
	
	def __init__(self)-> None:
		super().__init__()
		self.type='vec_bool'
		"""
		A class to calculate the Ochiai distance between two sets or lists.
    
		The Ochiai distance is a similarity measure between two sets, defined as:
		Ochiai = |A ∩ B| / sqrt(|A| * |B|)
		where A and B are the two sets being compared.
    
		This implementation supports both sets and lists as input.
		"""
    
	@staticmethod
	def _convert_to_set(input_data: Union[Set[T], List[T]]) -> Set[T]:
		"""
		Convert input data to a set if it's not already a set.
        
		Args:
			input_data: Input collection (either Set or List)
            
		Returns:
			Set containing the input elements
            
		Raises:
			TypeError: If input is neither a Set nor a List
		"""
		if isinstance(input_data, set):
			return input_data
		if isinstance(input_data, list):
			return set(input_data)
		raise TypeError("Input must be either a Set or a List")
    
	@staticmethod
	def validate_input(input_data: Union[Set[T], List[T]]) -> None:
		"""
		Validate that the input is a non-empty collection.
        
		Args:
			input_data: Input collection to validate
            
			Raises:
				ValueError: If input is empty
			TypeError: If input is not an iterable
		"""
		if not isinstance(input_data, Iterable):
			raise TypeError("Input must be an iterable (Set or List)")
		if not input_data:
			raise ValueError("Input collections cannot be empty")
    
	def compute(self, set_a: Union[Set[T], List[T]], 
                 set_b: Union[Set[T], List[T]]) -> float:
		"""
		Calculate the Ochiai distance between two collections.
        
		Args:
			set_a: First collection (Set or List)
			set_b: Second collection (Set or List)
            
		Returns:
			float: Ochiai distance between the two collections (between 0 and 1)
            
		Raises:
			ValueError: If either input is empty
		TypeError: If inputs are not of correct type
			ZeroDivisionError: If either collection is empty after conversion
		"""
		# Validate inputs
		self.validate_input(set_a)
		self.validate_input(set_b)
        
		# Convert inputs to sets
		set_a_conv = self._convert_to_set(set_a)
		set_b_conv = self._convert_to_set(set_b)

		# Calculate intersection
		intersection = set_a_conv.intersection(set_b_conv)
        
		# Calculate denominator
		denominator = (len(set_a_conv) * len(set_b_conv))**0.5
        
		# Handle division by zero
		if denominator == 0:
			raise ZeroDivisionError("Cannot calculate Ochiai distance: "
                                  "denominator is zero")
        
		# Calculate and return Ochiai distance
		return 1.0 - len(intersection) / denominator
		

class MotzkinStraus(vectorDistance):
	
	def __init__(self,p=2)-> None:
		super().__init__()

		self.p=p
		
	def compute(self,x :list[float], y :list[float])-> float:
		"""
		Calcule une distance hypothétique Motzkin-Straus généralisée entre deux vecteurs.
    
		:param x: Premier vecteur (sous forme de liste ou d'array).
		:param y: Deuxième vecteur (sous forme de liste ou d'array).
		:param p: Paramètre pour la norme de Minkowski (par défaut 2 pour la distance Euclidienne).
		:return: Distance Motzkin-Straus entre x et y.
		"""
		if len(x) != len(y):
			raise ValueError("Les vecteurs doivent avoir la même longueur.")
    
		# Calcul de la norme de Minkowski (généralement Euclidienne pour p=2)
		minkowski_distance=Minkowski(self.p).compute(x,y)
    
		# Ajout d'une composante structurelle simple (hypothétique)
		structure_distance = sum((x_i - y_i)**2 for x_i, y_i in zip(x, y)) / len(x)
    
		# Combinaison des deux distances
		motzkin_straus_distance = minkowski_distance + structure_distance
    
		return motzkin_straus_distance
		

class EnhancedRogersTanimoto(vectorDistance):
	
	def __init__(self, alpha=1)-> None:
		super().__init__()
		self.alpha=alpha
		self.type='vec_bin'

	def compute(self,vector_a :list[int], vector_b :list[int])-> float:
		"""
		Calcule la distance Rogers-Tanimoto améliorée entre deux vecteurs binaires.
    
		:param vector_a: Premier vecteur (de type list).
		:param vector_b: Deuxième vecteur (de type list).
		:param alpha: Facteur de régularisation (par défaut: 1).
		:return: Distance Rogers-Tanimoto améliorée entre vector_a et vector_b.
		"""
		if len(vector_a) != len(vector_b):
			raise ValueError("Les deux vecteurs doivent avoir la même longueur")
    
		a = b = c = d = 0
    
		for i in range(len(vector_a)):
			if vector_a[i] == 1 and vector_b[i] == 1:
				a += 1
			elif vector_a[i] == 1 and vector_b[i] == 0:
				b += 1
			elif vector_a[i] == 0 and vector_b[i] == 1:
				c += 1
			elif vector_a[i] == 0 and vector_b[i] == 0:
				d += 1
    
		# Calcul de la distance Rogers-Tanimoto améliorée
		return (a + b + c) / (a + b + c + d + self.alpha)

#import numpy as np
#from numpy import ones, pad, convolve,dot,linalg


class ContextualDynamicDistance(vectorDistance):
    
	def __init__(self)-> None:
		super().__init__()

		"""
		Initialize the CDD with a context weight function.
        
		:param context_weight_func: A function that takes in the contexts of two points
                                    and returns the weight for each feature.
		"""

	def compute(self, x :list, y :list, context_x :list, context_y :list)-> float:
		"""
		Calculate the Contextual Dynamic Distance (CDD) between two points.
        
		:param x: List or vector representing the first data point.
		:param y: List or vector representing the second data point.
		:param context_x: List or vector representing the context of the first data point.
		:param context_y: List or vector representing the context of the second data point.
        
		:return: The CDD value as a float.
		"""
		if len(x) != len(y) or len(context_x) != len(context_y):
			raise ValueError("Data points and contexts must be of the same length.")
        
		distance = 0.0
		for i in range(len(x)):
			weight = self.convolution_context_weight_func(context_x, context_y, i)
			distance += weight * (x[i] - y[i]) ** 2
        
		return distance ** 0.5

	def convolution_context_weight_func(self,context_x :list, context_y :list, index :int, kernel_size=3):
		"""
		A context weight function based on convolution.
    
		:param context_x: Context vector for the first point.
		:param context_y: Context vector for the second point.
		:param index: Current index for which the weight is calculated.
		:param kernel_size: Size of the convolution kernel.
    
		:return: The weight for the feature at the given index as a float.
		"""
		half_kernel = kernel_size // 2

		# Define convolution kernel (e.g., a simple averaging kernel)
		#kernel = np.ones(kernel_size) / kernel_size
		kernel = [1/ kernel_size for _ in range(kernel_size)]
		
		# Extract the relevant sub-contexts around the current index
		sub_context_x = context_x[max(0, index - half_kernel):min(len(context_x), index + half_kernel + 1)]
		sub_context_y = context_y[max(0, index - half_kernel):min(len(context_y), index + half_kernel + 1)]

		# Convolve the contexts with the kernel
		conv_x=0
		for i,j in zip(kernel,sub_context_x):
			conv_x+=i*j
		conv_y=0
		for i,j in zip(kernel,sub_context_y):
			conv_y+=i*j

		# Calculate the weight as the similarity of the convolved signals
		similarity = sum([x*y for x,y in zip(conv_x, conv_y)]) / ( (sum([_**2 for _ in conv_x]))^0.5 * (sum([_**2 for _ in conv_y]))^0.5 + 1e-10)
		return similarity
		
	def exemple(self):
		# Feature vectors
		self.obj1_exemple = [1.0, 2.0, 3.0]
		self.obj2_exemple = [4.0, 5.0, 6.0]
		# Context vectors
		self.obj3_exemple = [0.2, 0.3, 0.5]
		self.obj4_exemple = [0.1, 0.4, 0.6]
		super().exemple()
		

class Otsuka(vectorDistance):
    def __init__(self)-> None:
        """
        Initialize the Otsuka class with two categorical vectors.

        :param vector1: First categorical vector (list of strings).
        :param vector2: Second categorical vector (list of strings).
        """
        super().__init__()

    def compute(self, vector1 :list, vector2 :list)-> float:
        """
        Calculate the Otsuka distance between the two categorical vectors.

        :return: The Otsuka distance as a float.
        """
        if len(vector1) != len(vector2):
            raise ValueError("Vectors must be of the same length.")

        a = b = c = d = 0

        for v1, v2 in zip(vector1, vector2):
            if v1 == v2:
                a += 1
            elif v1 != v2 and v1 != 'X' and v2 != 'X':
                b += 1
            elif v1 != v2 and v1 == 'X':
                c += 1
            elif v1 != v2 and v2 == 'X':
                d += 1

        total = a + b + c + d
        if total == 0:
            return 0.0

        return 0.5 * ( (a + d) / total + (b + c) / total )

class RogersTanimoto(vectorDistance):
    def __init__(self)-> None:
        """
        Initialize the Rogers-Tanimoto class with two binary vectors.

        :param vector1: First binary vector for comparison.
        :param vector2: Second binary vector for comparison.
        """
        super().__init__()
        self.type='vec_int'

    def compute(self, vector1 :list[int], vector2 :list[int])-> float:
        """
        Calculate the Rogers-Tanimoto distance between the two binary vectors.

        :return: The Rogers-Tanimoto distance as a float.
        """
        if len(vector1) != len(vector2):
            raise ValueError("Vectors must be of the same length")
        self.vector1 = vector1
        self.vector2 = vector2
        # Calculate the components of the formula
        a = sum(v1 and v2 for v1, v2 in zip(self.vector1, self.vector2))  # Both are 1
        b = sum(v1 and not v2 for v1, v2 in zip(self.vector1, self.vector2))  # Present in vector1 but not in vector2
        c = sum(not v1 and v2 for v1, v2 in zip(self.vector1, self.vector2))  # Present in vector2 but not in vector1
        d = sum(not v1 and not v2 for v1, v2 in zip(self.vector1, self.vector2))  # Both are 0

        # Calculate the Rogers-Tanimoto distance
        distance = (a + b + c) / (a + b + c + d)

        return distance


class SokalMichener(vectorDistance):
    def __init__(self)-> None:
        """
        Initialize the SokalMichener class with two binary vectors.

        :param vector1: First binary vector for comparison.
        :param vector2: Second binary vector for comparison.
        """
        super().__init__()

    def compute(self, vector1 :list[int], vector2 :list[int])-> float:
        """
        Calculate the Sokal-Michener distance between the two binary vectors.

        :return: The Sokal-Michener distance as a float.
        """
        if len(vector1) != len(vector2):
            raise ValueError("Vectors must be of the same length")
        # Number of matches where both vectors have 1s (a)
        a = sum(v1 and v2 for v1, v2 in zip(vector1, vector2))

        # Number of matches where both vectors have 0s (d)
        d = sum((not v1) and (not v2) for v1, v2 in zip(vector1, vector2))

        # Total number of features (n)
        n = len(vector1)

        # Calculate the Sokal-Michener distance
        similarity = (a + d) / n
        distance = 1 - similarity

        return distance

class SokalSneath(vectorDistance):
    def __init__(self)-> None:
        """
        Initialize the SokalSneath class with two binary vectors.

        :param vector1: First binary vector for comparison.
        :param vector2: Second binary vector for comparison.
        """
        super().__init__()
        self.type='vec_int'

    def compute(self, vector1 :list[int], vector2 :list[int])-> float:
        """
        Calculate the Sokal-Sneath distance between the two binary vectors.

        :return: The Sokal-Sneath distance as a float.
        """
        if len(vector1) != len(vector2):
            raise ValueError("Vectors must be of the same length")
        # Number of matches where both vectors have 1s (a)
        a = sum(v1 and v2 for v1, v2 in zip(vector1, vector2))

        # Number of mismatches where vector1 has 1 and vector2 has 0 (b)
        b = sum(v1 and not v2 for v1, v2 in zip(vector1, vector2))

        # Number of mismatches where vector1 has 0 and vector2 has 1 (c)
        c = sum(not v1 and v2 for v1, v2 in zip(vector1, vector2))

        # Calculate the Sokal-Sneath distance
        distance = (c + 2 * b) / (a + b + c)

        return distance
        
class FagerMcGowan(vectorDistance):
	
	def __init__(self, N:int)-> None:
		super().__init__()
		self.type='vec_word'
		self.N=N
		"""
		FagerMcGowan similarity coefficient calculator.

		The FagerMcGowan similarity coefficient is used to measure the similarity 
		between two sets, particularly in ecological studies. It adjusts for the 
		expected overlap due to random chance, providing a more accurate reflection 
		of true similarity.

		Methods:
		--------
		compute(set1, set2, N):
			Calculates the FagerMcGowan similarity coefficient between two sets.
		"""

	def compute(self, set1: List[T], set2: List[T])-> float:
		"""
		Calculate the Fager-McGowan similarity coefficient between two sets.

		Parameters:
		-----------
		set1 : set
			The first set of elements (e.g., species in a habitat).
		set2 : set
			The second set of elements.
		N : int
			The total number of unique elements in the universal set.

		Returns:
		--------
			float
				The Fager-McGowan distance coefficient.
		"""
		set1_set: Set[T] = set(set1)
		set2_set: Set[T] = set(set2)
        
		intersection_size: int = len(set1_set.intersection(set2_set))

		set1_size = len(set1)  # Size of the first set
		set2_size = len(set2)  # Size of the second set

		# Calculate the Fager-McGowan similarity coefficient
		numerator = intersection_size - (set1_size * set2_size / self.N)
		denominator = min(set1_size, set2_size)

		if denominator == 0:
			return 0.0

		similarity = numerator / denominator
		return 1 - similarity
		
	def example(self):
			super().example()
			
from typing import List
import math

class JensenShannonDivergence(vectorDistance):

    def __init__(self) -> None:
        super().__init__()

    def compute(self, dist1: List[float], dist2: List[float]) -> float:
        """
        Calcule la Jensen-Shannon Divergence entre deux distributions de probabilités.

        :param dist1: Première distribution de probabilités (somme égale à 1).
        :param dist2: Deuxième distribution de probabilités (somme égale à 1).
        :return: La divergence Jensen-Shannon entre les deux distributions.
        """
        if len(dist1) != len(dist2):
            raise ValueError("Les distributions doivent avoir la même longueur")

        # Calcul de la distribution moyenne
        avg_dist: List[float] = [(p1 + p2) / 2 for p1, p2 in zip(dist1, dist2)]

        # Calcul de la divergence KL pour les deux distributions par rapport à la distribution moyenne
        kl_div1: float = self._kl_divergence(dist1, avg_dist)
        kl_div2: float = self._kl_divergence(dist2, avg_dist)

        # La Jensen-Shannon Divergence est la moyenne des deux divergences KL
        return (kl_div1 + kl_div2) / 2

    def _kl_divergence(self, dist_p: List[float], dist_q: List[float]) -> float:
        """
        Calcule la Kullback-Leibler Divergence entre deux distributions.

        :param dist_p: Distribution de probabilité p.
        :param dist_q: Distribution de probabilité q.
        :return: La divergence KL entre les distributions p et q.
        """
        divergence: float = 0.0
        for p, q in zip(dist_p, dist_q):
            if p > 0 and q > 0:
                divergence += p * math.log(p / q)
        return divergence
'''
# Exemple d'utilisation
dist1: List[float] = [0.4, 0.3, 0.2, 0.1]
dist2: List[float] = [0.3, 0.3, 0.2, 0.2]

# Créer une instance de la classe Jensen-Shannon Divergence
js_divergence = JensenShannonDivergence()

# Calculer la Jensen-Shannon Divergence
divergence: float = js_divergence.compute(dist1, dist2)
print(f"Jensen-Shannon Divergence: {divergence}")
'''

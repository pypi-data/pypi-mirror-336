###################################################

#################################
#Loss function
#################################
from .mainClass import *
from .tools     import log,exp

import math
#claude ai
class CrossEntropy(Distance):
	def __init__(self, epsilon: float = 1e-15):
		super().__init__()
		self.type='vec_nn'

		self.epsilon = epsilon  # Pour éviter le log(0)
		
	def compute(self, y_true, y_pred):
		return self.__call__(y_true, y_pred)
		
	def __call__(self, y_true: list[list[float]], y_pred: list[list[float]]) -> float:
		"""
		Calcule la cross-entropie entre les étiquettes vraies et les prédictions.

		:param y_true: Étiquettes vraies (one-hot encoded)
		:param y_pred: Probabilités prédites
		:return: Valeur de la cross-entropie
		"""
		total_ce = 0.0
		for true_row, pred_row in zip(y_true, y_pred):
			for true_val, pred_val in zip(true_row, pred_row):
				# Clip les valeurs prédites pour éviter log(0)
				pred_val = max(min(pred_val, 1 - self.epsilon), self.epsilon)
				total_ce -= true_val * log(pred_val)
        
		return total_ce / len(y_true)

	def gradient(self, y_true: list[list[float]], y_pred: list[list[float]]) -> list[list[float]]:
		"""
		Calcule le gradient de la cross-entropie.

		:param y_true: Étiquettes vraies (one-hot encoded)
		:param y_pred: Probabilités prédites
		:return: Gradient de la cross-entropie
		"""
		grad = []
		for true_row, pred_row in zip(y_true, y_pred):
			grad_row = []
			for true_val, pred_val in zip(true_row, pred_row):
				# Clip les valeurs prédites pour éviter division par zéro
				pred_val = max(min(pred_val, 1 - self.epsilon), self.epsilon)
				grad_row.append(-true_val / pred_val / len(y_true))
			grad.append(grad_row)
        
		return grad

	def example(self):
		# Exemple d'utilisation
		y_true = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
		y_pred = [[0.7, 0.2, 0.1], [0.1, 0.8, 0.1], [0.2, 0.2, 0.6]]

		loss = self.compute(y_true, y_pred)
		grad = self.gradient(y_true, y_pred)

		print(f"Cross-Entropie: {loss}")
		print(f"Gradient: ")
		for row in grad:
			print(row)

		return loss, grad
#claude ai 
class Softmax(Distance):

    def __init__(self) -> None:
        super().__init__()
        self.type='vec_nn'
        
    def compute(self, x):
      return self.__call__(x)

    def __call__(self, x: list[float]) -> list[float]:
        """
        Calcule la fonction softmax pour un vecteur d'entrée.

        :param x: Liste de valeurs d'entrée
        :return: Liste de probabilités softmax
        """
        # Soustrayons le maximum pour la stabilité numérique
        exp_x = [exp(xi - max(x)) for xi in x]
        sum_exp_x = sum(exp_x)
        return [xi / sum_exp_x for xi in exp_x]

    def gradient(self, softmax_output: list[float]) -> list[list[float]]:
        """
        Calcule le gradient de la fonction softmax.

        :param softmax_output: Sortie de la fonction softmax
        :return: Matrice jacobienne du gradient
        """
        n = len(softmax_output)
        gradient = []
        for i in range(n):
            row = []
            for j in range(n):
                if i == j:
                    row.append(softmax_output[i] * (1 - softmax_output[i]))
                else:
                    row.append(-softmax_output[i] * softmax_output[j])
            gradient.append(row)
        return gradient

    def example(self):
        # Exemple d'utilisation
        x = [1.0, 2.0, 3.0]
        
        softmax_output = self.compute(x)
        print("Sortie Softmax:")
        print(softmax_output)
        
        gradient = self.gradient(softmax_output)
        print("\nGradient Softmax:")
        for row in gradient:
            print(row)

        return softmax_output, gradient

class KullbackLeibler(Distance):

	def __init__(self) -> None:
		super().__init__()
		self.type='vec_nn'
 
	def compute(self, y_true, y_pred):
		return self.__call__(y_true, y_pred)
		
	def __call__(self, p, q):
		"""
		Calculate the Kullback-Leibler divergence between two probability distributions.
        
		:param p: The true probability distribution (list of probabilities).
		:param q: The predicted probability distribution (list of probabilities).
		:return: The KL divergence value.
		"""
		kl_divergence = 0.0
        
		for pi, qi in zip(p, q):
			if pi > 0 and qi > 0:  # To avoid log(0), we only calculate for positive values.
				kl_divergence += pi * log(pi / qi)
        
		return kl_divergence


class MeanAbsoluteError(Distance):

	def __init__(self) -> None:
		super().__init__()  
		self.type='vec_nn'

	def compute(self, y_true, y_pred):
		return self.__call__(y_true, y_pred)
		
	def __call__(self, y_true, y_pred):
		"""
		Calculate the Mean Absolute Error between two lists of values.
        
		:param y_true: List of true values.
		:param y_pred: List of predicted values.
		:return: The MAE value.
		"""
		if len(y_true) != len(y_pred):
			raise ValueError("The length of y_true and y_pred must be the same.")
        
		total_error = 0.0
		n = len(y_true)
        
		for i in range(n):
			total_error += abs(y_true[i] - y_pred[i])
        
		mae = total_error / n
		return mae

class MAE(MeanAbsoluteError):
	def __init__(self) -> None:
		super().__init__()


class MeanAbsolutePercentageError(Distance):

	def __init__(self) -> None:
		super().__init__()
		self.type='vec_float'

	def compute(self, y_true, y_pred):
		return self.__call__(y_true, y_pred)
		
	def __call__(self, y_true, y_pred):
		"""
		Calculate the Mean Absolute Percentage Error (MAPE) between two lists of values.
        
		:param y_true: List of true values.
		:param y_pred: List of predicted values.
		:return: The MAPE value as a percentage.
		"""
		if len(y_true) != len(y_pred):
			raise ValueError("The length of y_true and y_pred must be the same.")
        
		total_percentage_error = 0.0
		n = len(y_true)
        
		for i in range(n):
			if y_true[i] != 0:
				percentage_error = abs((y_true[i] - y_pred[i]) / y_true[i])
				total_percentage_error += percentage_error
			else:
				raise ValueError("y_true contains a zero value, which would cause a division by zero error in MAPE calculation.")
        
		mape = (total_percentage_error / n) * 100
		return mape

class MAPE(MeanAbsolutePercentageError):
	def __init__(self) -> None:
		super().__init__()
		
class MeanSquaredError(Distance):

	def __init__(self) -> None:
		super().__init__()
		self.type='vec_nn'

	def compute(self, y_true, y_pred):
		return self.__call__(y_true, y_pred)
		
	def __call__(self, y_true, y_pred):
		"""
		Calculate the Mean Squared Error (MSE) between two lists of values.
        
		:param y_true: List of true values.
		:param y_pred: List of predicted values.
		:return: The MSE value.
		"""
		if len(y_true) != len(y_pred):
			raise ValueError("The length of y_true and y_pred must be the same.")
        
		total_squared_error = 0.0
		n = len(y_true)
        
		for i in range(n):
			squared_error = (y_true[i] - y_pred[i]) ** 2
			total_squared_error += squared_error
        
		mse = total_squared_error / n
		return mse

class MSE(MeanSquaredError):
	def __init__(self) -> None:
		super().__init__()
		

class SquaredLogarithmicError(Distance):

	def __init__(self) -> None:
		super().__init__()
		self.type='vec_float'

	def compute(self, y_true, y_pred):
		return self.__call__(y_true, y_pred)
		
	def __call__(self, y_true, y_pred):
		"""
		Calculate the Squared Logarithmic Error (SLE) between two lists of values.
        
		:param y_true: List of true values. Must be positive.
		:param y_pred: List of predicted values. Must be positive.
		:return: The SLE value.
		"""
		if len(y_true) != len(y_pred):
			raise ValueError("The length of y_true and y_pred must be the same.")
        
		if any(v <= 0 for v in y_true) or any(v <= 0 for v in y_pred):
			raise ValueError("All values in y_true and y_pred must be positive for SLE calculation.")
        
		total_squared_log_error = 0.0
		n = len(y_true)
        
		for i in range(n):
			# Apply log transformation
			log_y_true = log(y_true[i] + 1)
			log_y_pred = log(y_pred[i] + 1)
			# Compute squared log error
			squared_log_error = (log_y_true - log_y_pred) ** 2
			total_squared_log_error += squared_log_error
        
		sle = total_squared_log_error / n
		return sle

class SLE(SquaredLogarithmicError):
	def __init__(self) -> None:
		super().__init__()


class GaloisWassersteinLoss(Distance):

    def __init__(self, alpha=1.0, beta=1.0, gamma=1.0) -> None:
        super().__init__()
        self.type='vec_nn'

        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.trellis = self.build_galois_trellis()

    def build_galois_trellis(self):
        """
        Construct a Galois trellis representing the hierarchical relationships between classes.
        
        :return: A dictionary representing the trellis where the keys are pairs of classes,
                 and the values are the distances between those classes.
        """
        # Example structure for the trellis
        # Replace this with a more complex or domain-specific trellis if necessary
        trellis = {
            (0, 0): 0, (0, 1): 1, (0, 2): 2,
            (1, 0): 1, (1, 1): 0, (1, 2): 1,
            (2, 0): 2, (2, 1): 1, (2, 2): 0
        }
        return trellis
    
    def compute_cdf(self, probabilities):
        """
        Compute the cumulative distribution function (CDF) from a list of probabilities.
        
        :param probabilities: List of probabilities for each class.
        :return: CDF as a list.
        """
        cdf = []
        cumulative_sum = 0.0
        for p in probabilities:
            cumulative_sum += p
            cdf.append(cumulative_sum)
        return cdf
    
    def compute(self, y_true, y_pred):
        """
        Compute the Galois distance between true and predicted distributions using the internal Galois trellis.
        
        :param y_true: List of true class probabilities.
        :param y_pred: List of predicted class probabilities.
        :return: The Galois distance value.
        """
        distance = 0.0
        for i in range(len(y_true)):
            for j in range(len(y_pred)):
                if y_true[i] > 0 and y_pred[j] > 0:
                    distance += self.trellis.get((i, j), 1) * abs(y_true[i] - y_pred[j])
        return distance
    
    def __call__(self, y_true, y_pred):
        """
        Calculate the Galois-Wasserstein Loss between the true and predicted distributions.
        
        :param y_true: List of true class probabilities.
        :param y_pred: List of predicted class probabilities.
        :return: The Galois-Wasserstein Loss value.
        """
        if len(y_true) != len(y_pred):
            raise ValueError("The length of y_true and y_pred must be the same.")
        
        # Compute CDF for true and predicted distributions
        cdf_true = self.compute_cdf(y_true)
        cdf_pred = self.compute_cdf(y_pred)
        
        # Compute Wasserstein distance
        wasserstein_distance = sum(abs(cdf_true[i] - cdf_pred[i]) for i in range(len(cdf_true)))
        
        # Compute Cross Entropy
        cross_entropy = CrossEntropy()(y_true, y_pred)
        
        # Compute Galois distance
        galois_distance = self.galois_distance(y_true, y_pred)
        
        # Compute combined loss
        loss = self.alpha * wasserstein_distance + self.beta * cross_entropy + self.gamma * galois_distance
        return loss
from typing import List, Union
from math import sqrt

class HuberLossDistance(Distance):
    """
    Huber Loss Distance: A robust loss function combining MSE and MAE.
    
    Attributes:
        delta (float): Threshold for switching between quadratic and linear loss.
    """
    def __init__(self, delta: float = 1.0):
        """
        Initialize Huber Loss Distance.
        
        Args:
            delta (float): Threshold for loss transition. Defaults to 1.0.
        """

        super().__init__()
        self.type='vec_nn'
        
        self.delta = delta

    def calculate(self, 
                  y_true: List[Union[int, float]], 
                  y_pred: List[Union[int, float]]) -> float:
        """
        Calculate Huber Loss Distance between two probability sequences.
        
        Args:
            y_true (List): True probability distribution
            y_pred (List): Predicted probability distribution
        
        Returns:
            float: Huber Loss Distance
        
        Raises:
            ValueError: If input lists have different lengths
        """
        if len(y_true) != len(y_pred):
            raise ValueError("Input sequences must have equal length")
        
        distances = []
        for true, pred in zip(y_true, y_pred):
            error = abs(true - pred)
            
            # Quadratic loss for small errors
            if error <= self.delta:
                distances.append(0.5 * error**2)
            
            # Linear loss for large errors
            else:
                distances.append(self.delta * (error - 0.5 * self.delta))
        
        # Root mean squared error
        return sqrt(sum(distances) / len(distances))

    def gradient(self, 
                 y_true: List[Union[int, float]], 
                 y_pred: List[Union[int, float]]) -> List[float]:
        """
        Calculate gradient of Huber Loss.
        
        Args:
            y_true (List): True probability distribution
            y_pred (List): Predicted probability distribution
        
        Returns:
            List[float]: Gradient of loss with respect to predictions
        """
        gradients = []
        for true, pred in zip(y_true, y_pred):
            error = true - pred
            
            # Clip gradient for large errors
            if abs(error) <= self.delta:
                gradients.append(error)
            else:
                gradients.append(self.delta * (1 if error > 0 else -1))
        
        return gradients


    
from typing import List, Union
from math import log, cosh, sqrt

class LogCoshLossDistance(Distance):
    """
    Log-Cosh Loss Distance: Smooth approximation of Mean Absolute Error.
    
    Attributes:
        scale (float): Scaling factor for loss sensitivity.
    """
    def __init__(self, scale: float = 1.0):
        """
        Initialize Log-Cosh Loss Distance.
        
        Args:
            scale (float): Scaling factor for loss sensitivity. Defaults to 1.0.
        """
        super().__init__()
        self.type='vec_nn'
        
        self.scale = scale

    def calculate(self, 
                  y_true: List[Union[int, float]], 
                  y_pred: List[Union[int, float]]) -> float:
        """
        Calculate Log-Cosh Loss Distance between probability sequences.
        
        Args:
            y_true (List): True probability distribution
            y_pred (List): Predicted probability distribution
        
        Returns:
            float: Log-Cosh Loss Distance
        
        Raises:
            ValueError: If input lists have different lengths
        """
        if len(y_true) != len(y_pred):
            raise ValueError("Input sequences must have equal length")
        
        distances = []
        for true, pred in zip(y_true, y_pred):
            error = true - pred
            # Log-cosh approximation of absolute error
            distances.append(log(cosh(self.scale * error)))
        
        return sqrt(sum(distances) / len(distances))

    def gradient(self, 
                 y_true: List[Union[int, float]], 
                 y_pred: List[Union[int, float]]) -> List[float]:
        """
        Calculate gradient of Log-Cosh Loss.
        
        Args:
            y_true (List): True probability distribution
            y_pred (List): Predicted probability distribution
        
        Returns:
            List[float]: Gradient of loss with respect to predictions
        """
        gradients = []
        for true, pred in zip(y_true, y_pred):
            error = true - pred
            # Derivative of log(cosh(x)) is tanh(x)
            gradients.append(self.scale * (error / cosh(self.scale * error)))
        
        return gradients

    
from typing import List, Union
from math import sqrt

class HingeLossDistance(Distance):
    """
    Hinge Loss Distance: SVM-inspired classification loss metric.
    
    Attributes:
        margin (float): Margin parameter for loss calculation.
    """
    def __init__(self, margin: float = 1.0):
        """
        Initialize Hinge Loss Distance.
        
        Args:
            margin (float): Margin for loss calculation. Defaults to 1.0.
        """
        super().__init__()
        self.type='vec_nn'
        
        self.margin = margin

    def calculate(self, 
                  y_true: List[Union[int, float]], 
                  y_pred: List[Union[int, float]]) -> float:
        """
        Calculate Hinge Loss Distance between probability sequences.
        
        Args:
            y_true (List): True classification labels (-1 or 1)
            y_pred (List): Predicted classification scores
        
        Returns:
            float: Hinge Loss Distance
        
        Raises:
            ValueError: If input lists have different lengths
        """
        if len(y_true) != len(y_pred):
            raise ValueError("Input sequences must have equal length")
        
        distances = []
        for true, pred in zip(y_true, y_pred):
            # Hinge loss: max(0, 1 - y * f(x))
            loss = max(0, self.margin - true * pred)
            distances.append(loss)
        
        return sqrt(sum(distances) / len(distances))

    def gradient(self, 
                 y_true: List[Union[int, float]], 
                 y_pred: List[Union[int, float]]) -> List[float]:
        """
        Calculate gradient of Hinge Loss.
        
        Args:
            y_true (List): True classification labels
            y_pred (List): Predicted classification scores
        
        Returns:
            List[float]: Gradient of loss with respect to predictions
        """
        gradients = []
        for true, pred in zip(y_true, y_pred):
            # Gradient: -y if margin condition violated, else 0
            if true * pred < self.margin:
                gradients.append(-true)
            else:
                gradients.append(0)
        
        return gradients

    
from typing import List, Union
from math import log, sqrt

class KLDivergenceDistance(Distance):
    """
    Kullback-Leibler Divergence: Probabilistic distance measure.
    
    Attributes:
        epsilon (float): Small value to prevent log(0).
    """
    def __init__(self, epsilon: float = 1e-10):
        """
        Initialize KL Divergence Distance.
        
        Args:
            epsilon (float): Smoothing parameter to avoid log(0).
        """
        super().__init__()
        self.type='vec_nn'
        
        self.epsilon = epsilon

    def calculate(self, 
                  p: List[Union[int, float]], 
                  q: List[Union[int, float]]) -> float:
        """
        Calculate KL Divergence between probability distributions.
        
        Args:
            p (List): Reference probability distribution
            q (List): Target probability distribution
        
        Returns:
            float: KL Divergence Distance
        
        Raises:
            ValueError: If distributions have different lengths
        """
        if len(p) != len(q):
            raise ValueError("Distributions must have equal length")
        
        divergences = []
        for p_i, q_i in zip(p, q):
            # Add epsilon to prevent log(0)
            safe_p = max(p_i, self.epsilon)
            safe_q = max(q_i, self.epsilon)
            
            # KL Divergence calculation
            divergence = safe_p * log(safe_p / safe_q)
            divergences.append(divergence)
        
        return sqrt(sum(divergences))

    def gradient(self, 
                 p: List[Union[int, float]], 
                 q: List[Union[int, float]]) -> List[float]:
        """
        Calculate gradient of KL Divergence.
        
        Args:
            p (List): Reference probability distribution
            q (List): Target probability distribution
        
        Returns:
            List[float]: Gradient of divergence
        """
        gradients = []
        for p_i, q_i in zip(p, q):
            # Add epsilon to prevent log(0)
            safe_p = max(p_i, self.epsilon)
            safe_q = max(q_i, self.epsilon)
            
            # Gradient of KL Divergence
            grad = log(safe_p / safe_q) + 1
            gradients.append(grad)
        
        return gradients

    
from typing import List, Union
from math import log, sqrt

class FocalLossDistance(Distance):
    """
    Focal Loss Distance: Emphasizes hard-to-classify examples.
    
    Attributes:
        gamma (float): Focusing parameter
        alpha (float): Balancing parameter
    """
    def __init__(self, gamma: float = 2.0, alpha: float = 0.25):
        """
        Initialize Focal Loss Distance.
        
        Args:
            gamma (float): Focusing parameter
            alpha (float): Class balancing parameter
        """
        super().__init__()
        self.type='vec_nn'
        
        self.gamma = gamma
        self.alpha = alpha

    def calculate(self, 
                  y_true: List[Union[int, float]], 
                  y_pred: List[Union[int, float]]) -> float:
        """
        Calculate Focal Loss Distance.
        
        Args:
            y_true (List): True binary labels
            y_pred (List): Predicted probabilities
        
        Returns:
            float: Focal Loss Distance
        """
        if len(y_true) != len(y_pred):
            raise ValueError("Input sequences must have equal length")
        
        distances = []
        for true, pred in zip(y_true, y_pred):
            # Clip predictions to prevent log(0)
            pred = max(min(pred, 1 - 1e-7), 1e-7)
            
            # Focal Loss computation
            focal_weight = (1 - pred) ** self.gamma
            alpha_weight = self.alpha if true > 0 else (1 - self.alpha)
            
            loss = -alpha_weight * focal_weight * (true * log(pred) + (1 - true) * log(1 - pred))
            distances.append(loss)
        
        return sqrt(sum(distances) / len(distances))

    def gradient(self, 
                 y_true: List[Union[int, float]], 
                 y_pred: List[Union[int, float]]) -> List[float]:
        """
        Calculate gradient of Focal Loss.
        
        Args:
            y_true (List): True binary labels
            y_pred (List): Predicted probabilities
        
        Returns:
            List[float]: Gradient of loss
        """
        gradients = []
        for true, pred in zip(y_true, y_pred):
            # Clip predictions
            pred = max(min(pred, 1 - 1e-7), 1e-7)
            
            # Gradient computation
            alpha_weight = self.alpha if true > 0 else (1 - self.alpha)
            gradient_term = (1 - pred) ** self.gamma * (
                true / pred - (1 - true) / (1 - pred)
            )
            
            gradients.append(alpha_weight * gradient_term)
        
        return gradients


    
from typing import List, Union
from math import log, sqrt

class SparseCategoricalCrossEntropyLossDistance(Distance):
    """
    Sparse Categorical Cross-Entropy Loss for integer-labeled classes.
    
    Attributes:
        epsilon (float): Small value to prevent log(0).
    """
    def __init__(self, epsilon: float = 1e-10):
        """
        Initialize Sparse Categorical Cross-Entropy Loss.
        
        Args:
            epsilon (float): Smoothing parameter to avoid log(0).
        """
        super().__init__()
        self.type='vec_nn'
        
        self.epsilon = epsilon

    def calculate(self, 
                  y_true: List[int], 
                  y_pred: List[List[float]]) -> float:
        """
        Calculate Sparse Categorical Cross-Entropy Loss.
        
        Args:
            y_true (List): True integer class labels
            y_pred (List): Predicted class probabilities
        
        Returns:
            float: Loss distance
        
        Raises:
            ValueError: If inputs are incompatible
        """
        if len(y_true) != len(y_pred):
            raise ValueError("Input sequences must have equal length")
        
        losses = []
        for true_label, pred_probs in zip(y_true, y_pred):
            # Ensure true label is within probability distribution
            if true_label < 0 or true_label >= len(pred_probs):
                raise ValueError(f"Invalid label {true_label}")
            
            # Get probability of true class
            true_prob = max(pred_probs[true_label], self.epsilon)
            
            # Compute loss
            loss = -log(true_prob)
            losses.append(loss)
        
        return sqrt(sum(losses) / len(losses))

    def gradient(self, 
                 y_true: List[int], 
                 y_pred: List[List[float]]) -> List[List[float]]:
        """
        Calculate gradient of Sparse Categorical Cross-Entropy Loss.
        
        Args:
            y_true (List): True integer class labels
            y_pred (List): Predicted class probabilities
        
        Returns:
            List[List[float]]: Gradient for each prediction
        """
        gradients = []
        for true_label, pred_probs in zip(y_true, y_pred):
            # Create gradient vector
            grad = [0.0] * len(pred_probs)
            grad[true_label] = -1 / max(pred_probs[true_label], self.epsilon)
            gradients.append(grad)
        
        return gradients


    
from typing import List, Union
from math import log, sqrt

class NegativeLogLikelihoodLossDistance(Distance):
    """
    Negative Log-Likelihood Loss for probabilistic models.
    
    Attributes:
        epsilon (float): Small value to prevent log(0).
    """
    def __init__(self, epsilon: float = 1e-10):
        """
        Initialize NLL Loss Distance.
        
        Args:
            epsilon (float): Smoothing parameter
        """
        super().__init__()
        self.type='vec_nn'
        
        self.epsilon = epsilon

    def calculate(self, 
                  y_true: List[Union[int, float]], 
                  y_pred: List[Union[int, float]]) -> float:
        """
        Calculate Negative Log-Likelihood Loss Distance.
        
        Args:
            y_true (List): True observed data
            y_pred (List): Predicted probabilities
        
        Returns:
            float: NLL Loss Distance
        """
        if len(y_true) != len(y_pred):
            raise ValueError("Input sequences must have equal length")
        
        losses = []
        for true, pred in zip(y_true, y_pred):
            # Clip prediction to prevent log(0)
            safe_pred = max(min(pred, 1 - self.epsilon), self.epsilon)
            
            # NLL loss: -log(likelihood)
            loss = -log(safe_pred)
            losses.append(loss)
        
        return sqrt(sum(losses) / len(losses))

    def gradient(self, 
                 y_true: List[Union[int, float]], 
                 y_pred: List[Union[int, float]]) -> List[float]:
        """
        Calculate NLL Loss Gradient.
        
        Args:
            y_true (List): True observed data
            y_pred (List): Predicted probabilities
        
        Returns:
            List[float]: Gradient of loss
        """
        gradients = []
        for true, pred in zip(y_true, y_pred):
            # Clip prediction to prevent division by zero
            safe_pred = max(min(pred, 1 - self.epsilon), self.epsilon)
            
            # Gradient: -1/prob
            grad = -1 / safe_pred
            gradients.append(grad)
        
        return gradients
    
    
from typing import List, Union
import math

class PoissonLossDistance(Distance):
    """
    Calculates Poisson Loss distance between probability distributions.
    
    Poisson Loss is suitable for count-based predictions, measuring 
    the divergence between predicted and actual probability distributions.
    """
    def __init__(self, epsilon: float = 1e-10):
        """
        """
        super().__init__()
        self.type='vec_nn'
            
    def calculate_loss(self, y_true: List[float], y_pred: List[float]) -> float:
        """
        Compute Poisson Loss between true and predicted probability distributions.
        
        Args:
            y_true (List[float]): Actual probability distribution
            y_pred (List[float]): Predicted probability distribution
        
        Returns:
            float: Poisson Loss distance
        
        Raises:
            ValueError: If input lists have different lengths or contain invalid probabilities
        """
        # Validate input distributions
        if len(y_true) != len(y_pred):
            raise ValueError("Input distributions must have equal length")
        
        # Validate probability values
        if not self._validate_probabilities(y_true) or not self._validate_probabilities(y_pred):
            raise ValueError("Probabilities must be non-negative")
        
        # Compute Poisson Loss
        loss = 0.0
        for true, pred in zip(y_true, y_pred):
            # Poisson Loss formula: y_pred - y_true * log(y_pred)
            loss += pred - true * math.log(pred) if pred > 0 else 0
        
        return loss
    
    def _validate_probabilities(self, distribution: List[float]) -> bool:
        """
        Validate that all values in distribution are non-negative.
        
        Args:
            distribution (List[float]): Probability distribution to validate
        
        Returns:
            bool: True if all values are valid, False otherwise
        """
        return all(val >= 0 for val in distribution)



from typing import List, Union
import math

class ContrastiveLossDistance(Distance):
    """
    Implements Contrastive Loss for similarity-based learning.
    
    Minimizes distances between similar samples while maximizing 
    distances between dissimilar samples.
    """
    
    def __init__(self, margin: float = 1.0):
        """
        Initialize Contrastive Loss with margin parameter.
        
        Args:
            margin (float): Margin for separating similar and dissimilar samples
        """

        super().__init__()
        self.type='vec_nn'
        
        self.margin = margin
    
    def calculate_loss(
        self, 
        embeddings1: List[float], 
        embeddings2: List[float], 
        is_similar: bool
    ) -> float:
        """
        Compute Contrastive Loss between two sample embeddings.
        
        Args:
            embeddings1 (List[float]): First sample's embedding
            embeddings2 (List[float]): Second sample's embedding
            is_similar (bool): Flag indicating if samples are similar
        
        Returns:
            float: Contrastive Loss value
        
        Raises:
            ValueError: If embeddings have different dimensions
        """
        # Validate embedding dimensions
        if len(embeddings1) != len(embeddings2):
            raise ValueError("Embeddings must have equal dimensions")
        
        # Calculate Euclidean distance between embeddings
        distance = math.sqrt(
            sum((a - b) ** 2 for a, b in zip(embeddings1, embeddings2))
        )
        
        # Contrastive Loss computation
        if is_similar:
            # For similar samples: minimize distance
            loss = distance ** 2
        else:
            # For dissimilar samples: maximize distance
            loss = max(0, self.margin - distance) ** 2
        
        return loss
    
    def batch_loss(
        self, 
        batch_embeddings1: List[List[float]], 
        batch_embeddings2: List[List[float]], 
        similarities: List[bool]
    ) -> float:
        """
        Compute average Contrastive Loss for a batch of samples.
        
        Args:
            batch_embeddings1 (List[List[float]]): First batch of embeddings
            batch_embeddings2 (List[List[float]]): Second batch of embeddings
            similarities (List[bool]): Similarity flags for each pair
        
        Returns:
            float: Average Contrastive Loss
        """
        if not (len(batch_embeddings1) == len(batch_embeddings2) == len(similarities)):
            raise ValueError("Batch sizes must match")
        
        total_loss = sum(
            self.calculate_loss(emb1, emb2, is_sim) 
            for emb1, emb2, is_sim in zip(batch_embeddings1, batch_embeddings2, similarities)
        )
        
        return total_loss / len(batch_embeddings1)
        


from typing import List, Union
import math

class TripletLossDistance(Distance):
    """
    Implements Triplet Loss for learning embeddings with correct sample ranking.
    
    Encourages closer distance between anchor and positive samples,
    while pushing negative samples further apart.
    """
    
    def __init__(self, margin: float = 0.2):
        """
        Initialize Triplet Loss with margin parameter.
        
        Args:
            margin (float): Margin for separating positive and negative samples
        """

        super().__init__()
        self.type='vec_nn'
        
        self.margin = margin
    
    def calculate_loss(
        self, 
        anchor: List[float], 
        positive: List[float], 
        negative: List[float]
    ) -> float:
        """
        Compute Triplet Loss between anchor, positive, and negative samples.
        
        Args:
            anchor (List[float]): Anchor sample embedding
            positive (List[float]): Positive sample embedding
            negative (List[float]): Negative sample embedding
        
        Returns:
            float: Triplet Loss value
        
        Raises:
            ValueError: If embeddings have different dimensions
        """
        # Validate embedding dimensions
        if not (len(anchor) == len(positive) == len(negative)):
            raise ValueError("Embeddings must have equal dimensions")
        
        # Calculate Euclidean distances
        pos_distance = math.sqrt(
            sum((a - p) ** 2 for a, p in zip(anchor, positive))
        )
        neg_distance = math.sqrt(
            sum((a - n) ** 2 for a, n in zip(anchor, negative))
        )
        
        # Triplet Loss computation
        loss = max(0, pos_distance - neg_distance + self.margin)
        
        return loss
    
    def batch_loss(
        self, 
        batch_anchors: List[List[float]], 
        batch_positives: List[List[float]], 
        batch_negatives: List[List[float]]
    ) -> float:
        """
        Compute average Triplet Loss for a batch of samples.
        
        Args:
            batch_anchors (List[List[float]]): Batch of anchor embeddings
            batch_positives (List[List[float]]): Batch of positive embeddings
            batch_negatives (List[List[float]]): Batch of negative embeddings
        
        Returns:
            float: Average Triplet Loss
        """
        if not (len(batch_anchors) == len(batch_positives) == len(batch_negatives)):
            raise ValueError("Batch sizes must match")
        
        total_loss = sum(
            self.calculate_loss(anchor, positive, negative) 
            for anchor, positive, negative in zip(
                batch_anchors, batch_positives, batch_negatives
            )
        )
        
        return total_loss / len(batch_anchors)



from typing import List, Union
import math

class CosineEmbeddingLossDistance(Distance):
    """
    Implements Cosine Embedding Loss for optimizing embedding similarities.
    
    Calculates loss based on cosine similarity between embeddings.
    """
    
    def __init__(self, margin: float = 0.0):
        """
        Initialize Cosine Embedding Loss with margin parameter.
        
        Args:
            margin (float): Margin for similarity threshold
        """

        super().__init__()
        self.type='vec_nn'
        
        self.margin = margin
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors.
        
        Args:
            vec1 (List[float]): First embedding vector
            vec2 (List[float]): Second embedding vector
        
        Returns:
            float: Cosine similarity value
        """
        # Compute dot product
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        
        # Compute magnitudes
        magnitude1 = math.sqrt(sum(a * a for a in vec1))
        magnitude2 = math.sqrt(sum(b * b for b in vec2))
        
        # Prevent division by zero
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def calculate_loss(
        self, 
        embedding1: List[float], 
        embedding2: List[float], 
        is_similar: bool
    ) -> float:
        """
        Compute Cosine Embedding Loss between two embeddings.
        
        Args:
            embedding1 (List[float]): First embedding vector
            embedding2 (List[float]): Second embedding vector
            is_similar (bool): Flag indicating if embeddings are similar
        
        Returns:
            float: Cosine Embedding Loss value
        
        Raises:
            ValueError: If embeddings have different dimensions
        """
        # Validate embedding dimensions
        if len(embedding1) != len(embedding2):
            raise ValueError("Embeddings must have equal dimensions")
        
        # Calculate cosine similarity
        cosine_sim = self._cosine_similarity(embedding1, embedding2)
        
        # Loss computation based on similarity
        if is_similar:
            # For similar embeddings: minimize distance
            loss = 1 - cosine_sim
        else:
            # For dissimilar embeddings: maximize distance
            loss = max(0, cosine_sim - self.margin)
        
        return loss
    
    def batch_loss(
        self, 
        batch_embeddings1: List[List[float]], 
        batch_embeddings2: List[List[float]], 
        similarities: List[bool]
    ) -> float:
        """
        Compute average Cosine Embedding Loss for a batch of samples.
        
        Args:
            batch_embeddings1 (List[List[float]]): First batch of embeddings
            batch_embeddings2 (List[List[float]]): Second batch of embeddings
            similarities (List[bool]): Similarity flags for each pair
        
        Returns:
            float: Average Cosine Embedding Loss
        """
        if not (len(batch_embeddings1) == len(batch_embeddings2) == len(similarities)):
            raise ValueError("Batch sizes must match")
        
        total_loss = sum(
            self.calculate_loss(emb1, emb2, is_sim) 
            for emb1, emb2, is_sim in zip(batch_embeddings1, batch_embeddings2, similarities)
        )
        
        return total_loss / len(batch_embeddings1)
        


from typing import List, Union
import math

class WassersteinLossDistance(Distance):
    """
    Implements Wasserstein Loss for stable neural network training.
    
    Calculates Earth Mover's Distance between probability distributions.
    """
    def __init__(self, epsilon: float = 1e-10):
        """
        
        """
        super().__init__()
        self.type='vec_nn'
            
    def calculate_loss(
        self, 
        distribution1: List[float], 
        distribution2: List[float]
    ) -> float:
        """
        Compute Wasserstein Loss between two probability distributions.
        
        Args:
            distribution1 (List[float]): First probability distribution
            distribution2 (List[float]): Second probability distribution
        
        Returns:
            float: Wasserstein Loss value
        
        Raises:
            ValueError: If distributions have different lengths or are invalid
        """
        # Validate distributions
        if len(distribution1) != len(distribution2):
            raise ValueError("Distributions must have equal length")
        
        if not self._validate_distributions(distribution1, distribution2):
            raise ValueError("Invalid probability distributions")
        
        # Compute cumulative distributions
        cumsum1 = self._cumulative_distribution(distribution1)
        cumsum2 = self._cumulative_distribution(distribution2)
        
        # Calculate Wasserstein distance (Earth Mover's Distance)
        wasserstein_distance = sum(
            abs(cum1 - cum2) for cum1, cum2 in zip(cumsum1, cumsum2)
        )
        
        return wasserstein_distance
    
    def _validate_distributions(
        self, 
        dist1: List[float], 
        dist2: List[float]
    ) -> bool:
        """
        Validate probability distributions.
        
        Args:
            dist1 (List[float]): First distribution
            dist2 (List[float]): Second distribution
        
        Returns:
            bool: True if distributions are valid, False otherwise
        """
        # Check non-negativity and sum to 1
        def is_valid_dist(dist: List[float]) -> bool:
            return (
                all(val >= 0 for val in dist) and 
                math.isclose(sum(dist), 1.0, rel_tol=1e-5)
            )
        
        return is_valid_dist(dist1) and is_valid_dist(dist2)
    
    def _cumulative_distribution(self, distribution: List[float]) -> List[float]:
        """
        Compute cumulative distribution.
        
        Args:
            distribution (List[float]): Input probability distribution
        
        Returns:
            List[float]: Cumulative distribution
        """
        cumsum = []
        current_sum = 0
        for prob in distribution:
            current_sum += prob
            cumsum.append(current_sum)
        return cumsum


from typing import List, Union
import math

class ReconstructionLossDistance(Distance):
    """
    Implements Reconstruction Loss for autoencoder training.
    
    Measures the difference between original and reconstructed data.
    """
    def __init__(self, epsilon: float = 1e-10):
        """
        
        """
        super().__init__()
        self.type='vec_nn'
            
    def calculate_loss(
        self, 
        original_data: List[float], 
        reconstructed_data: List[float], 
        loss_type: str = 'mse'
    ) -> float:
        """
        Compute Reconstruction Loss between original and reconstructed data.
        
        Args:
            original_data (List[float]): Original input data
            reconstructed_data (List[float]): Reconstructed data from autoencoder
            loss_type (str): Type of loss calculation ('mse', 'mae')
        
        Returns:
            float: Reconstruction Loss value
        
        Raises:
            ValueError: If data lists have different lengths or invalid loss type
        """
        # Validate input data
        if len(original_data) != len(reconstructed_data):
            raise ValueError("Original and reconstructed data must have equal length")
        
        # Compute loss based on selected type
        if loss_type == 'mse':
            # Mean Squared Error
            loss = sum((orig - recon) ** 2 for orig, recon in zip(original_data, reconstructed_data)) / len(original_data)
        elif loss_type == 'mae':
            # Mean Absolute Error
            loss = sum(abs(orig - recon) for orig, recon in zip(original_data, reconstructed_data)) / len(original_data)
        else:
            raise ValueError("Invalid loss type. Choose 'mse' or 'mae'")
        
        return loss
    
    def batch_reconstruction_loss(
        self, 
        batch_original: List[List[float]], 
        batch_reconstructed: List[List[float]], 
        loss_type: str = 'mse'
    ) -> float:
        """
        Compute average Reconstruction Loss for a batch of data.
        
        Args:
            batch_original (List[List[float]]): Batch of original input data
            batch_reconstructed (List[List[float]]): Batch of reconstructed data
            loss_type (str): Type of loss calculation
        
        Returns:
            float: Average Reconstruction Loss
        """
        if not (len(batch_original) == len(batch_reconstructed)):
            raise ValueError("Batch sizes must match")
        
        total_loss = sum(
            self.calculate_loss(orig, recon, loss_type) 
            for orig, recon in zip(batch_original, batch_reconstructed)
        )
        
        return total_loss / len(batch_original)


from typing import List, Tuple
import math

class VariationalLossDistance(Distance):
    """
    Implements Variational Loss for Variational Autoencoder (VAE) training.
    
    Combines reconstruction loss with KL divergence regularization.
    """
    def __init__(self, epsilon: float = 1e-10):
        """
        
        """
        super().__init__()
        self.type='vec_nn'
            
    def calculate_loss(
        self, 
        original_data: List[float], 
        reconstructed_data: List[float],
        mean: List[float],
        log_variance: List[float]
    ) -> Tuple[float, float, float]:
        """
        Compute Variational Loss components.
        
        Args:
            original_data (List[float]): Original input data
            reconstructed_data (List[float]): Reconstructed data
            mean (List[float]): Latent space mean
            log_variance (List[float]): Latent space log variance
        
        Returns:
            Tuple of (total_loss, reconstruction_loss, kl_divergence)
        """
        # Validate input dimensions
        if not (len(original_data) == len(reconstructed_data) == 
                len(mean) == len(log_variance)):
            raise ValueError("Input dimensions must match")
        
        # Reconstruction Loss (Mean Squared Error)
        reconstruction_loss = sum(
            (orig - recon) ** 2 
            for orig, recon in zip(original_data, reconstructed_data)
        ) / len(original_data)
        
        # KL Divergence computation
        kl_divergence = sum(
            -0.5 * (1 + log_var - (mean ** 2) - math.exp(log_var))
            for mean, log_var in zip(mean, log_variance)
        ) / len(mean)
        
        # Total Variational Loss (combine reconstruction and KL divergence)
        total_loss = reconstruction_loss + kl_divergence
        
        return total_loss, reconstruction_loss, kl_divergence
    
    def batch_variational_loss(
        self, 
        batch_original: List[List[float]], 
        batch_reconstructed: List[List[float]],
        batch_mean: List[List[float]],
        batch_log_variance: List[List[float]]
    ) -> Tuple[float, float, float]:
        """
        Compute average Variational Loss for a batch of data.
        
        Args:
            batch_original (List[List[float]]): Batch of original inputs
            batch_reconstructed (List[List[float]]): Batch of reconstructed data
            batch_mean (List[List[float]]): Batch of latent space means
            batch_log_variance (List[List[float]]): Batch of latent space log variances
        
        Returns:
            Tuple of average (total_loss, reconstruction_loss, kl_divergence)
        """
        if not (len(batch_original) == len(batch_reconstructed) == 
                len(batch_mean) == len(batch_log_variance)):
            raise ValueError("Batch sizes must match")
        
        # Compute losses for each sample
        batch_losses = [
            self.calculate_loss(orig, recon, mean, log_var)
            for orig, recon, mean, log_var in zip(
                batch_original, batch_reconstructed, batch_mean, batch_log_variance
            )
        ]
        
        # Average the losses
        total_loss = sum(loss[0] for loss in batch_losses) / len(batch_losses)
        recon_loss = sum(loss[1] for loss in batch_losses) / len(batch_losses)
        kl_divergence = sum(loss[2] for loss in batch_losses) / len(batch_losses)
        
        return total_loss, recon_loss, kl_divergence
        


from typing import List, Dict, Callable, Union
import math

class CustomWeightedLossDistance(Distance):
    """
    Implements custom weighted loss combining multiple loss components.
    
    Allows flexible loss computation for specialized neural network training.
    """
    
    def __init__(self):
        """
        Initialize custom weighted loss calculator.
        """

        super().__init__()
        self.type='vec_nn'
        
        # Default loss functions
        self._loss_functions = {
            'mse': self._mean_squared_error,
            'mae': self._mean_absolute_error,
            'cross_entropy': self._cross_entropy,
        }
    
    def _mean_squared_error(
        self, 
        true_values: List[float], 
        pred_values: List[float]
    ) -> float:
        """
        Calculate Mean Squared Error loss.
        
        Args:
            true_values (List[float]): Ground truth values
            pred_values (List[float]): Predicted values
        
        Returns:
            float: Mean Squared Error
        """
        return sum((t - p) ** 2 for t, p in zip(true_values, pred_values)) / len(true_values)
    
    def _mean_absolute_error(
        self, 
        true_values: List[float], 
        pred_values: List[float]
    ) -> float:
        """
        Calculate Mean Absolute Error loss.
        
        Args:
            true_values (List[float]): Ground truth values
            pred_values (List[float]): Predicted values
        
        Returns:
            float: Mean Absolute Error
        """
        return sum(abs(t - p) for t, p in zip(true_values, pred_values)) / len(true_values)
    
    def _cross_entropy(
        self, 
        true_values: List[float], 
        pred_values: List[float]
    ) -> float:
        """
        Calculate Cross Entropy loss.
        
        Args:
            true_values (List[float]): Ground truth probabilities
            pred_values (List[float]): Predicted probabilities
        
        Returns:
            float: Cross Entropy Loss
        """
        epsilon = 1e-15  # Prevent log(0)
        return -sum(
            t * math.log(max(p, epsilon)) + (1 - t) * math.log(max(1 - p, epsilon))
            for t, p in zip(true_values, pred_values)
        ) / len(true_values)
    
    def add_custom_loss(
        self, 
        name: str, 
        loss_function: Callable[[List[float], List[float]], float]
    ) -> None:
        """
        Add a custom loss function to the available losses.
        
        Args:
            name (str): Name of the loss function
            loss_function (Callable): Custom loss calculation function
        """
        self._loss_functions[name] = loss_function
    
    def compute_weighted_loss(
        self, 
        true_values: List[float], 
        pred_values: List[float], 
        loss_weights: Dict[str, float]
    ) -> float:
        """
        Compute weighted combination of loss functions.
        
        Args:
            true_values (List[float]): Ground truth values
            pred_values (List[float]): Predicted values
            loss_weights (Dict[str, float]): Weights for different loss components
        
        Returns:
            float: Weighted combined loss
        """
        # Validate input dimensions
        if len(true_values) != len(pred_values):
            raise ValueError("True and predicted values must have same length")
        
        # Compute weighted losses
        total_loss = 0.0
        for loss_name, weight in loss_weights.items():
            if loss_name not in self._loss_functions:
                raise ValueError(f"Unknown loss function: {loss_name}")
            
            loss_func = self._loss_functions[loss_name]
            total_loss += weight * loss_func(true_values, pred_values)
        
        return total_loss
        


from typing import List, Tuple, Callable
import math

class TemporalLossDistance(Distance):
    """
    Implements loss calculations for time-series data, 
    accounting for temporal dependencies.
    """
    def __init__(self, epsilon: float = 1e-10):
        """
        
        """
        super().__init__()
        self.type='vec_nn'
           
    def sequence_mse_loss(
        self, 
        true_sequence: List[List[float]], 
        pred_sequence: List[List[float]]
    ) -> float:
        """
        Calculate Mean Squared Error for time-series sequences.
        
        Args:
            true_sequence (List[List[float]]): Ground truth time-series
            pred_sequence (List[List[float]]): Predicted time-series
        
        Returns:
            float: Temporal Mean Squared Error
        """
        if len(true_sequence) != len(pred_sequence):
            raise ValueError("Sequence lengths must match")
        
        squared_errors = [
            sum((true - pred) ** 2 for true, pred in zip(true_step, pred_step)) 
            for true_step, pred_step in zip(true_sequence, pred_sequence)
        ]
        
        return sum(squared_errors) / len(true_sequence)
    
    def temporal_weighted_loss(
        self, 
        true_sequence: List[List[float]], 
        pred_sequence: List[List[float]],
        decay_factor: float = 0.9
    ) -> float:
        """
        Calculate temporal loss with exponential decay.
        
        Args:
            true_sequence (List[List[float]]): Ground truth time-series
            pred_sequence (List[List[float]]): Predicted time-series
            decay_factor (float): Decay rate for temporal importance
        
        Returns:
            float: Weighted temporal loss
        """
        if len(true_sequence) != len(pred_sequence):
            raise ValueError("Sequence lengths must match")
        
        weighted_losses = []
        for t, (true_step, pred_step) in enumerate(zip(true_sequence, pred_sequence)):
            # Compute step loss
            step_loss = sum((true - pred) ** 2 for true, pred in zip(true_step, pred_step))
            
            # Apply temporal decay
            weighted_loss = step_loss * (decay_factor ** t)
            weighted_losses.append(weighted_loss)
        
        return sum(weighted_losses) / len(true_sequence)
    
    def custom_temporal_loss(
        self, 
        true_sequence: List[List[float]], 
        pred_sequence: List[List[float]],
        loss_func: Callable[[List[float], List[float]], float]
    ) -> float:
        """
        Apply custom loss function to time-series sequences.
        
        Args:
            true_sequence (List[List[float]]): Ground truth time-series
            pred_sequence (List[List[float]]): Predicted time-series
            loss_func (Callable): Custom loss calculation function
        
        Returns:
            float: Temporal custom loss
        """
        if len(true_sequence) != len(pred_sequence):
            raise ValueError("Sequence lengths must match")
        
        sequence_losses = [
            loss_func(true_step, pred_step) 
            for true_step, pred_step in zip(true_sequence, pred_sequence)
        ]
        
        return sum(sequence_losses) / len(true_sequence)
        


from .mainClass import Distance

from typing import Tuple, List, Optional
import cv2
from dataclasses import dataclass
###########################################
''' a recoder
class FID:
class InceptionScore:

'''

@dataclass
class MatchResult:
    """
    Contains the results of image matching using SIFT.
    
    Attributes:
        distance (float): Computed distance between the two images
        num_matches (int): Number of good matches found
        match_ratio (float): Ratio of good matches to total keypoints
    """
    distance: float
    num_matches: int
    match_ratio: float

class SIFTImageDistance(Distance):
    """
    A class that computes the distance between two images using the SIFT algorithm.
    This implementation uses OpenCV's SIFT implementation and provides a measure
    of similarity between images that is invariant to scale, rotation, and translation.
    """
    
    def __init__(self, match_threshold: float = 0.7):
        """
        Initialize the SIFT image distance calculator.
        
        Args:
            match_threshold (float): Threshold for Lowe's ratio test (default: 0.7).
                Lower values create stricter matching criteria.
        """
        super().__init__()
        self.type='image'
        
        self.sift = cv2.SIFT_create()
        self.match_threshold = match_threshold
        
    def _extract_features(self, image: cv2.Mat) -> Tuple[List[cv2.KeyPoint], cv2.Mat]:
        """
        Extract SIFT keypoints and descriptors from an image.
        
        Args:
            image (cv2.Mat): Input image in grayscale format
            
        Returns:
            Tuple containing:
                - List of keypoints
                - Matrix of descriptors
        """
        keypoints, descriptors = self.sift.detectAndCompute(image, None)
        return keypoints, descriptors
    
    def _match_features(
        self,
        desc1: cv2.Mat,
        desc2: cv2.Mat
    ) -> List[List[cv2.DMatch]]:
        """
        Match descriptors between two images using k-nearest neighbors.
        
        Args:
            desc1 (cv2.Mat): Descriptors from first image
            desc2 (cv2.Mat): Descriptors from second image
            
        Returns:
            List of k-nearest neighbor matches for each keypoint
        """
        matcher = cv2.BFMatcher()
        return matcher.knnMatch(desc1, desc2, k=2)
    
    def _filter_matches(
        self,
        matches: List[List[cv2.DMatch]]
    ) -> List[cv2.DMatch]:
        """
        Filter matches using Lowe's ratio test to keep only good matches.
        
        Args:
            matches (List[List[cv2.DMatch]]): List of k-nearest neighbor matches
            
        Returns:
            List of good matches that pass the ratio test
        """
        good_matches = []
        for m, n in matches:
            if m.distance < self.match_threshold * n.distance:
                good_matches.append(m)
        return good_matches
    
    def compute(
        self,
        image1: cv2.Mat,
        image2: cv2.Mat
    ) -> Optional[MatchResult]:
        """
        Compute the SIFT-based distance between two images.
        
        Args:
            image1 (cv2.Mat): First input image (grayscale)
            image2 (cv2.Mat): Second input image (grayscale)
            
        Returns:
            MatchResult object containing distance metrics, or None if matching fails
            
        Raises:
            ValueError: If images are None or empty
        """
        # Input validation
        if image1 is None or image2 is None:
            raise ValueError("Input images cannot be None")
        if image1.size == 0 or image2.size == 0:
            raise ValueError("Input images cannot be empty")
            
        # Extract features from both images
        kp1, desc1 = self._extract_features(image1)
        kp2, desc2 = self._extract_features(image2)
        
        # Check if features were found in both images
        if desc1 is None or desc2 is None or len(kp1) == 0 or len(kp2) == 0:
            return None
            
        # Match features
        matches = self._match_features(desc1, desc2)
        good_matches = self._filter_matches(matches)
        
        # Compute distance metrics
        if len(good_matches) == 0:
            return None
            
        # Calculate average distance of good matches
        avg_distance = sum(m.distance for m in good_matches) / len(good_matches)
        
        # Calculate match ratio
        total_keypoints = min(len(kp1), len(kp2))
        match_ratio = len(good_matches) / total_keypoints
        
        return MatchResult(
            distance=avg_distance,
            num_matches=len(good_matches),
            match_ratio=match_ratio
        )
#################################################
from typing import Tuple, List, Optional
import cv2
from dataclasses import dataclass

@dataclass
class SURFMatchResult:
    """
    Contains the results of image matching using SURF.
    
    Attributes:
        distance (float): Computed distance between the two images
        num_matches (int): Number of good matches found
        match_ratio (float): Ratio of good matches to total keypoints
        avg_strength (float): Average strength of the matched features
    """
    distance: float
    num_matches: int
    match_ratio: float
    avg_strength: float

class SURFImageDistance(Distance):
    """
    A class that computes the distance between two images using the SURF algorithm.
    SURF (Speeded Up Robust Features) provides faster computation compared to SIFT
    while maintaining robustness to image transformations.
    
    Note: As of OpenCV 3.0, SURF is patented and moved to the contrib package.
    Make sure you have opencv-contrib-python installed.
    """
    
    def __init__(
        self,
        hessian_threshold: float = 400,
        match_threshold: float = 0.7,
        extended: bool = False
    ):
        """
        Initialize the SURF image distance calculator.
        
        Args:
            hessian_threshold (float): Threshold for the keypoint detector (default: 400).
                Higher values result in fewer keypoints.
            match_threshold (float): Threshold for ratio test (default: 0.7).
                Lower values create stricter matching criteria.
            extended (bool): Whether to use extended 128-element descriptors (default: False).
        """
        super().__init__()
        self.type='image'
        
        self.surf = cv2.xfeatures2d.SURF_create(
            hessianThreshold=hessian_threshold,
            extended=extended
        )
        self.match_threshold = match_threshold
        
    def _extract_features(self, image: cv2.Mat) -> Tuple[List[cv2.KeyPoint], cv2.Mat]:
        """
        Extract SURF keypoints and descriptors from an image.
        
        Args:
            image (cv2.Mat): Input image in grayscale format
            
        Returns:
            Tuple containing:
                - List of keypoints
                - Matrix of descriptors
        """
        keypoints, descriptors = self.surf.detectAndCompute(image, None)
        return keypoints, descriptors
    
    def _match_features(
        self,
        desc1: cv2.Mat,
        desc2: cv2.Mat
    ) -> List[List[cv2.DMatch]]:
        """
        Match descriptors between two images using FLANN-based matcher.
        FLANN (Fast Library for Approximate Nearest Neighbors) is optimized
        for fast matching of large datasets.
        
        Args:
            desc1 (cv2.Mat): Descriptors from first image
            desc2 (cv2.Mat): Descriptors from second image
            
        Returns:
            List of k-nearest neighbor matches for each keypoint
        """
        # FLANN parameters
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)
        
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        return flann.knnMatch(desc1, desc2, k=2)
    
    def _filter_matches(
        self,
        matches: List[List[cv2.DMatch]],
        kp1: List[cv2.KeyPoint],
        kp2: List[cv2.KeyPoint]
    ) -> Tuple[List[cv2.DMatch], float]:
        """
        Filter matches using ratio test and compute average feature strength.
        
        Args:
            matches (List[List[cv2.DMatch]]): List of k-nearest neighbor matches
            kp1 (List[cv2.KeyPoint]): Keypoints from first image
            kp2 (List[cv2.KeyPoint]): Keypoints from second image
            
        Returns:
            Tuple containing:
                - List of good matches that pass the ratio test
                - Average strength of matched features
        """
        good_matches = []
        total_strength = 0.0
        
        for m, n in matches:
            if m.distance < self.match_threshold * n.distance:
                good_matches.append(m)
                # Use response as feature strength
                strength1 = kp1[m.queryIdx].response
                strength2 = kp2[m.trainIdx].response
                total_strength += (strength1 + strength2) / 2
                
        avg_strength = total_strength / len(good_matches) if good_matches else 0
        return good_matches, avg_strength
    
    def compute(
        self,
        image1: cv2.Mat,
        image2: cv2.Mat
    ) -> Optional[SURFMatchResult]:
        """
        Compute the SURF-based distance between two images.
        
        Args:
            image1 (cv2.Mat): First input image (grayscale)
            image2 (cv2.Mat): Second input image (grayscale)
            
        Returns:
            SURFMatchResult object containing distance metrics, or None if matching fails
            
        Raises:
            ValueError: If images are None or empty
            RuntimeError: If SURF is not available in OpenCV installation
        """
        # Input validation
        if image1 is None or image2 is None:
            raise ValueError("Input images cannot be None")
        if image1.size == 0 or image2.size == 0:
            raise ValueError("Input images cannot be empty")
            
        try:
            # Extract features from both images
            kp1, desc1 = self._extract_features(image1)
            kp2, desc2 = self._extract_features(image2)
            
            # Check if features were found in both images
            if desc1 is None or desc2 is None or len(kp1) == 0 or len(kp2) == 0:
                return None
                
            # Match features
            matches = self._match_features(desc1, desc2)
            good_matches, avg_strength = self._filter_matches(matches, kp1, kp2)
            
            # Compute distance metrics
            if len(good_matches) == 0:
                return None
                
            # Calculate average distance of good matches
            avg_distance = sum(m.distance for m in good_matches) / len(good_matches)
            
            # Calculate match ratio
            total_keypoints = min(len(kp1), len(kp2))
            match_ratio = len(good_matches) / total_keypoints
            
            return SURFMatchResult(
                distance=avg_distance,
                num_matches=len(good_matches),
                match_ratio=match_ratio,
                avg_strength=avg_strength
            )
            
        except cv2.error as e:
            raise RuntimeError("SURF is not available. Make sure opencv-contrib-python is installed.") from e
##########################################
from typing import Tuple, List, Optional
import cv2
from dataclasses import dataclass

@dataclass
class ORBMatchResult:
    """
    Contains the results of image matching using ORB.
    
    Attributes:
        distance (float): Computed Hamming distance between the two images
        num_matches (int): Number of good matches found
        match_ratio (float): Ratio of good matches to total keypoints
        avg_response (float): Average response strength of matched keypoints
    """
    distance: float
    num_matches: int
    match_ratio: float
    avg_response: float

class ORBImageDistance(Distance):
    """
    A class that computes the distance between two images using the ORB algorithm.
    ORB (Oriented FAST and Rotated BRIEF) is a fast and efficient alternative to
    SIFT and SURF, particularly suitable for real-time applications.
    """
    
    def __init__(
        self,
        n_features: int = 500,
        scale_factor: float = 1.2,
        n_levels: int = 8,
        match_threshold: float = 0.75,
        fast_threshold: int = 20
    ):
        """
        Initialize the ORB image distance calculator.
        
        Args:
            n_features (int): Maximum number of features to detect (default: 500)
            scale_factor (float): Pyramid decimation ratio (default: 1.2)
            n_levels (int): Number of pyramid levels (default: 8)
            match_threshold (float): Threshold for ratio test (default: 0.75)
            fast_threshold (int): FAST detector threshold (default: 20)
        """
        super().__init__()
        self.type='image'
        
        self.orb = cv2.ORB_create(
            nfeatures=n_features,
            scaleFactor=scale_factor,
            nlevels=n_levels,
            fastThreshold=fast_threshold
        )
        self.match_threshold = match_threshold
        
    def _extract_features(self, image: cv2.Mat) -> Tuple[List[cv2.KeyPoint], cv2.Mat]:
        """
        Extract ORB keypoints and descriptors from an image.
        
        Args:
            image (cv2.Mat): Input image in grayscale format
            
        Returns:
            Tuple containing:
                - List of keypoints
                - Matrix of descriptors (binary)
        """
        keypoints, descriptors = self.orb.detectAndCompute(image, None)
        return keypoints, descriptors
    
    def _match_features(
        self,
        desc1: cv2.Mat,
        desc2: cv2.Mat
    ) -> List[List[cv2.DMatch]]:
        """
        Match binary descriptors between two images using Hamming distance.
        Uses Brute Force matcher with Hamming distance, which is optimal for
        binary descriptors like those produced by ORB.
        
        Args:
            desc1 (cv2.Mat): Descriptors from first image
            desc2 (cv2.Mat): Descriptors from second image
            
        Returns:
            List of k-nearest neighbor matches for each keypoint
        """
        # Create Brute Force Matcher with Hamming distance
        matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
        return matcher.knnMatch(desc1, desc2, k=2)
    
    def _filter_matches(
        self,
        matches: List[List[cv2.DMatch]],
        kp1: List[cv2.KeyPoint],
        kp2: List[cv2.KeyPoint]
    ) -> Tuple[List[cv2.DMatch], float]:
        """
        Filter matches using ratio test and compute average response strength.
        
        Args:
            matches (List[List[cv2.DMatch]]): List of k-nearest neighbor matches
            kp1 (List[cv2.KeyPoint]): Keypoints from first image
            kp2 (List[cv2.KeyPoint]): Keypoints from second image
            
        Returns:
            Tuple containing:
                - List of good matches that pass the ratio test
                - Average response strength of matched keypoints
        """
        good_matches = []
        total_response = 0.0
        
        for match_pair in matches:
            if len(match_pair) < 2:
                continue
                
            m, n = match_pair
            if m.distance < self.match_threshold * n.distance:
                good_matches.append(m)
                # Calculate average response of the matched keypoints
                response1 = kp1[m.queryIdx].response
                response2 = kp2[m.trainIdx].response
                total_response += (response1 + response2) / 2
                
        avg_response = total_response / len(good_matches) if good_matches else 0
        return good_matches, avg_response
    
    def compute(
        self,
        image1: cv2.Mat,
        image2: cv2.Mat
    ) -> Optional[ORBMatchResult]:
        """
        Compute the ORB-based distance between two images.
        
        Args:
            image1 (cv2.Mat): First input image (grayscale)
            image2 (cv2.Mat): Second input image (grayscale)
            
        Returns:
            ORBMatchResult object containing distance metrics, or None if matching fails
            
        Raises:
            ValueError: If images are None or empty
        """
        # Input validation
        if image1 is None or image2 is None:
            raise ValueError("Input images cannot be None")
        if image1.size == 0 or image2.size == 0:
            raise ValueError("Input images cannot be empty")
            
        try:
            # Extract features from both images
            kp1, desc1 = self._extract_features(image1)
            kp2, desc2 = self._extract_features(image2)
            
            # Check if features were found in both images
            if desc1 is None or desc2 is None or len(kp1) == 0 or len(kp2) == 0:
                return None
                
            # Match features
            matches = self._match_features(desc1, desc2)
            good_matches, avg_response = self._filter_matches(matches, kp1, kp2)
            
            # Compute distance metrics
            if len(good_matches) == 0:
                return None
                
            # Calculate average Hamming distance of good matches
            avg_distance = sum(m.distance for m in good_matches) / len(good_matches)
            
            # Calculate match ratio
            total_keypoints = min(len(kp1), len(kp2))
            match_ratio = len(good_matches) / total_keypoints
            
            return ORBMatchResult(
                distance=avg_distance,
                num_matches=len(good_matches),
                match_ratio=match_ratio,
                avg_response=avg_response
            )
            
        except Exception as e:
            raise RuntimeError(f"Error during ORB matching: {str(e)}")
#########################################
from typing import List, Tuple, Set
import cv2
from dataclasses import dataclass
from math import sqrt

@dataclass
class ChamferResult:
    """
    Contains the results of Chamfer distance calculation.
    
    Attributes:
        distance (float): The computed Chamfer distance
        forward_distance (float): Average distance from points in first image to second
        backward_distance (float): Average distance from points in second image to first
        num_points_img1 (int): Number of edge points in first image
        num_points_img2 (int): Number of edge points in second image
    """
    distance: float
    forward_distance: float
    backward_distance: float
    num_points_img1: int
    num_points_img2: int

class ChamferDistance(Distance):
    """
    A class that computes the Chamfer distance between two binary images.
    The Chamfer distance measures the average nearest neighbor distance
    between edge points in two images.
    """
    
    def __init__(
        self,
        edge_threshold: int = 100,
        edge_kernel_size: int = 3,
        bidirectional: bool = True
    ):
        """
        Initialize the Chamfer distance calculator.
        
        Args:
            edge_threshold (int): Threshold for Canny edge detection (default: 100)
            edge_kernel_size (int): Kernel size for edge detection (default: 3)
            bidirectional (bool): Whether to compute bidirectional distance (default: True)
        """
        super().__init__()
        self.type='image'
        
        self.edge_threshold = edge_threshold
        self.edge_kernel_size = edge_kernel_size
        self.bidirectional = bidirectional
    
    def _extract_edge_points(self, image: cv2.Mat) -> Set[Tuple[int, int]]:
        """
        Extract edge points from an image using Canny edge detection.
        
        Args:
            image (cv2.Mat): Input grayscale image
            
        Returns:
            Set of (x, y) coordinates of edge points
        """
        # Apply Canny edge detection
        edges = cv2.Canny(
            image,
            self.edge_threshold,
            self.edge_threshold * 2,
            self.edge_kernel_size
        )
        
        # Convert to set of points
        points = set()
        y_coords, x_coords = edges.nonzero()
        for x, y in zip(x_coords, y_coords):
            points.add((x, y))
            
        return points
    
    def _find_nearest_distance(
        self,
        point: Tuple[int, int],
        target_points: Set[Tuple[int, int]]
    ) -> float:
        """
        Find the distance to the nearest point in the target set.
        
        Args:
            point (Tuple[int, int]): Source point coordinates
            target_points (Set[Tuple[int, int]]): Set of target points
            
        Returns:
            float: Distance to nearest point
        """
        if not target_points:
            return float('inf')
            
        x1, y1 = point
        min_distance = float('inf')
        
        for x2, y2 in target_points:
            # Compute Euclidean distance
            dist = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            min_distance = min(min_distance, dist)
            
            # Early exit if we found a very close point
            if min_distance < 1.0:
                break
                
        return min_distance
    
    def _compute_directional_distance(
        self,
        source_points: Set[Tuple[int, int]],
        target_points: Set[Tuple[int, int]]
    ) -> Tuple[float, int]:
        """
        Compute average nearest neighbor distance from source to target points.
        
        Args:
            source_points (Set[Tuple[int, int]]): Set of source points
            target_points (Set[Tuple[int, int]]): Set of target points
            
        Returns:
            Tuple containing:
                - Average distance from source to target points
                - Number of source points
        """
        if not source_points:
            return 0.0, 0
            
        total_distance = 0.0
        for point in source_points:
            nearest_dist = self._find_nearest_distance(point, target_points)
            total_distance += nearest_dist
            
        return total_distance / len(source_points), len(source_points)
    
    def compute(
        self,
        image1: cv2.Mat,
        image2: cv2.Mat
    ) -> ChamferResult:
        """
        Compute the Chamfer distance between two images.
        
        Args:
            image1 (cv2.Mat): First input image (grayscale)
            image2 (cv2.Mat): Second input image (grayscale)
            
        Returns:
            ChamferResult object containing distance metrics
            
        Raises:
            ValueError: If images are None, empty, or have different sizes
        """
        # Input validation
        if image1 is None or image2 is None:
            raise ValueError("Input images cannot be None")
        if image1.size == 0 or image2.size == 0:
            raise ValueError("Input images cannot be empty")
        if image1.shape != image2.shape:
            raise ValueError("Images must have the same dimensions")
            
        # Extract edge points from both images
        points1 = self._extract_edge_points(image1)
        points2 = self._extract_edge_points(image2)
        
        # Compute forward distance (image1 -> image2)
        forward_dist, num_points1 = self._compute_directional_distance(points1, points2)
        
        if self.bidirectional:
            # Compute backward distance (image2 -> image1)
            backward_dist, num_points2 = self._compute_directional_distance(points2, points1)
            
            # Compute symmetric Chamfer distance
            chamfer_distance = (forward_dist + backward_dist) / 2
        else:
            # Use only forward distance
            backward_dist = 0.0
            num_points2 = len(points2)
            chamfer_distance = forward_dist
            
        return ChamferResult(
            distance=chamfer_distance,
            forward_distance=forward_dist,
            backward_distance=backward_dist,
            num_points_img1=num_points1,
            num_points_img2=num_points2
        )
########################################
from typing import Tuple, List, Dict
import cv2
from dataclasses import dataclass
from math import log10, exp, sqrt
import statistics

@dataclass
class PerceptualResult:
    """
    Contains the results of perceptual distance calculation.
    
    Attributes:
        distance (float): Overall perceptual distance score (0-1, lower is more similar)
        contrast_score (float): Difference in local contrast
        structure_score (float): Difference in structural information
        brightness_score (float): Difference in brightness distribution
        details: Dict containing component-specific metrics
    """
    distance: float
    contrast_score: float
    structure_score: float
    brightness_score: float
    details: Dict[str, float]

class PerceptualDistance(Distance):
    """
    A class that computes content-based perceptual distance between two images.
    Implements multiple perceptual metrics including contrast, structure,
    and brightness differences.
    """
    
    def __init__(
        self,
        block_size: int = 8,
        contrast_weight: float = 0.4,
        structure_weight: float = 0.4,
        brightness_weight: float = 0.2
    ):
        """
        Initialize the perceptual distance calculator.
        
        Args:
            block_size (int): Size of blocks for local analysis (default: 8)
            contrast_weight (float): Weight for contrast component (default: 0.4)
            structure_weight (float): Weight for structure component (default: 0.4)
            brightness_weight (float): Weight for brightness component (default: 0.2)
        """
        super().__init__()
        self.type='image'
        
        self.block_size = block_size
        self.weights = {
            'contrast': contrast_weight,
            'structure': structure_weight,
            'brightness': brightness_weight
        }
        
    def _compute_local_statistics(
        self,
        image: cv2.Mat
    ) -> Tuple[cv2.Mat, cv2.Mat]:
        """
        Compute local mean and standard deviation for image blocks.
        
        Args:
            image (cv2.Mat): Input grayscale image
            
        Returns:
            Tuple containing:
                - Local mean values
                - Local standard deviation values
        """
        # Calculate local means
        mean = cv2.blur(
            image.astype(float),
            (self.block_size, self.block_size)
        )
        
        # Calculate local standard deviations
        squared = cv2.blur(
            image.astype(float) ** 2,
            (self.block_size, self.block_size)
        )
        variance = squared - mean ** 2
        std = cv2.sqrt(cv2.max(variance, 0))
        
        return mean, std
    
    def _compute_contrast_difference(
        self,
        std1: cv2.Mat,
        std2: cv2.Mat
    ) -> float:
        """
        Compute contrast difference between two images.
        
        Args:
            std1 (cv2.Mat): Standard deviation map of first image
            std2 (cv2.Mat): Standard deviation map of second image
            
        Returns:
            float: Contrast difference score (0-1)
        """
        # Normalize standard deviations
        max_std = max(std1.max(), std2.max())
        if max_std == 0:
            return 0.0
            
        std1_norm = std1 / max_std
        std2_norm = std2 / max_std
        
        # Compute contrast difference
        contrast_diff = cv2.absdiff(std1_norm, std2_norm)
        return float(contrast_diff.mean())
    
    def _compute_structure_difference(
        self,
        image1: cv2.Mat,
        image2: cv2.Mat
    ) -> float:
        """
        Compute structural difference between two images using gradient information.
        
        Args:
            image1 (cv2.Mat): First input image
            image2 (cv2.Mat): Second input image
            
        Returns:
            float: Structure difference score (0-1)
        """
        # Compute gradients
        grad_x1 = cv2.Sobel(image1, cv2.CV_64F, 1, 0, ksize=3)
        grad_y1 = cv2.Sobel(image1, cv2.CV_64F, 0, 1, ksize=3)
        grad_x2 = cv2.Sobel(image2, cv2.CV_64F, 1, 0, ksize=3)
        grad_y2 = cv2.Sobel(image2, cv2.CV_64F, 0, 1, ksize=3)
        
        # Compute gradient magnitudes
        mag1 = cv2.magnitude(grad_x1, grad_y1)
        mag2 = cv2.magnitude(grad_x2, grad_y2)
        
        # Normalize magnitudes
        max_mag = max(mag1.max(), mag2.max())
        if max_mag == 0:
            return 0.0
            
        mag1_norm = mag1 / max_mag
        mag2_norm = mag2 / max_mag
        
        # Compute structural difference
        struct_diff = cv2.absdiff(mag1_norm, mag2_norm)
        return float(struct_diff.mean())
    
    def _compute_brightness_difference(
        self,
        mean1: cv2.Mat,
        mean2: cv2.Mat
    ) -> float:
        """
        Compute brightness distribution difference between two images.
        
        Args:
            mean1 (cv2.Mat): Local mean values of first image
            mean2 (cv2.Mat): Local mean values of second image
            
        Returns:
            float: Brightness difference score (0-1)
        """
        # Normalize mean values
        max_mean = max(mean1.max(), mean2.max())
        if max_mean == 0:
            return 0.0
            
        mean1_norm = mean1 / max_mean
        mean2_norm = mean2 / max_mean
        
        # Compute brightness difference
        bright_diff = cv2.absdiff(mean1_norm, mean2_norm)
        return float(bright_diff.mean())
    
    def compute(
        self,
        image1: cv2.Mat,
        image2: cv2.Mat
    ) -> PerceptualResult:
        """
        Compute the perceptual distance between two images.
        
        Args:
            image1 (cv2.Mat): First input image (grayscale)
            image2 (cv2.Mat): Second input image (grayscale)
            
        Returns:
            PerceptualResult object containing distance metrics
            
        Raises:
            ValueError: If images are None, empty, or have different sizes
        """
        # Input validation
        if image1 is None or image2 is None:
            raise ValueError("Input images cannot be None")
        if image1.size == 0 or image2.size == 0:
            raise ValueError("Input images cannot be empty")
        if image1.shape != image2.shape:
            raise ValueError("Images must have the same dimensions")
            
        # Compute local statistics
        mean1, std1 = self._compute_local_statistics(image1)
        mean2, std2 = self._compute_local_statistics(image2)
        
        # Compute component differences
        contrast_score = self._compute_contrast_difference(std1, std2)
        structure_score = self._compute_structure_difference(image1, image2)
        brightness_score = self._compute_brightness_difference(mean1, mean2)
        
        # Compute weighted total distance
        total_distance = (
            self.weights['contrast'] * contrast_score +
            self.weights['structure'] * structure_score +
            self.weights['brightness'] * brightness_score
        )
        
        # Collect detailed metrics
        details = {
            'local_contrast_variation': float(cv2.meanStdDev(std1 - std2)[0][0]),
            'brightness_distribution': float(cv2.compareHist(
                cv2.calcHist([image1], [0], None, [256], [0, 256]),
                cv2.calcHist([image2], [0], None, [256], [0, 256]),
                cv2.HISTCMP_BHATTACHARYYA
            ))
        }
        
        return PerceptualResult(
            distance=total_distance,
            contrast_score=contrast_score,
            structure_score=structure_score,
            brightness_score=brightness_score,
            details=details
        )
##################################
from typing import List, Tuple, Optional
from math import exp, sqrt
import statistics

class LPIPS(Distance):
    """
    A pure Python implementation of LPIPS (Learned Perceptual Image Patch Similarity).
    This is a simplified version that captures the core concepts without deep learning dependencies.
    
    The implementation uses a basic perceptual model based on:
    - Color differences
    - Local structure analysis
    - Basic feature extraction
    
    Note: For production use, consider using the official LPIPS implementation with proper
    neural networks and pre-trained weights.
    """
    
    def __init__(self, patch_size: int = 8):
        """
        Initialize the LPIPS calculator.
        
        Args:
            patch_size (int): Size of patches to compare (default: 8)
        """
        super().__init__()
        self.type='image'
        
        self.patch_size = patch_size
        self._weights = self._initialize_weights()
    
    def _initialize_weights(self) -> List[float]:
        """
        Initialize basic weights for feature importance.
        In real LPIPS, these would come from a trained network.
        
        Returns:
            List[float]: Weight values for different features
        """
        return [0.25, 0.35, 0.40]  # Weights for color, structure, and features
    
    def _extract_patches(self, image: List[List[List[float]]]) -> List[List[List[List[float]]]]:
        """
        Extract patches from the image for comparison.
        
        Args:
            image: RGB image as 3D list [height][width][3]
            
        Returns:
            4D list of patches [n_patches_h][n_patches_w][patch_size][patch_size]
        """
        height = len(image)
        width = len(image[0])
        patches = []
        
        for i in range(0, height - self.patch_size + 1, self.patch_size):
            row_patches = []
            for j in range(0, width - self.patch_size + 1, self.patch_size):
                patch = []
                for pi in range(self.patch_size):
                    patch_row = []
                    for pj in range(self.patch_size):
                        patch_row.append(image[i + pi][j + pj])
                    patch.append(patch_row)
                row_patches.append(patch)
            patches.append(row_patches)
        
        return patches
        
    def stdev(self,n):
      mean =sum(n)/len(n)
      SUM= 0
      for i in n :
       SUM +=(i-mean)**2
      return sqrt(SUM/(len(n)-1))
      
    def _compute_patch_features(self, patch: List[List[List[float]]]) -> List[float]:
        """
        Compute basic features for a patch.
        
        Args:
            patch: 3D list representing an image patch
            
        Returns:
            List[float]: Feature vector for the patch
        """
        # Calculate color statistics
        r_values = [pixel[0] for row in patch for pixel in row]
        g_values = [pixel[1] for row in patch for pixel in row]
        b_values = [pixel[2] for row in patch for pixel in row]
        
        color_mean = [
            statistics.mean(r_values),
            statistics.mean(g_values),
            statistics.mean(b_values)
        ]
        color_std = [
            self.stdev(r_values),
            self.stdev(g_values),
            self.stdev(b_values)
        ]
        # Calculate structure features (simplified gradient)
        structure_feature = 0.0
        for i in range(len(patch) - 1):
            for j in range(len(patch[0]) - 1):
                dx = sum(abs(x - y) for x, y in zip(patch[i][j], patch[i][j+1]))
                dy = sum(abs(x - y) for x, y in zip(patch[i][j], patch[i+1][j]))
                structure_feature += sqrt(dx*dx + dy*dy)
        
        return color_mean + color_std + [structure_feature]
    
    def compute(self, image1: List[List[List[float]]], 
                         image2: List[List[List[float]]]) -> float:
        """
        Calculate the perceptual distance between two images.
        
        Args:
            image1: First image as 3D list [height][width][3]
            image2: Second image as 3D list [height][width][3]
            
        Returns:
            float: Perceptual distance between the images
        
        Raises:
            ValueError: If images have different dimensions
        """
        if len(image1) != len(image2) or len(image1[0]) != len(image2[0]):
            raise ValueError("Images must have the same dimensions")
        
        # Extract patches
        patches1 = self._extract_patches(image1)
        patches2 = self._extract_patches(image2)
        
        total_distance = 0.0
        patch_count = 0
        
        # Compare corresponding patches
        for i in range(len(patches1)):
            for j in range(len(patches1[0])):
                features1 = self._compute_patch_features(patches1[i][j])
                features2 = self._compute_patch_features(patches2[i][j])
                
                # Calculate weighted feature difference
                patch_distance = 0.0
                for f1, f2, w in zip(features1, features2, self._weights):
                    patch_distance += w * (f1 - f2) ** 2
                
                total_distance += sqrt(patch_distance)
                patch_count += 1
        
        # Normalize by number of patches
        return total_distance / patch_count

    def __str__(self) -> str:
        """
        String representation of the LPIPS calculator.
        
        Returns:
            str: Description of the calculator
        """
        return f"LPIPS Calculator (patch_size={self.patch_size})"

######################################
from typing import List, Tuple, Dict, Optional
from math import log, sqrt, exp, pi
import statistics
from collections import defaultdict

class BRISQUE(Distance):
    """
    A pure Python implementation of BRISQUE (Blind/Referenceless Image Spatial Quality Evaluator).
    This is a simplified version that captures the core concepts without external dependencies.
    
    BRISQUE works by:
    1. Computing local normalized luminance values
    2. Computing pairwise products of neighboring values
    3. Fitting these products to an Asymmetric Generalized Gaussian Distribution (AGGD)
    4. Using these statistics as features for quality assessment
    
    Note: For production use, consider using the official implementation with proper
    optimization and pre-trained SVR model.
    """
    
    def __init__(self, patch_size: int = 8):
        """
        Initialize the BRISQUE calculator.
        
        Args:
            patch_size (int): Size of patches for local analysis
        """
        super().__init__()
        self.type='image'
        
        self.patch_size = patch_size
        self.gaussian_window = self._create_gaussian_window()
        
    def _create_gaussian_window(self, sigma: float = 1.5) -> List[List[float]]:
        """
        Create a Gaussian window for local normalization.
        
        Args:
            sigma (float): Standard deviation of Gaussian distribution
            
        Returns:
            List[List[float]]: 2D Gaussian window
        """
        window = []
        center = self.patch_size // 2
        
        for i in range(self.patch_size):
            row = []
            for j in range(self.patch_size):
                x = i - center
                y = j - center
                g = exp(-(x*x + y*y)/(2*sigma*sigma))
                g /= 2 * pi * sigma * sigma
                row.append(g)
            window.append(row)
            
        # Normalize
        total = sum(sum(row) for row in window)
        return [[v/total for v in row] for row in window]
    
    def _to_luminance(self, image: List[List[List[float]]]) -> List[List[float]]:
        """
        Convert RGB image to luminance values.
        
        Args:
            image: RGB image as 3D list [height][width][3]
            
        Returns:
            List[List[float]]: Luminance values
        """
        height = len(image)
        width = len(image[0])
        luminance = [[0.0] * width for _ in range(height)]
        
        for i in range(height):
            for j in range(width):
                # Convert RGB to luminance using standard coefficients
                r, g, b = image[i][j]
                luminance[i][j] = 0.2989 * r + 0.5870 * g + 0.1140 * b
                
        return luminance
    
    def _extract_patches(self, 
                        image: List[List[float]]) -> List[List[List[float]]]:
        """
        Extract patches from the image.
        
        Args:
            image: 2D luminance image
            
        Returns:
            List[List[List[float]]]: List of image patches
        """
        height = len(image)
        width = len(image[0])
        patches = []
        
        for i in range(0, height - self.patch_size + 1, self.patch_size):
            for j in range(0, width - self.patch_size + 1, self.patch_size):
                patch = []
                for pi in range(self.patch_size):
                    row = []
                    for pj in range(self.patch_size):
                        row.append(image[i + pi][j + pj])
                    patch.append(row)
                patches.append(patch)
                
        return patches
    
    def _compute_mscn_coefficients(self, 
                                 patch: List[List[float]]) -> List[List[float]]:
        """
        Compute Mean Subtracted Contrast Normalized (MSCN) coefficients.
        
        Args:
            patch: Image patch
            
        Returns:
            List[List[float]]: MSCN coefficients
        """
        # Compute local mean
        local_mean = 0.0
        for i in range(self.patch_size):
            for j in range(self.patch_size):
                local_mean += patch[i][j] * self.gaussian_window[i][j]
                
        # Compute local variance
        local_var = 0.0
        for i in range(self.patch_size):
            for j in range(self.patch_size):
                diff = patch[i][j] - local_mean
                local_var += diff * diff * self.gaussian_window[i][j]
                
        local_std = sqrt(local_var) + 1e-7
        
        # Compute MSCN coefficients
        mscn = [[0.0] * self.patch_size for _ in range(self.patch_size)]
        for i in range(self.patch_size):
            for j in range(self.patch_size):
                mscn[i][j] = (patch[i][j] - local_mean) / local_std
                
        return mscn
    
    def _compute_aggd_features(self, 
                             coeffs: List[List[float]]) -> List[float]:
        """
        Compute Asymmetric Generalized Gaussian Distribution features.
        
        Args:
            coeffs: MSCN coefficients
            
        Returns:
            List[float]: AGGD parameters
        """
        # Separate positive and negative coefficients
        left_coeffs = []
        right_coeffs = []
        
        for row in coeffs:
            for val in row:
                if val < 0:
                    left_coeffs.append(-val)
                else:
                    right_coeffs.append(val)
                    
        # Compute statistics
        if left_coeffs:
            left_mean = statistics.mean(left_coeffs)
            left_var = statistics.variance(left_coeffs) if len(left_coeffs) > 1 else 0
        else:
            left_mean = left_var = 0
            
        if right_coeffs:
            right_mean = statistics.mean(right_coeffs)
            right_var = statistics.variance(right_coeffs) if len(right_coeffs) > 1 else 0
        else:
            right_mean = right_var = 0
            
        # Return AGGD parameters
        return [left_mean, left_var, right_mean, right_var]
    
    def compute(self, image: List[List[List[float]]]) -> float:
        """
        Calculate the BRISQUE quality score for an image.
        Lower scores indicate better perceptual quality.
        
        Args:
            image: RGB image as 3D list [height][width][3]
            
        Returns:
            float: BRISQUE quality score
            
        Raises:
            ValueError: If image dimensions are too small
        """
        height = len(image)
        width = len(image[0])
        
        if height < self.patch_size or width < self.patch_size:
            raise ValueError(f"Image dimensions must be at least {self.patch_size}x{self.patch_size}")
        
        # Convert to luminance
        luminance = self._to_luminance(image)
        
        # Extract patches
        patches = self._extract_patches(luminance)
        
        # Compute features for each patch
        all_features = []
        for patch in patches:
            # Compute MSCN coefficients
            mscn = self._compute_mscn_coefficients(patch)
            
            # Compute AGGD features
            features = self._compute_aggd_features(mscn)
            all_features.append(features)
            
        # Compute final score (simplified version)
        # In practice, these features would be input to a trained SVR model
        score = 0.0
        for features in all_features:
            # Simple weighted sum of features
            score += sum(f * w for f, w in zip(features, [0.2, 0.2, 0.3, 0.3]))
            
        return score / len(all_features)
    
    def __str__(self) -> str:
        """
        String representation of the BRISQUE calculator.
        
        Returns:
            str: Description of the calculator
        """
        return f"BRISQUE Calculator (patch_size={self.patch_size})"
##################################
from typing import List, Tuple, Dict, Optional
from math import exp, sqrt
import statistics
from collections import defaultdict

class VGG16Distance(Distance):
    """
    A pure Python implementation of VGG16-based image distance calculation.
    This is a simplified version that captures the core concepts of using
    VGG16-like features for image comparison without deep learning dependencies.
    
    The implementation includes:
    1. Simplified convolutional layers
    2. Max pooling operations
    3. Feature extraction at multiple levels
    4. Distance computation between feature representations
    
    Note: For production use, consider using the official VGG16 implementation
    with pre-trained weights through a deep learning framework.
    """
    
    def __init__(self):
        """
        Initialize the VGG16-based distance calculator with simplified filters.
        """
        super().__init__()
        self.type='image'
        
        self.layer_configs = [
            # (n_filters, filter_size, pool_size)
            (64, 3, 2),   # Block 1
            (128, 3, 2),  # Block 2
            (256, 3, 2),  # Block 3
            (512, 3, 2),  # Block 4
            (512, 3, 2)   # Block 5
        ]
        self.filters = self._initialize_filters()

    
    def _initialize_filters(self) -> Dict[int, List[List[List[List[float]]]]]:
        """
        Initialize simplified convolutional filters that approximate VGG16 behavior.
        
        Returns:
            Dict[int, List[List[List[List[float]]]]]: Simplified filters for each layer
        """
        filters = {}
        current_depth = 3  # Starting with RGB
        
        for block_idx, (n_filters, filter_size, _) in enumerate(self.layer_configs):
            block_filters = []
            
            for _ in range(n_filters):
                # Create simplified edge detection filters
                filter_weights = [[[[0.0] * current_depth
                                  for _ in range(filter_size)]
                                 for _ in range(filter_size)]
                                for _ in range(1)]
                
                # Initialize with basic patterns (horizontal, vertical, diagonal)
                for c in range(current_depth):
                    if block_idx == 0:  # First layer processes RGB
                        filter_weights[0][0][1][c] = 1.0
                        filter_weights[0][2][1][c] = -1.0
                    else:  # Deeper layers
                        filter_weights[0][1][1][c] = 1.0
                        filter_weights[0][1][2][c] = -1.0
                
                block_filters.append(filter_weights)
            
            filters[block_idx] = block_filters
            current_depth = n_filters
            
        return filters
    
    def _convolve(self,
                  input_data: List[List[List[float]]],
                  filter_weights: List[List[List[List[float]]]]) -> List[List[List[float]]]:
        """
        Apply convolution operation with given filter weights.
        
        Args:
            input_data: Input feature maps
            filter_weights: Convolutional filter weights
            
        Returns:
            List[List[List[float]]]: Output feature maps
        """
        height = len(input_data)
        width = len(input_data[0])
        depth = len(input_data[0][0])
        
        filter_size = len(filter_weights[0][0])
        n_filters = len(filter_weights)
        
        # Calculate output dimensions
        out_height = height - filter_size + 1
        out_width = width - filter_size + 1
        
        # Initialize output
        output = [[[0.0] * n_filters
                   for _ in range(out_width)]
                  for _ in range(out_height)]
        
        # Perform convolution
        for h in range(out_height):
            for w in range(out_width):
                for f in range(n_filters):
                    value = 0.0
                    for i in range(filter_size):
                        for j in range(filter_size):
                            for d in range(depth):
                                value += (input_data[h+i][w+j][d] *
                                        filter_weights[f][0][i][j][d])
                    output[h][w][f] = max(0.0, value)  # ReLU activation
                    
        return output
    
    def _max_pool(self,
                 input_data: List[List[List[float]]],
                 pool_size: int) -> List[List[List[float]]]:
        """
        Apply max pooling operation.
        
        Args:
            input_data: Input feature maps
            pool_size: Size of pooling window
            
        Returns:
            List[List[List[float]]]: Pooled feature maps
        """
        height = len(input_data)
        width = len(input_data[0])
        depth = len(input_data[0][0])
        
        # Calculate output dimensions
        out_height = height // pool_size
        out_width = width // pool_size
        
        # Initialize output
        output = [[[0.0] * depth
                   for _ in range(out_width)]
                  for _ in range(out_height)]
        
        # Perform max pooling
        for h in range(out_height):
            for w in range(out_width):
                for d in range(depth):
                    pool_max = float('-inf')
                    for i in range(pool_size):
                        for j in range(pool_size):
                            pool_max = max(pool_max,
                                         input_data[h*pool_size+i][w*pool_size+j][d])
                    output[h][w][d] = pool_max
                    
        return output
    
    def _extract_features(self,
                         image: List[List[List[float]]]) -> List[List[List[List[float]]]]:
        """
        Extract hierarchical features using simplified VGG16-like architecture.
        
        Args:
            image: Input image as 3D list [height][width][3]
            
        Returns:
            List[List[List[List[float]]]]: Features from different layers
        """
        features = []
        current_input = image
        
        # Process each block
        for block_idx, (n_filters, filter_size, pool_size) in enumerate(self.layer_configs):
            # Apply convolutions
            conv_output = self._convolve(current_input,
                                       self.filters[block_idx])
            
            # Apply max pooling
            pool_output = self._max_pool(conv_output, pool_size)
            
            features.append(pool_output)
            current_input = pool_output
            
        return features
    
    def compute(self,
                         image1: List[List[List[float]]],
                         image2: List[List[List[float]]]) -> float:
        """
        Calculate the VGG16-based distance between two images.
        
        Args:
            image1: First image as 3D list [height][width][3]
            image2: Second image as 3D list [height][width][3]
            
        Returns:
            float: Distance score (lower means more similar)
            
        Raises:
            ValueError: If images have different dimensions
        """
        if (len(image1) != len(image2) or
            len(image1[0]) != len(image2[0])):
            raise ValueError("Images must have the same dimensions")
        
        # Extract features
        features1 = self._extract_features(image1)
        features2 = self._extract_features(image2)
        
        # Calculate distance at each layer
        total_distance = 0.0
        layer_weights = [0.1, 0.1, 0.2, 0.3, 0.3]  # More weight to deeper layers
        
        for feat1, feat2, weight in zip(features1, features2, layer_weights):
            # Calculate Euclidean distance between feature maps
            layer_distance = 0.0
            for h in range(len(feat1)):
                for w in range(len(feat1[0])):
                    for d in range(len(feat1[0][0])):
                        diff = feat1[h][w][d] - feat2[h][w][d]
                        layer_distance += diff * diff
                        
            total_distance += weight * sqrt(layer_distance)
            
        return total_distance
    
    def __str__(self) -> str:
        """
        String representation of the VGG16-based distance calculator.
        
        Returns:
            str: Description of the calculator
        """
        return "VGG16-Based Image Distance Calculator"
#######################################
from typing import List, Tuple, Dict, Optional, Union
from math import exp, sqrt
import statistics
from collections import defaultdict

class ResNetDistance(Distance):
    """
    A pure Python implementation of ResNet-based image distance calculation.
    This is a simplified version that captures the core concepts of using
    ResNet-like features for image comparison without deep learning dependencies.
    
    The implementation includes:
    1. Residual blocks with skip connections
    2. Batch normalization simulation
    3. Feature extraction at multiple levels
    4. Distance computation between feature representations
    
    Note: For production use, consider using the official ResNet implementation
    with pre-trained weights through a deep learning framework.
    """
    
    def __init__(self, n_blocks: int = 4):
        """
        Initialize the ResNet-based distance calculator.
        
        Args:
            n_blocks (int): Number of residual blocks
        """
        super().__init__()
        self.type='image'
        
        self.n_blocks = n_blocks
        self.block_configs = [
            # (channels, reduction)
            (64, 1),    # Block 1
            (128, 2),   # Block 2
            (256, 2),   # Block 3
            (512, 2)    # Block 4
        ][:n_blocks]
        self.filters = self._initialize_filters()

    
    def _initialize_filters(self) -> Dict[str, List[List[List[List[float]]]]]:
        """
        Initialize simplified convolutional filters for ResNet blocks.
        
        Returns:
            Dict[str, List[List[List[List[float]]]]]: Filters for each layer
        """
        filters = {}
        current_channels = 3  # Starting with RGB
        
        for block_idx, (channels, _) in enumerate(self.block_configs):
            # Main path filters
            filters[f'block{block_idx}_conv1'] = self._create_basic_filters(
                current_channels, channels, 3)
            filters[f'block{block_idx}_conv2'] = self._create_basic_filters(
                channels, channels, 3)
            
            # Shortcut path filter (1x1 conv for dimension matching)
            if current_channels != channels:
                filters[f'block{block_idx}_shortcut'] = self._create_basic_filters(
                    current_channels, channels, 1)
                
            current_channels = channels
            
        return filters
    
    def _create_basic_filters(self,
                            in_channels: int,
                            out_channels: int,
                            kernel_size: int) -> List[List[List[List[float]]]]:
        """
        Create basic convolutional filters.
        
        Args:
            in_channels: Number of input channels
            out_channels: Number of output channels
            kernel_size: Size of the kernel
            
        Returns:
            List[List[List[List[float]]]]: Basic convolutional filters
        """
        filters = []
        for _ in range(out_channels):
            filter_weights = [[[[0.0] * in_channels
                              for _ in range(kernel_size)]
                             for _ in range(kernel_size)]
                            for _ in range(1)]
            
            # Initialize with simple edge detection patterns
            for c in range(in_channels):
                filter_weights[0][kernel_size//2][kernel_size//2][c] = 1.0
                if kernel_size > 1:
                    filter_weights[0][0][0][c] = -0.5
                    filter_weights[0][-1][-1][c] = -0.5
                    
            filters.append(filter_weights)
            
        return filters
    
    def _batch_norm(self,
                   features: List[List[List[float]]],
                   epsilon: float = 1e-5) -> List[List[List[float]]]:
        """
        Apply simplified batch normalization.
        
        Args:
            features: Input feature maps
            epsilon: Small constant for numerical stability
            
        Returns:
            List[List[List[float]]]: Normalized feature maps
        """
        height = len(features)
        width = len(features[0])
        channels = len(features[0][0])
        
        # Calculate mean and variance per channel
        channel_stats = []
        for c in range(channels):
            values = [features[h][w][c]
                     for h in range(height)
                     for w in range(width)]
            mean = statistics.mean(values)
            var = statistics.variance(values) if len(values) > 1 else 0
            channel_stats.append((mean, var))
        
        # Normalize
        normalized = [[[0.0] * channels
                      for _ in range(width)]
                     for _ in range(height)]
        
        for h in range(height):
            for w in range(width):
                for c in range(channels):
                    mean, var = channel_stats[c]
                    normalized[h][w][c] = ((features[h][w][c] - mean) /
                                         sqrt(var + epsilon))
                    
        return normalized
    
    def _apply_residual_block(self,
                            input_data: List[List[List[float]]],
                            block_idx: int,
                            reduction: int) -> List[List[List[float]]]:
        """
        Apply a residual block with skip connection.
        
        Args:
            input_data: Input feature maps
            block_idx: Index of the current block
            reduction: Spatial reduction factor
            
        Returns:
            List[List[List[float]]]: Output feature maps
        """
        # Main path
        conv1 = self._convolve(input_data,
                              self.filters[f'block{block_idx}_conv1'],
                              stride=reduction)
        bn1 = self._batch_norm(conv1)
        relu1 = self._apply_relu(bn1)
        
        conv2 = self._convolve(relu1,
                              self.filters[f'block{block_idx}_conv2'],
                              stride=1)
        bn2 = self._batch_norm(conv2)
        
        # Shortcut path
        if reduction > 1 or f'block{block_idx}_shortcut' in self.filters:
            shortcut = self._convolve(input_data,
                                    self.filters[f'block{block_idx}_shortcut'],
                                    stride=reduction)
            shortcut = self._batch_norm(shortcut)
        else:
            shortcut = input_data
        
        # Add skip connection
        output = self._add_features(bn2, shortcut)
        return self._apply_relu(output)
    
    def _convolve(self,
                  input_data: List[List[List[float]]],
                  filter_weights: List[List[List[List[float]]]],
                  stride: int = 1) -> List[List[List[float]]]:
        """
        Apply convolution operation.
        
        Args:
            input_data: Input feature maps
            filter_weights: Convolutional filter weights
            stride: Convolution stride
            
        Returns:
            List[List[List[float]]]: Output feature maps
        """
        height = len(input_data)
        width = len(input_data[0])
        in_channels = len(input_data[0][0])
        
        kernel_size = len(filter_weights[0][0])
        out_channels = len(filter_weights)
        
        # Calculate output dimensions
        out_height = (height - kernel_size) // stride + 1
        out_width = (width - kernel_size) // stride + 1
        
        # Initialize output
        output = [[[0.0] * out_channels
                   for _ in range(out_width)]
                  for _ in range(out_height)]
        
        # Perform convolution
        for h in range(out_height):
            for w in range(out_width):
                for oc in range(out_channels):
                    value = 0.0
                    for i in range(kernel_size):
                        for j in range(kernel_size):
                            for ic in range(in_channels):
                                h_in = h * stride + i
                                w_in = w * stride + j
                                value += (input_data[h_in][w_in][ic] *
                                        filter_weights[oc][0][i][j][ic])
                    output[h][w][oc] = value
                    
        return output
    
    def _apply_relu(self,
                   features: List[List[List[float]]]) -> List[List[List[float]]]:
        """
        Apply ReLU activation function.
        
        Args:
            features: Input feature maps
            
        Returns:
            List[List[List[float]]]: Activated feature maps
        """
        return [[[max(0.0, val) for val in row]
                 for row in layer]
                for layer in features]
    
    def _add_features(self,
                     features1: List[List[List[float]]],
                     features2: List[List[List[float]]]) -> List[List[List[float]]]:
        """
        Add two feature maps element-wise.
        
        Args:
            features1: First feature maps
            features2: Second feature maps
            
        Returns:
            List[List[List[float]]]: Sum of feature maps
        """
        height = len(features1)
        width = len(features1[0])
        channels = len(features1[0][0])
        
        return [[[features1[h][w][c] + features2[h][w][c]
                 for c in range(channels)]
                for w in range(width)]
               for h in range(height)]
    
    def _extract_features(self,
                         image: List[List[List[float]]]) -> List[List[List[List[float]]]]:
        """
        Extract hierarchical features using ResNet-like architecture.
        
        Args:
            image: Input image as 3D list [height][width][3]
            
        Returns:
            List[List[List[List[float]]]]: Features from different blocks
        """
        features = []
        current_input = image
        
        # Process each block
        for block_idx, (_, reduction) in enumerate(self.block_configs):
            # Apply residual block
            block_output = self._apply_residual_block(current_input,
                                                    block_idx,
                                                    reduction)
            
            features.append(block_output)
            current_input = block_output
            
        return features
    
    def compute(self,
                         image1: List[List[List[float]]],
                         image2: List[List[List[float]]]) -> float:
        """
        Calculate the ResNet-based distance between two images.
        
        Args:
            image1: First image as 3D list [height][width][3]
            image2: Second image as 3D list [height][width][3]
            
        Returns:
            float: Distance score (lower means more similar)
            
        Raises:
            ValueError: If images have different dimensions
        """
        if (len(image1) != len(image2) or
            len(image1[0]) != len(image2[0])):
            raise ValueError("Images must have the same dimensions")
        
        # Extract features
        features1 = self._extract_features(image1)
        features2 = self._extract_features(image2)
        
        # Calculate distance at each block
        total_distance = 0.0
        block_weights = [0.1, 0.2, 0.3, 0.4][:self.n_blocks]  # More weight to deeper blocks
        
        for feat1, feat2, weight in zip(features1, features2, block_weights):
            # Calculate Euclidean distance between feature maps
            block_distance = 0.0
            for h in range(len(feat1)):
                for w in range(len(feat1[0])):
                    for c in range(len(feat1[0][0])):
                        diff = feat1[h][w][c] - feat2[h][w][c]
                        block_distance += diff * diff
                        
            total_distance += weight * sqrt(block_distance)
            
        return total_distance
    
    def __str__(self) -> str:
        """
        String representation of the ResNet-based distance calculator.
        
        Returns:
            str: Description of the calculator
        """
        return f"ResNet-Based Image Distance Calculator (n_blocks={self.n_blocks})"
######################################
from typing import List, Tuple, Dict, Optional, Union
from math import exp, sqrt
import statistics
from collections import defaultdict

class InceptionDistance(Distance):
    """
    A pure Python implementation of Inception-based image distance calculation.
    This is a simplified version that captures the core concepts of using
    Inception-like features for image comparison without deep learning dependencies.
    
    The implementation includes:
    1. Inception modules with parallel paths
    2. Multi-scale feature extraction
    3. Global average pooling
    4. Distance computation between feature representations
    
    Note: For production use, consider using the official Inception implementation
    with pre-trained weights through a deep learning framework.
    """
    
    def __init__(self, n_modules: int = 3):
        """
        Initialize the Inception-based distance calculator.
        
        Args:
            n_modules (int): Number of Inception modules
        """
        super().__init__()
        self.type='image'
        
        self.n_modules = n_modules
        self.filters = self._initialize_filters()
        self.module_configs = [
            # (1x1, 3x3_reduce, 3x3, 5x5_reduce, 5x5, pool_proj)
            (64, 96, 128, 16, 32, 32),    # Module 1
            (128, 128, 192, 32, 96, 64),  # Module 2
            (192, 192, 256, 48, 128, 96)  # Module 3
        ][:n_modules]
    
    def _initialize_filters(self) -> Dict[str, List[List[List[List[float]]]]]:
        """
        Initialize simplified convolutional filters for Inception modules.
        
        Returns:
            Dict[str, List[List[List[List[float]]]]]: Filters for each path
        """
        filters = {}
        current_channels = 3  # Starting with RGB
        
        for module_idx, config in enumerate(self.module_configs):
            # 1x1 convolutions
            filters[f'module{module_idx}_1x1'] = self._create_filters(
                current_channels, config[0], 1)
            
            # 3x3 path
            filters[f'module{module_idx}_3x3_reduce'] = self._create_filters(
                current_channels, config[1], 1)
            filters[f'module{module_idx}_3x3'] = self._create_filters(
                config[1], config[2], 3)
            
            # 5x5 path
            filters[f'module{module_idx}_5x5_reduce'] = self._create_filters(
                current_channels, config[3], 1)
            filters[f'module{module_idx}_5x5'] = self._create_filters(
                config[3], config[4], 5)
            
            # Pool projection
            filters[f'module{module_idx}_pool_proj'] = self._create_filters(
                current_channels, config[5], 1)
            
            current_channels = config[0] + config[2] + config[4] + config[5]
            
        return filters
    
    def _create_filters(self,
                       in_channels: int,
                       out_channels: int,
                       kernel_size: int) -> List[List[List[List[float]]]]:
        """
        Create basic convolutional filters.
        
        Args:
            in_channels: Number of input channels
            out_channels: Number of output channels
            kernel_size: Size of the kernel
            
        Returns:
            List[List[List[List[float]]]]: Basic convolutional filters
        """
        filters = []
        for _ in range(out_channels):
            filter_weights = [[[[0.0] * in_channels
                              for _ in range(kernel_size)]
                             for _ in range(kernel_size)]
                            for _ in range(1)]
            
            # Initialize with simple patterns
            for c in range(in_channels):
                if kernel_size == 1:
                    filter_weights[0][0][0][c] = 1.0 / in_channels
                else:
                    center = kernel_size // 2
                    filter_weights[0][center][center][c] = 1.0 / in_channels
                    filter_weights[0][0][0][c] = -0.2 / in_channels
                    filter_weights[0][-1][-1][c] = -0.2 / in_channels
                    
            filters.append(filter_weights)
            
        return filters
    
    def _convolve(self,
                  input_data: List[List[List[float]]],
                  filter_weights: List[List[List[List[float]]]], 
                  stride: int = 1) -> List[List[List[float]]]:
        """
        Apply convolution operation.
        
        Args:
            input_data: Input feature maps
            filter_weights: Convolutional filter weights
            stride: Convolution stride
            
        Returns:
            List[List[List[float]]]: Output feature maps
        """
        height = len(input_data)
        width = len(input_data[0])
        in_channels = len(input_data[0][0])
        
        kernel_size = len(filter_weights[0][0])
        out_channels = len(filter_weights)
        
        # Calculate output dimensions
        out_height = (height - kernel_size) // stride + 1
        out_width = (width - kernel_size) // stride + 1
        
        # Initialize output
        output = [[[0.0] * out_channels
                   for _ in range(out_width)]
                  for _ in range(out_height)]
        
        # Perform convolution
        for h in range(out_height):
            for w in range(out_width):
                for oc in range(out_channels):
                    value = 0.0
                    for i in range(kernel_size):
                        for j in range(kernel_size):
                            for ic in range(in_channels):
                                h_in = h * stride + i
                                w_in = w * stride + j
                                value += (input_data[h_in][w_in][ic] *
                                        filter_weights[oc][0][i][j][ic])
                    output[h][w][oc] = max(0.0, value)  # ReLU activation
                    
        return output
    
    def _max_pool(self,
                 input_data: List[List[List[float]]],
                 pool_size: int = 3,
                 stride: int = 1) -> List[List[List[float]]]:
        """
        Apply max pooling operation.
        
        Args:
            input_data: Input feature maps
            pool_size: Size of pooling window
            stride: Pooling stride
            
        Returns:
            List[List[List[float]]]: Pooled feature maps
        """
        height = len(input_data)
        width = len(input_data[0])
        channels = len(input_data[0][0])
        
        out_height = (height - pool_size) // stride + 1
        out_width = (width - pool_size) // stride + 1
        
        output = [[[0.0] * channels
                   for _ in range(out_width)]
                  for _ in range(out_height)]
        
        for h in range(out_height):
            for w in range(out_width):
                for c in range(channels):
                    max_val = float('-inf')
                    for i in range(pool_size):
                        for j in range(pool_size):
                            h_in = h * stride + i
                            w_in = w * stride + j
                            max_val = max(max_val, input_data[h_in][w_in][c])
                    output[h][w][c] = max_val
                    
        return output
    
    def _concatenate_features(self,
                            feature_maps: List[List[List[List[float]]]]) -> List[List[List[float]]]:
        """
        Concatenate feature maps along the channel dimension.
        
        Args:
            feature_maps: List of feature maps to concatenate
            
        Returns:
            List[List[List[float]]]: Concatenated feature maps
        """
        height = len(feature_maps[0])
        width = len(feature_maps[0][0])
        total_channels = sum(len(fm[0][0]) for fm in feature_maps)
        
        output = [[[0.0] * total_channels
                   for _ in range(width)]
                  for _ in range(height)]
        
        channel_offset = 0
        for fm in feature_maps:
            channels = len(fm[0][0])
            for h in range(height):
                for w in range(width):
                    for c in range(channels):
                        output[h][w][channel_offset + c] = fm[h][w][c]
            channel_offset += channels
            
        return output
    
    def _apply_inception_module(self,
                              input_data: List[List[List[float]]],
                              module_idx: int) -> List[List[List[float]]]:
        """
        Apply an Inception module with parallel paths.
        
        Args:
            input_data: Input feature maps
            module_idx: Index of the current module
            
        Returns:
            List[List[List[float]]]: Output feature maps
        """
        # 1x1 convolution path
        path1x1 = self._convolve(input_data,
                                self.filters[f'module{module_idx}_1x1'])
        
        # 3x3 path
        path3x3 = self._convolve(input_data,
                                self.filters[f'module{module_idx}_3x3_reduce'])
        path3x3 = self._convolve(path3x3,
                                self.filters[f'module{module_idx}_3x3'])
        
        # 5x5 path
        path5x5 = self._convolve(input_data,
                                self.filters[f'module{module_idx}_5x5_reduce'])
        path5x5 = self._convolve(path5x5,
                                self.filters[f'module{module_idx}_5x5'])
        
        # Pool path
        pool_path = self._max_pool(input_data)
        pool_path = self._convolve(pool_path,
                                  self.filters[f'module{module_idx}_pool_proj'])
        
        # Concatenate all paths
        return self._concatenate_features([path1x1, path3x3, path5x5, pool_path])
    
    def _extract_features(self,
                         image: List[List[List[float]]]) -> List[List[List[List[float]]]]:
        """
        Extract hierarchical features using Inception-like architecture.
        
        Args:
            image: Input image as 3D list [height][width][3]
            
        Returns:
            List[List[List[List[float]]]]: Features from different modules
        """
        features = []
        current_input = image
        
        # Process each module
        for module_idx in range(self.n_modules):
            module_output = self._apply_inception_module(current_input, module_idx)
            features.append(module_output)
            current_input = module_output
            
        return features
    
    def compute(self,
                         image1: List[List[List[float]]],
                         image2: List[List[List[float]]]) -> float:
        """
        Calculate the Inception-based distance between two images.
        
        Args:
            image1: First image as 3D list [height][width][3]
            image2: Second image as 3D list [height][width][3]
            
        Returns:
            float: Distance score (lower means more similar)
            
        Raises:
            ValueError: If images have different dimensions
        """
        if (len(image1) != len(image2) or
            len(image1[0]) != len(image2[0])):
            raise ValueError("Images must have the same dimensions")
        
        # Extract features
        features1 = self._extract_features(image1)
        features2 = self._extract_features(image2)
        
        # Calculate distance at each module
        total_distance = 0.0
        module_weights = [0.2, 0.3, 0.5][:self.n_modules]  # More weight to deeper modules
        
        for feat1, feat2, weight in zip(features1, features2, module_weights):
            # Calculate Euclidean distance between feature maps
            module_distance = 0.0
            for h in range(len(feat1)):
                for w in range(len(feat1[0])):
                    for c in range(len(feat1[0][0])):
                        diff = feat1[h][w][c] - feat2[h][w][c]
                        module_distance += diff * diff
                        
            total_distance += weight * sqrt(module_distance)
            
        return total_distance
    
    def __str__(self) -> str:
        """
        String representation of the Inception-based distance calculator.
        
        Returns:
            str: Description of the calculator
        """
        return f"Inception-Based Image Distance Calculator (n_modules={self.n_modules})"
#######################################


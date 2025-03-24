from .mainClass import *
from .lossFunction import MeanSquaredError


import cmath
from typing import List, Tuple

class SpectralConvergence(Distance):

    def __init__(self) -> None:
        super().__init__()
        self.type='sound'

    def compute(self, signal1: List[float], signal2: List[float]) -> float:
        """
        Compute the Spectral Convergence between two signals.

        :param signal1: The first signal as a list of floats.
        :param signal2: The second signal as a list of floats.
        :return: The spectral convergence between the two signals as a float.
        """
        # Compute the FFT for both signals
        fft1: List[complex] = Sound().FFT(signal1)
        fft2: List[complex] = Sound().FFT(signal2)

        # Compute magnitudes of the spectrums
        mag1: List[float] = Sound.magnitude(fft1)
        mag2: List[float] = Sound.magnitude(fft2)

        # Ensure both spectrums are of the same length
        if len(mag1) != len(mag2):
            raise ValueError("Both signals must have the same length.")

        # Compute the Spectral Convergence
        numerator: float = sum(abs(m1 - m2) for m1, m2 in zip(mag1, mag2))
        denominator: float = sum(mag1)

        # To avoid division by zero
        if denominator == 0:
            return float('inf')

        return numerator / denominator

import math
import cmath

class MFCCProcessor(Distance):
    def __init__(self, sample_rate: int = 16000, n_mfcc: int = 13, n_fft: int = 2048, n_mels: int = 26)-> None:
        super().__init__()
        self.type='sound'

        self.sample_rate = sample_rate
        self.n_mfcc = n_mfcc
        self.n_fft = n_fft
        self.n_mels = n_mels

    def _mel_to_hz(self, mel: float) -> float:
        return 700 * (10 ** (mel / 2595) - 1)

    def _hz_to_mel(self, hz: float) -> float:
        return 2595 * math.log10(1 + hz / 700)

    def _mel_filterbank(self) -> List[List[float]]:
        low_freq_mel = self._hz_to_mel(0)
        high_freq_mel = self._hz_to_mel(self.sample_rate / 2)
        mel_points = [low_freq_mel + i * (high_freq_mel - low_freq_mel) / (self.n_mels + 1) for i in range(self.n_mels + 2)]
        hz_points = [self._mel_to_hz(mel) for mel in mel_points]
        bin_points = [int(round((self.n_fft + 1) * hz / self.sample_rate)) for hz in hz_points]

        fbank = [[0.0] * (self.n_fft // 2 + 1) for _ in range(self.n_mels)]
        for m in range(1, self.n_mels + 1):
            f_m_minus = bin_points[m - 1]
            f_m = bin_points[m]
            f_m_plus = bin_points[m + 1]

            for k in range(f_m_minus, f_m):
                fbank[m-1][k] = (k - f_m_minus) / (f_m - f_m_minus)
            for k in range(f_m, f_m_plus):
                fbank[m-1][k] = (f_m_plus - k) / (f_m_plus - f_m)

        return fbank

    def _dct(self, x: List[float]) -> List[float]:
        N = len(x)
        y = [0.0] * N
        for k in range(N):
            for n in range(N):
                y[k] += x[n] * math.cos(math.pi * k * (2 * n + 1) / (2 * N))
        return y

    def compute(self, signal1: List[float], signal2: List[float]) -> Tuple[List[List[float]], List[List[float]]]:
        """
        Calcule les MFCC pour deux signaux audio.

        Args:
            signal1 (List[float]): Premier signal audio.
            signal2 (List[float]): Deuxième signal audio.

        Returns:
            Tuple[List[List[float]], List[List[float]]]: MFCC des deux signaux.
        """
        def process_signal(signal: List[float]) -> List[List[float]]:
            # Pré-accentuation
            pre_emphasis = 0.97
            emphasized_signal = [signal[i] - pre_emphasis * signal[i-1] for i in range(1, len(signal))]

            # Fenêtrage
            frame_length = self.n_fft
            frame_step = frame_length // 2
            frames = [emphasized_signal[i:i+frame_length] for i in range(0, len(emphasized_signal) - frame_length + 1, frame_step)]

            # Appliquer la fenêtre de Hamming
            hamming = [0.54 - 0.46 * math.cos(2 * math.pi * i / (frame_length - 1)) for i in range(frame_length)]
            windowed_frames = [[frame[i] * hamming[i] for i in range(len(frame))] for frame in frames]

            # FFT
            magnitude_frames = [[abs(x) for x in Sound().FFT(frame)] for frame in windowed_frames]

            # Mel filterbank
            mel_fb = self._mel_filterbank()
            mel_spectrum = [[sum(m * f for m, f in zip(mel_filter, frame[:len(mel_filter)])) for mel_filter in mel_fb] for frame in magnitude_frames]

            # Log
            log_mel_spectrum = [[math.log(x + 1e-8) for x in frame] for frame in mel_spectrum]

            # DCT
            mfcc = [self._dct(frame)[:self.n_mfcc] for frame in log_mel_spectrum]

            return mfcc

        mfcc1 = process_signal(signal1)
        mfcc2 = process_signal(signal2)

        return mfcc1, mfcc2

    def compare_mfcc(self, signal1: List[float], signal2: List[float]) -> List[float]:
        """
        Calcule et compare les MFCC de deux signaux audio.

        Args:
            signal1 (List[float]): Premier signal audio.
            signal2 (List[float]): Deuxième signal audio.

        Returns:
            List[float]: Distance euclidienne moyenne entre les MFCC des deux signaux.
        """
        mfcc1, mfcc2 = self.compute(signal1, signal2)

        # Assurez-vous que les deux MFCC ont le même nombre de trames
        min_frames = min(len(mfcc1), len(mfcc2))
        mfcc1 = mfcc1[:min_frames]
        mfcc2 = mfcc2[:min_frames]

        # Calculez la distance euclidienne moyenne
        distances = []
        for frame1, frame2 in zip(mfcc1, mfcc2):
            distance = math.sqrt(sum((a - b) ** 2 for a, b in zip(frame1, frame2)))
            distances.append(distance)

        return sum(distances) / len(distances)
        
    def example(self):

      # Générer les signaux de test
      test_signal1, test_signal2 = Sound.generate_test_signals()

      # Afficher les 10 premiers échantillons de chaque signal
      print("10 premiers échantillons du signal 1:", test_signal1[:10])
      print("10 premiers échantillons du signal 2:", test_signal2[:10])

      print(f"Nombre d'échantillons dans chaque signal: {len(test_signal1)}")
      print(f"Fréquence d'échantillonnage: 16000 Hz")
      print(f"Durée de chaque signal: 1.0 seconde")


      # Créer une instance de MFCCProcessor
      processor = MFCCProcessor()

      # Calculer les MFCC pour les deux signaux
      mfcc1, mfcc2 = processor.compute(test_signal1, test_signal2)

      # Comparer les MFCC
      distance = processor.compare_mfcc(test_signal1, test_signal2)

      print(f"Nombre de trames MFCC pour chaque signal: {len(mfcc1)}")
      print(f"Nombre de coefficients MFCC par trame: {len(mfcc1[0])}")
      print(f"Distance moyenne entre les MFCC des deux signaux: {distance}")

      # Afficher les premiers coefficients MFCC de la première trame pour chaque signal
      print("Premiers coefficients MFCC du signal 1:", mfcc1[0][:5])
      print("Premiers coefficients MFCC du signal 2:", mfcc2[0][:5])
      
#claude ai fft
'''
from typing import List
import cmath

class SignalProcessor(Distance):

    def __init__(self) -> None:
        super().__init__()
        self.type='sound'

    def _fft(self, signal: List[float]) -> List[complex]:
        """
        Calcule la Transformée de Fourier Rapide (FFT) d'un signal sonore.

        Args:
            signal (List[float]): Le signal d'entrée sous forme de liste de nombres flottants.

        Returns:
            List[complex]: La FFT du signal sous forme de liste de nombres complexes.
        """
        n = len(signal)
        if n <= 1:
            return signal

        # Diviser le signal en pair et impair
        even = self._fft(signal[0::2])
        odd = self._fft(signal[1::2])

        # Combiner
        combined = [0] * n
        for k in range(n // 2):
            t = cmath.exp(-2j * cmath.pi * k / n) * odd[k]
            combined[k] = even[k] + t
            combined[k + n // 2] = even[k] - t

        return combined

    @staticmethod
    def pad_to_power_of_two(signal: List[float]) -> List[float]:
        """
        Complète le signal avec des zéros pour atteindre une longueur qui est une puissance de 2.

        Args:
            signal (List[float]): Le signal d'entrée.

        Returns:
            List[float]: Le signal complété.
        """
        n = 1
        while n < len(signal):
            n *= 2
        return signal + [0.0] * (n - len(signal))

processor = SignalProcessor()
signal1 = [0.1, 0.2, 0.3, 0.4, 0.5]  # exemple de signal
signal2 = [0.2, 0.3, 0.4, 0.5, 0.6]  # autre exemple de signal
fft_difference = processor._fft(signal1)
print(fft_difference)
'''
##############"
import math
from typing import List

class PowerSpectralDensityDistance(Distance):

    def __init__(self, sample_rate: int=16000) -> None:
        super().__init__()
        self.type='sound'

        self.sample_rate = sample_rate

    def _psd(self, signal: List[float]) -> List[float]:
        fft_result = Sound().FFT(signal)
        magnitude_spectrum = [abs(freq) ** 2 for freq in fft_result[:len(fft_result) // 2]]
        return magnitude_spectrum

    def compute(self, signal1: List[float], signal2: List[float]) -> float:
        psd1 = self._psd(signal1)
        psd2 = self._psd(signal2)

        distance = sum((psd1[i] - psd2[i]) ** 2 for i in range(min(len(psd1), len(psd2))))
        return math.sqrt(distance)
    def example(self):
      test_signal1, test_signal2 = Sound.generate_test_signals()
      psd_calculator = PowerSpectralDensityDistance(sample_rate=16000)
      psd_distance = psd_calculator.compute(test_signal1, test_signal2)
      print("PSD Distance:", psd_distance)
      
import math
from typing import List

class CrossCorrelation(Distance):

    def __init__(self, sample_rate: int=16000) -> None:
        super().__init__()
        self.type='sound'

        self.sample_rate: int = sample_rate

    def _mean(self, signal: List[float]) -> float:
        return sum(signal) / len(signal)

    def _normalize(self, signal: List[float]) -> List[float]:
        mean_value: float = self._mean(signal)
        return [x - mean_value for x in signal]

    def compute(self, signal1: List[float], signal2: List[float]) -> float:
        signal1_normalized: List[float] = self._normalize(signal1)
        signal2_normalized: List[float] = self._normalize(signal2)

        numerator: float = sum(signal1_normalized[i] * signal2_normalized[i] for i in range(min(len(signal1_normalized), len(signal2_normalized))))
        denominator_signal1: float = math.sqrt(sum(x ** 2 for x in signal1_normalized))
        denominator_signal2: float = math.sqrt(sum(x ** 2 for x in signal2_normalized))

        denominator: float = denominator_signal1 * denominator_signal2

        return numerator / denominator if denominator != 0 else 0.0
        
#ai claude

from typing import List, Tuple
import math
import cmath

class PhaseDifferenceCalculator(Distance):

    def __init__(self, sample_rate: int=16000, window_size: int= 1024, hop_size: int=512) -> None:
        """
        Initialise le calculateur de différence de phase.

        Args:
            sample_rate (int): Taux d'échantillonnage des signaux.
            window_size (int): Taille de la fenêtre pour l'analyse.
            hop_size (int): Taille du saut entre les fenêtres successives.
        """
        super().__init__()
        self.type='sound'

        self.sample_rate: int = sample_rate
        self.window_size: int = window_size
        self.hop_size: int = hop_size


    '''
    def _fft(self, signal: List[float]) -> List[complex]:
        """
        Calcule la Transformée de Fourier Rapide (FFT) du signal.

        Args:
            signal (List[float]): Signal d'entrée.

        Returns:
            List[complex]: FFT du signal.
        """
        n: int = len(signal)
        if n <= 1:
            return signal
        even: List[complex] = self._fft(signal[0::2])
        odd: List[complex] = self._fft(signal[1::2])
        combined: List[complex] = [0] * n
        for k in range(n // 2):
            t: complex = cmath.exp(-2j * math.pi * k / n) * odd[k]
            combined[k] = even[k] + t
            combined[k + n // 2] = even[k] - t
        return combined
    '''
    def compute(self, signal1: List[float], signal2: List[float]) -> List[float]:
        """
        Calcule la différence de phase entre deux signaux.

        Args:
            signal1 (List[float]): Premier signal.
            signal2 (List[float]): Deuxième signal.

        Returns:
            List[float]: Différence de phase pour chaque segment.
        """
        if len(signal1) != len(signal2):
            raise ValueError("Les signaux doivent avoir la même longueur")

        phase_differences: List[float] = []
        num_segments: int = (len(signal1) - self.window_size) // self.hop_size + 1

        for i in range(num_segments):
            start: int = i * self.hop_size
            end: int = start + self.window_size

            segment1: List[float] = Sound._apply_window(signal1[start:end])
            segment2: List[float] = Sound._apply_window(signal2[start:end])

            fft1: List[complex] = Sound().FFT(segment1)
            fft2: List[complex] = Sound().FFT(segment2)

            phase_diff: float = 0
            for f1, f2 in zip(fft1, fft2):
                if abs(f1) > 1e-6 and abs(f2) > 1e-6:  # Éviter la division par zéro
                    phase1: float = cmath.phase(f1)
                    phase2: float = cmath.phase(f2)
                    diff: float = phase2 - phase1
                    # Normaliser la différence de phase entre -pi et pi
                    phase_diff += (diff + math.pi) % (2 * math.pi) - math.pi

            phase_differences.append(phase_diff / len(fft1))

        return phase_differences

    def get_time_axis(self) -> List[float]:
        """
        Génère l'axe temporel pour les différences de phase calculées.

        Returns:
            List[float]: Axe temporel en secondes.
        """
        num_segments: int = len(self.compute([0] * self.window_size, [0] * self.window_size))
        return [i * self.hop_size / self.sample_rate for i in range(num_segments)]

    def analyze_signals(self, signal1: List[float], signal2: List[float]) -> Tuple[List[float], List[float]]:
        """
        Analyse deux signaux et retourne la différence de phase et l'axe temporel.

        Args:
            signal1 (List[float]): Premier signal.
            signal2 (List[float]): Deuxième signal.

        Returns:
            Tuple[List[float], List[float]]: Différence de phase et axe temporel.
        """
        phase_diff: List[float] = self.compute(signal1, signal2)
        time_axis: List[float] = self.get_time_axis()
        return phase_diff, time_axis
        
    def example(self):
      # Paramètres
      sample_rate: int = 44100  # Hz
      window_size: int = 1024   # échantillons
      hop_size: int = 512       # échantillons

      # Créer une instance du calculateur
      calculator: PhaseDifferenceCalculator = PhaseDifferenceCalculator(sample_rate, window_size, hop_size)

      # Supposons que nous ayons deux signaux signal1 et signal2
      signal1: List[float] = [0.1 * math.sin(2 * math.pi * 440 * t / 16000) for t in range(16000)]
      signal2: List[float] = [0.1 * math.sin(2 * math.pi * 880 * t / 16000) for t in range(16000)]

      # Analyser les signaux
      phase_differences: List[float]
      time_axis: List[float]
      phase_differences, time_axis = calculator.analyze_signals(signal1, signal2)

      # Afficher les résultats
      print("Différences de phase:", phase_differences[:10])  # Affiche les 10 premières valeurs
      print("Axe temporel:", time_axis[:10])  # Affiche les 10 premières valeurs
      
from typing import List
import math

class TimeLagDistance(Distance):

    def __init__(self, sample_rate: int=16000) -> None:
        super().__init__()
        self.type='sound'

        self.sample_rate: int = sample_rate

    def _cross_correlation(self, signal1: List[float], signal2: List[float], lag: int) -> float:
        n: int = len(signal1)
        if lag > 0:
            shifted_signal2: List[float] = [0] * lag + signal2[:-lag]
        else:
            shifted_signal2: List[float] = signal2[-lag:] + [0] * (-lag)

        return sum(signal1[i] * shifted_signal2[i] for i in range(n))

    def compute(self, signal1: List[float], signal2: List[float], max_lag: int) -> int:
        best_lag: int = 0
        best_correlation: float = -float('inf')

        for lag in range(-max_lag, max_lag + 1):
            correlation: float = self._cross_correlation(signal1, signal2, lag)
            if correlation > best_correlation:
                best_correlation = correlation
                best_lag = lag

        return best_lag
    def example(self):
      signal1: List[float] = [0.1 * math.sin(2 * math.pi * 440 * t / 16000) for t in range(16000)]
      signal2: List[float] = [0.1 * math.sin(2 * math.pi * 440 * (t - 100) / 16000) for t in range(16000)]  # signal2 is shifted

      time_lag_calculator = TimeLagDistance(sample_rate=16000)

      best_lag: int = time_lag_calculator.compute(signal1, signal2, max_lag=500)

      print("Optimal time lag:", best_lag)
      
from typing import List

class PESQ(Distance):

    def __init__(self, sample_rate: int=16000) -> None:
        super().__init__()
        self.type='sound'

        self.sample_rate: int = sample_rate

    def _preprocess(self, signal: List[float]) -> List[float]:
        # Placeholder preprocessing steps: normalization and filtering
        max_val: float = max(abs(x) for x in signal)
        return [x / max_val for x in signal] if max_val != 0 else signal

    def _compare_signals(self, reference: List[float], degraded: List[float]) -> float:
        # Placeholder function to simulate signal comparison
        mse: float = sum((reference[i] - degraded[i]) ** 2 for i in range(min(len(reference), len(degraded))))
        return mse / len(reference)

    def compute(self, reference_signal: List[float], degraded_signal: List[float]) -> float:
        reference_processed: List[float] = self._preprocess(reference_signal)
        degraded_processed: List[float] = self._preprocess(degraded_signal)

        comparison_score: float = self._compare_signals(reference_processed, degraded_processed)

        # Placeholder formula for PESQ score (the actual PESQ model is more complex)
        pesq_score: float = 4.5 - comparison_score  # 4.5 is the best score in PESQ scale

        return max(1.0, min(pesq_score, 4.5))  # PESQ scores typically range between 1.0 and 4.5
        
        
import cmath
from typing import List

class LogSpectralDistance(Distance):

    def __init__(self, sample_rate: int=16000) -> None:
        super().__init__()
        self.type='sound'

        self.sample_rate: int = sample_rate

    def _log_magnitude_spectrum(self, signal: List[float]) -> List[float]:
        fft_result: List[complex] = Sound().FFT(signal)
        return [20 * math.log10(abs(x)) if abs(x) != 0 else 0 for x in fft_result]

    def compute(self, signal1: List[float], signal2: List[float]) -> float:
        log_spectrum1: List[float] = self._log_magnitude_spectrum(signal1)
        log_spectrum2: List[float] = self._log_magnitude_spectrum(signal2)

        # Calculate the squared differences between the log-magnitude spectra
        squared_diffs: List[float] = [(log_spectrum1[i] - log_spectrum2[i]) ** 2 for i in range(min(len(log_spectrum1), len(log_spectrum2)))]

        # Compute the LSD value
        mean_squared_diff: float = sum(squared_diffs) / len(squared_diffs)
        return math.sqrt(mean_squared_diff)
        
import math
from typing import List

class BarkSpectralDistortion(Distance):

    def __init__(self, sample_rate: int=16000) -> None:
        super().__init__()
        self.type='sound'

        self.sample_rate: int = sample_rate

    def _bark_scale(self, freq: float) -> float:
        return 13 * math.atan(0.00076 * freq) + 3.5 * math.atan((freq / 7500) ** 2)

    def _compute_bark_spectrum(self, signal: List[float]) -> List[float]:
        fft_result: List[complex] = Sound().FFT(signal)
        N: int = len(fft_result)
        bark_spectrum: List[float] = [0.0] * N

        for i in range(N):
            freq: float = i * (self.sample_rate / N)
            bark_freq: float = self._bark_scale(freq)
            magnitude: float = abs(fft_result[i])
            bark_spectrum[i] = 20 * math.log10(magnitude) if magnitude != 0 else 0

        return bark_spectrum

    def compute(self, signal1: List[float], signal2: List[float]) -> float:
        bark_spectrum1: List[float] = self._compute_bark_spectrum(signal1)
        bark_spectrum2: List[float] = self._compute_bark_spectrum(signal2)

        squared_diffs: List[float] = [(bark_spectrum1[i] - bark_spectrum2[i]) ** 2 for i in range(min(len(bark_spectrum1), len(bark_spectrum2)))]

        mean_squared_diff: float = sum(squared_diffs) / len(squared_diffs)
        return math.sqrt(mean_squared_diff)

import math
from typing import List

class ItakuraSaitoDistance(Distance):

    def __init__(self) -> None:
        super().__init__()
        self.type='sound'

    def _power_spectrum(self, signal: List[float]) -> List[float]:
        N: int = len(signal)
        power_spectrum: List[float] = [0.0] * N

        for i in range(N):
            power_spectrum[i] = signal[i] ** 2
        
        return power_spectrum

    def compute(self, signal1: List[float], signal2: List[float]) -> float:
        if len(signal1) != len(signal2):
            raise ValueError("Both signals must have the same length.")

        power_spectrum1: List[float] = self._power_spectrum(signal1)
        power_spectrum2: List[float] = self._power_spectrum(signal2)
        
        is_distance: float = 0.0
        for ps1, ps2 in zip(power_spectrum1, power_spectrum2):
            if ps2 > 0:
                is_distance += (ps1 / ps2) - math.log(ps1 / ps2) - 1
        
        return is_distance
        
import math
from typing import List

class SignalToNoiseRatio(Distance):

    def __init__(self) -> None:
        super().__init__()
        self.type='sound'

    def _power(self, signal: List[float]) -> float:
        power: float = sum(s ** 2 for s in signal) / len(signal)
        return power

    def compute(self, signal: List[float], noise: List[float]) -> float:
        if len(signal) != len(noise):
            raise ValueError("Signal and noise must have the same length.")

        signal_power: float = self._power(signal)
        noise_power: float = self._power(noise)

        if noise_power == 0:
            raise ValueError("Noise power is zero, cannot compute SNR.")

        snr: float = 10 * math.log10(signal_power / noise_power)
        return snr


import math

class PeakSignalToNoiseRatio(Distance):

    def __init__(self) -> None:
        super().__init__()
        self.type='sound'

    def compute(self, signal1: List[float], signal2: List[float], max_signal_value: float) -> float:
        mse: float = MeanSquaredError().compute(signal1, signal2)
        if mse == 0:
            return float('inf')  # Signals are identical

        psnr: float = 10 * math.log10(max_signal_value ** 2 / mse)
        return psnr
        
    def example(self):
      signal1: List[float] = [0.1 * math.sin(2 * math.pi * 440 * t / 16000) for t in range(16000)]
      signal2: List[float] = [0.1 * math.sin(2 * math.pi * 445 * t / 16000) for t in range(16000)]  # Slightly different frequency

      max_signal_value: float = 1.0  # Maximum possible value for a normalized signal

      psnr_value: float = self.compute(signal1, signal2, max_signal_value)

      print("Peak Signal-to-Noise Ratio (PSNR):", psnr_value)

class EnergyDistance(Distance):

    def __init__(self) -> None:
        super().__init__()
        self.type='sound'

    def _energy(self, signal: List[float]) -> float:
        energy: float = sum(s ** 2 for s in signal)
        return energy

    def compute(self, signal1: List[float], signal2: List[float]) -> float:
        if len(signal1) != len(signal2):
            raise ValueError("Both signals must have the same length.")

        energy1: float = self._energy(signal1)
        energy2: float = self._energy(signal2)

        energy_distance: float = abs(energy1 - energy2)
        return energy_distance
        
class EnvelopeCorrelation(Distance):

    def __init__(self) -> None:
        super().__init__()
        self.type='sound'

    def _envelope(self, signal: List[float]) -> List[float]:
        # Approximation of the envelope using the absolute value of the signal
        envelope: List[float] = [abs(s) for s in signal]
        return envelope

    def _mean(self, data: List[float]) -> float:
        return sum(data) / len(data)

    def _correlation(self, envelope1: List[float], envelope2: List[float]) -> float:
        mean1: float = self._mean(envelope1)
        mean2: float = self._mean(envelope2)

        numerator: float = sum((e1 - mean1) * (e2 - mean2) for e1, e2 in zip(envelope1, envelope2))
        denominator: float = math.sqrt(sum((e1 - mean1) ** 2 for e1 in envelope1) * sum((e2 - mean2) ** 2 for e2 in envelope2))

        if denominator == 0:
            return 0.0  # No correlation if denominator is zero

        return numerator / denominator

    def compute(self, signal1: List[float], signal2: List[float]) -> float:
        if len(signal1) != len(signal2):
            raise ValueError("Both signals must have the same length.")

        envelope1: List[float] = self._envelope(signal1)
        envelope2: List[float] = self._envelope(signal2)

        correlation: float = self._correlation(envelope1, envelope2)
        return correlation
        
class ZeroCrossingRateDistance(Distance):

    def __init__(self) -> None:
        super().__init__()
        self.type='sound'

    def _zero_crossing_rate(self, signal: List[float]) -> float:
        zero_crossings: int = 0
        for i in range(1, len(signal)):
            if (signal[i - 1] > 0 and signal[i] < 0) or (signal[i - 1] < 0 and signal[i] > 0):
                zero_crossings += 1

        zcr: float = zero_crossings / len(signal)
        return zcr

    def compute(self, signal1: List[float], signal2: List[float]) -> float:
        if len(signal1) != len(signal2):
            raise ValueError("Both signals must have the same length.")

        zcr1: float = self._zero_crossing_rate(signal1)
        zcr2: float = self._zero_crossing_rate(signal2)

        zcr_distance: float = abs(zcr1 - zcr2)
        return zcr_distance
        
class CochleagramDistance(Distance):

    def __init__(self, num_bands: int = 40)-> None:
        super().__init__()
        self.type='sound'

        self.num_bands: int = num_bands

    def _bandpass_filter(self, signal: List[float], band_index: int, total_bands: int) -> List[float]:
        # Simplified bandpass filter approximation
        filtered_signal: List[float] = [0.0] * len(signal)
        band_width: float = 0.5 / total_bands
        center_freq: float = (band_index + 0.5) * band_width
        for i in range(len(signal)):
            filtered_signal[i] = signal[i] * center_freq  # Simplified filter effect
        return filtered_signal

    def _cochleagram(self, signal: List[float]) -> List[List[float]]:
        cochleagram: List[List[float]] = []
        for band in range(self.num_bands):
            band_signal: List[float] = self._bandpass_filter(signal, band, self.num_bands)
            cochleagram.append(band_signal)
        return cochleagram

    def compute(self, signal1: List[float], signal2: List[float]) -> float:
        if len(signal1) != len(signal2):
            raise ValueError("Both signals must have the same length.")

        cochlea1: List[List[float]] = self._cochleagram(signal1)
        cochlea2: List[List[float]] = self._cochleagram(signal2)

        distance: float = Sound._mean_squared_error(cochlea1, cochlea2)
        return distance


from typing import List
import math

class ChromagramDistance(Distance):

    def __init__(self, num_bins: int = 12) -> None:
        super().__init__()
        self.type='sound'

        self.num_bins: int = num_bins

    def _frequency_to_bin(self, frequency: float) -> int:
        # Simple mapping of frequency to chroma bin
        if frequency>0:
           bin_index: int = int((12 * math.log2(frequency / 440.0) + 69) % 12)
           return bin_index
        else:
           return 0


    def _compute_chromagram(self, signal: List[float]) -> List[float]:
        chroma: List[float] = [0.0] * self.num_bins
        for sample in signal:
            # Simplified frequency estimation from signal sample (placeholder)
            frequency: float = abs(sample) * 1000.0
            bin_index: int = self._frequency_to_bin(frequency)
            chroma[bin_index] += 1

        # Normalize chromagram
        total_count: float = sum(chroma)
        if total_count > 0:
            chroma = [count / total_count for count in chroma]

        return chroma

    def compute(self, signal1: List[float], signal2: List[float]) -> float:
        if len(signal1) != len(signal2):
            raise ValueError("Both signals must have the same length.")

        chroma1: List[float] = self._compute_chromagram(signal1)
        chroma2: List[float] = self._compute_chromagram(signal2)

        distance: float = MeanSquaredError().compute(chroma1, chroma2)
        return distance

import cmath

class SpectrogramDistance(Distance):

    def __init__(self, window_size: int = 256, overlap: int = 128) -> None:
        super().__init__()
        self.type='sound'

        self.window_size: int = window_size
        self.overlap: int = overlap

    def _dft(self, signal: List[float]) -> List[complex]:
        N: int = len(signal)
        return [sum(signal[n] * cmath.exp(-2j * cmath.pi * k * n / N) for n in range(N)) for k in range(N)]

    def _spectrogram(self, signal: List[float]) -> List[List[float]]:
        step: int = self.window_size - self.overlap
        spectrogram: List[List[float]] = []

        for start in range(0, len(signal) - self.window_size + 1, step):
            windowed_signal: List[float] = signal[start:start + self.window_size]
            dft_result: List[complex] = self._dft(windowed_signal)
            magnitude: List[float] = [abs(freq) for freq in dft_result]
            spectrogram.append(magnitude)

        return spectrogram


    def compute(self, signal1: List[float], signal2: List[float]) -> float:
        if len(signal1) != len(signal2):
            raise ValueError("Both signals must have the same length.")

        spectrogram1: List[List[float]] = self._spectrogram(signal1)
        spectrogram2: List[List[float]] = self._spectrogram(signal2)
        distance: float = Sound._mean_squared_error(spectrogram1, spectrogram2)
        return distance
        
    def example(self):
			
      signal1: List[float] = [0.1 * math.sin(2 * math.pi * 440 * t / 16000) for t in range(16000)]
      signal2: List[float] = [0.1 * math.sin(2 * math.pi * 445 * t / 16000) for t in range(16000)]  # Slightly different frequency

      spectrogram_calculator = SpectrogramDistance(window_size=256, overlap=128)

      distance_value: float = spectrogram_calculator.compute(signal1, signal2)

      print("Spectrogram Distance:", distance_value)

import cmath

class CQTDistance(Distance):

    def __init__(self, num_bins: int = 24, window_size: int = 512) -> None:
        super().__init__()
        self.type='sound'

        self.num_bins: int = num_bins
        self.window_size: int = window_size

    def _dft(self, signal: List[float]) -> List[complex]:
        N: int = len(signal)
        return [sum(signal[n] * cmath.exp(-2j * cmath.pi * k * n / N) for n in range(N)) for k in range(N)]

    def _cqt(self, signal: List[float]) -> List[List[float]]:
        step: int = self.window_size
        cqt_matrix: List[List[float]] = []

        for start in range(0, len(signal) - self.window_size + 1, step):
            windowed_signal: List[float] = signal[start:start + self.window_size]
            dft_result: List[complex] = self._dft(windowed_signal)

            # Compute magnitude and split into bins
            magnitude: List[float] = [abs(freq) for freq in dft_result]
            cqt_bins: List[float] = [sum(magnitude[i] for i in range(self.num_bins))]  # Simplified CQT binning
            cqt_matrix.append(cqt_bins)

        return cqt_matrix

    def compute(self, signal1: List[float], signal2: List[float]) -> float:
        if len(signal1) != len(signal2):
            raise ValueError("Both signals must have the same length.")

        cqt1: List[List[float]] = self._cqt(signal1)
        cqt2: List[List[float]] = self._cqt(signal2)

        distance: float = Sound._mean_squared_error(cqt1, cqt2)
        return distance
    def example(self):
      signal1: List[float] = [0.1 * math.sin(2 * math.pi * 440 * t / 16000) for t in range(16000)]
      signal2: List[float] = [0.1 * math.sin(2 * math.pi * 445 * t / 16000) for t in range(16000)]  # Slightly different frequency

      cqt_calculator = CQTDistance(num_bins=24, window_size=512)

      distance_value: float = cqt_calculator.compute(signal1, signal2)

      print("CQT Distance:", distance_value)
      
import wave
from typing import Tuple

class CepstralDistance(Distance):

    def __init__(self, sample_rate: int = 16000, frame_size: int = 512, num_coefficients: int = 13) -> None:
        """
        Initializes the CepstralDistance class with the specified parameters.
        
        :param sample_rate: The sampling rate of the audio signal.
        :param frame_size: The size of each frame used for analysis.
        :param num_coefficients: The number of cepstral coefficients to extract.
        """
        super().__init__()
        self.type='sound'

        self.sample_rate: int = sample_rate
        self.frame_size: int = frame_size
        self.num_coefficients: int = num_coefficients



    def compute_cepstral_coefficients(self, signal: List[float]) -> List[float]:
        """
        Computes the cepstral coefficients of a given audio signal.
        
        :param signal: The input audio signal as a list of floats.
        :return: The cepstral coefficients as a list of floats.
        """
        # Compute the power spectrum (simplified for the example)
        power_spectrum: List[float] = [math.log(abs(s)) for s in signal if s!=0]

        # Apply the inverse Fourier transform to obtain cepstral coefficients
        cepstrum: List[float] = Sound().inverse_fft(power_spectrum)

        # Return only the first 'num_coefficients' coefficients
        return cepstrum[:self.num_coefficients]



    def compute_distance(self, cepstral_1: List[float], cepstral_2: List[float]) -> float:
        """
        Computes the Euclidean distance between two sets of cepstral coefficients.
        
        :param cepstral_1: The first set of cepstral coefficients.
        :param cepstral_2: The second set of cepstral coefficients.
        :return: The cepstral distance as a float.
        """
        return math.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(cepstral_1, cepstral_2)))

    def compute(self, file1: str, file2: str) -> float:
        """
        Computes the Cepstral Distance between two audio files.
        
        :param file1: Path to the first audio file.
        :param file2: Path to the second audio file.
        :return: The Cepstral Distance as a float.
        """
        audio_data_1, sample_rate_1 = Sound().read_audio(filepath=file1)
        audio_data_2, sample_rate_2 = Sound().read_audio(filepath=file2)

        if sample_rate_1 != sample_rate_2:
            raise ValueError("Sample rates of the two audio files must be the same.")

        cepstral_1: List[float] = self.compute_cepstral_coefficients(audio_data_1)
        cepstral_2: List[float] = self.compute_cepstral_coefficients(audio_data_2)

        distance: float = self.compute_distance(cepstral_1, cepstral_2)
        return distance



##############################################
#perplexity ai
from typing import List
import math

class SpectralFlatnessMeasure(Distance):
    def __init__(self, signal1: List[float], signal2: List[float]):
        """
        Initialize the SpectralFlatnessMeasure class with two sound signals.
        
        :param signal1: First sound signal as a list of float values
        :param signal2: Second sound signal as a list of float values
        """
        super().__init__()

        self.signal1 = signal1
        self.signal2 = signal2

    def calculate_sfm(self, signal: List[float]) -> float:
        """
        Calculate the Spectral Flatness Measure (SFM) for a given signal.
        
        :param signal: Sound signal as a list of float values
        :return: SFM value as a float
        """
        n = len(signal)
        
        # Calculate the geometric mean
        geometric_mean = math.exp(sum(math.log(abs(x) + 1e-6) for x in signal) / n)
        
        # Calculate the arithmetic mean
        arithmetic_mean = sum(abs(x) for x in signal) / n
        
        # Calculate SFM
        sfm = geometric_mean / arithmetic_mean
        
        return sfm

    def compare_sfm(self) -> float:
        """
        Compare the SFM values of the two signals and return their difference.
        
        :return: Difference between SFM values of signal1 and signal2
        """
        sfm1 = self.calculate_sfm(self.signal1)
        sfm2 = self.calculate_sfm(self.signal2)
        
        return abs(sfm1 - sfm2)
#################################################
'''
from typing import List
import math

class SpectralCentroidDistance:
    def __init__(self, signal1: List[float], signal2: List[float], sample_rate: int = 44100):
        """
        Initialize the SpectralCentroidDistance class with two audio signals.
        
        :param signal1: First audio signal as a list of float values
        :param signal2: Second audio signal as a list of float values
        :param sample_rate: Sampling rate of the audio signals (default: 44100 Hz)
        """
        self.signal1 = signal1
        self.signal2 = signal2
        self.sample_rate = sample_rate

    def calculate_spectral_centroid(self, signal: List[float]) -> float:
        """
        Calculate the spectral centroid for a given signal.
        
        :param signal: Audio signal as a list of float values
        :return: Spectral centroid value
        """
        magnitudes = self._fft_magnitude(signal)
        frequencies = self._fft_frequencies(len(signal))
        
        weighted_sum = sum(m * f for m, f in zip(magnitudes, frequencies))
        magnitude_sum = sum(magnitudes)
        
        return weighted_sum / magnitude_sum if magnitude_sum != 0 else 0

    def compare_brightness(self) -> float:
        """
        Compare the brightness of the two signals by calculating
        the difference between their spectral centroids.
        
        :return: Absolute difference between spectral centroids
        """
        centroid1 = self.calculate_spectral_centroid(self.signal1)
        centroid2 = self.calculate_spectral_centroid(self.signal2)
        
        return abs(centroid1 - centroid2)

    def _fft_magnitude(self, signal: List[float]) -> List[float]:
        """
        Calculate the magnitude spectrum of the signal using FFT.
        
        :param signal: Input signal
        :return: Magnitude spectrum
        """
        n = len(signal)
        fft = self._fft(signal)
        return [abs(x) for x in fft[:n//2]]

    def _fft_frequencies(self, n: int) -> List[float]:
        """
        Generate the frequency bins for FFT.
        
        :param n: Length of the signal
        :return: List of frequency bins
        """
        return [i * self.sample_rate / n for i in range(n//2)]

    def _fft(self, x: List[float]) -> List[complex]:
        """
        Cooley-Tukey FFT algorithm.
        
        :param x: Input signal
        :return: FFT of the signal
        """
        n = len(x)
        if n <= 1:
            return x
        even = self._fft(x[0::2])
        odd = self._fft(x[1::2])
        twiddle_factors = [math.e ** (-2j * math.pi * k / n) for k in range(n//2)]
        return [even[k] + twiddle_factors[k] * odd[k] for k in range(n//2)] + \
               [even[k] - twiddle_factors[k] * odd[k] for k in range(n//2)]
'''
##########################################
from typing import List
import math

class SpectralFlux(Distance):
    def __init__(self, signal1: List[float], signal2: List[float], frame_size: int = 1024, hop_size: int = 512):
        """
        Initialize the SpectralFlux class with two audio signals.

        :param signal1: First audio signal as a list of float values
        :param signal2: Second audio signal as a list of float values
        :param frame_size: Size of each frame for spectral analysis (default: 1024)
        :param hop_size: Number of samples between successive frames (default: 512)
        """
        super().__init__()

        self.signal1 = signal1
        self.signal2 = signal2
        self.frame_size = frame_size
        self.hop_size = hop_size

    def calculate_spectral_flux(self, signal: List[float]) -> List[float]:
        """
        Calculate the Spectral Flux for a given signal.

        :param signal: Audio signal as a list of float values
        :return: List of Spectral Flux values for each frame
        """
        frames = self._frame_signal(signal)
        spectra = [self._calculate_spectrum(frame) for frame in frames]
        
        flux = []
        for i in range(1, len(spectra)):
            diff = sum((spectra[i][j] - spectra[i-1][j])**2 for j in range(len(spectra[i])))
            flux.append(math.sqrt(diff))
        
        return flux

    def compare_spectral_flux(self) -> float:
        """
        Compare the Spectral Flux between the two signals.

        :return: Mean absolute difference of Spectral Flux values
        """
        flux1 = self.calculate_spectral_flux(self.signal1)
        flux2 = self.calculate_spectral_flux(self.signal2)
        
        # Ensure both flux lists have the same length
        min_length = min(len(flux1), len(flux2))
        flux1 = flux1[:min_length]
        flux2 = flux2[:min_length]
        
        # Calculate mean absolute difference
        diff = sum(abs(f1 - f2) for f1, f2 in zip(flux1, flux2)) / min_length
        return diff

    def _frame_signal(self, signal: List[float]) -> List[List[float]]:
        """
        Divide the signal into overlapping frames.

        :param signal: Input signal
        :return: List of frames
        """
        frames = []
        for i in range(0, len(signal) - self.frame_size + 1, self.hop_size):
            frames.append(signal[i:i+self.frame_size])
        return frames

    def _calculate_spectrum(self, frame: List[float]) -> List[float]:
        """
        Calculate the magnitude spectrum of a frame using FFT.

        :param frame: Input frame
        :return: Magnitude spectrum
        """
        fft_result = self._fft(frame)
        return [abs(x) for x in fft_result[:len(frame)//2]]

    def _fft(self, x: List[float]) -> List[complex]:
        """
        Cooley-Tukey FFT algorithm.

        :param x: Input signal
        :return: FFT of the signal
        """
        n = len(x)
        if n <= 1:
            return x
        even = self._fft(x[0::2])
        odd = self._fft(x[1::2])
        twiddle_factors = [math.e ** (-2j * math.pi * k / n) for k in range(n//2)]
        return [even[k] + twiddle_factors[k] * odd[k] for k in range(n//2)] + \
               [even[k] - twiddle_factors[k] * odd[k] for k in range(n//2)]

from typing import List
import math

class EnvelopeCrossDistance(Distance):
    def __init__(self, signal1: List[float], signal2: List[float], frame_size: int = 1024, hop_length: int = 512):
        """
        Initialize the EnvelopeCrossDistance class with two audio signals.

        :param signal1: First audio signal as a list of float values
        :param signal2: Second audio signal as a list of float values
        :param frame_size: Size of each frame for envelope calculation (default: 1024)
        :param hop_length: Number of samples between successive frames (default: 512)
        """
        super().__init__()

        self.signal1 = signal1
        self.signal2 = signal2
        self.frame_size = frame_size
        self.hop_length = hop_length

    def calculate_envelope(self, signal: List[float]) -> List[float]:
        """
        Calculate the amplitude envelope for a given signal.

        :param signal: Audio signal as a list of float values
        :return: List of amplitude envelope values
        """
        envelope = []
        for i in range(0, len(signal), self.hop_length):
            frame = signal[i:i + self.frame_size]
            envelope.append(max(abs(x) for x in frame))
        return envelope

    def calculate_cross_distance(self) -> float:
        """
        Calculate the Envelope Cross-Distance between the two signals.

        :return: Envelope Cross-Distance value
        """
        envelope1 = self.calculate_envelope(self.signal1)
        envelope2 = self.calculate_envelope(self.signal2)

        # Ensure both envelopes have the same length
        min_length = min(len(envelope1), len(envelope2))
        envelope1 = envelope1[:min_length]
        envelope2 = envelope2[:min_length]

        # Calculate the Euclidean distance between envelopes
        distance = math.sqrt(sum((e1 - e2) ** 2 for e1, e2 in zip(envelope1, envelope2)))
        
        # Normalize by the number of frames
        normalized_distance = distance / min_length

        return normalized_distance

##################################################
from typing import List
import math

class ShortTimeEnergyDistance(Distance):
    def __init__(self, signal1: List[float], signal2: List[float], frame_size: int = 1024, hop_size: int = 512):
        """
        Initialize the ShortTimeEnergyDistance class with two audio signals.

        :param signal1: First audio signal as a list of float values
        :param signal2: Second audio signal as a list of float values
        :param frame_size: Size of each frame for energy calculation (default: 1024)
        :param hop_size: Number of samples between successive frames (default: 512)
        """
        super().__init__()

        self.signal1 = signal1
        self.signal2 = signal2
        self.frame_size = frame_size
        self.hop_size = hop_size

    def calculate_short_time_energy(self, signal: List[float]) -> List[float]:
        """
        Calculate the Short-Time Energy for a given signal.

        :param signal: Audio signal as a list of float values
        :return: List of Short-Time Energy values
        """
        energy = []
        for i in range(0, len(signal) - self.frame_size + 1, self.hop_size):
            frame = signal[i:i + self.frame_size]
            frame_energy = sum(x**2 for x in frame) / self.frame_size
            energy.append(frame_energy)
        return energy

    def calculate_distance(self) -> float:
        """
        Calculate the Short-Time Energy Distance between the two signals.

        :return: Short-Time Energy Distance value
        """
        energy1 = self.calculate_short_time_energy(self.signal1)
        energy2 = self.calculate_short_time_energy(self.signal2)

        min_length = min(len(energy1), len(energy2))
        energy1 = energy1[:min_length]
        energy2 = energy2[:min_length]

        distance = math.sqrt(sum((e1 - e2)**2 for e1, e2 in zip(energy1, energy2)))
        normalized_distance = distance / min_length

        return normalized_distance

####################################
from typing import List
import math

class FrequencyBinDistance(Distance):
    def __init__(self, signal1: List[float], signal2: List[float], sample_rate: int = 44100, fft_size: int = 2048):
        """
        Initialize the FrequencyBinDistance class with two audio signals.

        :param signal1: First audio signal as a list of float values
        :param signal2: Second audio signal as a list of float values
        :param sample_rate: Sampling rate of the audio signals (default: 44100 Hz)
        :param fft_size: Size of the FFT (default: 2048)
        """
        super().__init__()

        self.signal1 = signal1
        self.signal2 = signal2
        self.sample_rate = sample_rate
        self.fft_size = fft_size
        self.frequency_bin_count = fft_size // 2

    def calculate_spectrum(self, signal: List[float]) -> List[float]:
        """
        Calculate the magnitude spectrum for a given signal.

        :param signal: Audio signal as a list of float values
        :return: Magnitude spectrum
        """
        fft_result = self._fft(signal[:self.fft_size])
        return [abs(x) for x in fft_result[:self.frequency_bin_count]]

    def calculate_bin_distance(self, start_freq: float, end_freq: float) -> float:
        """
        Calculate the Frequency Bin Distance between the two signals for a specific frequency range.

        :param start_freq: Start frequency of the range to compare (in Hz)
        :param end_freq: End frequency of the range to compare (in Hz)
        :return: Frequency Bin Distance value
        """
        spectrum1 = self.calculate_spectrum(self.signal1)
        spectrum2 = self.calculate_spectrum(self.signal2)

        bin_width = self.sample_rate / self.fft_size
        start_bin = int(start_freq / bin_width)
        end_bin = min(int(end_freq / bin_width), self.frequency_bin_count)

        distance = math.sqrt(sum((spectrum1[i] - spectrum2[i])**2 for i in range(start_bin, end_bin)))
        normalized_distance = distance / (end_bin - start_bin)

        return normalized_distance

    def _fft(self, x: List[float]) -> List[complex]:
        """
        Cooley-Tukey FFT algorithm.

        :param x: Input signal
        :return: FFT of the signal
        """
        n = len(x)
        if n <= 1:
            return x
        even = self._fft(x[0::2])
        odd = self._fft(x[1::2])
        twiddle_factors = [math.e ** (-2j * math.pi * k / n) for k in range(n//2)]
        return [even[k] + twiddle_factors[k] * odd[k] for k in range(n//2)] + \
               [even[k] - twiddle_factors[k] * odd[k] for k in range(n//2)]

#################################################
from typing import List
import math

class PitchDistance(Distance):
    def __init__(self, signal1: List[float], signal2: List[float], sample_rate: int = 44100, frame_size: int = 2048, num_harmonics: int = 5):
        """
        Initialize the PitchDistance class with two audio signals.

        :param signal1: First audio signal as a list of float values
        :param signal2: Second audio signal as a list of float values
        :param sample_rate: Sampling rate of the audio signals (default: 44100 Hz)
        :param frame_size: Size of the frame for FFT (default: 2048)
        :param num_harmonics: Number of harmonics to consider in HPS (default: 5)
        """
        super().__init__()

        self.signal1 = signal1
        self.signal2 = signal2
        self.sample_rate = sample_rate
        self.frame_size = frame_size
        self.num_harmonics = num_harmonics

    def calculate_pitch_distance(self) -> float:
        """
        Calculate the pitch distance between the two signals using HPS.

        :return: Pitch distance in Hz
        """
        pitch1 = self._estimate_pitch(self.signal1)
        pitch2 = self._estimate_pitch(self.signal2)
        return abs(pitch1 - pitch2)

    def _estimate_pitch(self, signal: List[float]) -> float:
        """
        Estimate the pitch of a signal using Harmonic Product Spectrum.

        :param signal: Audio signal as a list of float values
        :return: Estimated pitch in Hz
        """
        spectrum = self._calculate_spectrum(signal)
        hps = self._harmonic_product_spectrum(spectrum)
        peak_index = max(range(len(hps)), key=hps.__getitem__)
        return peak_index * self.sample_rate / self.frame_size

    def _calculate_spectrum(self, signal: List[float]) -> List[float]:
        """
        Calculate the magnitude spectrum of the signal.

        :param signal: Audio signal as a list of float values
        :return: Magnitude spectrum
        """
        fft_result = self._fft(signal[:self.frame_size])
        return [abs(x) for x in fft_result[:self.frame_size//2]]

    def _harmonic_product_spectrum(self, spectrum: List[float]) -> List[float]:
        """
        Apply Harmonic Product Spectrum algorithm.

        :param spectrum: Magnitude spectrum of the signal
        :return: HPS result
        """
        hps = spectrum.copy()
        for harmonic in range(2, self.num_harmonics + 1):
            downsampled = [0] * (len(spectrum) // harmonic)
            for i in range(len(downsampled)):
                downsampled[i] = spectrum[i * harmonic]
            hps = [hps[i] * downsampled[i] for i in range(len(downsampled))]
        return hps

    def _fft(self, x: List[float]) -> List[complex]:
        """
        Cooley-Tukey FFT algorithm.

        :param x: Input signal
        :return: FFT of the signal
        """
        n = len(x)
        if n <= 1:
            return x
        even = self._fft(x[0::2])
        odd = self._fft(x[1::2])
        twiddle_factors = [math.e ** (-2j * math.pi * k / n) for k in range(n//2)]
        return [even[k] + twiddle_factors[k] * odd[k] for k in range(n//2)] + \
               [even[k] - twiddle_factors[k] * odd[k] for k in range(n//2)]

#################################
from typing import List
import math

class LogFrequencySpectralDistance(Distance):
    def __init__(self, signal1: List[float], signal2: List[float], sample_rate: int = 44100, frame_size: int = 2048, min_freq: float = 20, max_freq: float = 20000, num_bins: int = 128):
        """
        Initialize the LogFrequencySpectralDistance class with two audio signals.

        :param signal1: First audio signal as a list of float values
        :param signal2: Second audio signal as a list of float values
        :param sample_rate: Sampling rate of the audio signals (default: 44100 Hz)
        :param frame_size: Size of the frame for FFT (default: 2048)
        :param min_freq: Minimum frequency for log-scale bins (default: 20 Hz)
        :param max_freq: Maximum frequency for log-scale bins (default: 20000 Hz)
        :param num_bins: Number of logarithmically spaced frequency bins (default: 128)
        """
        super().__init__()

        self.signal1 = signal1
        self.signal2 = signal2
        self.sample_rate = sample_rate
        self.frame_size = frame_size
        self.min_freq = min_freq
        self.max_freq = max_freq
        self.num_bins = num_bins
        self.log_freq_bins = self._create_log_freq_bins()

    def calculate_distance(self) -> float:
        """
        Calculate the Log-Frequency Spectral Distance between the two signals.

        :return: Log-Frequency Spectral Distance value
        """
        spectrum1 = self._calculate_log_spectrum(self.signal1)
        spectrum2 = self._calculate_log_spectrum(self.signal2)

        # Calculate Euclidean distance between log spectra
        distance = math.sqrt(sum((s1 - s2) ** 2 for s1, s2 in zip(spectrum1, spectrum2)))
        return distance

    def _calculate_log_spectrum(self, signal: List[float]) -> List[float]:
        """
        Calculate the log-frequency spectrum for a given signal.

        :param signal: Audio signal as a list of float values
        :return: Log-frequency spectrum
        """
        linear_spectrum = self._calculate_spectrum(signal)
        log_spectrum = [0] * self.num_bins

        for i, (low, high) in enumerate(self.log_freq_bins):
            bin_energy = sum(linear_spectrum[j] for j in range(low, high))
            log_spectrum[i] = math.log(bin_energy + 1e-10)  # Add small value to avoid log(0)

        return log_spectrum

    def _calculate_spectrum(self, signal: List[float]) -> List[float]:
        """
        Calculate the magnitude spectrum of the signal.

        :param signal: Audio signal as a list of float values
        :return: Magnitude spectrum
        """
        fft_result = self._fft(signal[:self.frame_size])
        return [abs(x) for x in fft_result[:self.frame_size//2]]

    def _create_log_freq_bins(self) -> List[tuple]:
        """
        Create logarithmically spaced frequency bins.

        :return: List of tuples representing frequency bin ranges
        """
        min_log = math.log(self.min_freq)
        max_log = math.log(self.max_freq)
        log_freq_step = (max_log - min_log) / self.num_bins

        bins = []
        for i in range(self.num_bins):
            low_freq = math.exp(min_log + i * log_freq_step)
            high_freq = math.exp(min_log + (i + 1) * log_freq_step)
            low_bin = int(low_freq * self.frame_size / self.sample_rate)
            high_bin = int(high_freq * self.frame_size / self.sample_rate)
            bins.append((low_bin, high_bin))

        return bins

    def _fft(self, x: List[float]) -> List[complex]:
        """
        Cooley-Tukey FFT algorithm.

        :param x: Input signal
        :return: FFT of the signal
        """
        n = len(x)
        if n <= 1:
            return x
        even = self._fft(x[0::2])
        odd = self._fft(x[1::2])
        twiddle_factors = [math.e ** (-2j * math.pi * k / n) for k in range(n//2)]
        return [even[k] + twiddle_factors[k] * odd[k] for k in range(n//2)] + \
               [even[k] - twiddle_factors[k] * odd[k] for k in range(n//2)]

#########################################
from typing import List, Tuple
import math

class CQTDistance(Distance):
    def __init__(self, signal1: List[float], signal2: List[float], sample_rate: int = 44100, 
                 min_freq: float = 55.0, max_freq: float = 7040.0, bins_per_octave: int = 12):
        """
        Initialize the CQTDistance class with two audio signals.

        :param signal1: First audio signal as a list of float values
        :param signal2: Second audio signal as a list of float values
        :param sample_rate: Sampling rate of the audio signals (default: 44100 Hz)
        :param min_freq: Minimum frequency for CQT (default: 55.0 Hz, A1 note)
        :param max_freq: Maximum frequency for CQT (default: 7040.0 Hz, A8 note)
        :param bins_per_octave: Number of bins per octave (default: 12, semitones)
        """
        super().__init__()

        self.signal1 = signal1
        self.signal2 = signal2
        self.sample_rate = sample_rate
        self.min_freq = min_freq
        self.max_freq = max_freq
        self.bins_per_octave = bins_per_octave
        self.num_octaves = math.ceil(math.log2(max_freq / min_freq))
        self.total_bins = self.num_octaves * bins_per_octave
        self.q_factor = 1 / (2 ** (1 / bins_per_octave) - 1)
        self.kernels = self._create_cqt_kernels()

    def calculate_distance(self) -> float:
        """
        Calculate the CQT distance between the two signals.

        :return: CQT distance value
        """
        cqt1 = self._compute_cqt(self.signal1)
        cqt2 = self._compute_cqt(self.signal2)

        # Calculate Euclidean distance between CQT representations
        distance = math.sqrt(sum((abs(c1) - abs(c2)) ** 2 for c1, c2 in zip(cqt1, cqt2)))
        return distance

    def _compute_cqt(self, signal: List[float]) -> List[complex]:
        """
        Compute the Constant-Q Transform for a given signal.

        :param signal: Audio signal as a list of float values
        :return: CQT coefficients
        """
        cqt = []
        for kernel in self.kernels:
            coefficient = sum(s * k.conjugate() for s, k in zip(signal, kernel))
            cqt.append(coefficient)
        return cqt

    def _create_cqt_kernels(self) -> List[List[complex]]:
        """
        Create CQT kernels for each frequency bin.

        :return: List of CQT kernels
        """
        kernels = []
        for k in range(self.total_bins):
            freq = self.min_freq * (2 ** (k / self.bins_per_octave))
            kernel_length = int(self.q_factor * self.sample_rate / freq)
            kernel = self._create_kernel(freq, kernel_length)
            kernels.append(kernel)
        return kernels

    def _create_kernel(self, freq: float, length: int) -> List[complex]:
        """
        Create a single CQT kernel for a specific frequency.

        :param freq: Frequency for the kernel
        :param length: Length of the kernel
        :return: CQT kernel as a list of complex values
        """
        kernel = []
        for n in range(length):
            t = n / self.sample_rate
            real = math.cos(2 * math.pi * freq * t)
            imag = math.sin(2 * math.pi * freq * t)
            window = 0.5 * (1 - math.cos(2 * math.pi * n / (length - 1)))  # Hann window
            kernel.append(complex(real * window, -imag * window))
        return kernel

#########################################
from typing import List
import math

class PEAQ(Distance):
    def __init__(self, reference: List[float], test: List[float], sample_rate: int = 44100):
        """
        Initialize the PEAQ class with reference and test audio signals.

        :param reference: Reference audio signal as a list of float values
        :param test: Test audio signal as a list of float values
        :param sample_rate: Sampling rate of the audio signals (default: 44100 Hz)
        """
        super().__init__()

        self.reference = reference
        self.test = test
        self.sample_rate = sample_rate
        self.frame_size = 2048
        self.hop_size = 1024

    def calculate_odg(self) -> float:
        """
        Calculate the Objective Difference Grade (ODG) between reference and test signals.

        :return: ODG value ranging from -4 (very annoying) to 0 (imperceptible difference)
        """
        movs = self._calculate_movs()
        odg = self._map_movs_to_odg(movs)
        return odg

    def _calculate_movs(self) -> List[float]:
        """
        Calculate Model Output Variables (MOVs) for PEAQ.

        :return: List of MOV values
        """
        ref_frames = self._frame_signal(self.reference)
        test_frames = self._frame_signal(self.test)
        
        total_noise_to_mask_ratio = 0
        total_bandwidth_difference = 0
        
        for ref_frame, test_frame in zip(ref_frames, test_frames):
            ref_spectrum = self._fft(ref_frame)
            test_spectrum = self._fft(test_frame)
            
            noise_to_mask_ratio = self._calculate_noise_to_mask_ratio(ref_spectrum, test_spectrum)
            bandwidth_difference = self._calculate_bandwidth_difference(ref_spectrum, test_spectrum)
            
            total_noise_to_mask_ratio += noise_to_mask_ratio
            total_bandwidth_difference += bandwidth_difference
        
        avg_noise_to_mask_ratio = total_noise_to_mask_ratio / len(ref_frames)
        avg_bandwidth_difference = total_bandwidth_difference / len(ref_frames)
        
        return [avg_noise_to_mask_ratio, avg_bandwidth_difference]

    def _map_movs_to_odg(self, movs: List[float]) -> float:
        """
        Map Model Output Variables (MOVs) to Objective Difference Grade (ODG).

        :param movs: List of MOV values
        :return: ODG value
        """
        # This is a simplified mapping function and doesn't represent the actual PEAQ neural network
        odg = -4 * (movs[0] / 30) - (movs[1] / 5)
        return max(-4, min(0, odg))

    def _frame_signal(self, signal: List[float]) -> List[List[float]]:
        """
        Divide the signal into overlapping frames.

        :param signal: Input signal
        :return: List of frames
        """
        frames = []
        for i in range(0, len(signal) - self.frame_size, self.hop_size):
            frames.append(signal[i:i+self.frame_size])
        return frames

    def _fft(self, frame: List[float]) -> List[complex]:
        """
        Perform Fast Fourier Transform on a frame.

        :param frame: Input frame
        :return: FFT result
        """
        n = len(frame)
        if n <= 1:
            return frame
        even = self._fft(frame[0::2])
        odd = self._fft(frame[1::2])
        return [even[k] + math.e**(-2j*math.pi*k/n) * odd[k] for k in range(n//2)] + \
               [even[k] - math.e**(-2j*math.pi*k/n) * odd[k] for k in range(n//2)]

    def _calculate_noise_to_mask_ratio(self, ref_spectrum: List[complex], test_spectrum: List[complex]) -> float:
        """
        Calculate the Noise-to-Mask Ratio (NMR) between reference and test spectra.

        :param ref_spectrum: Reference spectrum
        :param test_spectrum: Test spectrum
        :return: NMR value
        """
        # Simplified NMR calculation
        ref_power = sum(abs(x)**2 for x in ref_spectrum)
        noise_power = sum(abs(x-y)**2 for x, y in zip(ref_spectrum, test_spectrum))
        return 10 * math.log10(noise_power / (ref_power + 1e-10))

    def _calculate_bandwidth_difference(self, ref_spectrum: List[complex], test_spectrum: List[complex]) -> float:
        """
        Calculate the bandwidth difference between reference and test spectra.

        :param ref_spectrum: Reference spectrum
        :param test_spectrum: Test spectrum
        :return: Bandwidth difference value
        """
        # Simplified bandwidth difference calculation
        ref_bandwidth = self._estimate_bandwidth(ref_spectrum)
        test_bandwidth = self._estimate_bandwidth(test_spectrum)
        return abs(ref_bandwidth - test_bandwidth)

    def _estimate_bandwidth(self, spectrum: List[complex]) -> float:
        """
        Estimate the bandwidth of a spectrum.

        :param spectrum: Input spectrum
        :return: Estimated bandwidth
        """
        threshold = max(abs(x) for x in spectrum) / 100
        for i in range(len(spectrum) - 1, 0, -1):
            if abs(spectrum[i]) > threshold:
                return i * self.sample_rate / len(spectrum)
        return 0

##################################
from typing import List
import math

class PerceptualSpectralDivergence(Distance):
    def __init__(self, signal1: List[float], signal2: List[float], sample_rate: int = 44100, frame_size: int = 2048, hop_size: int = 512):
        """
        Initialize the PerceptualSpectralDivergence class with two audio signals.

        :param signal1: First audio signal as a list of float values
        :param signal2: Second audio signal as a list of float values
        :param sample_rate: Sampling rate of the audio signals (default: 44100 Hz)
        :param frame_size: Size of each frame for spectral analysis (default: 2048)
        :param hop_size: Number of samples between successive frames (default: 512)
        """
        super().__init__()

        self.signal1 = signal1
        self.signal2 = signal2
        self.sample_rate = sample_rate
        self.frame_size = frame_size
        self.hop_size = hop_size
        self.mel_filters = self._create_mel_filterbank(num_filters=40, low_freq=0, high_freq=sample_rate/2)

    def calculate_divergence(self) -> float:
        """
        Calculate the Perceptual Spectral Divergence between the two signals.

        :return: Perceptual Spectral Divergence value
        """
        frames1 = self._frame_signal(self.signal1)
        frames2 = self._frame_signal(self.signal2)

        divergence = 0.0
        for frame1, frame2 in zip(frames1, frames2):
            spectrum1 = self._calculate_power_spectrum(frame1)
            spectrum2 = self._calculate_power_spectrum(frame2)
            
            mel_spectrum1 = self._apply_mel_filterbank(spectrum1)
            mel_spectrum2 = self._apply_mel_filterbank(spectrum2)
            
            frame_divergence = self._kullback_leibler_divergence(mel_spectrum1, mel_spectrum2)
            divergence += frame_divergence

        return divergence / len(frames1)

    def _frame_signal(self, signal: List[float]) -> List[List[float]]:
        """
        Divide the signal into overlapping frames.

        :param signal: Input signal
        :return: List of frames
        """
        frames = []
        for i in range(0, len(signal) - self.frame_size + 1, self.hop_size):
            frames.append(signal[i:i+self.frame_size])
        return frames

    def _calculate_power_spectrum(self, frame: List[float]) -> List[float]:
        """
        Calculate the power spectrum of a frame.

        :param frame: Input frame
        :return: Power spectrum
        """
        fft_result = self._fft(frame)
        return [abs(x)**2 for x in fft_result[:len(frame)//2]]

    def _fft(self, x: List[float]) -> List[complex]:
        """
        Cooley-Tukey FFT algorithm.

        :param x: Input signal
        :return: FFT of the signal
        """
        n = len(x)
        if n <= 1:
            return x
        even = self._fft(x[0::2])
        odd = self._fft(x[1::2])
        twiddle_factors = [math.e ** (-2j * math.pi * k / n) for k in range(n//2)]
        return [even[k] + twiddle_factors[k] * odd[k] for k in range(n//2)] + \
               [even[k] - twiddle_factors[k] * odd[k] for k in range(n//2)]

    def _create_mel_filterbank(self, num_filters: int, low_freq: float, high_freq: float) -> List[List[float]]:
        """
        Create a Mel filterbank.

        :param num_filters: Number of Mel filters
        :param low_freq: Lowest frequency to consider
        :param high_freq: Highest frequency to consider
        :return: Mel filterbank
        """
        mel_low = self._hz_to_mel(low_freq)
        mel_high = self._hz_to_mel(high_freq)
        mel_points = [mel_low + i * (mel_high - mel_low) / (num_filters + 1) for i in range(num_filters + 2)]
        hz_points = [self._mel_to_hz(mel) for mel in mel_points]
        bin_indices = [int(round(hz * (self.frame_size / self.sample_rate))) for hz in hz_points]

        filters = [[0.0] * (self.frame_size // 2) for _ in range(num_filters)]
        for i in range(num_filters):
            for j in range(bin_indices[i], bin_indices[i+1]):
                filters[i][j] = (j - bin_indices[i]) / (bin_indices[i+1] - bin_indices[i])
            for j in range(bin_indices[i+1], bin_indices[i+2]):
                filters[i][j] = (bin_indices[i+2] - j) / (bin_indices[i+2] - bin_indices[i+1])
        return filters

    def _apply_mel_filterbank(self, spectrum: List[float]) -> List[float]:
        """
        Apply Mel filterbank to the power spectrum.

        :param spectrum: Power spectrum
        :return: Mel-filtered spectrum
        """
        return [sum(f * s for f, s in zip(filter_bank, spectrum)) for filter_bank in self.mel_filters]

    def _kullback_leibler_divergence(self, p: List[float], q: List[float]) -> float:
        """
        Calculate the Kullback-Leibler divergence between two distributions.

        :param p: First distribution
        :param q: Second distribution
        :return: KL divergence
        """
        return sum(p[i] * math.log(p[i] / q[i]) for i in range(len(p)) if p[i] > 0 and q[i] > 0)

    def _hz_to_mel(self, hz: float) -> float:
        """
        Convert Hz to Mel scale.

        :param hz: Frequency in Hz
        :return: Frequency in Mel scale
        """
        return 2595 * math.log10(1 + hz / 700)

    def _mel_to_hz(self, mel: float) -> float:
        """
        Convert Mel scale to Hz.

        :param mel: Frequency in Mel scale
        :return: Frequency in Hz
        """
        return 700 * (10**(mel / 2595) - 1)

#################################################
from typing import List, Tuple
import math

class PsychoacousticDistance(Distance):
    def __init__(self, signal1: List[float], signal2: List[float], sample_rate: int = 44100, frame_size: int = 2048, hop_size: int = 512):
        """
        Initialize the PsychoacousticDistance class with two audio signals.

        :param signal1: First audio signal as a list of float values
        :param signal2: Second audio signal as a list of float values
        :param sample_rate: Sampling rate of the audio signals (default: 44100 Hz)
        :param frame_size: Size of each frame for spectral analysis (default: 2048)
        :param hop_size: Number of samples between successive frames (default: 512)
        """
        super().__init__()

        self.signal1 = signal1
        self.signal2 = signal2
        self.sample_rate = sample_rate
        self.frame_size = frame_size
        self.hop_size = hop_size
        self.bark_scale = self._create_bark_scale()

    def calculate_distance(self) -> float:
        """
        Calculate the Psychoacoustic Distance between the two signals.

        :return: Psychoacoustic Distance value
        """
        frames1 = self._frame_signal(self.signal1)
        frames2 = self._frame_signal(self.signal2)

        total_distance = 0.0
        for frame1, frame2 in zip(frames1, frames2):
            spectrum1 = self._calculate_power_spectrum(frame1)
            spectrum2 = self._calculate_power_spectrum(frame2)
            
            bark_spectrum1 = self._to_bark_scale(spectrum1)
            bark_spectrum2 = self._to_bark_scale(spectrum2)
            
            masked_diff = self._apply_masking(bark_spectrum1, bark_spectrum2)
            frame_distance = sum(masked_diff)
            total_distance += frame_distance

        return total_distance / len(frames1)

    def _frame_signal(self, signal: List[float]) -> List[List[float]]:
        """
        Divide the signal into overlapping frames.

        :param signal: Input signal
        :return: List of frames
        """
        frames = []
        for i in range(0, len(signal) - self.frame_size + 1, self.hop_size):
            frames.append(signal[i:i+self.frame_size])
        return frames

    def _calculate_power_spectrum(self, frame: List[float]) -> List[float]:
        """
        Calculate the power spectrum of a frame.

        :param frame: Input frame
        :return: Power spectrum
        """
        fft_result = self._fft(frame)
        return [abs(x)**2 for x in fft_result[:len(frame)//2]]

    def _fft(self, x: List[float]) -> List[complex]:
        """
        Cooley-Tukey FFT algorithm.

        :param x: Input signal
        :return: FFT of the signal
        """
        n = len(x)
        if n <= 1:
            return x
        even = self._fft(x[0::2])
        odd = self._fft(x[1::2])
        twiddle_factors = [math.e ** (-2j * math.pi * k / n) for k in range(n//2)]
        return [even[k] + twiddle_factors[k] * odd[k] for k in range(n//2)] + \
               [even[k] - twiddle_factors[k] * odd[k] for k in range(n//2)]

    def _create_bark_scale(self) -> List[Tuple[float, float]]:
        """
        Create Bark scale frequency bands.

        :return: List of tuples representing Bark bands (lower_freq, upper_freq)
        """
        bark_bands = []
        for bark in range(25):  # 25 Bark bands
            lower_freq = 600 * math.sinh(bark / 6)
            upper_freq = 600 * math.sinh((bark + 1) / 6)
            bark_bands.append((lower_freq, upper_freq))
        return bark_bands

    def _to_bark_scale(self, spectrum: List[float]) -> List[float]:
        """
        Convert linear frequency spectrum to Bark scale.

        :param spectrum: Power spectrum
        :return: Bark scale spectrum
        """
        bark_spectrum = [0.0] * len(self.bark_scale)
        for i, (lower, upper) in enumerate(self.bark_scale):
            lower_bin = int(lower * self.frame_size / self.sample_rate)
            upper_bin = int(upper * self.frame_size / self.sample_rate)
            bark_spectrum[i] = sum(spectrum[lower_bin:upper_bin])
        return bark_spectrum

    def _apply_masking(self, spectrum1: List[float], spectrum2: List[float]) -> List[float]:
        """
        Apply a simple masking model to the difference between two spectra.

        :param spectrum1: First Bark scale spectrum
        :param spectrum2: Second Bark scale spectrum
        :return: Masked difference between spectra
        """
        masked_diff = []
        for i in range(len(spectrum1)):
            diff = abs(spectrum1[i] - spectrum2[i])
            mask_threshold = max(spectrum1[i], spectrum2[i]) * 0.1  # Simplified masking threshold
            masked_diff.append(max(0, diff - mask_threshold))
        return masked_diff

####################################
from typing import List, Tuple
import math

class MelFrequencyPerceptualDistance(Distance):
    def __init__(self, sample_rate: int, frame_size: int, hop_length: int):
        """
        Initialize the MelFrequencyPerceptualDistance calculator.

        Args:
            sample_rate (int): The sample rate of the audio.
            frame_size (int): The size of each frame for STFT.
            hop_length (int): The number of samples between successive frames.
        """
        super().__init__()

        self.sample_rate = sample_rate
        self.frame_size = frame_size
        self.hop_length = hop_length

    def mel_scale(self, frequency: float) -> float:
        """
        Convert frequency to mel scale.

        Args:
            frequency (float): The frequency in Hz.

        Returns:
            float: The mel scale value.
        """
        return 2595 * math.log10(1 + frequency / 700)

    def stft(self, signal: List[float]) -> List[List[complex]]:
        """
        Perform Short-Time Fourier Transform (STFT) on the signal.

        Args:
            signal (List[float]): The input audio signal.

        Returns:
            List[List[complex]]: The STFT of the signal.
        """
        stft_result = []
        for i in range(0, len(signal) - self.frame_size, self.hop_length):
            frame = signal[i:i+self.frame_size]
            windowed_frame = [x * 0.54 - 0.46 * math.cos((2 * math.pi * n) / (self.frame_size - 1)) 
                              for n, x in enumerate(frame)]  # Hamming window
            fft_frame = self._fft(windowed_frame)
            stft_result.append(fft_frame)
        return stft_result

    def _fft(self, frame: List[float]) -> List[complex]:
        """
        Perform Fast Fourier Transform (FFT) on a frame.

        Args:
            frame (List[float]): The input frame.

        Returns:
            List[complex]: The FFT of the frame.
        """
        n = len(frame)
        if n <= 1:
            return frame
        even = self._fft(frame[0::2])
        odd = self._fft(frame[1::2])
        combined = [0] * n
        for k in range(n//2):
            t = math.e ** (-2j * math.pi * k / n) * odd[k]
            combined[k] = even[k] + t
            combined[k + n//2] = even[k] - t
        return combined

    def mel_spectrogram(self, stft_result: List[List[complex]]) -> List[List[float]]:
        """
        Convert STFT to mel spectrogram.

        Args:
            stft_result (List[List[complex]]): The STFT of the signal.

        Returns:
            List[List[float]]: The mel spectrogram.
        """
        num_mel_filters = 128
        mel_filters = self._create_mel_filterbank(num_mel_filters)
        
        mel_spec = []
        for frame in stft_result:
            power_spectrum = [abs(x)**2 for x in frame]
            mel_frame = [sum(f * p for f, p in zip(filter_bank, power_spectrum)) 
                         for filter_bank in mel_filters]
            mel_spec.append(mel_frame)
        return mel_spec

    def _create_mel_filterbank(self, num_filters: int) -> List[List[float]]:
        """
        Create a mel filterbank.

        Args:
            num_filters (int): The number of mel filters to create.

        Returns:
            List[List[float]]: The mel filterbank.
        """
        min_freq = 0
        max_freq = self.sample_rate / 2
        min_mel = self.mel_scale(min_freq)
        max_mel = self.mel_scale(max_freq)
        mel_points = [min_mel + i * (max_mel - min_mel) / (num_filters + 1) for i in range(num_filters + 2)]
        hz_points = [700 * (10**(m / 2595) - 1) for m in mel_points]
        
        fft_bins = [int((self.frame_size + 1) * h / self.sample_rate) for h in hz_points]
        
        filters = [[0] * (self.frame_size // 2 + 1) for _ in range(num_filters)]
        for i in range(num_filters):
            for j in range(fft_bins[i], fft_bins[i+1]):
                filters[i][j] = (j - fft_bins[i]) / (fft_bins[i+1] - fft_bins[i])
            for j in range(fft_bins[i+1], fft_bins[i+2]):
                filters[i][j] = (fft_bins[i+2] - j) / (fft_bins[i+2] - fft_bins[i+1])
        return filters

    def calculate_distance(self, sound1: List[float], sound2: List[float]) -> float:
        """
        Calculate the Mel-Frequency Perceptual Distance between two sounds.

        Args:
            sound1 (List[float]): The first sound signal.
            sound2 (List[float]): The second sound signal.

        Returns:
            float: The perceptual distance between the two sounds.
        """
        stft1 = self.stft(sound1)
        stft2 = self.stft(sound2)
        
        mel_spec1 = self.mel_spectrogram(stft1)
        mel_spec2 = self.mel_spectrogram(stft2)
        
        distance = 0
        for frame1, frame2 in zip(mel_spec1, mel_spec2):
            for bin1, bin2 in zip(frame1, frame2):
                distance += (bin1 - bin2) ** 2
        
        return math.sqrt(distance)
###########################################
from typing import List, Tuple, Dict, Optional, Union, BinaryIO, Any
import math
import wave
import array
import os
from collections import deque
import struct

class PLPDistanceCalculator:
    """
    A class to calculate the Perceptual Linear Predictive (PLP) distance between two audio files.
    
    PLP analysis combines aspects of the critical-band spectral resolution, 
    equal-loudness curve, and intensity-loudness power law of human hearing.
    """
    
    def __init__(self, 
                 frame_size: int = 512, 
                 hop_length: int = 256, 
                 num_filters: int = 24,
                 lpc_order: int = 12) -> None:
        """
        Initialize the PLP Distance Calculator.
        
        Args:
            frame_size: Size of each analysis frame in samples (default: 512)
            hop_length: Number of samples between successive frames (default: 256)
            num_filters: Number of auditory filters to use (default: 24)
            lpc_order: Order of Linear Predictive Coding analysis (default: 12)
        """
        self.frame_size = frame_size
        self.hop_length = hop_length
        self.num_filters = num_filters
        self.lpc_order = lpc_order
        
        # Pre-compute critical band filters (bark scale approximation)
        self.filters = self._create_bark_filters()
        
        # Equal loudness curve approximate weights (bark scale)
        self.equal_loudness_weights = self._compute_equal_loudness_weights()

    def _create_bark_filters(self) -> List[List[float]]:
        """
        Create a bank of filters based on the Bark scale.
        
        The Bark scale is a psychoacoustical scale that matches the frequency 
        resolution of human hearing.
        
        Returns:
            A list of filter coefficients for each band
        """
        filters = []
        
        # Approximation of Bark scale frequency mapping
        for i in range(self.num_filters):
            # Create triangular filters spread across frequency range
            # Simplified approximation of Bark scale
            center_freq = 1.0 * (i + 1) / self.num_filters
            filter_width = 1.5 / self.num_filters
            
            # Create triangular filter
            filt = []
            for j in range(self.frame_size // 2):
                norm_freq = 1.0 * j / (self.frame_size // 2)
                
                # Triangular filter response
                if center_freq - filter_width <= norm_freq <= center_freq:
                    response = (norm_freq - (center_freq - filter_width)) / filter_width
                elif center_freq < norm_freq <= center_freq + filter_width:
                    response = 1.0 - (norm_freq - center_freq) / filter_width
                else:
                    response = 0.0
                
                filt.append(response)
                
            filters.append(filt)
            
        return filters
    
    def _compute_equal_loudness_weights(self) -> List[float]:
        """
        Compute approximate equal-loudness weights for auditory filters.
        
        These weights approximate the unequal sensitivity of human hearing
        at different frequencies.
        
        Returns:
            A list of weights for each auditory filter bank
        """
        weights = []
        
        # Simple approximation of equal-loudness contour
        for i in range(self.num_filters):
            # Normalized center frequency of each filter (0 to 1)
            norm_freq = (i + 0.5) / self.num_filters
            
            # Approximate equal-loudness weighting
            # Higher weight in mid-frequencies (most sensitive ~2-5kHz)
            # Lower weight for low and high frequencies
            if norm_freq < 0.2:
                # Low frequencies get reduced weight
                weight = 0.5 + 2.5 * norm_freq
            elif norm_freq > 0.6:
                # High frequencies get reduced weight
                weight = 2.5 - 2.0 * norm_freq
            else:
                # Mid frequencies get emphasized
                weight = 1.0
                
            weights.append(weight)
            
        return weights

    def _read_wav_file(self, file_path: str) -> Tuple[List[float], int]:
        """
        Read audio samples from a WAV file.
        
        Args:
            file_path: Path to the WAV file
            
        Returns:
            A tuple containing:
            - A list of audio samples (normalized to -1.0 to 1.0)
            - The sample rate of the audio file
            
        Raises:
            FileNotFoundError: If the specified file does not exist
            wave.Error: If there's an issue reading the WAV file
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with wave.open(file_path, 'rb') as wav_file:
            sample_rate = wav_file.getframerate()
            num_frames = wav_file.getnframes()
            num_channels = wav_file.getnchannels()
            sample_width = wav_file.getsampwidth()
            
            # Read all frames
            raw_data = wav_file.readframes(num_frames)
            
            # Convert bytes to samples based on sample width
            if sample_width == 1:  # 8-bit samples
                samples = array.array('b', raw_data)
                # Normalize to -1.0 to 1.0
                samples = [s / 128.0 for s in samples]
            elif sample_width == 2:  # 16-bit samples
                samples = array.array('h', raw_data)
                # Normalize to -1.0 to 1.0
                samples = [s / 32768.0 for s in samples]
            elif sample_width == 4:  # 32-bit samples
                # Using struct to unpack 32-bit samples
                samples = []
                for i in range(0, len(raw_data), 4):
                    sample = struct.unpack('<i', raw_data[i:i+4])[0]
                    samples.append(sample / 2147483648.0)  # Normalize to -1.0 to 1.0
            else:
                raise ValueError(f"Unsupported sample width: {sample_width}")
            
            # Convert stereo to mono by averaging channels if needed
            if num_channels == 2:
                mono_samples = []
                for i in range(0, len(samples), 2):
                    if i + 1 < len(samples):
                        mono_samples.append((samples[i] + samples[i+1]) / 2.0)
                    else:
                        mono_samples.append(samples[i])
                samples = mono_samples
                
            return samples, sample_rate

    def _apply_hamming_window(self, frame: List[float]) -> List[float]:
        """
        Apply a Hamming window to a frame of audio samples.
        
        Args:
            frame: A list of audio samples
            
        Returns:
            The windowed frame
        """
        windowed_frame = []
        frame_len = len(frame)
        
        for i in range(frame_len):
            # Hamming window formula: 0.54 - 0.46 * cos(2π * n / (N-1))
            window_val = 0.54 - 0.46 * math.cos(2 * math.pi * i / (frame_len - 1))
            windowed_frame.append(frame[i] * window_val)
            
        return windowed_frame

    def _compute_fft(self, frame: List[float]) -> List[complex]:
        """
        Compute the Fast Fourier Transform of a frame using a simple implementation.
        
        This is a basic recursive implementation for educational purposes.
        In production, you would use a more optimized FFT library.
        
        Args:
            frame: A list of audio samples
            
        Returns:
            The complex FFT coefficients
        """
        n = len(frame)
        
        # Base case
        if n <= 1:
            return frame
        
        # Split into even and odd indices
        even = self._compute_fft([frame[i] for i in range(0, n, 2)])
        odd = self._compute_fft([frame[i] for i in range(1, n, 2)])
        
        # Combine results
        result = [0] * n
        for k in range(n // 2):
            # Complex exponential (twiddle factor)
            angle = -2j * math.pi * k / n
            twiddle = math.cos(angle.imag) + 1j * math.sin(angle.imag)
            
            result[k] = even[k] + twiddle * odd[k]
            result[k + n // 2] = even[k] - twiddle * odd[k]
            
        return result

    def _power_spectrum(self, fft_result: List[complex]) -> List[float]:
        """
        Compute the power spectrum from FFT results.
        
        Args:
            fft_result: Complex FFT coefficients
            
        Returns:
            The power spectrum (magnitude squared)
        """
        # Only use the first half of the symmetric FFT result
        half_len = len(fft_result) // 2
        power = []
        
        for i in range(half_len):
            # Power = magnitude squared
            real = fft_result[i].real
            imag = fft_result[i].imag
            power.append(real * real + imag * imag)
            
        return power

    def _apply_bark_filters(self, power_spectrum: List[float]) -> List[float]:
        """
        Apply the Bark-scale filter bank to the power spectrum.
        
        Args:
            power_spectrum: Power spectrum values
            
        Returns:
            Filter bank energies
        """
        filter_energies = []
        
        for filt in self.filters:
            # Apply filter and sum
            energy = 0.0
            for i in range(min(len(power_spectrum), len(filt))):
                energy += power_spectrum[i] * filt[i]
            
            # Ensure no negative or zero values before log
            energy = max(energy, 1e-10)
            filter_energies.append(energy)
            
        return filter_energies

    def _apply_equal_loudness(self, filter_energies: List[float]) -> List[float]:
        """
        Apply equal-loudness weighting to the filter bank energies.
        
        Args:
            filter_energies: Energies from each filter bank
            
        Returns:
            Weighted filter bank energies
        """
        weighted_energies = []
        
        for i, energy in enumerate(filter_energies):
            if i < len(self.equal_loudness_weights):
                weight = self.equal_loudness_weights[i]
                weighted_energies.append(energy * weight)
            else:
                weighted_energies.append(energy)
                
        return weighted_energies

    def _apply_intensity_loudness_power_law(self, weighted_energies: List[float]) -> List[float]:
        """
        Apply the intensity-loudness power law (cubic root compression).
        
        Args:
            weighted_energies: Weighted filter bank energies
            
        Returns:
            Compressed filter bank energies
        """
        compressed_energies = []
        
        for energy in weighted_energies:
            # Cubic root compression approximates the power law
            compressed_energies.append(math.pow(energy, 0.33))
            
        return compressed_energies

    def _compute_autocorrelation(self, compressed_energies: List[float]) -> List[float]:
        """
        Compute the autocorrelation of the compressed filter bank energies.
        
        Args:
            compressed_energies: Compressed filter bank energies
            
        Returns:
            Autocorrelation coefficients
        """
        n = len(compressed_energies)
        autocorr = []
        
        for lag in range(self.lpc_order + 1):
            sum_val = 0.0
            for i in range(n - lag):
                sum_val += compressed_energies[i] * compressed_energies[i + lag]
            autocorr.append(sum_val)
            
        return autocorr

    def _compute_lpc(self, autocorr: List[float]) -> List[float]:
        """
        Compute Linear Predictive Coding coefficients using the Levinson-Durbin algorithm.
        
        Args:
            autocorr: Autocorrelation coefficients
            
        Returns:
            LPC coefficients
        """
        # Initialize LPC coefficients
        lpc_coeffs = [0.0] * self.lpc_order
        
        if len(autocorr) < 2 or autocorr[0] == 0:
            return lpc_coeffs
        
        # Levinson-Durbin algorithm
        E = autocorr[0]
        reflection_coeffs = []
        
        for i in range(self.lpc_order):
            # Compute reflection coefficient
            k = autocorr[i+1]
            for j in range(i):
                k -= lpc_coeffs[j] * autocorr[i-j]
            k /= E
            
            reflection_coeffs.append(k)
            
            # Update LPC coefficients
            new_coeffs = lpc_coeffs.copy()
            lpc_coeffs[i] = k
            for j in range(i):
                new_coeffs[j] = lpc_coeffs[j] - k * lpc_coeffs[i-j-1]
            
            lpc_coeffs = new_coeffs
            
            # Update error
            E *= (1 - k*k)
            
        return lpc_coeffs

    def _compute_cepstral_coefs(self, lpc_coeffs: List[float], num_ceps: int = 12) -> List[float]:
        """
        Convert LPC coefficients to cepstral coefficients.
        
        Args:
            lpc_coeffs: LPC coefficients
            num_ceps: Number of cepstral coefficients to compute
            
        Returns:
            Cepstral coefficients
        """
        ceps = [0.0] * num_ceps
        
        for n in range(num_ceps):
            if n < len(lpc_coeffs):
                ceps[n] = lpc_coeffs[n]
                
                for k in range(n):
                    if n-k-1 < len(lpc_coeffs) and k < len(ceps):
                        ceps[n] += (k+1) / (n+1) * lpc_coeffs[n-k-1] * ceps[k]
            
        return ceps

    def compute_plp_features(self, audio_samples: List[float]) -> List[List[float]]:
        """
        Compute PLP features for audio samples.
        
        Args:
            audio_samples: List of audio samples
            
        Returns:
            List of PLP feature vectors for each frame
        """
        features = []
        
        # Process the audio in frames
        for frame_start in range(0, len(audio_samples) - self.frame_size, self.hop_length):
            # Extract frame
            frame = audio_samples[frame_start:frame_start + self.frame_size]
            
            # Apply windowing
            windowed_frame = self._apply_hamming_window(frame)
            
            # Compute FFT
            fft_result = self._compute_fft(windowed_frame)
            
            # Compute power spectrum
            power = self._power_spectrum(fft_result)
            
            # Apply Bark filters
            filter_energies = self._apply_bark_filters(power)
            
            # Apply equal-loudness curve
            weighted_energies = self._apply_equal_loudness(filter_energies)
            
            # Apply intensity-loudness power law
            compressed_energies = self._apply_intensity_loudness_power_law(weighted_energies)
            
            # Compute autocorrelation
            autocorr = self._compute_autocorrelation(compressed_energies)
            
            # Compute LPC coefficients
            lpc_coeffs = self._compute_lpc(autocorr)
            
            # Convert to cepstral coefficients
            ceps = self._compute_cepstral_coefs(lpc_coeffs)
            
            features.append(ceps)
            
        return features

    def compute_plp_distance(self, file_path1: str, file_path2: str) -> Tuple[float, Dict[str, Any]]:
        """
        Compute the PLP distance between two audio files.
        
        Args:
            file_path1: Path to the first audio file
            file_path2: Path to the second audio file
            
        Returns:
            A tuple containing:
            - A float representing the distance (lower means more similar)
            - A dictionary with detailed metrics
            
        Raises:
            FileNotFoundError: If either specified file does not exist
            wave.Error: If there's an issue reading the WAV files
        """
        # Read audio files
        audio1, sr1 = self._read_wav_file(file_path1)
        audio2, sr2 = self._read_wav_file(file_path2)
        
        # Compute PLP features
        plp_features1 = self.compute_plp_features(audio1)
        plp_features2 = self.compute_plp_features(audio2)
        
        # Dynamic Time Warping to align features
        distance, path = self._dynamic_time_warping(plp_features1, plp_features2)
        
        # Normalize distance by path length
        path_length = len(path)
        normalized_distance = distance / path_length if path_length > 0 else float('inf')
        
        # Calculate additional metrics
        metrics = {
            "raw_distance": distance,
            "path_length": path_length,
            "normalized_distance": normalized_distance,
            "alignment_path": path,
            "num_frames1": len(plp_features1),
            "num_frames2": len(plp_features2)
        }
        
        return normalized_distance, metrics

    def _dynamic_time_warping(self, features1: List[List[float]], features2: List[List[float]]) -> Tuple[float, List[Tuple[int, int]]]:
        """
        Align two sequences of feature vectors using Dynamic Time Warping.
        
        Args:
            features1: PLP features for the first audio file
            features2: PLP features for the second audio file
            
        Returns:
            A tuple containing:
            - The minimum distance between sequences
            - The optimal path as a list of (i,j) index tuples
        """
        n = len(features1)
        m = len(features2)
        
        if n == 0 or m == 0:
            return float('inf'), []
        
        # Initialize distance matrix
        dtw_matrix = [[float('inf') for _ in range(m + 1)] for _ in range(n + 1)]
        dtw_matrix[0][0] = 0
        
        # Fill the DTW matrix
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                cost = self._euclidean_distance(features1[i-1], features2[j-1])
                dtw_matrix[i][j] = cost + min(
                    dtw_matrix[i-1][j],      # insertion
                    dtw_matrix[i][j-1],      # deletion
                    dtw_matrix[i-1][j-1]     # match
                )
        
        # Trace back to find the optimal path
        path = []
        i, j = n, m
        
        while i > 0 and j > 0:
            path.append((i-1, j-1))
            
            # Find the next cell (moving backward)
            min_val = min(
                dtw_matrix[i-1][j],
                dtw_matrix[i][j-1],
                dtw_matrix[i-1][j-1]
            )
            
            if min_val == dtw_matrix[i-1][j-1]:
                i -= 1
                j -= 1
            elif min_val == dtw_matrix[i-1][j]:
                i -= 1
            else:
                j -= 1
                
        # Reverse path to get the correct order
        path.reverse()
        
        return dtw_matrix[n][m], path

    def _euclidean_distance(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Compute the Euclidean distance between two vectors.
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            The Euclidean distance
        """
        # Handle vectors of different lengths
        min_len = min(len(vec1), len(vec2))
        sum_squared_diff = 0.0
        
        for i in range(min_len):
            diff = vec1[i] - vec2[i]
            sum_squared_diff += diff * diff
            
        # Add penalty for length difference
        len_diff = abs(len(vec1) - len(vec2))
        if len_diff > 0:
            sum_squared_diff += len_diff * 0.5
            
        return math.sqrt(sum_squared_diff)

    def get_formatted_result(self, file_path1: str, file_path2: str) -> str:
        """
        Get a formatted string describing the PLP distance result.
        
        Args:
            file_path1: Path to the first audio file
            file_path2: Path to the second audio file
            
        Returns:
            A formatted string describing the results of the PLP comparison
        """
        try:
            distance, metrics = self.compute_plp_distance(file_path1, file_path2)
            
            similarity = math.exp(-distance)  # Convert distance to similarity (0-1)
            
            result = (f"PLP Distance Analysis:\n"
                     f"  - Distance: {distance:.4f}\n"
                     f"  - Similarity: {similarity:.4f} ({similarity * 100:.2f}%)\n"
                     f"  - File 1: {os.path.basename(file_path1)} ({metrics['num_frames1']} frames)\n"
                     f"  - File 2: {os.path.basename(file_path2)} ({metrics['num_frames2']} frames)\n"
                     f"  - Alignment path length: {metrics['path_length']}")
            
            return result
            
        except Exception as e:
            return f"Error comparing audio files: {str(e)}"
#########################################

import numpy as np
from typing import List

class ChordSimilarityDistance(Distance):
    def __init__(self):
        # Définition des 12 classes de hauteur (pitch classes)
        super().__init__()

        self.pitch_classes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    def _chord_to_vector(self, chord: List[str]) -> np.ndarray:
        """Convertit un accord en vecteur binaire de 12 dimensions."""
        vector = np.zeros(12)
        for note in chord:
            index = self.pitch_classes.index(note)
            vector[index] = 1
        return vector

    def calculate_distance(self, chord1: List[str], chord2: List[str]) -> float:
        """
        Calcule la distance de similarité entre deux accords.

        Args:
            chord1 (List[str]): Premier accord (liste de noms de notes).
            chord2 (List[str]): Deuxième accord (liste de noms de notes).

        Returns:
            float: Distance de similarité entre les deux accords.
        """
        vector1 = self._chord_to_vector(chord1)
        vector2 = self._chord_to_vector(chord2)
        
        # Calcul de la distance cosinus
        similarity = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
        distance = 1 - similarity
        
        return distance
#######################################
import re
from typing import List

class SpeechRecognitionErrorRate(Distance):
    def __init__(self):
        super().__init__()


    def _preprocess(self, text: str) -> List[str]:
        """Prétraite le texte en le convertissant en minuscules et en le divisant en mots."""
        return re.findall(r'\w+', text.lower())

    def calculate_wer(self, reference: str, hypothesis: str) -> float:
        """
        Calcule le taux d'erreur de mots (WER) entre la référence et l'hypothèse.

        Args:
            reference (str): La transcription de référence.
            hypothesis (str): La transcription hypothétique générée par le système de reconnaissance vocale.

        Returns:
            float: Le taux d'erreur de mots (WER).
        """
        ref_words = self._preprocess(reference)
        hyp_words = self._preprocess(hypothesis)

        # Calcul de la distance de Levenshtein au niveau des mots
        d = [[0] * (len(hyp_words) + 1) for _ in range(len(ref_words) + 1)]

        for i in range(len(ref_words) + 1):
            d[i][0] = i
        for j in range(len(hyp_words) + 1):
            d[0][j] = j

        for i in range(1, len(ref_words) + 1):
            for j in range(1, len(hyp_words) + 1):
                if ref_words[i-1] == hyp_words[j-1]:
                    d[i][j] = d[i-1][j-1]
                else:
                    substitution = d[i-1][j-1] + 1
                    insertion = d[i][j-1] + 1
                    deletion = d[i-1][j] + 1
                    d[i][j] = min(substitution, insertion, deletion)

        return d[len(ref_words)][len(hyp_words)] / len(ref_words)

##########################################
from typing import List, Tuple, Dict, Optional, Union, BinaryIO, Any
import math
import wave
import array
import os
import struct
from collections import defaultdict

class EnvironmentalSoundMatchingDistance:
    """
    A class to calculate the similarity/distance between environmental sound recordings.
    
    This implementation uses a combination of spectral-temporal features and
    pattern matching techniques specifically designed for environmental sound
    classification. It works with WAV files and provides multiple distance metrics
    tailored for environmental sound recognition.
    
    The analysis focuses on capturing characteristics that distinguish environmental
    sounds such as texture, onset patterns, spectral distribution, and energy contours.
    """
    
    def __init__(self, 
                 frame_size: int = 1024, 
                 hop_length: int = 512, 
                 num_bands: int = 24,
                 num_temporal_bins: int = 20,
                 feature_selection: List[str] = None) -> None:
        """
        Initialize the Environmental Sound Matching Distance calculator.
        
        Args:
            frame_size: Size of each analysis frame in samples (default: 1024)
            hop_length: Number of samples between successive frames (default: 512)
            num_bands: Number of frequency bands for spectral analysis (default: 24)
            num_temporal_bins: Number of bins for temporal statistics (default: 20)
            feature_selection: List of features to extract (default: all features)
                Options include: 'spectral_centroid', 'spectral_flatness', 
                'spectral_contrast', 'temporal_envelope', 'onset_density',
                'spectral_flux', 'band_energy_ratio'
        """
        self.frame_size = frame_size
        self.hop_length = hop_length
        self.num_bands = num_bands
        self.num_temporal_bins = num_temporal_bins
        
        # Set default feature selection if none provided
        if feature_selection is None:
            self.feature_selection = [
                'spectral_centroid', 
                'spectral_flatness',
                'temporal_envelope', 
                'onset_density',
                'spectral_flux', 
                'band_energy_ratio'
            ]
        else:
            self.feature_selection = feature_selection
            
        # Create Mel-like frequency band boundaries
        self.band_edges = self._create_mel_bands()
        
        # Feature weights (can be adjusted for different environmental sound types)
        self.feature_weights = {
            'spectral_centroid': 1.0,
            'spectral_flatness': 1.2,
            'temporal_envelope': 1.5,
            'onset_density': 2.0,
            'spectral_flux': 1.8,
            'band_energy_ratio': 1.3
        }

    def _create_mel_bands(self) -> List[Tuple[int, int]]:
        """
        Create Mel-scale inspired frequency bands.
        
        Returns:
            A list of tuples representing (lower_bin, upper_bin) for each band
        """
        # We're approximating Mel bands with a simpler approach
        # that emphasizes lower frequencies more than higher ones
        bands = []
        
        # Use a logarithmic distribution for band edges
        max_bin = self.frame_size // 2
        
        for i in range(self.num_bands):
            # Logarithmic spacing
            low_factor = math.pow(max_bin, i / self.num_bands)
            high_factor = math.pow(max_bin, (i + 1) / self.num_bands)
            
            low_bin = int(low_factor)
            high_bin = int(high_factor)
            
            # Ensure we have at least 1 bin width
            if high_bin <= low_bin:
                high_bin = low_bin + 1
                
            # Make sure we don't exceed the maximum bin
            high_bin = min(high_bin, max_bin)
            
            bands.append((low_bin, high_bin))
            
        return bands

    def _read_wav_file(self, file_path: str) -> Tuple[List[float], int]:
        """
        Read audio samples from a WAV file.
        
        Args:
            file_path: Path to the WAV file
            
        Returns:
            A tuple containing:
            - A list of audio samples (normalized to -1.0 to 1.0)
            - The sample rate of the audio file
            
        Raises:
            FileNotFoundError: If the specified file does not exist
            wave.Error: If there's an issue reading the WAV file
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with wave.open(file_path, 'rb') as wav_file:
            sample_rate = wav_file.getframerate()
            num_frames = wav_file.getnframes()
            num_channels = wav_file.getnchannels()
            sample_width = wav_file.getsampwidth()
            
            # Read all frames
            raw_data = wav_file.readframes(num_frames)
            
            # Convert bytes to samples based on sample width
            if sample_width == 1:  # 8-bit samples
                samples = array.array('b', raw_data)
                # Normalize to -1.0 to 1.0
                samples = [s / 128.0 for s in samples]
            elif sample_width == 2:  # 16-bit samples
                samples = array.array('h', raw_data)
                # Normalize to -1.0 to 1.0
                samples = [s / 32768.0 for s in samples]
            elif sample_width == 4:  # 32-bit samples
                # Using struct to unpack 32-bit samples
                samples = []
                for i in range(0, len(raw_data), 4):
                    sample = struct.unpack('<i', raw_data[i:i+4])[0]
                    samples.append(sample / 2147483648.0)  # Normalize to -1.0 to 1.0
            else:
                raise ValueError(f"Unsupported sample width: {sample_width}")
            
            # Convert stereo to mono by averaging channels if needed
            if num_channels == 2:
                mono_samples = []
                for i in range(0, len(samples), 2):
                    if i + 1 < len(samples):
                        mono_samples.append((samples[i] + samples[i+1]) / 2.0)
                    else:
                        mono_samples.append(samples[i])
                samples = mono_samples
                
            return samples, sample_rate

    def _apply_window(self, frame: List[float]) -> List[float]:
        """
        Apply a Hann window to a frame of audio samples.
        
        The Hann window helps reduce spectral leakage when computing the FFT.
        
        Args:
            frame: A list of audio samples
            
        Returns:
            The windowed frame
        """
        windowed_frame = []
        frame_len = len(frame)
        
        for i in range(frame_len):
            # Hann window formula: 0.5 * (1 - cos(2π * n / (N-1)))
            window_val = 0.5 * (1.0 - math.cos(2.0 * math.pi * i / (frame_len - 1)))
            windowed_frame.append(frame[i] * window_val)
            
        return windowed_frame

    def _compute_fft(self, frame: List[float]) -> List[complex]:
        """
        Compute the Fast Fourier Transform of a frame.
        
        This implementation uses the Cooley-Tukey FFT algorithm.
        
        Args:
            frame: A list of audio samples
            
        Returns:
            The complex FFT coefficients
        """
        n = len(frame)
        
        # Ensure n is a power of 2 for FFT
        if n & (n - 1) != 0:
            # Pad with zeros if not a power of 2
            next_pow2 = 2 ** (n - 1).bit_length()
            frame = frame + [0.0] * (next_pow2 - n)
            n = next_pow2
            
        # Base case
        if n <= 1:
            return frame
        
        # Divide
        even = self._compute_fft(frame[0::2])
        odd = self._compute_fft(frame[1::2])
        
        # Combine
        result = [0] * n
        for k in range(n // 2):
            angle = -2j * math.pi * k / n
            twiddle = complex(math.cos(angle.imag), math.sin(angle.imag))
            
            result[k] = even[k] + twiddle * odd[k]
            result[k + n // 2] = even[k] - twiddle * odd[k]
            
        return result

    def _power_spectrum(self, fft_result: List[complex]) -> List[float]:
        """
        Compute the power spectrum from FFT results.
        
        Args:
            fft_result: Complex FFT coefficients
            
        Returns:
            The power spectrum (magnitude squared)
        """
        # Only use the first half of the symmetric FFT result
        half_len = len(fft_result) // 2
        power = []
        
        for i in range(half_len):
            # Power = magnitude squared
            real = fft_result[i].real
            imag = fft_result[i].imag
            power.append(real * real + imag * imag)
            
        return power

    def _compute_band_energies(self, power_spectrum: List[float]) -> List[float]:
        """
        Compute energy in each frequency band.
        
        Args:
            power_spectrum: Power spectrum values
            
        Returns:
            A list of energy values for each frequency band
        """
        band_energies = []
        
        for low_bin, high_bin in self.band_edges:
            # Sum energy in this band
            energy = sum(power_spectrum[low_bin:high_bin]) if low_bin < len(power_spectrum) else 0
            
            # Avoid log(0) issues
            energy = max(energy, 1e-10)
            
            band_energies.append(energy)
            
        return band_energies

    def _compute_spectral_centroid(self, power_spectrum: List[float]) -> float:
        """
        Compute the spectral centroid (center of mass of the spectrum).
        
        Args:
            power_spectrum: Power spectrum values
            
        Returns:
            The spectral centroid as a normalized value between 0 and 1
        """
        total_energy = sum(power_spectrum)
        
        if total_energy <= 0:
            return 0.0
        
        weighted_sum = sum(freq * energy for freq, energy in enumerate(power_spectrum))
        
        # Normalize by spectrum length to get value between 0-1
        return weighted_sum / (total_energy * len(power_spectrum))

    def _compute_spectral_flatness(self, band_energies: List[float]) -> float:
        """
        Compute spectral flatness (ratio of geometric mean to arithmetic mean).
        
        This is a measure of how noise-like (flat) vs. tone-like (peaked) a sound is.
        
        Args:
            band_energies: Energy values for each frequency band
            
        Returns:
            The spectral flatness as a value between 0 and 1
        """
        # Avoid log of negative/zero
        filtered_energies = [e for e in band_energies if e > 0]
        
        if not filtered_energies:
            return 0.0
        
        n = len(filtered_energies)
        
        # Geometric mean
        log_sum = sum(math.log(e) for e in filtered_energies)
        geometric_mean = math.exp(log_sum / n)
        
        # Arithmetic mean
        arithmetic_mean = sum(filtered_energies) / n
        
        if arithmetic_mean <= 0:
            return 0.0
            
        # Spectral flatness
        flatness = geometric_mean / arithmetic_mean
        
        return flatness

    def _detect_onsets(self, frames_energy: List[float], threshold_factor: float = 1.5) -> List[int]:
        """
        Detect onset positions in the audio signal.
        
        Args:
            frames_energy: Energy values for each frame
            threshold_factor: Factor to determine onset threshold
            
        Returns:
            A list of indices where onsets were detected
        """
        onsets = []
        
        if len(frames_energy) < 3:
            return onsets
        
        # Compute energy derivative
        energy_diff = [frames_energy[i] - frames_energy[i-1] for i in range(1, len(frames_energy))]
        
        # Adaptive threshold based on median energy change
        median_diff = sorted(energy_diff)[len(energy_diff) // 2]
        threshold = median_diff * threshold_factor
        
        # Detect positive energy changes above threshold
        for i in range(1, len(energy_diff)):
            if energy_diff[i-1] > threshold and energy_diff[i-1] > energy_diff[i]:
                onsets.append(i)
                
        return onsets

    def _compute_onset_density(self, onsets: List[int], num_frames: int) -> float:
        """
        Compute the onset density (number of onsets normalized by signal length).
        
        Args:
            onsets: List of onset positions
            num_frames: Total number of frames
            
        Returns:
            Onset density as a value typically between 0 and 1
        """
        if num_frames <= 1:
            return 0.0
            
        # Normalize by number of frames to get a value between 0-1
        # Multiply by a scaling factor to get more meaningful values
        scaling = 5.0  # Adjust based on typical environmental sounds
        density = min(1.0, len(onsets) / num_frames * scaling)
        
        return density

    def _compute_spectral_flux(self, power_spectra: List[List[float]]) -> List[float]:
        """
        Compute spectral flux between consecutive frames.
        
        Spectral flux measures how quickly the power spectrum changes over time.
        
        Args:
            power_spectra: List of power spectra for each frame
            
        Returns:
            A list of spectral flux values
        """
        flux = []
        
        for i in range(1, len(power_spectra)):
            # Sum of squared differences
            frame_flux = 0.0
            for j in range(min(len(power_spectra[i]), len(power_spectra[i-1]))):
                # Use half-wave rectification (only positive changes)
                diff = power_spectra[i][j] - power_spectra[i-1][j]
                frame_flux += max(0, diff) ** 2
                
            # Normalize by spectrum size
            if len(power_spectra[i]) > 0:
                frame_flux = math.sqrt(frame_flux) / len(power_spectra[i])
                
            flux.append(frame_flux)
            
        if not flux and power_spectra:
            # If only one frame, return zero flux
            flux = [0.0]
            
        return flux

    def _compute_band_energy_ratio(self, band_energies: List[float]) -> float:
        """
        Compute the ratio of low frequency energy to high frequency energy.
        
        This feature distinguishes sounds with more low-frequency content
        from those with more high-frequency content.
        
        Args:
            band_energies: Energy values for each frequency band
            
        Returns:
            Band energy ratio as a value typically between 0 and 1
        """
        if not band_energies:
            return 0.5  # Default to middle value
            
        # Split into low and high bands
        mid_point = len(band_energies) // 2
        
        low_energy = sum(band_energies[:mid_point])
        high_energy = sum(band_energies[mid_point:])
        
        total_energy = low_energy + high_energy
        
        if total_energy <= 0:
            return 0.5
            
        # Ratio of low to total energy (0-1 range)
        ratio = low_energy / total_energy
        
        return ratio

    def _compute_temporal_envelope(self, frames_energy: List[float]) -> List[float]:
        """
        Compute a simplified temporal envelope representation.
        
        Args:
            frames_energy: Energy values for each frame
            
        Returns:
            Normalized temporal envelope binned into fixed segments
        """
        if not frames_energy:
            return [0.0] * self.num_temporal_bins
            
        # Normalize energy values
        max_energy = max(frames_energy)
        if max_energy <= 0:
            return [0.0] * self.num_temporal_bins
            
        norm_energy = [e / max_energy for e in frames_energy]
        
        # Bin into temporal segments
        temporal_bins = [0.0] * self.num_temporal_bins
        
        for i, energy in enumerate(norm_energy):
            bin_idx = min(int(i * self.num_temporal_bins / len(norm_energy)), self.num_temporal_bins - 1)
            temporal_bins[bin_idx] = max(temporal_bins[bin_idx], energy)
            
        return temporal_bins

    def _extract_features(self, audio_samples: List[float]) -> Dict[str, Any]:
        """
        Extract audio features for environmental sound matching.
        
        Args:
            audio_samples: List of audio samples
            
        Returns:
            A dictionary of extracted features
        """
        # Initialize feature containers
        frames = []
        frames_energy = []
        power_spectra = []
        band_energies_list = []
        spectral_centroids = []
        spectral_flatness_list = []
        
        # Process the audio in frames
        for frame_start in range(0, len(audio_samples) - self.frame_size + 1, self.hop_length):
            # Extract frame
            if frame_start + self.frame_size <= len(audio_samples):
                frame = audio_samples[frame_start:frame_start + self.frame_size]
                
                # Apply windowing
                windowed_frame = self._apply_window(frame)
                frames.append(windowed_frame)
                
                # Compute frame energy
                frame_energy = sum(s*s for s in frame) / len(frame)
                frames_energy.append(frame_energy)
                
                # Compute FFT and power spectrum
                fft_result = self._compute_fft(windowed_frame)
                power_spectrum = self._power_spectrum(fft_result)
                power_spectra.append(power_spectrum)
                
                # Compute band energies
                band_energies = self._compute_band_energies(power_spectrum)
                band_energies_list.append(band_energies)
                
                # Compute spectral centroid if selected
                if 'spectral_centroid' in self.feature_selection:
                    centroid = self._compute_spectral_centroid(power_spectrum)
                    spectral_centroids.append(centroid)
                    
                # Compute spectral flatness if selected
                if 'spectral_flatness' in self.feature_selection:
                    flatness = self._compute_spectral_flatness(band_energies)
                    spectral_flatness_list.append(flatness)
        
        # Feature dictionary to store all extracted features
        features = {}
        
        # Calculate onset-related features if selected
        if 'onset_density' in self.feature_selection:
            onsets = self._detect_onsets(frames_energy)
            features['onset_density'] = self._compute_onset_density(onsets, len(frames))
            
        # Calculate spectral flux if selected
        if 'spectral_flux' in self.feature_selection:
            flux = self._compute_spectral_flux(power_spectra)
            features['spectral_flux_mean'] = sum(flux) / len(flux) if flux else 0.0
            features['spectral_flux_std'] = math.sqrt(sum((f - features['spectral_flux_mean'])**2 for f in flux) / len(flux)) if flux else 0.0
            
        # Calculate band energy ratio if selected
        if 'band_energy_ratio' in self.feature_selection:
            # Average band energies across frames
            avg_band_energies = []
            for i in range(self.num_bands):
                band_sum = sum(frame_bands[i] for frame_bands in band_energies_list if i < len(frame_bands))
                if band_energies_list:
                    avg_band_energies.append(band_sum / len(band_energies_list))
                else:
                    avg_band_energies.append(0.0)
                    
            features['band_energy_ratio'] = self._compute_band_energy_ratio(avg_band_energies)
            
        # Store spectral centroid statistics if calculated
        if spectral_centroids:
            features['spectral_centroid_mean'] = sum(spectral_centroids) / len(spectral_centroids)
            features['spectral_centroid_std'] = math.sqrt(sum((c - features['spectral_centroid_mean'])**2 for c in spectral_centroids) / len(spectral_centroids))
            
        # Store spectral flatness statistics if calculated
        if spectral_flatness_list:
            features['spectral_flatness_mean'] = sum(spectral_flatness_list) / len(spectral_flatness_list)
            features['spectral_flatness_std'] = math.sqrt(sum((f - features['spectral_flatness_mean'])**2 for f in spectral_flatness_list) / len(spectral_flatness_list))
            
        # Compute temporal envelope if selected
        if 'temporal_envelope' in self.feature_selection:
            features['temporal_envelope'] = self._compute_temporal_envelope(frames_energy)
            
        return features

    def compute_distance(self, file_path1: str, file_path2: str) -> Tuple[float, Dict[str, Any]]:
        """
        Compute the distance between two environmental sound files.
        
        Args:
            file_path1: Path to the first audio file
            file_path2: Path to the second audio file
            
        Returns:
            A tuple containing:
            - A float representing the distance (lower means more similar)
            - A dictionary with detailed metrics for each feature
            
        Raises:
            FileNotFoundError: If either specified file does not exist
            wave.Error: If there's an issue reading the WAV files
        """
        # Read audio files
        audio1, sr1 = self._read_wav_file(file_path1)
        audio2, sr2 = self._read_wav_file(file_path2)
        
        # Extract features
        features1 = self._extract_features(audio1)
        features2 = self._extract_features(audio2)
        
        # Calculate distances for each feature
        feature_distances = {}
        
        # Weighted sum of all distances
        weighted_distance_sum = 0.0
        weight_sum = 0.0
        
        # Compare spectral centroid if available
        if 'spectral_centroid_mean' in features1 and 'spectral_centroid_mean' in features2:
            centroid_dist = abs(features1['spectral_centroid_mean'] - features2['spectral_centroid_mean'])
            feature_distances['spectral_centroid'] = centroid_dist
            
            # Add to weighted sum
            weight = self.feature_weights.get('spectral_centroid', 1.0)
            weighted_distance_sum += centroid_dist * weight
            weight_sum += weight
            
        # Compare spectral flatness if available
        if 'spectral_flatness_mean' in features1 and 'spectral_flatness_mean' in features2:
            flatness_dist = abs(features1['spectral_flatness_mean'] - features2['spectral_flatness_mean'])
            feature_distances['spectral_flatness'] = flatness_dist
            
            # Add to weighted sum
            weight = self.feature_weights.get('spectral_flatness', 1.0)
            weighted_distance_sum += flatness_dist * weight
            weight_sum += weight
            
        # Compare temporal envelope if available
        if 'temporal_envelope' in features1 and 'temporal_envelope' in features2:
            env1 = features1['temporal_envelope']
            env2 = features2['temporal_envelope']
            
            # Calculate Euclidean distance between envelopes
            sum_squared = sum((e1 - e2)**2 for e1, e2 in zip(env1, env2[:len(env1)])) if env1 else 0
            envelope_dist = math.sqrt(sum_squared)
            feature_distances['temporal_envelope'] = envelope_dist
            
            # Add to weighted sum (normalize by maximum possible distance)
            normalized_dist = envelope_dist / math.sqrt(self.num_temporal_bins)
            weight = self.feature_weights.get('temporal_envelope', 1.0)
            weighted_distance_sum += normalized_dist * weight
            weight_sum += weight
            
        # Compare onset density if available
        if 'onset_density' in features1 and 'onset_density' in features2:
            onset_dist = abs(features1['onset_density'] - features2['onset_density'])
            feature_distances['onset_density'] = onset_dist
            
            # Add to weighted sum
            weight = self.feature_weights.get('onset_density', 1.0)
            weighted_distance_sum += onset_dist * weight
            weight_sum += weight
            
        # Compare spectral flux if available
        if 'spectral_flux_mean' in features1 and 'spectral_flux_mean' in features2:
            flux_dist = abs(features1['spectral_flux_mean'] - features2['spectral_flux_mean'])
            feature_distances['spectral_flux'] = flux_dist
            
            # Add to weighted sum
            weight = self.feature_weights.get('spectral_flux', 1.0)
            weighted_distance_sum += flux_dist * weight
            weight_sum += weight
            
        # Compare band energy ratio if available
        if 'band_energy_ratio' in features1 and 'band_energy_ratio' in features2:
            band_ratio_dist = abs(features1['band_energy_ratio'] - features2['band_energy_ratio'])
            feature_distances['band_energy_ratio'] = band_ratio_dist
            
            # Add to weighted sum
            weight = self.feature_weights.get('band_energy_ratio', 1.0)
            weighted_distance_sum += band_ratio_dist * weight
            weight_sum += weight
            
        # Calculate overall distance (normalized by weights)
        overall_distance = weighted_distance_sum / weight_sum if weight_sum > 0 else 0.0
        
        # Assemble metrics
        metrics = {
            "feature_distances": feature_distances,
            "overall_distance": overall_distance,
            "similarity": math.exp(-2 * overall_distance)  # Convert distance to similarity score (0-1)
        }
        
        return overall_distance, metrics

    def get_formatted_result(self, file_path1: str, file_path2: str) -> str:
        """
        Get a formatted string describing the environmental sound distance result.
        
        Args:
            file_path1: Path to the first audio file
            file_path2: Path to the second audio file
            
        Returns:
            A formatted string describing the results of the comparison
        """
        try:
            distance, metrics = self.compute_distance(file_path1, file_path2)
            similarity = metrics["similarity"]
            
            # Format the result string
            result = (f"Environmental Sound Matching Analysis:\n"
                     f"  - Overall Distance: {distance:.4f}\n"
                     f"  - Similarity: {similarity:.4f} ({similarity * 100:.2f}%)\n"
                     f"  - Files: {os.path.basename(file_path1)} and {os.path.basename(file_path2)}\n\n"
                     f"Feature-specific distances:")
            
            # Add feature-specific distances
            for feature, feature_dist in metrics["feature_distances"].items():
                result += f"\n  - {feature}: {feature_dist:.4f}"
                
            # Add sound classification hint if high similarity
            if similarity > 0.8:
                result += "\n\nClassification: Sounds likely belong to the same environmental category"
            elif similarity > 0.5:
                result += "\n\nClassification: Sounds share some environmental characteristics"
            else:
                result += "\n\nClassification: Sounds likely belong to different environmental categories"
            
            return result
            
        except Exception as e:
            return f"Error comparing audio files: {str(e)}"

    def classify_sound(self, file_path: str, reference_files: Dict[str, str]) -> Tuple[str, float]:
        """
        Classify an environmental sound by comparing it to reference sounds.
        
        Args:
            file_path: Path to the audio file to classify
            reference_files: Dictionary mapping category names to reference file paths
            
        Returns:
            A tuple containing:
            - The best matching category name
            - The similarity score for that category
            
        Raises:
            FileNotFoundError: If any specified file does not exist
            wave.Error: If there's an issue reading the WAV files
        """
        best_match = None
        best_similarity = -1.0
        
        for category, ref_path in reference_files.items():
            try:
                _, metrics = self.compute_distance(file_path, ref_path)
                similarity = metrics["similarity"]
                
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match = category
            except Exception as e:
                print(f"Error comparing with reference '{category}': {str(e)}")
                
        if best_match is None:
            return "Unknown", 0.0
            
        return best_match, best_similarity
###############################################
import zlib
from typing import List

class ZlibCompressionDistance(Distance):
    def __init__(self):
        """
        Initialize the ZlibCompressionDistance class.
        """
        super().__init__()

    def _compress(self, data: bytes) -> int:
        """
        Compress data using zlib and return the compressed size.

        Args:
            data (bytes): The input data to compress.

        Returns:
            int: The size of the compressed data.
        """
        compressed_data = zlib.compress(data)
        return len(compressed_data)

    def calculate_distance(self, signal1: List[float], signal2: List[float]) -> float:
        """
        Calculate the Zlib Compression Distance between two audio signals.

        Args:
            signal1 (List[float]): The first audio signal.
            signal2 (List[float]): The second audio signal.

        Returns:
            float: The compression-based distance between the two signals.
        """
        # Convert signals to bytes
        signal1_bytes = bytes(int(x * 255) for x in signal1)  # Normalize to 0-255 and convert to bytes
        signal2_bytes = bytes(int(x * 255) for x in signal2)

        # Compress individual signals
        c_signal1 = self._compress(signal1_bytes)
        c_signal2 = self._compress(signal2_bytes)

        # Concatenate and compress combined signals
        concatenated_bytes = signal1_bytes + signal2_bytes
        c_concatenated = self._compress(concatenated_bytes)

        # Calculate the Zlib Compression Distance
        distance = (c_concatenated - min(c_signal1, c_signal2)) / max(c_signal1, c_signal2)
        
        return distance
##############################################

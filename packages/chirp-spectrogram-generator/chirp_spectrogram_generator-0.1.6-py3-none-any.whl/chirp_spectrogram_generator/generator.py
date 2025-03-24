import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
from scipy.ndimage import gaussian_filter

class SpectrogramGenerator:
    def __init__(self, sample_rate=5000, duration=60.0, max_chirp_duration=15.0, num_time_bins=128, num_freq_bins=128,
                 max_frequency=100, max_chirp_band=30, output_dir="output", labels_file="labels.csv"):
        self.sample_rate = sample_rate
        self.duration = duration
        self.max_chirp_duration = max_chirp_duration
        self.num_time_bins = num_time_bins
        self.num_freq_bins = num_freq_bins
        self.max_frequency = max_frequency
        self.max_chirp_band = max_chirp_band
        self.output_dir = output_dir
        self.labels_file = os.path.join(output_dir, labels_file)
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_linear_chirp(self, start_freq, end_freq, duration):
        """Generate a linear chirp signal."""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        chirp_signal = np.sin(2 * np.pi * (start_freq * t + (end_freq - start_freq) * t**2 / (2 * duration)))
        return chirp_signal

    def generate_exponential_chirp(self, start_freq, end_freq, duration):
        """Generate an exponential chirp signal."""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        k = (end_freq / start_freq) ** (1 / duration)
        chirp_signal = np.sin(2 * np.pi * start_freq * (k**t - 1) / np.log(k))
        return chirp_signal

    def create_spectrogram_with_chirp(self, chirp_start_time, chirp_start_freq, chirp_end_freq, chirp_duration, chirp_type="linear"):
        """Create a spectrogram with a chirp at a specific position."""
        spectrogram = np.zeros((self.num_freq_bins, self.num_time_bins))

        if chirp_type == "linear":
            chirp_signal = self.generate_linear_chirp(chirp_start_freq, chirp_end_freq, chirp_duration)
        elif chirp_type == "exponential":
            chirp_signal = self.generate_exponential_chirp(chirp_start_freq, chirp_end_freq, chirp_duration)
        else:
            raise ValueError("Invalid chirp type. Use 'linear' or 'exponential'.")

        chirp_start_bin = int(chirp_start_time * self.num_time_bins / self.duration)
        chirp_end_bin = chirp_start_bin + int(chirp_duration * self.num_time_bins / self.duration)
        chirp_freq_bin_start = int(chirp_start_freq * self.num_freq_bins / self.max_frequency)
        chirp_freq_bin_end = int(chirp_end_freq * self.num_freq_bins / self.max_frequency)

        if chirp_type == "exponential" and chirp_freq_bin_start == 0:
            chirp_freq_bin_start = 1

        for t_bin in range(chirp_start_bin, chirp_end_bin):
            t_normalized = (t_bin - chirp_start_bin) / (chirp_end_bin - chirp_start_bin)
            if chirp_type == "linear":
                freq_bin = chirp_freq_bin_start + (chirp_freq_bin_end - chirp_freq_bin_start) * t_normalized
            elif chirp_type == "exponential":
                freq_bin = chirp_freq_bin_start * (chirp_freq_bin_end / chirp_freq_bin_start) ** t_normalized
            
            freq_bin = min(max(freq_bin, 0), self.num_freq_bins - 1)
            freq_bin_int = int(freq_bin)

            for f in range(max(0, freq_bin_int - 2), min(self.num_freq_bins, freq_bin_int + 3)):
                weight = np.exp(-0.5 * ((f - freq_bin) ** 2) / 0.5)
                spectrogram[f, t_bin] += weight

        noise_level = np.random.uniform(0.09, 0.3)
        spectrogram += noise_level * np.random.randn(self.num_freq_bins, self.num_time_bins)
        spectrogram = gaussian_filter(spectrogram, sigma=1)

        return spectrogram

    def get_last_saved_index(self):
        """Check the last saved image index to resume from where it stopped."""
        existing_files = [f for f in os.listdir(self.output_dir) if f.startswith("spectrogram_") and f.endswith(".png")]
        existing_indices = [int(f.split("_")[1].split(".")[0]) for f in existing_files if f.split("_")[1].split(".")[0].isdigit()]
        return max(existing_indices) if existing_indices else 0

    def generate_dataset(self, num_samples):
        """Generate a dataset of synthetic spectrograms and save them to disk incrementally."""
        start_index = self.get_last_saved_index() + 1
        print(f"Resuming from sample {start_index}")

        # Ensure labels.csv has headers if starting fresh
        if start_index == 1 and not os.path.exists(self.labels_file):
            with open(self.labels_file, "w") as f:
                f.write("Chirp_Start_Time,Chirp_Start_Freq,Chirp_End_Freq,Chirp_Duration,Chirp_Type\n")

        for i in range(start_index, num_samples + 1):
            chirp_start_time = np.random.uniform(0, self.duration - self.max_chirp_duration)
            chirp_duration = np.random.uniform(1.0, self.max_chirp_duration)
            chirp_start_freq = np.random.uniform(0, self.max_frequency)
            chirp_end_freq = np.clip(chirp_start_freq + np.random.uniform(-self.max_chirp_band, self.max_chirp_band), 0, self.max_frequency)
            chirp_type = np.random.choice(["linear", "exponential"])

            spectrogram = self.create_spectrogram_with_chirp(chirp_start_time, chirp_start_freq, chirp_end_freq, chirp_duration, chirp_type)

            image_path = os.path.join(self.output_dir, f"spectrogram_{i}.png")
            plt.imshow(spectrogram, aspect='auto', origin='lower', cmap='viridis', extent=[0, self.duration, 0, self.max_frequency])
            plt.xlabel("Time (s)")
            plt.ylabel("Frequency (Hz)")
            plt.title(f"Synthetic Spectrogram {i} ({chirp_type} chirp)")
            plt.colorbar(label="Intensity")
            plt.savefig(image_path)
            plt.close()

            # Open the file in append mode for each write to ensure data is flushed
            with open(self.labels_file, "a") as f:
                f.write(f"{chirp_start_time},{chirp_start_freq},{chirp_end_freq},{chirp_duration},{chirp_type}\n")

            if i % 100 == 0:  # Print progress every 100 samples
                print(f"Generated {i} spectrograms...")

        print("Dataset generation completed.")
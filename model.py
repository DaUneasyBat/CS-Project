import os
import wave
import numpy as np
from pydub import AudioSegment
from scipy.io import wavfile
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

class AudioModel:
    def __init__(self):
        self.file_path = ""
        self.wav_path = ""
        self.time_seconds = 0
        self.wav_data = None
        self.sampling_rate = 0
        self.channels = 0

    def load_file(self, file_path):
        self.file_path = file_path
        self._convert_to_wav()
        self._load_wav_data()
        self._remove_meta_data()
        self._handle_multi_channel()
        self.time_seconds = self._get_wav_duration()

    def _convert_to_wav(self):
        if not self.file_path.lower().endswith(".wav"):
            audio = AudioSegment.from_file(self.file_path)
            self.wav_path = os.path.splitext(self.file_path)[0] + ".wav"
            audio.export(self.wav_path, format="wav")

    def _load_wav_data(self):
        if self.wav_path:
            self.sampling_rate, self.wav_data = wavfile.read(self.wav_path)
            self.channels = 1 if len(self.wav_data.shape) == 1 else self.wav_data.shape[1]

    def remove_meta_data(self):
        pass

    def _handle_multi_channel(self):
        if self.channels > 1:
            self.wav_data = np.mean(self.wav_data, axis=1)

    def _get_wav_duration(self):
        return len(self.wav_data) / float(self.sampling_rate)

    def get_waveform(self):
        time_values = np.arange(0, self.time_seconds, 1/self.sampling_rate)
        return time_values, self.wav_data

    def compute_highest_resonance_frequency(self):
        frequency_domain = np.fft.fft(self.wav_data)
        peaks, _ = find_peaks(np.abs(frequency_domain))
        if peaks.any():
            highest_resonance_frequency = peaks[0] * (self.sampling_rate / len(frequency_domain))
            return highest_resonance_frequency
        return 0

    def compute_rt60(self, frequency_range):
        pass

    def plot_waveform(self):
        time_values, waveform = self.get_waveform()
        plt.plot(time_values, waveform)
        plt.xlabel('Time in seconds')
        plt.ylabel('Amplitude')
        plt.title('Waveform')
        plt.show()

    def plot_rt60(self, frequency_range):
        pass

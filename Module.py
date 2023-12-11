import wave
import numpy as np
from pydub import AudioSegment
import os


def analyze_wav(file_path):
    # Check if the file is a .wav file
    if not file_path.lower().endswith('.wav'):
        converted_file_path = convert_to_wav(file_path)
        if converted_file_path:
            file_path = converted_file_path
        else:
            print("Error converting file to .wav.")
            return None, None, None

    with wave.open(file_path, 'rb') as wav_file:
        framerate = wav_file.getframerate()
        frames = wav_file.getnframes()
        duration = frames / float(framerate)

        signal = np.frombuffer(wav_file.readframes(frames), dtype=np.int16)
        frequencies = np.fft.fft(signal)
        frequencies = np.abs(frequencies)[:len(frequencies) // 2]

        # Split frequencies into low, mid, and high sections
        low_freq_cutoff = 100  # Adjust as needed
        high_freq_cutoff = 1000  # Adjust as needed

        low_frequencies = frequencies[:low_freq_cutoff]
        mid_frequencies = frequencies[low_freq_cutoff:high_freq_cutoff]
        high_frequencies = frequencies[high_freq_cutoff:]

    return duration, low_frequencies, mid_frequencies, high_frequencies


def convert_to_wav(input_file):
    try:
        # Load the audio file using pydub
        audio = AudioSegment.from_file(input_file)

        # Create a new file path with the .wav extension
        output_file = os.path.splitext(input_file)[0] + ".wav"

        # Export the audio to the new .wav file
        audio.export(output_file, format="wav")

        return output_file

    except Exception as e:
        print(f"Error converting file to .wav: {e}")
        return None

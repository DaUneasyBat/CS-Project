import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from controller import AudioController

class AudioView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.setup_gui()

    def setup_gui(self):
        # Load File Button
        load_button = tk.Button(self.root, text="Load Audio File", command=self.load_file)
        load_button.pack()

        # Display Name of File
        self.file_label = tk.Label(self.root, text="")
        self.file_label.pack()

        # Display Waveform Button
        waveform_button = tk.Button(self.root, text="Display Waveform", command=self.display_waveform)
        waveform_button.pack()

        # Display Highest Resonance Frequency Button
        resonance_button = tk.Button(self.root, text="Display Resonance Frequency", command=self.display_resonance)
        resonance_button.pack()

        # Plot RT60 Button
        rt60_button = tk.Button(self.root, text="Plot RT60", command=self.plot_rt60)
        rt60_button.pack()

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav;*.mp3;*.aac")])
        if file_path:
            self.controller.load_file(file_path)
            self.file_label.config(text=f"Loaded: {os.path.basename(file_path)}")

    def display_waveform(self):
        self.controller.plot_waveform()

    def display_resonance(self):
        resonance_frequency = self.controller.compute_highest_resonance_frequency()
        tk.messagebox.showinfo("Resonance Frequency", f"Highest Resonance Frequency: {resonance_frequency} Hz")

    def plot_rt60(self):
        frequency_range = [20, 20000]
        self.controller.plot_rt60(frequency_range)

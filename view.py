# View.py
import os
import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from model import analyze_wav
from model import convert_to_wav
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile


class GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("File Upload and Analysis GUI")
        self.master.geometry("800x600")

        self.file_path = None
        self.current_plot_container = None
        self.analysis_data = None  # Store analysis data for use in button clicks

        self.create_widgets()

    def create_widgets(self):
        # File import button
        self.import_button = tk.Button(self.master, text="Import File", command=self.import_file)
        self.import_button.pack(pady=10)

        # File name label
        self.file_label = tk.Label(self.master, text="No file selected")
        self.file_label.pack(pady=5)

        # File name label

        # Upload button
        self.upload_button = tk.Button(self.master, text="Upload", state="disabled", command=self.upload_file)
        self.upload_button.pack(pady=10)

        # Plot buttons
        self.plot_button_low = tk.Button(self.master, text="Low", command=self.plot_button_clicked_low)
        self.plot_button_low.pack(side="left", padx=5)

        self.plot_button_mid = tk.Button(self.master, text="Mid", command=self.plot_button_clicked_mid)
        self.plot_button_mid.pack(side="left", padx=5)

        self.plot_button_high = tk.Button(self.master, text="High", command=self.plot_button_clicked_high)
        self.plot_button_high.pack(side="left", padx=5)

        self.plot_button_all = tk.Button(self.master, text="All", command=self.plot_button_clicked_all)
        self.plot_button_all.pack(side="left", padx=5)

        self.plot_button_rt60 = tk.Button(self.master, text="RT60", command=self.plot_button_clicked_rt60)
        self.plot_button_rt60.pack(side="right", padx=5)

    def import_file(self):
        self.file_path = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[("All files", "*.*")]
        )

        if self.file_path:
            # Check if the file is a .wav file
            if not self.file_path.lower().endswith('.wav'):
                self.converted_file_path = convert_to_wav(self.file_path)
                if self.converted_file_path:
                    self.file_path = self.converted_file_path
                else:
                    print("Error converting file to .wav.")
                    return None

            # Get only the filename from the path
            filename = os.path.basename(self.file_path)
            self.file_label.config(text=f"File selected: {filename}")
            self.upload_button.config(state="normal")

    def upload_file(self):
        self.analysis_data = analyze_wav(self.file_path)
        if self.analysis_data is not None:
            duration, _, _, _ = self.analysis_data
            self.time = tk.Label(self.master, text=f"Time is {duration}")
            self.time.pack(pady=5)
            print(f"Duration of the audio: {duration:.2f} seconds")

    def plot_button_clicked_low(self):
        if self.analysis_data is not None:
            _, low_frequencies, _, _ = self.analysis_data
            self.plot_data(range(len(low_frequencies)), low_frequencies, "Low Frequencies", "Frequency (Hz)", "Amplitude", "Low Plot", "top")

    def plot_button_clicked_mid(self):
        if self.analysis_data is not None:
            _, _, mid_frequencies, _ = self.analysis_data
            self.plot_data(range(len(mid_frequencies)), mid_frequencies, "Mid Frequencies", "Frequency (Hz)", "Amplitude", "Mid Plot", "top")

    def plot_button_clicked_high(self):
        if self.analysis_data is not None:
            _, _, _, high_frequencies = self.analysis_data
            self.plot_data(range(len(high_frequencies)), high_frequencies, "High Frequencies", "Frequency (Hz)", "Amplitude", "High Plot", "top")

    def plot_button_clicked_all(self):
        if self.analysis_data is not None:
            _, low_frequencies, mid_frequencies, high_frequencies = self.analysis_data
            self.plot_data_all(
                range(len(high_frequencies)),
                high_frequencies,
                range(len(mid_frequencies)),
                mid_frequencies,
                range(len(low_frequencies)),
                low_frequencies,
                "All Frequencies",
                "Frequency (Hz)",
                "Amplitude",
                "top"
            )

    def plot_data(self, x_values, y_values, title, xlabel, ylabel, plot_title, side):
        # Remove the current plot container if it exists
        if self.current_plot_container:
            self.current_plot_container.destroy()

        # Create a new plot based on the selected type
        fig, ax = plt.subplots()
        ax.plot(x_values, y_values, color='r')  # Adjust the plot as needed
        ax.set_title(plot_title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

        # Display the new plot in a container
        self.current_plot_container = tk.Frame(self.master)
        self.current_plot_container.pack(side=side, fill="both", expand=1)

        canvas = FigureCanvasTkAgg(fig, master=self.current_plot_container)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side="top", fill="both", expand=1)

    def plot_data_all(self, x_values_high, y_values_high, x_values_mid, y_values_mid, x_values_low, y_values_low, title,
                      xlabel, ylabel, side):
        if self.current_plot_container:
            self.current_plot_container.destroy()
        fig, ax = plt.subplots()
        ax.plot(x_values_high, y_values_high, color='r', label='high')
        ax.plot(x_values_mid, y_values_mid, color='b', label='mid')
        ax.plot(x_values_low, y_values_low, color='g', label='low')
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

        plt.legend()

        # To load the display window
        self.current_plot_container = tk.Frame(self.master)
        self.current_plot_container.pack(side=side, fill="both", expand=1)

        canvas = FigureCanvasTkAgg(fig, master=self.current_plot_container)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side="top", fill="both", expand=1)
    # ... (rest of the code remains unchanged)
    def plot_button_clicked_rt60(self):
        if self.current_plot_container:
            self.current_plot_container.destroy()

        sample_rate, data = wavfile.read(self.file_path)
        spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
        # prints var outputs
        def debugg(fstring):
            print(fstring) # comment out for prod
        # pass
        def find_target_frequency(freqs):
            for x in freqs:
                if x > 1000:
                    break
            return x
        def frequency_check():
        # you can choose a frequency which you want to check
            debugg (f'freqs {freqs[:10]}]')
            target_frequency = find_target_frequency(freqs)
            debugg (f'target_frequency {target_frequency}')
            index_of_frequency = np.where(freqs== target_frequency) [0] [0]
            debugg (f'index_of_frequncy {index_of_frequency}') # find a sound data for a particular frequency
            data_for_frequency = spectrum [index_of_frequency]
            debugg (f'data_for_frequency {data_for_frequency [:10]}')
            # change a digital signal for a values in decibels
            data_in_db_fun = 10 * np.log10(data_for_frequency)
            return data_in_db_fun
        data_in_db = frequency_check()
        plt.figure()
        # plot reverb time on grid
        plt.plot(t, data_in_db, linewidth=1, alpha=0.7, color='#004bc6')
        plt.xlabel('Time (s)')
        plt.ylabel('Power (dB)')
        # find a index of a max value
        index_of_max= np.argmax(data_in_db)
        value_of_max = data_in_db[index_of_max]
        plt.plot(t[index_of_max], data_in_db [index_of_max], 'go')
        # slice array from a max value
        sliced_array = data_in_db [index_of_max:]
        value_of_max_less_5 = value_of_max - 5
        # find a nearest value
        def find_nearest_value(array, value):
            array = np.asarray(array)
            debugg(f'array {array[:10]}')
            idx = (np.abs (array - value)).argmin()
            debugg(f'idx {idx}')
            debugg (f'array[idx] {array[idx]}')
            return array[idx]
        value_of_max_less_5 = find_nearest_value(sliced_array, value_of_max_less_5)
        index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)
        plt.plot(t[index_of_max_less_5], data_in_db [index_of_max_less_5], 'yo')
        # slice array from a max -5dB
        value_of_max_less_25 = value_of_max - 25
        value_of_max_less_25 = find_nearest_value(sliced_array, value_of_max_less_25)
        index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)
        plt.plot(t[index_of_max_less_25], data_in_db [index_of_max_less_25], 'ro')
        rt20 = (t[index_of_max_less_5] - t[index_of_max_less_25])[0]
        # extrapolate rt20 to rt60
        rt60 = 3 * rt20
        # optional set limits on plot
        #plt.xlim(0, ((round(abs(rt60), 2)) * 1.5))


        plt.grid()  # show grid
        plt.show() # show plots
        print (f'The RT60 reverb time is {(rt60)} seconds')
        self.current_plot_container = tk.Frame(self.master)
        self.current_plot_container.pack(side="top", fill="both", expand=1)

        canvas = FigureCanvasTkAgg(fig, master=self.current_plot_container)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side="top", fill="both", expand=1)



if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()
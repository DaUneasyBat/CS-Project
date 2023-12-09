from model import AudioModel
from view import AudioView

class AudioController:
    def __init__(self):
        self.model = AudioModel()
        self.view = None

    def set_view(self, view):
        self.view = view

    def load_file(self, file_path):
        self.model.load_file(file_path)

    def plot_waveform(self):
        self.view.display_waveform()

    def display_resonance(self):
        self.view.display_resonance()

    def plot_rt60(self, frequency_range):
        self.view.plot_rt60(frequency_range)

def main():
    controller = AudioController()
    root = tk.Tk()
    view = AudioView(root, controller)
    controller.set_view(view)
    root.mainloop()

if __name__ == "__main__":
    main()


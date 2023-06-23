import tkinter as tk


class GUIWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Transcription Display")
        self.window.geometry("400x300")
        self.window.configure(bg="white")

        self.text_label = tk.Label(self.window, text="", fg="black", bg="white", font=("Arial", 12))
        self.text_label.pack(pady=50)

    def update_text(self, text):
        self.text_label.config(text=text)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    gui = GUIWindow()
    gui.run()

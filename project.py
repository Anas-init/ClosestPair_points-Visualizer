from tkinter import Tk, Button, filedialog, messagebox, Canvas
import turtle
import time

class MainApp(Tk):
    coordinates = []

    def __init__(self):
        super().__init__()
        self.canvas = Canvas(self, bg="white", width=800, height=800)
        self.canvas.pack()

    def readFile(self, filename, coordinates):
        if not filename:
            messagebox.showerror("Error", "Please choose a file")
            return

        try:
            with open(filename, 'r') as file:
                for line in file:
                    if not line.strip():
                        continue
                    try:
                        cleaned_line = line.replace('(', '').replace(')', '').replace(',', '')
                        x_coordinates, y_coordinates = cleaned_line.split()
                        x_coordinates = int(x_coordinates)
                        y_coordinates = int(y_coordinates)
                        coordinates.append((x_coordinates, y_coordinates))
                    except ValueError:
                        messagebox.showerror("Error", f"Invalid line format: '{line.strip()}'. Expected two integers.")
                        return

        except FileNotFoundError:
            messagebox.showerror("Error", "File not found. Please select a valid file.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def Selectfile(self):
        filename = filedialog.askopenfilename(
            initialdir="/", 
            title="Select file", 
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        self.readFile(filename, self.coordinates)
        self.draw_coordinates()

    def draw_coordinates(self):
        self.canvas.create_line(50, 750, 750, 750, fill="black", width=2)
        self.canvas.create_line(50, 750, 50, 50, fill="black", width=2)
        self.canvas.create_text(40, 760, text="(0, 0)", anchor="ne")
        scale_factor = 30
        for (x, y) in self.coordinates:
            if x >= 0 and y >= 0:
                canvas_x = 50 + x * scale_factor
                canvas_y = 750 - y * scale_factor
                self.canvas.create_oval(
                    canvas_x - 3, canvas_y - 3,
                    canvas_x + 3, canvas_y + 3,
                    fill="blue", outline="blue"
                )
            
                


app = MainApp()
app.geometry("1000x800")
chooseFileButton = Button(app, text="Choose text file", command=app.Selectfile, highlightcolor="#38A3A5", bg="#F8F7FF", width=20, height=2)
chooseFileButton.place(relx=0.5, rely=0.95, anchor="s")

app.mainloop()
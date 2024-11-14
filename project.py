from tkinter import Tk, Button, filedialog, messagebox, Canvas, Scrollbar, Frame
import math,time

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def dist(p1, p2):
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

def closest_util(points, n):
    if n <= 3:
        min_dist = float('inf')
        closest_pair = None
        for i in range(n):
            for j in range(i + 1, n):
                d = dist(points[i], points[j])
                if d < min_dist:
                    min_dist = d
                    closest_pair = (points[i], points[j])
        return min_dist, closest_pair

    mid = n // 2
    pl = points[:mid]
    pr = points[mid:]

    dl, cl = closest_util(pl, mid)
    dr, cr = closest_util(pr, n - mid)

    d = min(dl, dr)
    closest_pair = cl if dl < dr else cr

    strip = []
    for i in range(n):
        if abs(points[i].x - points[mid].x) < d:
            strip.append(points[i])
    for i in range(len(strip)):
        j = i + 1
        while j < len(strip) and (strip[j].y - strip[i].y) < d:
            d_temp = dist(strip[i], strip[j])
            if d_temp < d:
                d = d_temp
                closest_pair = (strip[i], strip[j])
            j += 1

    return d, closest_pair

def closest(points):
    points.sort(key=lambda x: x.x)
    return closest_util(points, len(points))


class MainApp(Tk):
    coordinates = []

    def __init__(self):
        super().__init__()
        self.title("Closest Pair of Points Visualizer")
        self.canvas_width = 1500
        self.canvas_height = 1500
        self.margin = 50
        container = Frame(self)
        container.pack(fill="both", expand=True)

        self.scroll_canvas = Canvas(container, width=1200, height=900, bg="white")
        h_scrollbar = Scrollbar(container, orient="horizontal", command=self.scroll_canvas.xview)
        v_scrollbar = Scrollbar(container, orient="vertical", command=self.scroll_canvas.yview)
        self.scroll_canvas.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)

        h_scrollbar.pack(side="bottom", fill="x")
        v_scrollbar.pack(side="right", fill="y")
        self.scroll_canvas.pack(side="left", expand=True, fill="both")
        self.canvas = Canvas(self.scroll_canvas, bg="white", width=self.canvas_width, height=self.canvas_height)
        self.scroll_canvas.create_window((0, 0), window=self.canvas, anchor="nw")
        self.scroll_canvas.config(scrollregion=(0, 0, self.canvas_width, self.canvas_height))

    def readFile(self, filename):
        if not filename:
            messagebox.showerror("Error", "Please choose a file")
            return

        self.coordinates = []  

        try:
            with open(filename, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        cleaned_line = line.strip("()").replace(" ", "")
                        x_coordinates, y_coordinates = map(int, cleaned_line.split(','))
                        self.coordinates.append((x_coordinates, y_coordinates))
                    except ValueError:
                        messagebox.showerror("Error", f"Invalid line format: '{line}'. Expected format is '(x,y)'.")
                        return

            self.draw_coordinates()
            self.find_closest_pair()
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def Selectfile(self):
        filename = filedialog.askopenfilename(
            title="Select file",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        self.readFile(filename)

    def draw_coordinates(self):
        self.canvas.delete("all")

        # Draw X and Y axes
        self.canvas.create_line(self.margin, self.canvas_height - self.margin,
                                self.canvas_width - self.margin, self.canvas_height - self.margin, fill="black", width=2)
        self.canvas.create_line(self.margin, self.margin,
                                self.margin, self.canvas_height - self.margin, fill="black", width=2)
        self.canvas.create_text(self.margin - 10, self.canvas_height - self.margin + 10, text="(0, 0)", anchor="ne")
        max_x = max((x for x, y in self.coordinates), default=1)
        max_y = max((y for x, y in self.coordinates), default=1)

        # Adjust scaling factor to fit points within canvas bounds
        scale_x = (self.canvas_width - 3 * self.margin) / (max_x + 1)
        scale_y = (self.canvas_height - 3 * self.margin) / (max_y + 1)
        scale_factor = min(scale_x, scale_y)
        for (x, y) in self.coordinates:
            canvas_x = self.margin + x * scale_factor
            canvas_y = self.canvas_height - self.margin - y * scale_factor
            self.canvas.create_oval(canvas_x - 3, canvas_y - 3, canvas_x + 3, canvas_y + 3, fill="blue", outline="blue")

    def find_closest_pair(self):
        points = [Point(x, y) for x, y in self.coordinates]
        n = len(points)
        if n < 2:
            messagebox.showinfo("Result", "At least two points are required.")
            return

        min_dist, closest_pair = closest(points)
        p1, p2 = closest_pair

        self.display_closest_pair(p1, p2)
        messagebox.showinfo("Result", f"The smallest distance is {min_dist:.2f} between points ({p1.x}, {p1.y}) and ({p2.x}, {p2.y})")

    def display_closest_pair(self, p1, p2):
        max_x = max((x for x, y in self.coordinates), default=1)
        max_y = max((y for x, y in self.coordinates), default=1)
        scale_x = (self.canvas_width - 2 * self.margin) / (max_x + 1)
        scale_y = (self.canvas_height - 2 * self.margin) / (max_y + 1)
        scale_factor = min(scale_x, scale_y)

        canvas_x1 = self.margin + p1.x * scale_factor
        canvas_y1 = self.canvas_height - self.margin - p1.y * scale_factor
        canvas_x2 = self.margin + p2.x * scale_factor
        canvas_y2 = self.canvas_height - self.margin - p2.y * scale_factor
        self.canvas.create_line(canvas_x1, canvas_y1, canvas_x2, canvas_y2, fill="yellow", width=3)
        

app = MainApp()
app.geometry("1300x1000")
chooseFileButton = Button(app, text="Choose Text File", command=app.Selectfile, width=20)
chooseFileButton.place(relx=0.5, rely=0.02, anchor="n")

app.mainloop()

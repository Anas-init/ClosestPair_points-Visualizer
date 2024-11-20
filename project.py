import tkinter
from tkinter import Tk, Button, filedialog, messagebox, Canvas, Scrollbar, Frame
import math
import tkinter.ttk
import random;
import os;
from functools import lru_cache

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
    def __init__(self):
        super().__init__()
        self.title("DAA Project Part 2")
        self.geometry("1300x1000")
        self.coordinates = []

        # Create a header
        header = tkinter.Label(self, text="Select an Algorithm", font=("Helvetica", 20, "bold"), fg="black")
        header.pack(pady=(180, 10))

        # Buttons
        chooseCPP = Button(self, text="Closest Pair Problem", font=("Helvetica", 12), command=self.makeCPPWindow, width=20)
        chooseCPP.pack(pady=10)
        chooseKaratsuba = Button(self, text="Karatsuba Algorithm", font=("Helvetica", 12), command=self.makeKaratsubaWindow, width=20)
        chooseKaratsuba.pack(pady=10)

    def makeCPPWindow(self):
        self.destroy();
        cpp = CPP();
        cpp.mainloop();
        
    def makeKaratsubaWindow(self):
        self.destroy();
        ka = Karatsuba();
        ka.mainloop();
        
class CPP(Tk):
    def __init__(self):
        super().__init__()
        self.title("Closest Pair Point")
        self.geometry("1300x1000")
        self.coordinates = []
        
        # Scrollable Canvas Frame
        container = Frame(self)
        container.pack(fill="both", expand=True)

        self.scroll_canvas = Canvas(container, width=1200, height=900, bg="white")
        h_scrollbar = Scrollbar(container, orient="horizontal", command=self.scroll_canvas.xview)
        v_scrollbar = Scrollbar(container, orient="vertical", command=self.scroll_canvas.yview)
        self.scroll_canvas.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)

        h_scrollbar.pack(side="bottom", fill="x")
        v_scrollbar.pack(side="right", fill="y")
        self.scroll_canvas.pack(side="left", expand=True, fill="both")

        self.canvas = Canvas(self.scroll_canvas, bg="white", width=1500, height=1500)
        self.scroll_canvas.create_window((0, 0), window=self.canvas, anchor="nw")
        self.scroll_canvas.config(scrollregion=(0, 0, 1500, 1500))
        
        self.generateRandomFiles();
        chooseFileBtn = Button(self, text="Choose Input File", font=("Helvetica", 12), command=self.Selectfile, width=20)
        chooseFileBtn.place(relx=0.5, rely=0.02, anchor="n")
        
        
    def generateRandomFiles(self):
        curr_dir = os.getcwd();
        for i in range(1, 11):
            file_path = os.path.join(curr_dir, f"cpp{i}.txt")
            with open(file_path, "w") as file:
                num_points = random.randint(50, 100);
                for i in range(1, num_points + 1):
                    random_int_1 = random.randint(1, 30)
                    random_int_2 = random_int_1;
                    while random_int_2 == random_int_1:
                        random_int_2 = random.randint(1, 30)
                    file.write(f"({str(random_int_1)}, {str(random_int_2)})\n");
        
    def Selectfile(self):
        filename = filedialog.askopenfilename(
            title="Select file",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if filename:
            self.readFile(filename)

    def readFile(self, filename):
        self.coordinates = []

        try:
            with open(filename, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        cleaned_line = line.strip("()").replace(" ", "")
                        x, y = map(int, cleaned_line.split(','))
                        self.coordinates.append((x, y))
                    except ValueError:
                        messagebox.showerror("Error", f"Invalid line format: '{line}'. Expected format is '(x,y)'.")
                        return

            self.draw_coordinates()
            self.find_closest_pair()
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def draw_coordinates(self):
        self.canvas.delete("all")

        # Draw axes
        self.canvas.create_line(50, 1450, 1450, 1450, fill="black", width=2)  # X-axis
        self.canvas.create_line(50, 50, 50, 1450, fill="black", width=2)      # Y-axis

        # Scaling factor
        max_x = max((x for x, y in self.coordinates), default=1)
        max_y = max((y for x, y in self.coordinates), default=1)
        scale_x = (1400) / (max_x + 1)
        scale_y = (1400) / (max_y + 1)
        scale = min(scale_x, scale_y)

        # Draw points
        for x, y in self.coordinates:
            canvas_x = 50 + x * scale
            canvas_y = 1450 - y * scale
            self.canvas.create_oval(canvas_x - 5, canvas_y - 5, canvas_x + 5, canvas_y + 5, fill="blue")

    def find_closest_pair(self):
        if len(self.coordinates) < 2:
            messagebox.showinfo("Result", "At least two points are required.")
            return

        points = [Point(x, y) for x, y in self.coordinates]
        min_dist, closest_pair = closest(points)

        # Draw the closest pair
        if closest_pair:
            self.draw_closest_pair(closest_pair)

        p1, p2 = closest_pair
        messagebox.showinfo("Result", f"The smallest distance is {min_dist:.2f} between points ({p1.x}, {p1.y}) and ({p2.x}, {p2.y})")

    def draw_closest_pair(self, closest_pair):
        max_x = max((x for x, y in self.coordinates), default=1)
        max_y = max((y for x, y in self.coordinates), default=1)
        scale_x = (1400) / (max_x + 1)
        scale_y = (1400) / (max_y + 1)
        scale = min(scale_x, scale_y)

        p1, p2 = closest_pair
        canvas_x1 = 50 + p1.x * scale
        canvas_y1 = 1450 - p1.y * scale
        canvas_x2 = 50 + p2.x * scale
        canvas_y2 = 1450 - p2.y * scale

        self.canvas.create_line(canvas_x1, canvas_y1, canvas_x2, canvas_y2, fill="red", width=2)

class Karatsuba(Tk):
    def __init__(self):
        super().__init__()
        self.title("Karatsuba Algorithm")
        self.geometry("1300x1000")
        self.coordinates = []
        self.table = None;
        
        self.generateRandomFiles();
        chooseFileBtn = Button(self, text="Choose Input File", font=("Helvetica", 12), command=self.Selectfile, width=20)
        chooseFileBtn.place(relx=0.5, rely=0.02, anchor="n")
        
    def generateRandomFiles(self):
        curr_dir = os.getcwd();
        for i in range(1, 11):
            file_path = os.path.join(curr_dir, f"karatsuba{i}.txt")
            with open(file_path, "w") as file:
                random_int_1 = random.randint(100000, 100000000000000000)
                random_int_2 = random.randint(100000, 100000000000000000)
                file.write(f"{str(random_int_1)}, {str(random_int_2)}\n");

        
    def Selectfile(self):
        filename = filedialog.askopenfilename(
            title="Select file",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if filename:
            self.readFile(filename)

    def readFile(self, filename):
        x, y = None, None;

        try:
            with open(filename, 'r') as file:
                line = file.readline().strip()
                if not line:
                    messagebox.showerror("Error", "File is empty.")
                    return
                try:
                    cleaned_line = line.replace(" ", "")
                    x, y = map(int, cleaned_line.split(','))
                except ValueError:
                        messagebox.showerror("Error", f"Invalid line format: '{line}'. Expected format is 'x,y'.")
                        return

            self.createTable(x, y)
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
            
    def createTable(self, x, y):
        self.table = tkinter.ttk.Treeview(self, columns = ('X', 'Y', 'X * Y'), show = 'headings');
        self.table.heading('X', text = 'X');
        self.table.heading('Y', text = 'Y');
        self.table.heading('X * Y', text = 'ac * (10 ^ (2 * break_point)) + (ad + bc) * 10^(break_point) + bd');
        self.table.pack(fill = 'both', expand = True, padx = 5, pady=(70, 0));

        final_answer = self.applyKaratsuba(x, y);
        display_answer = tkinter.Label(self, text=f"Final Answer: {str(final_answer)}", font=("Helvetica", 20, "bold"), fg="black")
        display_answer.pack(anchor="w", padx=(10), pady=(10))
    
    @lru_cache(maxsize=None)
    def applyKaratsuba(self, x, y):
        if(x < 10 or y < 10): 
            self.table.insert(parent = '', index = tkinter.END, values = (x, y, f"{str(x * y)} (Base Case)"));
            return int(x * y);
        
        n_x = math.ceil(math.log10(x));
        n_y = math.ceil(math.log10(y));
        
        break_point = int(max(n_x, n_y) / 2);
        
        a = int(x / pow(10, break_point));
        b = int(x % pow(10, break_point));
        
        c = int(y / pow(10, break_point));
        d = int(y % pow(10, break_point));
            
        
        # equation 1:
        # => (a * 10^(break_point) + b) * (c * 10^(break_point) + d)
        # => ac * 10^(break_point) * 10^(break_point) + ad * 10^(break_point) + bc * 10^(break_point) + bd
        # => ac * (10 ^ (break_point + break_point)) + (ad + bc) * 10^(break_point) + bd
        # => ac * (10 ^ (2 * break_point)) + (ad + bc) * 10^(break_point) + bd
        
        # equation 2:
        # => (a + b) (c + d) - ac - bd
        # => ac + ad + bc + bd - ac - bd
        # => ac - ac + bd - bd + ad + bc
        # => ad + bc
        
        ac = int(self.applyKaratsuba (a, c));
        bd = int(self.applyKaratsuba (b, d));
        ad_plus_bc = int(self.applyKaratsuba (a + b, c + d) - ac - bd);

        self.table.insert(parent = '', index = tkinter.END, values = (x, y, f"{str(ac)} X 10^{str(break_point)} + {str(ad_plus_bc)} X 10^{str(break_point)} + {str(bd)}"));
        
        solved_equation = ac * pow(10, 2 * break_point) + (ad_plus_bc) * pow(10, break_point) + bd;
            
        return int(solved_equation);
    

app = MainApp()
app.mainloop()


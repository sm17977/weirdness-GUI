import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
from pandas import DataFrame

LARGE_FONT = ("Verdana", 12)
DEREKO_FILE_NAME = 'dereko_tokens.txt'
JSYNCC_FILE_NAME = 'all_jsyncc_tokens.txt'
DEREKO_TOKENS = {}
JSYNCC_TOKENS = {}


class MainWindow(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default="index.ico")
        tk.Tk.wm_title(self, "Test Window")
        self.geometry("800x400")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for f in (StartPage, PageOne, PageTwo, PageThree):
            frame = f(container,self)
            self.frames[f] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()

    def grid_conf(self, frame):
        for x in range(2):
            frame.grid_rowconfigure(self, x, weight=1)
        for y in range(3):
            frame.grid_columnconfigure(self, y, weight=1)



class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Corpora Statistics", font=LARGE_FONT)
        label.grid(row=0, column=0, sticky="nsew", columnspan=3, pady=(0,0))

        btn = ttk.Button(self, text="Jsyncc Stats",
                        command=lambda: controller.show_frame(PageOne))
        btn2 = ttk.Button(self, text="DeReKo Stats",
                        command=lambda: controller.show_frame(PageTwo))
        btn3 = ttk.Button(self, text="Weirdness",
                        command=lambda: controller.show_frame(PageThree))
        btn.grid(row=1, column=0, sticky="nsew", padx=(5,5), pady=(0,20))
        btn2.grid(row=1, column=1, sticky="nsew", padx=(5,5), pady=(0,20))
        btn3.grid(row=1, column=2, sticky="nsew", padx=(5,5), pady=(0,20))

        MainWindow.grid_conf(self, tk.Frame)


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Jsyncc Stats", font=LARGE_FONT)
        label.grid(row=0, column=0, sticky="nsew", columnspan=3, pady=(0,5))

        btn = ttk.Button(self, text="Return",
                        command=lambda: controller.show_frame(StartPage))
        btn2 = ttk.Button(self, text="DeReKo Stats",
                        command=lambda: controller.show_frame(PageTwo))
        btn3 = ttk.Button(self, text="Weirdness",
                        command=lambda: controller.show_frame(PageThree))
        txtbox = ttk.Entry(self, width=5)

        btn.grid(row=1, column=0, sticky="nsew", padx=(5, 5), pady=(5, 5))
        btn2.grid(row=1, column=1, sticky="nsew", padx=(5, 5), pady=(5, 5))
        btn3.grid(row=1, column=2, sticky="nsew", padx=(5, 5), pady=(5, 5))
        txtbox.grid(row=2, column=1, sticky="nsew", padx=(5, 5), pady=(5, 5))




        # Store Jsnycc tokens in a dictionary with key as token and value as frequency
        with open(JSYNCC_FILE_NAME, buffering=1000000, encoding="utf-8") as f:
            for line in f:
                if line in JSYNCC_TOKENS:
                    JSYNCC_TOKENS[line] = JSYNCC_TOKENS[line] + 1
                else:
                    JSYNCC_TOKENS[line] = 1
            f.close()

        sorted_jsnycc = {k: v for k, v in sorted(JSYNCC_TOKENS.items(), key=lambda item: item[1], reverse=True)}
        dframe = DataFrame({A: N for (A, N) in [x for x in sorted_jsnycc.items()][:10]}.items(), columns=['Token', 'Frequency'])
        f = plt.Figure(figsize=(3, 3))
        a = f.add_subplot(1,1,1)
        dframe = dframe[['Token', 'Frequency']].groupby(['Token'], sort=False).sum()
        dframe.plot(kind='bar', legend=True, ax=a, rot=0)

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=3, column=1, sticky="nsew", padx=(5, 5), pady=(5, 5))

        MainWindow.grid_conf(self, tk.Frame)




class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="DeReKo Stats", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        btn = ttk.Button(self, text="Return",
                        command=lambda: controller.show_frame(StartPage))
        btn2 = ttk.Button(self, text="Jsyncc Stats",
                        command=lambda: controller.show_frame(PageOne))
        btn.pack()
        btn2.pack()


class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Weirdness", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        btn = ttk.Button(self, text="Return",
                        command=lambda: controller.show_frame(StartPage))
        btn2 = ttk.Button(self, text="Jsyncc Stats",
                        command=lambda: controller.show_frame(PageOne))
        btn.pack()
        btn2.pack()

        f = Figure(figsize=(5, 5), dpi=100)
        a = f.add_subplot(111)
        a.plot([1,2,3,4,5,6,7,8],[5,4,7,4,3,2,1,3])

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas,self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


app = MainWindow()
app.mainloop()
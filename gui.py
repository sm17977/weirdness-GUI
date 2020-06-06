import tkinter as tk
from tkinter import ttk
from nltk import FreqDist
import json
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from pandas import DataFrame

LARGE_FONT = ("Verdana", 12)
DEREKO_FILE_NAME = 'dereko_freq.txt'
JSYNCC_FILE_NAME = 'jsyncc_freq.txt'
DEREKO_TOKENS = {}
JSYNCC_TOKENS = {}



class MainWindow(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default="index.ico")
        tk.Tk.wm_title(self, "Test Window")
        self.geometry("1000x500")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for f in (StartPage, PageOne, PageTwo, PageThree, PageFour):
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

    with open(JSYNCC_FILE_NAME, buffering=20000000, encoding="utf-8") as f:
        freq = FreqDist(json.loads(f.read()))


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)



        label = tk.Label(self, text="Jsyncc Stats", font=LARGE_FONT)
        label.pack()

        btn = ttk.Button(self, text="Return",
                        command=lambda: controller.show_frame(StartPage))
        btn2 = ttk.Button(self, text="DeReKo Stats",
                        command=lambda: controller.show_frame(PageTwo))
        btn3 = ttk.Button(self, text="Weirdness",
                        command=lambda: controller.show_frame(PageThree))
        btn4 = ttk.Button(self, text="Open Class Words Table",
                        command=lambda: controller.show_frame(PageFour))
        txtbox = ttk.Entry(self, width=5)

        btn.pack(side=tk.TOP)
        btn2.pack(side=tk.TOP)
        btn3.pack(side=tk.TOP)
        btn4.pack(side=tk.TOP)
        txtbox.pack(side=tk.TOP)

        df1 = DataFrame(self.freq.most_common(10), columns=['Token', 'Frequency'])
        fig, ax1 = plt.subplots(nrows=1, ncols=1,figsize=(4.5, 3))
        df1 = df1[['Token', 'Frequency']].groupby(['Token'], sort=False).sum()
        df1.plot(kind='bar', legend=True, ax=ax1, rot=0)


        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)




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
        btn3 = ttk.Button(self, text="Weirdness",
                        command=lambda: controller.show_frame(PageThree))
        txtbox = ttk.Entry(self, width=5)

        btn.pack(side=tk.TOP)
        btn2.pack(side=tk.TOP)
        btn3.pack(side=tk.TOP)
        txtbox.pack(side=tk.TOP)


        with open(DEREKO_FILE_NAME, buffering=20000000, encoding="utf-8") as f:
            freq = FreqDist(json.loads(f.read()))

        print("done")

        df1 = DataFrame(freq.most_common(10), columns=['Token', 'Frequency'])
        fig, ax1 = plt.subplots(nrows=1, ncols=1,figsize=(4.5, 3))
        df1 = df1[['Token', 'Frequency']].groupby(['Token'], sort=False).sum()
        df1.plot(kind='bar', legend=True, ax=ax1, rot=0)

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)




        MainWindow.grid_conf(self, tk.Frame)


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

class PageFour(tk.Frame):

    freq = PageOne.freq

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Jsyncc Open Class Words", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        btn = ttk.Button(self, text="Return",
                        command=lambda: controller.show_frame(StartPage))
        btn2 = ttk.Button(self, text="Jsyncc Stats",
                        command=lambda: controller.show_frame(PageOne))
        btn.pack()
        btn2.pack()

        f = Figure(figsize=(8, 5), dpi=100)
        ax = f.add_subplot(111)

        top_100 = [x[0] for x in self.freq.most_common(100)]
        top_10_batches = [top_100[idx:idx+10] for idx in range(0,100,10)]

        bf = [[''.join(x)] for x in top_10_batches]
        bd = []
        for x in bf:
            for y in x:
                a = ','.join(y.lower().splitlines())
                b = '%'
                c = '0'
                bd.append([a, b, c])



        print(bd)

        col_labels = ['Batches of 10', 'Relative Frequency', 'Open Class Words']
        table_vals = bd

        table = ax.table(cellText=table_vals,
                          colWidths=[0.1] * 11,
                          colLabels=col_labels,
                          cellLoc='center',
                          loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        table.scale(2, 2)
        table.auto_set_column_width(col=list(range(len(col_labels))))
        ax.set_axis_off()

        plt.subplots_adjust(left=0.2, bottom=0.2, top=1)

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack()




app = MainWindow()
app.mainloop()
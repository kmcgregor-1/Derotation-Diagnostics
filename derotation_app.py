import csv
from tkinter import *
from tkinter.filedialog import askopenfilename
import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import os

def main():
    root = Tk()
    root.wm_title("Field Rotation Diagnostics")
    root.geometry("600x300")
    root.configure(bg='white')
    root.resizable(width=False, height=False)

    global data
    data = []

    def ask_open_file():
        print("running ask open file")
        global file_name
        file_name = askopenfilename(filetypes=[('csv files','*csv')])
        return file_name

    def open_file():
        print("running open file")
        global file_selected
        file_name = ask_open_file()
        with open(file_name,'r') as f:
            file = list(csv.reader(f))
            #print(file)
            return file
        #Label(root,bg='white',text='file selected',fg='red').grid(row=1,column=1)

    def convert_to_polar(x_coord,y_coord):
        r = math.sqrt(x_coord**2+y_coord**2)
        theta = math.atan(y_coord/x_coord)
        return (r,theta)

    def make_list():
        print("running make list")
        acc = []
        file_list = open_file()
        i = 1
        while i < len(file_list):
            for num in file_list[i]:
                 acc.extend([convert_to_polar(float(file_list[i][0])-1024.,float(file_list[i][1])-1024.)])
            i += 1
        data.clear()
        data.extend(acc)
        #print(acc)
        Button(root,text=os.path.basename(file_name)+" Selected",bg="Green",command=make_list).grid(row=1,column=0,padx=40,pady=10)

    def plot_polar():
        print("running plot polar")
        theta = []
        for point in data:
            theta.append(point[0])
        r = []
        for point in data:
            r.append(point[1])
        ax.scatter(r,theta,s=5,cmap='hsv',alpha=0.75)
        ax.set_rmax(1024)
        ax.set_rticks(np.arange(0,1024,512))
        canvas.draw()

    def show_polar():
        print("running show polar")
        theta = []
        for point in data:
            theta.append(point[0])
        r = []
        for point in data:
            r.append(point[1])
        ax.scatter(r,theta,s=5,cmap='hsv')
        ax.set_title(os.path.basename(file_name)+" Field Rotation")
        ax.set_rmax(1024)
        ax.set_rticks(np.arange(0,1024,512))
        plt.show()
        """
        plot = Tk()
        plot.geometry("600x600")
        canvas = FigureCanvasTkAgg(fig, master=plot)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().grid().scale("all")
        plot.mainloop()
        """

    def plot_angular():
        fig1, ax1 = plt.subplots()
        theta = []
        for point in data:
            theta.append(point[1])
        time = np.arange(0,len(theta)/2,1)
        plt.scatter(time,theta[::2])
        ax1.set_title(os.path.basename(file_name)+" Field Rotation")
        plt.xlabel("Time (Exp)")
        plt.ylabel("Angle (Rads)")
        plt.show()

    fig, ax = plt.subplots(figsize=(3,3),subplot_kw={'projection': 'polar'})
    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().grid(column=2,rowspan=5)
    ax.set_rmax(1024)
    ax.set_rticks(np.arange(0,1024,512))
    #fig.set_facecolor("lightgrey")

    Label(root,bg='white',text="Directions:\n1. Perform Aperture Photometry to get a file\n   listing FITS coordinates of a star in a field\n2. Select file to convert to polar coordinates\n   and graph",
        justify="left").grid(row=0,column=0,columnspan=2)
    Button(root,text="SELECT FILE",bg="white",command=make_list).grid(row=1,column=0,padx=40,pady=10)
    Button(root,text="POLAR GRAPH PREVIEW",bg="white",command=plot_polar).grid(row=2,column=0,padx=40,pady=10)
    Button(root,text="POLAR GRAPH",bg="white",command=show_polar).grid(row=3,column=0,padx=40,pady=10)
    Button(root,text="ANGULAR GRAPH",bg="white",command=plot_angular).grid(row=4,column=0,padx=40,pady=10)

    menubar = Menu()
    fileMenu = Menu(menubar)
    menubar.add_cascade(label="File", menu=fileMenu)
    fileMenu.add_command(label="New Window",command=main)
    root.config(menu=menubar)

    root['bg'] = 'white'
    root.mainloop()
main()

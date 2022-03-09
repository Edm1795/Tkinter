from tkinter import *
from tkinter import ttk
import math
import numpy
import time


# Version 0.1
# 1. This is the first point where this project takes real formation. It opens a main window and displays speedometers showing the amount of
#     quantity in stock.  The speedometer itself works although has not been scaled yet to show mulitple items independently

# Version 0.2
# 2. Changed speedometerList to a dict. speedometerDict. This will make updates to stock items easier as the item
#       can be accessed by its key.

# Version 0.25
# 3.  Added list into speedometerDict which calls the updateSpeedometer method




#  This is a key improvement for scaling up the interface

class MainWindow:
    def __init__(self, master):

        # Master Window
        self.master = master
        self.master.title('Supply Chain Ver. 0.25')
        self.master.geometry("+150+500")  # position of the window in the screen (200x300)
        # self.master.geometry("700x400")  # set size of the root window (master) (1500x700);
        # if not set, the frames will fill the master window

        screenWidth = self.master.winfo_screenwidth()
        screenHeight = self.master.winfo_screenheight()

        # Instantiate frames
        self.frame0 = Frame(self.master, bd=5, padx=5, bg='#448833')  # Top long row
        self.frame1 = Frame(self.master, bd=5, padx=5, bg='#115533')  # Side Column
        self.frame2 = Frame(self.master, bd=5, padx=5,bg='#114466')  # Main frame
        # self.frame3 = Frame(self.master, bd=5, padx=5,bg='#112233')
        # self.frame4 = Frame(self.master, bd=5, padx=5,bg='#116633')

        # Place frames
        self.frame0.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.frame1.grid(row=1, column=0, sticky="nsew")
        self.frame2.grid(row=1, column=1, sticky="nsew")
        # self.frame3.grid(row=1, column=2, sticky="nsew")
        # self.frame4.grid(row=1, column=3, sticky="nsew")

        # configure weighting of frames
        self.master.grid_columnconfigure(0, weight=1) # ALlows frames to expand as master window expands
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=1)

        frameWidth = 10  # Units are in characters not pixels

        # Set up text boxes
        self.text1 = Text(self.frame1, height=20, width=frameWidth, bg='#113333', fg='white')
        self.text1.insert(INSERT, 'The complete works of Shakespeare were written by William')
        # self.text1.grid_columnconfigure(0, weight=1)
        self.text1.grid_rowconfigure(0, weight=1)
        self.text1.config(wrap='word')
        self.text1.pack()

        #  Entry widgets
        self.entry = Entry(self.frame0, width='10')
        self.entry.pack()

        self.addStockItemEntry = Entry(self.frame1, width='10')
        self.addStockItemEntry.pack()

        self.speedometerDict = {}  # list of all speedometer's and item names

        self.circleOrigin = self.calcCircleOrigin(10, 10, 80, 80)  # Returns a list of speedometer's values used for drawing line: [xOrigin, yOrigin, radius]


        self.addStockItemEntry.bind('<Return>',lambda event: self.addItem([1,9],[1,10],self.addStockItemEntry.get()))  # first value is number of degrees the speedometer must turn

       #  updateSpeedometer takes [xOrigin, yOrigin, radius]
        self.entry.bind('<Return>',lambda event: self.updateSpeedometer(585, self.circleOrigin[0], self.circleOrigin[1],self.circleOrigin[2]))  # first value is number of degrees the speedometer must turn

        # creating and placing scrollbar
        sb = Scrollbar(self.master, orient=VERTICAL)
        sb.grid(row=1, column=1, sticky='nse')

        # binding scrollbar with other widget (Text, Listbox, Frame, etc)
        self.text1.config(yscrollcommand=sb.set)
        sb.config(command=self.text1.yview)

    def addItem(self, LabRowCol, cirRowCol,itemName):  # adds stock items to the screen

        # in future only put in values to dict, save the draw circle as a different function
        #  This stores the construction (and implementation) of the speedometer and label
        #   as well as the update of the quantity of items thus: {key:[drawCircle()...,updateSpeedometer()...]}

        self.speedometerDict.update({itemName: [self.drawCircle(10, 10, 80, 80,3,[1,1],[1,2], 'Black Pens'),self.updateSpeedometer(585, self.circleOrigin[0], self.circleOrigin[1],self.circleOrigin[2])]})
        self.speedometerDict.update({itemName: self.drawCircle(10, 10, 80, 80,3,[1,3],[1,4], 'China Markers')})
        self.speedometerDict.update({itemName: self.drawCircle(10, 10, 80, 80,3,[1,5],[1,6], 'Red Pens')})
        self.speedometerDict.update({itemName: self.drawCircle(10, 10, 80, 80,3,[1,7],[1,8], 'Golf Pencils')})

        self.speedometerDict.update({itemName: [self.drawCircle(10, 10, 80, 80, 3,LabRowCol,cirRowCol, itemName),self.updateSpeedometer(500, self.circleOrigin[0], self.circleOrigin[1],self.circleOrigin[2])]})



    def calcCircleOrigin(self, x1, y1, x2, y2):
        ''' calculates the speedometer's important circle values: radius, and coordinates of origin
        inputs: x1,y1,x2,y2 of the containing box for the circle: upper left and lower right coordinates
        Outputs: list of the speedometer's circle values: [xOrigin,yOrigin, radius]'''
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2
        radius = (x2 - x1) / 2

        return [x, y, radius]


    def drawCircle(self,x1,y1,x2,y2, width, LabRowCol,cirRowCol, itemName):
        '''
        inputs:
        4 ints: coordinates of square: top left x,y, and bottom right x,y,.
         1 int: width of the circle's outline.
         2 lists: each with 2 ints:
                list 1: circle's position on frame row and column [col,row]
                list 2: label's position on frame row and column  [col,row] (be sure to set it beside the circle)
        1 str: name of item in stock
         '''

        # Create a canvas object
        self.c = Canvas(self.frame2, width=150, height=100, bg='white')

        # Draw an Oval in the canvas
        self.c.create_oval(x1, y1, x2, y2, width=width)
        # self.c.pack()
        self.c.grid(row=cirRowCol[0], column=cirRowCol[1], sticky='nse')

        self.label = Label(self.frame2, text=itemName)
        # self.label.pack()
        self.label.grid(row=LabRowCol[0], column=LabRowCol[1], sticky='nse')

    def colourChanger(self):
        '''
        This method changes the colour for the speedometer dial. It does not yet work properly;
        it simply returns the same colour every time
        '''
        colour = '#' + str(111111 + 10)
        return colour

    def updateSpeedometer(self, speed, XcircleOrigin, YCircleOrigin, radius):
        radius = radius - 5  # subtract width of circle's outline + extra to keep clear space from circle's outline
        list1 = []  # list for storing all coordinates
        speed += 1  # add 1 to speed so that the call to speedometer can be done with round numbers, ex 90

        #  calculate the coordinates of circle's circumference
        for deg in range(320, speed):
            x = XcircleOrigin - (radius * (math.cos(numpy.round(numpy.deg2rad(deg),2))))  # calc coordinate of x and y on circle's circum. xCoordOfOrigin - (rad. * cos(deg))
            y = YCircleOrigin - (radius * (math.sin(numpy.round(numpy.deg2rad(deg),2))))  # yCoordOfOrigin - (rad. * sin(deg)
            list1.append((numpy.round(x,2),numpy.round(y,2)))  # [(x,y),(x,y),(x,y)...


        for i in range(0, len(list1),2):  # move in steps of two, 0,2,4,6

            tup = list1[i]  # cache first tup of coordinates, for white colour line (to erase purple line); currently not used, line is not being erased
            nextTup = list1[i+1]  # cache next tup of coord. for purple line

            # print(self.colourChanger())
            self.c.create_line(XcircleOrigin, YCircleOrigin,nextTup[0],nextTup[1], fill=self.colourChanger(), width=3)  # draw line in circle; values: x and Y of both  ends of line (1st point: horiz, verti, end point horiz, vert.
            self.master.update()


    def runResults(self):

        self.c.create_line(55, 55, x, y, fill='purple', width=3)  # draw line in circle; values: x and Y of both  ends of line (1st point: horiz, verti, end point horiz, vert.
        self.master.update()

        # x(t) = r cos(t) + j
        # y(t) = r sin(t) + k

        btn = ttk.Button(self.master)
        print(btn.configure().keys())
        print(self.frame1.configure().keys())
        # print(dir(self.frame1))


def main():
    root = Tk()
    MainWindow(root)

    root.mainloop()


main()

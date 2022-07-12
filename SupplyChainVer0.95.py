from tkinter import *
from tkinter import ttk
import math
import numpy
import pickle as p
import time

###### Helpful for Navigating ############

# alt 2 --> opens book marks, shift F11, opens floating window
# alt 7 --> structure of code
# See all latest changes, right click, local history --> show history ( near bottom of menu)

############## Key Values for Program #################

######  Label's showing name of items:
#  self.labelWidth -------- inside itemNameFormatter()

######  Canvas holding all speedometers
#  canvasWidth ----  inside itemNameFormatter()
#  cavasHeight ------ inside itemNameFormatter()

# self.speedometerDict ----- The dict which holds the values of each item in stock, {itemNameAsKey: Value as list of lists [[values for drawCircle() label row and col...],[values for updateSpeedometer() circle row and col...],amount of stock]}

# Version 0.1
# 1. This is the first point where this project takes real formation. It opens a main window and displays speedometers showing the amount of
#     quantity in stock.  The speedometer itself works although has not been scaled yet to show mulitple items independently

# Version 0.2
# 2. Changed speedometerList to a dict. speedometerDict. This will make updates to stock items easier as the item
#       can be accessed by its key.

# Version 0.25
# 3.  Added list into speedometerDict which calls the updateSpeedometer method

# Version 0.3
# 4.  Adds pickle function to update config file
# 5.  Adds pickle function to load config file into speedometerDict
# 6. Improves addItem to receive name of item from user, update config file, and reload the screen to show new item
# 7. Sets w width to the Label widgets of 8 characters, this standardizes the size of all labels. Will need to create a new function to add new
#       lines to text inside the label widgets.
# 8. Adds button for updating speedometers

# Version 0.4
# 9. Adds "add item" button which opens a popup window, takes the name entered, updates the speedometer Dictionary and updates the config file

# Version 0.5
# 10. Add item function now automatically calualates the grid position to place the new item on the screen.
#           note: it only works on one row, and is not sophisticated.

# Version 0.6
# 11. Draw sped circles and speeds seperately.  Currently the drawcircles() can draw all speds but then updating the speed itself is only working on the last sped. probably
#            because drawcircles can only access the last canvas created.  Confirm the cause of the problem, then if correct make a list for all canvases.
#  12. Created self.canvases = [] and self.labels = [] to hold all such objects
#  13. drawCircles() now draws all the speedometers first, then updates the speedometers to their correct speeds one by one (quantities)

#  This is a key improvement for scaling up the interface

# Version 0.7
#  14. Adds itemNameFormatter(itemName) which formats the names of stock items so that they fit into their labels nicely (this was a lot of work)

# Version 0.8
#  15.  Put colour changing loop inside updateSpedometer()
#  16.  improved row configurations to fill screen properly:
#
#          self.master.grid_columnconfigure(0, weight=1) # Allows frames to expand as master window expands; weight tells how much of the columns it takes
#         self.master.grid_columnconfigure(1, weight=3) #  weight gives 3 times as much column as the other columns
#         # self.master.grid_columnconfigure(2, weight=1)
#         self.master.grid_rowconfigure(1, weight=1)  # rowconfigure states: first row takes 1 parts of space

#  Version 0.9
#  17.  Added numerical speeds to speedometers:
#           self.canvases[-1].create_text(18, 75, text="0", fill="black", font=('Helvetica 10'))  # draw "0" to left bottom of speedometer
#           self.canvases[-1].create_text(87, 75, text="100", fill="black", font=('Helvetica 10'))  # draw "100" to right bottom of speedometer

# Version 0.91
# 18. attempting to add buttons to each canvas holding the spedometer, so that values of the item can be changed--inside draw circle method
# so far so good, create canvas, create button on canvas, then append canvas.

# Version 0.92
# Edit button opens a new window,a nd receives input but doe snot correctly update the Speedometer Dict.

#  18.  Made screen responsive to speedometers, it places them into rows and cols based on size of screen and size of boxes

#             for k, val in self.speedometerDict.items():  # {itemNameAsKey: Value as list of lists [[values for drawCircle() label row and col...],[values for updateSpeedometer() circle row and col...]]}
#                 if col < maxNumOfBoxes:  # Below the maximum of allowed boxes
#                     self.drawCircle(k, [row, col], [row,
#                                                     col + 1])  # {'Blue Pens':[[1,1],[1,2],501],...} Note, only sends first two lists, not the final value 501.  Eg: [0,0],[0,1]... [0,2],[0,3]...[0,4],[0,5]
#                     col += 2  # Increment by 2 so as not to overlap with previous boxes
#                 else:  # Above the maximum of allowed boxes, sets values for drawing on the next row on the screen and draws circles and labels for the first item of that row
#                     col = 0
#                     row += 1
#                     self.drawCircle(k, [row, col], [row,
#                                                     col + 1])  # {'Blue Pens':[[1,1],[1,2],501],...} Note, only sends first two lists, not the final value 501
#                     col += 2  # Increment by 2 so as not to overlap with previous boxes

# Ver 0.93
# Program now can accept editing of stock quantities by way of the edit button. Key problem was associating the edit buttons to their correct items
# this was solved by sending the itemName to the editItem function as part of the buttons' commands using lambda so that the command would not be
# immediately run.

#  19. Next, get proper calculation of box widget size.  Need to instantiate one label w/o posting it and then get its pixel width
#  20. removed extraneous entry widgets; adjusted size of buttons, attempted to make a clearFrame() which is not working properly
#  21.  Added grid_propogate(0) to frame 1 and 2 to fix size of frames while inputting widgets (Jen's great discovery).
# 22. Improved much of the documentation
# 24. Changed some values on how the speeds are drawn in the circle: 1. now it increments through its loop in units of 1, rather than 2 which makes for a smoother
# turn of the circle. 2. This also lets even numbers be used for the max stock (now 578= max). 3. This makes setting up the stock divisions simpler mathematically.

# Ver. 0.94
# 25. added Def calcSpeed() which calculates the correct speed relative to what is full stock.  Eg: if 3 boxes = full stock, it will output 578 km/h (shown as 100 on
# the interface).

# Ver. 0.95
# 26. added update to stockAndUnitvalueDict

class MainWindow:
    def __init__(self, master):

        # Master Window
        self.master = master
        self.master.title('Supply Chain Ver. 0.95 In the Works')
        self.master.geometry("+150+500")  # position of the window in the screen (200x300)
        self.master.geometry("1000x400")  # set initial size of the root window (master) (1500x700);
        # if not set, the frames will fill the master window
        # self.master.attributes('-fullscreen', True)
        screenWidth = self.master.winfo_screenwidth()
        screenHeight = self.master.winfo_screenheight()

        # Instantiate frames
        self.frame0 = Frame(self.master, bd=5, padx=5, bg='#448833')  # Top long row
        self.frame1 = Frame(self.master, bd=5, padx=5, bg='#115533')  # Side Column
        self.frame2 = Frame(self.master, bd=5, padx=5,bg='#114466')  # Main frame

        # Place frames
        self.frame0.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.frame1.grid(row=1, column=0, columnspan=1, sticky="nsew")
        self.frame2.grid(row=1, column=1, columnspan=1, sticky="nsew")

        # configure weighting of frames
        self.master.grid_columnconfigure(0, weight=1) #  First int refers to column numberAllows frames to expand as master window expands; weight tells how much of the columns it takes
        self.master.grid_columnconfigure(1, weight=7) #  weight gives 3 times as much column as the other columns
        # self.master.grid_columnconfigure(2, weight=1)
        self.master.grid_rowconfigure(1, weight=1)  # rowconfigure states: first row takes 1 parts of space

        self.frame1.grid_propagate(0)  #  When adding widgets maintain weighting of frames
        self.frame2.grid_propagate(0)

        frameWidth = 10  # Units are in characters not pixels

        #  Instantiate lists for canvases and labels
        self.canvases = []
        self.labels = []

        self.labelWidth = 11  # Width in characters for the label showing name of item (used for item name formatter); increment up if more space needed

        #  Entry widgets
        self.entry = Entry(self.frame0, width='10')
        self.entry.pack()

        # self.addStockItemEntry = Entry(self.frame1, width='10')
        # self.addStockItemEntry.pack()
        # self.drawCircleEntry = Entry(self.frame1, width='15')
        # self.drawCircleEntry.pack()

        #######     320 = no stock                 578 = full stock                  258 = full range of values from no stock to full stock  ########
        # list of all speedometer's and item names. Structure:  #  {itemNameAsKey: Value as list of lists [[values for drawCircle() label row and col...],[values for updateSpeedometer() circle row and col...],Quantity of Item]}
        self.speedometerDict = {'Blue Pens':[[1,1],[1,2],501],'Staedtler Pens':[[1,3],[1,4],411],'China Markers':[[1,5],[1,6],401],'Red Pens':[[1,7],[1,8],330],'Paper Clips':[[1,9],[1,10],320],'White Tape':[[1,11],[1,12],501],'Golf Pencils':[[1,13],[1,14],401],'Scissors':[[2,1],[2,2],421],'Transparent Name Tag Slips (Small)':[[2,3],[2,4],380]}
        self.stockAndUnitValueDict ={'Blue Pens': [3,86]} # dictionary with list of 2 values [number of items constituting max stock, unit of speed for each item] Eg: 3 items = max stock, each item takes 86 km/h of speed

        self.circProp = (20,20,80,80,3)  # Properties needed for drawing circle inside of a box (x,y,x,y,outlineWidth)
        self.circleOrigin = self.calcCircleOrigin(self.circProp[0],self.circProp[1],self.circProp[2],self.circProp[3])  # Returns a list of speedometer's values used for drawing line: [xOrigin, yOrigin, radius, width]

        self.button = Button(self.frame1, text="Update Speds", width= 12, command=self.drawCircles)
        self.button.pack()

        self.addItemButton = Button(self.frame1, text="Add Item", width= 12, command=self.addItem)
        self.addItemButton.pack()

        self.clearFramesButton = Button(self.frame1, text="Clear Frames", width=12, command=self.clearSpeedoFrame)  #  Clears frame2, the speedometer frame of all widgets
        self.clearFramesButton.pack()

       #  updateSpeedometer takes [xOrigin, yOrigin, radius]
       #  self.entry.bind('<Return>',lambda event: self.updateSpeedometer(585, self.circleOrigin[0], self.circleOrigin[1],self.circleOrigin[2]))  # first value is number of degrees the speedometer must turn.

        # self.drawCircleEntry.bind('<Return>',lambda event: self.drawCircles())  # first value is number of degrees the speedometer must turn
        # {'Blue Pens':[[1,1],[1,2]],'China Markers':[[1,3],[1,4]]}

        # creating and placing scrollbar
        sb = Scrollbar(self.master, orient=VERTICAL)
        sb.grid(row=1, column=1, sticky='nse')

        # binding scrollbar with other widget (Text, Listbox, Frame, etc)
        # self.text1.config(yscrollcommand=sb.set)
        # sb.config(command=self.text1.yview)

    def calcSpeed(self):
        speedOfItem = (self.stockAndUnitValueDict['Blue Pens'][0] * self.stockAndUnitValueDict['Blue Pens'][1]) + 320  # multiples the number of stock by unit of speed then adds 320 (320 is actually the strating value for no stock or speed of 0 km/h)
        self.speedometerDict['Blue Pens'][2]=speedOfItem # add loop to check every k,v, if k == itemName: v = speedOfItem

    def addItem(self):
        """
        This function opens up a popup window, takes text from the user and adds that text as an item to the Speedometer Dictionary;
        it also updates the config file so that the item is permanently saved
        """
        top = Toplevel(self.master)
        top.geometry("400x150")
        top.title("Add New Item")

        # input for new item in stock
        addItemLabel = Label(top, text="Add New Item", font=('Cambria 12'))  #  Label(top, text="Add New Item", font=('Mistral 18 bold')).place(x=150, y=80)
        addItemLabel.grid(row=1, column=1)  # Note: .grid cannot be placed as a single line code: Label(...).grid(..) as the .grid will actually return None to the program and casue an error

        addItemEntry = Entry(top, width='40')
        addItemEntry.grid(row=1, column=2)

        addItemEntry.bind('<Return>', lambda event: addItemToSpeedometerDict())

        # input for setting max stock level for new item
        setMaxStockLabel = Label(top, text="Value for Max Stock", font=('Cambria 12'))  # Label(top, text="Add New Item", font=('Mistral 18 bold')).place(x=150, y=80)
        setMaxStockLabel.grid(row=2,column=1)  # Note: .grid cannot be placed as a single line code: Label(...).grid(..) as the .grid will actually return None to the program and casue an error

        setMaxStockEntry = Entry(top, width='40')
        setMaxStockEntry.grid(row=2, column=2)

        setMaxStockEntry.bind('<Return>', lambda event: combineAddItemAndMaxStock())

        def addItemToSpeedometerDict():

            self.updateSpeedometerDict(addItemEntry.get())  # enter text from popup window to be used for name of item being added
            self.updateConfigFile()

            completionMes = Label(top, text=addItemEntry.get() + ' added to your list of items', font=('Cambria 12'))
            completionMes.grid(row=3, column=1)

            # addItemEntry.delete(0, END)  # Delete text in entry field. (Note, This deletes the value inside the Entry itself not merely clearing the screen.)

        def addMaxStockValue(): # add max stock to self.stockAndUnitValueDict

            # self.updateSpeedometerDict(addItemEntry.get())  # enter text from popup window to be used for name of item being added
            # self.updateConfigFile()

            self.updateStockAndUnitValueDict(int(setMaxStockEntry.get()),addItemEntry.get()) # write max stock and set unit value for the given item to the dict.

            completionMes = Label(top, text=setMaxStockEntry.get() + ' set as max stock', font=('Cambria 12'))
            completionMes.grid(row=4, column=1)

            setMaxStockEntry.delete(0, END)  # Delete text in entry field
            addItemEntry.delete(0,END)  # Delete text in entry field. (Note, This deletes the value inside the Entry itself not merely clearing the screen.)

            print(self.stockAndUnitValueDict.items())

        def combineAddItemAndMaxStock():
            addItemToSpeedometerDict()
            addMaxStockValue()

    def updateStockAndUnitValueDict(self,maxStock,nameOfItem): # put max stock value into StockAndUnitValueDict
        '''
        This function sets the values for max stock and the unit value of stock for each item and writes them to the StockAndUnit...Dict
        :param maxStock: int for what constitute full stock of that item
        :param nameOfItem:  Str: name of item in stock
        '''
        self.stockAndUnitValueDict.update({nameOfItem: [0,0]}) # instantiate item in dictionary with placeholder values of 0,0, [max stock value,unit of stock value]
        self.stockAndUnitValueDict[nameOfItem][0] = maxStock
        self.stockAndUnitValueDict[nameOfItem][1] = 258/maxStock  # 258 is the total range of speed




    def editItem(self,itemName):
        """
        This function opens a new window for editing the total amount of stock available for the given item clicked on
        Inputs: str: itemName, this is the name of the item in stock associated with that button
        """
        top = Toplevel(self.master)
        top.geometry("400x150")
        top.title("Edit Quantity of Stock")

        editItemLabelTitle = Label(top, text=itemName, font=('Cambria 14'))
        editItemLabel = Label(top, text="New Value", font=('Cambria 12'))  # Label(top, text="Add New Item", font=('Mistral 18 bold')).place(x=150, y=80)

        editItemLabelTitle.grid(row=1,column=1)
        editItemLabel.grid(row=2,column=1)  # Note: .grid cannot be placed as a single line code: Label(...).grid(..) as the .grid will actually return None to the program and casue an error

        editItemEntry = Entry(top, width='10')

        editItemEntry.grid(row=2, column=2)
        editItemEntry.bind('<Return>', lambda event: updateQuantityInSpeedometerDict(itemName)) # send the itemName to the updateQuantity function

        def updateQuantityInSpeedometerDict(nameOfStock):
            """
            Searches for the correct item in the SpeedometerDict then updates the amount of stock.
            Inputs: str: nameOfStock, which gives the name of the item in the dict to be updated, {'Blue Pens': [[1,1],[1,2],101]} the third value is accessed ie. 101.
            """
            print(nameOfStock)
            print('Initial Set of Values:', self.speedometerDict.items())

            #self.speedometerDict[nameOfStock][2]=int(editItemEntry.get())  # update value in speedometerdict to value given in popup window
            self.stockAndUnitValueDict[nameOfStock][0]=int(editItemEntry.get())  # update stock and unit dict ([0]) with amount of stock spedified by user

            completionMes = Label(top, text=nameOfStock + ' updated to ' + editItemEntry.get(), font=('Cambria 12'))
            completionMes.grid(row=3, column=1)

            editItemEntry.delete(0,END)  # Delete text in entry field

            print('New Set of Values:  ', self.speedometerDict.items())
            # self.speedometerDict.update({'Blue Pens': [[1,1],[1,2],101]})  # 50 is inside a list of lists, only change the 50 keep other values as is.

    # def clear_text():
    #     text.delete(0, END)

    def updateSpeedometerDict(self,newItemName):
        """
        This function adds new items to the Speedometer Dictionary from the add item button on the interface;
        it also calculates the next position to place the new item on the screen

        inputs: str: name of new item to add
        """
        lastValue=list(self.speedometerDict.values())[-1]  # get last value from dict (list of lists: :[label(row,col):[2,5],circle(row,col):[2,6]],quantity:583]) from dict. [[1, 13], [1, 14], 401])
        self.speedometerDict.update({newItemName: [[2, lastValue[0][1]+2], [2, lastValue[1][1]+2], 578]})  #  increment up appropriate amount to place new item on empty slot on grid, sets a placeholder value of stock
        print(self.speedometerDict.items())


    def loadSpeedometerDict(self):
        """
        This method uses pickle to load the dictionary from config.txt into the speedometerDict
        """
        with open('config.txt', 'rb') as f:
            self.speedometerDict=p.load(f)
            print('The  speedometer dictionary has been loaded from the config file')

    def clearSpeedoFrame(self):
        """
        This method clears the main frame (frame2) of all its widgets holding all the speedometers;
        it also clears self.canvases list and the self.labels list so that new objects can be stored
        inside those lists.
        """
        for widgets in self.frame2.winfo_children():
            widgets.destroy()
            self.canvases.clear()
            self.labels.clear()

    def drawCircles(self):
        """
        This method draws all speedometers and speeds. First it draws the speedometers
        sequentially in the order of the speedometerDict, then it draws in the dial showing
        the speed of each item.
        """

        #### To get the pixel width of the labels run this test ####
        # labelTest = Label(self.frame2, width=self.labelWidth,text='test')
        # labelTest.grid(row=0,column=3)
        # self.master.update()
        # print(labelTest.winfo_width())  ## output is 83 for labelWidth = 11

        # self.clearSpeedoFrame()  # clears the main frame (frame2) of all its widgets
        row = 0
        col = 0
        x = self.frame2.winfo_width()
        maxNumOfBoxes=(self.frame2.winfo_width()//240)*2  # get size of main frame (displaying speds), floor divide (//) by size of box,multiply by 2 b/c otherwise boxes will overlap due to nature of layout. 150 = canvas width, 83 = labelWidth. note the calculated values do not work well, hence using 180 as total
        listIndexCounter=0  # used for index access to list of canvases, starting with first canvas, drawing each line, then next canvas

        # self.clearFrame()

        #  Call drawCircle() for each k,v in speedometerDict.  Creates canvas object, label object, grids them to the screen according to list of lists [[1,1],[1,2]]
        for k,val in self.speedometerDict.items():  #  {itemNameAsKey: Value as list of lists [[values for drawCircle() label row and col...],[values for updateSpeedometer() circle row and col...]]}
            if col < maxNumOfBoxes:  # Below the maximum of allowed boxes
                self.drawCircle(k,[row,col],[row,col+1])  #  {'Blue Pens':[[1,1],[1,2],501],...} Note, only sends first two lists, not the final value 501.  Eg: [0,0],[0,1]... [0,2],[0,3]...[0,4],[0,5]
                col+=2  # Increment by 2 so as not to overlap with previous boxes  [0,0],[0,1]... [0,2],[0,3]...[0,4],[0,5]
            else:   # Above the maximum of allowed boxes, sets values for drawing on the next row on the screen and draws circles and labels for the first item of that row
                col=0  # rest col to 0 so next row starts at far left of screen
                row+=1  # increment up to next row down
                self.drawCircle(k,[row,col],[row,col+1])  #  {'Blue Pens':[[1,1],[1,2],501],...} Note, only sends first two lists, not the final value 501
                col+=2  # Increment by 2 so as not to overlap with previous boxes in the row [0,0],[0,1]... [0,2],[0,3]...[0,4],[0,5]

        self.calcSpeed() # calculates the proper speed for each item and updates the speedometerDict with those proper speeds

        for k , val in self.speedometerDict.items():  # draw in the dial showing speeds of each item sequentially
            self.updateSpeedometer(val[2],self.circleOrigin[0], self.circleOrigin[1],self.circleOrigin[2],listIndexCounter)  #  val[2] is the speed, listIndexCounter access the list of canvases holding the speedometers
            listIndexCounter+=1


    def updateConfigFile(self):
        """
        This method writes the speedometerDict into the config.txt file
        """
        with open('config.txt', 'wb') as f:
            p.dump(self.speedometerDict, f)

    def calcCircleOrigin(self, x1, y1, x2, y2):
        """
        calculates the speedometer's important circle values: radius, and coordinates of origin
        inputs: x1,y1,x2,y2 of the containing box for the circle: upper left and lower right coordinates
        Outputs: list of the speedometer's circle values: [xOrigin,yOrigin, radius]
        """
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2
        radius = (x2 - x1) / 2

        return [x, y, radius]


    def drawCircle(self,itemName, LabRowCol,cirRowCol):
        """ This method is called by drawCircles.  It creates the speedometers and labels (item name) for each item in stock.
        First is creates a canvas, appends it to a list, then creates a label, appends that to another list, then draws the
        circles, adds the '0' and '100' speeds, then adds the labels.
        inputs:
        itemName: str of the stock item's name (this is the key from a dict.)
        LabRowCol: list of 2 ints for label's row and col placement [row,col]
        cirRowCol: list of 2 ints for speedometer's row and col placement [row,col]
         """

        def itemNameFormatter(itemName):
            """
                This method formats the name of stock items so that new lines are added to the appropriate spots
                making the name fit properly to the self.labelWidth
                Inputs: itemName string from dictionary, note: also takes the value self.labelWidth from the parent function, drawCircle()
                Outputs: a string with '\n' added to correct spots
            """

            string = ''
            cacheList = []
            listOfTerms = itemName.split()
            listToStr = ''
            for term in listOfTerms:
                if listOfTerms.index(term) == 0:  #  Check if dealing with very first word in name of item
                    if len(term) > self.labelWidth - 1:
                        cacheList.append(string + term + '\n')  #  If first word is too long add a newline and cache it
                    else:
                        string = string + term  # If first word is not too long add word to string
                else:
                    if len(string) + 1 + len(term) > self.labelWidth - 1:  # if dealing with second word or onwards
                        cacheList.append(string + '\n')  # If next word creates too long of a sequence add newline without new word and cache it
                        string = term  # after caching put the new word into the string (otherwise that new word will get left out)
                    else:
                        string = string + ' ' + term  #  If new word will not create too long a sequence, add space and the new word
            cacheList.append(string)  # cache the string
            return listToStr.join(cacheList)  # converts elements from list to string form


        canvasWidth = 150  # Width of canvas holding the speedometers, note, not including the labels
        cavasHeight = 100  # Height of canvas holding the speedometers

        # Create canvas object and label object and place them into their respective lists

        c = Canvas(self.frame2, width=canvasWidth, height=cavasHeight, bg='white')       # Create canvas for speedometer
        c.create_oval(self.circProp[0], self.circProp[1],self.circProp[2],self.circProp[3],width=self.circProp[4])
        c.create_text(18, 75, text="0", fill="black",font=('Helvetica 10'))                                  # draw "0" to left bottom of speedometer
        c.create_text(87, 75, text="100", fill="black",font=('Helvetica 10'))                             # draw "100" to right bottom of speedometer


        # create and place edit button for editing values of the stock item
        editButton = Button(c, text='Edit', command=lambda:self.editItem(itemName))      # create button on the canvas. to give an id: name='itemName'. The command runs editItem with the itemName as parameter
        c.create_window(110, 10, anchor=NW, window=editButton)      # Create a window on the canvas to hold to hold the button

        c.grid(row=cirRowCol[0], column=cirRowCol[1], sticky='nse')
        self.canvases.append(c)  # append the canvas to list

        # self.canvases.append(Canvas(self.frame2, width=canvasWidth, height=cavasHeight, bg='white'))
        self.labels.append(Label(self.frame2, width=self.labelWidth, text=itemNameFormatter(itemName)))

        # Access the last item (most recently appended element) in the canvases list, draw a circle with it, then grid it to the screen
        # self.canvases[-1].create_oval(self.circProp[0], self.circProp[1],self.circProp[2],self.circProp[3],width=self.circProp[4])


        # self.canvases[-1].grid(row=cirRowCol[0], column=cirRowCol[1], sticky='nse')

        #  Draw speed markings on to speedometers. Access most recently added canvas then draw numbers
        # self.canvases[-1].create_text(18, 75, text="0", fill="black", font=('Helvetica 10'))  # draw "0" to left bottom of speedometer
        # self.canvases[-1].create_text(87, 75, text="100", fill="black", font=('Helvetica 10'))  # draw "100" to right bottom of speedometer

        # Access the last item in the labels list and grid it to the screen
        self.labels[-1].grid(row=LabRowCol[0], column=LabRowCol[1], sticky='nse')






    def colourChanger(self):
        '''
        This method changes the colour for the speedometer dial. It does not yet work properly;
        it simply returns the same colour every time
        '''
        colour = '#' + str(111111 + 10)
        return colour

    def updateSpeedometer(self, speed, XcircleOrigin, YCircleOrigin, radius, listIndexCounter):
        """
        This calculates and draws the lines from the centre of the circle out to its circumference, this showing the speed of that item.
        :param speed: int: how fast (how many items you are holding in stock. 100 = full stock, 0 = no stock)
        :param XcircleOrigin: centre of circle (used for drawing the starting point of every line for the speed)
        :param YCircleOrigin: centre of circle (used for drawing the starting point of every line for the speed)
        :param radius: How long the lines need to be (from the centre out to the edge of the circle)
        :param listIndexCounter: index for accessing the list of canvases holding the speedometers, starts at 0, accesses first
        canvas, draws its speed, then moves to next canvas. the method which calls this method determines which canvas
        to access and to increment up.
        """
        radius = radius - 5  # subtract width of circle's outline + extra to keep clear space from circle's outline
        list1 = []  # list for storing all coordinates of circle's circumference
        speed += 1  # add 1 to speed so that the call to speedometer can be done with round numbers, ex 90
        colour = 111111  # set initial colour for speedometer dial

        #  calculate the coordinates of circle's circumference for drawing the speedometer around the circle
        for deg in range(320, speed): # 320 = no stock; 579 = full stock
            x = XcircleOrigin - (radius * (math.cos(numpy.round(numpy.deg2rad(deg),2))))  # calc coordinate of x on circle's circum. xCoordOfOrigin - (rad. * cos(deg))
            y = YCircleOrigin - (radius * (math.sin(numpy.round(numpy.deg2rad(deg),2))))  # calc y Coord on circle's circum. yCoordOfOrigin - (rad. * sin(deg)
            list1.append((numpy.round(x,2),numpy.round(y,2)))  # [(x,y),(x,y),(x,y)...


        for i in range(0, len(list1),1):  # move in steps of two, 0,2,4,6

            #tup = list1[i]  # cache first tup of coordinates, for white colour line (to erase purple line); currently not used, line is not being erased
            nextTup = list1[i]  # cache next tup of coord. for purple line

            colour += 50  # increment colour of speedometer dial to a new colour for each line. 40 gives nice blue to aqua change.  def colourChanger() is also available but not working
            self.canvases[listIndexCounter].create_line(XcircleOrigin, YCircleOrigin,nextTup[0],nextTup[1], fill='#'+str(colour), width=3)  # draw line in circle; values: x and Y of both  ends of line (1st point: horiz, verti, end point horiz, vert. 579 = full stock
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

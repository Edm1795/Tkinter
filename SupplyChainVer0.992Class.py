from tkinter import *
from tkinter import ttk
import math
import numpy
import pickle as p
from os.path import exists
from ctypes import windll  # used for fixing blurry fonts on win 10 and 11

# Idea (Delete or move) Move additem to its own class, instantiate the class when the button is pushed, or just call functions from it.


# import time
############## Helpful for Navigating ##############

# alt 2 --> opens book marks, shift F11, opens floating window.
# alt 7 --> structure of code
# See all latest changes, right click, local history --> show history ( near bottom of menu)
# ctrl + Shift + E = recently changed code
# dedent - shift + tab

########## Commit ##############
# select commit at top right (green arrow)
# Select name of file to commit
# Write in comments
# press commit and push
# press push

############# Adding New Functions as Buttons to Interface #############

### Example adding a button which takes an argument
#deleteItemButton = Button(top, command=lambda: self.deleteItem(itemName), text="Delete Item", width=12)
# Remember to also grid button


############## Key Values for Program ##############

############## Label's showing name of items ##############
#  self.labelWidth -------- inside itemNameFormatter()

##############   Canvas holding all speedometers ##############
#  canvasWidth ----  inside itemNameFormatter()
#  cavasHeight ------ inside itemNameFormatter()

# self.speedometerDict ----- The dict which holds the values of each item in stock, {itemNameAsKey: Value as list of lists [[values for drawCircle() label row and col...],[values for updateSpeedometer() circle row and col...],amount of stock]}
# self.stockAndUnitValueDict = {'Blue Pens': [3,86]} # dictionary with list of 2 values [number of items constituting max stock (appears actually to be current amount of stock, not the max), unit of speed for each item] Eg: 3 items = max stock, each item takes 86 km/h of speed
## update quantity in Speedometer diCt  takes the updated quantity, not the max.  calcSpeed() also uses the stockAndUnitValueDict[0]

######## Appearance ###########

### Labels showing name of item ###
# self.labels.append(Label(self.frame2, width=self.labelWidth, text=itemNameFormatter(itemName), bg="#121212", fg="white")) fg is text colour


## Speedometers ##
# c = Canvas(self.frame2, width=canvasWidth, height=cavasHeight, bg='white')  # Create canvas for speedometer (right side holding actual speeds)

### Pop Up Windows
# Add Item pop up         top = Toplevel(self.master)  # add bg="#373738" for colour


################## Extra Version Info is at very bottom of program's code ################
# Ver 0.98
# 34. VERY Important fix: The program now saves data and loads data correctly.
#     The problem was that the updateConfigFile() was being run before the dict itself was being updated thus the config file was receiving an empty dict.
#     This was resolved by moving the updateConfigFile() to the addMaxStockValue (line 293).
# 35. Next Item: Add config update to each individual 'edit' button which edits the stock quantity.
#     Added self.updateConfigFile() to updateQuantityInSpeedometerDict()
# 36. deleting function added to edit button for each speedometer

# Ver 0.99
# 37. Added assert to check addItem quanities are always integers. Interesting note: you do not need to use while loops
#     to make loops in tkinter, it simply automatically loops for you. The assert is inside a try block inside the addItemToSpeedometer() sub
#     function. The assert must be here so as to catch potential user errors before anything is added to the dictionary
# 38. Added display of Max Stock to edit item popup window. While doing this I found an odd problem with the stockAndUnit... where
# the max stock value was actually the current value of stock. THis is fixed, the dict now has 3 values {key,[0,0,0]} [Max,Unit speed,current stock]
# editItem() now has display for max stock in the item text option
# editItemLabelTitle = Label(top, text=itemName + '     ' + '(Max Stock = ' + str(self.stockAndUnitValueDict[itemName][0]) + ')', font=('Cambria 14'))
# calcSpeed() now calcs the speed by index 2 [2] the proper spot for current stock:
# speedOfItem = (self.stockAndUnitValueDict[k][2] * self.stockAndUnitValueDict[k][1]) + 320  # multiples the number of stock by unit of speed then adds 320 (320 is actually the strating value for no stock or speed of 0 km/h)
# 39. improved editItem display of full stock and current stock
# 40. added assert to editItem():  try:
#                 assert (str.isdigit(editItemEntry.get())), "Please input digits only."  # Only allow digits from user input, assert evals True continue on, otherwise run except cla.

# Ver 0.99Class
# 41. Added Item class
# 42. Moved non interface functions out to global space
# 43. Renamed all functional uses of speedometerDict to speedometerList
# 44. Code re-arrangement, Moved class Item to sit just under class MainWindow in the code
# 45. Rebuilt deleteItem() for classes
# 46. Adjusted positioning of text display in editItem popup
# 47. Added icon to top left of main window (Speedometer2.png)
# 48. Adjusted size of addItem popup

# Ver 0.992
# 49. moved editItem and deleteItem to global space


speedometerList = []  # List holding all instantiated classes of class Item (items of stock)

stockAndUnitValueDict = {}  #  Dictionary holding certain key values

class MainWindow:
    def __init__(self, master):

        # Master Window
        self.master = master
        self.master.title('Supply Chain Ver. 0.99 Near to Release')
        self.master.geometry("+150+500")  # position of the window in the screen (200x300)
        self.master.geometry("1000x400")  # set initial size of the root window (master) (1500x700);
        # if not set, the frames will fill the master window
        # self.master.attributes('-fullscreen', True)
        screenWidth = self.master.winfo_screenwidth()
        screenHeight = self.master.winfo_screenheight()

        # Instantiate frames
        self.frame0 = Frame(self.master, bd=5, padx=5, bg='#606266')  # Top long row
        self.frame1 = Frame(self.master, bd=5, padx=5, bg='#2a2b2b')  # Side Column
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

        windll.shcore.SetProcessDpiAwareness(1) # used for fixing blurry fonts on win 10 and 11
        #  Instantiate lists for canvases and labels
        self.canvases = []
        self.labels = []

        self.labelWidth = 11  # Width in characters for the label showing name of item (used for item name formatter); increment up if more space needed

        #  Entry widgets
        self.entry = Entry(self.frame0, width='10')
        self.entry.pack()

        self.photo = PhotoImage(file="Speedometer2.png")
        self.master.iconphoto(False, self.photo)

        # self.addStockItemEntry = Entry(self.frame1, width='10')
        # self.addStockItemEntry.pack()
        # self.drawCircleEntry = Entry(self.frame1, width='15')
        # self.drawCircleEntry.pack()

        #######     320 = no stock                 578 = full stock                  258 = full range of values from no stock to full stock  ########
        # list of all speedometer's and item names. eg: {'Blue Pens':[[1,1],[1,2],501],'Staedtler Pens':[[1,3],[1,4],411], Structure: {itemNameAsKey: Value as list of lists [[values for drawCircle() label row and col...],[values for updateSpeedometer() circle row and col...],Quantity of Item]}
        self.speedometerDict = {}
        self.stockAndUnitValueDict ={} # dictionary with key and list with 3 values (note: originally only had 2 values) [number of items constituting max stock, unit of speed for each item, current quantity of stock] Eg: 3 items = max stock, each item takes 86 km/h of speed, current number of items
        print('this is self',self.speedometerDict.items())
        print('this is list',*speedometerList)
        self.circProp = (20,20,80,80,3)  # Properties needed for drawing circle inside of a box (x,y,x,y,outlineWidth)
        self.circleOrigin = self.calcCircleOrigin(self.circProp[0],self.circProp[1],self.circProp[2],self.circProp[3])  # Returns a list of speedometer's values used for drawing line: [xOrigin, yOrigin, radius, width]

        self.button = Button(self.frame1, text="Update Speds", width= 12, command=self.drawCircles)
        self.button.pack()

        self.addItemButton = Button(self.frame1, text="Add Item", width= 12, command=addItem)
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

        loadSpeedometerDict()  # Load up all items from speedometerDict from config file and config2

        print('this is self after load', self.speedometerDict.items())
        print('this is list after loadfunc', *speedometerList)

    def calcSpeed(self,k):  # stockAndUnitValueDict {key:[max,unit speed,current quantity]}
        print('stock dictionary',stockAndUnitValueDict.items())
        speedOfItem = (stockAndUnitValueDict[k][2] * stockAndUnitValueDict[k][1]) + 320  # multiples the number of stock by unit of speed then adds 320 (320 is actually the strating value for no stock or speed of 0 km/h)
        for item in speedometerList:
            if k == item.getName():
                item.setSpeed(round(speedOfItem))
                return

        # speedometerDict[k][2]=round(speedOfItem) # Round value of stock to whole number then insert into dictionary
        # add loop to check every k,v, if k == itemName: v = speedOfItem

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
        sequentially in the order of the speedometerList, then it draws in the dial showing
        the speed of each item.
        """

        #### To get the pixel width of the labels run this test ####
        # labelTest = Label(self.frame2, width=self.labelWidth,text='test')
        # labelTest.grid(row=0,column=3)
        # self.master.update()
        # print(labelTest.winfo_width())  ## output is 83 for labelWidth = 11

        self.clearSpeedoFrame()  # clears the main frame (frame2) of all its widgets (without this clearing function, the speeds will not show when re-drawn a second time...)
        row = 0
        col = 0
        x = self.frame2.winfo_width()
        maxNumOfBoxes=(self.frame2.winfo_width()//240)*2  # get size of main frame (displaying speds), floor divide (//) by size of box,multiply by 2 b/c otherwise boxes will overlap due to nature of layout. 150 = canvas width, 83 = labelWidth. note the calculated values do not work well, hence using 180 as total
        listIndexCounter=0  # used for index access to list of canvases, starting with first canvas, drawing each line, then next canvas

        # self.clearFrame()
        print('this is still self', self.speedometerDict)
        print('this is still list', *speedometerList)
        #  Call drawCircle() for each k,v in speedometerDict.  Creates canvas object, label object, grids them to the screen according to list of lists [[1,1],[1,2]]
        for stockItem in speedometerList:  # {itemNameAsKey: Value as list of lists [[values for drawCircle() label row and col...],[values for updateSpeedometer() circle row and col...]]}
            if col < maxNumOfBoxes:  # Below the maximum of allowed boxes
                self.drawCircle(stockItem.getName(), [row, col], [row,col + 1])  # {'Blue Pens':[[1,1],[1,2],501],...} Note, only sends first two lists, not the final value 501.  Eg: [0,0],[0,1]... [0,2],[0,3]...[0,4],[0,5]
                col += 2  # Increment by 2 so as not to overlap with previous boxes  [0,0],[0,1]... [0,2],[0,3]...[0,4],[0,5]
            else:  # Above the maximum of allowed boxes, sets values for drawing on the next row on the screen and draws circles and labels for the first item of that row
                col = 0  # rest col to 0 so next row starts at far left of screen
                row += 1  # increment up to next row down
                self.drawCircle(stockItem.getName(), [row, col], [row,col + 1])  # {'Blue Pens':[[1,1],[1,2],501],...} Note, only sends first two lists, not the final value 501
                col += 2  # Increment by 2 so as not to overlap with previous boxes in the row [0,0],[0,1]... [0,2],[0,3]...[0,4],[0,5]

            self.calcSpeed(stockItem.getName())  # calculates the proper speed for each item and updates the speedometerList with those proper speeds

        for item in speedometerList:
            self.updateSpeedometer(item.getSpeed(), self.circleOrigin[0], self.circleOrigin[1], self.circleOrigin[2],listIndexCounter)
            listIndexCounter += 1

        # for k , val in self.speedometerDict.items():
        #     print(val)
        #     self.updateSpeedometer(val[2],self.circleOrigin[0], self.circleOrigin[1],self.circleOrigin[2],listIndexCounter)  #  val[2] is the speed, listIndexCounter access the list of canvases holding the speedometers
        #     listIndexCounter+=1

    # for k,val in self.speedometerDict.items():  #  {itemNameAsKey: Value as list of lists [[values for drawCircle() label row and col...],[values for updateSpeedometer() circle row and col...]]}
    #     if col < maxNumOfBoxes:  # Below the maximum of allowed boxes
    #         self.drawCircle(k,[row,col],[row,col+1])  #  {'Blue Pens':[[1,1],[1,2],501],...} Note, only sends first two lists, not the final value 501.  Eg: [0,0],[0,1]... [0,2],[0,3]...[0,4],[0,5]
    #         col+=2  # Increment by 2 so as not to overlap with previous boxes  [0,0],[0,1]... [0,2],[0,3]...[0,4],[0,5]
    #     else:   # Above the maximum of allowed boxes, sets values for drawing on the next row on the screen and draws circles and labels for the first item of that row
    #         col=0  # rest col to 0 so next row starts at far left of screen
    #         row+=1  # increment up to next row down
    #         self.drawCircle(k,[row,col],[row,col+1])  #  {'Blue Pens':[[1,1],[1,2],501],...} Note, only sends first two lists, not the final value 501
    #         col+=2  # Increment by 2 so as not to overlap with previous boxes in the row [0,0],[0,1]... [0,2],[0,3]...[0,4],[0,5]
    #
    #     self.calcSpeed(k) # calculates the proper speed for each item and updates the speedometerDict with those proper speeds

    # draw in the dial showing speeds of each item sequentially. val[2] is the speed



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

        c = Canvas(self.frame2, width=canvasWidth, height=cavasHeight, bg='white')  # Create canvas for speedometer (right side holding actual speeds)
        c.create_oval(self.circProp[0], self.circProp[1],self.circProp[2],self.circProp[3],width=self.circProp[4])
        c.create_text(18, 75, text="0", fill="black",font=('Helvetica 10'))   # draw "0" to left bottom of speedometer
        c.create_text(87, 75, text="100", fill="black",font=('Helvetica 10'))  # draw "100" to right bottom of speedometer


        # create and place edit button for editing values of the stock item
        editButton = Button(c, text='Edit', command=lambda:editItem(itemName))      # create button on the canvas. to give an id: name='itemName'. The command runs editItem with the itemName as parameter
        c.create_window(110, 10, anchor=NW, window=editButton)      # Create a window on the canvas to hold to hold the button

        c.grid(row=cirRowCol[0], column=cirRowCol[1], sticky='nse')
        self.canvases.append(c)  # append the canvas to list

        # self.canvases.append(Canvas(self.frame2, width=canvasWidth, height=cavasHeight, bg='white'))
        self.labels.append(Label(self.frame2, width=self.labelWidth, text=itemNameFormatter(itemName),bg="#121212",fg="white"))

        # Access the last item (most recently appended element) in the canvases list, draw a circle with it, then grid it to the screen
        # self.canvases[-1].create_oval(self.circProp[0], self.circProp[1],self.circProp[2],self.circProp[3],width=self.circProp[4])


        # self.canvases[-1].grid(row=cirRowCol[0], column=cirRowCol[1], sticky='nse')

        #  Draw speed markings on to speedometers. Access most recently added canvas then draw numbers
        # self.canvases[-1].create_text(18, 75, text="0", fill="black", font=('Helvetica 10'))  # draw "0" to left bottom of speedometer
        # self.canvases[-1].create_text(87, 75, text="100", fill="black", font=('Helvetica 10'))  # draw "100" to right bottom of speedometer

        # Access the last item in the labels list and grid it to the screen (probably because the last one is the latest added one)
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
        # print('this is list1',list1)

        for i in range(0, len(list1),1):  # move in steps of two, 0,2,4,6

            #tup = list1[i]  # cache first tup of coordinates, for white colour line (to erase purple line); currently not used, line is not being erased
            nextTup = list1[i]  # cache next tup of coord. for purple line

            colour += 50  # increment colour of speedometer dial to a new colour for each line. 40 gives nice blue to aqua change.  def colourChanger() is also available but not working
            self.canvases[listIndexCounter].create_line(XcircleOrigin, YCircleOrigin,nextTup[0],nextTup[1], fill='#'+str(colour), width=3)  # draw line in circle; values: x and Y of both  ends of line (1st point: horiz, verti, end point horiz, vert. 579 = full stock
            self.master.update()


    # def runResults(self):
    #
    #     self.c.create_line(55, 55, x, y, fill='purple', width=3)  # draw line in circle; values: x and Y of both  ends of line (1st point: horiz, verti, end point horiz, vert.
    #     self.master.update()
    #
    #     # x(t) = r cos(t) + j
    #     # y(t) = r sin(t) + k
    #
    #     btn = ttk.Button(self.master)
    #     print(btn.configure().keys())
    #     print(self.frame1.configure().keys())
    #     # print(dir(self.frame1))

class Item:

    def __init__(self,itemName,quantity,speed,fullStock,lastDateOfUpdate,labRowCol,cirRowCol):
        self.itemName = itemName
        self.quantity = quantity
        self.speed = speed
        self.fullStock = fullStock
        self.lastDateOfUpdate = lastDateOfUpdate
        self.labRowCol = labRowCol
        self.cirRowCol = cirRowCol

    def updateQuantity(self,quantity,lastDateOfUpdate):
        self.quantity = quantity
        self.lastDateOfUpdate = lastDateOfUpdate

    def getSpeed(self):
        return self.speed

    def setSpeed(self,speed):
        self.speed = speed

    def getFullStock(self):
        return self.fullStock

    def getLastDateOfUpdate(self):
        return self.lastDateOfUpdate

    def getQuantity(self):
        return self.quantity

    def getName(self):
        return self.itemName

    def setLabRowCol(self,labRowCol):
        self.labRowCol = labRowCol

    def setCirRowCol(self,cirRowCol):
        self.cirRowCol = cirRowCol

    def getLabRowCol(self):
        return self.labRowCol

    def getCirRowCol(self):
        return self.cirRowCol


def loadSpeedometerDict(): # see updateConfigFile() for saving of files
    global speedometerList  # make this list global so this function can access the list for updating
    global stockAndUnitValueDict
    """
    This method uses pickle to load the dictionaries from config.txt and config2.txt into the speedometerList and stockAndunitValueDict
    """

    # if exists('config.txt'):  # Returns True if file exists
    #     with open('config.txt', 'r') as f1:  # use wb mode so if file does not exist, it will create one
    #         self.speedometerDict=f1.readlines()
    #         f1.close()
    # else:
    #     with open('config.txt', 'w') as f1:  # use wb mode so if file does not exist, it will create one
    #         f1.close()
    #
    # if exists('config2.txt'):  # Returns True if file exists
    #     with open('config2.txt', 'r') as f2:  # use wb mode so if file does not exist, it will create one
    #         self.stockAndUnitValueDict = f2.readlines()
    #         f2.close()
    # else:
    #     with open('config2.txt', 'w') as f2:  # use wb mode so if file does not exist, it will create one
    #         f2.close()

    if exists('config.txt'):  # Returns True if file exists
        with open('config.txt', 'rb') as f: # use wb mode so if file does not exist, it will create one
            speedometerList=p.load(f)
            f.close()
            print('The speedometer dictionary has been loaded from the config file', *speedometerList)
    else:
        with open('config.txt','wb') as f:
            f.close()

    if exists('config2.txt'):  # Returns True if file exists
        with open('config2.txt', 'rb') as f2:
            stockAndUnitValueDict=p.load(f2)
            f2.close()
            print('The Stock dictionary has been loaded from the config2 file', stockAndUnitValueDict.items())
    else:
        with open('config2.txt','wb') as f2:
            f2.close()
    # speedometerDict = stockAndUnitValueDict
    print('this is list below and inside load', *speedometerList)
    # return speedometerDict, stockAndUnitValueDict

def addItem():
    """
    This function opens up a popup window, takes text from the user and adds that text as an item to the Speedometer Dictionary;
    it also updates the config file so that the item is permanently saved
    """
    top = Toplevel()  # add bg="#373738" for colour.  Appears that the root (self.master) is not needed to run this window
    top.geometry("500x150")
    top.title("Add New Item")

    # input for new item in stock
    addItemLabel = Label(top, text="New Item Name", font=('Cambria 14'))  #  Label(top, text="Add New Item", font=('Mistral 18 bold')).place(x=150, y=80)
    addItemLabel.grid(row=1, column=1)  # Note: .grid cannot be placed as a single line code: Label(...).grid(..) as the .grid will actually return None to the program and casue an error

    addItemEntry = Entry(top, width='40')
    addItemEntry.grid(row=1, column=2)

    # addItemEntry.bind('<Return>', lambda event: addItemToSpeedometerDict()) #### TURNED Off for a test, turns out this is not needed.

    # input for setting max stock level for new item
    setMaxStockLabel = Label(top, text="Value of Full Stock", font=('Cambria 14'))  # Label(top, text="Add New Item", font=('Mistral 18 bold')).place(x=150, y=80)
    setMaxStockLabel.grid(row=2,column=1)  # Note: .grid cannot be placed as a single line code: Label(...).grid(..) as the .grid will actually return None to the program and casue an error

    setMaxStockEntry = Entry(top, width='20')
    setMaxStockEntry.grid(row=2, column=2)

    setMaxStockEntry.bind('<Return>', lambda event: combineAddItemAndMaxStock())

    def addItemToSpeedometerDict():

        try:
            # This assert is actually for the addMaxStockValue() but the assert must be checked before reaching the addMaxStock...()
            assert (str.isdigit(setMaxStockEntry.get())), "Please input digits only." # Assert requires integers for max stock value from user in order to continue on

            updateSpeedometerDict(addItemEntry.get())  # enter text from popup window to be used for name of item being added
            # self.updateConfigFile()  # (This line moved as originally it was too early in the update process) update the config file with the new item so that it is saved for the next time opening the program

            completionMes = Label(top, text=addItemEntry.get() + ' added to your list of items', font=('Cambria 14'))
            completionMes.grid(row=3, column=1)

            # addItemEntry.delete(0, END)  # Delete text in entry field. (Note, This deletes the value inside the Entry itself not merely clearing the screen.)

        except AssertionError as i:  # THis loop will have to include the combine Function or the addItem function.

            print('exception reached',i)

            completionMes = Label(top, text=i.args[0], font=('Cambria 14'))
            completionMes.grid(row=4, column=1)

    def addMaxStockValue(): # add max stock to self.stockAndUnitValueDict

        # self.updateSpeedometerDict(addItemEntry.get())  # enter text from popup window to be used for name of item being added
        # self.updateConfigFile()
        # assert (str.isdigit(setMaxStockEntry.get())), "Please input digits only." # moved to earlier function addItemToSpeedometer()

        print('Full stock will be:', setMaxStockEntry.get(), addItemEntry.get())
        # write max stock and set unit value for the given item to the dict.
        updateStockAndUnitValueDict(int(setMaxStockEntry.get()),addItemEntry.get())
        updateConfigFile()  # Update config file (moved from above so that dict is updated first, then conifg file is updated

        completionMes = Label(top, text=setMaxStockEntry.get() + ' set as full stock', font=('Cambria 14'))
        completionMes.grid(row=4, column=1)

        setMaxStockEntry.delete(0, END)  # Delete text in entry field
        addItemEntry.delete(0,END)  # Delete text in entry field. (Note, This deletes the value inside the Entry itself not merely clearing the screen.)

        print(stockAndUnitValueDict.items())


    def combineAddItemAndMaxStock():
        addItemToSpeedometerDict()
        addMaxStockValue()

def editItem(itemName):
    """
    This function opens a new window for editing the total amount of stock available for the given item clicked on.
    It displays the name of the item, current stock, amount for full stock, an entry box, and a completion message if
    stock value is adjusted.
    Inputs: str: itemName, this is the name of the item in stock associated with that button
    """

    top = Toplevel() # top = Toplevel(self.master)
    top.geometry("500x180")
    top.title("Edit Quantity of Stock")

    # Construct Labels
    editItemLabelCurrStock = Label(top, text='Current Stock = ' + str(stockAndUnitValueDict[itemName][2]), font=('Cambria 12'))
    editItemLabelFuStock = Label(top, text='(Full Stock = ' + str(stockAndUnitValueDict[itemName][0]) + ')', font=('Cambria 12')) # Label displaying value for full stock
    editItemLabelTitle = Label(top, text=itemName, font=('Cambria 14'))
    editItemLabel = Label(top, text="New Value", font=('Cambria 14'))  # Label(top, text="Add New Item", font=('Mistral 18 bold')).place(x=150, y=80)
    # editItemLabelTitle = Label(top, text=itemName, font=('Cambria 14'))

    # Grid Labels
    editItemLabelTitle.grid(row=1, column=2)  # Name of item, eg: Plates
    editItemLabelCurrStock.grid(row=2,column=1)  # Current amount of stock
    editItemLabelFuStock.grid(row=3,column=1) # Amount constituting full stock
    editItemLabel.grid(row=4,column=1)  # "New Value",   Note: .grid cannot be placed as a single line code: Label(...).grid(..) as the .grid will actually return None to the program and casue an error
    # editItemLabel.grid_rowconfigure(1, weight=1)
    # editItemLabelTitle.place(x=0.5,y=0.5,anchor='center')

    editItemEntry = Entry(top, width='10')
    deleteItemButton = Button(top, command=lambda:deleteItem(itemName), text="Delete Item", width= 12)

    editItemEntry.grid(row=4, column=2)  # Entry box
    deleteItemButton.grid(row=5,column=1)  # Delete button


    editItemEntry.bind('<Return>', lambda event: updateQuantityInSpeedometerDict(itemName)) # send the itemName to the updateQuantity function

    def updateQuantityInSpeedometerDict(nameOfStock):
        """
        Searches for the correct item in the speedometerList then updates the amount of stock.
        Inputs: str: nameOfStock, which gives the name of the item in the dict to be updated, {'Blue Pens': [[1,1],[1,2],101]} the third value is accessed ie. 101.
        """
        print(nameOfStock)
        print('Initial Set of Values:', *speedometerList)
        print('Initial Set of Values stockAndUnit...:  ', stockAndUnitValueDict.items())
        #self.speedometerDict[nameOfStock][2]=int(editItemEntry.get())  # update value in speedometerdict to value given in popup window

        try:
            assert (str.isdigit(editItemEntry.get())), "Please input digits only."  # Only allow digits from user input, assert evals True continue on, otherwise run except cla.

            stockAndUnitValueDict[nameOfStock][2]=int(editItemEntry.get())  # (Note: this update should be done with the updateStock... function and not directly.) update stock and unit dict ([0]) with amount of stock spedified by user

            completionMes = Label(top, text=nameOfStock + ' stock updated to ' + editItemEntry.get(), font=('Cambria 14'))
            completionMes.grid(row=6, column=2)

            editItemEntry.delete(0,END)  # Delete text in entry field

            print('New Set of Values:  ', *speedometerList)
            print('New Set of Values:  ', stockAndUnitValueDict.items())
            # self.speedometerDict.update({'Blue Pens': [[1,1],[1,2],101]})  # 50 is inside a list of lists, only change the 50 keep other values as is.

            updateConfigFile()  # update the config file to permanetely save stock changes

        except AssertionError as i:  # THis loop will have to include the combine Function or the addItem function.

            print('exception reached', i)

            completionMes = Label(top, text=i.args[0], font=('Cambria 14'))
            completionMes.grid(row=6, column=1)
# def clear_text():
#     text.delete(0, END)


def deleteItem(itemName):
    '''
    This function searches the speedometerList for the item which the user has chosen to delete (from the edit button)
    and then removes that item from the speedometerList. Note, if there happens to be items with duplicate names, all will
    be deleted.

    :input: itemName: name of item from class Item which will be deleted
    :return: None
    '''
    c = 0
    for item in speedometerList:
        if item.getName() == itemName:
            del speedometerList[c]
            del stockAndUnitValueDict[itemName]
            return
        else:
            c+=1
    # del speedometerList[itemName]
    # del stockAndUnitValueDict[itemName]
    # updateConfigFile()
    # print('values deleted')


def updateSpeedometerDict(newItemName):
    """
      This function adds new items to the Speedometer Dictionary from the add item button on the interface;
      it also calculates the next position to place the new item on the screen

      :param newItemName:  str: name of new item to add
      """

    # If the item being added is the very first to the dictionary, place item in first spot on interface grid. Max stock == 578
    if len(speedometerList)==0:
        stockItem = Item(newItemName,10,578,10,'today',[1,0],[1,1])  # instantiate individual item
        speedometerList.append(stockItem)
            # ({newItemName: [[1, 0], [1, 1],578]})
    else: # If item is not the first, place it after the last item
        # get last value from dict (list of lists: :[label(row,col):[2,5],circle(row,col):[2,6]],quantity:583]) from dict. [[1, 13], [1, 14], 401])
        lastItem = speedometerList[-1]  # get last item of stock from the list of items (this is a class object)
        labRowCol = lastItem.getLabRowCol()  # get the labRowCol attribute, [x,y]
        cirRowCol = lastItem.getCirRowCol()
        print(cirRowCol)
        # lastValue = list(self.speedometerDict.items())[-1]
        # increment up appropriate amount to place new item on empty slot on grid, sets a placeholder value of stock
        stockItem = Item(newItemName, 10, 578, 10, 'today', [2, labRowCol[1] + 2], [2, cirRowCol[1] + 2])  # instantiate individual item
        speedometerList.append(stockItem)
        print(*speedometerList)

def updateStockAndUnitValueDict(maxStock,nameOfItem): # put max stock value into StockAndUnitValueDict
    '''
    This function sets the values for max stock and the unit value of stock for each item and writes them to the StockAndUnit...Dict
    :param maxStock: int for what constitute full stock of that item
    :param nameOfItem:  Str: name of item in stock
    '''
    stockAndUnitValueDict.update({nameOfItem: [0,0,0]}) # [max stock value,unit of stock value,current quantity of stock] instantiate item in dictionary with placeholder values of 0,0,0 [max stock value,unit of stock value,current quantity of stock]
    stockAndUnitValueDict[nameOfItem][0] = maxStock
    stockAndUnitValueDict[nameOfItem][1] = 258/maxStock  # 258 is the total range of speed

    print('stockAndUnitValueDict contents', stockAndUnitValueDict.items())

def updateConfigFile():  # See loadSpeedomterDict for other side of process

    """
    This method writes the speedometerList into the config.txt file
    """
    #
    # with open('config.txt', 'w') as f1:
    #     self.speedometerDict=f1.writelines()
    #     f1.close()
    # with open('config2.txt', 'w') as f2:
    #     self.speedometerDict=f2.writelines()
    #     f2.close()

    # original approach using pickle

    with open('config.txt', 'wb') as f: # Open in wb mode which deletes all contents previously saved and will write new contents
        p.dump(speedometerList, f)
        print('updating config file', *speedometerList)
        f.close()
    with open('config2.txt', 'wb') as f2:
        p.dump(stockAndUnitValueDict, f2)
        print('updating config2 file', stockAndUnitValueDict.items())
        f2.close()


class Item:

    def __init__(self,itemName,quantity,speed,fullStock,lastDateOfUpdate,labRowCol,cirRowCol):
        self.itemName = itemName
        self.quantity = quantity
        self.speed = speed
        self.fullStock = fullStock
        self.lastDateOfUpdate = lastDateOfUpdate
        self.labRowCol = labRowCol
        self.cirRowCol = cirRowCol

    def updateQuantity(self,quantity,lastDateOfUpdate):
        self.quantity = quantity
        self.lastDateOfUpdate = lastDateOfUpdate

    def getSpeed(self):
        return self.speed

    def setSpeed(self,speed):
        self.speed = speed

    def getFullStock(self):
        return self.fullStock

    def getLastDateOfUpdate(self):
        return self.lastDateOfUpdate

    def getQuantity(self):
        return self.quantity

    def getName(self):
        return self.itemName

    def setLabRowCol(self,labRowCol):
        self.labRowCol = labRowCol

    def setCirRowCol(self,cirRowCol):
        self.cirRowCol = cirRowCol

    def getLabRowCol(self):
        return self.labRowCol

    def getCirRowCol(self):
        return self.cirRowCol


# def instantiateItem(itemName,quantity,speed,fullStock,lastDateOfUpdate):
#     newItem = Item(itemName,quantity,speed,fullStock,lastDateOfUpdate)
#     speedometerDict.append(newItem)

def main():
    root = Tk()
    MainWindow(root)

    root.mainloop()


main()


# Version 0.1
# 1. This is the first point where this project takes real formation. It opens a main window and displays speedometers showing the amount of
#     quantity in stock.  The speedometer itself works although has not been scaled yet to show mulitple items independently

# Version 0.2
# 2. Changed speedometerList to a dict. speedometerDict. This will make updates to stock items easier as the item
#       can be accessed by its key.

# Version 0.25
# 3.  Added list into speedometerDict which calls the updateSpeedometer method

# Version 0.3
# 4.  Adds pickle functi on to update config file
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
# 27. moved the:
#             setMaxStockEntry.delete(0, END)  # Delete text in entry field
#             addItemEntry.delete(0,END)  # Delete text in entry field. (Note, This deletes the value inside the Entry itself not merely clearing the screen.)
# to be together inside the addMaxStockValue() function so both are deleted at the same spot and also so that the Entry field contents is still usable when needed
# for populating the dictionary StockandUnitValue.

# Ver 0.96 (start considering actual program flow from the very beginning of a user building inventory
# 28. Empty the speedometerDict (which holds all key values of items) and build it sequentially from the user interface.
# 29. added clearSpeedoframes() to drawCircles() method in order to fix drawing of speeds. originally if you pressed update speds more than once, it would not properly
# draw those speeds but would leave them all white.
# 30. Delete speedomterdict contents
# 31. fix index error when adding first item to updateSpeedometerDict.
# 32. Round values of stock to whole numbers then insert them into the speedometerdict (key fix)

# Ver 0.97
# 33. Improve the config file: upon opening the program, load speedometerDict and StockAndUnitValueDict to the program


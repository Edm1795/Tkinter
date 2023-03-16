from tkinter import *


class MainWindow:
    def __init__(self, master,title,numOfFrames,backGroundColour,textBoxColour,textColour):
        print('start')
        # Master Window
        self.master = master
        self.title = title
        self.master.title(self.title)
        self.numOfFrames = numOfFrames
        self.backGroundColour = backGroundColour
        self.textBoxColour = textBoxColour
        self.textColour = textColour
        self.frameCount = 0
        self.frames = []
        self.text = []
        self.textCount = 0
        self.master.geometry("+100+100")  # position of the window in the screen (200x300)
        # self.master.geometry("700x800")  # set size of the root window (master) (1500x700);
        # if not set, the frames will fill the master window

        # Instantiate the frames
        while self.frameCount < self.numOfFrames:
            self.frames.append(Frame(self.master, bd=5, padx=5, bg=self.backGroundColour))
            self.frameCount += 1

        # Place the frames on the grid and configure the weighting of the frames
        c = 0
        for frame in self.frames:
            frame.grid(row=1, column=c,sticky = "nsew")
            frame.grid_columnconfigure(c, weight=1)  # ALlows frames to expand as master window expands
            # frame.grid_rowconfigure(1, weight=1)
            # frame.grid_propagate(0)
            c += 1

        # Make frames expand as you resize the window. Conf the grid on the master window
        for num in range(0,self.numOfFrames):
            self.master.grid_columnconfigure(num, weight=1)


        # Create text boxes
        for frame in self.frames:
            t=Text(frame, height=60, width=15, bg=self.textBoxColour, fg=self.textColour)
            self.text.append(t)
            # t.grid_columnconfigure(0, weight=1)
            # t.grid_rowconfigure(0, weight=1)
            
        while self.textCount < self.numOfFrames:
            self.text[self.textCount].pack()
            self.textCount += 1
        print('done')

        # scrollBar = Scrollbar(self.master, command=self.text[0].yview)
        # scrollBar.grid(row=1, column=0, sticky='nsew')
        # self.text[0]['yscrollcommand'] = scrollBar.set

    def insertText(self, column, text):
        """
        This method inserts text into the specified column
        inputs: column as integer; text as string
        """
        self.text[column].insert(INSERT, text)


        # Set up text boxes
        self.text1 = Text(self.frames[0],bg='#113333', fg='white')
        print(self.text1.configure().keys())
        # self.text1.insert(INSERT, 'The complete works of Shakespeare were written by William')
        # # self.text1.grid_columnconfigure(0, weight=1)
        # self.text1.grid_rowconfigure(0, weight=2)
        # self.text1.config(wrap='word')
        # self.text1.pack()
        #
        # self.text2 = Text(self.frame2, height=30, width=frameWidth, bg='#112233', fg='white')
        # self.text2.insert(INSERT, '')
        # # self.text2.grid_columnconfigure(0, weight=1)
        # self.text2.grid_rowconfigure(0, weight=2)
        # self.text2.config(wrap='word')
        # self.text2.pack()
        #
        # self.text3 = Text(self.frame3, height=30, width=frameWidth, bg='#112233', fg='white')
        # self.text3.insert(INSERT, '')
        # # self.text3.grid_columnconfigure(0, weight=1)
        # self.text3.grid_rowconfigure(0, weight=2)
        # self.text3.config(wrap='word')
        # self.text3.pack()
        #
        # self.text4 = Text(self.frame4, height=30, width=frameWidth, bg='#112233', fg='white')
        # self.text4.insert(INSERT, '')
        # # self.text4.grid_columnconfigure(0, weight=1)
        # self.text4.grid_rowconfigure(0, weight=2)
        # self.text4.config(wrap='word')
        # self.text4.pack()
        #
        # btn = ttk.Button(master)
        # print(btn.configure().keys())
        # print(self.frame1.configure().keys())
        # # print(dir(self.frame1))
        #










from tkinter import *


class MainWindow:
    def __init__(self, master):

        # Master Window
        self.master = master
        self.master.title('Supply Chain Ver. 0.95 In the Works')
        self.master.geometry("+150+500")  # position of the window in the screen (200x300)
        self.master.geometry("1000x400")  # set initial size of the root window (master) (1500x700);
        # if not set, the frames will fill the master window
        # self.master.attributes('-fullscreen', True)
        self.addItemButton = Button(self.master, text="Add Item", width=12, command=self.addItem)
        self.addItemButton.pack()

    def addItem(self):
        """
        This function opens up a popup window, takes text from the user and adds that text as an item to the Speedometer Dictionary;
        it also updates the config file so that the item is permanently saved
        """
        top = Toplevel(self.master)
        top.geometry("400x150")
        top.title("Add New Item")

        # input for new item in stock
        addItemLabel = Label(top, text="Add New Item", font=(
            'Cambria 12'))  # Label(top, text="Add New Item", font=('Mistral 18 bold')).place(x=150, y=80)
        addItemLabel.grid(row=1,
                          column=1)  # Note: .grid cannot be placed as a single line code: Label(...).grid(..) as the .grid will actually return None to the program and casue an error

        addItemEntry = Entry(top, width='40')
        # addItemEntryCache = addItemEntry.get()
        addItemEntry.grid(row=1, column=2)

        addItemEntry.bind('<Return>', lambda
            event: addItemToSpeedometerDict())  # note: this function will clear data inside the addItemEntry thus making access to that data null

        addItemEntryCache = addItemEntry.get()  # cache the name of the new item (to be used when updatingthe Stock and unit value dict which at that time the contents of addItemEntry will have been cleared)

        print('1.item name at first mention:            ', addItemEntry.get())
        print('1.item name at first mention cache:', addItemEntryCache)

        # addItemEntry.delete(0, END)  # Delete text in entry field.  This will clear contents in the addItemEntry itself, not merely in the entry field on the interface.

        addItemEntry.delete(0,
                            END)  # Delete text in entry field.  This will clear contents in the addItemEntry itself, not merely in the entry field on the interface.

        print('2.item name at first mention:            ', addItemEntry.get())
        print('2.item name at first mention cache:', addItemEntryCache)

        # input for setting max stock level for new item
        setMaxStockLabel = Label(top, text="Value for Max Stock", font=(
            'Cambria 12'))  # Label(top, text="Add New Item", font=('Mistral 18 bold')).place(x=150, y=80)
        setMaxStockLabel.grid(row=2,
                              column=1)  # Note: .grid cannot be placed as a single line code: Label(...).grid(..) as the .grid will actually return None to the program and casue an error

        setMaxStockEntry = Entry(top, width='40')
        setMaxStockEntry.grid(row=2, column=2)

        setMaxStockEntry.bind('<Return>', lambda event: combineAddItemAndMaxStock(addItemEntryCache))

        def addItemToSpeedometerDict():
            self.updateSpeedometerDict(
                addItemEntry.get())  # enter text from popup window to be used for name of item being added
            self.updateConfigFile()

            completionMes = Label(top, text=addItemEntry.get() + ' added to your list of items', font=('Cambria 12'))
            completionMes.grid(row=3, column=1)

            print('1.item name at first mention:            ', addItemEntry.get())
            print('1.item name at first mention cache:', addItemEntryCache)

            # addItemEntry.delete(0, END)  # Delete text in entry field.  This will clear contents in the addItemEntry itself, not merely in the entry field on the interface.

            print('2.item name at first mention:            ', addItemEntry.get())
            print('2.item name at first mention cache:', addItemEntryCache)

        def addMaxStockValue(nameOfItem):  # add max stock to self.stockAndUnitValueDict

            # self.updateSpeedometerDict(addItemEntry.get())  # enter text from popup window to be used for name of item being added
            # self.updateConfigFile()

            self.updateStockAndUnitValueDict(int(setMaxStockEntry.get()),
                                             nameOfItem)  # write max stock and set unit value for the given item to the dict.

            completionMes = Label(top, text=setMaxStockEntry.get() + ' set as max stock', font=('Cambria 12'))
            completionMes.grid(row=4, column=1)

            setMaxStockEntry.delete(0, END)  # Delete text in entry field

        def combineAddItemAndMaxStock(nameOfItem):
            addItemToSpeedometerDict()
            addMaxStockValue(nameOfItem)

def main():
    root = Tk()
    MainWindow(root)

    root.mainloop()


main()


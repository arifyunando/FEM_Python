from tkinter import *
from PIL import ImageTk, Image  # Picture Processing library

"""
Instatantiate new window and define its properties
"""
# Create Window
root = Tk()
# Create Title
root.title('ME362')
# Define Default Window Size 
root.geometry("800x800")    #(Width x Height)
# root.state('zoomed')        #Fullscreen


"""
Widgets
"""
# Label
aFont = ("Century Gothic", 30)
test_label1 = Label(root, text="This is a label", font=aFont) #(window location, the label)
test_label1.grid(row=0, column=0)                       #(grid position of the widgets)

test_label2 = Label(root, text="This also a label")     #(window location, the label)
test_label2.grid(row=1, column=0)                       #(grid position of the widgets)

# Frame 
frame = LabelFrame(root)
frame.grid(row=0, column=1, padx= 30, pady=32, ipadx=60, ipady=62)

label_inframe = Label(frame, text="This also a label")  #(window location, the label)
label_inframe.grid(row=1, column=0)                     #(grid position of the widgets)

#button
n = 0
def a_function(an_argument):
    print(f'current value = {an_argument}')
    global n
    n += 1

myButton = Button(
    root,                   # Location
    text="Button",          # Text in the button
    font=('Arial', 15),     # Font style
    command= lambda: a_function(n),     # Function ran on click
    fg = 'blue',            # foreground color (in this case the text)
    bg = 'salmon',          # background color
    activebackground='red'  # background color while pressed
    )
myButton.grid(row = 2, column = 0)

# Entry Boxes
entry = Entry(
    root, 
    width = 20, 
    font = aFont, 
    justify="center", 
    state='readonly'
    )
entry.grid(row=1, column=1)
entry.configure(state='normal')
entry.insert(0, '23')
entry.configure(state='readonly')

value = entry.get()
print(value)

# Check Box
def checkFunction(var):
    print(var)

varCheck = StringVar()
varCheck.set("On")

checkBox = Checkbutton(
    root, 
    text='Switch', 
    onvalue= "On", 
    offvalue= "Off", 
    variable=varCheck,
    command= lambda: checkFunction(varCheck.get())
    )
checkBox.grid(row = 2, column= 1)

# Sliders
def scaleFunction(args):
    global slider
    global sliderEntry
    sliderEntry.configure(state='normal')
    sliderEntry.delete(0, END)
    sliderEntry.insert(0, f'{10**(slider.get()/10):.2f}')
    sliderEntry.configure(state='readonly')

sliderFrame = LabelFrame(root)
sliderFrame.grid(row=3, column=0, padx= 30, pady=32, ipadx=60, ipady=62)

slider = Scale(
    sliderFrame, 
    from_=-20, 
    to=20, 
    orient="horizontal", 
    width=20, 
    length=200,
    showvalue=0,
    command=scaleFunction
    )
slider.grid(row=4, column=1)

sliderEntry = Entry(
    sliderFrame, 
    width = 10,
    borderwidth= 5,
    font = ('verdana', 15), 
    justify="center", 
    state='readonly'
    )
sliderEntry.grid(row=1, column=1)
sliderEntry.configure(state='normal')
sliderEntry.insert(0, 1.00)
sliderEntry.configure(state='readonly')

# Radio Button
radioFrame = LabelFrame(root)
radioFrame.grid(row=4, column=0, padx= 30, pady=32)

colorMapVar = StringVar()
colorMapVar.set('jet')

radioJet = Radiobutton(
    radioFrame, 
    variable=colorMapVar, 
    text='Jet', 
    value='jet',
    font=('arial',10))
radioCopper = Radiobutton(
    radioFrame, 
    variable=colorMapVar, 
    text='Copper', 
    value='copper')
radioCool = Radiobutton(
    radioFrame, 
    variable=colorMapVar, 
    text='Cool', 
    value='cool')

'Optionally, use image instead of text beside the radio button'
# imageJet = Image.open('jet.png')
# imageCopper = Image.open('copper.png')
# imageCool = Image.open('cool.png')

# imageJet = ImageTk.PhotoImage(imageJet.resize((100,20)))
# imageCopper = ImageTk.PhotoImage(imageCopper.resize((100,20)))
# imageCool = ImageTk.PhotoImage(imageCool.resize((100,20)))

# radioJet.configure(image=imageJet)
# radioCopper.configure(image=imageCopper)
# radioCool.configure(image=imageCool)

radioJet.grid(row=0, column=0)
radioCopper.grid(row=1, column=0)
radioCool.grid(row=2, column=0)

# Keep it open
root.mainloop()
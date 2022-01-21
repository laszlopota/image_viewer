# Imports
from tkinter import *
from tkinter import filedialog
from time import sleep
from PIL import ImageTk, Image

# Setting up the window
minWidth = 192*4
minHeight = 108*4

root = Tk()
root.configure(background='white')
root.minsize(minWidth, minHeight)
root.title('Image viewer')
root.iconbitmap('python.ico')

# Opening images
imagesPath = []
imagesNames = []
imagesList = []
imagesPhotoList = []
def open_images():
    global imagesPath, imagesNames, imagesList, imagesPhotoList

    file_path = filedialog.askopenfilenames()
    for image in file_path:
        imagesPath.append(image)
        if '/' in imagesPath[-1]:
            index = len(imagesPath[-1])
            for character in imagesPath[-1][::-1]:
                index -= 1
                if character == '/':
                    imagesNames.append(imagesPath[-1][index + 1:])
                    break
        else:
            imagesNames.append(imagesPath[-1])
        imagesList.append((Image.open(image)))
        imagesPhotoList.append(ImageTk.PhotoImage(imagesList[-1]))

    if len(imagesList) != 0:
        resize_images()
        show_first_image()

# Resizing images
def resize_images():
    global imagesList, imagesPhotoList
    for i in range(len(imagesList)):
        currentImageWidth, currentImageHeight = imagesList[i].size
        newImageHeight = root.winfo_height() - 50
        newImageWidth = currentImageWidth * newImageHeight / currentImageHeight
        imagesList[i] = imagesList[i].resize((int(newImageWidth), int(newImageHeight)))
        imagesPhotoList[i] = ImageTk.PhotoImage(imagesList[i])


# Creating the image viewer
imageIndex = 0
def show_first_image():
    global imagesPath, imagesNames, imagesList, imageIndex, imageShow, nameLabel
    imageShow.grid_forget()
    imageShow = Label(
        root, image=imagesPhotoList[imageIndex], background='white', width=root.winfo_width(),
        height=root.winfo_height() - 50, border=0
    )
    imageShow.grid(row=0, column=0, columnspan=3)
    nameLabel['text'] = imagesNames[imageIndex]

def previous_image():
    global imagesPath, imagesNames, imagesList, imageIndex, imageShow, nameLabel
    if imageIndex != 0:
        imageShow.grid_forget()
        imageIndex -= 1
        imageShow = Label(
            root, image=imagesPhotoList[imageIndex], background='white', width=root.winfo_width(),
            height=root.winfo_height() - 50, border=0
        )
        imageShow.grid(row=0, column=0, columnspan=3)
        nameLabel['text'] = imagesNames[imageIndex]

def next_image():
    global imagesPath, imagesNames, imagesList, imageIndex, imageShow, nameLabel
    if imageIndex != len(imagesList)-1 and imageIndex != len(imagesList):
        imageShow.grid_forget()
        imageIndex += 1
        imageShow = Label(
            root, image=imagesPhotoList[imageIndex], background='white', width=root.winfo_width(),
            height=root.winfo_height() - 50, border=0
        )
        imageShow.grid(row=0, column=0, columnspan=3)
        nameLabel['text'] = imagesNames[imageIndex]


# Start page and base widgets
plusImage = Image.open('plus.jpg')
plusImage = plusImage.resize((150, 150))
plusImage = ImageTk.PhotoImage(plusImage)

imageShow = Label(
    root, image=plusImage, background='white', width=root.winfo_width(), height=root.winfo_height() - 50, border=0
)
imageShow.grid(row=0, column=0, columnspan=3)
nameLabel = Label(
    root, text='Select images!', width=int(root.winfo_width()/20), background='white', font=('Helvetica', 12)
)
nameLabel.grid(row=1, column=1)

buttonPrevious = Button(root, text='<<', border=0, width=20, height=2, background='white', command=previous_image)
buttonPrevious.grid(row=1, column=0)

buttonNext = Button(root, text='>>', border=0, width=20, height=2, background='white', command=next_image)
buttonNext.grid(row=1, column=2)

# Controls
imageShow.bind('<Button-1>', lambda event: open_images())
root.bind('<Up>', lambda event: next_image())
root.bind('<Right>', lambda event: next_image())
root.bind('<Down>', lambda event: previous_image())
root.bind('<Left>', lambda event: previous_image())

windowWidth = root.winfo_width()
windowHeight = root.winfo_height()
def get_window_size():
    global windowWidth, windowHeight
    windowWidth = root.winfo_width()
    windowHeight = root.winfo_height()

def on_resize():
    global imageShow, nameLabel, buttonPrevious, buttonNext, windowWidth, windowHeight
    if root.winfo_width() != windowWidth or root.winfo_height() != windowHeight:
        imageShow.grid_forget()
        if len(imagesList) != 0:
            resize_images()
            imageShow = Label(
                root, image=imagesPhotoList[imageIndex], background='white', width=root.winfo_width(),
                height=root.winfo_height() - 50, border=0
            )
            nameLabel['text'] = imagesNames[imageIndex]
        else:
            imageShow = Label(
                root, image=plusImage, background='white', width=root.winfo_width(), height=root.winfo_height() - 50,
                border=0
            )
            imageShow.bind('<Button-1>', lambda event: open_images())
            nameLabel['text'] = 'Select images!'
        imageShow.grid(row=0, column=0, columnspan=3)
        nameLabel.grid(row=1, column=1)

        buttonPrevious = Button(
            root, text='<<', border=0, width=20, height=2, background='white', command=previous_image
        )
        buttonPrevious.grid(row=1, column=0)

        buttonNext = Button(
            root, text='>>', border=0, width=20, height=2, background='white', command=next_image
        )
        buttonNext.grid(row=1, column=2)


root.bind('<Motion>', lambda event: get_window_size())
root.bind('<Configure>', lambda event: on_resize())

# Running the application
mainloop()

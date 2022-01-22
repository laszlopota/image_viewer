# Imports
from tkinter import *
from tkinter import filedialog
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
        resize_image()
        change_image()

# Resizing images
def resize_image():
    global imagesList, imagesPhotoList, imageIndex
    currentImageWidth, currentImageHeight = imagesList[imageIndex].size
    newImageHeight = root.winfo_height() - 50
    newImageWidth = currentImageWidth * newImageHeight / currentImageHeight
    imagesList[imageIndex] = imagesList[imageIndex].resize((int(newImageWidth), int(newImageHeight)))
    imagesPhotoList[imageIndex] = ImageTk.PhotoImage(imagesList[imageIndex])


# Creating the image viewer
imageIndex = 0
def change_image():
    global imageLabel, nameLabel, imagesPhotoList, imageIndex, imagesNames

    resize_image()
    imageLabel.grid_forget()
    imageLabel = Label(
        root, image=imagesPhotoList[imageIndex], background='white', width=root.winfo_width(),
        height=root.winfo_height() - 50, border=0
    )
    imageLabel.grid(row=0, column=0, columnspan=3)
    nameLabel['text'] = imagesNames[imageIndex]

def previous_image():
    global imageIndex
    if imageIndex != 0:
        imageIndex -= 1
        change_image()

def next_image():
    global imageIndex, imagesList
    if imageIndex != len(imagesList)-1 and imageIndex != len(imagesList):
        imageIndex += 1
        change_image()


# Start page and base widgets
plusImage = Image.open('plus.jpg')
plusImage = plusImage.resize((150, 150))
plusImage = ImageTk.PhotoImage(plusImage)

imageLabel = Label(
    root, image=plusImage, background='white', width=root.winfo_width(), height=root.winfo_height() - 50, border=0
)
imageLabel.grid(row=0, column=0, columnspan=3)
nameLabel = Label(
    root, text='Select images!', width=int(root.winfo_width()/20), background='white', font=('Helvetica', 12)
)
nameLabel.grid(row=1, column=1)

buttonPrevious = Button(root, text='<<', border=0, width=20, height=2, background='white', command=previous_image)
buttonPrevious.grid(row=1, column=0)

buttonNext = Button(root, text='>>', border=0, width=20, height=2, background='white', command=next_image)
buttonNext.grid(row=1, column=2)

# Controls
imageLabel.bind('<Button-1>', lambda event: open_images())
root.bind('<Up>', lambda event: next_image())
root.bind('<Right>', lambda event: next_image())
root.bind('<Down>', lambda event: previous_image())
root.bind('<Left>', lambda event: previous_image())

def on_resize():
    global imageLabel, nameLabel, buttonPrevious, buttonNext
    global imagesPhotoList, imagesList, imagesNames, imageIndex
    imageLabel.grid_forget()
    if len(imagesList) != 0:
        resize_image()
        imageLabel = Label(
            root, image=imagesPhotoList[imageIndex], background='white', width=root.winfo_width(),
            height=root.winfo_height() - 50, border=0
        )
    else:
        imageLabel = Label(
            root, image=plusImage, background='white', width=root.winfo_width(), height=root.winfo_height() - 50,
            border=0
        )
        imageLabel.bind('<Button-1>', lambda event: open_images())
    imageLabel.grid(row=0, column=0, columnspan=3)


root.bind('<Motion>', lambda event: on_resize())

# Running the application
mainloop()

#coding:utf-8

from Tkinter import *
from USB_IO_Card_object import *

from PIL.Image import open
from PIL.ImageTk import PhotoImage

Usb = USB2016()

##def UsbIoDeviceOpen():
##    if UsbIoInitial() == True:
##        Info.insert(1.0,"usb io device initial success!\n")    
##    pass
##
##def UsbIoDeviceClose():
##    if UsbIoUninitial() == True:
##        Info.insert(1.0,"usb io device close success!\n")    
##    pass

top = Tk()



frame00 = Frame(top, width = 150, height = 450)
frame00.grid(column = 0,row = 0)
frame00_01 = Frame(frame00, width = 0, height = 300, bg = 'yellow')
frame00_01.grid(column = 0,row = 0)
frame00_02 = Frame(frame00, width = 150, height = 300, bg = 'green')
frame00_02.grid(column = 1,row = 0,ipadx = 5)
frame00_03 = Frame(frame00, width = 150, height = 300, bg = 'red')
frame00_03.grid(column = 2,row = 0, ipadx = 10)


LedGreen = PhotoImage(open("green_led.jpg"))
LedGray = PhotoImage(open("gray_led.jpg"))
LedLabel = Label(frame00_01, image=LedGray)
LedLabel.pack(padx=20,anchor=CENTER)

def RefreshLed():
    Usb.init()
    if Usb.device_exist:
        LedLabel .config( image=LedGreen)
    else:
        LedLabel .config( image=LedGray)
        
def cleanUp():
    Usb.CloseDevice()
    Usb.FreeDeviceList()
    Usb.UsbIoUninitial()
    top.destroy()     

WorkLed = 0
def setWorkLed():
    global WorkLed
    if WorkLed == 0:
        WorkLed = 1
    else:
        WorkLed = 0
    Usb.SetWorkLedMode(WorkLed)
    

    
ResetButton = Button(frame00_02, text = '状态指示灯',command = setWorkLed)#,command = UsbIoDeviceOpen)
ResetButton.grid(column = 0, row = 0)
##EmptyLabel = Label(frame00_02, text = '   ')
##EmptyLabel.grid(column = 1, row = 0)
RefreshButton = Button(frame00_02, text = '刷新', command = RefreshLed)
RefreshButton.grid(column = 2, row = 0)

##EmptyLabel = Label(frame00_02, text = '   ')
##EmptyLabel.grid(column = 1, row = 1)

def write0xff():
    for i in range(16):
        Usb.WritePinValue(i,1)         


Write0xFFButton = Button(frame00_02, text = '全高',command = write0xff)
Write0xFFButton.grid(column = 0, row = 2)
##EmptyLabel = Label(frame00_02, text = '   ')
##EmptyLabel.grid(column = 1, row = 2)

def write0x00():
    for i in range(16):
        Usb.WritePinValue(i,0) 

Write0x00Button = Button(frame00_02, text = '全低',command = write0x00)
Write0x00Button.grid(column = 2, row = 2)

##EmptyLabel = Label(frame00_02, text = '   ')
##EmptyLabel.grid(column = 1, row = 3)

ReadButton = Button(frame00_02, text = 'Read')
ReadButton.grid(column = 0, row = 4)
##EmptyLabel = Label(frame00_02, text = '   ')
##EmptyLabel.grid(column = 1, row = 4)
TestButton = Button(frame00_02, text = 'Test')
TestButton.grid(column = 2, row = 4)


Bit = {}
BitVar = {}
BitValueOld={}
for i in range(16):
    BitValueOld[i]=0
    
def checkButton():    
    for i in range(16):
        if BitVar[i].get()!=BitValueOld[i]:
            Usb.WritePinValue(i,BitVar[i].get())
            BitValueOld[i] = BitVar[i].get()

for i in range(16):
    BitVar[i] = IntVar()
    BitVar[i].set(Usb.pin_info16_casted[i].pinValue)
    BitValueOld[i] = BitVar[i].get()
    Bit['Bit' + str(i)] = Checkbutton(frame00_03,variable = BitVar[i], text = 'Bit' + str(i), command = checkButton)
    Bit['Bit' + str(i)].grid(row = i%8, column = int(i/8))




frame_text = Frame(top, width = 450, height = 150)#, bg = 'purple')
frame_text.grid(column = 0,row = 1)

Info = Text(frame_text, width = 50, height = 10)
Info.pack(padx=10,pady=10)

top.title("X202测试程序")

#top.minsize(400,400)

#top.configure(bg = "green")
RefreshLed()
top.protocol("WM_DELETE_WINDOW",cleanUp)
top.mainloop()

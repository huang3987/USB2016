#coding:utf-8

#CopyRight (c) 1997-2016 Mason Electronic Co., Ltd
#Author:  Huang Li
## **************************
##大族明信/运营部/生产中心/工程部/黄利
##内网Email：huangl@mason.com   
##微信号: huang39872007
##固话：0755-26736083  分机：6083
##手机：13798288730     短号：6730
##***************************



from ctypes import *
import ctypes
import time

(INPUT_MODE, OUTPUT_MODE) = (0, 1)
(LOW_LEVEL, HIGHT_LEVEL) = (0, 1)
(NO_INNER_PULL_UP, INNER_PULL_UP) = (0, 1)
(CLOSE_WORK_LED, OPEN_WORK_LED) = (0, 1)

class USB2016:
    "class for the usb device"
    
    class pin_info(Structure):
        _fields_ = [
                ("pinIndex", c_uint),
                ("pinMode",  c_uint),
                ("pinValue",  c_uint)
                            ]
        
    class device_list:
        pass
    
    class device_info(Structure):
        pass
    
    device_info._fields_ = [
               ("serial_number", c_char_p),
                ("device_path", c_char_p),
                ("next", POINTER(device_info) )
                        ]
    
    pin_info16 = (pin_info * 16)()

    io_exist = False
    list_exist = False
    device_exist = False
    
    def __init__(self):
        
        self.io = CDLL("usb_io_interface.dll")

        if self.device_exist:
            self.CloseDevice()
        if self.list_exist:
            self.FreeDeviceList()
        if self.io_exist:
            self.UsbIoUninitial()
            
        if self.UsbIoInitial():
            print "Usb Io Initial Success!"
            if self.GetDeviceList():
                print "Get Usb Device List Success!"
                if self.GetDeviceHandle():
                    print "Get Usb Device Handle Success!"
                    self.GetAllPinInfo()
                else:
                    print "Get Usb Device Handle Failed!"    
            else:
                print "Get Usb Device List Failed!"
        else:
            print "Usb Io Initial Failed!"


        
    def init(self):
        self.__init__()
        
    def UsbIoInitial(self):
        if self.io.usb_io_init() == 0:
            self.io_exist = True
            return True 
        else:
            self.io_exist=False
            return False

    def GetDeviceList(self):
        self.io.usb_io_get_device_list.restype = POINTER(self.device_info)
        if self.io_exist:
            self.device_list = self.io.usb_io_get_device_list()
            try:
                value_test =  self.device_list.contents
            except ValueError:
                self.list_exist = False
                return False
            finally:
                pass
            self.list_exist =  True            
            return self.device_list
        else:
            self.list_exist = False
            return False

    def GetDeviceHandle(self):
        if self.io_exist and self.list_exist:
            self.handle = self.io.usb_io_open_device(self.device_list)
            if self.handle != 0:
                self.device_exist = True
                print "usb device %s open success!" % self.device_list.contents.serial_number
                return self.handle
            else:
                self.device_exist = False
                print "usb device  open failed!"
                return False
        else:
            self.device_exist = False
            print "system is not ready for usb device  open!"
            return False

    def SetWorkLedMode(self, led_mode = OPEN_WORK_LED):
        self.led_mode = led_mode
        if self.io_exist and self.list_exist and self.device_exist:
            return_code = self.io.usb_io_set_work_led_mode( self.handle, led_mode)
            if return_code == 0:
                print "set led mode success!"
                return True
            else:
                print "set led mode failed!"
                return False
        else:
            print "system is not ready for open the work led!"
            



    def GetAllPinInfo(self):
         if self.io_exist and self.list_exist and self.device_exist:
            return_code = self.io.usb_io_get_all_pin_info(self.handle, self.pin_info16)
            if return_code == 0:
                self.pin_info16_casted = cast(self.pin_info16, POINTER(self.pin_info))
                for n in range(16):
                    print "Index of pin %d  is %d" % (n, self.pin_info16_casted[n]. pinIndex)
                    print "Mode of pin %d is %d "% (n, self.pin_info16_casted[n]. pinMode)
                    print "Value of pin %d is %d \n"% (n, self.pin_info16_casted[n]. pinValue)
                return True

    def SetPinMode(self, pinIndex = 0, pin_mode = INPUT_MODE, input_pin_mode = INNER_PULL_UP):   
        if self.io_exist and self.list_exist and self.device_exist:
            return_code = self.io.usb_io_set_pin_mode(self.handle, pinIndex, pin_mode, input_pin_mode )
            if return_code == 0:
                print "set pin %s mode %s success, input pin mode is %s" % (str(pinIndex), str(pin_mode),str(input_pin_mode))
                self.pin_info16_casted[pinIndex].pinMode = pin_mode
                return True
        
    

    def WritePinValue(self, outputPinIndex = 0, pin_level = LOW_LEVEL):
        self.outputPinIndex = outputPinIndex
        self.pin_level = pin_level
        
        if self.io_exist and self.list_exist and self.device_exist:
            if self.SetPinMode(pinIndex=outputPinIndex,pin_mode=OUTPUT_MODE):
                return_code = self.io.usb_io_write_output_pin_value(self.handle, outputPinIndex, pin_level)
            if return_code == 0:
                print "Write pin %s success, the value is %s" % (str(outputPinIndex), str(pin_level))
                self.pin_info16_casted[outputPinIndex].pinValue = pin_level
                return True
        

    
    def ReadPinValue(self, pinIndex = 0):
        #self.pinIndex = pinIndex
        level = c_uint()
        if self.io_exist and self.list_exist and self.device_exist:
            return_code = self.io.usb_io_read_input_pin_value(self.handle, pinIndex, byref(level))
            if return_code == 0:
                print "Read pin %s success, the value is %s" % (str(pinIndex), str(level.value))
                self.pin_info16_casted[pinIndex].pinValue = level.value
                return True
        

    def CloseDevice(self):
        if self.device_exist:
            return_code = self.io.usb_io_close_device( self.handle)
            if return_code != 0:
                print "usb io device %s close success!" % self.handle
                self.device_exist = False
                return True
  

    def FreeDeviceList(self):
        if self.list_exist:
            return_code = self.io.usb_io_free_device_list(self.device_list)
            if return_code != 0:
                print  "Usb device list was free!"
                self.list_exist = False
                return True
            else:
                print "No usb device to free!"
                return False        

    def UsbIoUninitial(self):
        if self.io_exist:
            return_code = self.io.usb_io_uninit()
            if return_code == 0:
                print "usb io close success!"
                self.io_exist = False
            return True



if __name__ == "__main__":
    Usb = USB2016()
    Usb.SetWorkLedMode()
    Usb.GetAllPinInfo()
        
    #Usb.SetPinMode(pin_mode = OUTPUT_MODE)
    Usb.WritePinValue()
    Usb.ReadPinValue()

    Usb.CloseDevice()
    Usb.FreeDeviceList()
    Usb.UsbIoUninitial()

# All Necessary Imports
import Tkinter as tk
import os
import picamera
import RPi.GPIO as GPIO
from time import sleep
import datetime
import time
import webbrowser


# Camera Setup
piCam = picamera.PiCamera()
piCam.rotation = 90

piCam_resolution = "480p"
piCam_framerate = "30FPS"


# Global Numbers
number_delay = 0
number_brightness = 50
number_contrast = 0
number_sharpness = 0


# Buttons/RGB LED Setup
buttons = [ 18 , 19 ]
rgb_led_red = 17
rgb_led_green = 16
rgb_led_blue = 15

GPIO.setmode(GPIO.BCM)
GPIO.setup(buttons, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setwarnings(False)


# Functions for handling the RGB LED
def blink(rgb_pin):
    GPIO.setup(rgb_pin, GPIO.OUT)
    GPIO.output(rgb_pin, GPIO.HIGH)

def turnOff(rgb_pin):
    GPIO.setup(rgb_pin, GPIO.OUT)
    GPIO.output(rgb_pin, GPIO.LOW)

def redOn():
    blink(rgb_led_red)

def yellowOn():
    blink(rgb_led_red)
    blink(rgb_led_green)

def redOff():
    turnOff(rgb_led_red)

def yellowOff():
    turnOff(rgb_led_red)
    turnOff(rgb_led_green)
    
    
# GUI_Main
class GUI:
    def __init__(self, master):
        master.attributes("-fullscreen", True)
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack(fill=tk.BOTH, expand = True)

        global number_delay

        for row in range(4):
            tk.Grid.rowconfigure(self.frame, row, weight = 1)

        for col in range(4):
            tk.Grid.columnconfigure(self.frame, col, weight = 1)

        # Camera Location
        self.cameraSpace = tk.Label(self.frame, text = "Camera Live", bg = "black",)
        self.cameraSpace.grid(row = 0, column = 0, rowspan = 4, columnspan = 4, sticky = tk.N+tk.S+tk.E+tk.W)

        # Quit Button
        self.quitButton = tk.Button(self.frame, text = "Quit", bg = "light grey", font = "30", command = lambda:[os._exit(0)])
        self.quitButton.grid(row = 0, column = 3, rowspan = 1, columnspan = 1, sticky = tk.N+tk.S+tk.E+tk.W)

        # Delay Timer Screen Button
        self.timerButton = tk.Button(self.frame, text = "Delay Timer", bg = "light grey", font = "30", command = self.open_GUI_Delay)
        self.timerButton.grid(row = 1, column = 3, rowspan = 1, columnspan = 1, sticky = tk.N+tk.S+tk.E+tk.W)

        # Settings Button
        self.pictureButton = tk.Button(self.frame, text = "Settings", bg = "light grey", font = "30", command = self.open_GUI_Settings)
        self.pictureButton.grid(row = 3, column = 3, rowspan = 1, columnspan = 1, sticky = tk.N+tk.S+tk.E+tk.W)

        # Library Button
        self.libraryButton = tk.Button(self.frame, text = "Library", bg = "light grey", font = "30", command = lambda: self.openLibrary())
        self.libraryButton.grid(row = 2, column = 3, rowspan = 1, columnspan = 1, sticky = tk.N+tk.S+tk.E+tk.W)


    # Opens Library 
    def openLibrary(self):
        pyDir = str(os.path.dirname(os.path.abspath(__file__)))
        webbrowser.open("Library//")

    # Opens GUI Delay Screen
    def open_GUI_Delay(self):
        piCam.stop_preview()
        self.newWindow = tk.Toplevel(self.master)
        self.app = GUI_Delay(self.newWindow)

    # Opens GUI Settings Screen
    def open_GUI_Settings(self):
        piCam.stop_preview()
        self.newWindow = tk.Toplevel(self.master)
        self.app = GUI_Settings(self.newWindow)

            
# GUI_Delay
class GUI_Delay:
    def __init__(self, master):
        master.attributes("-fullscreen", True)
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack(fill=tk.BOTH, expand = True)

        global number_delay

        for row in range(5):
            tk.Grid.rowconfigure(self.frame, row, weight = 1)
       
        for col in range(2):
            tk.Grid.columnconfigure(self.frame, col, weight=1)

        # Input Screen
        self.display = tk.Label(self.frame, text= str(number_delay), bg = "light yellow",  anchor = tk.E ,height = 1, font = (45))
        self.display.grid(row = 0, column = 0, columnspan = 1, sticky = tk.E+tk.W+tk.N+tk.S)

        # Minute Display
        self.minuteDisplay = tk.Label(self.frame, text="Second(s)", anchor = tk.W, bg = "light yellow", height = 1, font = (45))
        self.minuteDisplay.grid(row = 0, column = 1, columnspan = 1, sticky = tk.E+tk.W+tk.N+tk.S)

        # Reset Button. Resets the Delay to 0.
        self.resetButton = tk.Button(self.frame, text = "Reset", bg = "light grey", font = "30", command = self.resetDelay)
        self.resetButton.grid(row = 4, column = 0, rowspan = 1, columnspan = 2, sticky = tk.N+tk.S+tk.E+tk.W)

        # "Up" Button. Moves timer up by 1 second.
        self.timerUpButton = tk.Button(self.frame, text = "+", bg = "light grey", font = "30", command= lambda:[self.addOne()])
        self.timerUpButton.grid(row = 1, column = 0, columnspan = 2, sticky = tk.N+tk.S+tk.E+tk.W)

        # "Down" Button. Moves timer down by 1 second.
        self.timerDownButton = tk.Button(self.frame, text = "-", bg = "light grey", font = "30", command= lambda:[self.subOne()])
        self.timerDownButton.grid(row = 2, column = 0, columnspan = 2, sticky = tk.N+tk.S+tk.E+tk.W)

        # "Done" Button. Sets the timer.
        self.timerUpButton = tk.Button(self.frame, text = "Set!", bg = "Green", font = "30", command = self.close_windows)
        self.timerUpButton.grid(row = 3, column = 0, columnspan = 2, sticky = tk.N+tk.S+tk.E+tk.W)

    # Function that adds one second to the delay.
    def addOne(self):
        global number_delay
        if (number_delay < 15):
            number_delay += 1
            self.display["text"] = number_delay

    # Function that subtracts one second from the delay.    
    def subOne(self):
        global number_delay
        if (number_delay > 0):
            number_delay -= 1
            self.display["text"] = number_delay

    # This closes the overlay window.
    def close_windows(self):
        piCam.start_preview(fullscreen=False, window = (0, -60, 516, 600)) 
        self.master.destroy()

    # This resets the delay timer.
    def resetDelay(self):
        global number_delay
        number_delay = 0
        self.close_windows()


# GUI_Settings
class GUI_Settings:
    def __init__(self, master):
        master.attributes("-fullscreen", True)
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack(fill=tk.BOTH, expand = True)

        global number_brightness
        global number_contrast
        global number_sharpness
        global piCam_resolution
        global piCam_framerate

        for row in range(6):
            tk.Grid.rowconfigure(self.frame, row, weight = 1)
       
        for col in range(5):
            tk.Grid.columnconfigure(self.frame, col, weight = 1)
        
        # Setting Scrolls
        self.resolutionPresets = tk.Label(self.frame, text="Resolution",  bg = "light yellow", height = 1, font = (45))
        self.resolutionPresets.grid(row = 0, column = 0, columnspan = 1, sticky = tk.N+tk.S+tk.E+tk.W)

        self.infoResolution = tk.Label(self.frame, text = "", bg = "grey", height = 1, font = (45))
        self.infoResolution.grid(row = 1, column = 0, columnspan = 1, sticky = tk.N+tk.S+tk.E+tk.W)

        # Resolution Buttons
        self.res1 = tk.Button(self.frame, text = "1080p", bg = "light grey", height = 1, font=(45), state = tk.NORMAL, command = lambda: self.buttonAlt("1080p"))
        self.res1.grid(row=3, column = 0, columnspan = 1, sticky = tk.N+tk.S+tk.E+tk.W)

        self.res2 = tk.Button(self.frame, text = "720p", bg = "dark grey", height = 1, font=(45), state = tk.DISABLED, command = lambda: self.buttonAlt("720p"))
        self.res2.grid(row=2, column = 0, columnspan = 1, sticky = tk.N+tk.S+tk.E+tk.W)

        self.res3 = tk.Button(self.frame, text = "480p", bg = "light grey", height = 1, font=(45), state = tk.NORMAL, command = lambda: self.buttonAlt("480p"))
        self.res3.grid(row=1, column = 0, columnspan = 1, sticky = tk.N+tk.S+tk.E+tk.W)

        self.buttonChanges(piCam_resolution)

        # Frame Rate
        self.frameRate = tk.Label(self.frame, text="Frame Rate",  bg = "light yellow", height = 1, font = (45))
        self.frameRate.grid(row = 0, column = 1, columnspan = 1, sticky = tk.N+tk.S+tk.E+tk.W)

         # 24
        self.frameRate24 = tk.Button(self.frame, text= "24FPS", bg = "light grey", height = 1, font = (45), state = tk.NORMAL, command = lambda: self.buttonAlt("24FPS"))
        self.frameRate24.grid(row = 1, column = 1, columnspan = 1, sticky = tk.N+tk.S+tk.E+tk.W)

        # 30
        self.frameRate30 = tk.Button(self.frame, text= "30FPS", bg = "dark grey", height = 1, font = (45), state = tk.DISABLED, command = lambda: self.buttonAlt("30FPS"))
        self.frameRate30.grid(row = 2, column = 1, columnspan = 1, sticky = tk.N+tk.S+tk.E+tk.W)

        # 60
        self.frameRate60 = tk.Button(self.frame, text= "60FPS", bg = "light grey", height = 1, font = (45), state = tk.NORMAL, command = lambda: self.buttonAlt("60FPS"))
        self.frameRate60.grid(row = 3, column = 1, columnspan = 1, sticky = tk.N+tk.S+tk.E+tk.W)

        self.buttonChanges(piCam_framerate)
       
        # Brightness
        self.brightness = tk.Label(self.frame, text = "Brightness", bg = "light yellow", height = 1, font = (45))
        self.brightness.grid(row = 0, column = 2, columnspan = 1, sticky = tk.N+tk.S+tk.E+tk.W)

        self.infoBrightness = tk.Label(self.frame, text = str(number_brightness), bg = "light grey", height = 1, font = (45))
        self.infoBrightness.grid(row = 1, column = 2, columnspan = 1, sticky = tk.N+tk.S+tk.E+tk.W)

        # Brightness +1
        self.timerUpButton = tk.Button(self.frame, text = "+", bg = "light grey", font = "30", command = lambda:self.addOneB())
        self.timerUpButton.grid(row = 2, column = 2, columnspan = 1, sticky = tk.N+tk.S+tk.E+tk.W)

        # Brightness -1
        self.timerDownButton = tk.Button(self.frame, text = "-", bg = "light grey", font = "30", command = lambda:self.subOneB())
        self.timerDownButton.grid(row = 3, column = 2, columnspan = 1, sticky = tk.N+tk.S+tk.E+tk.W)

        # Contrast
        self.contrast = tk.Label(self.frame, text = "Contrast", bg = "light yellow", height = 1, font = (45))
        self.contrast.grid(row = 0, column = 3, columnspan = 1, sticky = tk.N+tk.S+tk.E+tk.W)

        self.infoContrast = tk.Label(self.frame, text = str(number_contrast), bg = "light grey", height = 1, font = (45))
        self.infoContrast.grid(row = 1, column = 3, columnspan = 1, sticky = tk.N+tk.S+tk.E+tk.W)

        # Contrast +1
        self.timerUpButton = tk.Button(self.frame, text = "+", bg = "light grey", font = "30", command = lambda:self.addOneC())
        self.timerUpButton.grid(row = 2, column = 3, columnspan = 1, sticky = tk.N+tk.S+tk.E+tk.W)

        # Contrast -1
        self.timerDownButton = tk.Button(self.frame, text = "-", bg = "light grey", font = "30", command = lambda:self.subOneC())
        self.timerDownButton.grid(row = 3, column = 3, columnspan = 1, sticky = tk.N+tk.S+tk.E+tk.W)

        # Sharpness
        self.sharpness = tk.Label(self.frame, text = "Sharpness", bg = "light yellow", height = 1, font = (45))
        self.sharpness.grid(row = 0, column = 4, columnspan = 1, sticky = tk.N+tk.S+tk.E+tk.W)

        self.infoSharp = tk.Label(self.frame, text = str(number_sharpness), bg = "light grey", height = 1, font = (45))
        self.infoSharp.grid(row = 1, column = 4, columnspan = 1, sticky = tk.N+tk.S+tk.E+tk.W)

        # Sharpness +1
        self.sharpUpButton = tk.Button (self.frame, text = "+", bg = "light grey", height = 1, font = 45, command = lambda:self.addOneS())
        self.sharpUpButton.grid(row = 2, column = 4, columnspan = 1, sticky = tk.N+tk.S+tk.E+tk.W)

        # Sharpness -1
        self.sharpDownButton = tk.Button(self.frame, text = "-", bg = "light grey", font = "30", command = lambda:self.subOneS())
        self.sharpDownButton.grid(row = 3, column = 4, columnspan = 1, sticky = tk.N+tk.S+tk.E+tk.W)
         
        # Done Button
        self.done = tk.Button(self.frame, text = "Done!", bg = "light grey", font = "30", command = self.close_windows)
        self.done.grid(row = 4, column = 0, columnspan = 5, sticky = tk.N+tk.S+tk.E+tk.W)

         # Reset Button
        self.resetButton = tk.Button(self.frame, text = "Reset", bg = "light grey", font = "30", command = self.reset_settings)
        self.resetButton.grid(row = 5, column = 0, rowspan = 1, columnspan = 5, sticky = tk.N+tk.S+tk.E+tk.W)

    # Resets the Brightness, Contrast, and Sharpness to default values.
    def reset_settings(self):
        global number_brightness
        global number_contrast
        global number_sharpness

        number_brightness = 49
        number_contrast = -1
        number_sharpness = -1

        self.addOneB()
        self.addOneC()
        self.addOneS()

    # Closes the overlay window.
    def close_windows(self):
        piCam.start_preview(fullscreen=False, window = (0, -60, 516, 600)) 
        self.master.destroy()

    # Brightness +1
    def addOneB(self):
        global number_brightness
        if (number_brightness < 100):
            number_brightness += 1
            piCam.brightness = number_brightness
            self.infoBrightness["text"] = number_brightness

    # Brightness -1
    def subOneB(self):
        global number_brightness
        if (number_brightness > 0):
            number_brightness -= 1
            piCam.brightness = number_brightness
            self.infoBrightness["text"] = number_brightness

    # Contrast +1
    def addOneC(self):
        global number_contrast
        if (number_contrast < 100):
            number_contrast += 1
            piCam.contrast = number_contrast
            self.infoContrast["text"] = number_contrast

    # Contrast -1    
    def subOneC(self):
        global number_contrast
        if (number_contrast > -100):
            number_contrast-= 1
            piCam.contrast = number_contrast
            self.infoContrast["text"] = number_contrast

    # Sharpness +1
    def addOneS(self):
        global number_sharpness
        if (number_sharpness < 100):
            number_sharpness += 1
            piCam.sharpness = number_sharpness
            self.infoSharp["text"] = number_sharpness

    # Sharpness -1   
    def subOneS(self):
        global number_sharpness
        if (number_sharpness > -100):
            number_sharpness -= 1
            piCam.sharpness = number_sharpness
            self.infoSharp["text"] = number_sharpness

    # Calls button changes.
    def buttonAlt(self, type):
        if (type == "1080p"):
            self.buttonChanges("1080p")
        elif (type == "720p"):
            self.buttonChanges("720p")
        elif (type == "480p"):
            self.buttonChanges("480p")
        elif (type == "24FPS"):
            self.buttonChanges("24FPS")
        elif (type == "30FPS"):
            self.buttonChanges("30FPS")
        else:
            self.buttonChanges("60FPS")

    # Changes button states and sets resolution/framerate as well.
    def buttonChanges(self, button):
        global piCam_resolution
        global piCam_framerate
        
        if (button == "1080p"):
            self.res1["state"] = tk.DISABLED
            self.res1["bg"] = "dark grey"
        
            self.res2["state"] = tk.NORMAL
            self.res2["bg"] = "light grey"
        
            self.res3["state"] = tk.NORMAL
            self.res3["bg"] = "light grey"

            piCam_resolution = "1080p"
            piCam.resolution = (1920,1080)
            
        elif (button == "720p"):
            self.res1["state"] = tk.NORMAL
            self.res1["bg"] = "light grey"
            
            self.res2["state"] = tk.DISABLED
            self.res2["bg"] = "dark grey"

            self.res3["state"] = tk.NORMAL
            self.res3["bg"] = "light grey"

            piCam_resolution = "720p"
            piCam.resolution = (1280,720)
            
        elif (button == "480p"):
            self.res1["state"] = tk.NORMAL
            self.res1["bg"] = "light grey"
            
            self.res2["state"] = tk.NORMAL
            self.res2["bg"] = "light grey"

            self.res3["state"] = tk.DISABLED
            self.res3["bg"] = "dark grey"

            piCam_resolution = "480p"
            piCam.resolution = (640,480)
            
        elif (button == "60FPS"):
            self.frameRate60["state"] = tk.DISABLED
            self.frameRate60["bg"] = "dark grey"

            self.frameRate30["state"] = tk.NORMAL
            self.frameRate30["bg"] = "light grey"

            self.frameRate24["state"] = tk.NORMAL
            self.frameRate24["bg"] = "light grey"

            piCam_framerate = "60FPS"
            piCam.framerate = (60)

        elif (button == "30FPS"):
            
            self.frameRate30["state"] = tk.DISABLED
            self.frameRate30["bg"] = "dark grey"

            self.frameRate60["state"] = tk.NORMAL
            self.frameRate60["bg"] = "light grey"
            
            self.frameRate24["state"] = tk.NORMAL
            self.frameRate24["bg"] = "light grey"

            piCam_framerate = "30FPS"
            piCam.framerate = (30)
        
        else:
        
            self.frameRate30["state"] = tk.NORMAL
            self.frameRate30["bg"] = "light grey"

            self.frameRate60["state"] = tk.NORMAL
            self.frameRate60["bg"] = "light grey"

            self.frameRate24["state"] = tk.DISABLED
            self.frameRate24["bg"] = "dark grey"

            piCam_framerate = "24FPS"
            piCam.framerate = (24)

        
# Camera Functions
pyDir = str(os.path.dirname(os.path.abspath(__file__)))

# Takes Picture
def piCam_takePicure():
    sleep(number_delay)
    piCam_date = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
    piCam.capture("Library/Pictures/" + piCam_date + ".jpeg")
    yellowOn()
    sleep(0.15)
    yellowOff()

# Starts Recording 
def piCam_startRecord():
    global cam_recording
    global number_delay
    sleep(number_delay)
    cam_recording = True
    piCam_date = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
    piCam.start_recording("Library/Videos/" + piCam_date + ".h264")
    redOn()

# Stops Recording 
def piCam_stopRecord():
    global cam_recording
    cam_recording = False
    piCam.stop_recording()
    redOff()
    
    
# Start Function 
def main():
    global cam_recording
    cam_recording = False
    piCam.start_preview(fullscreen=False, window = (0, -60, 516, 600))    
    pyCam = tk.Tk()
    pyCam.title("piCamcorder")
    app = GUI(pyCam)
    
    def GPIO_Loop():
        global cam_recording
        if (GPIO.input(18) == GPIO.HIGH) and (cam_recording == False):
            GPIO.wait_for_edge(18, GPIO.FALLING)
            piCam_startRecord()
        elif (GPIO.input(18) == GPIO.HIGH) and (cam_recording == True):
            GPIO.wait_for_edge(18, GPIO.FALLING)
            piCam_stopRecord()
        elif (GPIO.input(19) == GPIO.HIGH):
            piCam_takePicure()
        pyCam.after(10, GPIO_Loop)
    
    pyCam.after(10, GPIO_Loop)
    pyCam.mainloop()
    

# Let the piCamcorder begin!
main()

# SpectrumAnalyzer-v02a.py(w)  (15-03-2015)
# For Python version 2.6 or 2.7
# With external module pyaudio (for Python version 2.6 or 2.7); NUMPY module (for used Python version)
# Created by Onno Hoekstra (pa2ohh)
import pyaudio
import math
import time
import wave
import struct
import numpy.fft

from time import gmtime, strftime
import tkFont
from Tkinter import *
from tkFileDialog import askopenfilename
from tkSimpleDialog import askstring
from tkMessageBox import *

# Values that can be modified
DBdivlist = [1, 2, 3, 5, 10, 20]        # dB per division
DBdivindex = 4                          # 10 dB/div as initial value
DBlevel = 0                             # Reference level

GRWN = 1000                             # Width of the grid
GRHN = 500                              # Height of the grid
X0L = 20                                # Left top X value of grid
Y0T = 25                                # Left top Y value of grid

SAMPLErate = 48000                      # Sample rate of the sound system 24000 48000 96000 192000

TRACEmode = 1                           # 1 normal mode, 2 max hold mode, 3 average mode
TRACEaverage = 10                       # Number of average sweeps for average mode
TRACEreset = True                       # True for first new trace, reset max hold and averageing 
UPDATEspeed = 1.1                       # Update speed can be increased when problems if PC too slow, default 1.1
Vdiv = 8                                # Number of vertical divisions
WAVinput = 0                            # DEFAULT 0 for Audio device input, 1 for WAV file channel 1 input, 2 for WAV file channel 2 input
ZEROpadding = 1                         # ZEROpadding for signal interpolation between frequency samples (0=none)


# Colors that can be modified
COLORframes = "#000080"                 # Color = "#rrggbb" rr=red gg=green bb=blue, Hexadecimal values 00 - ff
COLORcanvas = "#000000"
COLORgrid = "#808080"
COLORtrace1 = "#00ff00"
COLORtrace2 = "#ff8000"
COLORtext = "#ffffff"
COLORsignalband = "#ff0000"
COLORaudiobar = "#606060"
COLORaudiook = "#00ff00"
COLORaudiomax = "#ff0000"


# Button sizes that can be modified
Buttonwidth1 = 12
Buttonwidth2 = 8


# Initialisation of general variables
STARTfrequency = 0.0                    # Startfrequency
STOPfrequency = 10000.0                 # Stopfrequency
ZEROpadding = 1                         # The zero padding value is 2 ** ZERO padding, calculated on initialize

                       
# Other global variables required in various routines
GRW = GRWN                              # Initialize GRW
GRH = GRHN                              # Initialize GRH

CANVASwidth = GRW + 2 * X0L             # The canvas width
CANVASheight = GRH + 80                 # The canvas height

AUDIOsignal1 = []                       # Audio trace channel 1
AUDIOdevin = None                       # Audio device for input. None = Windows default
AUDIOdevout = None                      # Audio device for output. None = Windows default
AUDIOlevel = 0.0                        # Level of audio input 0 to 1
AUDIOstatus = 0                         # 0 audio off, 1 audio on

FFTbandwidth = 0                        # The FFT bandwidth
FFTresult = []                          # FFT result
FFTwindow = 5                           # FFTwindow 0=None (rectangular B=1), 1=Cosine (B=1.24), 2=Triangular non-zero endpoints (B=1.33),
                                        # 3=Hann (B=1.5), 4=Blackman (B=1.73), 5=Nuttall (B=2.02), 6=Flat top (B=3.77)
FFTwindowname = "--"                    # The FFT window name
FFTmemory = numpy.ones(1)               # The memory for averaging

RUNstatus = 1                           # 0 stopped, 1 start, 2 running, 3 stop now, 4 stop and restart
RXbuffer = 0.0                          # Data contained in input buffer in %
RXbufferoverflow = False

STARTsample = 0                         # The start sample used for the display, be calculated on initialize
STOPsample = 0                          # The stop sample used for the display, be calculated on initialize

SMPfftpwrTwo = 11                       # The power of two of SMPfft
SMPfft = 2 ** SMPfftpwrTwo              # Initialize

STOREtrace = False                      # Store and display trace

FFTwindowshape = numpy.ones(SMPfft)     # The FFT window curve

T1line = []                             # Trace line channel 1
T2line = []                             # Trace line channel 2

# =================================== Start widgets routines ========================================
def Bnot():
    print "Routine not made yet"


def BNormalmode():
    global RUNstatus
    global TRACEmode

    TRACEmode = 1
    if RUNstatus == 0:      # Update if stopped
        UpdateScreen()
    if RUNstatus == 2:      # Restart if running
        RUNstatus = 4
    

def BMaxholdmode():
    global RUNstatus
    global TRACEmode

    TRACEmode = 2
    if RUNstatus == 0:      # Update if stopped
        UpdateScreen()
    if RUNstatus == 2:      # Restart if running
        RUNstatus = 4
    

def BAveragemode():
    global RUNstatus
    global TRACEaverage
    global TRACEmode

    TRACEmode = 3

    s = askstring("Power averaging", "Value: " + str(TRACEaverage) + "x\n\nNew value:\n(1-n)")

    if (s == None):         # If Cancel pressed, then None
        return()

    try:                    # Error if for example no numeric characters or OK pressed without input (s = "")
        v = int(s)
    except:
        s = "error"

    if s != "error":
        TRACEaverage = v

    if TRACEaverage < 1:
        TRACEaverage = 1

    if RUNstatus == 0:      # Update if stopped
        UpdateScreen()
    if RUNstatus == 2:      # Restart if running
        RUNstatus = 4


def BFFTwindow():
    global FFTwindow
    global RUNstatus
    
    FFTwindow = FFTwindow + 1
    if FFTwindow > 6:
        FFTwindow = 0

    CALCFFTwindowshape()    # Make the FFTwindowshape for the windowing function
    
    UpdateScreen()          # Always Update

    if RUNstatus == 0:      # Update if stopped
        UpdateScreen()
    if RUNstatus == 2:      # Restart if running
        RUNstatus = 4


def BAudiostatus():
    global AUDIOstatus
    global RUNstatus
    
    if AUDIOstatus == 0:
        AUDIOstatus = 1
    else:
        AUDIOstatus = 0
    if RUNstatus == 0:      # Update if stopped
        UpdateScreen()


def BSTOREtrace():
    global STOREtrace
    global T1line
    global T2line
    if STOREtrace == False:
        T2line = T1line
        STOREtrace = True
    else:
        STOREtrace = False
    UpdateTrace()           # Always Update


def BCSVfile():
    STOREcsvfile()          # Store the trace as CSV file


def BScreensetup():
    global GRWN
    global GRW
    global GRHN
    global GRH
    global STOREtrace
    global Vdiv
    
    if (STOREtrace == True):
        showwarning("WARNING","Clear stored trace first")
        return()

    s = askstring("Screensize", "Give number:\n(1, 2 or 3)")

    # if (s == None):         # If Cancel pressed, then None
    #     return()

    try:                    # Error if for example no numeric characters or OK pressed without input (s = "")
        v = int(s)
    except:
        s = "error"

    if s != "error":
        if v == 1:
            GRW = int(GRWN / 4)
            GRH = int(GRHN / 4)
        if v == 2:
            GRW = int(GRWN / 2)
            GRH = int(GRHN / 2)
        if v == 3:
            GRW = int(GRWN)
            GRH = int(GRHN)

    s = askstring("Divisions", "Value: " + str(Vdiv) + "\n\nNew value:\n(4-100)")

    if (s == None):         # If Cancel pressed, then None
        return()

    try:                    # Error if for example no numeric characters or OK pressed without input (s = "")
        v = int(s)
    except:
        s = "error"

    if s != "error":
        Vdiv = v

    if Vdiv < 4:
        Vdiv = 4

    if Vdiv > 100:
        Vdiv = 100
    UpdateTrace()


def BStart():
    global RUNstatus
    
    if (RUNstatus == 0):
        RUNstatus = 1
    UpdateScreen()          # Always Update


def Blevel1():
    global DBlevel
    global RUNstatus

    DBlevel = DBlevel - 1
    
    if RUNstatus == 0:      # Update if stopped
        UpdateTrace()


def Blevel2():
    global DBlevel
    global RUNstatus

    DBlevel = DBlevel + 1
    
    if RUNstatus == 0:      # Update if stopped
        UpdateTrace()


def Blevel3():
    global DBlevel
    global RUNstatus

    DBlevel = DBlevel - 10
    
    if RUNstatus == 0:      # Update if stopped
        UpdateTrace()


def Blevel4():
    global DBlevel
    global RUNstatus

    DBlevel = DBlevel + 10
    
    if RUNstatus == 0:      # Update if stopped
        UpdateTrace()


def BStop():
    global RUNstatus
    
    if (RUNstatus == 1):
        RUNstatus = 0
    elif (RUNstatus == 2):
        RUNstatus = 3
    elif (RUNstatus == 3):
        RUNstatus = 3
    elif (RUNstatus == 4):
        RUNstatus = 3
    UpdateScreen()          # Always Update


def BSetup():
    global AUDIOsignal1
    global RUNstatus
    global SAMPLErate
    global T1line
    global ZEROpadding
    
    if (RUNstatus != 0):
        showwarning("WARNING","Stop sweep first")
        return()
    
    s = askstring("Sample rate","Sample rate of soundcard.\n\nValue: " + str(SAMPLErate) + "\n\nNew value:\n(6000, 12000, 24000, 48000, 96000, 192000)")

    if (s == None):         # If Cancel pressed, then None
        return()

    try:                    # Error if for example no numeric characters or OK pressed without input (s = "")
        v = int(s)
    except:
        s = "error"

    if s != "error":
        SAMPLErate = v
        AUDIOsignal1 = []   # Reset Audio trace channel 1    
        T1line = []         # Reset trace line 1
         
    # StartStop = askyesno("Start Stop","Start-Stop mode on?", default = NO)

    s = askstring("Zero padding","For better interpolation of levels between frequency samples.\nBut increases processing time!\n\nValue: " + str(ZEROpadding) + "\n\nNew value:\n(0-5, 0 is no zero padding)")

    if (s == None):         # If Cancel pressed, then None
        return()

    try:                    # Error if for example no numeric characters or OK pressed without input (s = "")
        v = int(s)
    except:
        s = "error"

    if s != "error":
        if v < 0:
            v = 0
        if v > 5:
            v = 5
        ZEROpadding = v

    UpdateScreen()          # Always Update    


def BStartfrequency():
    global RUNstatus
    global STARTfrequency
    global STOPfrequency

    # if (RUNstatus != 0):
    #    showwarning("WARNING","Stop sweep first")
    #    return()
    
    s = askstring("Startfrequency: ","Value: " + str(STARTfrequency) + " Hz\n\nNew value:\n")
    
    if (s == None):         # If Cancel pressed, then None
        return()

    try:                    # Error if for example no numeric characters or OK pressed without input (s = "")
        v = int(s)
    except:
        s = "error"

    if s != "error":
        STARTfrequency = v

    if STARTfrequency < 0:
        STARTfrequency = 0

    if STOPfrequency <= STARTfrequency:
        STOPfrequency = STARTfrequency + 1

    if RUNstatus == 0:      # Update if stopped
        UpdateTrace()
    if RUNstatus == 2:      # Restart if running
        RUNstatus = 4


def BStopfrequency():
    global RUNstatus
    global STARTfrequency
    global STOPfrequency
    
    # if (RUNstatus != 0):
    #    showwarning("WARNING","Stop sweep first")
    #    return()

    s = askstring("Stopfrequency: ","Value: " + str(STOPfrequency) + " Hz\n\nNew value:\n")

    if (s == None):         # If Cancel pressed, then None
        return()

    try:                    # Error if for example no numeric characters or OK pressed without input (s = "")
        v = int(s)
    except:
        s = "error"

    if s != "error":
        STOPfrequency = abs(v)

    if STOPfrequency < 10:  # Minimum stopfrequency 10 Hz
        STOPfrequency = 10
        
    if STARTfrequency >= STOPfrequency:
        STARTfrequency = STOPfrequency - 1

    if RUNstatus == 0:      # Update if stopped
        UpdateTrace()
    if RUNstatus == 2:      # Restart if running
        RUNstatus = 4


def Bsamples1():
    global RUNstatus
    global SMPfftpwrTwo
    global SMPfft
    global TRACEreset
    
    if (SMPfftpwrTwo > 6):  # Min 64
        SMPfftpwrTwo = SMPfftpwrTwo - 1
        TRACEreset = True   # Reset trace peak and trace average
        SMPfft = 2 ** int(SMPfftpwrTwo)

    if RUNstatus == 0:      # Update if stopped
        UpdateScreen()
    if RUNstatus == 2:      # Restart if running
        RUNstatus = 4


def Bsamples2():
    global RUNstatus
    global SMPfftpwrTwo
    global SMPfft
    global TRACEreset
      
    if (SMPfftpwrTwo < 16): # Max 65536
        SMPfftpwrTwo = SMPfftpwrTwo + 1
        TRACEreset = True   # Reset trace peak and trace average
        SMPfft = 2 ** int(SMPfftpwrTwo)

    if RUNstatus == 0:      # Update if stopped
        UpdateScreen()
    if RUNstatus == 2:      # Restart if running
        RUNstatus = 4


def BDBdiv1():
    global DBdivindex
    global RUNstatus
    
    if (DBdivindex >= 1):
        DBdivindex = DBdivindex - 1

    if RUNstatus == 0:      # Update if stopped
        UpdateTrace()


def BDBdiv2():
    global DBdivindex
    global DBdivlist
    global RUNstatus
    
    if (DBdivindex < len(DBdivlist) - 1):
        DBdivindex = DBdivindex + 1

    if RUNstatus == 0:      # Update if stopped
        UpdateTrace()


# ============================================ Main routine ====================================================
    
def AUDIOin():   # Read the audio from the stream and store the data into the arrays
    global AUDIOdevin
    global AUDIOdevout
    global AUDIOsignal1
    global AUDIOstatus
    global RUNstatus
    global RXbuffer
    global RXbufferoverflow
    global SAMPLErate
    global SMPfft
    global UPDATEspeed
    
    while (True):                                           # Main loop
        PA = pyaudio.PyAudio()
        FORMAT = pyaudio.paInt16                            # Audio format 16 levels and 2 channels
        CHUNK = int(SMPfft)

        # RUNstatus = 1 : Open Stream
        if (RUNstatus == 1):
            INITIALIZEstart()                               # Initialize variables

            if UPDATEspeed < 1:
                UPDATEspeed = 1.0

            TRACESopened = 1

            try:
                chunkbuffer = CHUNK
                if chunkbuffer < SAMPLErate / 10:           # Prevent buffer overload if small number of samples
                    chunkbuffer = int(SAMPLErate / 10)

                chunkbuffer = int(UPDATEspeed * chunkbuffer)
                
                stream = PA.open(format = FORMAT,
                    channels = TRACESopened, 
                    rate = SAMPLErate, 
                    input = True,
                    output = True,
                    frames_per_buffer = int(chunkbuffer),
                    input_device_index = AUDIOdevin,
                    output_device_index = AUDIOdevout)
                RUNstatus = 2
            except:                                         # If error in opening audio stream, show error
                RUNstatus = 0
                txt = "Sample rate: " + str(SAMPLErate) + ", try a lower sample rate.\nOr another audio device."
                showerror("Cannot open Audio Stream", txt)

            UpdateScreen()                                  # UpdateScreen() call        

            
        # RUNstatus = 2: Reading audio data from soundcard
        if (RUNstatus == 2):
            buffervalue = stream.get_read_available()       # Buffer reading testroutine
            RXbuffer = 100.0 * float(buffervalue) / chunkbuffer  # Buffer filled in %. Overflow at 2xchunkbuffer
            RXbufferoverflow = False
            try:
                signals = ""
                if buffervalue > chunkbuffer:               # ADDED FOR RASPBERRY PI WITH ALSA, PERHAPS NOT NECESSARY WITH PULSE
                    signals = stream.read(chunkbuffer)      # Read samples from the buffer

                if (AUDIOstatus == 1):                      # Audio on
                        stream.write(signals, chunkbuffer)
            except:
                AUDIOsignal1 = []
                RUNstatus = 4
                RXbufferoverflow = True                     # Buffer overflow at 2x chunkbuffer


            # Conversion audio samples to values -32762 to +32767 (ones complement) and add to AUDIOsignal1
            AUDIOsignal1 = []                               # Clear the AUDIOsignal1 array for trace 1
            AUDIOsignal1.extend(numpy.fromstring(signals, "Int16"))

            UpdateAll()                                     # Update Data, trace and screen


        # RUNstatus = 3: Stop
        # RUNstatus = 4: Stop and restart
        if (RUNstatus == 3) or (RUNstatus == 4):
            stream.stop_stream()
            stream.close()
            PA.terminate()
            if RUNstatus == 3:
                RUNstatus = 0                               # Status is stopped 
            if RUNstatus == 4:          
                RUNstatus = 1                               # Status is (re)start
            UpdateScreen()                                  # UpdateScreen() call


        # Update tasks and screens by TKinter 
        root.update_idletasks()
        root.update()                                       # update screens

    
def WAVin():   # Read the audio from the WAV file and store the data into the array and read data from the array
    global AUDIOdevin
    global AUDIOdevout
    global AUDIOsignal1
    global AUDIOstatus
    global RUNstatus
    global RXbuffer
    global RXbufferoverflow
    global SAMPLErate
    global SMPfft
    global UPDATEspeed
    global WAVchannels
    global WAVfilename
    global WAVframerate
    global WAVframes
    global WAVinput
    global WAVsamplewidth
    global WAVsignal1
    global WAVsignal2

    
    while (True):                                           # Main loop
        CHUNK = int(SMPfft)

        # RUNstatus = 1 : Open WAV file
        if (RUNstatus == 1):
            INITIALIZEstart()                               # Initialize variables

            chunkbuffer = CHUNK

            WAVfilename = ASKWAVfilename()

            if (WAVfilename == None): # No input, cancel or error
                WAVfilename = ""

            if (WAVfilename == ""):
                RUNstatus = 0
            else:
                WAVf = wave.open(WAVfilename, 'rb')
                WAVframes = WAVf.getnframes()
                # print "frames: ", WAVframes
                WAVchannels = WAVf.getnchannels()
                # print "channels: ", WAVchannels
                WAVsamplewidth = WAVf.getsampwidth()
                # print "samplewidth: ", WAVsamplewidth
                WAVframerate = WAVf.getframerate()
                # print "framerate: ", WAVframerate
                SAMPLErate = WAVframerate

                signals = WAVf.readframes(WAVframes)        # Read the data from the WAV file and convert to WAVsignalx[]
                
                i = 0
                f = 0
                s = ""

                WAVsignal1 = []
                WAVsignal2 = []

                if (WAVsamplewidth == 1) and (WAVchannels == 1):
                    while (f < WAVframes):
                        s = str(struct.unpack('B', signals[i:(i+1)]))
                        v = int(s[1:-2]) - 128
                        WAVsignal1.append(v) 
                        WAVsignal2.append(0) 
                        i = i + 1
                        f = f + 1
                    
                if (WAVsamplewidth == 1) and (WAVchannels == 2):
                    while (f < WAVframes):
                        s = str(struct.unpack('B', signals[i:(i+1)]))
                        v = int(s[1:-2]) - 128
                        WAVsignal1.append(v) 
                        s = str(struct.unpack('B', signals[(i+1):(i+2)]))
                        v = int(s[1:-2])
                        WAVsignal2.append(v) 
                        i = i + 2
                        f = f + 1

                if (WAVsamplewidth == 2) and (WAVchannels == 1):
                    while (f < WAVframes):
                        s = str(struct.unpack('h', signals[i:(i+2)]))
                        v = int(s[1:-2])
                        WAVsignal1.append(v) 
                        WAVsignal2.append(0) 
                        i = i + 2
                        f = f + 1

                if (WAVsamplewidth == 2) and (WAVchannels == 2):
                    while (f < WAVframes):
                        s = str(struct.unpack('h', signals[i:(i+2)]))
                        v = int(s[1:-2])
                        WAVsignal1.append(v) 
                        s = str(struct.unpack('h', signals[(i+2):(i+4)]))
                        v = int(s[1:-2])
                        WAVsignal2.append(v) 
                        i = i + 4
                        f = f + 1

            WAVf.close()
            WAVpntr = 0                                     # Pointer to WAV array that has to be read
            UpdateScreen()                                  # UpdateScreen() call
            if RUNstatus == 1:
                RUNstatus = 2

            
        # RUNstatus = 2: Reading audio data from WAVsignalx array
        if (RUNstatus == 2):
            RXbuffer = 0                                    # Buffer filled in %. No overflow for WAV mode
            RXbufferoverflow = False

            AUDIOsignal1 = []
            n = 0

            if WAVinput == 1:
                while n < chunkbuffer:
                    v = WAVsignal1[WAVpntr]
                    AUDIOsignal1.append(v)

                    WAVpntr = WAVpntr + 1
                    if WAVpntr >= len(WAVsignal1):
                        WAVpntr = 0

                    n = n + 1

            if WAVinput == 2:
                while n < chunkbuffer:
                    v = WAVsignal2[WAVpntr]
                    AUDIOsignal1.append(v)

                    WAVpntr = WAVpntr + 1
                    if WAVpntr >= len(WAVsignal2):
                        WAVpntr = 0

                    n = n + 1

            UpdateAll()                                     # Update Data, trace and screen


        if (RUNstatus == 3) or (RUNstatus == 4):
            RUNstatus = 0                                   # Status is stopped 
            UpdateScreen()                                  # UpdateScreen() call


        # Update tasks and screens by TKinter 
        root.update_idletasks()
        root.update()                                       # update screens


def UpdateAll():        # Update Data, trace and screen
    global AUDIOsignal1
    global SMPfft

    if len(AUDIOsignal1) < SMPfft:
        return
    
    DoFFT()             # Fast Fourier transformation
    MakeTrace()         # Update the traces
    UpdateScreen()      # Update the screen 


def UpdateTrace():      # Update trace and screen
    MakeTrace()         # Update traces
    UpdateScreen()      # Update the screen


def UpdateScreen():     # Update screen with trace and text
    MakeScreen()        # Update the screen
    root.update()       # Activate updated screens    


def DoFFT():            # Fast Fourier transformation
    global AUDIOsignal1
    global AUDIOlevel
    global FFTmemory
    global FFTresult
    global FFTwindowshape
    global SAMPLErate
    global SMPfft
    global STARTfrequency
    global STOPfrequency
    global STARTsample
    global STOPsample
    global TRACEaverage
    global TRACEmode
    global TRACEreset
    global ZEROpadding
    
    T1 = time.time()                        # For time measurement of FFT routine
    
    REX = []
    IMX = []
      

    # Convert list to numpy array REX for faster Numpy calculations
    FFTsignal = AUDIOsignal1[:SMPfft]                       # Take the first fft samples
    REX = numpy.array(FFTsignal)                            # Make a numpy arry of the list


    # Set Audio level display value
    MAXaudio = 16000.0                                      # MAXaudio is 16000 for a normal soundcard, 50% of the total range of 32768
    REX = REX / MAXaudio
    
    MAXlvl = numpy.amax(REX)                                # First check for maximum positive value
    AUDIOlevel = MAXlvl                                     # Set AUDIOlevel

    MINlvl = numpy.amin(REX)                                # Then check for minimum positive value
    MINlvl = abs(MINlvl)                                    # Make absolute
    if MINlvl > AUDIOlevel:
        AUDIOlevel = MINlvl


    # Do the FFT window function
    REX = REX * FFTwindowshape                              # The windowing shape function only over the samples


    # Zero padding of array for better interpolation of peak level of signals
    ZEROpaddingvalue = int(2 ** ZEROpadding)
    fftsamples = ZEROpaddingvalue * SMPfft                  # Add zero's to the arrays

    # Save previous trace in memory for max or average trace
    FFTmemory = FFTresult

    # FFT with numpy 
    ALL = numpy.fft.fft(REX, n=fftsamples)                  # Do FFT + zeropadding till n=fftsamples with NUMPY  ALL = Real + Imaginary part
    ALL = numpy.absolute(ALL)                               # Make absolute SQR(REX*REX + IMX*IMX) for VOLTAGE!
    ALL = ALL * ALL                                         # Convert from Voltage to Power (P = (U*U) / R; R = 1)
    
    le = len(ALL)
    le = le / 2                                             # Only half is used, other half is mirror
    ALL = ALL[:le]                                          # So take only first half of the array
    
    Totalcorr = float(ZEROpaddingvalue)/ fftsamples         # For VOLTAGE!
    Totalcorr = Totalcorr * Totalcorr                       # For POWER!
    FFTresult = Totalcorr * ALL

    if TRACEmode == 1:                                      # Normal mode 1, do not change
        pass

    if TRACEmode == 2 and TRACEreset == False:              # Max hold mode 2, change v to maximum value
        FFTresult = numpy.maximum(FFTresult, FFTmemory)

    if TRACEmode == 3 and TRACEreset == False:              # Average mode 3, add difference / TRACEaverage to v
        FFTresult = FFTmemory + (FFTresult - FFTmemory) / TRACEaverage

    TRACEreset = False                                      # Trace reset done

    T2 = time.time()
    # print (T2 - T1)                                         # For time measurement of FFT routine


def MakeTrace():        # Update the grid and trace
    global FFTresult
    global DBdivindex   # Index value
    global DBdivlist    # dB per division list
    global DBlevel      # Reference level
    global GRH          # Screenheight
    global GRW          # Screenwidth
    global SAMPLErate
    global STARTfrequency
    global STOPfrequency
    global STARTsample
    global STOPsample
    global STOREtrace
    global T1line
    global T2line
    global Vdiv         # Number of vertical divisions
    global X0L          # Left top X value
    global Y0T          # Left top Y value


    # Set the TRACEsize variable
    TRACEsize = len(FFTresult)                              # Set the trace length

    if TRACEsize == 0:                                      # If no trace, skip rest of this routine
        return()


    # Vertical conversion factors (level dBs) and border limits
    Yconv = float(GRH) / (Vdiv * DBdivlist[DBdivindex])     # Conversion factors, Yconv is the number of screenpoints per dB
    Yc = float(Y0T) + Yconv * (DBlevel)                     # Yc is the 0 dBm position, can be outside the screen!
    Ymin = Y0T                                              # Minimum position of screen grid (top)
    Ymax = Y0T + GRH                                        # Maximum position of screen grid (bottom)

    # Horizontal conversion factors (frequency Hz) and border limits
    Fpixel = float(STOPfrequency - STARTfrequency) / GRW    # Frequency step per screen pixel
    Fsample = float(SAMPLErate / 2) / (TRACEsize - 1)       # Frequency step per sample   
    STARTsample = float(STARTfrequency) / Fsample           # First sample in FFTresult[] that is used
    STARTsample = int(math.ceil(STARTsample))               # First within screen range

    STOPsample = float(STOPfrequency) / Fsample             # Last sample in FFTresult[] that is used
    STOPsample = int(math.floor(STOPsample))                # Last within screen range, math.floor actually not necessary, part of int

    MAXsample = TRACEsize                                   # Just an out of range check
    if STARTsample > (MAXsample - 1):
        STARTsample = MAXsample - 1

    if STOPsample > MAXsample:
        STOPsample = MAXsample

    T1line = []
    n = STARTsample
    Slevel = 0.0            # Signal level
    Nlevel = 0.0            # Noise level
    while n <= STOPsample:
        F = n * Fsample

        x = X0L + (F - STARTfrequency)  / Fpixel
        T1line.append(int(x + 0.5))
        try:
            y =  Yc - Yconv * (10 * math.log10(float(FFTresult[n])) + 17)   # Convert power to DBs, except for log(0) error
        except:                                                             #  Add 17 dB for max value of +10 dB ALSO in CSV file routine!

            y = Ymax
            
        if (y < Ymin):
            y = Ymin
        if (y > Ymax):
            y = Ymax
        T1line.append(int(y + 0.5))

        n = n + 1               


def STOREcsvfile():     # Store the trace as CSV file [frequency,dB value]
    global FFTresult
    global SAMPLErate


    # Set the TRACEsize variable
    TRACEsize = len(FFTresult)                              # Set the trace length

    if TRACEsize == 0:                                      # If no trace, skip rest of this routine
        return()

    # Make the file name and open it
    tme =  strftime("%Y%b%d-%H%M%S", gmtime())              # The time
    filename = "Spectrum-" + tme
    filename = filename + ".csv"

    Wfile = open(filename,'w')                        # Open output file

    Fsample = float(SAMPLErate / 2) / (TRACEsize - 1)       # Frequency step per sample   

    n = 0
    while n < TRACEsize:
        F = n * Fsample
        V = 10 * math.log10(float(FFTresult[n])) + 17       # Add 17 dB for max value of +10 dB
        txt = str(F) + "," + str(V) + "\n"
        Wfile.write(txt)
        n = n + 1               

    Wfile.close()                                           # Close the file


def MakeScreen():       # Update the screen with traces and text
    global AUDIOlevel   # Level of audio input 0 to 1
    global AUDIOstatus  # 0 audio off, 1 audio on
    global CANVASheight
    global CANVASwidth
    global COLORaudiobar
    global COLORaudiomax
    global COLORaudiook 
    global COLORgrid    # The colors
    global COLORsignalband
    global COLORtext
    global COLORtrace1
    global COLORtrace2
    global DBdivindex   # Index value
    global DBdivlist    # dB per division list
    global DBlevel      # Reference level
    global FFTwindow
    global X0L          # Left top X value
    global Y0T          # Left top Y value
    global GRW          # Screenwidth
    global GRH          # Screenheight
    global RUNstatus    # 0 stopped, 1 start, 2 running, 3 stop now, 4 stop and restart
    global RXbuffer
    global RXbufferoverflow
    global S1line
    global S2line
    global SAMPLErate
    global SMPfft       # number of FFT samples
    global STARTfrequency
    global STOPfrequency
    global STOREtrace
    global T1line
    global T2line
    global TRACEaverage # Number of traces for averageing
    global TRACEmode    # 1 normal 2 max 3 average
    global UPDATEspeed
    global Vdiv         # Number of vertical divisions


    # Delete all items on the screen
    de = ca.find_enclosed ( 0, 0, CANVASwidth+1000, CANVASheight+1000)    
    for n in de: 
        ca.delete(n)
 

    # Draw horizontal grid lines
    i = 0
    x1 = X0L
    x2 = X0L + GRW
    while (i <= Vdiv):
        y = Y0T + i * GRH/Vdiv
        Dline = [x1,y,x2,y]
        ca.create_line(Dline, fill=COLORgrid)            
        i = i + 1


    # Draw vertical grid lines
    i = 0
    y1 = Y0T
    y2 = Y0T + GRH
    while (i < 11):
        x = X0L + i * GRW/10
        Dline = [x,y1,x,y2]
        ca.create_line(Dline, fill=COLORgrid)
        i = i + 1


    # Draw traces
    if len(T1line) > 4:                                     # Avoid writing lines with 1 coordinate    
        ca.create_line(T1line, fill=COLORtrace1)            # Write the trace 1

    if STOREtrace == True and len(T2line) > 4:              # Write the trace 2 if active
        ca.create_line(T2line, fill=COLORtrace2)            # and avoid writing lines with 1 coordinate


    # General information on top of the grid
    if (AUDIOstatus == 1):
        txt = "Audio on "
    else:
        txt = "Audio off"

    txt = txt + "    Sample rate: " + str(SAMPLErate)
    txt = txt + "    FFT samples: " + str(SMPfft)

    if FFTwindow == 0:
        txt = txt + "    Rectangular (no) window (B=1) "
    if FFTwindow == 1:
        txt = txt + "    Cosine window (B=1.24) "
    if FFTwindow == 2:
        txt = txt + "    Triangular window (B=1.33) "
    if FFTwindow == 3:
        txt = txt + "    Hann window (B=1.5) "
    if FFTwindow == 4:
        txt = txt + "    Blackman window (B=1.73) "
    if FFTwindow == 5:
        txt = txt + "    Nuttall window (B=2.02) "
    if FFTwindow == 6:
        txt = txt + "    Flat top window (B=3.77) "
        
    x = X0L
    y = 12
    idTXT = ca.create_text (x, y, text=txt, anchor=W, fill=COLORtext)


    # Start and stop frequency and dB/div and trace mode
    txt = str(STARTfrequency) + " to " + str(STOPfrequency) + " Hz"
    txt = txt +  "    " + str(DBdivlist[DBdivindex]) + " dB/div"
    txt = txt + "    Level: " + str(DBlevel) + " dB "

    if TRACEmode == 1:
        txt = txt + "    Normal mode "

    if TRACEmode == 2:
        txt = txt + "    Maximum hold mode "
    
    if TRACEmode == 3:
        txt = txt + "    Power average  mode (" + str(TRACEaverage) + ") " 

    x = X0L
    y = Y0T+GRH+12
    idTXT = ca.create_text (x, y, text=txt, anchor=W, fill=COLORtext)


    # Soundcard level bargraph
    txt1 = "||||||||||||||||||||"   # Bargraph
    le = len(txt1)                  # length of bargraph
    t = int(math.sqrt(AUDIOlevel) * le)

    n = 0
    txt = ""
    while(n < t and n < le):
        txt = txt + "|"
        n = n + 1

    x = X0L
    y = Y0T+GRH+32

    IDtxt = ca.create_text (x, y, text=txt1, anchor=W, fill=COLORaudiobar)

    if AUDIOlevel >= 1.0:
        IDtxt = ca.create_text (x, y, text=txt, anchor=W, fill=COLORaudiomax)
    else:
        IDtxt = ca.create_text (x, y, text=txt, anchor=W, fill=COLORaudiook)


    # Runstatus and level information
    if (RUNstatus == 0) or (RUNstatus == 3):
        txt = "Sweep stopped"
    else:
        txt = "Sweep running"

    # txt = txt + "    Buffer (%): " + str(int (RXbuffer))

    # if RXbufferoverflow == True:
    #    txt = txt + " OVERFLOW"

    if RXbuffer > 100:
        txt = txt + "."
    
    x = X0L + 100
    y = Y0T+GRH+32
    IDtxt  = ca.create_text (x, y, text=txt, anchor=W, fill=COLORtext)


def INITIALIZEstart():
    global SMPfft
    global SMPfftpwrTwo
    global TRACEreset


    # First some subroutines to set specific variables
    SMPfft = 2 ** int(SMPfftpwrTwo)                         # Calculate the number of FFT samples from SMPfftpwrtwo

    CALCFFTwindowshape()

    TRACEreset = True                                       # Clear the memory for averaging or peak
    

def CALCFFTwindowshape():                       # Make the FFTwindowshape for the windowing function
    global FFTbandwidth                         # The FFT bandwidth
    global FFTwindow                            # Which FFT window number is selected
    global FFTwindowname                        # The name of the FFT window function
    global FFTwindowshape                       # The window shape
    global SAMPLErate                           # The sample rate
    global SMPfft                               # Number of FFT samples
    
    
    # FFTname and FFTbandwidth in milliHz
    FFTwindowname = "No such window"
    FFTbw = 0
    
    if FFTwindow == 0:
        FFTwindowname = "0-Rectangular (no) window (B=1) "
        FFTbw = 1.0

    if FFTwindow == 1:
        FFTwindowname = "1-Cosine window (B=1.24) "
        FFTbw = 1.24

    if FFTwindow == 2:
        FFTwindowname = "2-Triangular window (B=1.33) "
        FFTbw = 1.33

    if FFTwindow == 3:
        FFTwindowname = "3-Hann window (B=1.5) "
        FFTbw = 1.5

    if FFTwindow == 4:
        FFTwindowname = "4-Blackman window (B=1.73) "
        FFTbw = 1.73

    if FFTwindow == 5:
        FFTwindowname = "5-Nuttall window (B=2.02) "
        FFTbw = 2.02

    if FFTwindow == 6:
        FFTwindowname = "6-Flat top window (B=3.77) "
        FFTbw = 3.77

    FFTbandwidth = int(1000.0 * FFTbw * SAMPLErate / float(SMPfft)) 

    # Calculate the shape
    FFTwindowshape = numpy.ones(SMPfft)         # Initialize with ones

    # m = 0                                       # For calculation of correction factor, furhter no function

    n = 0
    while n < SMPfft:

        # Cosine window function
        # medium-dynamic range B=1.24
        if FFTwindow == 1:
            w = math.sin(math.pi * n / (SMPfft - 1))
            FFTwindowshape[n] = w * 1.571

        # Triangular non-zero endpoints
        # medium-dynamic range B=1.33
        if FFTwindow == 2:
            w = (2.0 / SMPfft) * ((SMPfft/ 2.0) - abs(n - (SMPfft - 1) / 2.0))
            FFTwindowshape[n] = w * 2.0

        # Hann window function
        # medium-dynamic range B=1.5
        if FFTwindow == 3:
            w = 0.5 - 0.5 * math.cos(2 * math.pi * n / (SMPfft - 1))
            FFTwindowshape[n] = w * 2.000

        # Blackman window, continuous first derivate function
        # medium-dynamic range B=1.73
        if FFTwindow == 4:
            w = 0.42 - 0.5 * math.cos(2 * math.pi * n / (SMPfft - 1)) + 0.08 * math.cos(4 * math.pi * n / (SMPfft - 1))
            FFTwindowshape[n] = w * 2.381

        # Nuttall window, continuous first derivate function
        # high-dynamic range B=2.02
        if FFTwindow == 5:
            w = 0.355768 - 0.487396 * math.cos(2 * math.pi * n / (SMPfft - 1)) + 0.144232 * math.cos(4 * math.pi * n / (SMPfft - 1))- 0.012604 * math.cos(6 * math.pi * n / (SMPfft - 1))
            FFTwindowshape[n] = w * 2.811

        # Flat top window, 
        # medium-dynamic range, extra wide bandwidth B=3.77
        if FFTwindow == 6:
            w = 1.0 - 1.93 * math.cos(2 * math.pi * n / (SMPfft - 1)) + 1.29 * math.cos(4 * math.pi * n / (SMPfft - 1))- 0.388 * math.cos(6 * math.pi * n / (SMPfft - 1)) + 0.032 * math.cos(8 * math.pi * n / (SMPfft - 1))
            FFTwindowshape[n] = w * 1.000
        
        # m = m + w / SMPfft                          # For calculation of correction factor
        n = n + 1

    # if m > 0:                                     # For calculation of correction factor
    #     print "correction 1/m: ", 1/m             # For calculation of correction factor



def SELECTaudiodevice():        # Select an audio device
    global AUDIOdevin
    global AUDIOdevout

    PA = pyaudio.PyAudio()
    ndev = PA.get_device_count()

    n = 0
    ai = ""
    ao = ""
    while n < ndev:
        s = PA.get_device_info_by_index(n)
        # print n, s
        if s['maxInputChannels'] > 0:
            ai = ai + str(s['index']) + ": " + s['name'] + "\n"
        if s['maxOutputChannels'] > 0:
            ao = ao + str(s['index']) + ": " + s['name'] + "\n"
        n = n + 1
    PA.terminate()

    AUDIOdevin = None
    
    s = askstring("Device","Select audio INPUT device:\nPress Cancel for Windows Default\n\n" + ai + "\n\nNumber: ")
    if (s != None):             # If Cancel pressed, then None
        try:                    # Error if for example no numeric characters or OK pressed without input (s = "")
            v = int(s)
        except:
            s = "error"

        if s != "error":
            if v < 0 or v > ndev:
                v = 0
            AUDIOdevin = v

    AUDIOdevout = None

    s = askstring("Device","Select audio OUTPUT device:\nPress Cancel for Windows Default\n\n" + ao + "\n\nNumber: ")
    if (s != None):             # If Cancel pressed, then None
        try:                    # Error if for example no numeric characters or OK pressed without input (s = "")
            v = int(s)
        except:
            s = "error"

        if s != "error":
            if v < 0 or v > ndev:
                v = 0
            AUDIOdevout = v


def ASKWAVfilename():

    filename = askopenfilename(filetypes=[("WAVfile","*.wav"),("allfiles","*")])

    if (filename == None):              # No input, cancel pressed or an error
        filename = ""

    if (filename == ""):
        return(filename)
    
    if filename[-4:] != ".wav":
        filename = filename + ".wav"

    return(filename)


# ================ Make Screen ==========================

root=Tk()
root.title("SpectrumAnalyzer-v02a.py(w) (15-03-2015): Audio Spectrum Analyzer")

root.minsize(100, 100)

frame1 = Frame(root, background=COLORframes, borderwidth=5, relief=RIDGE)
frame1.pack(side=TOP, expand=1, fill=X)

frame2 = Frame(root, background="black", borderwidth=5, relief=RIDGE)
frame2.pack(side=TOP, expand=1, fill=X)

frame3 = Frame(root, background=COLORframes, borderwidth=5, relief=RIDGE)
frame3.pack(side=TOP, expand=1, fill=X)

ca = Canvas(frame2, width=CANVASwidth, height=CANVASheight, background=COLORcanvas)
ca.pack(side=TOP)

b = Button(frame1, text="Normal mode", width=Buttonwidth1, command=BNormalmode)
b.pack(side=LEFT, padx=5, pady=5)

b = Button(frame1, text="Max hold", width=Buttonwidth1, command=BMaxholdmode)
b.pack(side=LEFT, padx=5, pady=5)

b = Button(frame1, text="Average", width=Buttonwidth1, command=BAveragemode)
b.pack(side=LEFT, padx=5, pady=5)

b = Button(frame1, text="FFTwindow", width=Buttonwidth1, command=BFFTwindow)
b.pack(side=LEFT, padx=5, pady=5)

b = Button(frame1, text="Store trace", width=Buttonwidth1, command=BSTOREtrace)
b.pack(side=LEFT, padx=5, pady=5)

b = Button(frame1, text="CSV.file", width=Buttonwidth1, command=BCSVfile)
b.pack(side=LEFT, padx=5, pady=5)

b = Button(frame1, text="Setup", width=Buttonwidth1, command=BSetup)
b.pack(side=RIGHT, padx=5, pady=5)

b = Button(frame1, text="Screen setup", width=Buttonwidth1, command=BScreensetup)
b.pack(side=RIGHT, padx=5, pady=5)

b = Button(frame1, text="Audio on/off", width=Buttonwidth1, command=BAudiostatus)
b.pack(side=RIGHT, padx=5, pady=5)

b = Button(frame3, text="Start", width=Buttonwidth2, command=BStart)
b.pack(side=LEFT, padx=5, pady=5)

b = Button(frame3, text="Stop", width=Buttonwidth2, command=BStop)
b.pack(side=LEFT, padx=5, pady=5)

b = Button(frame3, text="Startfreq", width=Buttonwidth2, command=BStartfrequency)
b.pack(side=LEFT, padx=5, pady=5)

b = Button(frame3, text="Stopfreq", width=Buttonwidth2, command=BStopfrequency)
b.pack(side=LEFT, padx=5, pady=5)

b = Button(frame3, text="+Samples", width=Buttonwidth2, command=Bsamples2)
b.pack(side=RIGHT, padx=5, pady=5)

b = Button(frame3, text="-Samples", width=Buttonwidth2, command=Bsamples1)
b.pack(side=RIGHT, padx=5, pady=5)

b = Button(frame3, text="+dB/div", width=Buttonwidth2, command=BDBdiv2)
b.pack(side=RIGHT, padx=5, pady=5)

b = Button(frame3, text="-dB/div", width=Buttonwidth2, command=BDBdiv1)
b.pack(side=RIGHT, padx=5, pady=5)

b = Button(frame3, text="LVL+10", width=Buttonwidth2, command=Blevel4)
b.pack(side=RIGHT, padx=5, pady=5)

b = Button(frame3, text="LVL-10", width=Buttonwidth2, command=Blevel3)
b.pack(side=RIGHT, padx=5, pady=5)

b = Button(frame3, text="LVL+1", width=Buttonwidth2, command=Blevel2)
b.pack(side=RIGHT, padx=5, pady=5)

b = Button(frame3, text="LVL-1", width=Buttonwidth2, command=Blevel1)
b.pack(side=RIGHT, padx=5, pady=5)

# ================ Call main routine ===============================
root.update()               # Activate updated screens

if WAVinput == 0:
    SELECTaudiodevice()
    AUDIOin()
else:                       # Input from WAV file instead of audio device
    WAVin()
 



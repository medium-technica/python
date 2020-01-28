"""
portaudio.py

Higher-level wrapper for portaudio_.
Brings a somewhat more object-oriented packaging,
in the form of a class called 'stream'
"""

import math

import portaudio_

READ = portaudio_.READ_ONLY
WRITE = portaudio_.WRITE_ONLY
READWRITE = portaudio_.READ_WRITE
MONO = portaudio_.MONO
STEREO = portaudio_.STEREO


class stream:
    """
    Defines a 'stream' class for audio operations
    """
    def __init__(self, samplerate=44100, mode="rw", channels=2):
        """
        Constructor - create an open audio stream

        Arguments:
          - samplerate (default 44100)
          - mode - "r" for read, "w" for write, "rw" for read/write
          - channels - either 1 or 2 (default 2)

        Returns
          - stream handle
        """
        if mode == "r":
            mode_ = READ
        elif mode == "w":
            mode_ = WRITE
        else:
            mode = "rw"
            mode_ = READWRITE

        if channels == 1:
            channels_ = MONO
        else:
            channels_ = STEREO

        self.samplerate = getClosestRate(samplerate)
        self.stream = portaudio_.Open(self.samplerate, mode_, channels_)
        self.mode = mode
        self.channels = channels
        self.wavfiles = {}

    def __del__(self):
        #print "deleting stream handle"
        portaudio_.Close(self.stream)

    def close(self):
        """
        Closes a previously opened audio stream
        """
        portaudio_.Close(self.stream)

    def readableFrames(self):
        """
        readableFrames
        
        Returns the number of frames that could be read from the
        stream without this call blocking

        Arguments:
          - None

        Returns:
          - number of readable frames
        """
        return portaudio_.GetReadable(self.stream)

    def read(self, numframes):
        """
        read

        Read audio frames, and return them as a list of frame tuples
        that can be processed.
        
        Arguments:
          - nframes - number of frames to read and return

        Returns:
          - sequence of frames. Each 'frame' is a tuple, consisting
            of 1 element if mono, 2 if stereo

        Notes:
          - If there aren't enough audio frames available to satisfy this
            request, this function will block until enough frames come
            available.
          - This is one painfully slow function. There's a huge overhead
            in converting raw C buffers into python sequences. If you
            need speed, and don't need to be able to process the received
            data, use readRaw() instead
        """
        return portaudio_.Read(self.stream, numframes)

    def readRaw(self, numframes):
        """
        readRaw

        Reads a number of audio frames and returns these as a raw string.
        Best when you don't need to process the data.
        Runs much faster than the read() method.

        Arguments:
          - nframes - number of frames to read and return
        Returns:
          - raw frame data, returned as a string. Not very useful if you
            want to do any processing, but MUCH faster than Read()!

        Note:
          - If there aren't enough audio frames available to satisfy this request,
            this method will block until enough frames come available
        """
        return portaudio_.ReadRaw(self.stream, numframes)
    
    def writeableFrames(self):
        """
        writeableFrames

        Returns the number of frames that could be written to the
        stream without having to wait.

        Arguments:
         - None

        Returns:
          - number of writeable frames
        """
        return portaudio_.GetWriteable(self.stream)

    def write(self, frames):
        """
        write

        write out a list of frames to audio stream

        Arguments:
          - frames - sequence of frames - each frame is a 1 or 2-element tuple,
            according to whether the stream is mono or stereo. See L{read}

        Returns
          - None

        Notes:
          - This routine will block untill all the data has been written
        """
        portaudio_.Write(self.stream, frames)

    def writeRaw(self, buf):
        """
        Write raw data to audio stream

        Arguments:
          - buf - string of raw data to write, as returned by L{readRaw}

        Returns:
          - None

        Notes:
          - This routine will block untill all the data has been written
          - Faster than L{write}, at a price of not being able to process
            the data
        """

        portaudio_.WriteRaw(self.stream, buf)

    def resample(self, old, oldrate):
        """
        Converts an audio sample from one rate, to a rate which matches
        the currently open stream

        Arguments:
          - frames - sequence of frame tuples
          - oldrate - former sample rate of data
        Returns:
          - frames - a new sequence of frame tuples, converted to
            rate matching this stream
        """
        return portaudio_.Resample(old,
                                   oldrate,
                                   self.samplerate);

    def _convertSampleRate(self, old, oldrate):
        """
        Converts an audio sample from one rate, to a rate which matches
        the currently open stream

        Arguments:
          - frames - sequence of frame tuples
          - oldrate - former sample rate of data
        Returns:
          - frames - a new sequence of frame tuples, converted to
            rate matching this stream
        """

        # Determine sample time in seconds
        oldnSamples = len(old)
        sampTime = float(oldnSamples) / float(oldrate)
        nSamples = int(sampTime * self.samplerate)
        ratio = float(nSamples) / float(oldnSamples)
        
        if self.channels == 1:
            newbuf = [(0,)] * nSamples
            x = 0
            while x < nSamples:
                x0 = float(x) / ratio
                xPart, x0Low = math.modf(x0)
                x0Low = int(x0Low)
                x0High = x0Low + 1
                dx = x0High - x0Low
                y0Low = old[x0Low][0]
                try:
                    y0High = old[x0High][0]
                except:
                    y0High = old[-1][0]
                dy = float(y0High - y0Low)
                y = y0Low + (dy * xPart)
                newbuf[x] = (int(y),)
                #print "x0Low=%f, x0High=%f, xPart=%f, y0Low=%f, y0High=%f, dy=%f" \
                #        % (x0Low, x0High, xPart, y0Low, y0High, dy)
                x += 1
            return newbuf
        else:
            newbuf = [(0,)] * nSamples
            x = 0
            #print "ratio=%f" % ratio
            while x < nSamples:
                x0 = float(x) / ratio
                xPart, x0Low = math.modf(x0)
                x0Low = int(x0Low)
                x0High = x0Low + 1
                dx = x0High - x0Low
                y0LowL = old[x0Low][0]
                y0LowR = old[x0Low][1]
                try:
                    y0HighL = old[x0High][0]
                    y0HighR = old[x0High][1]
                except:
                    y0HighL = old[-1][0]
                    y0HighR = old[-1][1]
                dyL = float(y0HighL - y0LowL)
                dyR = float(y0HighR - y0LowR)
                yL = y0LowL + (dyL * xPart)
                yR = y0LowR + (dyR * xPart)
                newbuf[x] = (int(yL), int(yR))
                #print "x0Low=%f, x0High=%f, xPart=%f, y0Low=%f, y0High=%f, dy=%f" \
                #        % (x0Low, x0High, xPart, y0Low, y0High, dy)
                x += 1
            return newbuf

    def playWavFile(self, path):
        """
        Plays a WAV file.

        Internally, this method reads the WAV data from disk, converts to a raw
        bit stream, and re-samples it to match the sample rate of the currently open
        stream. Once the data is ready, it gets cached in a dict, so that the same
        file won't need to be read more than once.

        Arguments:
          - path - pathname of wav file to play
        Returns:
          - None
        """

        global sounds
        if not self.wavfiles.has_key(path):
            rawFrames, rawRate, rawChannels = readWavFile(path, 2)
            if rawRate != self.samplerate:
                rawFramesNew = self.resample(rawFrames, rawRate)
            self.wavfiles[path] = (rawFramesNew, self.samplerate, rawChannels)
        self.write(self.wavfiles[path][0])

def readWavFile(path, channels=1):
    """
    readWavFile

    Read a WAV file into a raw buffer string, suitable for playing out
    to a stream with the L{writeRaw} method.

    Arguments:
      - file - path of WAV file to read

    Returns:
      - tuple (sequence_of_frames, samplerate, channels)

    Note:
      - to play this WAV data, use L{writeRaw}, not L{write}
    """
    return portaudio_.ReadWavFile(path, channels)

def getClosestRate(rate):
    """
    getClosestRate
    
    Returns the closest available sample rate to the one given
    
    Arguments:
      - wantedRate - desired sample rate

    Returns:
      - actualRate - closest available sample rate to the one wanted
    """
    inRates = portaudio_.GetInputSampleRates()
    outRates = portaudio_.GetOutputSampleRates()

    diffs = []
    for r in inRates:
        if r in outRates:
            diffs.append((r, math.fabs(math.log(rate) - math.log(r))))
    smallest = diffs[0] # impossible
    for r in diffs:
        if r[1] < smallest[1]:
            smallest = r
    return smallest[0]

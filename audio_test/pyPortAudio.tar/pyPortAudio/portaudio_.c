/*
 * pyPortAudio
 *
 * Module: portaudio_.c
 *
 * Lower-level part of the python binding.
 *
 * Author: David McNab <david@rebirthing.co.nz>
 *
 * License: Gnu General Public License
 */

#include "Python.h"
#include "pablio.h"
#include "ringbuffer.h"

#ifdef WIN32
#include "sndfile-win32.h"
#else
#include "sndfile.h"
#endif

/************************************************************
 * UTILITY FUNCTION
 *
 * Get a list of available input sample rates for the default
 * audio device. 
 */

void GetInputSampleRates(int *numRates, double **ratesList)
{
  PaDeviceID inId = Pa_GetDefaultInputDeviceID();
  const PaDeviceInfo *inInfo = Pa_GetDeviceInfo(inId);
  *numRates = inInfo->numSampleRates;
  *ratesList = (double *)inInfo->sampleRates;
}


/*************************************************************
 * UTILITY FUNCTION
 *
 * Get a list of available output sample rates for the default
 * audio device. 
 */

void GetOutputSampleRates(int *numRates, double **ratesList)
{
  PaDeviceID outId = Pa_GetDefaultOutputDeviceID();
  const PaDeviceInfo *outInfo = Pa_GetDeviceInfo(outId);
  *numRates = outInfo->numSampleRates;
  *ratesList = (double *)outInfo->sampleRates;
}


  /**
     long GetAudioStreamWriteable( PABLIO_Stream *aStream );
     long GetAudioStreamReadable( PABLIO_Stream *aStream );
     PaError OpenAudioStream( PABLIO_Stream **aStreamPtr, double sampleRate,
            PaSampleFormat format, long flags );
     long ReadAudioStream( PABLIO_Stream *aStream, void *data, long numFrames );
     long WriteAudioStream( PABLIO_Stream *aStream, void *data, long numFrames );
     PaError CloseAudioStream( PABLIO_Stream *aStream );
  **/

char pa_Open_doc[] = 
"pa_Open\n"
"Arguments:\n"
"  - samplerate (default 44100)\n"
"  - mode - either READ_ONLY, WRITE_ONLY or READ_WRITE (default READ_WRITE)\n"
"  - channels - either MONO or STEREO\n"
"Returns\n"
"  - stream handle\n"
;

PyObject *pa_Open(PyObject *self, PyObject *args, PyObject *kwds)
{
  PABLIO_Stream *pStream;
  double samplerate = 44100;
  int mode = PABLIO_READ | PABLIO_WRITE;
  int channels = PABLIO_STEREO;
  PaError err;

  static char *kwlist[] = {"rate", "mode", "channels", NULL};

  if (!PyArg_ParseTupleAndKeywords(args, kwds, "|dii", kwlist,
                                   &samplerate, &mode, &channels))
    return NULL; 

  err = OpenAudioStream(&pStream, samplerate, paInt16, mode|channels);
  if (err != paNoError)
    return Py_None;
  else
    return Py_BuildValue("l", pStream);
}

char pa_Close_doc[] = 
"pa_Close\n"
"\n"
"Closes an audio stream\n"
"\n"
"Arguments:\n"
"  - stream - handle of audio stream to close\n"
"Returns\n"
"  - None\n"
;

PyObject *pa_Close(PyObject *self, PyObject *args, PyObject *kwds)
{
  PABLIO_Stream *pStream;

  static char *kwlist[] = {"stream", NULL};

  if (!PyArg_ParseTupleAndKeywords(args, kwds, "l", kwlist, &pStream))
    return NULL; 
  if (!pStream)
    return NULL;
  if (pStream)
    CloseAudioStream(pStream);
  return Py_None;
}

char pa_GetInputSampleRates_doc[] =
"GetInputSampleRates\n"
"\n"
"Returns a list of available sample rates for stream input.\n"
"\n"
"Arguments:\n"
"  - None\n"
"Returns - either\n"
"  - A list of available sample rates, OR\n"
"  - A list [-1, minimum, maximum]\n"
;

PyObject *pa_GetInputSampleRates(PyObject *self, PyObject *args)
{
  PyObject *ratesList;

  int numRates;
  double *ratesArray;
  int i;
  
  GetInputSampleRates(&numRates, &ratesArray);

  if (numRates == -1)
    {
      /* Create 3-elem list with [-1, min, max] */
      ratesList = Py_BuildValue("[lll]",
                                -1, (long)ratesArray[0], (long)ratesArray[1]);
    }
  else
    {
      /* Create n-elem list with all the rates */
      ratesList = PyList_New(numRates);
      for (i = 0; i < numRates; i++)
        PyList_SET_ITEM(ratesList, i, Py_BuildValue("l", (long)ratesArray[i]));
    }

  return ratesList;
}


char pa_GetOutputSampleRates_doc[] =
"GetOutputSampleRates\n"
"\n"
"Returns a list of available sample rates for stream output.\n"
"\n"
"Arguments:\n"
"  - None\n"
"Returns - either\n"
"  - A list of available sample rates, OR\n"
"  - A list [-1, minimum, maximum]\n"
;

PyObject *pa_GetOutputSampleRates(PyObject *self, PyObject *args)
{
  PyObject *ratesList;

  int numRates;
  double *ratesArray;
  int i;
  
  GetOutputSampleRates(&numRates, &ratesArray);

  if (numRates == -1)
    {
      /* Create 3-elem list with [-1, min, max] */
      ratesList = Py_BuildValue("[lll]",
                                -1, (long)ratesArray[0], (long)ratesArray[1]);
    }
  else
    {
      /* Create n-elem list with all the rates */
      ratesList = PyList_New(numRates);
      for (i = 0; i < numRates; i++)
        PyList_SET_ITEM(ratesList, i, Py_BuildValue("l", (long)ratesArray[i]));
    }

  return ratesList;
}



char pa_GetReadable_doc[] = 
"GetReadable\n"
"\n"
"Returns the number of frames that could be read from the\n"
"stream without having to wait.\n"
"\n"
"Arguments:\n"
"  - stream - stream handle\n"
"Returns\n"
"  - number of readable frames\n"
;

PyObject *pa_GetReadable(PyObject *self, PyObject *args, PyObject *kwds)
{
  PABLIO_Stream *pStream;
  long res;

  static char *kwlist[] = {"stream", NULL};

  if (!PyArg_ParseTupleAndKeywords(args, kwds, "l", kwlist, &pStream))
    return NULL; 
  if (!pStream)
    return NULL;

  res = GetAudioStreamReadable(pStream);
  return Py_BuildValue("l", res);
}

char pa_ReadRaw_doc[] = 
"pa_ReadRaw\n"
"Arguments:\n"
"  - stream - stream handle\n"
"  - nframes - number of frames to read and return\n"
"Returns:\n"
"  - raw frame data, returned as a string. Not very useful if you\n"
"    want to do any processing, but MUCH faster than Read()!\n"
"\n"
"Note:\n"
"  - If there aren't enough audio frames available to satisfy this request,\n"
"    this function will block until enough frames come available\n"
;

PyObject *pa_ReadRaw(PyObject *self, PyObject *args, PyObject *kwds)
{
  PABLIO_Stream *pStream;
  long nFrames;
  long framesRead;
  short *buf;

  static char *kwlist[] = {"stream", "numframes", NULL};

  if (!PyArg_ParseTupleAndKeywords(args, kwds, "ll", kwlist, &pStream, &nFrames))
    return NULL; 
  if (!pStream)
    return NULL;

  /* Create a big enough buffer for the stream data */
  if ((buf = malloc(nFrames * pStream->bytesPerFrame)) == NULL)
    return NULL;

  /* Suck the raw data */
  framesRead = ReadAudioStream(pStream, buf, nFrames);

  /* return it as a string */
  return Py_BuildValue("s#", buf, framesRead * pStream->bytesPerFrame);
}


char pa_Read_doc[] = 
"pa_Read\n"
"Arguments:\n"
"  - stream - stream handle\n"
"  - nframes - number of frames to read and return\n"
"Returns:\n"
"  - sequence of frames. Each 'frame' is a tuple\n"
"\n"
"Notes:\n"
"  - If there aren't enough audio frames available to satisfy this request,\n"
"    this function will block until enough frames come available\n"
"  - This is one painfully slow function. There's a huge overhead in converting\n"
"    raw C buffers into python sequences. If you need speed, and don't need to be\n"
"    able to process the received data, use ReadRaw() instead\n"
;

PyObject *pa_Read(PyObject *self, PyObject *args, PyObject *kwds)
{
  PABLIO_Stream *pStream;
  long nFrames;
  long framesRead;
  short *buf;
  PyObject *framesList;
  long i;

  static char *kwlist[] = {"stream", "numframes", NULL};

  if (!PyArg_ParseTupleAndKeywords(args, kwds, "ll", kwlist, &pStream, &nFrames))
    return NULL; 
  if (!pStream)
    return NULL;

  /* Create a big enough buffer for the stream data */
  if ((buf = malloc(nFrames * pStream->bytesPerFrame)) == NULL)
    return NULL;

  /* Suck the raw data */
  framesRead = ReadAudioStream(pStream, buf, nFrames);

  /* Build up a list of frames */
  framesList = PyList_New(framesRead);
  if (pStream->samplesPerFrame == 1)
    {
      for (i = 0; i < framesRead; i++)
        {
          PyList_SET_ITEM(framesList, i, Py_BuildValue("(i)", buf[i]));
        }
    }
  else if (pStream->samplesPerFrame == 2)
    {
      for (i = 0; i < framesRead; i++)
        {
          PyList_SET_ITEM(framesList, i, Py_BuildValue("(ii)", buf[i*2], buf[i*2+1]));
        }
    }

  /* finished with buffer */
  free(buf);

  /* send back our frame samples list */
  return framesList;
}

char pa_GetWriteable_doc[] = 
"GetWriteable\n"
"\n"
"Returns the number of frames that could be written to the\n"
"stream without having to wait.\n"
"\n"
"Arguments:\n"
"  - streamPtr\n"
"Returns\n"
"  - number of writeable frames\n"
;

PyObject *pa_GetWriteable(PyObject *self, PyObject *args, PyObject *kwds)
{
  PABLIO_Stream *pStream;
  long res;

  static char *kwlist[] = {"stream", NULL};

  if (!PyArg_ParseTupleAndKeywords(args, kwds, "l", kwlist, &pStream))
    return NULL; 
  if (!pStream)
    return NULL;

  res = GetAudioStreamWriteable(pStream);
  return Py_BuildValue("l", res);
}

char pa_Write_doc[] = 
"pa_Write\n"
"\n"
"Write data to audio stream\n"
"\n"
"Arguments:\n"
"  - stream - handle of stream to write to\n"
"  - frames - sequence of frames - each frame is a 1 or 2-element tuple,\n"
"    according to whether the stream is mono or stereo\n"
"Returns\n"
"  - None\n"
"\n"
"Notes:\n"
"  - This routine will block untill all the data has been written\n"
;

PyObject *pa_Write(PyObject *self, PyObject *args, PyObject *kwds)
{
  PABLIO_Stream *pStream;
  long nFrames;
  long framesWritten;
  short *buf;
  PyObject *framesList;
  int frameSize;
  long i;
  int tmp1, tmp2;
  PyObject *tmpobj;

  static char *kwlist[] = {"stream", "data", NULL};

  if (!PyArg_ParseTupleAndKeywords(args, kwds, "lO", kwlist,
                                   &pStream, &framesList))
    return NULL; 
  if (!pStream)
    return NULL;

  //printf("write: entered\n");
  
  /* Determine number of frames */
  nFrames = PyList_Size(framesList);

  /* Determine number of channels */
  if (nFrames > 0)
    {
      tmpobj = PyList_GetItem(framesList, 0);
      frameSize = PyTuple_Size(tmpobj);
      //printf("tmp=0x%lx, size=%d\n", tmpobj, frameSize);
    }
  else
    return Py_None;

  //printf("write: %d frames of size %d\n", nFrames, frameSize);
  if (frameSize == -1)
    frameSize = 1;

  /* Create temporary buffer */
  buf = malloc(nFrames * pStream->bytesPerFrame);

  //printf("write: ok2\n");

  /*
   * Construct raw buffer from frames list
   */

  /* Build mono output */
  if (pStream->samplesPerFrame == 1)
    {
      //printf("write: ok3\n");
      for (i = 0; i < nFrames; i++)
        {
          PyArg_ParseTuple(PyList_GetItem(framesList, i), "i|i", &tmp1, &tmp2);
          if (frameSize == 1)
            buf[i] = tmp1;
          else
            buf[i] = ((long)tmp1 + (long)tmp2) / 2;
        }
      //printf("write: ok4\n");
    }

  /* build stereo output */
  else if (pStream->samplesPerFrame == 2)
    {
      //printf("write: ok5\n");
      for (i = 0; i < nFrames; i++)
        {
          //printf("dissecting a frame\n");
          PyArg_ParseTuple(PyList_GetItem(framesList, i), "i|i", &tmp1, &tmp2);

          if (frameSize == 1)
            {
              buf[i * 2] = buf[i * 2 + 1] = tmp1;
            }
          else
            {
              buf[i * 2] = tmp1;
              buf[i * 2 + 1] = tmp2;
            }
        }
      //printf("write: ok6\n");
    }

  //printf("write: ok7\n");
  
  /* Dump the raw data */
  framesWritten = WriteAudioStream(pStream, buf, nFrames);

  //printf("write: ok8\n");

  /* discard buffer and framelist ref */
  //printf("ditch buf\n");
  free(buf);
  //printf("ditch ref\n");
  //Py_DECREF(framesList);
  //printf("survived\n");

  /* return it as a string */
  return Py_None;
}


char pa_WriteRaw_doc[] = 
"pa_WriteRaw\n"
"\n"
"Write raw data to audio stream\n"
"\n"
"Arguments:\n"
"  - stream - handle of stream to write to\n"
"  - buf - string of raw data to write\n"
"Returns\n"
"  - None\n"
"\n"
"Notes:\n"
"  - This routine will block untill all the data has been written\n"
"  - Faster than Write(), at a price of not being able to process the data"
;

PyObject *pa_WriteRaw(PyObject *self, PyObject *args, PyObject *kwds)
{
  PABLIO_Stream *pStream;
  long nFrames;
  long framesWritten;
  short *buf;
  int bufSiz;

  static char *kwlist[] = {"stream", "data", NULL};

  if (!PyArg_ParseTupleAndKeywords(args, kwds, "ls#", kwlist,
                                   &pStream, &buf, &bufSiz))
    return NULL; 
  if (!pStream)
    return NULL;

  /* Determine number of frames */
  nFrames = bufSiz / pStream->bytesPerFrame;
  
  /* Dump the raw data */
  framesWritten = WriteAudioStream(pStream, buf, nFrames);

  /* discard buffer */
  free(buf);

  /* return it as a string */
  return Py_None;
}


char pa_ReadWavFileRaw_doc[] = 
"pa_ReadWavFileRaw\n"
"\n"
"Read a WAV file into a raw buffer string\n"
"\n"
"Arguments:\n"
"  - file - path of WAV file to read\n"
"Returns:\n"
"  - tuple:\n"
"      - raw data as a string\n"
"      - number of frames\n"
"      - sample rate\n"
"      - channels\n"
"Note:\n"
"  - to play this WAV data, use WriteRaw(), not Write()\n"
;

#define FRAMES_PER_READ 5000

PyObject *pa_ReadWavFileRaw(PyObject *self, PyObject *args)
{
  char *bufPtr;
  int readCount;
  SNDFILE   *infile;
  SF_INFO   sfinfo ;

  char *file;
  char *buf;
  int nFrames;
  int bytesPerFrame;
  int sampleRate;
  int channels;

  if (!PyArg_ParseTuple(args, "s", &file))
    return NULL; 
  if (!file)
    return NULL;

  nFrames = 0;

  if (!(infile = sf_open(file, SFM_READ, &sfinfo)))
    {
      printf("Not able to open input file %s.\n", file);
      sf_perror (NULL) ;
      return NULL;
    } 

  bytesPerFrame = sfinfo.channels * 2;
  sampleRate = sfinfo.samplerate;
  channels = sfinfo.channels;

  if ((buf = malloc(FRAMES_PER_READ * bytesPerFrame)) == NULL)
    return NULL;

  while (1)
    {
      bufPtr = buf + nFrames * bytesPerFrame;
      readCount = sf_readf_short(infile, (short *)bufPtr, FRAMES_PER_READ);
      if (!readCount)
        break;

      /* extend the buffer */
      nFrames += readCount;
      buf = realloc(buf, (nFrames + FRAMES_PER_READ) * bytesPerFrame);
    }

  sf_close(infile);

  /* make a string of the raw wav data */
  return Py_BuildValue("s#lii", 
                       buf, nFrames * bytesPerFrame,
                       nFrames,
                       sampleRate,
                       channels
                       );
}

char pa_ReadWavFile_doc[] = 
"pa_ReadWavFile\n"
"\n"
"Read a WAV file into a sequence of frames\n"
"\n"
"Arguments:\n"
"  - file - path of WAV file to read\n"
"  - channels - number of channels requested for output\n"
"Returns:\n"
"  - wav data - tuple (list_of_frames_tuples, samplerate, channels)\n"
"Note:\n"
"  - to play this WAV data, use L{Write}, not L{WriteRaw}\n"
;

PyObject *pa_ReadWavFile(PyObject *self, PyObject *args)
{
  char *bufPtr;
  int readCount;
  SNDFILE   *infile;
  SF_INFO   sfinfo ;

  char *file;
  char *buf;
  short *frames;
  int nFrames;
  int bytesPerFrame;
  int sampleRate;
  int channels;
  int channelsOut;
  PyObject *framesList;
  int i;

  if (!PyArg_ParseTuple(args, "si", &file, &channelsOut))
    return NULL; 
  if (!file)
    return NULL;

  nFrames = 0;

  if (!(infile = sf_open(file, SFM_READ, &sfinfo)))
    {
      printf("Not able to open input file %s.\n", file);
      sf_perror (NULL) ;
      return NULL;
    } 

  bytesPerFrame = sfinfo.channels * 2;
  sampleRate = sfinfo.samplerate;
  channels = sfinfo.channels;

  if ((buf = malloc(FRAMES_PER_READ * bytesPerFrame)) == NULL)
    return NULL;

  while (1)
    {
      bufPtr = buf + nFrames * bytesPerFrame;
      readCount = sf_readf_short(infile, (short *)bufPtr, FRAMES_PER_READ);
      if (!readCount)
        break;

      /* extend the buffer */
      nFrames += readCount;
      buf = realloc(buf, (nFrames + FRAMES_PER_READ) * bytesPerFrame);
    }

  sf_close(infile);

  /* Build up a list of frames */
  framesList = PyList_New(nFrames);
  frames = (short *)buf;
  if (channels == 1)
    {
      for (i = 0; i < nFrames; i++)
        {
          if (channelsOut == 1)
            PyList_SET_ITEM(framesList, i, Py_BuildValue("(i)", frames[i]));
          else
            PyList_SET_ITEM(framesList, i, Py_BuildValue("(ii)", frames[i], frames[i]));
        }
    }
  else if (channels == 2)
    {
      for (i = 0; i < nFrames; i++)
        {
          if (channelsOut == 1)
            PyList_SET_ITEM(framesList, i, Py_BuildValue("(i)", ((long)frames[i*2] + (long)frames[i*2+1])/2));
          else
            PyList_SET_ITEM(framesList, i, Py_BuildValue("(ii)", frames[i*2], frames[i*2+1]));
        }
    }

  /* finished with buffer */
  free(buf);

  /* send back our frame samples list */
  return Py_BuildValue("(Oll)", framesList, sampleRate, channels);

}


char pa_Resample_doc[] = 
"pa_Resample\n"
"\n"
"Converts a sample from one sample rate to another\n"
"\n"
"Arguments:\n"
"  - oldsample - list of frames tuples\n"
"  - oldrate  - old sample rate (frames per sec)\n"
"  - newrate  - new sample rate (frames per sec)\n"
"Returns:\n"
"  - wav data - new sample, converted to new sample rate\n"
;

PyObject *pa_Resample(PyObject *self, PyObject *args)
{
  PyObject *oldSample;
  PyObject *newSample;
  int channels;
  int oldrate;
  int newrate;
  //PyObject *ret;
  int x, y, yR;

  int oldnSamples;
  float sampTime;
  int nSamples;
  float ratio;
  //int i;
  PyObject *tmpTuple;

  float x0, xPart, dx, y0Low, y0LowR, y0High=0, y0HighR=0, dy, dyR;
  int x0Low, x0High;

  if (!PyArg_ParseTuple(args, "Oii",
                        &oldSample, &oldrate, &newrate))
    return NULL; 

  /* extract old sample from sequence into C buffer */
  oldnSamples = PyList_Size(oldSample);
  sampTime = (float)oldnSamples / (float)oldrate;
  nSamples = sampTime * newrate;
  ratio = (float)nSamples / (float)oldnSamples;

  /* determine number of channels */
  if (PyList_Size(oldSample) == 0)
    return Py_BuildValue("[]");
  channels = PyTuple_Size(PyList_GET_ITEM(oldSample, 1));

  newSample = PyList_New(nSamples);
  if (channels == 1)
    {
      for (x = 0; x < nSamples; x++)
        {
          x0 = (float)x / ratio;
          x0Low = x0;
          xPart = x0 - (float)x0Low;
          x0High = x0Low + 1;
          dx = x0High - x0Low;
          y0Low = PyInt_AsLong(PyTuple_GET_ITEM(PyList_GET_ITEM(oldSample, x0Low), 0));
          if (x0High < oldnSamples)
            y0High = PyInt_AsLong(PyTuple_GET_ITEM(PyList_GET_ITEM(oldSample, x0High), 0));
          dy = y0High - y0Low;
          y = y0Low + (dy * xPart);
          PyList_SET_ITEM(newSample,
                          x,
                          Py_BuildValue("(i)", (int)y));
        }
      return newSample;
    }
  else
    {
      for (x = 0; x < nSamples; x++)
        {
          x0 = (float)x / ratio;
          x0Low = x0;
          xPart = x0 - (float)x0Low;
          x0High = x0Low + 1;
          dx = x0High - x0Low;
          tmpTuple = PyList_GET_ITEM(oldSample, x0Low);
          y0Low = PyInt_AsLong(PyTuple_GET_ITEM(tmpTuple, 0));
          y0LowR = PyInt_AsLong(PyTuple_GET_ITEM(tmpTuple, 1));
          if (x0High < oldnSamples)
            {
              tmpTuple = PyList_GET_ITEM(oldSample, x0High);
              y0High = PyInt_AsLong(PyTuple_GET_ITEM(tmpTuple, 0));
              y0HighR = PyInt_AsLong(PyTuple_GET_ITEM(tmpTuple, 1));
            }
          dy = y0High - y0Low;
          dyR = y0HighR - y0LowR;
          y = y0Low + (dy * xPart);
          yR = y0LowR + (dyR * xPart);
          PyList_SET_ITEM(newSample,
                          x,
                          Py_BuildValue("(ii)", (int)y, (int)yR));
        }
      return newSample;
    }
}


//****************************************************************************
//* Table of methods - anything you add above has to get added here
//* *************************************************************************

static PyMethodDef portaudioMethods[] = {

  {"Open",
   (PyCFunction)pa_Open,
   METH_KEYWORDS | METH_VARARGS,
   pa_Open_doc
  },

  {"GetInputSampleRates",
   (PyCFunction)pa_GetInputSampleRates,
   0,
   pa_GetInputSampleRates_doc
  },

  {"GetOutputSampleRates",
   (PyCFunction)pa_GetOutputSampleRates,
   0,
   pa_GetOutputSampleRates_doc
  },

  {"Close",
   (PyCFunction)pa_Close,
   METH_KEYWORDS | METH_VARARGS,
   pa_Close_doc
  },

  {"GetReadable",
   (PyCFunction)pa_GetReadable,
   METH_KEYWORDS | METH_VARARGS,
   pa_GetReadable_doc
  },

  {"Read",
   (PyCFunction)pa_Read,
   METH_KEYWORDS | METH_VARARGS,
   pa_Read_doc
  },

  {"ReadRaw",
   (PyCFunction)pa_ReadRaw,
   METH_KEYWORDS | METH_VARARGS,
   pa_ReadRaw_doc
  },

  {"GetWriteable",
   (PyCFunction)pa_GetWriteable,
   METH_KEYWORDS | METH_VARARGS,
   pa_GetWriteable_doc
  },

  {"Write",
   (PyCFunction)pa_Write,
   METH_KEYWORDS | METH_VARARGS,
   pa_Write_doc
  },

  {"WriteRaw",
   (PyCFunction)pa_WriteRaw,
   METH_KEYWORDS | METH_VARARGS,
   pa_WriteRaw_doc
  },

  {"ReadWavFile",
   (PyCFunction)pa_ReadWavFile,
   METH_VARARGS,
   pa_ReadWavFile_doc
  },

  {"ReadWavFileRaw",
   (PyCFunction)pa_ReadWavFileRaw,
   METH_VARARGS,
   pa_ReadWavFileRaw_doc
  },

  {"Resample",
   (PyCFunction)pa_Resample,
   METH_VARARGS,
   pa_Resample_doc
  },

  /* Sentinel */
  {NULL, NULL, 0, NULL}
  };

char doc_module[] = "This is the docstring for portaudio_";

void
initportaudio_(void)
{
  PyObject *module;

  module = Py_InitModule3("portaudio_", portaudioMethods, doc_module);

  /* Create the module constants */
  PyObject_SetAttrString(module, "READ_ONLY", Py_BuildValue("i", PABLIO_READ));
  PyObject_SetAttrString(module, "WRITE_ONLY", Py_BuildValue("i", PABLIO_WRITE));
  PyObject_SetAttrString(module, "READ_WRITE", Py_BuildValue("i", PABLIO_READ_WRITE));
  PyObject_SetAttrString(module, "MONO", Py_BuildValue("i", PABLIO_MONO));
  PyObject_SetAttrString(module, "STEREO", Py_BuildValue("i", PABLIO_STEREO));
}

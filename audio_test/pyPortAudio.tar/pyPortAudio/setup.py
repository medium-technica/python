#!/usr/bin/env python
# Python setup script for PortAudio python wrapper.
#
# Written David McNab, 11 Feb 2003

import sys,os
from distutils.core import setup, Extension

paSources = ['portaudio_.c',
                     '../pablio/pablio.c',
                     '../pablio/ringbuffer.c',
                     '../pa_common/pa_lib.c']

paRuntimeLibDirs = None
#paLibs = ['sndfile']
paLibs = ['sndfile']


# Yikes - we're very implementation-dependent here

if sys.platform.find('linux') != -1:
    print "Adding '../pa_unix_oss.c' for *nix OS"
    paSources.append('../pa_unix_oss/pa_unix_oss.c')
    paRuntimeLibDirs = ['/usr/lib', '/usr/local/lib']
    paDefines = None
elif sys.platform == 'win32':
    print "Adding '../pa_win_wmme.c' for windoze"
    paSources.append('../pa_win_wmme/pa_win_wmme.c')
    paLibs=['winmm', 'libsndfile']
    paDefines = ['WIN32', None]
    pass
else:
    print "Sorry - I don't know how to build Portaudio_ for your system"
    print "Why not try hacking this setup script and reading through"
    print "some of the source code? Shouldn't be too hard."
    sys.exit(1)

portaudio_ = Extension('portaudio_',
                       sources=paSources,
                       include_dirs=["../pablio",
                                     "../pa_common",
                                     "/usr/include"
                                     ],
                       define_macros=paDefines,
                       extra_compile_args=['-g'],
                       libraries=paLibs,
                       library_dirs=['/usr/lib', '/usr/local/lib'],
                       runtime_library_dirs=paRuntimeLibDirs
				 )

setup(name='portaudio',
	  version = '0.1',
	  description = 'Python bindings for PortAudio (pablio layer)',
      py_modules = ['portaudio'],
	  ext_modules = [portaudio_]
	  )

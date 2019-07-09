
### Introduction

The Keyword Detector  is a customizable hotword detection engine for the FAPS Demonstrator. 
You to create your own hotword like "OK Tobi" or "Eva". It is powered by the snowboy library and therefore:

* **highly customizable**: you can freely define your own magic phrase here –
let it be “Ok Demonstrator”, "Hey Tobias", etc... , you name it.

* **always listening** but protects your privacy: the keyword detector does not use Internet
and does *not* stream your voice to the cloud. Everything is computed on the device

* light-weight and **embedded**: the current application can run on every hardware with a linux installation.
It even runs on a Raspberry Pi and consumes less than 10% CPU on the weakest Pi (single-core 700MHz ARMv6).

* Apache licensed!

Currently we have built wrappers for:

* Python2/Python3

### Dependencies

To run the module you will likely need the following:

* SoX (audio conversion)
* PortAudio or PyAudio (audio capturing)
* ATLAS or OpenBLAS (matrix computation)

### Installation Ubuntu/Raspberry Pi

First `apt-get` install `sox`, `portaudio` and its Python binding `pyaudio`:

    sudo apt-get install python-pyaudio python3-pyaudio sox
    pip install pyaudio
Compile a supported swig version (3.0.10 or above)

    wget http://downloads.sourceforge.net/swig/swig-3.0.10.tar.gz
    sudo apt-get install libpcre3 libpcre3-dev
    ./configure --prefix=/usr                  \
            --without-clisp                    \
            --without-maximum-compile-warnings &&
    make
    make install &&
    install -v -m755 -d /usr/share/doc/swig-3.0.10 &&
    cp -v -R Doc/* /usr/share/doc/swig-3.0.10
       
Then install the `atlas` matrix computing library:

    sudo apt-get install libatlas-base-dev
    
Make sure that you can record audio with your microphone:

    rec t.wav
        
If you need extra setup on your audio (especially on a Raspberry Pi), please see the rasperry pi documentation.

### Test

Execute the following command and say "Tobi" via your microphone.

    python demo.py
    

### Running

Execute the following command 

    python FAPSKeyWordDetector.py

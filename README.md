# SecurityCamera

The project is used protect your house with a  Raspberry Pi Camera Module connected to a Raspberry Pi.
## Installation

### Requirements
* Raspberry Pi
* Raspberry Pi Camera module
* python 2.7

### Installing
First install the face_recognition  library by ageitgey and follow the [instructions](https://gist.github.com/ageitgey/1ac8dbe8572f3f533df6269dab35df65) for instalation on Raspberry Pi.

Then, install the opencv library using the [instuctions](https://www.pyimagesearch.com/2018/09/26/install-opencv-4-on-your-raspberry-pi/) from pyimagesearch.

At the end, install Flaks library using pip.
```bash
pip install opencv-python
```

## Runnig
After installing all the libraries clone the code from the git repository and run main.py:
```bash
sudo python main.py
```


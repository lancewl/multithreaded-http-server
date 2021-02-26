# Multithreaded HTTP Server

## Requirement

* Python 3.7 and above

## Installation

### [pip](https://pip.pypa.io/en/stable/)

```bash
pip install requirements.txt
```

### [pipenv](https://pipenv.kennethreitz.org/en/latest/#) 

Use pipenv to manage and install the Python packages.

```bash
pipenv install
```

## Usage

### Server Script

The `server.py` will run a multithreaded HTTP Server serving the current folder by default.

```bash
Usage: server.py [OPTIONS]

Options:
  --port INTEGER  Listening Port
  --dir TEXT      Serving directory relative to current directory
  --help          Show this message and exit.
```

Example:

```bash
python server.py --port 1234 --dir test/test_32k
```

Above command will run the server on port 1234 and serve the test/test_32k directory(relative to the current directory).

### Client Script

The `client.py` will ask you several questions about your experiments then spawning multiple clients to download the files you selected.

Run:

```bash
python client.py
```

Preview of questions be asked from the script:

```bash
? Please enter the server IP and port:  http://localhost:8888/
```

```bash
? Please Choose the files to download: (<up>, <down> to move, <space> to select, <a> to toggle, <i> to invert)
> o A.txt
  o B.txt
  o C.txt
```

```bash
? Please choose the mode for downloading: (Use arrow keys)
> serial
  parallel
```

```bash
? How many client would you like to spawn?  1
```

```bash
? How many experiments would you like to repeat for each client?  1
```

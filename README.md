# HTTPDummy

```
                                    __________________
                                   /        ________  \
                                  /   _____|       |___\
                                 |   /  __         __   |
                                /|  |  /o \   _   /o \  |  
                               | | /           \        |
                                \|/   __           __   |
                                  \    |\_________/|   /   
                                   \___|___________|__/                  
                                        |         |
                                       /\_________/\
    _   _ _____ _____ ____  ____     _/     \ /     \_
   | | | |_   _|_   _|  _ \|  _ \ _ | _ _ __ V__  _ __|___  _   _
   | |_| | | |   | | | |_) | | | | | | | '_ ` _ \| '_ ` _ \| | | |
   |  _  | | |   | | |  __/| |_| | |_| | | | | | | | | | | | |_| |
   |_| |_| |_|   |_| |_|   |____/ \__,_|_| |_| |_|_| |_| |_|\__, |
                                                            |___/
```

HTTPDummy is a development HTTP server tool that prints information about the requests it receives to stdout.

## Installation

```
pip install httpdummy
```

## Usage

```
usage: httpdummy [-h] [-H [HEADERS]] [-B [BODY]] [-a ADDRESS] [-p PORT]
                 [-r [RESPONSE_FILE]]

A dummy http server that prints requests and responds

optional arguments:
  -h, --help            show this help message and exit
  -H [HEADERS], --headers [HEADERS]
  -B [BODY], --body [BODY]
  -a ADDRESS, --address ADDRESS
  -p PORT, --port PORT
  -r [RESPONSE_FILE], --response-file [RESPONSE_FILE]
```

  - Add the `-H` flag to print request headers.
  - Add the `-B` flag to print request body.

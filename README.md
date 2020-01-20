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

Use the `--response-file` to specify a YAML file to set up custom responses for arbitrary method / path combinations. For example, this command...

```
httpdummy --response-file ~/repsonses.yaml
```

... with `~/responses.yaml` contents ...

```
---
responses:
  POST /api/foo:
    status: 201
    headers:
      Foo: bar
      Sna: fu
    body: |+
      Hi there!
```

... will make HTTPDummy respond to POST requests to `/api/foo` with the 201 status code, and the configured headers and body.

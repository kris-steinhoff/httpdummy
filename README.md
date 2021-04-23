# HTTPDummy

HTTPDummy is a development HTTP server tool that prints information about the requests it receives to stdout.

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

## Installation

With PIP:

```
pip install httpdummy
```

With Docker:

```
docker pull ksofa2/httpdummy
```

## Usage

```
usage: httpdummy [-h] [-a ADDRESS] [-p PORT] [-H | --print-headers {on,off}]
                 [-B | --print-body {on,off}] [--server-reloader {on,off}]
                 [--server-reloader-type {stat,watchdog}]
                 [--server-debugger {on,off}]
                 [config_file]

A dummy http server that prints requests and responds

positional arguments:
  config_file           path to configuration file

optional arguments:
  -h, --help            show this help message and exit
  -a ADDRESS, --address ADDRESS
                        address to bind to (default 127.0.0.1)
  -p PORT, --port PORT  port to open on (default 5000)
  -H
  --print-headers {on,off}
                        print request headers to stdout
  -B
  --print-body {on,off}
                        print request body to stdout
  --server-reloader {on,off}
                        enable Werkzeug server reloader (default on if
                        config_file is specified)
  --server-reloader-type {stat,watchdog}
                        Werkzeug server reloader type (default watchdog)
  --server-debugger {on,off}
                        enable Werkzeug server debugger (default off)
```

```
httpdummy ~/httpdummy_config.yml
```

... with `~/httpdummy_config.yml` contents ...

```
---
responses:
  GET /api/foo:
    status: 200
    headers:
      Foo: bar
      Sna: fu
    body: |+
      Hi there!

      How are you?

  POST /api/foo:
    status: 201
    headers:
      Content-type: application/json
    body: |+
      {"answer": 42}
```

... will make HTTPDummy respond to POST requests to `/api/foo` with the 201 status code, and the configured headers and body.

NOTE: When started with a config file, HTTPDummy will listen for changes to that file and restart when a change is detected to reload the config file.

## Docker

An image for HTTPDummy is available on DockerHub: <https://hub.docker.com/r/ksofa2/httpdummy>

```
docker run -it -p 127.0.0.1:5000:5000 ksofa2/httpdummy
```

The Docker image can be configured with environment variables, which are set with these defaults:

```
HTTPDUMMY_ADDRESS=0.0.0.0
HTTPDUMMY_PORT=5000
HTTPDUMMY_PRINT_HEADERS=on
HTTPDUMMY_PRINT_BODY=on
HTTPDUMMY_SERVER_RELOADER=on
HTTPDUMMY_SERVER_RELOADER_TYPE=stat
HTTPDUMMY_SERVER_DEBUGGER=off
HTTPDUMMY_CONFIG_FILE=
```

An example `docker-compose.yaml` file:

```
---
version: '3'

services:
  httpdummy:
    image: ksofa2/httpdummy
    environment:
      - HTTPDUMMY_CONFIG_FILE=/srv/httpdummy_config.yml
    ports:
      - 127.0.0.1:5000:5000
    volumes:
      - .:/srv
```

V3SProtoComm
============

V3SProtoComm is a library for communication and control of robots via Protobuf.
The library supports the following communications:

  - Receiving vision data in polling and multithread mode
  - Sending speed commands in polling and multithread mode
  - Receiving game data from the VSSReferee in polling mode
  - Sending replacement packages to the VSSReplacer in polling mode

[![Python package](https://github.com/TauraBots/V3SProtoComm/actions/workflows/python-package.yml/badge.svg)](https://github.com/TauraBots/V3SProtoComm/actions/workflows/python-package.yml)

Installation
------------

You can install the package directly from GitHub with pip:
```
    pip install git+https://github.com/TauraBots/V3SProtoComm.git
```
Or, if you have cloned the repository, install the dependencies from the requirements file:
```
    pip3 install -r requirements.txt
```
Usage
-----

To test the package, run the "gotoball.py" example:

    python3 gotoball.py

The example uses vision data to control a differential drive robot, directing it
towards the ball by rotating to align its orientation and moving forward until
it is close enough (i.e., when it "dominates" the ball).

Project Structure
-----------------
```
V3SProtoComm/
├── core
│   ├── comm
│   │   ├── controls.py
│   │   ├── __init__.py
│   │   ├── protocols
│   │   │   ├── command_pb2.py
│   │   │   ├── common_pb2.py
│   │   │   ├── __init__.py
│   │   │   ├── packet_pb2.py
│   │   │   ├── protobuf
│   │   │   │   ├── firasim
│   │   │   │   │   ├── command.proto
│   │   │   │   │   ├── common.proto
│   │   │   │   │   ├── packet.proto
│   │   │   │   │   ├── protobuf.sh
│   │   │   │   │   └── replacement.proto
│   │   │   │   ├── __init__.py
│   │   │   │   └── vssreferee
│   │   │   │       ├── protobuf.sh
│   │   │   │       ├── vssref_command.proto
│   │   │   │       ├── vssref_common.proto
│   │   │   │       └── vssref_placement.proto
│   │   ├── __init__.py
│   │   ├── receiver.py
│   │   ├── referee.py
│   │   ├── replacer.py
│   │   ├── thread_job.py
│   │   ├── transmitter.py
│   │   └── vision.py
├── gotoball.py
├── README.txt
├── requirements.txt
└── tests.py

```
> [!NOTE]
>  To ensure that the non-Python files (such as the .proto files in the protobuf directory)
>  are included in the package, a MANIFEST.in file is used with the following directive:

------------

      recursive-include core/comm/protocols/protobuf *

Contributing
------------

Contributions are welcome! Feel free to open issues or submit pull requests.


# IPE ServiceHub Protos

This package contains Python bindings for communicating with
the [ServiceHub](https://arxiv.org/abs/2011.00112).
The bindings are auto-generated from the raw `.proto` files
and published to `PyPi`.

This package is rarely used itself. 
Rather, more elaborate packages such as
[qiclib](https://github.com/quantuminterface/qiclib) or [cirque](https://gitlab.kit.edu/kit/ipe-sdr/ipe-sdr-dev/software/cirque)
provide wrappers to enable higher level APIs

## Installation

```bash
pip install ipe_servicehub_protos
```

## Usage

```python
import ipe_servicehub_protos.oscilloscope_pb2

channel = ipe_servicehub_protos.oscilloscope_pb2.Channel(value=0)
# ... 
```

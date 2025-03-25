def test_can_import_protos():
    import ipe_servicehub_protos.oscilloscope_pb2
    import ipe_servicehub_protos.oscilloscope_pb2_grpc

    _channel = ipe_servicehub_protos.oscilloscope_pb2.Channel(value=1)
    _stub = ipe_servicehub_protos.oscilloscope_pb2_grpc.OscilloscopeService()

def test_can_import_protos_relative():
    from ipe_servicehub_protos import oscilloscope_pb2, oscilloscope_pb2_grpc

    _channel = oscilloscope_pb2.Channel(value=1)
    _stub = oscilloscope_pb2_grpc.OscilloscopeService()

import ipe_servicehub_protos


def test_has_version():
    assert isinstance(ipe_servicehub_protos.__version__, str)
    assert isinstance(ipe_servicehub_protos.__version_tuple__, tuple)


import qiclib.packages.grpc.datatypes_pb2 as _datatypes_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DataCollectionMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AVERAGE: _ClassVar[DataCollectionMode]
    AMPLITUDE_PHASE: _ClassVar[DataCollectionMode]
    IQCLOUD: _ClassVar[DataCollectionMode]
    RAW_TRACE: _ClassVar[DataCollectionMode]
    STATES: _ClassVar[DataCollectionMode]
    STATE_COUNT: _ClassVar[DataCollectionMode]
    QM_JUMPS: _ClassVar[DataCollectionMode]
AVERAGE: DataCollectionMode
AMPLITUDE_PHASE: DataCollectionMode
IQCLOUD: DataCollectionMode
RAW_TRACE: DataCollectionMode
STATES: DataCollectionMode
STATE_COUNT: DataCollectionMode
QM_JUMPS: DataCollectionMode

class CellIndexes(_message.Message):
    __slots__ = ("cells",)
    CELLS_FIELD_NUMBER: _ClassVar[int]
    cells: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, cells: _Optional[_Iterable[int]] = ...) -> None: ...

class CellInfo(_message.Message):
    __slots__ = ("sequencer", "recording", "readout", "manipulation", "coupling", "storage", "digital_trigger")
    SEQUENCER_FIELD_NUMBER: _ClassVar[int]
    RECORDING_FIELD_NUMBER: _ClassVar[int]
    READOUT_FIELD_NUMBER: _ClassVar[int]
    MANIPULATION_FIELD_NUMBER: _ClassVar[int]
    COUPLING_FIELD_NUMBER: _ClassVar[int]
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    DIGITAL_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    sequencer: int
    recording: int
    readout: int
    manipulation: int
    coupling: int
    storage: int
    digital_trigger: int
    def __init__(self, sequencer: _Optional[int] = ..., recording: _Optional[int] = ..., readout: _Optional[int] = ..., manipulation: _Optional[int] = ..., coupling: _Optional[int] = ..., storage: _Optional[int] = ..., digital_trigger: _Optional[int] = ...) -> None: ...

class AllCellInfo(_message.Message):
    __slots__ = ("cells",)
    CELLS_FIELD_NUMBER: _ClassVar[int]
    cells: _containers.RepeatedCompositeFieldContainer[CellInfo]
    def __init__(self, cells: _Optional[_Iterable[_Union[CellInfo, _Mapping]]] = ...) -> None: ...

class StartCellInfo(_message.Message):
    __slots__ = ("all_cells", "cells")
    ALL_CELLS_FIELD_NUMBER: _ClassVar[int]
    CELLS_FIELD_NUMBER: _ClassVar[int]
    all_cells: bool
    cells: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, all_cells: bool = ..., cells: _Optional[_Iterable[int]] = ...) -> None: ...

class BusyCellInfo(_message.Message):
    __slots__ = ("busy", "cells")
    BUSY_FIELD_NUMBER: _ClassVar[int]
    CELLS_FIELD_NUMBER: _ClassVar[int]
    busy: bool
    cells: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, busy: bool = ..., cells: _Optional[_Iterable[int]] = ...) -> None: ...

class QubitStateCellInfo(_message.Message):
    __slots__ = ("states",)
    STATES_FIELD_NUMBER: _ClassVar[int]
    states: int
    def __init__(self, states: _Optional[int] = ...) -> None: ...

class PlatformInfo(_message.Message):
    __slots__ = ("cell_count", "dac_count", "adc_count")
    CELL_COUNT_FIELD_NUMBER: _ClassVar[int]
    DAC_COUNT_FIELD_NUMBER: _ClassVar[int]
    ADC_COUNT_FIELD_NUMBER: _ClassVar[int]
    cell_count: int
    dac_count: int
    adc_count: int
    def __init__(self, cell_count: _Optional[int] = ..., dac_count: _Optional[int] = ..., adc_count: _Optional[int] = ...) -> None: ...

class DACStatus(_message.Message):
    __slots__ = ("ready", "overflow")
    READY_FIELD_NUMBER: _ClassVar[int]
    OVERFLOW_FIELD_NUMBER: _ClassVar[int]
    ready: bool
    overflow: bool
    def __init__(self, ready: bool = ..., overflow: bool = ...) -> None: ...

class ADCStatus(_message.Message):
    __slots__ = ("valid", "over_voltage", "over_range")
    VALID_FIELD_NUMBER: _ClassVar[int]
    OVER_VOLTAGE_FIELD_NUMBER: _ClassVar[int]
    OVER_RANGE_FIELD_NUMBER: _ClassVar[int]
    valid: bool
    over_voltage: bool
    over_range: bool
    def __init__(self, valid: bool = ..., over_voltage: bool = ..., over_range: bool = ...) -> None: ...

class ConverterStatus(_message.Message):
    __slots__ = ("error", "report", "dacs", "adcs")
    ERROR_FIELD_NUMBER: _ClassVar[int]
    REPORT_FIELD_NUMBER: _ClassVar[int]
    DACS_FIELD_NUMBER: _ClassVar[int]
    ADCS_FIELD_NUMBER: _ClassVar[int]
    error: bool
    report: str
    dacs: _containers.RepeatedCompositeFieldContainer[DACStatus]
    adcs: _containers.RepeatedCompositeFieldContainer[ADCStatus]
    def __init__(self, error: bool = ..., report: _Optional[str] = ..., dacs: _Optional[_Iterable[_Union[DACStatus, _Mapping]]] = ..., adcs: _Optional[_Iterable[_Union[ADCStatus, _Mapping]]] = ...) -> None: ...

class DACIndex(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: int
    def __init__(self, value: _Optional[int] = ...) -> None: ...

class DACSignalTypes(_message.Message):
    __slots__ = ("types",)
    TYPES_FIELD_NUMBER: _ClassVar[int]
    types: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, types: _Optional[_Iterable[int]] = ...) -> None: ...

class DACRouting(_message.Message):
    __slots__ = ("type", "dac", "cells")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DAC_FIELD_NUMBER: _ClassVar[int]
    CELLS_FIELD_NUMBER: _ClassVar[int]
    type: int
    dac: int
    cells: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, type: _Optional[int] = ..., dac: _Optional[int] = ..., cells: _Optional[_Iterable[int]] = ...) -> None: ...

class ADCIndexes(_message.Message):
    __slots__ = ("adcs",)
    ADCS_FIELD_NUMBER: _ClassVar[int]
    adcs: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, adcs: _Optional[_Iterable[int]] = ...) -> None: ...

class ADCRouting(_message.Message):
    __slots__ = ("adc", "cells", "mode")
    ADC_FIELD_NUMBER: _ClassVar[int]
    CELLS_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    adc: int
    cells: _containers.RepeatedScalarFieldContainer[int]
    mode: int
    def __init__(self, adc: _Optional[int] = ..., cells: _Optional[_Iterable[int]] = ..., mode: _Optional[int] = ...) -> None: ...

class ExperimentParameters(_message.Message):
    __slots__ = ("mode", "shots", "cells", "recordings")
    MODE_FIELD_NUMBER: _ClassVar[int]
    SHOTS_FIELD_NUMBER: _ClassVar[int]
    CELLS_FIELD_NUMBER: _ClassVar[int]
    RECORDINGS_FIELD_NUMBER: _ClassVar[int]
    mode: DataCollectionMode
    shots: int
    cells: _containers.RepeatedScalarFieldContainer[int]
    recordings: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, mode: _Optional[_Union[DataCollectionMode, str]] = ..., shots: _Optional[int] = ..., cells: _Optional[_Iterable[int]] = ..., recordings: _Optional[_Iterable[int]] = ...) -> None: ...

class ExperimentResults(_message.Message):
    __slots__ = ("progress", "max_progress", "finished", "mode", "results")
    class SingleCellResults(_message.Message):
        __slots__ = ("data_double_1", "data_double_2", "data_sint32_1", "data_sint32_2", "data_uint32")
        DATA_DOUBLE_1_FIELD_NUMBER: _ClassVar[int]
        DATA_DOUBLE_2_FIELD_NUMBER: _ClassVar[int]
        DATA_SINT32_1_FIELD_NUMBER: _ClassVar[int]
        DATA_SINT32_2_FIELD_NUMBER: _ClassVar[int]
        DATA_UINT32_FIELD_NUMBER: _ClassVar[int]
        data_double_1: _containers.RepeatedScalarFieldContainer[float]
        data_double_2: _containers.RepeatedScalarFieldContainer[float]
        data_sint32_1: _containers.RepeatedScalarFieldContainer[int]
        data_sint32_2: _containers.RepeatedScalarFieldContainer[int]
        data_uint32: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, data_double_1: _Optional[_Iterable[float]] = ..., data_double_2: _Optional[_Iterable[float]] = ..., data_sint32_1: _Optional[_Iterable[int]] = ..., data_sint32_2: _Optional[_Iterable[int]] = ..., data_uint32: _Optional[_Iterable[int]] = ...) -> None: ...
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    MAX_PROGRESS_FIELD_NUMBER: _ClassVar[int]
    FINISHED_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    progress: int
    max_progress: int
    finished: bool
    mode: DataCollectionMode
    results: _containers.RepeatedCompositeFieldContainer[ExperimentResults.SingleCellResults]
    def __init__(self, progress: _Optional[int] = ..., max_progress: _Optional[int] = ..., finished: bool = ..., mode: _Optional[_Union[DataCollectionMode, str]] = ..., results: _Optional[_Iterable[_Union[ExperimentResults.SingleCellResults, _Mapping]]] = ...) -> None: ...

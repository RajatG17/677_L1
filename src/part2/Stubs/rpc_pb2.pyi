from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class stockLookupMessage(_message.Message):
    __slots__ = ["stockName"]
    STOCKNAME_FIELD_NUMBER: _ClassVar[int]
    stockName: str
    def __init__(self, stockName: _Optional[str] = ...) -> None: ...

class stockLookupResponseMessage(_message.Message):
    __slots__ = ["lookupResponse", "tradingVolume"]
    LOOKUPRESPONSE_FIELD_NUMBER: _ClassVar[int]
    TRADINGVOLUME_FIELD_NUMBER: _ClassVar[int]
    lookupResponse: float
    tradingVolume: int
    def __init__(self, lookupResponse: _Optional[float] = ..., tradingVolume: _Optional[int] = ...) -> None: ...

class stockTradeRequestMessage(_message.Message):
    __slots__ = ["N", "stockName", "type"]
    N: int
    N_FIELD_NUMBER: _ClassVar[int]
    STOCKNAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    stockName: str
    type: str
    def __init__(self, stockName: _Optional[str] = ..., N: _Optional[int] = ..., type: _Optional[str] = ...) -> None: ...

class stockTradeResponseMessage(_message.Message):
    __slots__ = ["tradeResult"]
    TRADERESULT_FIELD_NUMBER: _ClassVar[int]
    tradeResult: int
    def __init__(self, tradeResult: _Optional[int] = ...) -> None: ...

class stockUpdateRequestMessage(_message.Message):
    __slots__ = ["price", "stockName"]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    STOCKNAME_FIELD_NUMBER: _ClassVar[int]
    price: float
    stockName: str
    def __init__(self, stockName: _Optional[str] = ..., price: _Optional[float] = ...) -> None: ...

class stockUpdateResponseMessage(_message.Message):
    __slots__ = ["updateResult"]
    UPDATERESULT_FIELD_NUMBER: _ClassVar[int]
    updateResult: int
    def __init__(self, updateResult: _Optional[int] = ...) -> None: ...

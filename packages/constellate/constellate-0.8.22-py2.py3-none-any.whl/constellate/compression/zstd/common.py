import codecs
from typing import Union, Protocol, Optional

Encoder = Union[str, codecs.Codec]
Decoder = Union[str, codecs.Codec]


class ZstdCompressionParameters:
    def __init__(
        self,
        level: int = 3,
        write_checksum: bool = True,
        write_content_size: bool = True,
        threads: int = -1,
        encoder: Optional[Encoder] = "utf-8",
        decoder: Optional[Decoder] = "utf-8",
    ):
        self._level = level
        self._write_checksum = write_checksum
        self._write_content_size = write_content_size
        self._threads = threads

        if isinstance(encoder, str):
            encoder = codecs.lookup(encoder)
        if isinstance(decoder, str):
            decoder = codecs.lookup(decoder)

        self._encoder = encoder
        self._decoder = decoder

    @property
    def level(self) -> int:
        return self._level

    @property
    def write_checksum(self) -> bool:
        return self._write_checksum

    @property
    def write_content_size(self) -> bool:
        return self._write_content_size

    @property
    def threads(self) -> int:
        return self._threads

    @property
    def encoder(self) -> Optional[codecs.Codec]:
        return self._encoder

    @property
    def decoder(self) -> Optional[codecs.Codec]:
        return self._decoder


DataInput = Union[bytes, str]
DataOutput = Union[bytes, str]


class ZstdCompressorProtocol(Protocol):
    def compress(self, data: DataInput = None) -> bytes:
        pass


class ZstdDecompressorProtocol(Protocol):
    def decompress(self, data: Union[bytes] = None) -> DataOutput:
        pass

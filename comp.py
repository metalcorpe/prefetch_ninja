import sys
import ctypes
import enum

class CompAlgo(enum.Enum):
    COMPRESSION_FORMAT_NONE = 0x0000
    COMPRESSION_FORMAT_DEFAULT = 0x0001
    COMPRESSION_FORMAT_LZNT1 = 0x0002
    COMPRESSION_FORMAT_XPRESS = 0x0003
    COMPRESSION_FORMAT_XPRESS_HUFF = 0x0004

class CompEngi(enum.Enum):
    COMPRESSION_ENGINE_STANDARD = 0x0000
    COMPRESSION_ENGINE_MAXIMUM = 0x0100
    COMPRESSION_ENGINE_HIBER = 0x0200

class ErrorCodes(enum.Enum):
    STATUS_SUCCESS = 0x00000000
    STATUS_BUFFER_ALL_ZEROS = 0x00000117
    STATUS_INVALID_PARAMETER = 0xC000000D
    STATUS_UNSUPPORTED_COMPRESSION = 0xC000025F
    STATUS_NOT_SUPPORTED = 0xC00000BB
    STATUS_BUFFER_TOO_SMALL = 0xC0000023

def tohex(val, nbits):
    """Utility to convert (signed) integer to hex."""
    return hex((val + (1 << nbits)) % (1 << nbits))

def compress(algo:CompAlgo, uncompressed,
             engine:CompEngi=CompEngi.COMPRESSION_ENGINE_STANDARD, chunk_size:int=4096):

    calgo = algo.value|engine.value

    NULL = ctypes.POINTER(ctypes.c_uint)()
    SIZE_T = ctypes.c_uint
    DWORD = ctypes.c_uint32
    USHORT = ctypes.c_uint16
    UCHAR = ctypes.c_ubyte
    ULONG = ctypes.c_uint32

    # You must have at least Windows 8, or it should fail.
    try:
        RtlCompressBuffer = ctypes.windll.ntdll.RtlCompressBuffer
    except AttributeError as e:
        sys.exit("[ - ] {e}\n"
                 "[ - ] Windows 8+ required for this script to decompress Win10 Prefetch files")

    RtlGetCompressionWorkSpaceSize = \
        ctypes.windll.ntdll.RtlGetCompressionWorkSpaceSize


    ntCompressBufferWorkSpaceSize = ULONG()
    ntCompressFragmentWorkSpaceSize = ULONG()

    ntstatus = RtlGetCompressionWorkSpaceSize(USHORT(calgo),
                                              ctypes.byref(ntCompressBufferWorkSpaceSize),
                                              ctypes.byref(ntCompressFragmentWorkSpaceSize))

    if ntstatus:
        raise EnvironmentError(f'Cannot get workspace size, err: '
                               f'{tohex(ntstatus, 32)}:{ErrorCodes(tohex(ntstatus, 32)).name}')

    uncompressed_size = len(uncompressed)

    ntUnCompressed = (UCHAR * uncompressed_size).from_buffer_copy(uncompressed)
    ntCompressed = (UCHAR * uncompressed_size)()
    ntFinalCompressedSize = ULONG()
    ntWorkspace = (UCHAR * ntCompressBufferWorkSpaceSize.value)()

    ntstatus = RtlCompressBuffer(
        USHORT(calgo),  # CompressionFormatAndEngine,
        ctypes.byref(ntUnCompressed),  # Uncompressed Buffer
        ULONG(uncompressed_size),  # Uncompressed Buffer Size
        ctypes.byref(ntCompressed),  # Compressed Buffer
        ULONG(uncompressed_size),  # Compressed Buffer Size
        ULONG(chunk_size),  # Uncompressed Chunk Size
        ctypes.byref(ntFinalCompressedSize),  # Final Compressed Size
        ctypes.byref(ntWorkspace)  # Work Space from RtlGetCompressionWorkSpaceSize
    )
    if ntstatus:
        raise ValueError(f'Cannot Compress Buffer, err: '
                         f'{tohex(ntstatus, 32)}:{ErrorCodes(tohex(ntstatus, 32)).name}')

    compressed = bytearray(ntCompressed)[:ntFinalCompressedSize.value]

    return algo, compressed

def header(algo, uncompressed, crc):
    if algo is 4:
        sig = 0x44d414d
        import binascii, struct
        # crc = binascii.crc32(compressed)
        header = struct.pack('<LL',sig,len(uncompressed))

        return header

        
import struct
import enum
import datetime


class WinVer(enum.Enum):
    XP_2003 = 17
    Vista_7 = 23
    Win8_1 = 26
    Win10 = 30


def ssca_2008_hash_function(filename):
    hash_value = 314159
    filename_index = 0
    filename_length = len(filename)

    while filename_index + 8 < filename_length:
        character_value = ord(filename[filename_index + 1]) * 37
        character_value += ord(filename[filename_index + 2])
        character_value *= 37
        character_value += ord(filename[filename_index + 3])
        character_value *= 37
        character_value += ord(filename[filename_index + 4])
        character_value *= 37
        character_value += ord(filename[filename_index + 5])
        character_value *= 37
        character_value += ord(filename[filename_index + 6])
        character_value *= 37
        character_value += ord(filename[filename_index]) * 442596621
        character_value += ord(filename[filename_index + 7])

        hash_value = ((character_value - (hash_value * 803794207)) % 0x100000000)

        filename_index += 8

    while filename_index < filename_length:
        hash_value = (((37 * hash_value) + ord(filename[filename_index])) % 0x100000000)

        filename_index += 1

    return hash_value


def build_header(unknown0, fileSize, executableName, hash, unknown1, version: enum = WinVer.Win10):
    signature = 'SCCA'
    # Parse the file header
    # 84 bytes
    version = struct.pack('I',version.value)
    signature = signature.encode()
    unknown0 = struct.pack('I',17) # 15 or 17
    fileSize = struct.pack('I',fileSize)
    executableName = struct.pack('60s', executableName.encode('utf-16-le'))
    # TODO: Calculate HASH
    # rawhash = hex(struct.unpack_from("I", infile.read(4))[0])
    # hash = rawhash.lstrip("0x")

    unknown1 = struct.pack('I', 0)

    header = version + signature + unknown0 + fileSize + executableName + rawhash + unknown1

    return header


def BuildfileInformation30(metricsCount, traceChainsOffset, traceChainsCount, filenameStringsOffset,
                           filenameStringsSize, volumesInformationOffset, volumesCount, volumesInformationSize,
                           unknown0, lastRunTime):
    # File Information
    # 224 bytes
    metricsOffset = 304
    metricsOffset = struct.pack('I', metricsOffset)
    metricsCount = struct.pack('I', metricsCount)
    traceChainsOffset = struct.pack('I', traceChainsOffset)
    traceChainsCount = struct.pack('I', traceChainsCount)
    filenameStringsOffset = struct.pack('I', filenameStringsOffset)
    filenameStringsSize = struct.pack('I', filenameStringsSize)
    volumesInformationOffset = struct.pack('I', volumesInformationOffset)
    volumesCount = struct.pack('I', volumesCount)
    volumesInformationSize = struct.pack('I', volumesInformationSize)
    unknown0 = struct.pack('II', 19, 1)  # Empty values
    runCount = len(lastRunTime)
    tmp = b''
    for i in lastRunTime:
        delta = datetime.datetime.fromtimestamp(i) - datetime.datetime(1601, 1, 1)
        tmp += struct.pack('Q', delta)
    tmp += struct.pack('Q', 0)*(8 - runCount)
    lastRunTime = tmp
    unknown1 = struct.pack('Q', 0) * 2
    runCount = struct.pack('I', runCount)
    unknown2 = struct.pack('I', 1)  # 1, 2, 7
    unknown3 = struct.pack('I', 0)  # 0, 3
    unknown4 = struct.pack('I', 0) * 22

    return metricsOffset + metricsCount + traceChainsOffset + traceChainsCount + filenameStringsOffset\
        + filenameStringsSize + volumesInformationOffset + volumesCount + volumesInformationSize + unknown0\
        + lastRunTime + unknown1 + runCount + unknown2 + unknown3 + unknown4


def BuildmetricsArray30(unknown0, unknown1, unknown2, filenameOffset, filenameLength, unknown3, mftRecordNumber,
                   mftSeqNumber):
    # File Metrics Array
    # 32 bytes per array, not parsed in this script
    # infile.seek(self.metricsOffset)
    unknown0 = struct.pack('I', unknown0)
    unknown1 = struct.pack('I', unknown1)
    unknown2 = struct.pack('I', unknown2)
    filenameOffset = struct.pack('I', filenameOffset)
    filenameLength = struct.pack('I', filenameLength)
    unknown3 = struct.pack('I', unknown3)
    mftRecordNumber = mftRecordNumber
    mftSeqNumber = struct.pack('H', mftSeqNumber)

    return unknown0 + unknown1 + unknown2 + filenameOffset + filenameLength + unknown3 + mftRecordNumber + mftSeqNumber


def traceChainsArray30(total_block, uknown0, uknown1, uknown2):
    # Trace Chains Array
    # Read though, not being parsed for information
    # 8 bytes
    trace_chane = struct.pack('IBBH', total_block, uknown0, uknown1, uknown2)
    return trace_chane

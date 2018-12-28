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


def build_header(unknown0, file_size, executable_name, hash, unknown1, version: enum = WinVer.Win10):
    signature = 'SCCA'
    # Parse the file header
    # 84 bytes
    version = struct.pack('I', version.value)
    signature = signature.encode()
    unknown0 = struct.pack('I', 17)  # 15 or 17
    file_size = struct.pack('I', file_size)
    executable_name = struct.pack('60s', executable_name.encode('utf-16-le'))
    # TODO: Calculate HASH
    raw_hash = struct.pack('I', 1)
    # raw_hash = hex(struct.pack('I', infile.read(4))[0])
    # hash = raw_hash.lstrip('0x')

    unknown1 = struct.pack('I', 0)

    header = version + signature + unknown0 + file_size + executable_name + raw_hash + unknown1

    return header


def build_file_information_30(metrics_count, trace_chains_offset, trace_chains_count, filename_strings_offset,
                              filename_strings_size, volumes_information_offset, volumes_count,
                              volumes_information_size, unknown0, last_run_time):
    # File Information
    # 224 bytes
    metrics_offset = 304
    metrics_offset = struct.pack('I', metrics_offset)
    metrics_count = struct.pack('I', metrics_count)
    trace_chains_offset = struct.pack('I', trace_chains_offset)
    trace_chains_count = struct.pack('I', trace_chains_count)
    filename_strings_offset = struct.pack('I', filename_strings_offset)
    filename_strings_size = struct.pack('I', filename_strings_size)
    volumes_information_offset = struct.pack('I', volumes_information_offset)
    volumes_count = struct.pack('I', volumes_count)
    volumes_information_size = struct.pack('I', volumes_information_size)
    unknown0 = struct.pack('II', 19, 1)  # Empty values
    run_count = len(last_run_time)
    tmp = b''
    for i in last_run_time:
        delta = datetime.datetime.fromtimestamp(i) - datetime.datetime(1601, 1, 1)
        tmp += struct.pack('Q', delta)
    tmp += struct.pack('Q', 0) * (8 - run_count)
    last_run_time = tmp
    unknown1 = struct.pack('Q', 0) * 2
    run_count = struct.pack('I', run_count)
    unknown2 = struct.pack('I', 1)  # 1, 2, 7
    unknown3 = struct.pack('I', 0)  # 0, 3
    unknown4 = struct.pack('I', 0) * 22

    return metrics_offset + metrics_count + trace_chains_offset + trace_chains_count + filename_strings_offset \
        + filename_strings_size + volumes_information_offset + volumes_count + volumes_information_size + unknown0 \
        + last_run_time + unknown1 + run_count + unknown2 + unknown3 + unknown4


def build_metrics_array30(unknown0, unknown1, unknown2, filename_offset, filename_length, unknown3, mft_record_number,
                          mft_seq_number):
    # File Metrics Array
    # 32 bytes per array, not parsed in this script
    # infile.seek(metricsOffset)
    unknown0 = struct.pack('I', unknown0)
    unknown1 = struct.pack('I', unknown1)
    unknown2 = struct.pack('I', unknown2)
    filename_offset = struct.pack('I', filename_offset)
    filename_length = struct.pack('I', filename_length)
    unknown3 = struct.pack('I', unknown3)
    mft_record_number = mft_record_number
    mft_seq_number = struct.pack('H', mft_seq_number)

    return unknown0 + unknown1 + unknown2 + filename_offset + filename_length + unknown3 + mft_record_number \
        + mft_seq_number


def build_trace_chains_array30(total_block, unknown0, unknown1, unknown2):
    # Trace Chains Array
    # Read though, not being parsed for information
    # 8 bytes
    trace_chane = struct.pack('IBBH', total_block, unknown0, unknown1, unknown2)
    return trace_chane


def build_filename_strings(filename_strings: list):
    tmp = b''
    for i in filename_strings:
        tmp += i.encode('utf-16-le')
    
    return tmp


def build_volume_information_30(volumes_count,
                                vol_path_offset, vol_path_length, vol_creation_time, vol_serial_number,
                                file_ref_offset, file_ref_count, dir_strings_offset, dir_strings_count,
                                unknown0, unknown1, unknown2, unknown3, unknown4):
    # Volumes Information
    # 96 bytes

    # infile.seek(volumesInformationOffset)

    volumesInformationArray = []
    directoryStringsArray = []

    count = 0
    while count < volumes_count:

        vol_path_offset = struct.pack('I', vol_path_offset)
        vol_path_length = struct.pack('I', vol_path_length)
        vol_creation_time = struct.pack('Q', vol_creation_time)
        vol_serial_number = int(f'0x{vol_serial_number}', 16)
        vol_serial_number = struct.pack('I', vol_serial_number)
        file_ref_offset = struct.pack('I', file_ref_offset)
        file_ref_count = struct.pack('I', file_ref_count)
        dir_strings_offset = struct.pack('I', dir_strings_offset)
        dir_strings_count = struct.pack('I', dir_strings_count)
        unknown0 = struct.pack('I', unknown0)
        unknown1 = struct.pack('6I', unknown1)
        unknown2 = dir_strings_count
        unknown2 = struct.pack('I', unknown2)
        unknown3 = struct.pack('6I', unknown3)
        unknown4 = struct.pack('I', unknown4)



        directoryStringsArray.append(directoryStrings(infile))

        infile.seek(volumesInformationOffset + vol_path_offset)
        volume = {}
        volume['Volume Name'] = infile.read(vol_path_length * 2).replace('\x00'.encode(), ''.encode())
        volume['Creation Date'] = convertTimestamp(vol_creation_time)
        volume['Serial Number'] = vol_serial_number
        volumesInformationArray.append(volume)

        count += 1
        infile.seek(volumesInformationOffset + (96 * count))
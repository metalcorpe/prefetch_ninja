
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

# asd = [
#     '\VOLUME{01d43a7d47c65e36-a848b071}\PROGRAM FILES\\7-ZIP\\7ZFM.EXE'.upper(), #.encode('utf-16-le'),
#     '\HARDDISKVOLUME1\PROGRAM FILES\\7-ZIP\\7ZFM.EXE'.upper(), #.encode('utf-16-le'),
#     'C:\PROGRAM FILES\\7-ZIP\\7ZFM.EXE'.upper(), #.encode('utf-16-le'),
#     '\DEVICE\HARDDISKVOLUME1\PROGRAM FILES\\7-ZIP\\7ZFM.EXE'.upper(), #.encode('utf-16-le'),
#
#     '\VOLUME{01d43a7d47c65e36-a848b071}\PROGRAM FILES\\7-ZIP\\7ZFM.EXE'.upper().encode('utf-16-le').decode(),
#     '\HARDDISKVOLUME1\PROGRAM FILES\\7-ZIP\\7ZFM.EXE'.upper().encode('utf-16-le').decode(),
#     'C:\PROGRAM FILES\\7-ZIP\\7ZFM.EXE'.upper().encode('utf-16-le').decode(),
#     '\DEVICE\HARDDISKVOLUME1\PROGRAM FILES\\7-ZIP\\7ZFM.EXE'.upper().encode('utf-16-le').decode(),
#
#     '\\VOLUME{01d43a7d47c65e36-a848b071}\\PROGRAM FILES\\7-ZIP\\7ZFM.EXE',
#     '\\VOLUME{01d43a7d47c65e36-a848b071}\\PROGRAM FILES\\7-ZIP\\7ZFM.EXE'.upper(),
#     '\\VOLUME{01d43a7d47c65e36-a848b071}\\PROGRAM FILES\\7-ZIP\\7ZFM.EXE'.encode('utf-16-le').__str__(),
#     '\\VOLUME{01d43a7d47c65e36-a848b071}\\PROGRAM FILES\\7-ZIP\\7ZFM.EXE'.upper().encode('utf-16-le').__str__(),
#     '\HARDDISKVOLUME2\PROGRAM FILES\\7-ZIP\\7ZFM.EXE'.upper(),  # .encode('utf-16-le'),
#     '\DEVICE\HARDDISKVOLUME2\PROGRAM FILES\\7-ZIP\\7ZFM.EXE'.upper(),  # .encode('utf-16-le'),
#     '\HARDDISKVOLUME2\PROGRAM FILES\\7-ZIP\\7ZFM.EXE'.upper().encode('utf-16-le').decode(),
#
#     '\DEVICE\HARDDISKVOLUME2\PROGRAM FILES\\7-ZIP\\7ZFM.EXE'.upper().encode('utf-16-le').decode(),
#
# ]
#
# for i in asd:
#     tmp = hex(ssca_2008_hash_function(i))
#     print(f' {True if tmp[2:].upper() == "69B8961D" else False} {tmp:<10} {i} ')
# # ssca_2008_hash_function()

import os
file = 'C:\Program Files\\7-Zip\\7zFM.exe'
_, file = os.path.splitdrive(file)
volume_id = 2
file_for_hash = f'\DEVICE\HARDDISKVOLUME{volume_id}{file}'.upper().encode('utf-16-le').decode()
raw_hash = ssca_2008_hash_function(file_for_hash)
print(f'{True if hex(raw_hash)[2:].upper() == "69B8961D" else False} {hex(raw_hash)}')

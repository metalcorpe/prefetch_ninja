import prefetch
import tempfile
import builder
import comp

d = prefetch.DecompressWin10()
# infile = 'C:\Windows\Prefetch\\7ZFM.EXE-69B8961D.pf'
# infile = 'C:\\Users\\v.vouvoutsis\OneDrive\dis\Windows-Prefetch-Parser\TestFiles\Win10\CALC.EXE-3FBEF7FD.pf'
infile = 'CALC.EXE-3FBEF7FD.pf'

f0 = open(infile, 'rb')
if f0.read(3) == b'MAM':
    f0.close()
else:
    raise FutureWarning
asd = prefetch.Prefetch(infile)
decompressed = d.decompress(infile)
t = tempfile.mkstemp()
f = open(t[1], "wb+")
f.write(decompressed)
f.seek(0)

# tmp = asd.resources
# tmp[19] = tmp[19][0:-6] + b'66' + tmp[19][-4:]
# print(tmp[19])
# a = builder.build_filename_strings(tmp)

# print(asd.filenameStringsSize, len(a))
# print(asd.filenames)
print(decompressed[84:84+224])

ttt = builder.build_file_information_30(asd.metricsCount,asd.traceChainsOffset,asd.traceChainsCount,
                                        asd.filenameStringsOffset,asd.filenameStringsSize,asd.volumesInformationOffset,
                                        asd.volumesCount,asd.volumesInformationSize,0,asd.timestamps)

print(bytearray(ttt))
print(len(decompressed[84:84+224]),'-',len(bytearray(ttt)))

# # a = decompressed[0:asd.filenameStringsOffset] + decompressed[asd.filenameStringsOffset:asd.filenameStringsOffset + asd.filenameStringsSize] + decompressed[asd.filenameStringsSize:]
# a = decompressed[0:asd.filenameStringsOffset] + a + decompressed[asd.filenameStringsOffset + asd.filenameStringsSize:]
#
# we = comp.compress(comp.CompAlgo.COMPRESSION_FORMAT_XPRESS_HUFF, a)
#
# head = comp.header(4, a)
#
# wer = head + we[1]
#
# f0 = open(infile, 'wb')
# f0.write(wer)

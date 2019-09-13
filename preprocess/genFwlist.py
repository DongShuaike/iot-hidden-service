import os

rootPath = '/home/dsk/Documents/Experiments/firmware'
vendors = ['netgear', 'DLink', 'tplink']

filePath = '/home/dsk/PycharmProjects/iot-hidden-service/res/'
fileList = []
with open(os.path.join(filePath, 'fileList'),'w') as fp:
    for vd in vendors:
        vendorPath = os.path.join(rootPath, vd)
        for f in os.listdir(vendorPath):
            fPath = os.path.join(vendorPath, f)
            if not os.path.isdir(fPath):
                fileList.append(fPath)
    for f in fileList:
        fp.write(f+'\n')


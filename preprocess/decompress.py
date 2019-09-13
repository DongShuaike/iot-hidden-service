import os
import magic
import zipfile, tarfile, rarfile
import gzip
import re
import results

def zipOp(filePath):
    """
    Only *.bin files will be extracted
    :param filePath: The path to a zip file
    :return: an integer indicating whether the extraction is success
    """
    try:
        zip = zipfile.ZipFile(filePath)
    except Exception:
        print(filePath, 'not a valid zip file')
        return -1
    outputPath = filePath[:-4]
    if os.path.exists(outputPath):
        print('output path exists, stop.')
        return -1
    else:
        os.makedirs(outputPath)
    try:
        zip.extractall(path=outputPath)
    except Exception:
        print('zip extraction failed')
        return -1
    """for info in fp.filelist:
        binfile = re.findall(r".*\.bin", info.filename)
        if len(binfile)>0:
            binname = binfile[0]
            bindata = fp.read(binname)
    outputPath = filePath.split(".")[0]
    try:
        os.makedirs(outputPath)
    except Exception:
        print('Dir existed, calcel mkdir')
        return -1
    with open(os.path.join(outputPath, binname), 'wb') as p:
        try:
            p.write(bindata)
            print(binname,'has been read and saved')
            return 0
        except Exception:
            print('writing', binname, 'wrong')
            return -1
    """

def gzipOp(filePath):
    outputPath = filePath[:-3]#name before ".gz"
    if os.path.exists(outputPath):
        print('output path exists, stop.')
        return -1
    try:
        with gzip.open(filePath, 'rb') as f:
            data = f.read()
    except Exception:
        print(filePath, 'not a valid gzip file')
        return -1
    with open(outputPath,'wb') as f:
        f.write(data)

def tarOp(filePath):
    try:
        tar = tarfile.open(filePath)
    except Exception:
        print(filePath, 'not a valid tar file')
        return -1
    outputPath = filePath[:-4]#name before ".tar"
    if os.path.exists(outputPath):
        print('output path exists, stop.')
        return -1
    else:
        os.makedirs(outputPath)
    try:
        tar.extractall(path=outputPath)
    except Exception:
        print('something wrong in extracting all files from tar')

def rarOp(filePath):
    try:
        rar = rarfile.RarFile(filePath)
    except Exception:
        print(filePath, 'not a valid rar file')
        return -1
    outputPath = filePath[:-4]#name before ".rar"
    if os.path.exists(outputPath):
        print('output path exists, stop.')
        return -1
    else:
        os.makedirs(outputPath)
    try:
        rar.extractall(path=outputPath)
    except Exception:
        print('something wrong in extracting all files from rar')

def decompress(m, filePath):
    id = m.id_filename(filePath)
    if id == 'application/gzip':
        gzipOp(filePath)
    elif id == 'application/x-tar':
        tarOp(filePath)
    elif id == 'application/zip':
        zipOp(filePath)
    elif id == 'application/x-rar':
        rarOp(filePath)

if __name__ == "__main__":
    cfg = results.Config()
    fileListPath = cfg.fileListPath
    m = magic.Magic(flags=magic.MAGIC_MIME_TYPE)

    with open(fileListPath, 'r') as fp:
        for line in fp.readlines():
            fPath = line.strip()
            decompress(m, fPath)



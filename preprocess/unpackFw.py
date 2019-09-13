import binwalk
import os
import config
from .decompress import decompress
import magic

UNIX_DIRS = ["bin", "etc", "dev", "home", "lib", "mnt", "opt", "root",
                 "run", "sbin", "tmp", "usr", "var"]
UNIX_THRESHOLD = 4

def io_find_rootfs(start, recurse=True):
    path = start
    while (len(os.listdir(path)) == 1 and
           os.path.isdir(os.path.join(path, os.listdir(path)[0]))):
        path = os.path.join(path, os.listdir(path)[0])
    count = 0
    for subdir in os.listdir(path):
        if subdir in UNIX_DIRS and \
            os.path.isdir(os.path.join(path, subdir)):
            count += 1
    if count >= UNIX_THRESHOLD:
        return (True, path)

    if recurse:
        for subdir in os.listdir(path):
            if os.path.isdir(os.path.join(path, subdir)):
                res = io_find_rootfs(os.path.join(path, subdir),
                                     False)
                if res[0]:
                    return res
    return (False, start)

if __name__ == "__main__":
    rootPath = '/home/dsk/Documents/Experiments/firmware'
    vendors = ['DLink', 'tplink', 'netgear']
    m = magic.Magic(flags=magic.MAGIC_MIME_TYPE)
    """
    For some recursive zip files like zip[zip,], do decompress again
    """
    """for vendor in vendors:
        vendorPath = os.path.join(rootPath, vendor)
        for dirName, subdirList, fileList in os.walk(vendorPath):
            for f in fileList:
                fPath = os.path.join(dirName, f)
                decompress(m, fPath)
    print('decompressing recursively finished')
    """

    unixList = []
    for vendor in vendors:
        vendorPath = os.path.join(rootPath, vendor)
        for dirName, subdirList, fileList in os.walk(vendorPath):
            # bypass those with ".extracted" in its name
            if ".extracted" in dirName:
                continue
            for f in fileList:
                if f[-4:] == '.bin' or f[-4:] == '.img':
                    fPath = os.path.join(dirName, f)
                    # binwalk it
                    print(dirName)
                    folderName = '/'.join(fPath.split('/')[:-1])+'/_'+f+'.extracted'
                    print(folderName)
                    if os.path.exists(folderName):
                        #os.system('rm -rf "'+folderName+'"')
                        continue

                    else:
                        binwalk.scan(fPath, '-e', '-y', 'filesystem', '-C', dirName, signature=True, quiet=True)
                        #for module in binwalk.scan(fPath, '-e', '-y', 'filesystem', '-C', dirName,
                        #                          signature=True, quiet=True):

    for vendor in vendors:
        vendorPath = os.path.join(rootPath, vendor)
        for dirName, subdirList, fileList in os.walk(vendorPath):
            for subdir in subdirList:
                subdirPath = os.path.join(dirName, subdir)
                try:
                    unix = io_find_rootfs(subdirPath)
                    if unix[0]:
                        unixList.append(unix[1])
                except PermissionError:
                    print('permission error, emitted')

    cfg = config.Config()
    with open(cfg.unixListPath,'w') as fp:
        for unix in unixList:
            fp.write(unix+'\n')







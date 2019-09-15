import os
from config import Config
import magic
import json

def searchWebFiles(m, dirPath):
    print('searching in', dirPath)
    htmls = {}
    phps = {}
    jss = {}
    asps = {}
    cgis = {}
    for dirName, subdirs, files in os.walk(dirPath):
        for f in files:
            fPath = os.path.join(dirName, f)
            if m.id_filename(fPath) == 'text/html':
                if dirName in htmls:
                    htmls[dirName].append(f)
                else:
                    htmls[dirName] = [f]
            elif m.id_filename(fPath) == 'text/x-php':
                if dirName in phps:
                    phps[dirName].append(f)
                else:
                    phps[dirName] = [f]
            elif f[-3:] == '.js':
                if dirName in jss:
                    jss[dirName].append(f)
                else:
                    jss[dirName] = [f]
            elif f[-4:] == '.asp':
                if dirName in asps:
                    asps[dirName].append(f)
                else:
                    asps[dirName] = [f]
            #elif m.id_filename(fPath) == 'application/x-executable': --> too many false positives
            elif f[-4:] == '.cgi' or f[-5:] == '.fcgi':
                if dirName in cgis:
                    cgis[dirName].append(f)
                else:
                    cgis[dirName] = [f]
    mapper = {'html':htmls, 'php':phps, 'js':jss, 'asp':asps, 'cgi':cgis}
    return (dirPath, mapper)

if __name__ == "__main__":
    cfg = Config()
    rootPath = cfg.rootPath
    vendors = cfg.vendors
    unixListPath = cfg.unixListPath
    webContentsPath = cfg.webContentsPath
    m = magic.Magic(flags=magic.MAGIC_MIME_TYPE)
    webcontents = {}
    with open(unixListPath, 'r') as fp:
        for line in fp.readlines():
            dirPath = line.strip()
            webs = searchWebFiles(m, dirPath)
            webcontents[webs[0]] = webs[1]
    with open(webContentsPath, 'w') as fp:
        fp.write(json.dumps(webcontents))
        print('web contents have been stored.')


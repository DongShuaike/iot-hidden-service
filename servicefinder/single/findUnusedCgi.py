import os, re, json

def findCgis(rootPath):
    cgis = {}
    for dirName, subdirs, files in os.walk(rootPath):
        for f in files:
            if f[-4:] == '.cgi':
                fPath = os.path.join(dirName, f)
                cgis[f] = fPath
    return cgis

def findunUsedCgis(rootPath, cgis):
    pattern = re.compile('([^/\'\"=]*\.cgi).*[\'\"&]')
    used = []
    for dirName, subdirs, files in os.walk(rootPath):
        for f in files:
            if f[-4:] in ['.php','.asp', '.htm'] or f[-5:] == '.html' or f[-3:] == '.js':
                fPath = os.path.join(dirName, f)
                try:
                    data = open(fPath,'r').read().strip()
                    used.extend(re.findall(pattern, data))
                except Exception:
                    print('something error...')
    unused = []
    for k in cgis:
        if not k in used:
            unused.append(cgis[k])
    return unused

if __name__ == '__main__':
    rootPath = '/home/dsk/Documents/Experiments/firmware/netgear/N300-v1.1.0.54_1.0.1/_N300-V1.1.0.54_1.0.1.img.extracted/_N300.bin.extracted/squashfs-root/'
    cgis = findCgis(rootPath)
    unused = findunUsedCgis(rootPath, cgis)
    with open('./results/singleFile/'+rootPath.replace('/','_'),'w') as fp:
        fp.write(json.dumps(unused))
    print(rootPath,' done ')



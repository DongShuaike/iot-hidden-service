import os, json
from config import Config
import re

types = ['html', 'js', 'php', 'asp']
global_pattern = re.compile('([^/\'\"=]*\.cgi).*[\'\"&]')

"""
The form of webContents is like:
{
'dirPath':
    {'html':
        {
        '/a/b/c':
        [
            'a.html','b.html',...
        ],
        'c/d/e':
        [
            'c.html'
        ],
        },
     'js':
        {
        '/a/b/c':[]
        },
    },
}
"""
def getWeb2Cgi(webContents, dirPath):
    print('dirPath', dirPath)
    mapping = {'html':{}, 'js':{}, 'php':{}, 'asp':{}}
    """
    The form of mapping is like:
    {
        'html':
        {
            '/a/b/c':
            {
                'a.html':[cgi1, cgi2]
                'b.html':[]
            }
        }
    }
    """
    def naiveSearch(data, patterns): #r'"([^"]*\.cgi).*"'
        occurs = []
        for pattern in patterns:
            occurs.extend(re.findall(pattern, data))
            #TODO: deal with <action="/cgi-bin/luci">, no extension name
            #TODO: deal with <form action=/apply.cgi
            #TODO: deal with <action="/cgi-bin/cgi_system.cgi">
        return occurs

    for tp in types:
        for k in webContents[dirPath][tp]:
            if not k in mapping[tp]:
                mapping[tp][k]={}
            for f in webContents[dirPath][tp][k]:
                fPath = os.path.join(k,f)
                try:
                    data = open(fPath,'r').read().strip()
                    #occurs = naiveSearch(data, [r'"([^/"]*\.cgi).*"', r'<action="(.*)"\s',
                    #                            r'<form action=(.*\.cgi)', r'/([^/"]*\.cgi).*"'])
                    occurs = naiveSearch(data, [global_pattern])
                    mapping[tp][k][f] = occurs
                except Exception:
                    mapping[tp][k][f] = []

    return mapping

def filterUnusedCgi(webContents, mappings, dirPath):
    def findUnused(targets, cgis):
        unused = []
        for k in cgis:
            for f in cgis[k]:
                if f not in targets:
                    unused.append(f)
        return unused
    """
    The form of webContents is like:
    {
    'dirPath':
        {'html':
            {
            '/a/b/c':
            [
                'a.html','b.html',...
            ],
            'c/d/e':
            [
                'c.html'
            ],
            },
        },
    }
    """
    """
    The form of mappings is like:
    {
        dirPath:
        {
            'html':
            {
                '/a/b/c':
                {
                    'a.html':[cgi1, cgi2]
                    'b.html':[]
                }
            }
        }
    }
    """
    """
    The form of unusedCgis is
    {
        '/a/b/c':[cgi1, cgi2],
        '/d/e':[cgi3]
    }
    """
    cgis = webContents[dirPath]['cgi']
    lst = []
    for tp in types:
        for k in mappings[dirPath][tp]:
            for l in mappings[dirPath][tp][k]:
                lst.extend(mappings[dirPath][tp][k][l])
    if dirPath == "/home/dsk/Documents/Experiments/firmware/DLink/DAP-1562__1150__Firmware (1.00)/dap1562_FW_100/_dap1562_FW_100.bin.extracted/squashfs-root":
        print('lst', lst)
    unused = findUnused(lst, cgis)
    return unused

if __name__ == "__main__":
    mappings = {}
    cfg = Config()
    webContentsPath = cfg.webContentsPath
    webContents = json.loads(open(webContentsPath,'r').readline().strip())
    for rootPath in webContents:
        mapping = getWeb2Cgi(webContents, rootPath)
        mappings[rootPath] = mapping
    with open(cfg.web2cgiPath,'w') as fp:
        fp.write(json.dumps(mappings))

    unusedCgis = {}
    markeds = {}
    for rootPath in webContents:
        unused = filterUnusedCgi(webContents, mappings, rootPath)
        unusedCgis[rootPath] = unused
    with open(cfg.unusedCgisPath, 'w') as fp:
        fp.write(json.dumps(unusedCgis))


import os, json
from config import Config
import re

types = ['html', 'js', 'php', 'asp']
"""
The form of webContents is like:
{
'dirPath':
    {'html':
        {
        '/a/b/c':['a.html','b.html',...],
            'c/d/e':['c.html'],
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
        return occurs

    for tp in types:
        for k in webContents[dirPath][tp]:
            if not k in mapping[tp]:
                mapping[tp][k]={}
            for f in webContents[dirPath][tp][k]:
                fPath = os.path.join(k,f)
                try:
                    data = open(fPath,'r').read().strip()
                    occurs = naiveSearch(data, [r'"([^"]*\.cgi).*"', r'<action="(.*)"\s', r'<form action=(.*\.cgi)'])
                    mapping[tp][k][f] = occurs
                except Exception:
                    mapping[tp][k][f] = []

    return mapping

def filterUnusedCgi(webContents, mappings, dirPath):
    unusedCgis = {}
    """
    The form of unusedCgis is
    {
        '/a/b/c':[cgi1, cgi2],
        '/d/e':[cgi3]
    }
    """
    marked_kf = {}
    for tp in types:
        for k in mappings[dirPath][tp]:
            for l in mappings[dirPath][tp][k]:
                for f in mappings[dirPath][tp][k][l]:
                    for k1 in webContents[dirPath]['cgi']:
                        for f1 in webContents[dirPath]['cgi'][k1]:
                            if f1 == f:
                                if not k1 in marked_kf:
                                    marked_kf[k1] = [f1]
                                else:
                                    marked_kf[k1].append(f1)

    for k in webContents[dirPath]['cgi']:
        unusedCgis[k] = []
        if not k in marked_kf:
            unusedCgis[k] = webContents[dirPath]['cgi'][k]
        else:
            for f in webContents[dirPath]['cgi'][k]:
                if not f in marked_kf[k]:
                    unusedCgis[k].append(f)
    return marked_kf, unusedCgis


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
        marked, unused = filterUnusedCgi(webContents, mappings, rootPath)
        markeds[rootPath] = marked
        unusedCgis[rootPath] = unused
    with open('/home/dsk/PycharmProjects/iot-hidden-service/results/marked','w') as fp:
        fp.write(json.dumps(markeds))
    with open(cfg.unusedCgisPath, 'w') as fp:
        fp.write(json.dumps(unusedCgis))


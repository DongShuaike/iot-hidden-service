class Config:
    def __init__(self):
        self.workPath = '/home/dsk/PycharmProjects/iot-hidden-service'
        self.resultPath = self.workPath+'/results'
        self.rootPath = '/home/dsk/Documents/Experiments/firmware'
        self.fileListPath = self.resultPath+'/fileList' #filePath recording all downloaded files
        self.unixListPath = self.resultPath+'/unixList'
        self.webContentsPath = self.resultPath+'/webContents' # store all web-related file mappings
        self.web2cgiPath = self.resultPath+'/web2cgi'
        self.unusedCgisPath = self.resultPath+'/unusedCgis'
        self.vendors = ['DLink', 'netgear', 'tplink']
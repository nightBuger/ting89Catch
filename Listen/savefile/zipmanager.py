from Listen.savefile.fileclassify import FileSection
import sys
import zipfile
import os
import zipfile


class ZipManager():
    __manager__ = {}
    __outputfilepath__ = './'
    __prefix__ = ""
    
    def __init__(self,outputfilepath=None,prefix=None,sectionsize=100):
        self.__prefix__ = "未命名" if prefix == None else prefix
        self.__outputfilepath__ = "." if outputfilepath == None else outputfilepath
        self.sectionObject = FileSection(sectionsize) 
    def __getManager__(self):
        return self.__manager__
    
    def __str__(self) -> str:
        return str(self.__getManager__())

    def AddFile(self,filename):
        basename = os.path.basename(filename)
        section = self.sectionObject.get_file_section_by_name(basename)['low-hi']
        if section not in self.__getManager__() :
            self.__getManager__()[section] = []
        self.__getManager__()[section].append(filename)

    def AddDir(self,dirname):
        for filename in os.listdir(dirname):
            self.AddFile(os.path.join(dirname,filename))
    
    def ZipAll(self):
        d = self.__getManager__()
        for key in d:
            with zipfile.ZipFile(os.path.join(self.__outputfilepath__,self.__prefix__ + "_" + key+".zip"), 'w') as zip:
                for file in d[key]:
                    zip.write(file,arcname=os.path.basename(file))


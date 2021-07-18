from fileclassify import FileSection
import sys
import zipfile
import os


class ZipManager():
    __manager__ = {}
    sectionObject = FileSection(100)
    __outputfilepath__ = './'
    def __getManager__(self):
        return self.__manager__
    
    def __str__(self) -> str:
        return str(self.__getManager__())

    def AddFile(self,filename):
        section = self.sectionObject.get_file_section_by_name(filename)['low-hi']
        if section not in self.__getManager__() :
            self.__getManager__()[section] = []
        self.__getManager__()[section].append(filename)

zipmanager = ZipManager()


filelist = os.listdir('E:\Scrapy\Listen\本次下载的小说的名字')
for filename in filelist:
    zipmanager.AddFile(filename)

print(zipmanager)
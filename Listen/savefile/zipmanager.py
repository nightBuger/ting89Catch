
import zipfile

class ZipManager():
    __manager__ = {}
    sectionObject = None
    __outputfilepath__ = './'
    def __getManager__(self):
        return self.__manager__
    
    def __str__(self) -> str:
        return str(self.__getManager__)

    def AddFile(self,filename):
        section = self.sectionObject.get_file_section_by_name(filename)
        if section not in self.__getManager__() :
            self.__getManager__()[section] = []
        self.__getManager__()[section].append(filename)

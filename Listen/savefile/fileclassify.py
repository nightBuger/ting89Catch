import re

class FileSection:
    def __init__(self,size:int):
        self.section_size = size
    def get_file_section_by_name(self,filename:str):
        filename = filename.split('.')[0]
        s = re.search('(\d+)',filename)
        if s:
            index = s.group(0)
            return self.get_file_section_by_index(int(index),len(index) if len(str(self.section_size)) < len(index) else len(str(self.section_size)))
        else :
            print(f'wrong filename :<{filename}>, exit App')
            exit(1)

    def get_file_section_by_index(self,fileindex:int,size:int):
        fileindex -= 1
        low = fileindex//self.section_size * self.section_size + 1
        hi = low + self.section_size -1
        format_string = '{:0>' + str(size) + 'd}'
        low = format_string.format(low)
        hi = format_string.format(hi)
        return {'low': low,'hi':hi,'low-hi':f'{low}-{hi}'}

'''# size = 5
# s = '{:0>' + str(size) + 'd}'
# s = s.format(32)
# print(s)

f = FileSection(1000000)

print(f.get_file_section_by_name('100'))

'''
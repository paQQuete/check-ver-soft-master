import json
import os
import codecs

from . import sensdata

'''
all sensitive data in sensdata.py
'''


DIR = sensdata.DIR




class DataSoup():
    def __init__(self, directory):
        self._filesList = self._parseFiles(directory)
        self._parseDataFromFile()
        pass

    def _parseFiles(self, dir: str) -> list:
        return os.listdir(dir)


    def _parseDataFromFile(self) -> dict:
        flist = self._filesList
        for each in flist:
            with codecs.open(each, mode='r', encoding='utf-8-sig') as f:
                file = f.read()
                file = file.replace('\r', '').replace('\n', '')
                data = json.loads(file)
                pass

    def makeCollection(self):
        pass






if __name__ == '__main__':
    A = DataSoup(DIR)


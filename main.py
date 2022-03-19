import json
import os
import codecs
from datetime import datetime
import sensdata

'''
all sensitive data in sensdata.py
'''

DIR = sensdata.DIR


class GetDataFiles():

    @staticmethod
    def getFromDirectory(dir) -> list:
        os.chdir(dir)
        return os.listdir(dir)


class DataSoup():

    @staticmethod
    def parseDataFromFile(flist) -> list[dict]:
        outlist = list()

        for each in flist:
            outdict = dict()
            hostname = each[:each.rindex('-')]
            unixtime = int(each[each.rindex('-') + 1:each.rindex(',')])
            ntime = datetime.fromtimestamp(unixtime)

            # Serialize datetime here!
            ntime = ntime.strftime('%Y-%m-%d %H:%M:%S')

            outdict.update({'hostname': hostname, 'unixtime': unixtime, 'normal time': ntime})
            with codecs.open(each, mode='r', encoding='utf-8-sig') as f:
                file = f.read()
                file = file.replace('\r', '').replace('\n', '')
                data = json.loads(file)
                outdict.update({'data': data})
                outlist.append(outdict)

        return outlist




if __name__ == '__main__':
    fileslist = GetDataFiles.getFromDirectory(DIR)
    A = DataSoup.parseDataFromFile(fileslist)

    with open('data-out.json', mode='w', encoding='utf-8') as f:
        json.dump(A, f, ensure_ascii=False, indent=4)

    print('vse')

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

            each_split = each.split('~')
            hostname = each_split[0]
            username = each_split[1]
            time = each_split[2].split(',')
            time = time[0]

            ntime = datetime.fromtimestamp(int(time))

            # Serialize datetime here!
            ntime = ntime.strftime('%Y-%m-%d %H:%M:%S')

            outdict.update({'username': username, 'hostname': hostname, 'unixtime': time, 'normal time': ntime})
            with codecs.open(each, mode='r', encoding='utf-8-sig') as f:
                file = f.read()
                file = file.replace('\r', '').replace('\n', '')
                data = json.loads(file)
                outdict.update({'data': data})
                outlist.append(outdict)

        return outlist


class GivenOutData():

    @staticmethod
    def givenSelectedData1C(data: list[dict]) -> list[dict]:
        queryPublisher = '1С-Софт'
        queryDisplayVersion1octet = '8'
        queryDisplayVersion2octet = '3'
        queryDisplayVersion3octet = '19'
        outlist = list()
        alreadyHostnames = list()

        for each in data:
            if each['hostname'] in alreadyHostnames:
                continue

            for eachsoft in each['data']:
                eachsoft = {k.upper(): v for k, v in eachsoft.items()}

                if eachsoft['PUBLISHER'] == queryPublisher and eachsoft['DISPLAYVERSION'].split('.')[
                    2] == queryDisplayVersion3octet:
                    each['data'] = eachsoft
                    outlist.append(each)
                    alreadyHostnames.append(each['hostname'])
                    break

        return outlist

    @staticmethod
    def given1cAbove19(data: list[dict]) -> list[dict]:
        queryPublisher = '1С-Софт'
        queryDisplayVersion1octet = '8'
        queryDisplayVersion2octet = '3'
        queryDisplayVersion3octet = '19'
        outlist = list()
        alreadyHostnames = list()
        thisScopeVersion = list()

        for each in data:
            if each['hostname'] in alreadyHostnames:
                continue

            for eachsoft in each['data']:
                eachsoft = {k.upper(): v for k, v in eachsoft.items()}

                if eachsoft['PUBLISHER'] == queryPublisher and eachsoft['DISPLAYVERSION'].split('.')[
                    2] == queryDisplayVersion3octet:
                    each['data'] = eachsoft
                    outlist.append(each)
                    alreadyHostnames.append(each['hostname'])
                    break

        return outlist


    @staticmethod
    def storeToFile(data):
        with open('data-out.json', mode='w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    fileslist = GetDataFiles.getFromDirectory(DIR)
    A = DataSoup.parseDataFromFile(fileslist)

    B = GivenOutData.givenSelectedData1C(A)
    GivenOutData.storeToFile(B)

    print('vse')

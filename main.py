import json
import os
import codecs
from datetime import datetime
from typing import Tuple, List
import hashlib

import peewee
from models import *

import sensdata

'''
all sensitive data in sensdata.py
'''
DIR = sensdata.DIR
qVersion = 19
showOnlyAboveQVersions = True
suf = qVersion


class GetDataFiles():

    @staticmethod
    def getFromDirectory(directory) -> list:
        os.chdir(directory)
        return os.listdir(directory)


class DataSoup():#

    '''

    перед записью в таблицу нужно проверять:
    есть ли Хостнейм в таблице, если есть - НЕ делать новую запись (в начале читаем БД на это и потом используем данные из памяти)
    есть ли Конкретная запись о софте (row) - НЕ делать новую запись (тоже самое) (

    '''

    def __init__(self, flist):
        self._parseData = self.parseDataFromFile(flist)


    def prepareDB(self) -> list[list]:


        for each in self._parseData:
            hostname = each['hostname']
            username = each['username']
#


    @staticmethod
    def parseDataFromFile(flist) -> list[dict]:
        outlist = list()

        for each in flist:
            outdict = dict()
            alreadyUsedHashes_files = list()
            alreadyUsed_hosts = list()

            each_split = each.split('~')
            hostname = each_split[0]
            username = each_split[1]
            time = each_split[2].split(',')
            time = time[0]

            ntime = datetime.fromtimestamp(int(time))

            # Serialize datetime here!
            ntime = ntime.strftime('%Y-%m-%d %H:%M:%S')

            outdict.update({'username': username, 'hostname': hostname, 'unixtime': time, 'normal time': ntime})#
            hash_obj = hashlib.md5(str(username+hostname+time).encode())
            alreadyUsedHashes_files.append(hash_obj.hexdigest())#

            hash_obj = hashlib.md5(str(hostname).encode())
            alreadyUsedHashes_hosts.append(hash_obj.hexdigest())  #

            with codecs.open(each, mode='r', encoding='utf-8-sig') as f:
                file = f.read()
                file = file.replace('\r', '').replace('\n', '')
                data = json.loads(file)
                outdict.update({'data': data})
                outlist.append(outdict)

        return outlist


class GivenOutData():

    @staticmethod
    def givenSelectedData1C(data: list[dict]) -> tuple[list[dict], str]:
        queryPublisher = '1С-Софт'
        queryDisplayVersion1octet = '8'
        queryDisplayVersion2octet = '3'
        queryDisplayVersion3octet = '19'
        outlist = list()
        alreadyHostnames = list()
        suffix = '8.3.19'

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

        return outlist, suffix

    @staticmethod
    def given1cAbove19(data: list[dict], qV: int, flag: bool) -> tuple[list[dict], str]:
        queryPublisher = '1С-Софт'
        queryDisplayVersion1octet = '8'
        queryDisplayVersion2octet = '3'
        queryDisplayVersion3octet = 19
        outlist = list()
        alreadyHostnames = list()
        tempVerisons = list()
        tempEachsoft = dict()
        suffix = str()

        for each in data:
            if each['hostname'] in alreadyHostnames:
                continue

            tempVerisons = list()

            for eachsoft in each['data']:
                eachsoft = {k.upper(): v for k, v in eachsoft.items()}

                if eachsoft['PUBLISHER'] == queryPublisher:
                    tempVerisons.append(int(eachsoft['DISPLAYVERSION'].split('.')[2]))
                    tempEachsoft.update({k: v for k, v in eachsoft.items()})

            if qV not in tempVerisons and flag == True:
                # нужной версии нет на машине и флаг указывает на то что нужно показывать эту машину в экспорте

                each['data'] = tempEachsoft
                outlist.append(each)
                alreadyHostnames.append(each['hostname'])

        return outlist, suffix

    @staticmethod
    def storeToFile(data):
        filename = f'data-out.json'

        with open(filename, mode='w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

class DBwork():
    @staticmethod
    def save_toRowModel(data: list):
        row = models.Row(machine=data[0])



if __name__ == '__main__':
    fileslist = GetDataFiles.getFromDirectory(DIR)
    A = DataSoup.parseDataFromFile(fileslist)

    # B, suf = GivenOutData.given1cAbove19(A, qVersion, showOnlyAboveQVersions)
    B = GivenOutData.givenSelectedData1C(A)

    GivenOutData.storeToFile(B)

    print('vse')

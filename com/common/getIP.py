# -*- coding: UTF-8 -*-
import csv
import datetime
import os
import requests
from com.common.getPath import Path


class SaveIP(object):
    def __init__(self):
        self.path = Path().get_current_path()

    def save(self, *args, page=''):
        try:
            if args[0].get('X-Real-Ip') is not None:
                ip = args[0]['X-Real-Ip']
            elif args[0].get('host') is not None:
                ip = args[0]['host']
            else:
                ip = ""
            data = [ip, page, datetime.datetime.now().__format__("%Y-%m-%d %H:%M:%S")]
            file = os.path.join(self.path, "request_ip_info.csv")
            out = open(file, 'a', newline='')
            csv_write = csv.writer(out, dialect='excel')
            csv_write.writerow(data)
        except:
            pass

    def get_ip_address(self, ip: str):
        params = {"ip": ip}
        try:
            re = requests.get("http://ip.taobao.com/service/getIpInfo.php", params=params, timeout=1)
            if re.status_code != 200:
                re = requests.get("http://freeapi.ipip.net/" + ip)
                location = re.json()
                return location[0] + location[1] + location[2] + location[3] + "-" + location[4]
            location = re.json()['data']
            return location['country'] + location['region'] + location['city'] + "-" + location['isp']
        except Exception as e:
            return None

    def analysis(self):
        try:
            ip_address = {}
            file = csv.reader(open(os.path.join(self.path, "request_ip_info.csv"), 'r'))
            file_address = os.path.join(self.path, "request_ip_info_address.csv")
            out_address = open(file_address, 'w', newline='')
            csv_write = csv.writer(out_address, dialect='excel')
            new_data = []
            for item in file:
                temp = item
                if item[0] not in ip_address and item[0] != "":
                    address = self.get_ip_address(item[0])
                    temp.append(address)
                    new_data.append(temp)
                    ip_address[item[0]] = address
                    csv_write.writerow(temp)
                else:
                    address = ip_address.get(item[0])
                    temp.append(address)
                    new_data.append(temp)
                    csv_write.writerow(temp)
            return new_data
        except:
            pass

    def read_accesslog(self):
        try:
            result = []
            file = csv.reader(open(os.path.join(self.path, "request_ip_info_address.csv"), 'r'))
            i = 1
            for item in file:
                temp = item
                temp.insert(0, i)
                result.append(temp)
                i += 1
            return result
        except Exception as e:
            pass


if __name__ == '__main__':
    result = SaveIP().analysis()
    for item in result:
        print(item)

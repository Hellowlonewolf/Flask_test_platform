# -*- coding: UTF-8 -*-
import datetime
import json
import os
import time
import datetime
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from com.common.getPath import Path
from com.service.model import CoreSysDate
import logging

class Run_job:

    def __init__(self):
        self.engine = create_engine("mysql+pymysql://tobuser:ts@123@172.16.0.13/xy_standard_asset?charset=utf8")
        self.session = sessionmaker(self.engine)
        self.mySession = self.session()
        self.result = self.mySession.query(CoreSysDate)

    def get_core_sys_date(self):
        return datetime.datetime.strptime(
            str(self.result.filter(CoreSysDate.project_code == 'xy').first().core_sys_date),
            "%Y-%m-%d")

    def get_status(self):
        self.status = self.result.filter(CoreSysDate.project_code == 'xy').first().core_sys_status
        return self.status

    def tear_down(self):
        self.session.close_all()

    def write_line(self, line):
        try:
            fp = open('schedule_times.txt', 'a+')
            fp.write(line + '\n')
        except:
            pass

    def loadDataSet(self, line, splitChar='\t'):
        """
        输入：文件名
        输出：数据集
        描述：从文件读入数据集
        """
        fileName = 'schedule_times.txt'
        file = os.path.join(Path().get_current_path()+"/logs", 'myapp.log')
        dataSet = []
        with open(file) as fr:
            for line in fr.readlines()[-200:]:
                if str(line).find('runjob') != -1:
                    dataSet.append(line)
        return dataSet[-14:]

    def run(self, to_date):
        try:
            cur_day = self.get_core_sys_date()
            try:
                end_day = datetime.datetime.strptime(to_date, "%Y-%m-%d")
            except:
                end_day = cur_day + datetime.timedelta(days=int(to_date))
            i = 0
            temp = ''
            while cur_day < end_day:
                if end_day > cur_day:
                    cur_status = self.get_status()
                    if cur_status == 'normal' and temp != cur_day:
                        r = requests.post('http://172.16.0.13:8013/start')
                        logging.info("批处理日期：%s", str(cur_day.strftime("%Y-%m-%d")))
                        temp = cur_day
                        i = 0
                else:
                    logging.info('跑批日期小于当期日期')
                time.sleep(2)
                cur_day = self.get_core_sys_date()
                cur_status = self.get_status()
                logging.info("查询批处理状态 %s %s",cur_day,cur_status)
                i += 1
                if i > 30:
                    break
            logging.info("跑批结束")
            return {'message': True}
        except Exception as e:
            logging.error(str(e))
            return {'message': False}
        finally:
            self.tear_down()

    def get_date(self):
        date = self.get_core_sys_date().strftime("%Y-%m-%d")
        # self.tear_down()
        return str(date)


if __name__ == '__main__':
    enddate = '20171233'

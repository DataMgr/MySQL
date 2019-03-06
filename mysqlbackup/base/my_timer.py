from   datetime import datetime
import time


class Timer(object):

    def __init__(self):
        self.m_accumulate_ms = 0
        self.m_start_time = 0
        self.m_end_time = 0
        
    def sleep_s(self, second):
        time.sleep(second)

    def start(self):
        self.m_start_time = datetime.now()

    def stop(self):
        self.m_accumulate_ms = (datetime.now() - self.m_start_time).total_seconds()*1000
        return self.m_accumulate_ms 
        
    def pause(self):
        self.m_accumulate_ms = self.m_accumulate_ms + (datetime.now() - self.m_start_time).total_seconds()*1000
        return self.m_accumulate_ms

    def get_second(self):
        return self.m_accumulate_ms/1000
        
    def get_ms(self):
        return self.m_accumulate_ms 
    
    def set_start_time(self, i_strTime, i_strFmt="%Y-%m-%d %H:%M:%S.%f"):
        self.m_start_time = datetime.strptime(i_strTime, i_strFmt)

    def set_end_time(self, i_strTime, i_strFmt="%Y-%m-%d %H:%M:%S.%f"):
        self.m_end_time = datetime.strptime(i_strTime, i_strFmt)

    def calc_elapse_ms(self):
        return  (self.m_end_time - self.m_start_time).total_seconds() * 1000

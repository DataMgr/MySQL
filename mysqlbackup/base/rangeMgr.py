import common

class timer_RangeMgr:

    def __init__(self):
        self.m_List = []
        self.m_From = '0'
        self.m_To = '0'

    def setRange(self, i_timeType, i_nFrom, i_nTo):
        l_timeType = i_timeType.upper()

        if 'MONTH' == l_timeType:
            self.m_From = 1
            self.m_To = 12

        if 'WEEK' == l_timeType:
            self.m_From = 1
            self.m_To = 7

        if 'DAY' == l_timeType:
            self.m_From = 1
            self.m_To   = 31

        if 'HOUR' == l_timeType:
            self.m_From = 0
            self.m_To   = 23

        if 'MINUTE' == l_timeType:
            self.m_From = 1
            self.m_To = 59

        if (i_nFrom >= self.m_From) and (i_nTo <= self.m_To):
            self.m_From = i_nFrom
            self.m_To = i_nTo
            return True
        else:
            self.m_From = 0
            self.m_To = 0
            return False

    def setList(self, i_strHourList):
        self.m_List = []

        tmp_lists = i_strHourList.split(",")

        for i in range(len(tmp_lists)):
            self.m_List.append(common.toNum(tmp_lists[i]))

    def exist(self, i_nVal):
        if '*' in self.m_List:
            return True

        l_nVal = common.toNum(i_nVal)

        if len(self.m_List) > 0:
            retVal = l_nVal in self.m_List

        if l_nVal >= self.m_From and l_nVal <= self.m_To:
            retVal = True

        return retVal


if __name__ == "__main__":
    myRange=py_RangeMgr();
    myRange.setRange('hour',1,5)
    myRange.setList('6,8,20')
    print(myRange.exist(40))
       
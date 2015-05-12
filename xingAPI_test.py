__author__ = 'junho'

#-*-coding: utf-8 -*-

import sys
import win32com.client
import pythoncom

class XASessionEvents:
    logInState = 0
    def OnLogin(self, code, msg):
        print("OnLogin method is called")
        print(str(code))
        print(str(msg))
        if str(code) == '0000':
            XASessionEvents.logInState = 1

    def OnLogout(self):
        print("OnLogout method is called")

    def OnDisconnect(self):
        print("OnDisconnect method is called")

class XAQueryEvents:
    queryState = 0
    def OnReceiveData(self, szTrCode):
        print("ReceiveData")
        XAQueryEvents.queryState = 1
    def OnReceiveMessage(self, systemError, mesageCode, message):
        print("ReceiveMessage")


if __name__ == "__main__":
    server_addr = "demo.ebestsec.co.kr" # 모의투자의 주소는 demo.ebestsec.co.kr
                                        # 실제 거래할 때는 "hts.ebestsec.co.kr"
    server_port = 20001
    server_type = 0
    user_id = "iamjunho"
    user_pass = "boribori"
    user_certificate_pass = "NotAvailable"

    #--------------------------------------------------------------------------
    # Login Session
    #--------------------------------------------------------------------------
    inXASession = win32com.client.DispatchWithEvents("XA_Session.XASession", XASessionEvents)
    inXASession.ConnectServer(server_addr, server_port)
    inXASession.Login(user_id, user_pass, user_certificate_pass, server_type, 0)

    while XASessionEvents.logInState == 0:
        pythoncom.PumpWaitingMessages()

    # Call the GetAccountListCount() method
    nCount = inXASession.GetAccountListCount()
    print("The number of account: ", nCount)

    for i in range(nCount):
        print("Account: %d - %s" % (i, inXASession.GetAccountList(i)))

    #--------------------------------------------------------------------------
    # Get single data
    #--------------------------------------------------------------------------
    inXAQuery = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
    inXAQuery.LoadFromResFile("C:\\eBEST\\xingAPI\\Res\\t1102.res")
    inXAQuery.SetFieldData('t1102InBlock', 'shcode', 0, '000150')
    inXAQuery.Request(0)

    while XAQueryEvents.queryState == 0:
        pythoncom.PumpWaitingMessages()

    # Get FieldData
    name = inXAQuery.GetFieldData('t1102OutBlock', 'hname', 0)
    price = inXAQuery.GetFieldData('t1102OutBlock', 'price', 0)
    print("name: ", name)
    print("price: ", price)
    XAQueryEvents.queryState = 0

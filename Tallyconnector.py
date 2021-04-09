# Importing necessary packages
import logging
import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog
from tkinter.ttk import Progressbar
from tkinter.scrolledtext import ScrolledText
import time
import pyodbc
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import json
import requests
import re
import traceback
import fiscalyear
import itertools
# ssl._create_default_https_context = ssl._create_unverified_context
options = ["https://65.0.148.45:8181","https://demo.effitrac.com","https://msme.effitrac.com"]
scenario = ["Actual","PY"]
with open('config.json','r') as jsonfile:
    jsondata = json.load(jsonfile)
# 
# baseurl = jsondata['BaseUrl']
Batchsize = jsondata['BatchSize']
logfile = jsondata['LOG']


logging.basicConfig(filename=logfile,
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s')


url = '{}/erp/rest/dashboard/{}/{}/?cmpCode=RGS&orgCode={}'
delete_url = '{}/erp/rest/dashboard/dashboard/delete/?cmpCode=RGS&orgCode={}&accessToken={}&fyYear={}'
l1 = []
l2 = []
l3 = []
g1 = []
g2 = []


class TallyERP:
    def __init__(self):
        self.conn = None
        self.allvoucher_data = None
        self.my_purchase = None
        self.due_list = []
        self.company_name = None
        self.cursor = None
        self.current_fiscal_year = None

    def connection(self):
        """ Check the Tally ODBC connection """
        try:
            self.conn = pyodbc.connect("DSN=TALLYODBC64_9000")
        except pyodbc.InterfaceError:
            try:
                self.conn = pyodbc.connect('DSN=TALLYODBC_9000')
            except Exception:
                self.conn = None
        except Exception:
            return False
        if not self.conn:
            logging.info("NO ODBC CONNECTION FOR TALLY")
            return False
        self.cursor = self.conn.cursor()
        return True

    def get_company_name(self):
        """
            get the current company name from tally
        """
        try:
            result = self.conn.execute('select $Name from company')
            data = result.fetchall()
            self.company_name = data[0][0]
            return True
        except Exception:
            logging.error("ERROR WHILE GET THE COMPANY NAME %s",traceback.format_exc())
            return False

    def get_all_vouchers(self):
        """
            get the due date from tally vouchers table
        """
        try:
            allvoucher_result = self.cursor.execute(
                "select $voucherNumber,$Date,$StockItemName,$BasicDueDateOfPymt,$PartyLedgerName from allvouchers")
            self.allvoucher_data = allvoucher_result.fetchall()
            return self.allvoucher_data
        except Exception:
            logging.error("Error Occur Get Voucher List %s",traceback.format_exc())
            return False

    def get_group_details(self):
        """
            get the group details from tally
        """
        try:
            ledgertable = self.cursor.execute(
                "select $Name,$Parent,$_PrimaryGroup from ledger")
            ledgergroup = ledgertable.fetchall()
            grouptale = self.cursor.execute("select $Name,$Parent from groups")
            groupdata = grouptale.fetchall()
            for data in ledgergroup:
                l1.append(data[0])
                l2.append(data[1])
                l3.append(data[2])

            for data in groupdata:
                g1.append(data[0])
                g2.append(data[1])

        except Exception:
            logging.error("Error Occur Group Details %s",traceback.format_exc())
            return False

    def get_my_vouchers(self):
        try:
            result = self.cursor.execute('''select $VoucherTypeName, $VoucherNumber, $Date, $PartyLedgerName,$STATENAME,$COUNTRYOFRESIDENCE,$DELIVERYCITY,$LedgerName, \
                $StockItemName,$Discount,$Rate,$BilledQty,$SubAmount,$Led1,$AMT1,$Led2,$AMT2,$Led3,$AMT3,$Led4,$AMT4,$Led5,$AMT5,$Led6,$AMT6,$Led7,$AMT7,$Led8,$AMT8 from myvouchers where $StockItemName=' ' ''')
            self.my_vouchers_list = result.fetchall()
            logging.info("Fetch All Vouchers List")
            return self.my_vouchers_list
            
        except Exception:
            logging.error("Error Occur Get MyVoucher List %s",traceback.format_exc())
            return False

    def get_my_purchase(self):
        """
            get all the vouchers,inventory and ledgers from tally
        """
        try:
            result = self.cursor.execute("select $VoucherTypeName, $VoucherNumber, $Date, $PartyLedgerName,$STATENAME,$COUNTRYOFRESIDENCE,$DELIVERYCITY,$LedgerName, \
                    $StockItemName,$Discount,$Rate,$BilledQty,$SubAmount,$Led1,$AMT1,$Led2,$AMT2,$Led3,$AMT3,$Led4,$AMT4,$Led5,$AMT5,$Led6,$AMT6,$Led7,$AMT7,$Led8, \
                        $AMT8 from mypurchase")
            logging.info("Fetch All My Purchase List")
            self.my_purchase = result.fetchall()
            return self.my_purchase
        except Exception:
            logging.info("Exception Occur When data fetching in ODBC %s",traceback.format_exc())
            return False

    def get_financial_year(self, finicial_year):
        # get the financial year
        fiscalyear.setup_fiscal_calendar(start_month=4, start_day=1)
        current_year = fiscalyear.FiscalYear(finicial_year)
        FY_start, FY_end = current_year.start, current_year.end
        return FY_start, FY_end

    def get_fiscal_year(self, txn_date,is_datetime=False):
        if not is_datetime:
            txn_date = datetime.strptime(txn_date, '%Y-%m-%d')
        start, end_date = self.get_financial_year(txn_date.year)
        if txn_date >= end_date:
            FY = "{}-{}".format(end_date.year, end_date.year+1)
        elif txn_date <= end_date:
            FY = "{}-{}".format(end_date.year-1, end_date.year)
        else:
            FY = None
        return FY

    def get_float_converstion(self, data):
        """ convert string into float """
        if not data:
            return None
        if type(data) == float:
            return data
        else:
            return float(re.sub(',', '', data))
        
    def get_ledger_group(self,ledgername,position):
        """ return ledger parents , primary data"""
        # jsondata = json.load(open('partyledgergroups.json','r'))
        with open('partyledgergroups.json','r') as jsonfile:
            jsondata = json.load(jsonfile)
            jsonfile.close()
        if not ledgername in jsondata:
            return None
        payload = jsondata[ledgername]
        try:
            if position=='primary':
                with open('tallymapping.json','r') as jsonfile:
                    jsondata = json.load(jsonfile)
                    tallydefault = jsondata['TallydefaultGroup']
                    effitractmapping=jsondata['EffitrackGroup']
                jsonfile.close()
                data = payload[-1]
                if data in tallydefault:
                    index = tallydefault.index(data)
                    return effitractmapping[index]

                if re.search('expense',data):
                    return "Other expenses(Expense)"
                
                if re.search('income',data):
                    return "Other Income(Revenue)"

                return "Others"
            return payload[-position]
        except Exception:
            return None
    
    def get_groups_list(self,ledgername,ledgerlist):
        if ledgername in ledgerlist: 
            return ledgerlist[ledgername]
        return False

    def Account_payable(self,partyledgername,ledgerjsondata):
        data = self.get_groups_list(partyledgername,ledgerjsondata)
        if not data:
            return False
        if 'Sundry Creditors' in data:
            return True
        return False

        # #TODO: change the config for purchase
        # return True
        # if re.search("purchase",data.lower()):
        #     return True
        # if re.search("payment",data.lower()):
        #     return True
        # return False

    def Accounts_Receivable(self,partyledgername,ledgerjsondata):
        result = self.get_groups_list(partyledgername,ledgerjsondata)
        if not result:
            return False
        if 'Sundry Debtors' in result:
            return True
        return False
        #TODO: Need to change the config 
        # return True
        # if re.search("sales",data.lower()):
        #     return True
        # if re.search('invoice',data.lower()):
        #     return True
        # if re.search('receipt',data.lower()):
        #     return True
        # return False

    def metricdate(self,txndate):
        txdate_split = txndate.split("-")
        metricyear = int(txdate_split[0])+1
        # currentyear = datetime.now().year
        metricdate = "{}-{}-{}".format(metricyear,txdate_split[1],txdate_split[2])
        # print("txndate ",txndate)
        # print("metricdate",metricdate)
        return metricdate

    def m_total_amount(self,partyname,ledgerlist,ledgeramountlist):
        if partyname in ledgerlist:
            return ledgeramountlist[ledgerlist.index(partyname)]
        return None

    def check_period(self,date):
        global fiscal_year
        # self.current_fiscal_year = None
        if scenario_var.get() == 'Actual':
            self.current_fiscal_year = self.get_fiscal_year(datetime.now(),is_datetime=True)
            print(self.current_fiscal_year)
        elif scenario_var.get() == 'PY':
            self.current_fiscal_year = self.get_fiscal_year(datetime.now() - relativedelta(years = 1),is_datetime=True)
        fiscal_year = self.get_fiscal_year(date)
        if fiscal_year == self.current_fiscal_year:
            return True
        return False

    def my_purchase_process(self, my_purchase):
        """ 
            create a payload and store into a file
        """
        # global ledgerjsondata
        with open('partyledgergroups.json') as jsonfile:
            ledgerjsondata = json.load(jsonfile)
        
        sales_summary = []
        Account_payable = []
        Accounts_Receivable=[]
        # profit_and_loss_list = []
        for data in my_purchase:
            if not self.check_period(str(data[2])):
                return False 
            _metricdate = str(data[2]) if scenario_var == 'Actual' else self.metricdate(str(data[2]))
            salessummarypayload = {
                "orgCode": remove_space(root.orgtext.get()),
                "cmpCode": "RGS",
                "companyName":self.company_name,
                "fyYear": self.get_fiscal_year(str(data[2])),
                "scenario": scenario_var.get(),
                "dashboardType": "sales_summary",
                "metricType": data[0],
                "txnDate": str(data[2]),
                "dayOfMonth": data[2].day if data[2] else None,
                "monthOfYear": data[2].month if data[2] else None,
                "dayOfYear": data[2].year if data[2] else None,
                "metricDate": _metricdate,
                "dueDate": self.get_due_date(data[2], data[1], data[3]),
                "mId": data[1],
                "mPartyCode": None,
                "mPartyName": data[3],
                "mPcode": None,
                "mDesc": data[8],
                "mQty": data[11],
                "mUnitPrice": self.get_float_converstion(data[10]),
                "mDiscount": data[9],
                "mGST": None,
                "mTotalPrice": self.get_float_converstion(data[12]),
                "mLedger1": data[13],
                "mLedgerAmt1": self.get_float_converstion(data[14]),
                "mLedger2": data[15],
                "mLedgerAmt2": self.get_float_converstion(data[16]),
                "mLedger3": data[17],
                "mLedgerAmt3": self.get_float_converstion(data[18]),
                "mLedger4": data[19],
                "mLedgerAmt4": self.get_float_converstion(data[20]),
                "mLedger5": data[21],
                "mLedgerAmt5":  self.get_float_converstion(data[22]),
                "mLedger6": data[23],
                "mLedgerAmt6": self.get_float_converstion(data[24]),
                "mLedger7": data[25],
                "mLedgerAmt7": self.get_float_converstion(data[26]),
                "mLedger8": data[27],
                "mLedgerAmt8": self.get_float_converstion(data[28]),
                "mTotalAmount": self.m_total_amount(data[3],[data[13],data[15],data[17],data[19],data[21],data[23],data[25],data[27]],\
                    [self.get_float_converstion(data[14]),self.get_float_converstion(data[14]),self.get_float_converstion(data[16]),self.get_float_converstion(data[18]),\
                        self.get_float_converstion(data[20]),self.get_float_converstion(data[22]),self.get_float_converstion(data[24]),self.get_float_converstion(data[26]),\
                            self.get_float_converstion(data[28])]),
                "mState": data[4],
                "mCity": data[6],
                "mCountry": data[5]
            }
            if self.Account_payable(data[3],ledgerjsondata):
                AP_payload = {
                    "orgCode": remove_space(root.orgtext.get()),
                    "cmpCode": "RGS",
                    "companyName":self.company_name,
                    "fyYear": self.get_fiscal_year(str(data[2])),
                    "scenario": scenario_var.get(),
                    "dashboardType": "Account_payable",
                    "metricType": data[0],
                    "txnDate": str(data[2]),
                    "dayOfMonth": data[2].day if data[2] else None,
                    "monthOfYear": data[2].month if data[2] else None,
                    "dayOfYear": data[2].year if data[2] else None,
                    "metricDate": _metricdate,
                    "dueDate": self.get_due_date(data[2], data[1], data[3]),
                    "mId": data[1],
                    "mPartyCode": None,
                    "mPartyName": data[3],
                    "mPcode": None,
                    "mDesc": data[8],
                    "mQty": data[11],
                    "mUnitPrice": self.get_float_converstion(data[10]),
                    "mDiscount": data[9],
                    "mGST": None,
                    "mTotalPrice": self.get_float_converstion(data[12]),
                    "mLedger1": data[13],
                    "mLedgerAmt1": self.get_float_converstion(data[14]),
                    "mLedger2": data[15],
                    "mLedgerAmt2": self.get_float_converstion(data[16]),
                    "mLedger3": data[17],
                    "mLedgerAmt3": self.get_float_converstion(data[18]),
                    "mLedger4": data[19],
                    "mLedgerAmt4": self.get_float_converstion(data[20]),
                    "mLedger5": data[21],
                    "mLedgerAmt5":  self.get_float_converstion(data[22]),
                    "mLedger6": data[23],
                    "mLedgerAmt6": self.get_float_converstion(data[24]),
                    "mLedger7": data[25],
                    "mLedgerAmt7": self.get_float_converstion(data[26]),
                    "mLedger8": data[27],
                    "mLedgerAmt8": self.get_float_converstion(data[28]),
                    "mTotalAmount": self.m_total_amount(data[3],[data[13],data[15],data[17],data[19],data[21],data[23],data[25],data[27]],\
                        [self.get_float_converstion(data[14]),self.get_float_converstion(data[14]),self.get_float_converstion(data[16]),self.get_float_converstion(data[18]),\
                        self.get_float_converstion(data[20]),self.get_float_converstion(data[22]),self.get_float_converstion(data[24]),self.get_float_converstion(data[26]),\
                            self.get_float_converstion(data[28])]),
                    "mState": data[4],
                    "mCity": data[6],
                    "mCountry": data[5]
                }
                Account_payable.append(AP_payload)
            if self.Accounts_Receivable(data[3],ledgerjsondata):
                AR_payload = {
                    "orgCode": remove_space(root.orgtext.get()),
                    "cmpCode": "RGS",
                    "companyName":self.company_name,
                    "fyYear": self.get_fiscal_year(str(data[2])),
                    "scenario": scenario_var.get(),
                    "dashboardType": "Accounts_Receivable",
                    "metricType": data[0],
                    "txnDate": str(data[2]),
                    "dayOfMonth": data[2].day if data[2] else None,
                    "monthOfYear": data[2].month if data[2] else None,
                    "dayOfYear": data[2].year if data[2] else None,
                    "metricDate": _metricdate,
                    "dueDate": self.get_due_date(data[2], data[1], data[3]),
                    "mId": data[1],
                    "mPartyCode": None,
                    "mPartyName": data[3],
                    "mPcode": None,
                    "mDesc": data[8],
                    "mQty": data[11],
                    "mUnitPrice": self.get_float_converstion(data[10]),
                    "mDiscount": data[9],
                    "mGST": None,
                    "mTotalPrice": self.get_float_converstion(data[12]),
                    "mLedger1": data[13],
                    "mLedgerAmt1": self.get_float_converstion(data[14]),
                    "mLedger2": data[15],
                    "mLedgerAmt2": self.get_float_converstion(data[16]),
                    "mLedger3": data[17],
                    "mLedgerAmt3": self.get_float_converstion(data[18]),
                    "mLedger4": data[19],
                    "mLedgerAmt4": self.get_float_converstion(data[20]),
                    "mLedger5": data[21],
                    "mLedgerAmt5":  self.get_float_converstion(data[22]),
                    "mLedger6": data[23],
                    "mLedgerAmt6": self.get_float_converstion(data[24]),
                    "mLedger7": data[25],
                    "mLedgerAmt7": self.get_float_converstion(data[26]),
                    "mLedger8": data[27],
                    "mLedgerAmt8": self.get_float_converstion(data[28]),
                    "mTotalAmount": self.m_total_amount(data[3],[data[13],data[15],data[17],data[19],data[21],data[23],data[25],data[27]],\
                        [self.get_float_converstion(data[14]),self.get_float_converstion(data[14]),self.get_float_converstion(data[16]),self.get_float_converstion(data[18]),\
                        self.get_float_converstion(data[20]),self.get_float_converstion(data[22]),self.get_float_converstion(data[24]),self.get_float_converstion(data[26]),\
                            self.get_float_converstion(data[28])]),
                    "mState": data[4],
                    "mCity": data[6],
                    "mCountry": data[5]
                }
                Accounts_Receivable.append(AR_payload)
            sales_summary.append(salessummarypayload)
            # profit_and_loss_list.append(profit_and_loss_payload)         
        # self.save_purchase(profit_and_loss_list,'p&l.json')
        self.save_purchase(Accounts_Receivable,'AR.json')
        self.save_purchase(Account_payable,'AP.json')
        return self.save_purchase(sales_summary,'salessummary.json')

    def get_due_date(self, txn_date, vouchernumber, ledgername):
        """ 
            get due date from the vouchers tally
        """
        due_date = txn_date + timedelta(days=30)
        if not self.due_list:
            return str(due_date)
        for data in self.due_list:
            if str(txn_date) == data['Date'] and vouchernumber == data['voucherNumber'] and ledgername == data['LedgerName']:
                try:
                    print("DueDate", data['BasicDueDateOfPymt'],
                        data['Date'], data['voucherNumber'], data['LedgerName'])
                    duedate = data['BasicDueDateOfPymt'].split('Days')[0]
                    actualduedate = txn_date + timedelta(days=int(duedate))
                    print(str(actualduedate))
                    return str(actualduedate)
                except Exception:
                    return str(due_date)
        return str(due_date)

    def get_due_date_list(self, allvoucher_data):
        """
            create due date payload
        """
        try:
            for data in allvoucher_data:
                if data[3]:
                    payload = {
                        'companyName': self.company_name,
                        'voucherNumber': data[0],
                        'Date': str(data[1]),
                        'StockItemName': data[2],
                        'BasicDueDateOfPymt': data[3],
                        'LedgerName': data[4]
                    }
                    self.due_list.append(payload)
        except Exception:
            return False

    def save_purchase(self, purchase_list,filename):
        """
            save data into file 
        """
        print("save_purchase")
        logging.info("Saved: %s. Total Data= %s",filename,len(purchase_list))
        with open(filename, "w+") as json_file:
            json_file.write(json.dumps(purchase_list, indent=4))
        return True
        
        # SERVERPROCESS.start()
TALLYPROCESS = TallyERP()


class Group:
    def __init__(self):
        self.payload = {}
        self.final = "\u0004 Primary"

    def iter1(self):
        finallist = []
        for i in self.duplicates(g2, self.final):
            finallist.append(g1[i])
        return finallist

    def duplicates(self, list, item):
        return [i for i, x in enumerate(list) if x == item]

    def iter2(self, parselist):
        templist = []
        for i in parselist:
            if i in g2:
                self.payload[i] = [g1[i] for i in self.duplicates(g2, i)]
                templist.append([g1[i] for i in self.duplicates(g2, i)])
        newl = list(itertools.chain.from_iterable(templist))
        return newl

    def createjson(self):
        result1 = self.iter1()
        if result1:
            self.payload[self.final] = result1
        iter = self.iter2(result1)

        while True:
            if not iter:
                break
            iter = self.iter2(iter)
        return self.payload


# GB = Group()
# groupdata = GB.createjson()


class LedgerGroup:
    def __init__(self, payload):

        self.payload = payload
        self.final = "\u0004 Primary"
        self.partyledgergroup = {}

    def topdownsearch(self, key):
        keys = list(self.payload.keys())
        for ind, i in enumerate(keys):
            if key in self.payload[i]:
                return keys[ind]

    def find_parents(self, ledgername):
        key = []
        if ledgername in l1:
            idx = l1.index(ledgername)
            iterdata = l2[idx]
            key.append(iterdata)
            primarylist = self.payload[self.final]
            while True:
                if iterdata in primarylist:
                    break
                if re.search("Primary", iterdata):
                    break
                iterdata = self.topdownsearch(iterdata)
                key.append(iterdata)
            return key

    def process_ledger(self):

        self.partyledgergroup["l1"] = l1
        self.partyledgergroup["l2"] = l2
        self.partyledgergroup["l3"] = l3
        self.partyledgergroup["g1"] = g1
        self.partyledgergroup["g2"] = g2

        for i in l1:
            self.partyledgergroup[i] = self.find_parents(i)
        with open('partyledgergroups.json', 'w+') as jsonfile:
            jsonfile.write(json.dumps(self.partyledgergroup, indent=4))
            jsonfile.close()
            logging.info("SAVE PROCESS LEDGER")
        logging.info("Party ledger group created")


class ServerRequests:
    def __init__(self):
        self.authToken = None
        self.orgcode = None

    def verify_orgcode_authtoken(self, tabletype,urltype, Orgcode,authtoken):
        # logging.info("ORGCODE %s", Orgcode)
        try:
            manageurl = url.format(baseurl,tabletype,urltype,Orgcode)
            auth_url = "&accessToken={}".format(authtoken)
            request_url = manageurl + auth_url
            print(request_url)
            res = requests.post(request_url, headers={
                                'Content-Type': 'application/json'}, verify=False)
        except requests.exceptions.ConnectionError:
            return "Connection Error"
        except Exception as ex:
            print(repr(ex))
            # logging.info("Connection Error Please Contact Us")
            res = None
        # logging.info(res.json())
        # print(res.json()['reponseMessages'])
        if not res or res.status_code != 200:
            return False
        print(res.json()['reponseMessages'])
        return res.json()['reponseMessages']
        # self.authToken = authtoken
        
    def delete_duplicate(self,orgcode,authtoken):
        try:
            # FY = TALLYPROCESS.get_fiscal_year(datetime.now(),is_datetime=True)
            request_url = delete_url.format(baseurl,orgcode,authtoken,fiscal_year)
            # print(request_url)
            res = requests.post(request_url,headers={'Content-Type': 'application/json'}, verify=False)
        except requests.exceptions.ConnectionError:
            logging.info("Connection Error Please Check Internet")
            return "Connection Error"
        except Exception:
            logging.info("Error Occur When Delete Duplicate %s",traceback.format_exc())
            res = None
        
        if not res or res.status_code != 200:
            return False
        # logging.info(res.json())
        logging.info("Delete successfully %s",res.json())
        return res.json()['reponseMessages']

    def get_data_to_server(self,filename):
        try:
            with open(filename) as json_file:
                payload = json.load(json_file)
                json_file.close()
                print("GET FROM SERVER")
                print(len(payload))

                if len(payload) >= Batchsize:
                    return payload[:Batchsize]
                else:
                    return payload
        except Exception as ex:
            print(repr(ex))
            return False

    def pop_from_list(self, removepayload,filename):
        with open(filename) as json_file:
            payload = json.load(json_file)
            json_file.close()
        newlist = [i for i in payload if i not in removepayload]
        logging.info("payload info %s",len(payload))
        with open(filename, 'w+') as jsonfile:
            jsonfile.write(json.dumps(newlist, indent=4))
            jsonfile.close()
        return True

    def start(self):
        while True:
            try:
                salessummary_payload = self.get_data_to_server('salessummary.json')
                # pl_payload = self.get_data_to_server('p&l.json')
                AP_payload = self.get_data_to_server('AP.json')
                AR_payload = self.get_data_to_server('AR.json')
                # print("get_payload")
                
                if not salessummary_payload and not AP_payload and not AR_payload :
                    return True

                if salessummary_payload:
                    result = self.send_data_from_file('SalesSummary', 'Create',salessummary_payload)
                    if result:
                        self.pop_from_list(salessummary_payload,'salessummary.json')
                if AP_payload:
                    result = self.send_data_from_file('AdvancePayment','Create',AP_payload)
                    if result=="Connection Error":
                        return result
                    if result:
                        self.pop_from_list(AP_payload,'AP.json')
                if AR_payload:
                    result = self.send_data_from_file('AdvanceReceipt','Create',AR_payload)
                    if result=="Connection Error":
                        return result
                    if result:
                        self.pop_from_list(AR_payload,'AR.json')
                # if pl_payload:
                #     result = self.send_data_from_file('ProfitAndLoss','Create',pl_payload)
                #     if result:
                #         self.pop_from_list(pl_payload,'p&l.json')
                
            except Exception:
                logging.info("Exception Occur Data Push to server %s",traceback.format_exc())
                return False

    def send_data_from_file(self,tabletype,urltype,data):
        try:
            payload = json.dumps(data)
            # print(data[0])
            manageurl = url.format(baseurl,tabletype,urltype,remove_space(root.orgtext.get()))
            auth_url = "&accessToken={}".format(remove_space(root.authtext.get()))
            request_url = manageurl+auth_url
            res = requests.post(request_url, data=payload, headers={
                                'Content-Type': 'application/json'}, verify=False)
        except requests.exceptions.ConnectionError:
            return "Connection Error"
        except Exception:
            logging.info("Exception Occur Send data to Server %s",traceback.format_exc())
            # print(repr(ex))
            res = None
        # print(res)
        if not res or res.status_code != 200:
            print("RESPONSE FAIL")
            return False
        logging.info("{} Batch Data push to server".format(tabletype))
        return True


SERVERPROCESS = ServerRequests()

class TextHandler(logging.Handler):
    """This class allows you to log to a tkinter Text or ScrolledText widget"""

    def __init__(self, text):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        
        # self.other_dns.grid(row=0,column=0)
        
        self.other_dns = None
        # self.other_dns.grid_forget()
        # Store a reference to the Text it will log to
        self.text = text
        
    def main_page(self):
        # self.other_dns = Entry(root, width=100,state='disable')
        self.other_dns = Entry(root, width=100)
        var.set(options[0])       
        root.var = OptionMenu(root,var,*options)
        root.var.config(bg="#E8D579",width=50)
        root.var.grid(row=0,column=0,padx=10,pady=10,ipady=1)
        scenario_var.set(scenario[0])
        root.scenario_var = OptionMenu(root,scenario_var,*scenario)
        root.scenario_var.config(bg="#E8D579",width=10)
        root.scenario_var.grid(row=1,column=0,padx=1,pady=10,ipady=1)
        
        link_Label = Label(root, text="CompanyCode :", bg="#E8D579")
        # link_Label.place()

        link_Label.grid(row=3,column=0,padx=10,pady=10,ipady=1,sticky='w')

        root.orgtext = Entry(root ,width=100)


        root.orgtext.grid(row=3, column=0,padx=120,pady=10,ipady=3)
        link_Label_auth = Label(root, text="AuthToken :", bg="#E8D579")
        # link_Label.place()

        link_Label_auth.grid(row=4,column=0,padx=20,pady=10,ipady=0,sticky='w')

        root.authtext = Entry(root ,width=100)
        root.authtext.grid(row=4, column=0,padx=120,pady=10,ipady=3)

        copyButton = Button(root, text="Transfer Tally Backup", command=StartUI, width=15)
        # copyButton.pack(side=LEFT, padx=10,ipadx=5,ipady=5)
        copyButton.grid(row=5, column=0,pady=5,padx=100)
    
    
    def emit(self, record):
        msg = self.format(record)

        def append():
            self.text.configure(state='normal')
            self.text.insert(tk.END, msg + '\n')
            self.text.configure(state='disabled')
            # Autoscroll to the bottom
            self.text.yview(tk.END)
        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)
        
def remove_space(text):
    if not text:
        print("EMPTY")
        return None
    pattern = re.compile(r'\s+')
    return re.sub(pattern,'',text)

def check_tally_connection():
    if not TALLYPROCESS.connection():
        messagebox.showerror(
            "Error!", "Open Tally and check odbc connection string")
        exit()
    logging.info("Fetching data form Tally..Please wait....")
    result = TALLYPROCESS.get_company_name()
    if not result:
        messagebox.showerror("Error!", "Open Tally Load TDL & company")
        logging.error("Open Tally and Load Company ")
        exit()
    else:
        if not messagebox.askokcancel("Confirm", "Are you sure to Fetch the Company:{}".format(TALLYPROCESS.company_name)):
            exit()

    logging.info("Opened {}".format(TALLYPROCESS.company_name))


def StartUI():
    print(datetime.now())
    global baseurl
    baseurl = var.get()
    print("BASE URL",baseurl)
    if not remove_space(root.orgtext.get()) or not remove_space(root.authtext.get()):
        if messagebox.askretrycancel("Error!", "Please Enter OrgCode and AuthToken "):
            root.mainloop()
        else:
            exit()
        # root.orgtext.set("")
    else:
        # logging.info("Get AuthToken Using Orgcode: %s", root.orgtext.get())
        Validationresult = SERVERPROCESS.verify_orgcode_authtoken('TokenGenerate','Validate',remove_space(root.orgtext.get()),remove_space(root.authtext.get()))
        if not Validationresult:
            logging.info("Connection Error please Try after some times")
            if messagebox.askretrycancel("Message","Connection Error Please Try after some times"):
                root.mainloop()
            else:
                exit()
        elif Validationresult == "Connection Error":
            if messagebox.askretrycancel("Error","Please Check Internet Connection"):
                root.mainloop()
            else:
                exit()
        elif not Validationresult == 'Success':
            logging.info("Invalid Access Token")
            if messagebox.askretrycancel("Error","Invalid Access Token or ORGCODE"):
                root.mainloop()
            else:
                exit()
        else:
            messagebox.showinfo("Message","Token Verified Successfully")
            logging.info("AuthToken Verified")
    check_tally_connection()
    TALLYPROCESS.get_group_details()
    GB = Group()
    groupdata = GB.createjson()
    LG = LedgerGroup(groupdata)
    LG.process_ledger()
    logging.info("group details got")
    TALLYPROCESS.get_due_date_list(TALLYPROCESS.get_all_vouchers())
    my_purchase = TALLYPROCESS.get_my_purchase()
    my_vouchers = TALLYPROCESS.get_my_vouchers()

    
    myvoucherslist = my_purchase + my_vouchers
    if not myvoucherslist:
        messagebox.showinfo("Message","Empty Data Please Load TDL")
        exit()
        #"C:\Program Files\TallyPrime\tally.exe" /NOINITDL "/TDL:C:\Users\cooki\Documents\tallyerp\PurchaseDetails.txt"

    if not TALLYPROCESS.my_purchase_process(myvoucherslist):
        print("Period Not match")
        logging.info("Period not match with scenario")
        if messagebox.askretrycancel("Error","Period Not match with Scenario"):
            root.mainloop()
        else:
            exit()
        print("data saved into tally")
    logging.info("Payload Ready Please Ignore Not Responding.... Data Pushing Into Server")
    messagebox.showinfo("Message","TALLY DATA EXTRACTION COMPLETED. NOW SENDING TO SERVER")
    logger.info("SENDING TO SERVER")
    
    if not SERVERPROCESS.delete_duplicate(remove_space(root.orgtext.get()),remove_space(root.authtext.get())):
        messagebox.showerror("Message","Connection Error Please Try after some times")
        exit()
    # # print("delete tables")
    response = SERVERPROCESS.start()
    if response == "Connection Error":
        if messagebox.askretrycancel("Error!","Please Check Internet"):
            exit()
    if response:
        messagebox.showinfo("Message","All Data Push to server")
        exit()
    else:
        messagebox.askretrycancel("Message","Error While data push to server Contact Us")
        exit()
    print(datetime.now())
mymappinglist = ["Revenue from operations","Other income","Cost of materials consumed","Purchases of Stock-in-Trade",\
    "Changes in inventories of finished goods work-in-progress and Stock-in-Trade","Employee benefits expense", \
    "Finance costs","Depreciation and amortization expense","Other expenses","Current tax","Deferred tax"]
def set_mapping():
    # check_tally_connection()
    # TALLYPROCESS.get_group_details()
    with open('partyledgergroups.json') as jsonfile:
        ledger = json.load(jsonfile)
    ledgerlist = ledger['l1']  
    
    # scrollbar = Scrollbar(master)  
    # scrollbar.pack(side = LEFT, fill = Y)
    # mylist = Listbox(master,yscrollcommand=scrollbar.set)
    # variable = mymappinglist[0]
    # for i in ledgerlist:
    #     mylist.insert(END,i)
    #     myoption = OptionMenu(master,variable,*mymappinglist)
    
    # # myoption.pack(RIGHT,BOTH)
    # # mylist.pack()
    # # myoption
    # mylist.pack(fill = BOTH ) 
  
    # scroll_bar.config( command = mylist.yview )
    master.mainloop()
    

# master = tk.Tk()
# set_mapping()
root = tk.Tk()
root.geometry("820x820")
root.title("Tally to Effitrac")
root.config(background="#5f5f5f")
st = ScrolledText(root, state='disabled')
# st.place()
st.grid(row=6,column=0,pady=10)
var = StringVar(root)
scenario_var = StringVar(root)
# Create textLogger
text_handler = TextHandler(st)
text_handler.main_page()
logging.basicConfig(filename=logfile,
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s')

global logger
# Add the handler to logger
logger = logging.getLogger()

logger.addHandler(text_handler)

# logger.info("Getting Group details")
# CreateWidgets()

root.mainloop()

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
import json
import requests
import re
import ssl
import fiscalyear
import itertools
# ssl._create_default_https_context = ssl._create_unverified_context

logging.basicConfig(
    level=logging.INFO,
    format='%(process)d | %(levelname)s | %(message)s'
)


url = 'https://65.0.148.45:8181/erp/rest/dashboard/{}/{}/?cmpCode=RGS&orgCode={}'
l1 = []
l2 = []
l3 = []
g1 = []
g2 = []
global _orgcode
global _authtoken

class TallyERP:
    def __init__(self):
        self.conn = None
        self.allvoucher_data = None
        self.my_purchase = None
        self.due_list = []
        self.company_name = None
        self.cursor = None

    def connection(self):
        logger.info("CALL TALLY")
        try:
            self.conn = pyodbc.connect("DSN=TALLYODBC64_9000")
        except pyodbc.InterfaceError:
            self.conn = pyodbc.connect('DSN=TALLYODBC_9000')
        except Exception:
            return False
        self.cursor = self.conn.cursor()
        return True

    def get_company_name(self):
        try:
            result = self.conn.execute('select $Name from company')
            data = result.fetchall()
            self.company_name = data[0][0]
            return True
        except Exception as ex:
            print(repr(ex))
            return False

    def get_all_vouchers(self):
        try:
            allvoucher_result = self.cursor.execute(
                "select $voucherNumber,$Date,$StockItemName,$BasicDueDateOfPymt,$PartyLedgerName from allvouchers")
            self.allvoucher_data = allvoucher_result.fetchall()
            return self.allvoucher_data
        except Exception:
            return False

    def get_group_details(self):
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
            return False

    def get_my_purchase(self):
        try:
            result = self.cursor.execute("select $VoucherTypeName, $VoucherNumber, $Date, $PartyLedgerName,$STATENAME,$COUNTRYOFRESIDENCE,$DELIVERYCITY,$LedgerName, \
                    $StockItemName,$Discount,$Rate,$BilledQty,$SubAmount,$Led1,$AMT1,$Led2,$AMT2,$Led3,$AMT3,$Led4,$AMT4,$Led5,$AMT5,$Led6,$AMT6,$Led7,$AMT7,$Led8, \
                        $AMT8 from mypurchase")
            self.my_purchase = result.fetchall()
            return self.my_purchase
        except Exception:
            return False

    def get_financial_year(self, finicial_year):
        # get the financial year
        fiscalyear.setup_fiscal_calendar(start_month=4, start_day=1)
        current_year = fiscalyear.FiscalYear(finicial_year)
        FY_start, FY_end = current_year.start, current_year.end
        return FY_start, FY_end

    def get_fiscal_year(self, txn_date):
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
        if not data:
            return None
        if type(data) == float:
            return data
        else:
            return float(re.sub(',', '', data))
        
    def get_ledger_group(self,ledgername,position):
        jsondata = json.load(open('partyledgergroups.json','r'))
        if not ledgername in jsondata:
            return None
        payload = jsondata[ledgername]
        # print(payload)
        logging.info(payload)
        try:
            return payload[-position]
        except Exception:
            return None
        
    def my_purchase_process(self, my_purchase):
        purchase_list = []
        profit_and_loss_list = []
        for data in my_purchase:
            profit_and_loss_payload = {
                "orgCode": remove_space(root.orgtext.get()),
                "cmpCode": "RGS",
                "companyName":self.company_name,
                "fyYear": self.get_fiscal_year(str(data[2])),
                "scenario": "Actual",
                "dashboardType": None,
                "metricType": data[0],
                "txnDate": str(data[2]),
                "dayOfMonth": data[2].day if data[2] else None,
                "monthOfYear": data[2].month if data[2] else None,
                "dayOfYear": data[2].year if data[2] else None,
                "metricDate": str(data[2]),
                "mId": data[1],
                "mPartyName": data[3],
                "mDesc": data[8],
                "mQty": data[11],
                "mUnitPrice": self.get_float_converstion(data[10]),
                "mDiscount": data[9],
                "mTotalPrice": self.get_float_converstion(data[12]),
                "mTotalAmount": self.get_float_converstion(data[14]),
                "mState": data[4],
                "mCity": data[6],
                "mCountry": data[5],
                "mLedger1": data[13],
                "mLegder1group1":self.get_ledger_group(data[13],1) if data[13] else None,
                "mLegder1group2":self.get_ledger_group(data[13],2) if data[13] else None,
                "mLegder1group3":self.get_ledger_group(data[13],3) if data[13] else None,
                "mLegder1group4":self.get_ledger_group(data[13],4) if data[13] else None,
                "mLegder1group5":self.get_ledger_group(data[13],5) if data[13] else None,
                "mLedgerAmt1":data[14],
                "mLedger2":data[15],
                "mLegder2group1":self.get_ledger_group(data[15],1) if data[15] else None,
                "mLegder2group2":self.get_ledger_group(data[15],2) if data[15] else None,
                "mLegder2group3":self.get_ledger_group(data[15],3) if data[15] else None,
                "mLegder2group4":self.get_ledger_group(data[15],4) if data[15] else None,
                "mLegder2roup5":self.get_ledger_group(data[15],5) if data[15] else None,
                "mLedgerAmt2":self.get_float_converstion(data[16]),
                "mLedger3":data[17],
                "mLegder3group1":self.get_ledger_group(data[17],1) if data[17] else None,
                "mLegder3group2":self.get_ledger_group(data[17],2) if data[17] else None,
                "mLegder3group3":self.get_ledger_group(data[17],3) if data[17] else None,
                "mLegder3group4":self.get_ledger_group(data[17],4) if data[17] else None,
                "mLegder3group5":self.get_ledger_group(data[17],5) if data[17] else None,
                "mLedgerAmt3":self.get_float_converstion(data[18]),
                "mLedger4":data[19],
                "mLegder4group1":self.get_ledger_group(data[19],1) if data[19] else None,
                "mLegder4group2":self.get_ledger_group(data[19],2) if data[19] else None,
                "mLegder4group3":self.get_ledger_group(data[19],3) if data[19] else None,
                "mLegder4group4":self.get_ledger_group(data[19],4) if data[19] else None,
                "mLegder4group5":self.get_ledger_group(data[19],5) if data[19] else None,
                "mLedgerAmt4":self.get_float_converstion(data[20]),
                "mLedger5":data[21],
                "mLegder5group1":self.get_ledger_group(data[21],1) if data[21] else None,
                "mLegder5group2":self.get_ledger_group(data[21],2) if data[21] else None,
                "mLegder5group3":self.get_ledger_group(data[21],3) if data[21] else None,
                "mLegder5group4":self.get_ledger_group(data[21],4) if data[21] else None,
                "mLegder5group5":self.get_ledger_group(data[21],5) if data[21] else None,
                "mLedgerAmt5":self.get_float_converstion(data[22]),
                "mLedger6":data[23],
                "mLegder6group1":self.get_ledger_group(data[23],1) if data[23] else None,
                "mLegder6group2":self.get_ledger_group(data[23],2) if data[23] else None,
                "mLegder6group3":self.get_ledger_group(data[23],3) if data[23] else None,
                "mLegder6group4":self.get_ledger_group(data[23],4) if data[23] else None,
                "mLegder6group5":self.get_ledger_group(data[23],5) if data[23] else None,
                "mLedgerAmt6":self.get_float_converstion(data[24]),
                "mLedger7": data[25],
                "mLegder7group1":self.get_ledger_group(data[25],1) if data[25] else None,
                "mLegder7group2":self.get_ledger_group(data[25],2) if data[25] else None,
                "mLegder7group3":self.get_ledger_group(data[25],3) if data[25] else None,
                "mLegder7group4":self.get_ledger_group(data[25],4) if data[25] else None,
                "mLegder7group5":self.get_ledger_group(data[25],5) if data[25] else None,
                "mLedgerAmt7":self.get_float_converstion(data[26]),
                "mLedger8":data[27],
                "mLegder8group1":self.get_ledger_group(data[27],1) if data[27] else None,
                "mLegder8group2":self.get_ledger_group(data[27],2) if data[27] else None,
                "mLegder8group3":self.get_ledger_group(data[27],3) if data[27] else None,
                "mLegder8group4":self.get_ledger_group(data[27],4) if data[27] else None,
                "mLegder8group5":self.get_ledger_group(data[27],5) if data[27] else None,
                "mLedgerAmt8":self.get_float_converstion(data[28]),
            }
            
            payload = {
                "orgCode": remove_space(root.orgtext.get()),
                "cmpCode": "RGS",
                "companyName":self.company_name,
                "fyYear": self.get_fiscal_year(str(data[2])),
                "scenario": "Actual",
                "dashboardType": None,
                "metricType": data[0],
                "txnDate": str(data[2]),
                "dayOfMonth": data[2].day if data[2] else None,
                "monthOfYear": data[2].month if data[2] else None,
                "dayOfYear": data[2].year if data[2] else None,
                "metricDate": str(data[2]),
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
                "mTotalAmount": self.get_float_converstion(data[14]),
                "mState": data[4],
                "mCity": data[6],
                "mCountry": data[5]
            }
            purchase_list.append(payload)
            profit_and_loss_list.append(profit_and_loss_payload)
        self.save_purchase(profit_and_loss_list,'p&l.json')
        return self.save_purchase(purchase_list,'purchase.json')

    def get_due_date(self, txn_date, vouchernumber, ledgername):

        due_date = txn_date + timedelta(days=30)
        if not self.due_list:
            return str(due_date)
        for data in self.due_list:
            if str(txn_date) == data['Date'] and vouchernumber == data['voucherNumber'] and ledgername == data['LedgerName']:
                print("DueDate", data['BasicDueDateOfPymt'],
                      data['Date'], data['voucherNumber'], data['LedgerName'])
                return str(due_date)
        return str(due_date)

    def get_due_date_list(self, allvoucher_data):
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
        print("save_purchase")
        logging.info("Save Payload. length= %s",len(purchase_list))
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


GB = Group()
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
            logging.info("SAVE PROCESS LEDGER")
        logging.info("Party ledger group created")


class ServerRequests:
    def __init__(self):
        self.authToken = None
        self.orgcode = None

    def verify_orgcode_authtoken(self, tabletype,urltype, Orgcode,authtoken):
        logging.info("ORGCODE %s", Orgcode)
        try:
            manageurl = url.format(tabletype,urltype,Orgcode)
            auth_url = "&accessToken={}".format(authtoken)
            request_url = manageurl + auth_url
            print(request_url)
            res = requests.post(request_url, headers={
                                'Content-Type': 'application/json'}, verify=False)
        except Exception as ex:
            logging.info(repr(ex))
            res = None
        # logging.info(res.json())
        # print(res.json()['reponseMessages'])
        if not res or res.status_code != 200:
            return False
        logging.info(res.json())
        print(res.json()['reponseMessages'])
        return res.json()['reponseMessages']
        # self.authToken = authtoken
        

    def get_data_to_server(self,filename):
        try:
            with open(filename) as json_file:
                payload = json.load(json_file)
                json_file.close()
                print("GET FROM SERVER")
                print(len(payload))

                if len(payload) >= 100:
                    return payload[:100]
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
                payload = self.get_data_to_server('purchase.json')
                pl_payload = self.get_data_to_server('p&l.json')
                
                print("get_payload")
                if not payload and pl_payload :
                    return True
                result1 = self.send_data_from_file('SalesSummary', 'Create',payload)
                result2 = self.send_data_from_file('AdvancePayment','Create',payload)
                result3 = self.send_data_from_file('AdvanceReceipt','Create', payload)
                result4 = self.send_data_from_file('ProfitAndLoss','Create',pl_payload)
                if result1 and result2 and result3 and result4:
                    print("data push to server")
                    logging.info("data pushed to server")
                    self.pop_from_list(payload,'purchase.json')
                    self.pop_from_list(pl_payload,'p&l.json')
            except Exception as ex:
                print(repr(ex))
                return False

    def send_data_from_file(self,tabletype,urltype,data):
        try:
            newdata = []
            if type == 'AdvancePayment' or type == 'AdvanceReceipt':
                for i in data:
                    i['mPaidAmount'] = None
                    newdata.append(i)
            if newdata:
                data = newdata

            payload = json.dumps(data)
            # print(data[0])
            manageurl = url.format(tabletype,urltype,remove_space(root.orgtext.get()))
            auth_url = "&accessToken={}".format(remove_space(root.authtext.get()))
            request_url = manageurl+auth_url
            res = requests.post(request_url, data=payload, headers={
                                'Content-Type': 'application/json'}, verify=False)
        except Exception as ex:
            print(repr(ex))
            res = None
        print(res)
        if not res or res.status_code != 200:
            print("RESPONSE FAIL")
            return False
        logger.info("Batch Data push to server")
        time.sleep(0.2)
        return True


SERVERPROCESS = ServerRequests()


class TextHandler(logging.Handler):
    """This class allows you to log to a tkinter Text or ScrolledText widget"""

    def __init__(self, text):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        link_Label = Label(root, text="ORGcode :", bg="#E8D579")
        # link_Label.place()

        link_Label.grid(row=1,column=0,padx=20,pady=10,ipady=1,sticky='w')

        root.orgtext = Entry(root ,width=100)
        # root.orgtext.pack(side=LEFT,ipadx=10,ipady=10)
        
        # root.orgtext.pack(fill='both')

        root.orgtext.grid(row=1, column=0,padx=120,pady=0,ipady=3)
        link_Label_auth = Label(root, text="AuthToken :", bg="#E8D579")
        # link_Label.place()

        link_Label_auth.grid(row=2,column=0,padx=20,pady=10,ipady=0,sticky='w')

        root.authtext = Entry(root ,width=100)
        root.authtext.grid(row=2, column=0,padx=120,pady=10,ipady=3)


        copyButton = Button(root, text="START", command=StartUI, width=15)
        # copyButton.pack(side=LEFT, padx=10,ipadx=5,ipady=5)
        copyButton.grid(row=3, column=0,pady=5,padx=100)
        self.text = text

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
    pattern = re.compile(r'\s+')
    return re.sub(pattern,'',text)

def StartUI():
    print(datetime.now())
    if remove_space(root.orgtext.get()) and remove_space(root.authtext.get()) == "":
        messagebox.showerror("Error!", "Please Enter OrgCode and AuthToken ")
        # root.orgtext.set("")
    else:
        logger.info("Get AuthToken Using Orgcode: %s", root.orgtext.get())
        Validationresult = SERVERPROCESS.verify_orgcode_authtoken('TokenGenerate','Validate',remove_space(root.orgtext.get()),remove_space(root.authtext.get()))
        if not Validationresult:
            logger.info("Connection Error please Try after some times")
            messagebox.askretrycancel("Message","Connection Error Please Try after some times")
            exit()
        elif not Validationresult == 'Success':
            logger.info("Invalid Access Token")
            messagebox.showerror("Error","Invalid Access Token or ORGCODE")
        else:
            messagebox.showinfo("Message","Token Verified Successfully")
            logger.info("AuthToken Verified")
    try:
        json_data = json.load(open('purchase.json'))
    except Exception as ex:
        print(repr(ex))
        json_data = None

    if json_data:
        print("data send to server before fetch")
        if SERVERPROCESS.start():
            messagebox.showinfo("Message","DATA PUSHED INTO ALL ENDPOINTS")
        else:
            print("false")
    else:
        print("NO data in json")    
       # data = json.load(open("purchase.json"))
       # print(data)
       # SERVERPROCESS.send_data_from_file(data)
    if not TALLYPROCESS.connection():
        messagebox.showerror(
            "Error!", "Open Tally and check odbc connection string")
        exit()

    result = TALLYPROCESS.get_company_name()
    if not result:
        messagebox.showerror("Error!", "Open Tally and Load company")
        logging.error("Open Tally and Load Company")
        # exit()
    else:
        if not messagebox.askokcancel("Confirm", "Are you sure to Fetch the Company:{}".format(TALLYPROCESS.company_name)):
            exit()
        logging.info("Opened {}".format(TALLYPROCESS.company_name))
        TALLYPROCESS.get_group_details()
        groupdata = GB.createjson()
        LG = LedgerGroup(groupdata)
        LG.process_ledger()
        logging.info("group details got")
        TALLYPROCESS.get_due_date_list(TALLYPROCESS.get_all_vouchers())
        my_purchase = TALLYPROCESS.get_my_purchase()
        logging.info("GET DATA FROM TALLY")
        # print(len(my_purchase))
        # print(my_purchase[0])
        
        if TALLYPROCESS.my_purchase_process(my_purchase):
        	print("data saved into tally")
        # json_data = json.load(open('purchase.json'))
        # payload = json_data[0]
        # print(payload)
        # SERVERPROCESS.send_data_from_file('SalesSummary',payload)
        # if SERVERPROCESS.start():
        # 	messagebox.showinfo("Message","All Data Push to server")
        # 	exit()

        # messagebox.showinfo("Message",root.orgtext.get())
        # authtoken.set("")
        # root.orgtext.set("")

    # root.update()
    # root.progress['value']=0
    # root.update()
    # while root.progress['value'] < 100:
    # 	root.progress['value'] += 10
    # 	# Keep updating the master object to redraw the progress bar
    # 	root.update()
    # 	time.sleep(0.5)
    # time.sleep(2)

    # messagebox.showinfo("Message","Successfully Loaded data")
    # root.destory()
    print(datetime.now())

root = tk.Tk()
root.geometry("820x620")
root.title("Tally_backup")
root.config(background="black")
st = ScrolledText(root, state='disabled')
# st.place()
st.grid(row=5,column=0,pady=10)

# Create textLogger
text_handler = TextHandler(st)
logging.basicConfig(filename='test.log',
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s')

global logger
# Add the handler to logger
logger = logging.getLogger()

logger.addHandler(text_handler)

# logger.info("Getting Group details")


# CreateWidgets()

root.mainloop()

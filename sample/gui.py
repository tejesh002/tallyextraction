# Importing necessary packages 
import shutil 
import tkinter as tk 
from tkinter import *
from tkinter import messagebox, filedialog 
from tkinter.ttk import Progressbar
import time
import pyodbc
from datetime import datetime, timedelta
import json
import requests
import json
import ssl
import urllib
ssl._create_default_https_context = ssl._create_unverified_context

conn=pyodbc.connect('DSN=TALLYODBC64_9000')
cursor = conn.cursor()
url = 'https://65.0.148.45:8181/erp/rest/dashboard/TokenGenerate/Create/?cmpCode=RGS&orgCode={}'

class TallyERP:
	def __init__(self):
		self.conn = None
		self.allvoucher_data = None
		self.my_purchase = None
		self.due_list=[]
		self.company_name = None

	def connection(self):
		try:
			self.conn = pyodbc.connect("DSN=TALLYODBC64_9000")
			return True
		except Exception:
			return False
	
	def get_company_name(self):
		try:
			result  = conn.execute('select $Name from company')
			data = result.fetchall()
			self.company_name = data[0][0]
			return self.company_name
		except Exception:
			return False

	def get_all_vouchers(self):
		try:
			allvoucher_result = cursor.execute("select $voucherNumber,$Date,$StockItemName,$BasicDueDateOfPymt,$PartyLedgerName from allvouchers")
			self.allvoucher_data = allvoucher_data.fetchall()
			return self.allvoucher_data
		except Exception:
			return False

	def get_my_purchase(self):
		try:
			result = cursor.execute("select $VoucherTypeName, $VoucherNumber, $Date, $PartyLedgerName,$STATENAME,$COUNTRYOFRESIDENCE,$DELIVERYCITY,$LedgerName, \
                    $StockItemName,$Discount,$Rate,$BilledQty,$SubAmount,$Led1,$AMT1,$Led2,$AMT2,$Led3,$AMT3,$Led4,$AMT4,$Led5,$AMT5,$Led6,$AMT6,$Led7,$AMT7,$Led8,$AMT8 from mypurchase")
			self.my_purchase = result.fetchall()
			return self.my_purchase
		except Exception:
			return False

	def my_purchase_process(self,my_purchase):
		purchase_list = []
		for data in my_purchase:
			payload = {
				'CompanyName':company_name,
				'vouchertypename':data[0],
				'vouchernumber':data[1],
				'txn_date' : str(data[2]),
				'partyname':data[3],
				'state':data[4],
				'country':data[5],
				'city':data[6],
				'mDes':data[7],
				'productname':data[8],
				'discount':data[9],
				'rate':data[10],
				'Billedqty':data[11],
				'Amount':data[12],
				'DUEDATE':self.get_due_date(data[2],data[1],data[3]),
				'ledger1':data[13],
				'amount1':data[14],
				'ledger2':data[15],
				'amount2':data[16],
				'ledger3':data[17],
				'amount3':data[18],
				'ledger4':data[19],
				'amount4':data[20],
				'ledger5':data[21],
				'amount5':data[22],
				'ledger6':data[23],
				'amount6':data[24],
				'ledger7':data[25],
				'amount7':data[26],
				'ledger8':data[27],
				'amount8':data[28]
			}
			purchase_list.append(payload)
		return purchase_list

	def get_due_date(self,txn_date,vouchernumber,ledgername):
		
		due_date = txn_date + timedelta(days=30)
		if not self.due_list:
			return str(due_date)
		for data in self.due_list:
			if str(txn_date)==data['Date'] and vouchernumber == data['voucherNumber'] and ledgername == data['LedgerName']:
				print("DueDate",data['BasicDueDateOfPymt'],data['Date'],data['voucherNumber'],data['LedgerName']) 
				return str(due_date)
		return str(due_date)

	def get_due_date_list(self,allvoucher_data):
		try:
			for data in allvoucher_data:
				if data[3]:
					payload = {
						'companyName':company_name,
						'voucherNumber':data[0],
						'Date':str(data[1]),
						'StockItemName':data[2],
						'BasicDueDateOfPymt':data[3],
						'LedgerName':data[4]
					}
					due_list.append(payload)
		except Exception:
			return False
	def save_purchase(purchase_list):
		with open("purchase.json","w+") as json_file:
			json_file.write(json.dumps(purchase_list,indent=4))

class ServerRequests:
	def __init__(self):
		self.authToken = None

	def get_auth_token(self,Orgcode):
		try:
			request_url = url.format(Orgcode)
			res =  requests.post(request_url,data={}, headers={'Content-Type': 'application/json'},verify=False)
		except Exception:
			res = None

		if not res or res.status_code!= 200:
			return False
		self.authToken = res.json()['accessToken']
		return True
	
def CreateWidgets(): 

	link_Label = Label(root, text ="Enter ORG code : ", 
					bg = "#E8D579") 
	link_Label.grid(row = 1, column = 0, 
					pady = 5, padx = 5) 
	
	root.orgtext = Entry(root, width = 50, 
							textvariable = get_org_code) 
 
	root.orgtext.grid(row = 1, column = 1, 
						pady = 5, padx = 5, 
						columnspan = 2)

	copyButton = Button(root, text ="start", 
						command = StartUI, width = 15) 
	copyButton.grid(row = 3, column = 1, 
					pady = 5, padx = 5) 
	

def StartUI(): 
	if authtoken.get()=="" and get_org_code.get()=="":
		messagebox.showerror("Error!","Enter authtoken and org_Code")
		authtoken.set("")
		get_org_code.set("")
	else:
		if not ServerRequests().get_auth_token(get_org_code.get()):
			messagebox.showerror("Message","Connection Error Please Try after some times")
		# else:
		# 	messagebox.showinfo("Message","AuthTokenGenerated SuccessFully")
		if not TallyERP().connection():
			messagebox.showerror("Error!","Open Tally and check odbc connection string")
		
		result = TallyERP().get_company_name()
		if not result:
			messagebox.showerror("Error!","Open Tally and Load company")
		else:
			if not messagebox.askokcancel("Confirm","Are you sure to Continue to this company "+ "result"):
				exit()
			TallyERP().get_due_date_list(TallyERP().get_all_vouchers())
			TallyERP().get_my_purchase
		
		# messagebox.showinfo("Message",get_org_code.get())
		authtoken.set("")
		get_org_code.set("")

	
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

root = tk.Tk()
root.geometry("830x120") 
root.title("Tally_backup") 
root.config(background = "black") 

authtoken = StringVar() 
get_org_code = StringVar()


CreateWidgets() 

root.mainloop() 

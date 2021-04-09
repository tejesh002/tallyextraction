import fiscalyear
from datetime import datetime
import re
import xmltodict
import codecs
import json
from settingsconfig import input_xml,output_xml,output_json
from database import DB

def respone_to_json(response_xml):
    try:
        with open(input_xml,'w') as xml_file:
            xml_file.write(response_xml)
            
        input_xml_data = open(input_xml)
        output_xml_data = open(output_xml,'w+')
        output_json_data = open(output_json,'w+')
        
        for line in input_xml_data:
            data = re.sub("&#4;"," ",line)
            output_xml_data.writelines(data)
        output_xml_data.close()
        input_xml_data.close()

        with codecs.open(output_xml,'r','utf-8')  as xml_file:
            root = xmltodict.parse(xml_file.read())
            json_dict = json.dumps(root,indent=4)
            output_json_data.write(json_dict)
        output_json_data.close()
        return True
    except Exception as ex:
        print("Exception response to json",ex)
        return False

def get_financial_year(finicial_year):
    # get the financial year 
    fiscalyear.setup_fiscal_calendar(start_month=4,start_day=1)
    current_year = fiscalyear.FiscalYear(finicial_year)
    FY_start, FY_end = current_year.start , current_year.end
    return FY_start,FY_end

def get_fiscal_year(txn_date):
        start,end_date = get_financial_year(txn_date.year)
        if txn_date >= end_date:
            FY = "{}-{}".format(end_date.year,end_date.year+1)
        elif txn_date <= end_date:
            FY = "{}-{}".format(end_date.year-1,end_date.year)
        else:
            FY= None  
        return FY
def metricdate(self,txndate):
        txdate_split = txndate.split("-")
        metricyear = int(txdate_split[0])+1
        # currentyear = datetime.now().year
        metricdate = "{}-{}-{}".format(metricyear,txdate_split[1],txdate_split[2])
        # print("txndate ",txndate)
        # print("metricdate",metricdate)
        return metricdate
def savetoDB(filepath):
    with open(filepath,'r') as jsonfile:
        data = json.load(jsonfile)
        jsonfile.close()
    return data

sales = 'salessummary.json'
ar = 'AR.json'
ap = 'AP.json'
pl = 'p&l.json'
path = "C:\\Users\\Cookie\\Documents\\tally\\tallyjsonbackup\\{}\\{}\\{}"

def salessummary():
    data = savetoDB(path.format('payagri','2019-20',sales))
    DB.conn.execute(DB.salessummary.insert(),data)
    data = savetoDB(path.format('bloom','2019-20',sales))
    DB.conn.execute(DB.salessummary.insert(),data)
    data = savetoDB(path.format('payagri','2020-21',sales))
    DB.conn.execute(DB.salessummary.insert(),data)
    data = savetoDB(path.format('bloom','2020-21',sales))
    DB.conn.execute(DB.salessummary.insert(),data)


def advrecepit():
    data = savetoDB(path.format('payagri','2019-20',ar))
    DB.conn.execute(DB.AR.insert(),data)
    data = savetoDB(path.format('bloom','2019-20',ar))
    DB.conn.execute(DB.AR.insert(),data)
    data = savetoDB(path.format('payagri','2020-21',ar))
    DB.conn.execute(DB.AR.insert(),data)
    data = savetoDB(path.format('bloom','2020-21',ar))
    DB.conn.execute(DB.AR.insert(),data)


def advpayment():
    data = savetoDB(path.format('payagri','2019-20',ap))
    DB.conn.execute(DB.AP.insert(),data)
    data = savetoDB(path.format('bloom','2019-20',ap))
    DB.conn.execute(DB.AP.insert(),data)
    data = savetoDB(path.format('payagri','2020-21',ap))
    DB.conn.execute(DB.AP.insert(),data)
    data = savetoDB(path.format('bloom','2020-21',ap))
    DB.conn.execute(DB.AP.insert(),data)


def profitandloss():
    data = savetoDB(path.format('payagri','2019-20',pl))
    DB.conn.execute(DB.PL.insert(),data)
    data = savetoDB(path.format('bloom','2019-20',pl))
    DB.conn.execute(DB.PL.insert(),data)
    data = savetoDB(path.format('payagri','2020-21',pl))
    DB.conn.execute(DB.PL.insert(),data)
    data = savetoDB(path.format('bloom','2020-21',pl))
    DB.conn.execute(DB.PL.insert(),data)

salessummary()
advpayment()
advrecepit()
profitandloss()
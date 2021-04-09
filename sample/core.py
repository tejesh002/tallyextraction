import os
import subprocess
import patoolib
import requests
import xmltodict
import json
import datetime
from xml.etree import ElementTree as ET
from utils import respone_to_json
from settingsconfig import TALLY_DATA_PATH, BACKUP_PATH , TALLY_REQUEST_URL,LOAD_TALLY,output_json,output_json_dump
from xml_request import GET_COMPANY_LIST,MASTER_REQUEST,VOUCHER_REQUEST,GET_COMPANY_LIST_PRIME
import fiscalyear
import codecs
import socket
from Tally_data import TALLY_DATA
from database import DB
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(process)d | %(levelname)s | %(message)s'
)

# from pymediainfo import MediaInfo

# ET.XML(response,[target='xml',encoding='utf-8'])

def extract_zip_to_folder(filename):
    patoolib.extract_archive(filename, outdir=TALLY_DATA_PATH)

def list_path():
    for filename in os.listdir(BACKUP_PATH):
        file_path = os.path.join(BACKUP_PATH,filename)
        extract_zip_to_folder(file_path)
        if open_tally(filename):
            delete_file(file_path)

def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

def check_tally_open():

    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as a_socket:
        return a_socket.connect_ex(('localhost',9000)) == 0
    
def open_tally(company):
    """
    "C:\\Program Files\\Tally.ERP9\\tally.exe" //NOGUI //NOINILOAD //LOAD:{}"
    """
    if not check_tally_open():
        try:
            subprocess.run(LOAD_TALLY.format(company),shell=True,timeout=10)
        except Exception:
            if check_tally_open:
                return True
            return Exception
    else:
        output = subprocess.check_output('''TASKKILL /F /IM tally.exe''',shell=True)
        open_tally(company)
        return output
    # output = check_output(LOAD_TALLY.format(company),shell=True)
    # os.system(LOAD_TALLY.format(company))

# list_path()


def request_tally(xml_list):
    """
    send the xml request to tally server
    """
    print("request start_time",datetime.datetime.now())
    headers = {'Content-Type': 'application/json'} # set what your server accepts
    response =  requests.post(TALLY_REQUEST_URL, data=xml_list, headers=headers).text
    print("request end_time",datetime.datetime.now())
    # response.iter_content
    # if not response:
    #     return None    
    return response


#print(response_data)

def get_company_name_from_xml_response(response_data,prime=False):
    """
     get the company name form the xml response
    """
    if prime:
        data = xmltodict.parse(response_data)
        return data['LISTOFCOMPANIES']['NAME']

    root = ET.fromstring(response_data)
    company_list = root.findall(".//COMPANYNAME.LIST")
    company_name = company_list[0].find("COMPANYNAME").text
    return company_name



def xml_string_to_file(xml_response,file_path):
    with open(file_path, "wb") as xml_file:
        for chunk in xml_response.iter_content(chunk_size=1024):
            xml_file.write(chunk)
        # data = ET.XML(xml_response)
        # xml_file.write(ET.tostring(data))


def get_current_financial_year(finicial_year = datetime.datetime.now().year):
    # get the financial year & default FY is Last 2 fiscalyear
    fiscalyear.setup_fiscal_calendar(start_month=4,start_day=1)
    current_year = fiscalyear.FiscalYear(finicial_year)
    # FY_start, FY_end = str(current_year.start.year)+current_year.start.strftime('%m')+current_year.start.strftime("%d") ,\
    #      str(current_year.end.year) + current_year.end.strftime('%m') + current_year.end.strftime('%d')
         
    return current_year

def convert_xml_to_json(xml_file,json_file=None,json_flag=False):
    with codecs.open(xml_file,'r','utf-16')  as xml_file:
        data_dict = xmltodict.parse(xml_file.read())
        json_dict = json.dumps(data_dict,indent=4)
    
    if json_flag:
        return json_dict

    with open(json_file,"w+") as json_data:
        json_data.write(json_dict)

def core_process():
    company_list = request_tally(GET_COMPANY_LIST_PRIME)
    company_name = get_company_name_from_xml_response(company_list,prime=True)
    respone = get_current_financial_year()
    difference_date = respone.start - respone.end
    if respone.end > datetime.datetime.now():
        difference_date = respone.start - datetime.datetime.now()
    difference_days = abs(difference_date.days)
    # difference_days = 90
    print(difference_days)

    for data in range(0,difference_days,2):
        end_date = respone.start + datetime.timedelta(days=data+1)
        start_date = respone.start +datetime.timedelta(days=data)
        FY_start,FY_end = str(start_date.year)+start_date.strftime('%m')+start_date.strftime('%d'), \
            str(end_date.year)+end_date.strftime('%m')+end_date.strftime('%d')
        print("start date={},end_date={}".format(start_date,end_date))
        voucher_response = request_tally(VOUCHER_REQUEST.format(company_name,FY_start,FY_end))
        response = respone_to_json(voucher_response)
        if respone:
            TALLY_DATA.start(output_json,output_json_dump)
            inventory_list,ledger_list = DB.insert_table()
            if inventory_list:
                DB.conn.execute(DB.inventory_table_obj.insert(),inventory_list)
            else:
                print("NO INVENTORY DATA")
            if ledger_list:
                DB.conn.execute(DB.ledger_table_obj.insert(),ledger_list)
            else:
                print("NO LEDGER DATA")
            print("data inserted to db")
    # print(company_name)
    # print(respone)

def single_process(FY_start,FY_end):
    company_list = request_tally(GET_COMPANY_LIST_PRIME)
    company_name = get_company_name_from_xml_response(company_list,prime=True)
    # respone = get_current_financial_year()
    # difference_date = respone.start - respone.end
    # if respone.end > datetime.datetime.now():
    #     difference_date = respone.start - datetime.datetime.now()
    # difference_days = abs(difference_date.days)
    # print(difference_days)

    # for data in range(0,difference_days,2):
    #     end_date = respone.start + datetime.timedelta(days=data+1)
    #     start_date = respone.start +datetime.timedelta(days=data)
    #     FY_start,FY_end = str(start_date.year)+start_date.strftime('%m')+start_date.strftime('%d'), \
    #         str(end_date.year)+end_date.strftime('%m')+end_date.strftime('%d')
    #     print("start date={},end_date={}".format(start_date,end_date))
    voucher_response = request_tally(VOUCHER_REQUEST.format(company_name,FY_start,FY_end))
    response = respone_to_json(voucher_response)
    if response:
        TALLY_DATA.start(output_json,output_json_dump)
        inventory_list,ledger_list = DB.insert_table()
        DB.conn.execute(DB.inventory_table_obj.insert(),inventory_list)
        DB.conn.execute(DB.ledger_table_obj.insert(),ledger_list)
        print("data inserted to db")

# single_process(20190413,20190414)
# core_process()
# print(get_current_financial_year())
# print(datetime.datetime.now().isoformat())
# # print(company_name)
# # start,end = get_current_financial_year()
# # print(start,end)

# voucher_response = request_tally(VOUCHER_REQUEST.format(company_name,20190401,20200331))
# respone_to_json(voucher_response)
# print(datetime.datetime.now().isoformat())
# xml_string_to_file(voucher_response,"/xml/new_voucher.xml")

# convert_xml_to_json("master.xml","master.json")

# response_data = request_tally(GET_COMPANY_LIST)
# company_name = get_company_name_from_xml_response(response_data)
# master_response = request_tally(MASTER_REQUEST.format(company_name))


# root = ET.XML(master_response,[target='xml',encoding='utf-8'])
# root = ET.XML(master_response)
# media = MediaInfo.parse(master_response)


# xmltodict = xmltodict.parse(master_response,encoding='utf-8')

# root = fromstring(master_response)

# from xmljson import badgerfish as bf

# from xml.etree.ElementTree import fromstring
# df_data = bf.data(fromstring(master_response))

#python core.py >> tallyerp.log 2>&1 &
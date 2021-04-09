import os
TALLY_DATA_PATH="C:\\Users\\Public\\Tally.ERP9\\Data"
BACKUP_PATH = os.getcwd()+"\\backup"
MASTER_RESPONSE_PATH = os.getcwd()+"\\xml\\master_response.xml"
VOUCHER_RESPONSE_PATH = os.getcwd()+"\\xml\\voucher_response.xml"
TALLY_REQUEST_URL = 'http://localhost:9000'
SCENARIO = {}
LOAD_TALLY = '''"C:\\Program Files\\Tally.ERP9\\tally.exe" /NOGUI /NOINILOAD /LOAD:{}'''
input_xml = "data_files\\input_xml.xml"
output_xml = "data_files\\output_xml.xml"
output_json = "data_files\\output_json.json"
output_json_dump = "data_files\\output_json_dump.json"
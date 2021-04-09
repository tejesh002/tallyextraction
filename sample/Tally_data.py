import json
from datetime import datetime, timedelta
from utils import get_financial_year,get_fiscal_year


# input_file='single_voucher_sales.json'
# json_files = open(input_file) 
# voucher_data = json.load(json_files)
# json_files.close()

# import_data = voucher_data['ENVELOPE']['BODY']['IMPORTDATA'] \
#     ['REQUESTDATA']['TALLYMESSAGE']


class Tally:
    def __init__(self):
        pass

    def start(self,input_file,output_file):
        json_files = open(input_file) 
        voucher_data = json.load(json_files)
        json_files.close()

        import_data = voucher_data['ENVELOPE']['BODY']['IMPORTDATA'] \
            ['REQUESTDATA']['TALLYMESSAGE']
        # return import_data

        ledger_list,inventory_payload = self.save_data(import_data)
        
        payload = {"LEDGER_DATA":ledger_list,"INVENTORY_DATA":inventory_payload}
        
        with open(output_file,'w') as json_file:
            json_file.write(json.dumps(payload,indent=4))
        return True

    
    def save_data(self,import_data):
        ledger_list = []
        inventory_list = []
        for data in import_data:
            if 'VOUCHER' in data:
                M_TYPE = self.get_m_type(data)
                M_STATE = self.get_m_state(data)
                M_COUNTRY = self.get_m_country(data)
                M_CITY = self.get_m_city(data)
                M_PARTY_NAME = self.get_m_party_name(data)
                TXN_DATE = self.get_txn_date(data)
                FY_YEAR = get_fiscal_year(TXN_DATE)
                VOUCHER_NUMBER =self.get_voucher_number(data)
                DUE_DATE = self.get_m_due_date(data,TXN_DATE)
                INVENTRY_DATA = self.get_inventry_list(data)
                LEDGER_DATA = self.get_ledger_details(data)
                IS_DISCOUNT = self.get_is_discount(data)
                DISCOUNT = None
                if LEDGER_DATA:
                    # print(len(LEDGER_DATA))
                    for index,ledger in enumerate(LEDGER_DATA):
                        M_DESC = self.get_m_desc(ledger)
                        IS_COMPANY = True if index==0 else False
                        LEDGER_AMOUNT = self.get_m_price(ledger)
                        ledger_payload = {
                            "M_TYPE":M_TYPE,
                            "M_STATE":M_STATE,
                            "M_COUNTRY":M_COUNTRY,
                            "M_CITY":M_CITY,
                            "M_PARTY_NAME":M_PARTY_NAME,
                            "TXN_DATE":str(TXN_DATE),
                            "DUE_DATE":str(DUE_DATE),
                            "DAY_OF_MONTH":TXN_DATE.month if TXN_DATE else None,
                            "MONTH_OF_YEAR":TXN_DATE.year if TXN_DATE else None,
                            "DAY_OF_YEAR":TXN_DATE.day if TXN_DATE else None,
                            "FY_YEAR":FY_YEAR,
                            "VOUCHERNUMBER":VOUCHER_NUMBER,
                            "M_DESC":M_DESC,
                            "IS_COMPANY":IS_COMPANY,
                            "LEDGER_AMOUNT":LEDGER_AMOUNT
                        }
                        print("LEDGER_DATA",ledger_payload)
                        ledger_list.append(ledger_payload)
                
                if INVENTRY_DATA:
                    # print("LENGTH",len(INVENTRY_DATA))         
                    for inventory in INVENTRY_DATA:
                        PRODUCT_NAME = self.get_product_name(inventory)
                        QUANTITY, UOM = self.get_quantity(inventory)
                        RATE = self.get_inventory_rate(inventory)
                        AMOUNT = self.get_inventory_amount(inventory)
                        if IS_DISCOUNT:
                            DISCOUNT = self.get_discount(inventory)
                        inventory_payload = {
                            "M_TYPE":M_TYPE,
                            "TXN_DATE":str(TXN_DATE),
                            "DAY_OF_MONTH":TXN_DATE.month if TXN_DATE else None,
                            "MONTH_OF_YEAR":TXN_DATE.year if TXN_DATE else None,
                            "DAY_OF_YEAR":TXN_DATE.day if TXN_DATE else None,
                            "VOUCHERNUMBER":VOUCHER_NUMBER,
                            "PRODUCTNAME":PRODUCT_NAME,
                            "QUANTITY":QUANTITY,
                            "QUANTITY_UNIT":UOM,
                            "RATE":RATE,
                            "DISCOUNT":DISCOUNT,
                            "AMOUNT":AMOUNT,
                            "CGST":None,
                            "SGST":None,
                            "IGST":None
                        }
                        print("INVENTORY_PAYLOAD",inventory_payload)
                        inventory_list.append(inventory_payload)
                        
        return ledger_list,inventory_list

    def get_m_type(self,tally_data):
        try:
            return tally_data['VOUCHER']['VOUCHERTYPENAME']
        except KeyError:
            return None
        except Exception as e:
            # print(repr(e))
            return None
        
    def get_m_state(self,tally_data):
        try:
            return tally_data['VOUCHER']['STATENAME']
        except KeyError:
            return None
        except Exception as e:
            # print(repr(e))
            return None
        
    def get_m_country(self,tally_data):
        try:
            return tally_data['VOUCHER']['COUNTRYOFRESIDENCE']
        except KeyError:
            return None
        except Exception as e:
            # print(repr(e))
            return None

    def get_m_city(self,tally_data):
        try:
            return tally_data['VOUCHER']['DELIVERYCITY']
        except KeyError:
            return None
        except Exception as e:
            # print(repr(e))
            return None
    
    def get_m_party_name(self,tally_data):
        try:
            return tally_data['VOUCHER']['PARTYLEDGERNAME']
        except KeyError:
            return None
        except Exception as e:
            # print(repr(e))
            return None
        
    def get_m_desc(self,tally_data):
        try:
            return tally_data['LEDGERNAME']
        except KeyError:
            return None
        except Exception as e:
            # print(repr(e))
            return None
    
    def get_m_due_date(self,tally_data,txn_date):

        self.due_date = txn_date + timedelta(days=30)

        if "BASICDUEDATEOFPYMT" in tally_data['VOUCHER']:
            due_date = tally_data['VOUCHER']['BASICDUEDATEOFPYMT']

            if not due_date:
                return self.due_date
            try:
                due_days = int(due_date.split("Days")[0])
                self.due_date = txn_date + timedelta(days=due_days)
            except ValueError:
                return self.due_date
            except Exception:
                due_days = datetime.strptime(due_date,'%d-%b-%Y')
                self.due_date = txn_date + timedelta(days=due_days.day)
            
            return self.due_date
        else:
            return self.due_date
    
    def get_txn_date(self,tally_data):
        try:
            basicdatetime = tally_data['VOUCHER']['BASICDATETIMEOFINVOICE']
            if basicdatetime:
                date = datetime.strptime(basicdatetime,'%d-%b-%Y at %H:%M')
            else:
                date_time = tally_data['VOUCHER']['DATE']
                if not datetime:
                    return None
                date = datetime.strptime(date_time,'%Y%m%d')
            return date
        except KeyError:
            date_time = tally_data['VOUCHER']['DATE']
            if not datetime:
                return None
            date = datetime.strptime(date_time,'%Y%m%d')
            return date
        except Exception as e:
            # print(repr(e))
            return None
    
    def get_voucher_number(self,tally_data):
        try:
            return tally_data['VOUCHER']["VOUCHERNUMBER"]
        except KeyError:
            return None
        except Exception as e:
            # print(repr(e))
            return None
    
    def get_ledger_details(self,tally_data):
        try:
            if "ALLLEDGERENTRIES.LIST" in tally_data['VOUCHER']:
                ledger_list = tally_data['VOUCHER']['ALLLEDGERENTRIES.LIST']
            elif "LEDGERENTRIES.LIST" in tally_data['VOUCHER']:
                ledger_list = tally_data['VOUCHER']['LEDGERENTRIES.LIST']
            else:
                ledger_list = []
            if type(ledger_list) == dict:
                return [ledger_list]
            return ledger_list
        except KeyError:
            return None
        except TypeError:
            return None
        except Exception as e:
            # print(repr(e))
            return None
            
    def get_inventry_list(self,tally_data):
        try:
            if "INVENTORYENTRIES.LIST" in tally_data['VOUCHER']:
                inventory_list = tally_data['VOUCHER']['INVENTORYENTRIES.LIST']
            elif "ALLINVENTORYENTRIES.LIST" in tally_data['VOUCHER']:
                inventory_list = tally_data['VOUCHER']['ALLINVENTORYENTRIES.LIST']
            else:
                inventory_list = []
            if type(inventory_list) == dict:
                return [inventory_list]
            return inventory_list
        except KeyError:
            return None
        except TypeError:
            return None
        except Exception as e:
            # print(repr(e))
            return None

    def get_m_price(self,tally_data):
        try:
            return tally_data['AMOUNT']
        except KeyError:
            return None
        except Exception as e:
            # print(repr(e))
            return None
    
    def get_product_name(self,tally_data):
        try:
            return tally_data['STOCKITEMNAME']
        except KeyError:
            return None
        except Exception as e:
            # print(repr(e))
            return None
    
    def get_quantity(self,tally_data):
        try:
            quantity = tally_data['BILLEDQTY']
            qty = quantity.split(" ")
            return qty[0],qty[1]
        except KeyError:
            return None, None
        except Exception as e:
            # print(repr(e))
            return None,None
        
    def get_inventory_rate(self,tally_data):
        try:
            rate = tally_data["RATE"]
            return rate.split("/")[0]
        except KeyError:
            return None
        except Exception as e:
            # print(repr(e))
            return None
    
    def get_inventory_amount(self,tally_data):
        try:
            return tally_data["AMOUNT"]
        except KeyError:
            return None
        except Exception as e:
            # print(repr(e))
            return None
    
    def get_discount(self,tally_data):
        try:
            if "DISCOUNT" in tally_data:
                return tally_data["DISCOUNT"]
            return None
        except KeyError:
            return None
        except Exception as e:
            # print(repr(e))
            return None
        
    def get_is_discount(self,tally_data):
        try:
            IS_DISCOUNT = tally_data['VOUCHER']['HASDISCOUNTS']
            if IS_DISCOUNT == 'Yes':
                return True
            return False
        except KeyError:
            return None
        except Exception as e:
            # print(repr(e))
            return None

TALLY_DATA=Tally()
# TALLY_DATA.start('jsons\\inputjson\\selectmarketing.json','jsons\\outputjson\\selectmarketingdump.json')

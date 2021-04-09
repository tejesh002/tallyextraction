from sqlalchemy import create_engine
from sqlalchemy import Table , MetaData, Column, Integer, VARCHAR, String, DATETIME, DECIMAL, BOOLEAN
from sqlalchemy.engine.url import URL
import json
import logging
# from settingsconfig import output_json_dump

# logging.basicConfig(filename="db.log",filemode="w",format='%(name)s - %(levelname)s - %(message)s')
class Database():

    def __init__(self):
        self.url = URL('mysql','root','root','localhost',3306,database='tallyerp')
        self.sqlite = 'sqlite:///mypurchase.sqlite'
        self.engine = create_engine(self.url)
        self.conn = self.engine.connect()
        self.meta = MetaData()
        self.ledger_table_obj = None
        self.inventory_table_obj = None
        self.count=0
        # self.inventory_table_dump()
        # self.ledger_table_dump()
        self.salessummary()
        self.AP()
        self.AR()
        self.PL()
        self.create_table()
        

    def insert_table(self):
        
        with open(output_json_dump) as json_file:
            json_data = json.load(json_file)
            inventory_list = json_data['INVENTORY_DATA']
            ledger_list = json_data['LEDGER_DATA']
            # self.inventory_insert(inventory_list)
            # self.ledger_insert(ledger_list)
            # inventory_insert = self.inventory_table_obj.insert().values(inventory_list)
            # ledger_insert = self.ledger_table_obj.insert().values(ledger_list)
            # self.conn.execute(inventory_insert)
            # self.conn.execute(ledger_insert)        
        return inventory_list,ledger_list

    def inventory_insert(self,inventory_list):
        count = 0
        for inventory in inventory_list:
            try:   
                insert_data = self.inventory_table_obj.insert().values(
                    M_TYPE=inventory['M_TYPE'],
                    TXN_DATE=inventory['TXN_DATE'],
                    DAY_OF_MONTH=inventory['DAY_OF_MONTH'],
                    MONTH_OF_YEAR=inventory['MONTH_OF_YEAR'],
                    DAY_OF_YEAR=inventory['DAY_OF_YEAR'],
                    PRODUCTNAME=inventory['PRODUCTNAME'],
                    VOUCHERNUMBER=inventory['VOUCHERNUMBER'],
                    QUANTITY=inventory['QUANTITY'],
                    QUANTITY_UNIT=inventory['QUANTITY_UNIT'],
                    RATE=inventory['RATE'],
                    AMOUNT=inventory['AMOUNT'],
                    CGST=inventory['CGST'],
                    SGST=inventory['SGST'],
                    IGST=inventory['IGST']
                )
                self.conn.execute(insert_data)
                count = count+1
                print("data inserted",count)
                # logging.info("INSERTED DATA %s",inventory)
            except Exception as ex:
                print(ex)
                # logging.info('Error occur while insert data in inventory %s',ex)

    def ledger_insert(self,ledger_list):

        for ledger in ledger_list:
            try:
                count = 0
                insert_data = self.ledger_table_obj.insert().values(
                    M_TYPE=ledger['M_TYPE'],
                    M_STATE=ledger['M_STATE'],
                    M_CITY=ledger['M_CITY'],
                    M_COUNTRY = ledger['M_COUNTRY'],
                    M_PARTY_NAME = ledger['M_PARTY_NAME'],
                    TXN_DATE = ledger['TXN_DATE'],
                    DUE_DATE = ledger['DUE_DATE'],
                    DAY_OF_MONTH=ledger['DAY_OF_MONTH'],
                    MONTH_OF_YEAR=ledger['MONTH_OF_YEAR'],
                    DAY_OF_YEAR=ledger['DAY_OF_YEAR'],
                    FY_YEAR=ledger['FY_YEAR'],
                    VOUCHERNUMBER=ledger['VOUCHERNUMBER'],
                    M_DESC=ledger['M_DESC'],
                    LEDGER_AMOUNT=ledger['LEDGER_AMOUNT']
                )
                self.conn.execute(insert_data)
                count = count +1
                print("Data inserted",count)
                # logging.info("INSERTED DATA %s",ledger)
            except Exception as ex:
                print(ex)
                # logging.info("Erro occur while insert DB %s",ex)
    
    def create_table(self):
        self.meta.create_all(self.engine)

    def inventory_table_dump(self):
        self.inventory_table_obj = Table(
            'inventory_table_dump', self.meta,
            Column("S_NO",Integer(),primary_key=True),
            Column("M_TYPE",VARCHAR(200),server_default=None),
            Column("TXN_DATE", VARCHAR(200),server_default=None),
            Column("DAY_OF_MONTH", Integer(),server_default=None),
            Column("MONTH_OF_YEAR", Integer(),server_default=None),
            Column("DAY_OF_YEAR", Integer(),server_default=None),
            Column("VOUCHERNUMBER", VARCHAR(200),server_default=None),
            Column("PRODUCTNAME", VARCHAR(200),server_default=None),
            Column("QUANTITY", DECIMAL(10,2),server_default=None),
            Column("QUANTITY_UNIT", VARCHAR(200),server_default=None),
            Column("RATE", DECIMAL(10,2),server_default=None),
            Column("DISCOUNT", DECIMAL(10,2),server_default=None),
            Column("AMOUNT", DECIMAL(10,2),server_default=None),
            Column("CGST",VARCHAR(200),server_default=None),
            Column("SGST",VARCHAR(200),server_default=None),
            Column("IGST",VARCHAR(200),server_default=None), 
        )
        
    def ledger_table_dump(self):
        self.ledger_table_obj = Table(
            "ledger_table_dump",self.meta,
            Column("S_NO",Integer(),primary_key=True),
            Column("M_TYPE",VARCHAR(200),server_default=None),
            Column("M_STATE",VARCHAR(200),server_default=None),
            Column("M_COUNTRY", VARCHAR(200),server_default=None),
            Column("M_CITY", VARCHAR(200),server_default=None),
            Column("M_PARTY_NAME", VARCHAR(200),server_default=None),
            Column("TXN_DATE", VARCHAR(200),server_default=None),
            Column("DUE_DATE", VARCHAR(200),server_default=None),
            Column("DAY_OF_MONTH", Integer(),server_default=None),
            Column("MONTH_OF_YEAR", Integer(),server_default=None),
            Column("DAY_OF_YEAR", Integer(),server_default=None),
            Column("FY_YEAR",VARCHAR(200),server_default=None),
            Column("VOUCHERNUMBER",VARCHAR(200),server_default=None),
            Column("M_DESC",VARCHAR(200),server_default=None),
            Column("IS_COMPANY",BOOLEAN()),
            Column("LEDGER_AMOUNT",DECIMAL(10,2),server_default=None)
        )
    def salessummary(self):
        self.salessummary = Table(
            "salessummary",self.meta,
            Column("orgCode",VARCHAR(200),server_default=None),
            Column("cmpCode",VARCHAR(200),server_default=None),
            Column("companyName",VARCHAR(200),server_default=None),
            Column("fyYear",VARCHAR(200),server_default=None),
            Column("scenario",VARCHAR(200),server_default=None),
            Column("dashboardType",VARCHAR(200),server_default=None),
            Column("metricType", VARCHAR(200),server_default=None),
            Column("txnDate", VARCHAR(200),server_default=None),
            Column("dayOfMonth", VARCHAR(200),server_default=None),
            Column("monthOfYear", VARCHAR(200),server_default=None),
            Column("dayOfYear", VARCHAR(200),server_default=None),
            Column("metricDate", VARCHAR(200),server_default=None),
            Column("dueDate", VARCHAR(200),server_default=None),
            Column("mId", VARCHAR(200),server_default=None),
            Column("mPartyCode",VARCHAR(200),server_default=None),
            Column("mPartyName",VARCHAR(200),server_default=None),
            Column("mPcode",VARCHAR(200),server_default=None),
            Column("mDesc",VARCHAR(200),server_default=None),
            Column("mQty",VARCHAR(200),server_default=None),
            Column("mUnitPrice",VARCHAR(200),server_default=None),
            Column("mDiscount",VARCHAR(200),server_default=None),
            Column("mGST",VARCHAR(200),server_default=None),
            Column("mTotalPrice",VARCHAR(200),server_default=None),
            Column("mLedger1",VARCHAR(200),server_default=None),
            Column("mLedgerAmt1",VARCHAR(200),server_default=None),
            Column("mLedger2",VARCHAR(200),server_default=None),
            Column("mLedgerAmt2",VARCHAR(200),server_default=None),
            Column("mledger3",VARCHAR(200),server_default=None),
            Column("mLedgerAmt3",VARCHAR(200),server_default=None),
            Column("mledger4",VARCHAR(200),server_default=None),
            Column("mLedgerAmt4",VARCHAR(200),server_default=None),
            Column("mledger5",VARCHAR(200),server_default=None),
            Column("mLedgerAmt5",VARCHAR(200),server_default=None),
            Column("mledger6",VARCHAR(200),server_default=None),
            Column("mLedgerAmt6",VARCHAR(200),server_default=None),
            Column("mledger7",VARCHAR(200),server_default=None),
            Column("mLedgerAmt7",VARCHAR(200),server_default=None),
            Column("mledger8",VARCHAR(200),server_default=None),
            Column("mLedgerAmt8",VARCHAR(200),server_default=None),
            Column("mTotalAmount",VARCHAR(200),server_default=None),
            Column("mState",VARCHAR(200),server_default=None),
            Column("mCity",VARCHAR(200),server_default=None),
            Column("mCountry",VARCHAR(200),server_default=None),
               
        )
    def PL(self):
        self.PL = Table(
            "pl",self.meta,
            Column("orgCode",VARCHAR(200),server_default=None),
            Column("cmpCode",VARCHAR(200),server_default=None),
            Column("companyName",VARCHAR(200),server_default=None),
            Column("fyYear",VARCHAR(200),server_default=None),
            Column("scenario",VARCHAR(200),server_default=None),
            Column("dashboardType",VARCHAR(200),server_default=None),
            Column("metricType", VARCHAR(200),server_default=None),
            Column("txnDate", VARCHAR(200),server_default=None),
            Column("dayOfMonth", VARCHAR(200),server_default=None),
            Column("monthOfYear", VARCHAR(200),server_default=None),
            Column("dayOfYear", VARCHAR(200),server_default=None),
            Column("metricDate", VARCHAR(200),server_default=None),
            Column("mId", VARCHAR(200),server_default=None),
            Column("mPartyName",VARCHAR(200),server_default=None),
            Column("mDesc",VARCHAR(200),server_default=None),
            Column("mQty",VARCHAR(200),server_default=None),
            Column("mUnitPrice",VARCHAR(200),server_default=None),
            Column("mDiscount",VARCHAR(200),server_default=None),
            Column("mTotalPrice",VARCHAR(200),server_default=None),
            Column("mTotalAmount",VARCHAR(200),server_default=None),
            Column("mState",VARCHAR(200),server_default=None),
            Column("mCity",VARCHAR(200),server_default=None),
            Column("mCountry",VARCHAR(200),server_default=None), 
            Column("mLedger1",VARCHAR(200),server_default=None),
            Column("mLegder1group1",VARCHAR(200),server_default=None),
            Column("mLegder1group2",VARCHAR(200),server_default=None),
            Column("mLegder1group3",VARCHAR(200),server_default=None),
            Column("mLegder1group4",VARCHAR(200),server_default=None),
            Column("mLegder1group5",VARCHAR(200),server_default=None),
            Column("mLedgerAmt1",VARCHAR(200),server_default=None),
            Column("mLedger2",VARCHAR(200),server_default=None),
            Column("mLegder2group1",VARCHAR(200),server_default=None),
            Column("mLegder2group2",VARCHAR(200),server_default=None),
            Column("mLegder2group3",VARCHAR(200),server_default=None),
            Column("mLegder2group4",VARCHAR(200),server_default=None),
            Column("mLegder2group5",VARCHAR(200),server_default=None),
            Column("mLedgerAmt2",VARCHAR(200),server_default=None),
            Column("mLedger3",VARCHAR(200),server_default=None),
            Column("mLegder3group1",VARCHAR(200),server_default=None),
            Column("mLegder3group2",VARCHAR(200),server_default=None),
            Column("mLegder3group3",VARCHAR(200),server_default=None),
            Column("mLegder3group4",VARCHAR(200),server_default=None),
            Column("mLegder3group5",VARCHAR(200),server_default=None),
            Column("mLedgerAmt3",VARCHAR(200),server_default=None),
            Column("mLedger4",VARCHAR(200),server_default=None),
            Column("mLegder4group1",VARCHAR(200),server_default=None),
            Column("mLegder4group2",VARCHAR(200),server_default=None),
            Column("mLegder4group3",VARCHAR(200),server_default=None),
            Column("mLegder4group4",VARCHAR(200),server_default=None),
            Column("mLegder4group5",VARCHAR(200),server_default=None),
            Column("mLedgerAmt4",VARCHAR(200),server_default=None),
            Column("mLedger5",VARCHAR(200),server_default=None),
            Column("mLegder5group1",VARCHAR(200),server_default=None),
            Column("mLegder5group2",VARCHAR(200),server_default=None),
            Column("mLegder5group3",VARCHAR(200),server_default=None),
            Column("mLegder5group4",VARCHAR(200),server_default=None),
            Column("mLegder5group5",VARCHAR(200),server_default=None),
            Column("mLedgerAmt5",VARCHAR(200),server_default=None),
            Column("mLedger6",VARCHAR(200),server_default=None),
            Column("mLegder6group1",VARCHAR(200),server_default=None),
            Column("mLegder6group2",VARCHAR(200),server_default=None),
            Column("mLegder6group3",VARCHAR(200),server_default=None),
            Column("mLegder6group4",VARCHAR(200),server_default=None),
            Column("mLegder6group5",VARCHAR(200),server_default=None),
            Column("mLedgerAmt6",VARCHAR(200),server_default=None),
            Column("mLedger7",VARCHAR(200),server_default=None),
            Column("mLegder7group1",VARCHAR(200),server_default=None),
            Column("mLegder7group2",VARCHAR(200),server_default=None),
            Column("mLegder7group3",VARCHAR(200),server_default=None),
            Column("mLegder7group4",VARCHAR(200),server_default=None),
            Column("mLegder7group5",VARCHAR(200),server_default=None),
            Column("mLedgerAmt7",VARCHAR(200),server_default=None),
            Column("mLedger8",VARCHAR(200),server_default=None),
            Column("mLegder8group1",VARCHAR(200),server_default=None),
            Column("mLegder8group2",VARCHAR(200),server_default=None),
            Column("mLegder8group3",VARCHAR(200),server_default=None),
            Column("mLegder8group4",VARCHAR(200),server_default=None),
            Column("mLegder8group5",VARCHAR(200),server_default=None),
            Column("mLedgerAmt8",VARCHAR(200),server_default=None),
             
        )
    def AP(self):
        self.AP = Table(
            "AP",self.meta,
            Column("orgCode",VARCHAR(200),server_default=None),
            Column("cmpCode",VARCHAR(200),server_default=None),
            Column("companyName",VARCHAR(200),server_default=None),
            Column("fyYear",VARCHAR(200),server_default=None),
            Column("scenario",VARCHAR(200),server_default=None),
            Column("dashboardType",VARCHAR(200),server_default=None),
            Column("metricType", VARCHAR(200),server_default=None),
            Column("txnDate", VARCHAR(200),server_default=None),
            Column("dayOfMonth", VARCHAR(200),server_default=None),
            Column("monthOfYear", VARCHAR(200),server_default=None),
            Column("dayOfYear", VARCHAR(200),server_default=None),
            Column("metricDate", VARCHAR(200),server_default=None),
            Column("dueDate", VARCHAR(200),server_default=None),
            Column("mId", VARCHAR(200),server_default=None),
            Column("mPartyCode",VARCHAR(200),server_default=None),
            Column("mPartyName",VARCHAR(200),server_default=None),
            Column("mPcode",VARCHAR(200),server_default=None),
            Column("mDesc",VARCHAR(200),server_default=None),
            Column("mQty",VARCHAR(200),server_default=None),
            Column("mUnitPrice",VARCHAR(200),server_default=None),
            Column("mDiscount",VARCHAR(200),server_default=None),
            Column("mGST",VARCHAR(200),server_default=None),
            Column("mTotalPrice",VARCHAR(200),server_default=None),
            Column("mLedger1",VARCHAR(200),server_default=None),
            Column("mLedgerAmt1",VARCHAR(200),server_default=None),
            Column("mLedger2",VARCHAR(200),server_default=None),
            Column("mLedgerAmt2",VARCHAR(200),server_default=None),
            Column("mledger3",VARCHAR(200),server_default=None),
            Column("mLedgerAmt3",VARCHAR(200),server_default=None),
            Column("mledger4",VARCHAR(200),server_default=None),
            Column("mLedgerAmt4",VARCHAR(200),server_default=None),
            Column("mledger5",VARCHAR(200),server_default=None),
            Column("mLedgerAmt5",VARCHAR(200),server_default=None),
            Column("mledger6",VARCHAR(200),server_default=None),
            Column("mLedgerAmt6",VARCHAR(200),server_default=None),
            Column("mledger7",VARCHAR(200),server_default=None),
            Column("mLedgerAmt7",VARCHAR(200),server_default=None),
            Column("mledger8",VARCHAR(200),server_default=None),
            Column("mLedgerAmt8",VARCHAR(200),server_default=None),
            Column("mTotalAmount",VARCHAR(200),server_default=None),
            Column("mState",VARCHAR(200),server_default=None),
            Column("mCity",VARCHAR(200),server_default=None),
            Column("mCountry",VARCHAR(200),server_default=None),
               
        )
    def AR(self):
        self.AR = Table(
            "AR",self.meta,
            Column("orgCode",VARCHAR(200),server_default=None),
            Column("cmpCode",VARCHAR(200),server_default=None),
            Column("companyName",VARCHAR(200),server_default=None),
            Column("fyYear",VARCHAR(200),server_default=None),
            Column("scenario",VARCHAR(200),server_default=None),
            Column("dashboardType",VARCHAR(200),server_default=None),
            Column("metricType", VARCHAR(200),server_default=None),
            Column("txnDate", VARCHAR(200),server_default=None),
            Column("dayOfMonth", VARCHAR(200),server_default=None),
            Column("monthOfYear", VARCHAR(200),server_default=None),
            Column("dayOfYear", VARCHAR(200),server_default=None),
            Column("metricDate", VARCHAR(200),server_default=None),
            Column("dueDate", VARCHAR(200),server_default=None),
            Column("mId", VARCHAR(200),server_default=None),
            Column("mPartyCode",VARCHAR(200),server_default=None),
            Column("mPartyName",VARCHAR(200),server_default=None),
            Column("mPcode",VARCHAR(200),server_default=None),
            Column("mDesc",VARCHAR(200),server_default=None),
            Column("mQty",VARCHAR(200),server_default=None),
            Column("mUnitPrice",VARCHAR(200),server_default=None),
            Column("mDiscount",VARCHAR(200),server_default=None),
            Column("mGST",VARCHAR(200),server_default=None),
            Column("mTotalPrice",VARCHAR(200),server_default=None),
            Column("mLedger1",VARCHAR(200),server_default=None),
            Column("mLedgerAmt1",VARCHAR(200),server_default=None),
            Column("mLedger2",VARCHAR(200),server_default=None),
            Column("mLedgerAmt2",VARCHAR(200),server_default=None),
            Column("mledger3",VARCHAR(200),server_default=None),
            Column("mLedgerAmt3",VARCHAR(200),server_default=None),
            Column("mledger4",VARCHAR(200),server_default=None),
            Column("mLedgerAmt4",VARCHAR(200),server_default=None),
            Column("mledger5",VARCHAR(200),server_default=None),
            Column("mLedgerAmt5",VARCHAR(200),server_default=None),
            Column("mledger6",VARCHAR(200),server_default=None),
            Column("mLedgerAmt6",VARCHAR(200),server_default=None),
            Column("mledger7",VARCHAR(200),server_default=None),
            Column("mLedgerAmt7",VARCHAR(200),server_default=None),
            Column("mledger8",VARCHAR(200),server_default=None),
            Column("mLedgerAmt8",VARCHAR(200),server_default=None),
            Column("mTotalAmount",VARCHAR(200),server_default=None),
            Column("mState",VARCHAR(200),server_default=None),
            Column("mCity",VARCHAR(200),server_default=None),
            Column("mCountry",VARCHAR(200),server_default=None),
               
        )
DB = Database()
# DB.inventory_table_dump()
# DB.ledger_table_dump()
# DB.create_table()
# inventory, ledger = DB.insert_table(output_json)
# # inventory_insert = DB.inventory_table_obj.insert().inventory
# # ledger_insert = DB.ledger_table_obj.insert().ledger
# DB.conn.execute(DB.inventory_table_obj.insert(),inventory)
# DB.conn.execute(DB.ledger_table_obj.insert(),ledger)
# print("date inserted")
# DB.insert_table()
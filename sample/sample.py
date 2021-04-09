# # 
# import pyodbc
# import subprocess
# def run(cmd):
#     completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
#     return completed


# def subprocessop(command):
#     output = subprocess.Popen(["powershell","-Command",command],shell=True,stdout=subprocess.PIPE)
#     result = output.communicate()[0],output.returncode
#     return result


# mypurchase = '''select $VoucherTypeName, $VoucherNumber, $Date, $PartyLedgerName,$STATENAME,$COUNTRYOFRESIDENCE,$DELIVERYCITY,$LedgerName, \
#                     $StockItemName,$Discount,$Rate,$BilledQty,$SubAmount,$Led1,$AMT1,$Led2,$AMT2,$Led3,$AMT3,$Led4,$AMT4,$Led5,$AMT5,$Led6,$AMT6,$Led7,$AMT7,$Led8, \
#                         $AMT8 from mypurchase'''

# myvoucher = '''select $VoucherTypeName, $VoucherNumber, $Date, $PartyLedgerName,$STATENAME,$COUNTRYOFRESIDENCE,$DELIVERYCITY,$LedgerName, \
#                     $StockItemName,$Discount,$Rate,$BilledQty,$SubAmount,$Led1,$AMT1,$Led2,$AMT2,$Led3,$AMT3,$Led4,$AMT4,$Led5,$AMT5,$Led6,$AMT6,$Led7,$AMT7,$Led8, \
#                         $AMT8 from myvouchers'''


# conn = pyodbc.connect("DSN=TALLYODBC64_9000")
# cursor = conn.cursor()

# mypurchaseresult = cursor.execute(mypurchase)
# mypurchaseoutput = mypurchaseresult.fetchall()

# myvouchersresult = cursor.execute(mypurchase)
# myvouchersop = myvouchersresult.fetchall()



import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

def send_mail(send_from,send_to, subject, text, files=None,server="127.0.0.1"):
    # assert isinstance(send_to, list)
    msg = MIMEMultipart()
    msg['FROM'] = send_from
    msg['TO'] = COMMASPACE.join(send_to)
    msg['DATE'] = formatdate(localtime=True)

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f,'r') as file:
            part = MIMEApplication(
                file.read(),Name=basename(f)
            )
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)
    
    smtp = smtplib.SMTP(server)
    smtp.sendmail(send_from,send_to,msg.as_string)
    smtp.close

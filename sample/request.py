import requests
import json
import ssl
import urllib

ssl._create_default_https_context = ssl._create_unverified_context



url = 'https://65.0.148.45:8181/erp/rest/dashboard/TokenGenerate/Create/?cmpCode=RGS&orgCode=PAYAGRI'


res =  requests.post(url,data={}, headers={'Content-Type': 'application/json'},verify=False)
print(res.status_code)
print(res.json())
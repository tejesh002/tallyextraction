import json


json_files = open('master.json') 
voucher_data = json.load(json_files)
json_files.close()

import_data = voucher_data['ENVELOPE']['BODY']['IMPORTDATA'] \
    ['REQUESTDATA']['TALLYMESSAGE']
print(len(import_data))

duties_and_taxes = []
group_list = []
for data in import_data:
    if 'GROUP' in data:
        groupname = data['GROUP']['@NAME']
        parent = data['GROUP']['PARENT']
        payload = {
        "group_name" :groupname,
        "parent" :parent
        }
        # print(payload)
        # if parent == 'Duties & Taxes':
        #     duties_and_taxes.append(groupname)

    if "LEDGER" in data:
        

        group_list.append(payload)

       
        
    

with open('group.json','w') as json_file:
    json_file.write(json.dumps({"group":group_list}))




json_file = open('group.json')
data = json.load(json_file)
group = data['group']


def get_duties_tax(gname):
    g_list = []
    for i in group:
        if i['parent'] == gname:
            groupname = i['group_name']
            g_list.append(groupname)
            for j in group:
                    if j['parent'] == groupname:
                        g_list.append(j['group_name'])
                        for k in group:
                            if k['parent'] == groupname:
                                g_list.append(k['group_name'])
                            else:
                                break
                    else:
                        break
    
    return g_list

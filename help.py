import json

st = json.loads('''{
		"firstname":"ABC",
		"middlename":"DEF",
		"lastname":"GHI",
		"salutation":"Mr.",
		"clienttype":2,
		"addressline1":"abcdefg",
		"addressline2":"hijklmno",
		"suburb":"sub",
		"city":"Mumbai",
		"state":"Maharashtra",
		"country":5,
		"zip":"zipcode",
		"homephone":"9892839021",
		"workphone":"8934628291",
		"mobilephone":"9855645531",
		"email1":"abc@def.com",
		"email2":"ghi@jkl.com",
		"employername":"Employer",
		"comments":"abcdef",
		"photo":"efiufheu",
		"onlineaccreated":false,
		"localcontact1name":"abcd",
		"localcontact1address":"ghijklm",
		"localcontact1details":"jwdiuheduhef",
		"localcontact2name":"efgh",
		"localcontact2address":"fgeifhui",
		"localcontact2details":"efiehiufhurihf",
		"includeinmailinglist":true,
		"entityid":2,
		"tenantof":0,
		"tenantofproperty":0
	}''')

table_name = "client"
# key = list(st.keys())
# print(f"{','.join(key)}\n\n\n")
# print(''.join(["%s,"*len(key)]))
# print('\n\n\n')
# s = f"{table_name}"
# for i in key:
#     s += f'["{i}"],{table_name}'
# print(s)
s = ''
keys = list(st.keys())
for i in keys:
    s+=f'{i}=%s,'
print(s)

import json

s = json.loads('''{
      "contactname": "Rudra_2",
      "phone": "9456545514",
      "email": "efg",
      "role": "manager",
      "effectivedate": "2021-02-04 10:00:00",
      "tenureenddate": "2024-02-04 10:00:00",
      "details": "hreiufhuire"
    }''')
               
t = 'contact_insert'
print(','.join(s.keys()))
print('=%s,'.join(s.keys())+"=%s")
print(('%s,'*(len(s.keys())+3))[:-1])
print(f'{t}["' + f'"],{t}["'.join(s.keys())+'"]')
import http.client, urllib.parse
params = urllib.parse.urlencode({})
headers = {"X-EVC-RI": 123,
           "X-EVC-BOX": 123,
           "X-EVC-MDL": 123,
           "X-EVC-OS" : 123,
           "Accept" : "application/json",
           "Content" : "application/json"}
conn = http.client.HTTPConnection('http://devevspcharger.uplus.co.kr/api/v1/OCPP/authorize/',8000)
conn.request("POST", "", params, headers)
response = conn.getresponse()
print(response.status, response.reason)

data = response.read()
conn.close()
import requests
from logsConfigs import log as appLog
class HttpService:

    def post_Request(self, invoiceJson):
        url = "http://localhost:7048/BC170/api/v2.0/companies(8ed64ff1-5645-eb11-bf69-000d3a9d969f)/salesOrders"
        headers = {
            'Authorization': 'Basic REVWT1BTXEFkbWluaXN0cmF0b3I6U29mdGlxQDIwMjI=',
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=invoiceJson)
        print(response.json())
        appLog(1,"Dynamics API response : "+response.text)
        return response.json()

    def getAllItems(self):
        url = "http://localhost:7048/BC170/api/v2.0/companies(8ed64ff1-5645-eb11-bf69-000d3a9d969f)/items"
        payload = {}
        headers = {
            'Authorization': 'Basic REVWT1BTXEFkbWluaXN0cmF0b3I6U29mdGlxQDIwMjI='
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        return response.json()



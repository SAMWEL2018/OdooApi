import requests


class HttpService:

    def post_Request(self, invoiceJson):
        url = "http://localhost:7048/BC170/api/daniel/oyake/v1.0/companies(8ed64ff1-5645-eb11-bf69-000d3a9d969f)/salesOrders"
        headers = {
            'Authorization': 'Basic SUlTIEFQUFBPT0xcQkMxNzA6U29mdGlxQDIwMjI=',
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=invoiceJson)
        print(response.text)
        return response.json()

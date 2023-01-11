import sys
import xmlrpc.client
from configs import Configs
from HttpService import HttpService

cfg = Configs()

url = cfg.url
db = "vombaka-oyake-prod-5154444"  # database name here
username = 'sales@oyake.co.ke'
password = "Sm@rt2022"
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))



items= HttpService()

class Fetch:

    def __init__(self):
        try:
            self.uid = common.authenticate(db, username, password, {})
            self.models= xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        except:
            print("Connection error to Odoo")

    def posHeader(self, id):
        try:
            pos_order = 'pos.order'

            pos =self.models.execute_kw(db, self.uid, password, pos_order, 'search', [[['id', '=', id]]])
            order = self.models.execute_kw(db, self.uid, password, pos_order, 'read', [pos])

            return order[0] if len(order) > 0 else None
        except Exception as e:
            return "ERROR "

    def getLines(self, id):
        pos = self.models.execute_kw(db, self.uid, password, 'pos.order.line', 'search', [[['order_id', '=', id]]])
        lines = self.models.execute_kw(db, self.uid, password, 'pos.order.line', 'read', [pos])
        return lines

    def getPayment(self, id):
        pos = self.models.execute_kw(db, self.uid, password, 'pos.payment', 'search', [[['id', '=', id]]])
        payment = self.models.execute_kw(db, self.uid, password, 'pos.payment', 'read', [pos])
        return payment

    def getItemid(self,referenceNo):

        pr = items.getAllItems()['value']
        for i in pr:
            item_x = i['number']
            if item_x == referenceNo:
                return i['id']

    def getReferenceNo(self,name):
        pos = self.models.execute_kw(db, self.uid, password, 'product.template', 'search',[[['name', '=',name]]])
        product = self.models.execute_kw(db, self.uid, password, 'product.template', 'read', [pos])
        reference = product[0]['default_code']
        if reference == False:
            return None
        return reference


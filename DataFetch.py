import xmlrpc
from configs import Configs
from HttpService import HttpService

cfg = Configs()

url = cfg.url
db = "oyake_softiq"  # database name here
username = 'odoo@softiqtechnologies.co.ke'
password = "admin4321"
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
items= HttpService()

class Fetch:

    def posHeader(self, id):
        pos_order = 'pos.order'
        pos = models.execute_kw(db, uid, password, pos_order, 'search', [[['id', '=', id]]])
        order = models.execute_kw(db, uid, password, pos_order, 'read', [pos])

        return order[0] if len(order) > 0 else None

    def getLines(self, id):
        pos = models.execute_kw(db, uid, password, 'pos.order.line', 'search', [[['order_id', '=', id]]])
        lines = models.execute_kw(db, uid, password, 'pos.order.line', 'read', [pos])
        return lines

    def getPayment(self, id):
        pos = models.execute_kw(db, uid, password, 'pos.payment', 'search', [[['id', '=', id]]])
        payment = models.execute_kw(db, uid, password, 'pos.payment', 'read', [pos])
        return payment

    def getItemid(self,referenceNo):

        pr = items.getAllItems()['value']
        for i in pr:
            item_x = i['number']
            if item_x == referenceNo:
                return i['id']

    def getReferenceNo(self,name):
        pos = models.execute_kw(db, uid, password, 'product.template', 'search',[[['name', '=',name]]])
        product = models.execute_kw(db, uid, password, 'product.template', 'read', [pos])
        reference = product[0]['default_code']
        if reference == False:
            return None
        return reference


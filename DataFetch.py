import xmlrpc

url = "http://localhost:8069"
db = "oyake_softiq"  # database name here
username = 'odoo@softiqtechnologies.co.ke'
password = "admin4321"
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))


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

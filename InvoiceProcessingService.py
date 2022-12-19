import xmlrpc.client as cl

from DataFetch import Fetch
from DynamicsJsnObject import PostInvoice
from HttpService import HttpService
from OrderTrackerNumber import findCurrentOrderIndex, filemodification

url = "http://localhost:8069"
db = "oyake_softiq"  # database name here
username = 'odoo@softiqtechnologies.co.ke'
password = "admin4321"
common = cl.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = cl.ServerProxy('{}/xmlrpc/2/object'.format(url))


class InvoiceProcessingService:

    def __init__(self):
        self.fetch = Fetch()
        self.invoice = PostInvoice()
        self.http = HttpService()

    def processInvoice(self):

        id = int(findCurrentOrderIndex())

        ordered = self.fetch.posHeader(id)
        if ordered is not None:
            name = ordered['name']
            customer = ordered['company_id'][1]
            orderDate = ordered['date_order']

            self.invoice.name = name
            self.invoice.billToName = name
            self.invoice.sellToCustomerName = customer
            self.invoice.documentDate = orderDate
            self.invoice.postingDate = orderDate

            lineStmt = self.fetch.getLines(id)
            paymentM = self.fetch.getPayment(id)

            # exact item info
            itemlist = []
            for info in lineStmt:
                item = {
                    "product_name": info['full_product_name'],
                    "quantity": info['qty'],
                    "price_unit": info['price_unit'],
                    "product_uom_id": info['product_uom_id'][1]
                }
                itemlist.append(item)

            self.invoice.productsLine = itemlist

            # Exact payment for each item
            for payM in paymentM:
                payment_method = payM['payment_method_id'][1]
                amountInc = payM['amount']
                self.invoice.amount = amountInc
                self.invoice.amountIncludingVAT = amountInc
                self.invoice.amountInc = amountInc
                self.invoice.paymentMethod = payment_method

            print("Invoice :", self.invoice.getJson())
            # push invoice to dynamics

            try:
                self.http.post_Request(self.invoice.getJson())
                filemodification(str(id + 1))

            except Exception as e:

                print("Exception In Invoice Processing", e)

            return self.invoice
        else:

            print("No new Order")
            return "No new order"


        # toPost = PostMethod()
        # toPost.post_Request(invoice.getJson())

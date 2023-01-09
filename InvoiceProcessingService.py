import xmlrpc.client as cl


from DataFetch import Fetch
from DynamicHeaderObject import PostH
from DynamicsJsnObject import PostInvoice
from HttpService import HttpService
from configs import Configs
from OrderTrackerNumber import findCurrentOrderIndex, filemodification
from logsConfigs import log as appLog

class InvoiceProcessingService:

    def __init__(self):
        self.fetch = Fetch()
        self.invoice = PostInvoice()
        self.http = HttpService()
        self.header = PostH()
        self.cfg = Configs()


    def processInvoice(self):
        id = int(findCurrentOrderIndex())
        ordered = self.fetch.posHeader(id)
        if ordered is not None:
            pos_reference = ordered['pos_reference']
            self.header.externalDocumentNumber = pos_reference
            lineStmt = self.fetch.getLines(id)

            # exact item info
            itemlist = []
            for info in lineStmt:
                product_name = info['full_product_name']
                RefNo = self.fetch.getReferenceNo(product_name)


                if RefNo is not None:
                    Item_id = self.fetch.getItemid(RefNo)
                    print('iTEM ID', Item_id)

                    item = {
                        "itemId": Item_id,
                        "quantity": info['qty'],
                        "unitPrice": info['price_unit'],

                    }
                    itemlist.append(item)
                    self.header.salesOrderLines = itemlist

                    # Exact payment for each item
                    print("Invoice Header :", self.header.getJson())

                    try:
                        self.http.post_Request(self.header.getJson())
                        appLog(1,"Posted Sales Order : "+self.header.getJson())
                        filemodification(str(id + 1))
                    except Exception as e:
                        print("Exception In Invoice Processing", e)
                else:
                    res = "Reference no from odoo product  is Empty!"
                    appLog(2,"Response from API: "+res)


        # return self.header
        else:
            print("No new Order")
            return "No new order"
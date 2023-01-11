import xmlrpc.client as cl

import requests.exceptions

from DataFetch import Fetch
from DynamicHeaderObject import PostH
from DynamicsJsnObject import PostInvoice
from HttpService import HttpService
from configs import Configs
from OrderTrackerNumber import findCurrentOrderIndex, OrderTrackingUpdate, SkippedOrder
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
        if ordered is not None and "ERROR" not in str(ordered):
            pos_reference = ordered['pos_reference']
            self.header.externalDocumentNumber = pos_reference
            lineStmt = self.fetch.getLines(id)

            # exact item info
            itemlist = []
            for info in lineStmt:
                product_name = info['full_product_name']
                RefNo = self.fetch.getReferenceNo(product_name)
                print('reference ',RefNo)

                if RefNo is not None:
                    Item_id = self.fetch.getItemid(RefNo)
                    print('iTEM ID', Item_id)

                    if Item_id is not None:
                        item = {
                            "itemId": Item_id,
                            "quantity": info['qty'],
                            "unitPrice": info['price_unit'],

                        }
                        itemlist.append(item)
                        self.header.salesOrderLines = itemlist

                        # Exact payment for each item
                        print("Invoice Header :", self.header.getJson())

                    else:

                        SkippedOrder((str(id))+" skipped Order")
                        OrderTrackingUpdate(str(id + 1))
                else:
                    res = "Reference no from odoo product  is Empty!"
                    SkippedOrder((str(id)," Product missing reference No "))
                    OrderTrackingUpdate(str(id + 1))
                    appLog(2,"Response from API: "+res)
                    return
            try:
                res = self.http.post_Request(self.header.getJson())
                if "error" not in str(res):
                    appLog(1,"Posted Sales Order : "+self.header.getJson())
                    OrderTrackingUpdate(str(id + 1))
                else:
                    print('Exception on Dynamics url')
            except requests.exceptions.RequestException as e:
                print("Exception In Posting the order", e)
        else:
            print("No new Order",ordered)
            return "No new order"
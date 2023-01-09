import os


class Configs:
    def __init__(self):
        self.url = os.getenv("url")
        self.db=os.getenv("oyake_softiq")
        self.username = os.getenv("odoo@softiqtechnologies.co.ke")
        self.password = os.getenv("admin4321")
        self.logd  = os.getenv("logdir")
# coding: utf-8

import sys
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Command

from app import app, db

from applications.good.model import Good
from applications.receiver.model import Receiver
from applications.commodity.models import Commodity
from applications.inventory.models import Inventory, InventoryItems
from applications.point_sale.models import PointSale, PointSaleItem
from applications.provider_app.models import Provider
from applications.security.model import User, Role
from applications.waybill.models import WayBillItems, WayBill
from applications.acceptance.model import Acceptance
from applications.price.model import Price, PriceParish
from applications.order.model import Order, OrderItem
from applications.return_app.model import Return, ReturnItem
from applications.waybill_return.model import WayBillReturn, WayBillReturnItems
from applications.seller.model import Seller
from applications.collection.model import Collect
from applications.events.model import Event
from models.invoice import Invoice
from models.invoiceitem import InvoiceItem
from models.retailinvoice import RetailInvoice
from models.retailinvoiceitem import RetailInvoiceItem
from models.revision import Revision, RevisionItem
from models.sync import Sync, SyncSession, SyncItemSession
from models.warehouse import WareHouse
from applications.settings.model import Profile
from applications.mails.model import Mail

__author__ = 'StasEvseev'


class MyMan(Manager):

    def run(self, commands=None, default_command=None):
        """
        Prepares manager to receive command line input. Usually run
        inside "if __name__ == "__main__" block in a Python script.

        :param commands: optional dict of commands. Appended to any commands
                         added using add_command().

        :param default_command: name of default command to run if no
                                arguments passed.
        """

        if commands:
            self._commands.update(commands)

        if default_command is not None and len(sys.argv) == 1:
            sys.argv.append(default_command)

        try:
            result = self.handle(sys.argv[0], sys.argv[1:])
        except SystemExit as e:
            result = e.code
            sys.exit(result or 0)


man = MyMan(app)
man.add_command('db', MigrateCommand)

migrate = Migrate(app, db)
manager = Manager(app)


class TestConfig(object):
    # SQLALCHEMY_DATABASE_URI = 'sqlite://'
    testing = True
    debug = True
    FIXTURES_DIRS = ['datas/fixtures']

app.config.from_object(TestConfig)


class SuperUserCommand(Command):
    """

    Команда создания суперпользователя.

    """
    def run(self):
        app.create_superuser()

manager.add_command('db', MigrateCommand)
manager.add_command('create_superuser', SuperUserCommand())

if __name__ == "__main__":
    manager.run()

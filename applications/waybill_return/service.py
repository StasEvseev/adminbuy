#coding: utf-8
from sqlalchemy import desc
from applications.waybill_return.model import WayBillReturn, TYPE, RecType, POINTSALE, RECEIVER, WayBillReturnItems, \
    RETAIL, StatusType, FINISH, IN_PROG, DRAFT
from db import db
from log import error, debug
from services import ModelService
from services.core import BaseSQLAlchemyModelService


class WayBillReturnService(BaseSQLAlchemyModelService):
    model = WayBillReturn

    class WayBillReturnServiceExc(BaseSQLAlchemyModelService.ServiceException):
        pass

    @classmethod
    def generate_number(cls, date, type):
        """
        Генерация номера для накладной.
        Маска - [порядкой номер для дня] - [тип(1,2)] - [дата полная].
        Пример - 001-1-20122014 - означает первая розничная накладная на дату 20 декабря 2014 года.
        """
        waybillreturn = WayBillReturn.query.filter(
            WayBillReturn.date == date).order_by(desc(WayBillReturn.id)).first()
        if waybillreturn is None:
            return u"В-001-" + str(type) + "-" + date.strftime("%d%m%Y")
        else:
            number = waybillreturn.number
            numbers = number.split("-")
            number = int(numbers[0])
            return "-".join([u"В", '%03d' % (number + 1), str(type), numbers[2]])

    #TODO изменить сигнатуру метода
    @classmethod
    def create(cls, pointsale_id, receiver_id, date, date_to, type, typeRec, return_id):
        """
        Создаем или получаем итоговую накладную.
        Сначала проверяем, есть ли уже накладная по параметрам уникальности(приходная накладная, получатели
        (точки или получатель) и тип).
        Если накладной нет, то создаем.
        Если накладная уже есть, генерим исключение. Но если нам передали флаг forse, то извлекаем из БД и возвращаем.
        """
        if not ModelService.check_id(receiver_id) and not ModelService.check_id(pointsale_id):
            raise WayBillReturnService.WayBillReturnServiceExc(u"No receiver or point sale")

        type = int(type)
        typeRec = int(typeRec)
        if type not in TYPE.keys():
            raise WayBillReturnService.WayBillReturnServiceExc(u"Тип накладной указан неверно - %s." % type)
        if typeRec not in RecType.keys():
            raise WayBillReturnService.WayBillReturnServiceExc(u"Тип получателя указан неверно - %s." % typeRec)

        waybillreturn = WayBillReturn()
        waybillreturn.returninst_id = return_id
        waybillreturn.date = date
        waybillreturn.date_to = date_to
        if typeRec == POINTSALE:
            if not ModelService.check_id(pointsale_id):
                raise WayBillReturnService.WayBillReturnServiceExc(u"Ошибка. Нельзя выбрать тип 'Торговая точка' и 'Оптовика'.")
            waybillreturn.pointsale_id = pointsale_id
        elif typeRec == RECEIVER:
            if not ModelService.check_id(receiver_id):
                raise WayBillReturnService.WayBillReturnServiceExc(u"Ошибка. Нельзя выбрать тип 'Оптовика' и 'Торговую точку'.")
            waybillreturn.receiver_id = receiver_id

        waybillreturn.type = type
        waybillreturn.number = cls.generate_number(date, type)
        waybillreturn.typeRec = typeRec
        db.session.add(waybillreturn)
        return waybillreturn

    @classmethod
    def build_retail_items(cls, items):
        """
        Собираем объекты для более удобной обработки из списка словарей.
        """
        try:
            return [WayBillReturnItems(good_id=it['good_id'],
                                       count_plan=it['count_plan'] if 'count_plan' in it and it['count_plan'] else None,
                                       count=it['count'] if 'count' in it and it['count'] else None
                                       ) for it in items]
        except KeyError as exc:
            error(u"Ошибка при сохранении позиций товара. " + unicode(exc))
            raise WayBillReturnService.WayBillReturnServiceExc(u"Ошибка при сохранении позиций товара.")

    @classmethod
    def upgrade_items(cls, waybillreturn, items):
        from applications.price.service import PriceService
        from services import GoodService

        waybillreturn.items.delete()
        db.session.add(waybillreturn)

        for it in items:
            good = GoodService.get_good(it.good_id)
            if waybillreturn.type == RETAIL:
                if not good.price_id or not PriceService.get_price(good.price_id).price_retail:
                    raise WayBillReturnService.WayBillReturnServiceExc(
                        u"Товар без розничной цены. %s" % good.full_name)
            else:
                if not good.price_id or not PriceService.get_price(good.price_id).price_gross:
                    raise WayBillReturnService.WayBillReturnServiceExc(
                        u"Товар без оптовой цены. %s" % good.full_name)
            it.waybill = waybillreturn
            db.session.add(it)

    @classmethod
    def status(cls, waybillreturn, status):
        from applications.point_sale.service import PointSaleService
        from applications.return_app.service import ReturnService
        debug(u"Смена статуса `накладной возврата` %s с %s на %s." % (waybillreturn.id, waybillreturn.status, StatusType[status]))

        if status == DRAFT:
            waybillreturn.items.delete()

        if status == IN_PROG:
            waybillreturn.items.delete()
            return_inst = ReturnService.get_by_id(waybillreturn.returninst_id)
            point = waybillreturn.pointsale

            for item in return_inst.items:
                good_id = item.good_id
                res = PointSaleService.item_to_pointsale_good(point.id, good_id)
                if res:
                    itemreturn = WayBillReturnItems()
                    itemreturn.waybill = waybillreturn
                    itemreturn.good_id = good_id
                    itemreturn.count_plan = res.count
                    db.session.add(itemreturn)

        if status == FINISH:
            from_point = waybillreturn.pointsale
            to_point = PointSaleService.get_central()
            for item in waybillreturn.items:
                PointSaleService.sync_good_increment(from_point.id, item.good_id, item.count * -1 if item.count else 0)
                PointSaleService.sync_good_increment(to_point.id, item.good_id, item.count if item.count else 0)

        waybillreturn.status = status
        debug(u"Смена статуса `накладной возврата` %s с %s на %s завершено." % (waybillreturn.id, waybillreturn.status, StatusType[status]))
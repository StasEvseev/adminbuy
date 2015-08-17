#coding: utf-8
from datetime import datetime
from flask.ext.restful import fields
from applications.order.model import Order, OrderItem
from applications.order.service import OrderService
from resources.core import BaseCanoniseResource, BaseInnerCanon
from services import HelperService


class OrderItemInnerCanon(BaseInnerCanon):
    inner_model = Order
    model = OrderItem

    attr_json = {
        'id': fields.Integer,
        'full_name': fields.String,
        'date': fields.String,
        'remission': fields.String,
        'count': fields.String,
        'price_prev': fields.Price,
        'price_post': fields.Price
    }

    default_sort = 'asc', 'id'


class OrderCanon(BaseCanoniseResource):
    model = Order

    attr_json = {
        'id': fields.Integer,
        'date_start': fields.String,
        'date_end': fields.String,
        'provider_id': fields.Integer,
        'provider': fields.Nested({
            'name': fields.String
        })
    }

    def post_save(self, obj, data, create_new=False):

        if obj.id:
            if datetime.now().date() > HelperService.convert_to_pydate(obj.date_end).date():
                raise BaseCanoniseResource.CanonException(u"Нельзя редактировать заказ с истекшим сроком.")

            OrderService.set_handling(obj.id)

            items = data['items'] if 'items' in data else []

            for item in items:
                OrderService.set_count_by_id(item['id'], item['count'])

        super(OrderCanon, self).post_save(obj, data, create_new=create_new)
#coding: utf-8
from datetime import datetime
from flask.ext.restful import fields, marshal_with
from applications.return_app.service import ReturnService
from applications.return_app.model import Return, ReturnItem
from resources.core import BaseCanoniseResource, BaseInnerCanon, BaseStatusResource
# from services import HelperService


class ReturnItemInnerCanon(BaseInnerCanon):
    inner_model = Return
    model = ReturnItem

    attr_json = {
        'id': fields.Integer,
        'full_name': fields.String,
        # 'date': fields.String,
        'remission': fields.String,
        'count_delivery': fields.String,
        'count_rem': fields.String,
        'count': fields.String,
        'price_with_NDS': fields.Price,
        # 'price_post': fields.Price
    }

    default_sort = 'asc', 'id'


ITEM = {
    'id': fields.Integer,
    'date_start': fields.String,
    'date_end': fields.String,
    'name': fields.String,
    'provider_id': fields.Integer,
    'provider': fields.Nested({
        'name': fields.String
    }),
    'status': fields.Integer(attribute='status.code'),
    'status_str': fields.String(attribute='status.value'),
}


class ReturnCanon(BaseCanoniseResource):
    model = Return

    attr_json = ITEM

    def post_save(self, obj, data, create_new=False):

        if obj.id:
            # if datetime.now().date() > HelperService.convert_to_pydate(obj.date_end).date():
            #     raise BaseCanoniseResource.CanonException(u"Нельзя редактировать заказ с истекшим сроком.")

            # ReturnService.set_handling(obj.id)

            items = data['items'] if 'items' in data else []

            for item in items:
                ReturnService.set_count_by_id(item['id'], item['count'])
                # OrderService.set_count_by_id(item['id'], item['count'])

        super(ReturnCanon, self).post_save(obj, data, create_new=create_new)


class ReturnStatusResource(BaseStatusResource):
    
    service = ReturnService

    @marshal_with(ITEM)
    def post(self, id):
        return self._action(id)
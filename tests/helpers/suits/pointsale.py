#coding: utf-8
from app import db
from applications.point_sale.models import PointSale
from tests.helpers.suits import BaseSuite


class PointSaleSuite(BaseSuite):

    def create_test_pointsale(self, name, address, is_central=False):
        # with self.application.app_context():
        pointsale = PointSale(name=name, address=address, is_central=is_central)
        db.session.add(pointsale)
        db.session.commit()
        return pointsale

    def create_pointsale_rest(self, name, address, is_central=False):
        return self.client.put('/api/pointsale', data=self._serialize({'data':{
            'name': name,
            'address': address,
            'is_central': is_central
        }}), headers=self._get_headers(True))

    def update_pointsale_rest(self, id, name=None, address=None, is_central=False):
        data = {}
        if name:
            data['name'] = name
        if address:
            data['address'] = address
        data['is_central'] = is_central
        return self.client.post("/api/pointsale/" + str(id), data=self._serialize({
            'data': data}), headers=self._get_headers(True))
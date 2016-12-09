#coding: utf-8
from tests.helpers.suits import BaseSuite

__author__ = 'StasEvseev'


class RevisionSuite(BaseSuite):

    def create_revision(self, pointsale_id, seller_id, date):
        return self.client.put("/api/revision",
                               data=self._serialize({'data': {
                                   'pointsale_id': pointsale_id,
                                   'seller_id': seller_id,
                                   'date': unicode(date)
                               }}),
                               headers=self._get_headers())

    def update_item_revision(self, item_id, good_id, count):
        return self.client.post("/api/revisionitem/" + str(item_id),
                                data=self._serialize({'data': {
                                    'good_id': good_id,
                                    'count_after': count
                                }}),
                                headers=self._get_headers(True))

    def add_item_revision(self, revision_id, good_id, count):
        return self.client.put("/api/revisionitem",
                               data=self._serialize({'data': {
                                   'revision_id': revision_id,
                                   'good_id': good_id,
                                   'count_after': count
                               }}),
                               headers=self._get_headers(True))

    def approve_revision(self, revision_id):
        return self.client.post("/api/revision/" + str(revision_id) + "/approve", headers=self._get_headers(True))

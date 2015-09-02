#coding: utf-8
from tests.helpers.suits import BaseSuite


class InventorySuite(BaseSuite):

    def create_inventory(self, location_id, number):
        return self.client.put("/api/inventory",
                               data=self._serialize({'data': {
                                   'location_id': location_id,
                                   'number': number
                               }}),
                               headers=self._get_headers())

    def update_inventory(self, inventory_id, location_id=None, number=None, datetime=None, items=None):
        par = {}
        if location_id:
            par['location_id'] = location_id
        if number:
            par['number'] = number
        if items:
            par['items'] = items
        if datetime:
            par['datetime'] = str(datetime)
        return self.client.post("/api/inventory/" + str(inventory_id),
                                data=self._serialize({'data': par}),
                                headers=self._get_headers(True))

    def inventory_status(self, inventory_id, status):
        return self.client.post("/api/inventory/" + str(inventory_id) + "/status",
                                data=self._serialize({'data': {
                                    'status': status
                                }}),
                                headers=self._get_headers(True))

    # def update_item_revision(self, item_id, good_id, count):
    #     return self.client.post("/api/revisionitem/" + str(item_id),
    #                             data=self._serialize({'data': {
    #                                 'good_id': good_id,
    #                                 'count_after': count
    #                             }}),
    #                             headers=self._get_headers(True))
    #
    # def add_item_revision(self, revision_id, good_id, count):
    #     return self.client.put("/api/revisionitem",
    #                            data=self._serialize({'data': {
    #                                'revision_id': revision_id,
    #                                'good_id': good_id,
    #                                'count_after': count
    #                            }}),
    #                            headers=self._get_headers(True))

    # def approve_revision(self, revision_id):
    #     return self.client.post("/api/revision/" + str(revision_id) + "/approve", headers=self._get_headers(True))
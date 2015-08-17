#coding: utf-8

from . import BaseSuite


class AcceptanceSuite(BaseSuite):

    def acceptance_status(self, acc_id, status):
        return self.client.post("/api/acceptance/" + str(acc_id) + "/status",
                                data=self._serialize({'data': {
                                    'status': status
                                }}),
                                headers=self._get_headers(True))

    def create(self, date, type=None, provider_id=-1, pointsale_id=-1, invoice_id=-1):
        data = {
            'invoice_id': invoice_id,
            'pointsale_id': pointsale_id,
            'provider_id': provider_id,
            'date': unicode(date)
        }
        if type:
            data['type'] = type
        return self.client.put("/api/acceptance", data=self._serialize({'data': data}),
                               headers=self._get_headers(True))

    def update(self, id, date=None, type=None, provider=None, pointsale_id=-1, invoice_id=-1):
        data = {}
        if date:
            data['date'] = unicode(date)

        return self.client.post("/api/acceptance/" + str(id), data=self._serialize(
            {'data': data}), headers=self._get_headers(True))

    def update_items(self, id, items=None):
        return self._update_items(id, 'items', items)

    def update_new_items(self, id, items=None):
        return self._update_items(id, 'new_items', items)

    def _update_items(self, id, attr, items=None):
        data = {}
        if items:
            data[attr] = items
        return self.client.post('/api/acceptance/' + str(id), data=self._serialize(
            {'data': data}), headers=self._get_headers(True))
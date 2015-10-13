#coding: utf-8\n__author__ = 'StasEvseev'
import re


class BaseResourceAngular(object):
    def _convert_attr_to_js(self, attr):
        return re.sub(ur"<[^>]+>", ":id", attr)


class ResourceGetAngularUrl(BaseResourceAngular):

    def __init__(self, prefix_rest, url, res):
        self.prefix_rest = prefix_rest
        self.url = url
        self.res = res

    def url_get(self):
        return "".join([self.prefix_rest, self.url, self._convert_attr_to_js(self.res.prefix_url_with_id)])


class ResourceAngularUrl(BaseResourceAngular):
    def __init__(self, prefix_rest, url, res):
        self.prefix_rest = prefix_rest
        self.url = url
        self.res = res

    def url_create(self):
        return "".join([self.prefix_rest, self.url, self._convert_attr_to_js(self.res.prefix_url_without_id)])

    def url_update(self):
        return "".join([self.prefix_rest, self.url, self._convert_attr_to_js(self.res.prefix_url_with_id)])

    def url_delete(self):
        return "".join([self.prefix_rest, self.url, self._convert_attr_to_js(self.res.prefix_url_with_id)])

    def url_get(self):
        return "".join([self.prefix_rest, self.url, self._convert_attr_to_js(self.res.prefix_url_with_id)])

    def url_getall(self):
        return "".join([self.prefix_rest, self.url, self._convert_attr_to_js(self.res.prefix_url_without_id)])

    # def _convert_attr_to_js(self, attr):
    #     return re.sub(ur"<[^>]+>", ":id", attr)


class ResourceAngularInnerUrl(ResourceAngularUrl):
    def _convert_attr_to_js(self, attr):
        str = re.sub(ur"<int:inner_id>", ":inner_id", attr)
        return re.sub(ur"<int:id>", ":id", str)
#coding: utf-8\n__author__ = 'StasEvseev'


class Validator(object):
    class ValidateError(Exception):
        pass

    # def __init__(self):
    #     pass
        # self.id = id
        # self.attr = attr

    def validate_python(self, value):
        pass

    def validate_js(self):
        pass

    def initial(self, id, label, prefix):
        self.id = id
        self.attr = prefix + "." + id
        self.prefix = prefix
        self.label = label


class RequiredValidator(Validator):

    def __init__(self, message):
        self.message = message

    def validate_python(self, value):
        if value is None:
            raise Validator.ValidateError(u"")

    def validate_js(self):
        return u"""
        if(!%s) {
            setError("%s", "%s");
        } else {
            setError("%s");
        }""" % (self.attr, self.id, self.message, self.id)


class RequiredPredExpres(Validator):
    def __init__(self, attr_predicate, message):
        self.attr_predicate = attr_predicate
        self.message = message

    def validate_js(self):
        return u"""
            if(%(predicate)s) {
                if(!%(attr)s) {
                    setError("%(id)s", "%(message)s");
                } else {
                    setError("%(id)s");
                }
            } else {
                setError("%(id)s");
            }
        """ % {
            'attr': self.attr,
            'id': self.id,
            'message': self.message,
            'predicate': self.prefix + "." + self.attr_predicate
        }


class RequiredPredicate(Validator):
    def __init__(self, attr_predicate, message1, message2):
        self.attr_predicate = attr_predicate
        self.message1 = message1
        self.message2 = message2

        self.__attr = self.attr_predicate.split(".")

    def validate_js(self):
        return u"""
        if(%(prefix)s && %(prefix_predicate)s) {
            if(!%(attr)s) {
                setError("%(id)s", "%(message_predicate_1)s");
            } else {
                setError("%(id)s");
            }
        } else if (%(prefix)s && !%(prefix_predicate)s) {
            if(%(attr)s) {
                setError("%(id)s", "%(message_predicate_2)s");
            } else {
                setError("%(id)s");
            }
        }
        """ % {
            'prefix': self.prefix + "." + self.__attr[0],
            'prefix_predicate': self.prefix + "." + self.attr_predicate,
            'attr': self.attr,
            'id': self.id,
            'message_predicate_1': self.message1 % self.label,
            'message_predicate_2': self.message2 % self.label
        }
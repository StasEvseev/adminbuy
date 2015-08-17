#coding: utf-8


class Behavior(object):
    pass


class BehaviorHidden(Behavior):
    pass


class BehaviorHiddenPredicate(BehaviorHidden):

    def __init__(self, predicate_js):
        self.predicate_js = predicate_js

    def view(self):
        return "ng-hide='%s'" % self.predicate_js
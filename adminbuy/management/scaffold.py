# coding: utf-8

from flask.ext.script import Command, Option

from adminbuy.scaffolding import scaffold_angular


class ScaffoldingCommand(Command):

    option_list = (
        Option('--name', '-n', dest='name', required=True),
    )

    def run(self, name):
        scaffold_angular(name)

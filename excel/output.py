#coding:utf-8
import os

import xlrd
import xlwt
from xlutils.copy import copy


path = os.path.dirname(__file__)
PATH_TEMPLATE = os.path.join(path, 'template')


class PrintInvoiceHelper(object):

    pass


class PrintInvoice(object):
    """
    Класс для генерации отчетов в excel.
    """
    def __init__(self, path, destination):
        self.path = path
        self.destination_filename = destination
        self.read_book = xlrd.open_workbook(path, formatting_info=True)
        self.write_book = copy(self.read_book)
        self.sheets = None
        self.global_begin = 0

    def set_cells(self, number_sheet, number_begin, list_cell):

        read_sheet = self.read_book.sheet_by_index(number_sheet)

        _sheet = SheetInvoice()
        _sheet.begin = number_begin

        for n, cell in enumerate(list_cell):
            style_index = read_sheet.cell(number_begin, n).xf_index
            style_old = self.read_book.xf_list[style_index]
            style_font = self.read_book.font_list[style_old.font_index]
            style_format = self.read_book.format_map[style_old.format_key]

            style = xlwt.XFStyle()
            _sheet._set_border(style_old, style)
            _sheet._set_format(style_format, style)
            _sheet._set_font(style_font, style)

            if type(cell) == tuple:
                _, cl = cell
                widths = [(n + x + 1, read_sheet.colinfo_map[x + 1].width) for x in xrange(cl - 1)]
            else:
                widths = None

            cel = CellInvoice(n, cell, style, widths)
            cel.width = read_sheet.colinfo_map[number_begin].width

            _sheet.add_cells(cel)

        setattr(self, 'sheet_%s_%s' % (number_sheet, number_begin), _sheet)

    def write(self, sheet, begin, of, list):
        write_sheet = self.write_book.get_sheet(sheet)
        sheet_ = getattr(self, 'sheet_%s_%s' % (sheet, begin))
        # begin = sheet_.begin
        begin = self.global_begin + of
        for el in list:
            offset = 0
            for cell in sheet_.get_cells():
                index, name, style, widths = cell.render()
                cols = None
                if type(name) == tuple:
                    name, cols = name
                try:
                    value = unicode(el[name])
                except KeyError:
                    continue
                if cols:
                    write_sheet.write_merge(begin, begin, index + offset, index + cols - 1 + offset, value, style)
                    offset += cols - 1
                else:
                    write_sheet.write(begin, index + offset, value, style)
                write_sheet.col(index).width = cell.width
                # if widths:
                #     for i in widths:
                #         index, width = i
                #         write_sheet.col(index).width = width
            begin += 1
        self.global_begin = begin

        self.write_book.save(
            self.destination_filename)


class SheetInvoice(object):
    begin = 0
    collection_cell = None

    def __init__(self):
        self.collection_cell = []

    def add_cells(self, cell):
        self.collection_cell.append(cell)

    def get_cells(self):
        return self.collection_cell

    def _set_border(self, style_old, style_new):
        border = style_old.border
        style_new.borders.bottom = border.bottom_line_style
        style_new.borders.left = border.left_line_style
        style_new.borders.right = border.right_line_style
        style_new.borders.top = border.top_line_style

    def _set_format(self, format, style_new):
        style_new.num_format_str = format.format_str

    def _set_font(self, font, style_new):
        style_new.font.name = font.name
        style_new.font.height = font.height


class CellInvoice(object):
    index = 0
    style = xlwt.XFStyle()
    name = None
    widths = None

    def __init__(self, index, name, style=None, widths=None):
        self.index = index
        self.name = name
        if style is not None:
            self.style = style
        self.widths = widths

    def render(self):
        return [self.index, self.name, self.style, self.widths]
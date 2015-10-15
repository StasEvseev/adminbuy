# coding: utf-8
"""
Модуль отвечающий за события в системе.

Например:
 - получение почты с накладной
 - формирование расходных накладных
 - приемка товара


Принята модель сохранения событий в реляционной базе следующая:
 type - некий enum обозначающий тип события(Приемка почты, формирование накладной...);
 datetime - timestamp without timezone день, время события;
 data - тут будут сохранятся JSON со специфичными для события данными.
"""
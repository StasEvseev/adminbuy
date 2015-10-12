#coding: utf-8
import json

import uuid
import os

from flask import g, jsonify, request, Response
from flask.ext import restful
from flask.ext.restful import reqparse, marshal_with, fields, abort

from sqlalchemy import desc, asc, or_, and_
from sqlalchemy.sql.sqltypes import BigInteger, BIGINT
from sqlalchemy_utils import ChoiceType
from sqlalchemy.orm.collections import InstrumentedList
from werkzeug.wrappers import BaseResponse

from excel.output import PrintInvoice, PATH_TEMPLATE
from helper import get_relation_model

from applications.security.auth import auth, auth_admin

from log import error, debug
from db import db

from config import PATH_WEB, PATH_TO_GENERATE_INVOICE


parser = reqparse.RequestParser()
parser.add_argument('filter_field', type=str)
parser.add_argument('filter_text', type=unicode)
parser.add_argument('sort_field', type=str)
parser.add_argument('sort_course', type=str)
parser.add_argument('count', type=int)
parser.add_argument('page', type=int)
parser.add_argument("ids", type=unicode, location='args')


class BaseTokenMixinResource(object):
    decorators = [auth.login_required]


class BaseTokeniseResource(restful.Resource):
    decorators = [auth.login_required]


class BaseTokeniseAdminResource(BaseTokeniseResource):
    decorators = [auth.login_required,
                  auth_admin.login_required]


class BasePrintResource(BaseTokeniseResource):
    prefix_url_with_id = "/<int:id>"

    TEMPLATE = ""

    @marshal_with({
        'link': fields.String
    })
    def get(self, id):
        pi = self._get_template()
        self.handle(pi, id)
        path = pi.path_web
        return {"link": path}

    def handle(self, pi, id):

        pass

    def _get_template(self):
        file_name = str(uuid.uuid4()) + ".xls"
        path_to_target = os.path.join(PATH_TO_GENERATE_INVOICE, file_name)
        path = os.path.join(PATH_WEB, file_name)

        pi = PrintInvoice(
            path=os.path.join(PATH_TEMPLATE, self.TEMPLATE),
            destination=path_to_target)
        pi.path_web = path
        return pi


class FilterObj(object):
    """
    Класс, основное назначение которого - фильтрация в базе.
    """
    @classmethod
    def filter_query(cls, query, filter_field, filter_text, sort_field, sort_course, page, count, model,
                     multif, clazz, default_sort=None):
        """
        Метод для дополнительной фильтрации.
        """
        if filter_field and filter_text:
            debug(u"Фильтрация %s." % clazz)
            if filter_field in multif.keys():
                flds = multif[filter_field]
                subq = []
                for fld in flds:
                    rels = fld.split(".")
                    """
                    Проверяем фильтрацию на связанные модели. Если есть, то надо сначала связать эти таблицы.
                    """
                    if len(rels) == 1:
                        debug(u"Фильтрация %s по модели." % fld)
                        sss = []
                        for ss in filter_text.split(" "):
                            sss.append(model.__table__.columns[fld].ilike("%"+ss+"%"))
                        subq.append(and_(*sss))
                    else:
                        debug(u"Фильтрация %s по связанной модели %s." % (clazz, fld))
                        rel_m, attr = rels
                        cl = get_relation_model(model, rel_m)
                        query = query.join(cl)
                        subq.append(cl.__table__.columns[attr].ilike("%"+filter_text+"%"))
                query = query.filter(or_(*subq))
            else:
                query = query.filter(
                    model.__table__.columns[filter_field].ilike("%"+filter_text+"%")
                )
            debug(u"Фильтрация %s успешна." % clazz)
        if sort_field and sort_course:
            query = query.order_by(
                {'desc': desc, 'asc': asc}[sort_course](model.__table__.columns[sort_field])
            )
        elif not default_sort:
            query = query.order_by(desc(model.id))
        else:
            ord, fld = default_sort
            query = query.order_by(
                {'desc': desc, 'asc': asc}[ord](model.__table__.columns[fld])
            )
        max_ = query.count()

        if page and count:
            query = query.offset((page - 1) * count).limit(count)
        records = query.all()
        count_ = query.count()
        return records, max_, count_


class GetResource(BaseTokeniseResource):
    """
    Ресурс для выбора связанных записей(никаких редактирований, добавлений, удалений).
    """
    model = None
    multif = {}
    default_sort = None
    attr_json = {}
    prefix_url_with_id = "/<int:id>"

    @classmethod
    def _register_into_rest(cls):
        self = cls()
        type1 = type(
            cls.__name__ + "Item",
            (BaseTokeniseResource, ),
            {
                "get": marshal_with({'items': fields.List(fields.Nested(cls.attr_json)),
                                     'count': fields.Integer,
                                     'max': fields.Integer})(self.get.__func__).__get__(self, cls),
                "parent": self
            }
        )
        return type1

    def query_initial(self, *args, **kwargs):
        return self.model.query

    def get(self, *args, **kwargs):
        """
        Работа с большим количество записей по модели.
        """
        args_pars = parser.parse_args()

        filter_field = args_pars['filter_field']
        filter_text = args_pars['filter_text']
        sort_field = args_pars['sort_field']
        sort_course = args_pars['sort_course']
        page = args_pars['page']
        count = args_pars['count']

        query = self.query_initial(*args, **kwargs)

        records, max_, count_ = FilterObj.filter_query(
            query, filter_field, filter_text, sort_field, sort_course, page, count,
            model=self.model, multif=self.multif, clazz=self.__class__,
            default_sort=self.default_sort)

        return {'items': records, 'count': count_, 'max': max_}


class BaseStatusResource(BaseTokeniseResource):
    service = None

    @classmethod
    def getService(cls):
        return None

    def _action(self, id):
        service = BaseStatusResource.getService()
        try:
            object = service.get_by_id(id)
            status = request.json['data']['status']
            service.status(object, status)
            db.session.add(object)
            db.session.commit()
            return object
        except Exception as exc:
            message = u" Не удалось сменить статус `%s` %s." % (service.model, id)
            error(message + unicode(exc))
            abort(400, message=message)


class BaseCanoniseResource(object):
    """
    Базовый класс ресурсов. Формирует CRUD URL для :attr model.
    """
    model = None
    attr_json = {}

    attr_response_post = {}
    attr_response_put = {}

    default_sort = None

    multif = {"filter_field": ()}

    prefix_url_with_id = "/<int:id>"
    prefix_url_without_id = ""

    base_class = BaseTokeniseResource

    class CanonException(Exception):
        pass

    @classmethod
    def _register_into_rest(cls):
        """
        Регистрация ресурсов в РЕСТе.
        """
        self = cls()
        cls.attr_response_post = cls.attr_response_post or cls.attr_json
        cls.attr_response_put = cls.attr_response_put or cls.attr_json
        type1 = type(
            cls.__name__ + "Item",
            (cls.base_class, ),
            {
                "get": marshal_with({'items': fields.List(fields.Nested(cls.attr_json)),
                                     'count': fields.Integer,
                                     'max': fields.Integer})(self.get_items.__func__).__get__(self, cls),
                "put": marshal_with(cls.attr_response_put)(self.put.__func__).__get__(self, cls),
                "parent": self
            }
        )

        type2 = type(
            cls.__name__ + "Items",
            (cls.base_class, ),
            {
                "get": marshal_with(cls.attr_json)(self.get.__func__).__get__(self, cls),
                "post": marshal_with(cls.attr_response_post)(self.post.__func__).__get__(self, cls),
                "delete": self.delete,
                "parent": self
            }
        )

        return (cls.prefix_url_without_id, type1), (cls.prefix_url_with_id, type2)

    def filter_query(self, query, filter_field, filter_text, sort_field, sort_course, page, count):
        """
        Метод для дополнительной фильтрации.
        """

        return FilterObj.filter_query(query, filter_field, filter_text, sort_field, sort_course, page, count,
                                      model=self.model, multif=self.multif, clazz=self.__class__,
                                      default_sort=self.default_sort)

    def _get_attr_relation(self):
        """
        Формируем словарь из :attr_json для связанных моделей.

        Ищем значения с указанными attribute через точку(означает либо аттрибут связанной модели, либо ChoiceType.

        Убираем ChoiceType.
        """
        def _f(item):

            name, value = item
            if not hasattr(value, "attribute") or getattr(value, "attribute") == None or not "." in getattr(value, "attribute"):
                return False
            attr_m = getattr(value, "attribute").split('.')[0]

            if hasattr(getattr(self.model, attr_m), "type") and getattr(self.model, attr_m).type.__class__ == ChoiceType:
                return False
            return True

        return filter(_f, self.attr_json.iteritems())

    #===================================================================================================================
    #BASE CRUD - вынести в отдельный объект
    def get_by_id(self, id):
        return self.model.query.get(id)

    def save_model(self, obj):
        db.session.add(obj)
        return obj

    def pre_delete(self, obj):
        pass

    def post_delete(self, obj):
        debug(u"Удаление записи %s." % obj)

    def pre_save(self, obj, data):
        return obj

    def _type_column(self, model, name):
        if name in model._sa_class_manager and hasattr(model._sa_class_manager[name].property, 'columns') and model._sa_class_manager[name].property.columns:
            return model._sa_class_manager[name].property.columns[0].type

    def post_save(self, obj, data, create_new=False):
        """
        Сохранение связанных моделей, если вдруг приходит в параметрах.
        Смотрим :attr_json, если в описании есть аттрибуты связанных моделей
        (Пример: {'price_post': Attr(attribute='price.price_post')}, - это значит что если в запросе придет параметр
        'price.price_post', то ищем связанную модель 'price' в нашей модели, если нашли, то изменяем ее атрибуты, если
        нет, то создаем новую модель и привязываем к нашей).

        @New version 0.1:
        Появилось поле ChoiceType, которое тоже нужно прокидывать в рест, в качестве значения в БД, либо в расшифровке.
        Специально для него, тоже проставляем `attribute. В итоге надо как то искать такие поля и игнорировать, иначе
        система работает с ними как со связанными через модельку.
        """
        if data:
            attr_relation = self._get_attr_relation()
            list_created_obj = []
            for key, attr in attr_relation:
                objnest = obj
                full_p = attr.attribute
                chain_models, _, at = attr.attribute.rpartition(".")
                for chain_model in chain_models.split("."):
                    try:
                        #Ищем поля ChoiceType
                        try:
                            if objnest == obj \
                                    and hasattr(objnest._sa_class_manager[chain_model].property, 'columns') \
                                    and objnest._sa_class_manager[chain_model].property.columns \
                                    and isinstance(objnest._sa_class_manager[chain_model].property.columns[0].type, ChoiceType):
                                break
                        except AttributeError as exc:
                            error(unicode(exc))
                            raise Exception(exc)
                        value = getattr(objnest, chain_model)
                        if not value and key in data:
                            rel_model = get_relation_model(objnest, chain_model)
                            instance = rel_model()
                            setattr(objnest, chain_model, instance)
                            objnest = getattr(objnest, chain_model)
                        else:
                            objnest = value
                    except AttributeError as exc:
                        break
                    except Exception as exc:
                        pass
                else:
                    try:
                        setattr(objnest, at, data[full_p])
                    except (KeyError, AttributeError):
                        pass
                    else:
                        if objnest not in list_created_obj:
                            list_created_obj.append(objnest)
            for objs in list_created_obj:
                db.session.add(objs)

    #===================================================================================================================

    def fill_obj(self, data, obj=None):
        """
        заполнение объекта данными с json
        """
        if 'id' in data:
            obj = self.get_by_id(data['id'])
        elif not obj:
            obj = self.model()
        for key in self.attr_json.keys():
            if key not in data:
                continue
            value = data.get(key)
            if value is not False and value in [-1, 0]:
                value = None
            try:
                #В случаях, когда у модели поле типа int, long, а пришла пустая строка - нужно далеть поле None
                if type(self._type_column(obj, key)) in [BIGINT, BigInteger] and value in ['']:
                    setattr(obj, key, None)
                else:
                    if not isinstance(getattr(obj, key), InstrumentedList):
                        setattr(obj, key, value)
            except (AttributeError, TypeError) as exc:
                pass
        return obj

    #===================================================================================================================
    #REST

    def query_initial(self, ids=None, *args, **kwargs):
        if ids:
            return self.model.query.filter(self.model.id.in_(ids))
        return self.model.query

    def get_items(self, *args, **kwargs):
        """
        Работа с большим количество записей по модели.
        """
        args_pars = parser.parse_args()
        ids = args_pars['ids']
        filter_field = args_pars['filter_field']
        filter_text = args_pars['filter_text']
        sort_field = args_pars['sort_field']
        sort_course = args_pars['sort_course']
        page = args_pars['page']
        count = args_pars['count']

        if ids:
            ids = json.loads(ids)
            query = self.query_initial(ids, *args, **kwargs)
        else:
            query = self.query_initial(*args, **kwargs)



        records, max_, count_ = self.filter_query(
            query, filter_field, filter_text, sort_field, sort_course, page, count)

        return {'items': records, 'count': count_, 'max': max_}

    def put(self):
        """
        Сохранение новой записи.
        """
        try:
            data = request.json['data']
            good_stub = self.fill_obj(data)
            obj = self.pre_save(good_stub, data)
            obj = self.save_model(obj)
            db.session.flush()
            self.post_save(obj, data, create_new=True)
            db.session.commit()
        except BaseCanoniseResource.CanonException as exc:
            debug(unicode(exc))
            db.session.rollback()
            abort(400, message=unicode(exc))
        except Exception as exc:
            error(u"Ошибка при создании записи модели %s. %s", unicode(self.model.__class__.__name__), unicode(exc))
            db.session.rollback()
            raise
        else:
            pass
            # db.session.commit()
        return obj

    def get(self, id):
        """
        Получение объекта в форме JSON.
        """
        return self.model.query.get(id)

    def post(self, id):
        """
        Редактирование записи.
        """
        try:
            data = request.json['data']
            good_stub = self.fill_obj(data, self.get_by_id(id))
            obj = self.pre_save(good_stub, data)
            obj = self.save_model(obj)
            self.post_save(good_stub, data)
            db.session.commit()
        except BaseCanoniseResource.CanonException as exc:
            debug(unicode(exc))
            db.session.rollback()
            abort(400, message=unicode(exc))
        except Exception as exc:
            error(u"Ошибка при редактировании записи %d модели %s. %s", id, self.model.__class__.__name__, unicode(exc))
            db.session.rollback()
            raise
        else:
            pass
            # db.session.commit()
        return obj

    def delete(self, id):
        """
        Удаление записи.
        """
        try:
            obj = self.get_by_id(id)
            self.pre_delete(obj)
            db.session.delete(obj)
            self.post_delete(obj)
            db.session.commit()
        except BaseCanoniseResource.CanonException as exc:
            debug(unicode(exc))
            db.session.rollback()
            abort(400, message=unicode(exc))
        except Exception as exc:
            error(u"Ошибка при редактировании записи %d модели %s. %s", id, self.model.__class__.__name__, unicode(exc))
            db.session.rollback()
            raise


class BaseInnerCanon(BaseCanoniseResource):
    inner_model = None
    model = None
    attr_link = "items"

    prefix_url_with_id = "/<int:inner_id>/items/<int:id>"
    prefix_url_without_id = "/<int:inner_id>/items"

    def post(self, inner_id, id):
        error(u"Вызов post в BaseInnerCanon")
        raise
        pass

    def put(self, inner_id):
        error(u"Вызов put в BaseInnerCanon")
        raise
        pass

    def delete(self, inner_id, id):
        error(u"Вызов delete в BaseInnerCanon")
        raise
        pass

    def get(self, inner_id, id):
        error(u"Вызов get в BaseInnerCanon")
        raise
        pass

    def query_initial(self, inner_id, **kwargs):
        try:
            return getattr(self.inner_model.query.get(inner_id), self.attr_link)
        except Exception as exc:
            error(u"Ошибка в инициализации запроса. " + unicode(exc))
            raise exc


class ExtraMixin(object):
    def post_save(self, obj, data, create_new=True):
        super(ExtraMixin, self).post_save(obj, data, create_new)


class BaseModelPackResource(restful.Resource):
    model = None

    def get(self):
        args = parser.parse_args()

        filter_field = args['filter_field']
        filter_text = args['filter_text']
        sort_field = args['sort_field']
        sort_course = args['sort_course']
        page = args['page']
        count = args['count']

        query = self.model.query

        if filter_field and filter_text:
            query = query.filter(
                self.model.__table__.columns[filter_field].like("%"+filter_text+"%")
            )
        if sort_field and sort_course:
            query = query.order_by(
                {'desc': desc, 'asc': asc}[sort_course](self.model.__table__.columns[sort_field])
            )
        max_ = query.count()

        if page and count:
            query = query.offset((page - 1) * count).limit(count)
        mails = query.all()
        count_ = query.count()

        return {'items': mails, 'count': count_, 'max': max_}


class TokenResource(BaseTokeniseResource):

    def get(self):
        token = g.user.generate_auth_token()
        return jsonify({
            'token': token.decode('ascii')
        })


class ProfileResource(BaseTokeniseResource):
    def get(self):
        from services.userservice import UserService
        token = request.authorization['username']

        user = UserService.user_to_token(token)
        if user:
            fname = user.first_name or ""
            lname = user.last_name or ""
            position = u"Администратор" if user.is_superuser else u"Пользователь"

            name = " ".join([fname, lname]) if fname or lname else "Без имени"

            return jsonify({
                'name': name,
                'position': position,
                'iconUrl': "static/images/users/2.jpg",
                'is_superuser': user.is_superuser
            })
        else:
            abort(401)


class RegistrationResource(restful.Resource):
    def post(self):
        if request.json is None:
            abort(400, message=u"Пустые параметры")
        from services.userservice import UserService
        login = request.json.get('login')
        email = request.json.get('email')
        password = request.json.get('password')
        retypepassword = request.json.get('retypepassword')
        if login is None or email is None or password is None or retypepassword is None:
            abort(400, message=u"Недостаточно данных")
        if password != retypepassword:
            abort(400, message=u"Пароли не совпадают")

        if not UserService.check_duplicate(login, email):
            abort(400, message=u"Дупликат")

        user = UserService.registration(login, email, password)

        db.session.add(user)
        db.session.commit()

        return jsonify({
            'token': user.generate_auth_token().decode('ascii')
        })


class IdentityResource(BaseTokeniseResource):
    def get(self):
        from services.userservice import UserService
        token = request.authorization['username']

        user = UserService.user_to_token(token)
        if user:
            return jsonify({'identity': [x.name for x in user.roles]})
        abort(401)


class AuthResource(restful.Resource):
    def post(self):
        from applications.security.model import User

        def is_empty(at):
            return at in [None, ""]

        username = request.json.get('user')
        password = request.json.get('password')
        if is_empty(username) or is_empty(password):
            abort(400, message=u"Имя и пароль не должны быть пустыми.") # missing arguments
        user = User.query.filter(User.login==username).first()
        if not user or not user.verify_password(password):
            abort(400, message=u"Пользователя с указаными именем и паролем не найдены в системе.")

        if user.active is False:
            abort(400, message=u"Пользователь не активен. Обратитесь с администратору.")

        return jsonify({
            'token': user.generate_auth_token().decode('ascii')
        })
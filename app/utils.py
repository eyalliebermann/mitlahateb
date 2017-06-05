from flask import jsonify


def handle_error(error, status_code):
    resp = jsonify(error)
    resp.status_code = status_code
    return resp


class SQLAlchemyService(object):
    __model__ = None
    __db__ = None

    def save(self, obj):
        self._isinstance(obj)
        self.__db__.session.add(obj)
        self.__db__.session.commit()
        return obj

    def all(self):
        return self.__model__.query.all()

    def get(self, id):
        return self.__model__.query.get(id)

    def get_all(self, *ids):
        return self.__model__.query.filter(self.__model__.id.in_(ids)).all()

    def _find(self, **kwargs):
        return self.__model__.query.filter_by(**kwargs)

    def find(self, **kwargs):
        return self._find(**kwargs).all()

    def first(self, **kwargs):
        return self._find(**kwargs).first()

    def one(self, **kwargs):
        return self._find(**kwargs).one()

    def get_or_404(self, id):
        return self.__model__.query.get_or_404(id)

    def new(self, **kwargs):
        return self.__model__(**self._preprocess_params(kwargs))

    def update(self, model, **kwargs):
        self._isinstance(model)
        for k, v in self._preprocess_params(kwargs).items():
            setattr(model, k, v)
        self.save(model)
        return model

    def delete(self, obj):
        self._isinstance(obj)
        self.__db__.session.delete(obj)
        self.__db__.session.commit()

    def paginate(self, page=1, per_page=10, order_by=None, desc=False,
                 filter_by={}, error_out=True):
        order_by = order_by or self.__model__.id
        order_by = order_by.desc() if desc else order_by.asc()
        return self.__model__.query.filter_by(**filter_by).order_by(order_by) \
            .paginate(page, per_page, error_out)

    def _isinstance(self, obj, raise_error=True):
        rv = isinstance(obj, self.__model__)
        if not rv and raise_error:
            raise ValueError('%s is not of type %s' % (obj, self.__model__))
        return rv

    def _preprocess_params(self, kwargs):
        kwargs.pop('csrf_token', None)
        kwargs.pop('submit', None)
        return kwargs

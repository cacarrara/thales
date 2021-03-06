import uuid

from slugify import slugify
import sqlalchemy
from sqlalchemy import engine_from_config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import zope.sqlalchemy


NAMING_CONVENTION = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}


class Base:
    def __json__(self, request):
        json_exclude = getattr(self, '__json_exclude__', set())
        return {key: str(value) for key, value in self.__dict__.items()
                if not key.startswith('_') and key not in json_exclude}


metadata = sqlalchemy.MetaData(naming_convention=NAMING_CONVENTION)
ModelBase = declarative_base(cls=Base, metadata=metadata)


class Model(ModelBase):
    __abstract__ = True

    id = sqlalchemy.Column(
        sqlalchemy.String(36),
        primary_key=True,
        default=str(uuid.uuid4()),
    )


class NamedModel(Model):
    __abstract__ = True
    name = sqlalchemy.Column(sqlalchemy.String(200), unique=True)
    slug = sqlalchemy.Column(sqlalchemy.String(256), unique=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_slug()

    def set_slug(self):
        self.slug = slugify(self.name)

    def __str__(self):
        return self.name


def get_engine(settings, prefix='sqlalchemy.'):
    return engine_from_config(settings, prefix)


def get_session_factory(engine):
    factory = sessionmaker()
    factory.configure(bind=engine)
    return factory


def get_tm_session(session_factory, transaction_manager):
    dbsession = session_factory()
    zope.sqlalchemy.register(dbsession, transaction_manager=transaction_manager)
    return dbsession


def includeme(config):
    settings = config.get_settings()
    settings['tm.manager_hook'] = 'pyramid_tm.explicit_manager'

    config.include('pyramid_tm')

    session_factory = get_session_factory(get_engine(settings))
    config.registry['dbsession_factory'] = session_factory

    config.add_request_method(
        lambda r: get_tm_session(session_factory, r.tm),
        'db',
        reify=True
    )

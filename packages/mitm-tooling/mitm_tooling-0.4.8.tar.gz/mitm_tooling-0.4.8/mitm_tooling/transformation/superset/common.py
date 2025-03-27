from typing import Type

import pydantic
import sqlalchemy as sa
from pydantic import AnyUrl, ConfigDict

from mitm_tooling.representation import SchemaName
from mitm_tooling.representation.sql_representation import SQL_REPRESENTATION_DEFAULT_SCHEMA
from mitm_tooling.utilities.io_utils import FilePath
from mitm_tooling.utilities.sql_utils import create_sa_engine, dialect_cls_from_url, any_url_into_sa_url
from .definitions import StrUrl

SQLiteFileOrEngine = FilePath | sa.Engine


class DBConnectionInfo(pydantic.BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    sql_alchemy_uri: StrUrl
    explicit_db_name: str | None = None
    schema_name: SchemaName = SQL_REPRESENTATION_DEFAULT_SCHEMA
    catalog: str | None = None  # for future use

    @property
    def sa_url(self) -> sa.URL:
        return any_url_into_sa_url(self.sql_alchemy_uri)

    @property
    def db_name_in_uri(self) -> str:
        return self.sa_url.database

    @property
    def db_name(self) -> str:
        return self.explicit_db_name or self.db_name_in_uri

    @property
    def dialect_cls(self) -> Type[sa.engine.Dialect]:
        return dialect_cls_from_url(self.sql_alchemy_uri)


def _mk_engine(arg: SQLiteFileOrEngine) -> sa.Engine:
    if isinstance(arg, sa.Engine):
        return arg
    else:
        return create_sa_engine(AnyUrl(f'sqlite:///{str(arg)}'), poolclass=sa.pool.StaticPool)

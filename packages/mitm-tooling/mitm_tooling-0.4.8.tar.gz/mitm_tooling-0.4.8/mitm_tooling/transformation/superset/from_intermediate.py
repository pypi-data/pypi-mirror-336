from mitm_tooling.representation import Header
from .asset_bundles.asset_bundles import SupersetDatasourceBundle, \
    SupersetMitMDatasetBundle
from .common import DBConnectionInfo
from .definitions.mitm_dataset import MitMDatasetIdentifier


def header_into_superset_datasource_bundle(header: Header,
                                           db_conn_info: DBConnectionInfo) -> SupersetDatasourceBundle:
    from ..sql.from_intermediate import header_into_db_meta
    from .from_sql import db_meta_into_superset_datasource_bundle
    db_meta = header_into_db_meta(header)
    return db_meta_into_superset_datasource_bundle(db_meta, db_conn_info)


def header_into_mitm_dataset_bundle(header: Header,
                                    db_conn_info: DBConnectionInfo,
                                    dataset_identifier: MitMDatasetIdentifier) -> SupersetMitMDatasetBundle:
    from ..sql.from_intermediate import header_into_db_meta
    from .from_sql import db_meta_into_mitm_dataset_bundle
    db_meta = header_into_db_meta(header)
    return db_meta_into_mitm_dataset_bundle(db_meta, db_conn_info, dataset_identifier, header.mitm)

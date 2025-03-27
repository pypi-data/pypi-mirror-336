from typing import Literal

from mitm_tooling.transformation.superset.definitions import SupersetChartDef, SupersetVizType, ChartParams, \
    DatasourceIdentifier
from mitm_tooling.transformation.superset.definitions.mitm_dataset import MitMDatasetIdentifier
from mitm_tooling.transformation.superset.factories.chart import mk_chart_def
from mitm_tooling.transformation.superset.factories.query import mk_query_object, mk_query_context


class MAEDCustomChartParams(ChartParams):
    viz_type: Literal[SupersetVizType.MAED_CUSTOM] = SupersetVizType.MAED_CUSTOM
    mitm_dataset: MitMDatasetIdentifier


def mk_maed_custom_chart(name: str,
                         mitm_dataset_identifier: MitMDatasetIdentifier,
                         datasource_identifier: DatasourceIdentifier,
                         **kwargs) -> SupersetChartDef:
    params = MAEDCustomChartParams(datasource=datasource_identifier, mitm_dataset=mitm_dataset_identifier)
    qo = mk_query_object()
    qc = mk_query_context(datasource=datasource_identifier, queries=[qo], form_data=params)

    return mk_chart_def(name,
                        dataset_uuid=datasource_identifier.uuid,
                        viz_type=SupersetVizType.MAED_CUSTOM,
                        params=params,
                        qc=qc,
                        **kwargs)

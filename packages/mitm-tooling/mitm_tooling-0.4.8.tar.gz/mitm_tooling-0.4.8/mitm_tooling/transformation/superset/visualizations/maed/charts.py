from collections.abc import Sequence

from mitm_tooling.data_types import MITMDataType
from mitm_tooling.definition import get_mitm_def, ConceptName, MITM, RelationName, TypeName
from mitm_tooling.representation import SQLRepresentationSchema, Header, mk_sql_rep_schema
from mitm_tooling.utilities.identifiers import naive_pluralize
from ..abstract import DatasourceIdentifierMap, ChartDefCollection, ChartCollectionCreator, ChartCreator
from ...definitions import FilterOperator, DatasourceIdentifier, SupersetChartDef
from ...factories.core import mk_adhoc_filter
from ...factories.generic_charts import mk_pie_chart, mk_time_series_bar_chart, mk_avg_count_time_series_chart


class ConceptCountTS(ChartCreator):

    def __init__(self,
                 concept: ConceptName,
                 groupby_relations: Sequence[RelationName] = ('object',),
                 time_relation: RelationName = 'time'):
        self.concept = concept
        self.groupby_relations = list(groupby_relations)
        self.time_relation = time_relation
        props, rels = get_mitm_def(MITM.MAED).get(concept)
        self.props = props
        self.relations = rels
        defined_relations = set(self.relations.relation_names)
        assert set(self.groupby_relations) <= defined_relations
        assert self.time_relation in self.relations.relation_names

    def mk_chart(self, datasource_identifier: DatasourceIdentifier) -> SupersetChartDef:
        filters = [mk_adhoc_filter('kind',
                                   FilterOperator.EQUALS,
                                   self.props.key)] if self.props.is_sub else None
        return mk_time_series_bar_chart(f'{self.concept.title()} Counts',
                                        datasource_identifier,
                                        'type',
                                        MITMDataType.Text,
                                        x_col=self.time_relation,
                                        groupby_cols=self.groupby_relations,
                                        filters=filters
                                        )


class RelationPie(ChartCreator):

    def __init__(self, concept: ConceptName, relation: RelationName):
        self.relation = relation
        assert relation in get_mitm_def(MITM.MAED).get_relations(concept).relation_names

    def mk_chart(self, datasource_identifier: DatasourceIdentifier) -> SupersetChartDef:
        return mk_pie_chart(naive_pluralize(self.relation).title(),
                            datasource_identifier,
                            col=self.relation,
                            dt=MITMDataType.Text)


class ConceptTypeAvgCountTS(ChartCreator):

    def __init__(self,
                 concept: ConceptName,
                 type_name: TypeName,
                 groupby_relations: Sequence[RelationName] = ('object',),
                 time_relation: RelationName = 'time'):
        self.concept = concept
        self.type_name = type_name
        self.groupby_relations = list(groupby_relations)
        self.time_relation = time_relation
        props, rels = get_mitm_def(MITM.MAED).get(concept)
        self.props = props
        self.relations = rels
        defined_relations = set(self.relations.relation_names)
        assert set(self.groupby_relations) <= defined_relations
        assert self.time_relation in self.relations.relation_names

    def mk_chart(self, datasource_identifier: DatasourceIdentifier) -> SupersetChartDef:
        return mk_avg_count_time_series_chart(f'{self.type_name.title()} Time Series',
                                              datasource_identifier,
                                              groupby_cols=self.groupby_relations,
                                              time_col=self.time_relation,
                                              )


class ConceptTypesAvgCountTSCollection(ChartCollectionCreator):

    def __init__(self, concept: ConceptName, sql_rep_schema: SQLRepresentationSchema):
        super().__init__()
        self.sql_rep_schema = sql_rep_schema
        self.concept = concept
        assert self.concept in self.sql_rep_schema.type_tables

    def mk_chart_collection(self, ds_id_map: DatasourceIdentifierMap) -> ChartDefCollection:
        charts: ChartDefCollection = {}
        for type_name, tbl in self.sql_rep_schema.type_tables[self.concept].items():
            ds_id = ds_id_map[tbl.name]
            charts[f'{self.concept}-{type_name}-ts'] = ConceptTypeAvgCountTS(self.concept, type_name).mk_chart(ds_id)
        return charts


class BaselineMAEDCharts(ChartCollectionCreator):

    def __init__(self, header: Header, sql_rep_schema: SQLRepresentationSchema | None = None):
        super().__init__()
        self.header = header
        self.sql_rep_schema = sql_rep_schema or mk_sql_rep_schema(header)
        self.mitm_def = header.mitm_def

    def mk_chart_collection(self, ds_id_map: DatasourceIdentifierMap) -> ChartDefCollection:
        charts = {}
        observation_table_name = self.sql_rep_schema.concept_tables['observation'].name
        # alternatively, mk_table_name('observation')
        for sub_concept in self.mitm_def.sub_concept_map['observation']:
            charts[f'{sub_concept}-count-ts'] = ConceptCountTS(sub_concept).mk_chart(ds_id_map[observation_table_name])
        charts['observation-objects-pie'] = RelationPie('observation', 'object').mk_chart(
            ds_id_map[observation_table_name])
        charts.update(ConceptTypesAvgCountTSCollection('measurement',
                                                       self.sql_rep_schema).mk_chart_collection(ds_id_map))
        return charts

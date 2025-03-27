from abc import ABC, abstractmethod
from typing import Self, Type, Callable

from mitm_tooling.representation import TableName, Header
from ..asset_bundles.asset_bundles import SupersetVisualizationBundle
from ..definitions import DatasourceIdentifier, SupersetChartDef, \
    SupersetDashboardDef
from ..definitions.mitm_dataset import MitMDatasetIdentifier

ChartDefCollection = dict[str, SupersetChartDef]
DashboardDefCollection = dict[str, SupersetDashboardDef]
DatasourceIdentifierMap = dict[TableName, DatasourceIdentifier]


class ChartCreator(ABC):

    @abstractmethod
    def mk_chart(self, datasource_identifier: DatasourceIdentifier) -> SupersetChartDef:
        ...


class ChartCollectionCreator(ABC):

    @abstractmethod
    def mk_chart_collection(self, ds_id_map: DatasourceIdentifierMap) -> ChartDefCollection:
        ...

    @classmethod
    def cls_from_dict(cls, chart_creators: dict[str, tuple[TableName, ChartCreator]]) -> Type[Self]:
        chart_creators = dict(chart_creators)

        class ConcreteChartCollectionCreator(cls):

            def __init__(self, header: Header):
                super().__init__(header)
                self._chart_creators = chart_creators

            def mk_chart_collection(self, ds_id_map: DatasourceIdentifierMap) -> ChartDefCollection:
                return {name: cc.mk_chart(ds_id_map[table_name]) for name, (table_name, cc) in
                        self._chart_creators.items()}

        return ConcreteChartCollectionCreator


class DashboardCreator(ABC):

    @property
    @abstractmethod
    def chart_collection_creator(self) -> ChartCollectionCreator:
        ...

    @abstractmethod
    def mk_dashboard(self, chart_collection: ChartDefCollection) -> SupersetDashboardDef:
        ...

    def mk_bundle(self, ds_id_map: DatasourceIdentifierMap) -> SupersetVisualizationBundle:
        chart_collection = self.chart_collection_creator.mk_chart_collection(ds_id_map)
        return SupersetVisualizationBundle(charts=list(chart_collection.values()),
                                           dashboards=[self.mk_dashboard(chart_collection)])


class VisualizationCreator(ABC):

    def __init__(self, header: Header, **kwargs):
        self.header = header

    @property
    @abstractmethod
    def dashboard_creator_constructors(self) -> dict[str, Callable[
        [Header, MitMDatasetIdentifier], DashboardCreator]]:
        ...

    def mk_dashboard_bundles(self,
                             mitm_dataset_identifier: MitMDatasetIdentifier,
                             ds_id_map: DatasourceIdentifierMap) -> dict[str, SupersetVisualizationBundle]:
        return {name: constr(self.header, mitm_dataset_identifier).mk_bundle(ds_id_map) for name, constr in
                self.dashboard_creator_constructors.items()}

    def mk_bundle(self,
                  mitm_dataset_identifier: MitMDatasetIdentifier,
                  ds_id_map: DatasourceIdentifierMap) -> SupersetVisualizationBundle:
        bundle_map = self.mk_dashboard_bundles(mitm_dataset_identifier, ds_id_map)
        return SupersetVisualizationBundle.combine(*bundle_map.values())

    @classmethod
    def wrap_single(cls, dashboard_creator_constr: Callable[
        [Header, MitMDatasetIdentifier], DashboardCreator]) -> Type[Self]:
        dashboard_creator_constr_ = dashboard_creator_constr

        class ConcreteVisualizationCreator(cls):
            @property
            def dashboard_creator_constructors(self) -> dict[str, Callable[
                [Header, MitMDatasetIdentifier], DashboardCreator]]:
                return {'default': dashboard_creator_constr_}

        return ConcreteVisualizationCreator

    @classmethod
    def empty(cls) -> Type[Self]:
        class ConcreteVisualizationCreator(cls):
            @property
            def dashboard_creator_constructors(self) -> dict[str, Callable[
                [Header, MitMDatasetIdentifier], DashboardCreator]]:
                return {}

        return ConcreteVisualizationCreator

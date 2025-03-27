from mitm_tooling.definition import MITM
from mitm_tooling.representation import Header
from mitm_tooling.transformation.superset.definitions import SupersetDefFile, StrUUID, BaseSupersetDefinition, \
    SupersetId


class MitMDatasetIdentifier(BaseSupersetDefinition):
    dataset_name: str
    id: SupersetId | None = None
    uuid: StrUUID | None = None


class RelatedObjectIdentifier(BaseSupersetDefinition):
    id: SupersetId | None = None
    uuid: StrUUID


class RelatedTable(RelatedObjectIdentifier):
    table_name: str | None = None


class RelatedSlice(RelatedObjectIdentifier):
    slice_name: str | None = None


class RelatedDashboard(RelatedObjectIdentifier):
    dashboard_title: str | None = None


class SupersetMitMDatasetDef(SupersetDefFile):
    uuid: StrUUID
    dataset_name: str
    mitm: MITM
    mitm_header: Header | None = None
    database_uuid: StrUUID
    tables: list[RelatedTable] | None = None
    slices: list[RelatedSlice] | None = None
    dashboards: list[RelatedDashboard] | None = None
    version: str = '1.0.0'

    @property
    def identifier(self) -> MitMDatasetIdentifier:
        return MitMDatasetIdentifier(dataset_name=self.dataset_name, uuid=self.uuid)

    @property
    def filename(self) -> str:
        return self.dataset_name

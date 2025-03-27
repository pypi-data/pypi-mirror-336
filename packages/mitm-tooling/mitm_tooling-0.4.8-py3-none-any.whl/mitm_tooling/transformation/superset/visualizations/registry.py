from typing import Type

from mitm_tooling.definition import MITM
from mitm_tooling.representation import Header
from .maed.registry import MAEDVisualizationType, maed_visualization_creators
from ..definitions.mitm_dataset import MitMDatasetIdentifier
from ..visualizations.abstract import VisualizationCreator, DatasourceIdentifierMap, SupersetVisualizationBundle

VisualizationType = MAEDVisualizationType | None

mitm_visualization_creators = {
    MITM.MAED: maed_visualization_creators
}


def get_mitm_visualization_creator(mitm: MITM, visualization_type: VisualizationType) -> Type[
                                                                                             VisualizationCreator] | None:
    if creators := mitm_visualization_creators.get(mitm):
        if (creator := creators.get(visualization_type)) is not None:
            return creator


def mk_visualization(visualization_type: VisualizationType,
                     header: Header,
                     mitm_dataset_identifier: MitMDatasetIdentifier,
                     ds_id_map: DatasourceIdentifierMap) -> SupersetVisualizationBundle | None:
    if (creator := get_mitm_visualization_creator(header.mitm, visualization_type)) is not None:
        return creator(header).mk_bundle(mitm_dataset_identifier, ds_id_map)

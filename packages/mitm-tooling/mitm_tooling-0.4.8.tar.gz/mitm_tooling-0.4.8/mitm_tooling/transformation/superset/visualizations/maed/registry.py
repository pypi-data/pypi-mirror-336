from enum import StrEnum
from typing import Type

from mitm_tooling.transformation.superset.visualizations.abstract import VisualizationCreator
from mitm_tooling.transformation.superset.visualizations.maed.dashboards import BaselineMAEDDashboard, \
    ExperimentalMAEDDashboard


class MAEDVisualizationType(StrEnum):
    Baseline = 'baseline'
    Experimental = 'experimental'


maed_visualization_creators: dict[MAEDVisualizationType, Type[VisualizationCreator]] = {
    MAEDVisualizationType.Baseline: VisualizationCreator.wrap_single(lambda h, mdi: BaselineMAEDDashboard(h)),
    MAEDVisualizationType.Experimental: VisualizationCreator.wrap_single(lambda h, mdi: ExperimentalMAEDDashboard(h,
                                                                                                                  mdi)),
}

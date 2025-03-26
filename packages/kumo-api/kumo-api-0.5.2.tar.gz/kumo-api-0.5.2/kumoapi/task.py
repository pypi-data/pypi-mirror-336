from typing import List

from kumoapi.common import StrEnum


class TaskType(StrEnum):
    BINARY_CLASSIFICATION = 'binary_classification'
    MULTICLASS_CLASSIFICATION = 'multiclass_classification'
    MULTILABEL_CLASSIFICATION = 'multilabel_classification'
    MULTILABEL_RANKING = 'multilabel_ranking'
    REGRESSION = 'regression'
    TEMPORAL_LINK_PREDICTION = 'temporal_link_prediction'
    STATIC_LINK_PREDICTION = 'static_link_prediction'
    FORECASTING = 'forecasting'

    LINK_PREDICTION = 'link_prediction'  # Deprecated.

    @staticmethod
    def get_node_pred_tasks() -> List['TaskType']:
        return [
            TaskType.BINARY_CLASSIFICATION,
            TaskType.MULTICLASS_CLASSIFICATION,
            TaskType.MULTILABEL_CLASSIFICATION,
            TaskType.MULTILABEL_RANKING,
            TaskType.REGRESSION,
            TaskType.FORECASTING,
        ]

    @staticmethod
    def get_link_pred_tasks() -> List['TaskType']:
        return [
            TaskType.TEMPORAL_LINK_PREDICTION,
            TaskType.STATIC_LINK_PREDICTION,
            TaskType.LINK_PREDICTION,
        ]

    @staticmethod
    def get_classification_tasks() -> List['TaskType']:
        return [
            TaskType.BINARY_CLASSIFICATION,
            TaskType.MULTICLASS_CLASSIFICATION,
            TaskType.MULTILABEL_CLASSIFICATION,
        ]

from typing import List, Tuple

from kumoapi.common import StrEnum


class TrainingStage(StrEnum):
    TRAIN = 'train'
    VAL = 'val'
    TEST = 'test'
    PRED = 'pred'

    @staticmethod
    def list_stages() -> List['TrainingStage']:
        return [TrainingStage.TRAIN, TrainingStage.VAL, TrainingStage.TEST]

    def add_stage_prefix(self, name: str) -> str:
        return f'{self.value}_{name}'

    @classmethod
    def split_staged_name(cls, name: str) -> Tuple['TrainingStage', str]:
        stage, suffix = name.split('_', maxsplit=1)
        return cls(stage), suffix

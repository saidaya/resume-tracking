from dataclasses import dataclass, field
from typing import Optional
from typing import List


class SkillAnnotation:
    def __init__(self, skill: str):
        self.skill = skill

class ResponseData:
    def __init__(self, message: str, **kwargs):
        self.message = message
        self.data = kwargs

    def to_dict(self):
        return {'message': self.message, **self.data}

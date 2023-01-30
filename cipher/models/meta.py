from pydantic import BaseModel, Field


class Meta(BaseModel):
    meta_dict: dict = Field(default_factory=dict)

    def __getitem__(self, item):
        return self.meta_dict[item]

    def __setitem__(self, key, value):
        self.meta_dict[key] = value

    def to_dict(self):
        return self.meta_dict

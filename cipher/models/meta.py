from pydantic import BaseModel, Field


class Meta(BaseModel):
    meta_dict: dict = Field(default_factory=dict)

    def __getitem__(self, key):
        return self.meta_dict[key]

    def __setitem__(self, key, value):
        self.meta_dict[key] = value

    def get(self, key, default=None):
        return self.meta_dict.get(key, default)

    def to_dict(self):
        return self.meta_dict

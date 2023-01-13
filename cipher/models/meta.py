from pydantic import BaseModel, Field


class Meta(BaseModel):
    meta_dict: dict = Field(default_factory=dict)

    def __getattr__(self, item):
        if item in self.meta_dict:
            return self.meta_dict[item]
        else:
            return super().__getattribute__(item)

    def __setattr__(self, key, value):
        if hasattr(self, key):
            super().__setattr__(key, value)
        else:
            self.meta_dict[key] = value

    def __getitem__(self, item):
        return self.meta_dict[item]

    def __setitem__(self, key, value):
        self.meta_dict[key] = value

    def to_dict(self):
        return self.meta_dict

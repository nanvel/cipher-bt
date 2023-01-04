class DatasWrapper:
    def __init__(self, datas):
        self.datas = datas

    @property
    def df(self):
        return self.datas[0]

    def __getitem__(self, item):
        return self.datas[item]

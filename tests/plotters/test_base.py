from cipher.plotters import Plotter


class ExamplePlotter(Plotter):
    @classmethod
    def check_requirements(cls):
        pass

    def run(self, rows: list):
        pass


def test_extras_df(output):
    result = ExamplePlotter(output=output).extras_df

    assert len([i for i in result["base"] if i != 0]) == 25
    assert len([i for i in result["balance"] if i != 0]) == 38
    assert result["sessions_long_open"].notnull().any()
    assert not result["sessions_short_open"].notnull().any()

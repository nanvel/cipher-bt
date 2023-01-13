from cipher.use_cases import CreateStrategy

from .. import DATA_PATH


def test_name_to_class_name():
    use_case = CreateStrategy(templates_root=DATA_PATH / "templates")

    assert use_case._name_to_class_name("strategy") == "Strategy"
    assert use_case._name_to_class_name("my_strategy") == "MyStrategy"
    assert use_case._name_to_class_name("AStrategy") == "AStrategy"

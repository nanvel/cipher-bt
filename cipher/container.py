from pathlib import Path

from dependency_injector import containers, providers

from cipher.resources import init_logging
from cipher.services import DataService
from cipher.use_cases import CreateStrategy, InitRepository


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    logging = providers.Resource(init_logging, level=config.log_level)

    templates_root = providers.Object(Path(__file__).parent / "templates")

    data_service = providers.Singleton(DataService, cache_root=config.cache_root)

    init_repository = providers.Factory(InitRepository, templates_root=templates_root)
    create_strategy = providers.Factory(CreateStrategy, templates_root=templates_root)

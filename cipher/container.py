from pathlib import Path

from dependency_injector import containers, providers

from .resources import init_logging
from .services import DataService
from .settings import Settings
from .use_cases import CreateStrategy, InitRepository


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(pydantic_settings=[Settings()])

    logging = providers.Resource(init_logging, level=config.log_level)

    templates_root = providers.Object(Path(__file__).parent / "templates")

    data_service = providers.Singleton(DataService, cache_root=config.cache_root)

    init_repository = providers.Factory(InitRepository, templates_root=templates_root)
    create_strategy = providers.Factory(CreateStrategy, templates_root=templates_root)

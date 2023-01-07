from pathlib import Path

from dependency_injector import containers, providers

from .services import DataService
from .settings import Settings
from .use_cases import CreateRepository


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(pydantic_settings=[Settings()])

    templates_root = providers.Object(Path(__file__).parent / "templates")

    data_service = providers.Singleton(DataService, cache_root=config.cache_root)

    create_repository = providers.Factory(
        CreateRepository, templates_root=templates_root
    )

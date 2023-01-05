from dependency_injector import containers, providers

from .services import DataService
from .settings import Settings


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(pydantic_settings=[Settings()])

    data_service = providers.Singleton(DataService, cache_root=config.cache_root)

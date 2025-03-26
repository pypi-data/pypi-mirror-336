from .base import BaseProvider
from .null import NullProvider
from .cloudflare import CloudflareProvider
from ..settings import domain_settings


def get_domain_provider(name: str):
    return domain_settings.PROVIDERS.get(name)


__all__ = [
    "get_domain_provider",
    "BaseProvider",
    "NullProvider",
    "CloudflareProvider",
]

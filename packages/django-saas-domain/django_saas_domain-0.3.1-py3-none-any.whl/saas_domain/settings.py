from django.core.signals import setting_changed
from saas_base.settings import Settings

DEFAULTS = {
    'SUPPORTED_PROVIDERS': [],
    'BLOCKED_DOMAINS': [],
    'PROVIDERS': {},
}


class DomainSettings(Settings):
    IMPORT_PROVIDERS = [
        'PROVIDERS',
    ]

    def get_supported_providers(self):
        if self.SUPPORTED_PROVIDERS:
            return self.SUPPORTED_PROVIDERS
        return list(self.PROVIDERS.keys())


domain_settings = DomainSettings('SAAS_DOMAIN', defaults=DEFAULTS)
setting_changed.connect(domain_settings.listen_setting_changed)

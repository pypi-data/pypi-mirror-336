import typing as t
import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from saas_base.db import CachedManager

__all__ = ["Domain", "DomainManager"]


class DomainManager(CachedManager["Domain"]):
    natural_key = ["hostname"]

    def get_by_natural_key(self, hostname: str):
        return self.get_from_cache_by_natural_key(hostname)

    def get_tenant_id(self, hostname: str) -> t.Optional[int]:
        try:
            instance = self.get_by_natural_key(hostname)
            return instance.tenant_id
        except self.model.DoesNotExist:
            return None


class Domain(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    tenant = models.ForeignKey(settings.SAAS_TENANT_MODEL, on_delete=models.CASCADE)
    provider = models.CharField(max_length=100)
    hostname = models.CharField(max_length=100, unique=True)
    verified = models.BooleanField(default=False, editable=False)
    ssl = models.BooleanField(default=False, editable=False)
    active = models.BooleanField(default=False, editable=False)
    instrument_id = models.CharField(max_length=256, null=True, blank=True, editable=False)
    instrument = models.JSONField(blank=True, null=True, editable=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    objects = DomainManager()

    class Meta:
        verbose_name = _("domain")
        verbose_name_plural = _("domains")
        ordering = ['created_at']
        db_table = 'saas_domain'

    def __str__(self):
        return self.hostname

    @property
    def base_url(self) -> str:
        if self.ssl:
            return f'https://{self.hostname}'
        return f'http://{self.hostname}'

    def natural_key(self):
        return self.hostname,

    def disable(self):
        self.verified = False
        self.active = False
        self.ssl = False
        self.instrument = None
        self.save()

from django.db import models
from django.contrib.auth.models import User

from servers.utils import COUNTRIES

class Tag(models.Model):
    name = models.CharField(max_length=16)

    def __unicode__(self):
        return self.name

    def natural_key(self):
        return self.name

class Server(models.Model):
    name = models.CharField(max_length=16)
    owner = models.ForeignKey(User)
    location = models.CharField(max_length=2, choices=COUNTRIES)
    tags = models.ManyToManyField(Tag, blank=True)

    ipv4 = models.GenericIPAddressField(verbose_name='IPv4', protocol='ipv4',
            blank=True, null=True)
    ipv6 = models.GenericIPAddressField(verbose_name='IPv6', protocol='ipv6',
            blank=True, null=True)

    tor = models.CharField(max_length=64, blank=True)

    ssh_rsa_fingerprint = models.CharField(max_length=64, blank=True)
    ssh_dsa_fingerprint = models.CharField(max_length=64, blank=True)

    is_online = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    @property
    def domain(self):
        return '%s.darkscience.net' % self.name

    def as_dict(self):
        result = {}

        for field in ('name', 'ipv4', 'ipv6', 'tor', 'ssh_rsa_fingerprint',
                'ssh_dsa_fingerprint', 'is_online', 'location'):
            if getattr(self, field, None):
                result[field] = getattr(self, field)

        tags = [tag.name for tag in self.tags.all()]
        if tags and self.is_online:
            result['tags'] = tags

        result['owner'] = self.owner.username
        return result

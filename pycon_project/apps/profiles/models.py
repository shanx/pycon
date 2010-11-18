from django.db import models
from django.utils.translation import ugettext_lazy as _

from idios.models import ProfileBase


class Profile(ProfileBase):
    
    name = models.CharField(_("name"), max_length=100)
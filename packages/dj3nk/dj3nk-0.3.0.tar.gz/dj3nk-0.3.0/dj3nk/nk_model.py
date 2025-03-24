# -*- coding: utf-8 -*-
import importlib.util

if importlib.util.find_spec("django") is not None:
    from django.db import models
    from django.conf import settings

    from .natural_key_generator import NaturalKeyGenerator

    nature_key_generator = NaturalKeyGenerator(config=getattr(settings, "DJ3NK", None))

    def gnk() -> int:
        return nature_key_generator.generate_nk()

    class NKModel(models.Model):
        id = models.BigIntegerField("id", primary_key=True, default=gnk)

        class Meta:
            abstract = True

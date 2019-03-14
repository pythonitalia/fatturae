from django.db import models


class SenderManager(models.Manager):
    def get_for_user(self, user):
        return self.get_queryset().get(user=user)

from django.db import models


class StoreManagement(models.Model):
    is_open = models.BooleanField(default=False)

    def __str__(self):
        if self.is_open:
            return "Store is Open"
        else:
            return "Store is Closed"

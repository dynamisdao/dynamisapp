from django.db import models


class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class EthTransaction(TimestampModel):
    from_address = models.CharField(max_length=1023)
    to_address = models.CharField(max_length=1023)
    hash = models.CharField(max_length=127, unique=True)
    value = models.CharField(max_length=255)
    datetime = models.DateTimeField()
    confirmations = models.IntegerField()

    def eth_value(self):
        return int(self.value) * 0.000000000000000001

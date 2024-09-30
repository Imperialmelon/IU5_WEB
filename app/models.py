from django.db import models

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Cargo(models.Model):
    title = models.CharField(max_length=255, unique=True, blank=False, null=False)
    price_per_ton = models.IntegerField(validators=[MinValueValidator(1)])
    short_description = models.TextField()
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    logo_file_path = models.CharField(max_length=255, null=False, default="")

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'cargo'


class Shipping(models.Model):
    class RequestStatus(models.TextChoices):
        DRAFT = "DRAFT"
        DELETED = "DELETED"
        FORMED = "FORMED"
        COMPLETED = "COMPLETED"
        REJECTED = "REJECTED"

    status = models.CharField(
        max_length=10,
        choices=RequestStatus.choices,
        default=RequestStatus.DRAFT,
    )

    creation_datetime = models.DateTimeField(auto_now_add=True)
    formation_datetime = models.DateTimeField(blank=True, null=True)
    completion_datetime = models.DateTimeField(blank=True, null=True)
    organization = models.CharField(max_length=255)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_requests')
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managed_requests', blank=True, null=True)
    total_price = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'shipping'


class Shipping_Cargo(models.Model):
    shipping = models.ForeignKey(Shipping, on_delete=models.CASCADE)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    amount = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.shipping_id}-{self.cargo_id}"

    class Meta:
        db_table = 'cargoes_in_shipping'
        unique_together = ('cargo', 'shipping'),
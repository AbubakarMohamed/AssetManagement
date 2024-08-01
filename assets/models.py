from django.db import models
import uuid

class Asset(models.Model):
    ASSET_CHOICES = [
        ('Laptop', 'Laptop'),
        ('Desktop', 'Desktop'),
        ('Extension', 'Extension'),
        ('Banner', 'Banner'),
        ('Screen', 'Screen'),
    ]
    
    name = models.CharField(max_length=255)
    total_quantity = models.PositiveIntegerField()
    available_quantity = models.PositiveIntegerField()
    unique_id = models.CharField(max_length=50, unique=True)  # Change to CharField for custom prefix
    arrival_date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = self.generate_unique_id()
        super().save(*args, **kwargs)

    def generate_unique_id(self):
        prefix = "AMS-SPH-"
        base_id = uuid.uuid4().hex[:6].upper()  # Generate a unique part
        return f"{prefix}{base_id}"

    def __str__(self):
        return self.name


class Lend(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    lent_date = models.DateField(auto_now_add=True)
    returned_date = models.DateField(null=True, blank=True)
    condition = models.CharField(max_length=50, default='Good')
    quantity_good = models.PositiveIntegerField(null=True, blank=True, default=0)
    quantity_bad = models.PositiveIntegerField(null=True, blank=True, default=0)
    person_picking = models.CharField(max_length=100, blank=True, null=True)
    organisation = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    picking = models.DateField(null=True, blank=True)
    returning = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Lend of {self.quantity} {self.asset.name} ({self.condition})"


class Maintenance(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    maintenance_date = models.DateField(auto_now_add=True)
    is_fixed = models.BooleanField(default=False)

    def __str__(self):
        return f"Maintenance of {self.quantity} {self.asset.name} ({'Fixed' if self.is_fixed else 'Pending'})"

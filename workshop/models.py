from django.core.validators import MinValueValidator
from django.db import models
from utils.base_model import BaseModel


class Customer(BaseModel):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


class RepairItem(BaseModel):
    PRIORITY = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )

    serial_number = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    visual_status = models.TextField(blank=True, null=True)
    todo = models.TextField(blank=True, null=True)
    done = models.TextField(blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=False)
    priority = models.CharField(max_length=100, choices=PRIORITY, default='low')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='repair_items')

    def __str__(self):
        return self.serial_number

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Repair Item'
        verbose_name_plural = 'Repair Items'


class Estimate(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='estimates')
    name = models.CharField(max_length=100)
    converted = models.BooleanField(default=False)
    repair_item = models.ForeignKey(RepairItem, on_delete=models.CASCADE, related_name='estimates', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Estimate'
        verbose_name_plural = 'Estimates'


class Costs(BaseModel):
    COST_TYPE = (
        ("cost", "Cost"),
        ("profit", "Profit"),
    )
    name = models.CharField(max_length=100, null=True, blank=True)
    cost_type = models.CharField(max_length=100, choices=COST_TYPE)
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        validators=[
            MinValueValidator(0)
        ]
    )
    repair_item = models.ForeignKey(RepairItem, on_delete=models.CASCADE, related_name='costs', null=True, blank=True)
    estimate = models.ForeignKey(Estimate, on_delete=models.CASCADE, related_name='costs', null=True, blank=True)

    def __str__(self):
        return f"{str(self.amount)}-{self.cost_type}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Cost'
        verbose_name_plural = 'Costs'


class Notes(BaseModel):
    text = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='notes/', null=True, blank=True)
    repair_item = models.ForeignKey(RepairItem, on_delete=models.CASCADE, related_name='notes', null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='notes', null=True, blank=True)

    def __str__(self):
        return self.text[:20]

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'

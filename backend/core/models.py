from django.db import models

# Create your models here.
# DB項目を作成している

class Product(models.Model):
    sku = models.CharField(max_length=32, unique=True, db_index=True)
    name = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    reorder_point = models.IntegerField(default=0)
    safety_stock = models.IntegerField(default=0)
    def __str__(self): return f"{self.sku} {self.name}"

class Stock(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="stock")
    qty_on_hand = models.IntegerField(default=0)
    qty_reserved = models.IntegerField(default=0)

class SalesOrder(models.Model):
    status = models.CharField(max_length=16, default="CREATED")
    created_at = models.DateTimeField(auto_now_add=True)

class SalesOrderLine(models.Model):
    order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name="lines")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    qty = models.IntegerField()

class PurchaseOrder(models.Model):
    status = models.CharField(max_length=16, default="DRAFT")  # DRAFT, ORDERED, RECEIVED
    created_at = models.DateTimeField(auto_now_add=True)

class PurchaseOrderLine(models.Model):
    po = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name="lines")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    qty_ordered = models.IntegerField(default=0)
    qty_received = models.IntegerField(default=0)

class InboundReceipt(models.Model):
    po = models.ForeignKey(PurchaseOrder, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
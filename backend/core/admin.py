from django.contrib import admin

# Register your models here.
from .models import Product, Stock, SalesOrder, SalesOrderLine, PurchaseOrder, PurchaseOrderLine, InboundReceipt

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("sku", "name", "price", "reorder_point", "safety_stock")
    search_fields = ("sku", "name")

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("product", "qty_on_hand", "qty_reserved")

class SalesOrderLineInline(admin.TabularInline):
    model = SalesOrderLine
    extra = 0

@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "created_at")
    inlines = [SalesOrderLineInline]

class PurchaseOrderLineInline(admin.TabularInline):
    model = PurchaseOrderLine
    extra = 0

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "created_at")
    inlines = [PurchaseOrderLineInline]

@admin.register(InboundReceipt)
class InboundReceiptAdmin(admin.ModelAdmin):
    list_display = ("id", "po", "created_at")
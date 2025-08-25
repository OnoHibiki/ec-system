from rest_framework import serializers
from core.models import SalesOrder, SalesOrderLine, Product

class SalesOrderLineInSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    qty = serializers.IntegerField(min_value=1)

class CheckoutSerializer(serializers.Serializer):
    lines = SalesOrderLineInSerializer(many=True)

    def create(self, validated_data):
        order = SalesOrder.objects.create()
        for l in validated_data["lines"]:
            SalesOrderLine.objects.create(
                order=order,
                product_id=l["product_id"],
                qty=l["qty"],
            )
        return order

class InboundLineSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    qty_received = serializers.IntegerField(min_value=1)

class InboundSerializer(serializers.Serializer):
    po_id = serializers.IntegerField()
    receipts = InboundLineSerializer(many=True)
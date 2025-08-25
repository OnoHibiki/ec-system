from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core.services import allocate_inventory, receive_inbound
from .serializers import CheckoutSerializer, InboundSerializer

@api_view(["POST"])
def checkout(request):
    """
    カート確定 → SalesOrder作成 → 在庫引当（不足分はPO起票）
    """
    s = CheckoutSerializer(data=request.data)
    s.is_valid(raise_exception=True)
    order = s.save()
    allocate_inventory(order)
    return Response({"order_id": order.id, "status": order.status}, status=status.HTTP_201_CREATED)

@api_view(["POST"])
def inbound(request):
    """
    入荷確定 → 在庫加算・予約解放（簡易） → POステータス更新
    """
    s = InboundSerializer(data=request.data)
    s.is_valid(raise_exception=True)
    po = receive_inbound(s.validated_data["po_id"], s.validated_data["receipts"])
    return Response({"po_id": po.id, "status": po.status}, status=status.HTTP_200_OK)

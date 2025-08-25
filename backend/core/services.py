from django.db import transaction
from .models import Stock, SalesOrder, SalesOrderLine, PurchaseOrder, PurchaseOrderLine

class Shortage(Exception):
    pass

@transaction.atomic
def allocate_inventory(order: SalesOrder):
    """
    受注の各行について在庫引当。足りない分は仕入発注（DRAFT）を自動起票。
    """
    lines = order.lines.select_related("product").all()
    for line in lines:
        # 在庫行をロックして読み取り（同時実行対策）
        stock = Stock.objects.select_for_update(skip_locked=True).get(product=line.product)

        available = stock.qty_on_hand - stock.qty_reserved
        if available >= line.qty:
            stock.qty_reserved += line.qty
            stock.save(update_fields=["qty_reserved"])
        else:
            # 不足分は自動で発注起票（DRAFT）
            shortage = line.qty - available
            if available > 0:
                stock.qty_reserved += available
                stock.save(update_fields=["qty_reserved"])
            po, _ = PurchaseOrder.objects.get_or_create(status="DRAFT")
            PurchaseOrderLine.objects.create(po=po, product=line.product, qty_ordered=shortage)
    order.status = "ALLOCATED"
    order.save(update_fields=["status"])
    return order


@transaction.atomic
def receive_inbound(po_id: int, receipts: list[dict]):
    """
    入荷処理：{product_id, qty_received} の配列を受け取り、在庫を増やし、予約を解放する。
    """
    po = PurchaseOrder.objects.select_for_update().get(id=po_id)
    for r in receipts:
        pol = PurchaseOrderLine.objects.select_for_update().get(po=po, product_id=r["product_id"])
        pol.qty_received += int(r["qty_received"])
        pol.save(update_fields=["qty_received"])

        # 在庫を増やす
        stock = Stock.objects.select_for_update(skip_locked=True).get(product_id=r["product_id"])
        stock.qty_on_hand += int(r["qty_received"])
        stock.save(update_fields=["qty_on_hand"])

    # 一行でも入荷したら RECEIVED にしておく（最小仕様）
    po.status = "RECEIVED"
    po.save(update_fields=["status"])
    return po
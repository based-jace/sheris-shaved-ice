from .models import Item,Attributes,Type,Purchase,PurchaseItem

def item_creation(count,purchaseItem):
    if count == 0: 
        item_instance = Item.objects.create(item_id=purchaseItem.item_id,quantity=purchaseItem.quantity)
        item_instance.save()
    #if an item with a certain attribute exists it appends the quantity to it.
    if count > 0:
        item_instance = Item.objects.get(item_id=purchaseItem.item_id)
        item_instance.quantity += purchaseItem.quantity
        item_instance.save()
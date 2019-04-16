from decimal import Decimal
import datetime

from .models import Item, Attributes, Type, Purchase, PurchaseItem

class db_methods:
    @staticmethod
    def item_creation(count,purchaseItem):
        if count == 0: 
            item_instance = Item.objects.create(item_id=purchaseItem.item_id,quantity=purchaseItem.quantity)
            item_instance.save()
        #if an item with a certain attribute exists it appends the quantity to it.
        if count > 0:
            item_instance = Item.objects.get(item_id=purchaseItem.item_id)
            item_instance.quantity += purchaseItem.quantity
            item_instance.save()

    @staticmethod
    def add_item(atts):
        atts = dict(atts)
        item_keys = ['quantity']
        att_keys = ['name', 'description', 'type_id']
        item_stuff = {}
        att_stuff = {}

        for i in item_keys:
            if i in atts:
                item_stuff[i] = atts[i][0]

        for i in att_keys:
            if i in atts:
                att_stuff[i] = atts[i][0]

        type_id = Type.objects.get(id=int(att_stuff['type_id']) + 1 )
        att_stuff['type_id'] = type_id
        attributes = Attributes(**att_stuff)
        attributes.save()

        item_stuff['item_id'] = attributes
        item = Item(**item_stuff)
        item.save()

    @staticmethod
    def neworder(atts):
        purchase_stuff = {
            'total_amount': atts['cost'][0],
            'purchase_date': datetime.date.today(),
            #'item_id': item_id
        }

        purchase = Purchase(**purchase_stuff)
        purchase.save()

        #TODO set of a while loop to go through the different rows of orders.

        item = Item.objects.get(id=int(atts['attname'][0]) + 1) # PK starts at 1

        item_stuff = {
            'purchase_id': purchase,
            'item_id': item,
            'purchase_id':purchase,
            'quantity': atts['quantity'][0],
            'total_amount': atts['cost'][0]
        }

        purchase_item = PurchaseItem(**item_stuff)
        purchase_item.save()

        # pil_stuff = {
        #     'purchase_id': purchase,
        #     'items_id': item
        # }

        # purchase_item_link = PurchaseItemLink(**pil_stuff)
        # purchase_item_link.save()

        item.quantity += int(item_stuff['quantity'])
        item.save()

        #purchaseItem = PurchaseItem.objects.create(item_id=attributes[int(request.POST.get('attname'))],purchase_id=purchase,quantity=int(request.POST.get('quantity')),total_amount=Decimal(request.POST.get('cost')))
        #purchaseItem.save()
        #Checks to see if there are any instances of the object in the datbase
        #count = Item.objects.filter(item_id=purchaseItem.item_id).count()
        #Creates an item       
        #db_methods.item_creation(count,purchaseItem)

    @staticmethod
    def edititem(atts,item_id,attribute_id):

        type_id1 = atts['type_id']
        type_id = Type.objects.get(id=int(type_id1)+1 )

        attribute_stuff = {
            'id':attribute_id,
            'type_id':type_id,
            'name':atts['name'],
            'description':atts['description']
        }

        updated_attribute = Attributes(**attribute_stuff)
        updated_attribute.save()

        item_stuff = {
            'id':item_id,
            'item_id':updated_attribute,
            'quantity':atts['quantity']
        }

        updated_item = Item(**item_stuff)
        updated_item.save()
        
    @staticmethod
    def delete_selected(atts):        
        selected_stuff = atts.getlist('checkbox')
        
        for i in selected_stuff:
            attribute = Item.objects.get(pk=i).item_id            
            Item.objects.get(pk=i).delete()
            attribute.delete()


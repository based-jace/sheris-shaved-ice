from decimal import Decimal
import datetime
import json
from django.urls import reverse

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

        orderlist = []
        for item in atts['orderlist']:
            t = item.split(",")
            orderData = {
                'itemid':t[0],
                'quantity':t[1],
                'total_amount':t[2]
            }
            orderlist.append(orderData)
        
        cost = 0.0
        for order in orderlist:
            cost += float(order['total_amount'])

        purchase_stuff = {
            'total_amount': cost,
            'purchase_date': datetime.date.today(),
        }

        purchase = Purchase(**purchase_stuff)
        purchase.save()

        count = 0
        for order in orderlist:
            item = Item.objects.get(id=int(order['itemid'])) # PK starts at 1

            item_stuff = {
                'id':order.id,
                'purchase_id': purchase,
                'item_id': item,
                'quantity': int(order['quantity']),
                'total_amount': float(order['total_amount'])
            }

            purchase_item = PurchaseItem(**item_stuff)
            purchase_item.save()

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
            item = Item.objects.get(pk=i)
            item.available = False
            item.save()

    @staticmethod 
    def editorder(atts,orders,purchase):
        #TODO make it so you can remove entire PurchaseItems
        orderlist = []
        index = 0
        #Total amount of items changed
        difference = 0
        #TODO clean up the code by breaking it down into different functions
        #Unpacks the neccessary data and organizes it into a dictionary
        for order in orders:
            item = Item.objects.get(pk=int(atts.get("attname" + str(index))))
            orderitems = {
                'id':order.id,
                'item_id':item,
                'purchase_id':order.purchase_id,
                'quantity':atts.get("quantity" + str(index)),
                'total_amount':atts.get("cost" + str(index))
            }
            orderlist.append(orderitems)
            difference = int(atts.get("quantity" + str(index)))-order.quantity
            #Makes sure the item quantity cannot go below 0
            if item.quantity + difference > 0:
                item.quantity += difference
            else:
                item.quantity = 0
                item.available = False
            item.save()
            orderlist.append(orderitems)
            index += 1

        index = 0
        #Updates the existing order with the changed information
        for order in orders:
            order = PurchaseItem(**orderlist[index])
            order.save()
            index += 1
            # print(order.quantity)
            # order.item_id = Item.objects.get(id=int(atts['attname']))
            # order.quantity = atts['quantity']
            # order.total_amount = atts['cost']
            # order.save()

    @staticmethod
    def jsonify_items(items):
        if len(items) > 0:
            print(items[0].id)
            json_items = [{
                'id': item.id,
                'name': item.item_id.name,
                'quantity': item.quantity,
                'available': item.available,
                'type': item.item_id.type_id.name,
                'description': item.item_id.description,
                'edit_url': reverse('inv_manage:edititem', args=[item.id])
                } for item in items
            ]
            return json.dumps(json_items)

    
        
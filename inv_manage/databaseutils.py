import datetime
import json
from django.urls import reverse
from decimal import Decimal

from .models import Item, Attributes, Type, Purchase, PurchaseItem

class db_methods:

    @staticmethod
    def create_type(atts):
        newType = Type(name=atts.get("name"))
        newType.save()

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

        type_id = Type.objects.get(id=int(att_stuff['type_id']))
        att_stuff['type_id'] = type_id
        attributes = Attributes(**att_stuff)
        attributes.save()

        item_stuff['item_id'] = attributes
        item = Item(**item_stuff)
        item.save()

    @staticmethod
    def neworder(atts):
        #Grabs all the orders creates a dictionary with there data and adds them to a array
        orderlist = []
        for item in atts['orderlist']:
            t = item.split(",")
            orderData = {
                'itemid':t[0],
                'quantity':t[1],
                'total_amount':t[2]
            }
            orderlist.append(orderData)
        
        #sums the total amount of all purchase items
        cost = 0.0
        for order in orderlist:
            cost += float(order['total_amount'])

        purchase_stuff = {
            'total_amount': cost,
            'purchase_date': datetime.date.today(),
        }

        purchase = Purchase(**purchase_stuff)
        purchase.save()

        #Creates purhcase items and appends the new amount to the inventory item its associated with.
        count = 0
        for order in orderlist:
            item = Item.objects.get(id=int(order['itemid'])) # PK starts at 1

            item_stuff = {
                'purchase_id': purchase,
                'item_id': item,
                'quantity': int(order['quantity']),
                'total_amount': float(order['total_amount'])
            }

            purchase_item = PurchaseItem(**item_stuff)
            purchase_item.save()

            item.quantity += int(item_stuff['quantity'])
            item.save()

    @staticmethod
    def edititem(atts,item_id):
        type_id = atts['type_id']
        type_object = Type.objects.get(id=int(type_id))
        attribute_stuff = {
            'type_id':type_object,
            'name':atts['name'],
            'description':atts['description']
        }

        updated_attributes = Attributes.objects.get(pk=int(item_id))

        for i, j in zip(attribute_stuff.keys(), attribute_stuff.values()):
            setattr(updated_attributes, i, j)

        updated_attributes.save()

        item_stuff = {
            'id':item_id,
            'item_id':updated_attributes,
            'quantity':atts['quantity']
        }

        updated_item = Item(**item_stuff)
        updated_item.save()
        
    @staticmethod
    def delete_selected(atts):       
        selected_stuff = atts.getlist('checkbox[]')
        for i in selected_stuff:          
            item = Item.objects.get(pk=i)
            item.available = False
            item.save()

    @staticmethod
    def delete_orders(orders):       
        selected_stuff = orders.getlist('checkbox[]')
        for i in selected_stuff:     
            print(i)     
            Purchase.objects.get(pk=i).delete()

    # update = 0
    # delete = -1
    # create new = -2
    @staticmethod 
    def editorder(atts,purchase):
        orderData = []
        for order in atts.getlist('orderlist'):
            #
            # 0 = create new or purchaseItem id, 1 = item id, 2 = quantity, 3 = cost for item, 4 = update,delete codes
            splitdata = order.split(',')
            item = Item.objects.get(id=int(splitdata[1]))
            #make a new purchaseItem
            if splitdata[0] == '-2' and splitdata[4] == '0':               
                purchaseItem = {
                    'item_id':item,
                    'purchase_id':purchase,
                    'quantity':int(splitdata[2]),
                    'total_amount':Decimal(splitdata[3])
                }
                if item.available == True:
                    item.quantity += purchaseItem['quantity']
                    item.save()
                purchase.total_amount += purchaseItem['total_amount']
                purchase.save()
                orderData.append(purchaseItem)
            else:
                #update an item
                if splitdata[4] == '0':
                    purchaseItem = {
                    'id':int(splitdata[0]),
                    'item_id':item,
                    'purchase_id':purchase,
                    'quantity':int(splitdata[2]),
                    'total_amount':Decimal(splitdata[3])
                    }
                    #TODO change it so that when changing the item associated with the purchaseItem and the quantity/total_amount 
                    #it deletes teh old purchase item and creates a new one
                    orderItem = PurchaseItem.objects.get(id=purchaseItem['id'])
                    if item.available == True and purchaseItem['item_id'] == orderItem.item_id:                        
                        item.quantity += (purchaseItem['quantity'] - orderItem.quantity)
                        item.save()
                    elif item.available == True and purchaseItem['item_id'] != orderItem.item_id:
                        item.quantity += purchaseItem['quantity']
                        item.save()
                        orderItem.item_id.quantity -= orderItem.quantity
                        orderItem.item_id.save()
                        orderItem.delete()
                    purchase.total_amount += (purchaseItem['total_amount'] - orderItem.total_amount)
                    purchase.save()
                    orderData.append(purchaseItem)
                #delete an item
                elif splitdata[4] == '-1' and splitdata[0] != '-2':
                    deleteItem = PurchaseItem.objects.get(id=int(splitdata[0]))
                    item.quantity -= deleteItem.quantity
                    item.save()
                    purchase.total_amount -= deleteItem.total_amount
                    purchase.save()
                    deleteItem.delete()

        for order in orderData:
            purchase = PurchaseItem(**order)    
            purchase.save()   

    @staticmethod
    def jsonify_items(items):
        json_items = []
        if len(items) > 0:
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

    @staticmethod
    def jsonify_orders(orders):
        json_items = []
        print(json_items)
        if len(orders) > 0:
            json_items = [{
                'id': order.id,
                'date': str(order.purchase_date),
                'num_items': len((PurchaseItem.objects.filter(purchase_id = order.id))),
                'total': "$" + str(order.total_amount),
                'edit_url': reverse('inv_manage:editorder', args=[order.id]),
            } for order in orders
        ]
        return json.dumps(json_items)
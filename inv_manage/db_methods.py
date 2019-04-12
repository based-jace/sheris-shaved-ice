from .models import Item, Purchase, Attributes, Type

class db_methods:
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
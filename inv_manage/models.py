from django.db import models

# Create your models here.

class Type(models.Model):
    name = models.CharField(max_length=32)
    def __str__(self):
        return self.name

class Attributes(models.Model):
    type_id = models.ForeignKey(Type,on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256,blank=True,null=True)
    def __str__(self):
        return self.name + " - " + self.type_id.name

    #TODO talk to team about creation of items
class Item(models.Model):
    item_id = models.ForeignKey(Attributes,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    def __str__(self):
        return self.item_id.name

class Purchase(models.Model):
    #item_id = models.ForeignKey(PurchaseItemLink,on_delete=models.CASCADE)
    purchase_date = models.DateField('purchase date')
    total_amount = models.DecimalField(max_digits=10,decimal_places=2)
    
# class PurchaseItemLink(models.Model):
#     purchase_id = models.ForeignKey(Purchase,on_delete=models.CASCADE)
#     items_id = models.ForeignKey(Item,on_delete=models.CASCADE)

class PurchaseItem(models.Model):
    item_id = models.ForeignKey(Item,on_delete=models.CASCADE)
    purchase_id = models.ForeignKey(Purchase,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_amount = models.DecimalField(max_digits=10,decimal_places=2)

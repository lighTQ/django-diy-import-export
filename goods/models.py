from django.db import models

# Create your models here.

class Goods(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Books(models.Model):
    def func(self):
        return "unkonw publish "
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    price = models.IntegerField()
    publish = models.ForeignKey(to='Publish', on_delete=models.SET(func))

    def get_book_name(self):
        return "经典名著：《"+self.name+"》"

    def publish_detail(self):
        return {'name':self.publish.name,'addr':self.publish.addr}

#
class Publish(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,unique=True)
    addr = models.CharField(max_length=100,default='BJ')
#
    # def __str__(self):
    #     import json
    #     return json.dumps({'name':self.name, 'addr':self.addr})
        # return self.name


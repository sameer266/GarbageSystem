from django.db import models

from ckeditor.fields import RichTextField


class AboutUS(models.Model):
    company_name=models.CharField(max_length=100)
    logo= models.ImageField(upload_to='logoimage/')
    address = models.CharField(max_length=1000)
    email = models.EmailField()
    contactNo= models.CharField(max_length=15)
   
    class Meta:
        ordering =['-id']
        
        
class PrivacyPolicy(models.Model):
    title=models.CharField(max_length=200)
    description=RichTextField()
    
    
class Customers(models.Model):
    companyName=models.CharField(max_length=200)
    ownerName=models.CharField(max_length=200)
    address=models.CharField(max_length=200)
    phoneNo=models.PositiveBigIntegerField()
  
    def __str__(self):
        return self.ownerName
    
    class Meta:
        ordering =['-id']
        
from django.db import models



class AboutUS(models.Model):
    company_name=models.CharField(max_length=100)
    logo= models.ImageField(upload_to='logoimage/')
    address = models.CharField(max_length=1000)
    email = models.EmailField()
    contactNo= models.CharField(max_length=15)
   
    class Meta:
        ordering =['-id']
        
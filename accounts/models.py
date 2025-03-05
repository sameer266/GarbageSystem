from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin

#  Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email,  name=None, phone_no=None, password=None, password2=None,address=None,**extra_fields):
      
      if not email:
          raise ValueError('User must have an email address')

      user = self.model(
          email=self.normalize_email(email),
          name=name,
          phone_no= phone_no,
          address= address
      )

      user.set_password(password)
      user.is_user = True
      user.save(using=self._db)
      return user

    def create_superuser(self, email,name=None, phone_no=None, password=None,**extra_fields):
      user = self.create_user(
          email,
          password=password,
          name=name,
          phone_no= phone_no
      )
      user.is_admin = True
      user.is_superuser =True
      user.save(using=self._db)
      return user

#  Custom User Model
class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=200,null=True, blank=True)
    is_user = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_agent= models.BooleanField(default=False)
    is_sub_admin=models.BooleanField(default=False)
    phone_no = models.CharField(max_length=150, null=True, blank=True)
    address = models.CharField(max_length=150, null=True, blank=True )
    image = models.ImageField(upload_to="image/", null=True, blank=True)
    
    activate = models.BooleanField(default =False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_no','name']



    @property
    def is_staff(self):
        return self.is_admin +self.is_agent +self.is_user
        
        
    def __str__(self):
        return self.name







       
class UserOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_otp')
    otp_code = models.CharField(max_length=50)
    otp_code_expiration = models.DateTimeField()
    def __str__(self):
        return str(self.user.name) + str(self.otp_code)
        
        
        
''' reward points for user based on order '''
class Reward(models.Model):
    percentage = models.FloatField(default=0)

    def __str__(self):
        return f"{self.percentage}%"

class UserReward(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,limit_choices_to={'is_user': True}, related_name='user_rewards')
    points = models.FloatField(default=0)
    total_transaction_amount = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user.name} - {self.points} points"

class UserRedeem(models.Model):
    reward = models.ForeignKey(UserReward, on_delete=models.CASCADE, related_name='user_redemptions')
    redeem_points = models.FloatField()
    redeem_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reward.user.name} redeemed {self.redeem_points} points on {self.redeem_date}"
    
    
    
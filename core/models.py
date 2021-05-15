from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.contrib.auth import get_user_model
import logging



logger = logging.getLogger(__name__)



class UserManager(BaseUserManager):
    
    def create_user(self, password = None, **exta_fields):
        """This method is to create user"""
        # if not email:
        #     raise ValueError("Invalid Email address")
        user = self.model( **exta_fields)
        user.set_password(password)

        user.save(using = self._db)

        return user

    def create_superuser(self, **exta_fields):
        user = get_user_model().objects.create_user(**exta_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using = self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """This is a Custom user  model use user_id insted of username"""

    facebook_image = models.CharField(null=True,blank=True,max_length = 255)
    user_id = models.CharField(max_length = 255,unique = True)
    facebook_name = models.CharField(null=True,blank=True,max_length = 255)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    facebook_id = models.CharField(max_length=255,blank=True,null=True,unique = True)
    friend =  ArrayField(models.CharField(max_length=255,null=True),null=True,blank=True)
    flag = models.CharField(max_length = 50)
    token = models.CharField(max_length = 255,null=True)

    objects = UserManager()

    USERNAME_FIELD = 'user_id'

    def __str__(self):
        return self.user_id

class League(models.Model):
    profiles =  models.ManyToManyField('Profile', blank=True)
    name = models.CharField(max_length = 100)
    image = models.CharField(max_length = 255)
    # end = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    first_prize = models.IntegerField()
    scond_prize = models.IntegerField()
    rest_prize = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
    



        
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL , on_delete= models.CASCADE)
    my_league = models.ForeignKey(
            League,
            on_delete = models.PROTECT,null=True)
    send_friend =  ArrayField(models.CharField(max_length=255,null=True),null=True,blank=True)
    friends =  models.ManyToManyField('Profile',related_name='friend', blank=True)
    facebook_id = models.CharField(max_length=255,blank=True,null=True,unique = True)
    name = models.CharField(max_length = 100)
    image = models.CharField(max_length = 255)
    level = models.IntegerField(default=1)
    next_level = models.IntegerField(default=100)
    score = models.IntegerField(default=0)
    win = models.IntegerField(default=0)
    loss = models.IntegerField(default=0)
    draw = models.IntegerField(default=0)
    next_gift = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    coins = models.IntegerField(default=2000)
    gem = models.IntegerField(null=True)
    league_coins = models.IntegerField(default=0)
    flag = models.CharField(max_length = 50)
    token = models.CharField(max_length = 255,null=True)
    is_active=models.BooleanField(default=False)
    daily_coins=models.BooleanField(default=False)
    league_prize=models.BooleanField(default=False)

    l_prize = models.IntegerField(default=0,null=True,blank=True)
    l_rank = models.IntegerField(default=0,null=True,blank=True)
    l_coins = models.IntegerField(default=0,null=True,blank=True)
    l_league = models.CharField(max_length = 40,null=True,blank=True)
    l_next = models.CharField(max_length = 40,null=True,blank=True)
    l_image = models.CharField(max_length = 255,null=True,blank=True)
    

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-league_coins']


class Question(models.Model):
    question = models.CharField(max_length = 455, unique=True)
    category = models.CharField(max_length = 255)
    answer = models.CharField(max_length = 255)
    obtion1 = models.CharField(max_length = 255,blank=True)
    obtion2 = models.CharField(max_length = 255,blank=True)
    obtion3 = models.CharField(max_length = 255,blank=True)
    obtion4 = models.CharField(max_length = 255,blank=True)
    image = models.CharField(max_length = 255,blank=True)
    time = models.IntegerField()
    question_type = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question


class Answer(models.Model):

    room= models.ForeignKey(
            'Room',
            related_name='room',
            on_delete = models.CASCADE)
    player1_id = models.IntegerField(null=True,blank=True)
    player2_id = models.IntegerField(null=True,blank=True)
    player1_score = models.IntegerField(null=True,blank=True)
    player2_score = models.IntegerField(null=True,blank=True)
    player1_answer = models.CharField(max_length = 255,null=True,blank=True)
    player2_answer = models.CharField(max_length = 255,null=True,blank=True)
    question = models.CharField(max_length = 455)
    category = models.CharField(max_length = 255)
    correct = models.CharField(max_length = 255)
    question_num = models.IntegerField()
    

    def __str__(self):
        return str(self.id)


class Room(models.Model):
    questions = models.ManyToManyField(Question,related_name='questions',blank=True)
    category = models.CharField(max_length=100)
    avaliable = models.BooleanField(default=True)
    player1 = models.ForeignKey(
            Profile,
            related_name='player1',
            on_delete = models.CASCADE,null=True)
    player2 = models.ForeignKey(
            Profile,
            related_name='player2',
            on_delete = models.CASCADE,null=True)
    is_facebook=models.BooleanField(default=False,null=True)
    is_random=models.BooleanField(default=False,null=True)
    started=models.BooleanField(default=False)
    finished=models.BooleanField(default=False)
    take_prize=models.BooleanField(default=False)
    players_answer = models.ManyToManyField(Answer,related_name='players_answer',blank=True)
    player1_prize = models.IntegerField()
    player2_prize = models.IntegerField(null=True)
    player1_profile = models.IntegerField()
    player2_profile = models.IntegerField(default=0,null=True,blank=True)
    player1_score = models.IntegerField(default=0)
    player2_score = models.IntegerField(default=0)
    player1_left = models.BooleanField(default=False)
    player2_left = models.BooleanField(default=False)
    player1_answered = models.IntegerField(default=0)
    player2_answered = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

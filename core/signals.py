from django.db.models.signals import post_save
from .models import User
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
import random
from .models import Profile, League,Room
from push_notifications.models import  GCMDevice


def checkLevel(instance):
    if instance.score >= instance.next_level:
        instance.level+=1
        print("Level "+str(instance.level))
        instance.next_level=instance.next_level*2
        instance.save()
    else:
        print("no Level")


@receiver(post_save, sender=Room)
def post_save_room_prize(sender, instance, created, **kwargs):

    # 

    if instance.started and not instance.take_prize:
       

        if instance.players_answer.count()==5 or instance.player1_left or instance.player2_left and not instance.take_prize:

        
            if instance.player1_left :
                
                # instance.player1_left=False
                # winner
                profile=Profile.objects.get(pk=instance.player2.id)
                checkLevel(profile)
                print("winner "+str(profile.name))
                profile.coins+=instance.player2_prize*2
                profile.score+=instance.player2_score
                profile.win+=1
                if not instance.is_facebook:
                    profile.league_coins+=instance.player2_prize*2
                instance.take_prize=True
                profile.save()
                instance.player1_answered+=1
                instance.save()
            # losser
                losser=Profile.objects.get(pk=instance.player1.id)
                losser.loss+=1
                print("losser "+str(losser.name))
                losser.save()


            if instance.player2_left :
            # winner
                instance.player2_left=False
                profile=Profile.objects.get(pk=instance.player1.id)
                checkLevel(profile)
                profile.coins+=instance.player1_prize*2
                profile.score+=instance.player1_score
                profile.win+=1
                print("winner "+str(profile.name))
                if not instance.is_facebook:
                    profile.league_coins+=instance.player1_prize*2
                instance.take_prize=True
                profile.save()
                instance.player1_answered+=1
                instance.save()
            # losser
                losser=Profile.objects.get(pk=instance.player2.id)
                print("losser "+str(losser.name))
                losser.loss+=1
                losser.save()
                
                

            if instance.player2_answered == instance.player1_answered:

                if instance.player1_score==instance.player2_score:
                    profile1=Profile.objects.get(pk=instance.player1.id)
                    profile2=Profile.objects.get(pk=instance.player2.id)
                    checkLevel(profile1)
                    checkLevel(profile2)
                    instance.take_prize=True
                    profile1.draw+=1
                    profile2.draw+=1
                    instance.player1_answered+=1
                    instance.save()
                    profile2.save()
                    profile1.save()

                if instance.player1_score<instance.player2_score:
                    profile=Profile.objects.get(pk=instance.player2.id)
                    checkLevel(profile)
                    print("winner "+str(profile.name))
                    
                    profile.coins+=instance.player2_prize*2
                    instance.take_prize=True
                    profile.score+=instance.player2_score
                    profile.win+=1
                    if not instance.is_facebook:
                        profile.league_coins+=instance.player2_prize*2
                    profile.save()
                    instance.player1_answered+=1
                    instance.save()
                # losser
                    losser=Profile.objects.get(pk=instance.player1.id)
                    checkLevel(losser)
                    losser.loss+=1
                    print("losser "+str(losser.name))
                    losser.save()
                    

                elif instance.player2_score<instance.player1_score:
                    # winner
                
                    profile=Profile.objects.get(pk=instance.player1.id)
                    checkLevel(profile)
                    profile.coins+=instance.player1_prize*2
                    profile.score+=instance.player1_score
                    profile.win+=1
                    instance.take_prize=True
                    print("winner "+str(profile.name))
                    if not instance.is_facebook:
                        profile.league_coins+=instance.player1_prize*2
                    profile.save()
                    instance.player1_answered+=1
                    instance.save()
                # losser
                    losser=Profile.objects.get(pk=instance.player2.id)
                    checkLevel(losser)
                    print("losser "+str(losser.name))
                    losser.loss+=1
                    losser.save()


@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created and not instance.is_staff:
        Profile.objects.create(user= instance,my_league_id=1)
        profile = Profile.objects.get(user= instance)
        profile.token=instance.token
        GCMDevice.objects.create(
            registration_id=instance.token, 
            cloud_message_type="FCM",
            user=instance)

        if instance.facebook_id:
            profile.name=instance.facebook_name
            profile.image=instance.facebook_image
            profile.gem=5
            profile.flag=instance.flag
            profile.facebook_id=instance.facebook_id
           
        else:
            profile.name='Guest'+str(random.randrange(20, 5000, 3))
            profile.image='https://easyquzy.herokuapp.com/static/media/8.png'
            profile.gem=2
            profile.flag=instance.flag
        
        friend=instance.friend
        if friend :
           
            for item in friend:
                try:
                    user=Profile.objects.get(facebook_id=item)
                    profile.friends.add(user)
                    user.friends.add(profile)
                    user.save()
                except ObjectDoesNotExist:
                    pass

        profile.save()
        league=League.objects.get(pk=1)
        league.profiles.add(Profile.objects.get(user=instance))
        league.save()

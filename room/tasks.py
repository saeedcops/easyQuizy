
# Create your tasks here
from __future__ import absolute_import, unicode_literals
import time
from celery import shared_task
from app.celery import app
from core.models import League,Profile,User,Room,Answer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from push_notifications.models import  GCMDevice
import random

channel_layer = get_channel_layer()

def send_notification(user,message,icon,league,prize,coins=None,rank=None,next_league=None):
    fcm_device = GCMDevice.objects.get(
            cloud_message_type="FCM",
            user=User.objects.get(pk=user))

    fcm_device.send_message(message,extra={
             "icon":icon,
             "prize": prize,
             "coins": coins,
             "rank":rank,
             "next":next_league,
             "league":league})

# @transaction.atomic

def send_answer(room,question,q_num,timer):
    
    score=question.time-timer
    answer=question.answer.split('|')[1]
    # time.sleep(timer)
    room.player2_score+=score
    room.player2_answered=q_num
    room.save()

    try:
        answer_o=Answer.objects.get(room=room,question=question.question.strip(),question_num=q_num)

        answer_o.player2_id=room.player2_profile
        answer_o.player2_score=score
        answer_o.player2_answer=answer
        answer_o.save()
        room.save()
        

    except Answer.DoesNotExist:
        
        answer_o=Answer.objects.create(room=room,player1_id=0,player2_id=room.player2_profile,
                                player2_score=score,player2_answer=answer,question=question.question.strip(),
                                category=question.category,correct=question.answer,question_num=q_num)
        room.players_answer.add(answer_o)
        room.save()
        
    async_to_sync(channel_layer.group_send)(
            str(room.id), {
                'type': 'recieve_group_message',
                    'player1score':room.player1_score,
                    'player2score':room.player2_score,
                    'sender':room.player2_profile,
                    'question':q_num
            })

@shared_task
def random_room(room_id:int):
    
    # 
    room=Room.objects.get(pk=room_id)
    
    async_to_sync(channel_layer.group_send)(
        str(room_id), {
            'type': 'recieve_group_message',
                'player1score':-2,
                'player2score':-2,
                'sender':2,
                'question':1
        })

    q_num=0

    for question in room.questions.all():
        
        timer= random.randint(4,question.time-1)
        # timer=5
        time.sleep(timer)
        room=Room.objects.get(pk=room_id)

        if room.player1_answered == room.player2_answered:
            q_num+=1
            
            send_answer(room=room,question=question,q_num=q_num,timer=timer)
            
            room =Room.objects.get(pk=room_id)
            if room.player1_left:
                # print("player1_left")
                room.delete()
                break

            if room.player1_answered == room.player2_answered:
                continue
            else:
                while room.player1_answered < room.player2_answered:
                    # print("player2_answered >> "+str(q_num))
                    time.sleep(1)
                    room =Room.objects.get(pk=room_id)
                    if room.player1_left:
                        # print("player1_left")
                        room.delete()
                        break
                    
            continue

        elif room.player1_answered > room.player2_answered:
            q_num+=1
            if room.player1_left:
                # print("player1_left")
                room.delete()
                break
            send_answer(room=room,question=question,q_num=q_num,timer=timer)
           
            continue
   

    return str(room_id)


@app.task(name='tasks.league_prize')
def league_prize():

    bronze=League.objects.get(name='Bronze')
    silver=League.objects.get(name='Silver')
    gold=League.objects.get(name='Gold')
    diamond=League.objects.get(name='Diamond')
    legendary=League.objects.get(name='Legendary')

    bronze_profiles=[profile for profile in bronze.profiles.all()]
    silver_profiles=[profile for profile in silver.profiles.all()]
    gold_profiles=[profile for profile in gold.profiles.all()]
    diamond_profiles=[profile for profile in diamond.profiles.all()]
    legendary_profiles=[profile for profile in legendary.profiles.all()]

    bronze.profiles.clear()
    silver.profiles.clear()
    gold.profiles.clear()
    diamond.profiles.clear()

    bronze.save()
    silver.save()
    gold.save()
    diamond.save()

    sum=0
# BRONZE
    for profile in bronze_profiles:
        prize=0
        coins= profile.league_coins
        profile.league_coins=0
            
        if sum==0:
                
            profile.gem+=bronze.first_prize
            prize=bronze.first_prize
                
        elif sum==1:
                
            profile.gem+=bronze.scond_prize
            prize=bronze.scond_prize

        elif sum>1 and sum<5:
                
            profile.gem+=bronze.rest_prize
            prize=bronze.rest_prize

        silver.profiles.add(profile)
        sum+=1
        profile.my_league=silver
        profile.l_prize =prize
        profile.l_rank =sum
        profile.l_coins =coins
        profile.l_league =bronze.name
        profile.l_next =silver.name
        profile.l_image =bronze.image
        profile.league_prize=True
    
        profile.save()
        silver.save()
        
        send_notification(profile.user.id,"League",bronze.image,bronze.name,prize,coins,sum,silver.name)

    sum=0
# SILVER
    for profile in silver_profiles:
        coins= profile.league_coins
        profile.league_coins=0
        prize=0
            
        if sum==0:
                
            profile.gem+=silver.first_prize
            prize=silver.first_prize
                
        elif sum==1:
                
            profile.gem+=silver.scond_prize
            prize=silver.scond_prize

        elif sum>1 and sum<5:
                
            profile.gem+=silver.rest_prize
            prize=silver.rest_prize

        gold.profiles.add(profile)
        profile.my_league=gold
        sum+=1
       
        profile.l_prize =prize
        profile.l_rank =sum
        profile.l_coins =coins
        profile.l_league =silver.name
        profile.l_next =gold.name
        profile.l_image =silver.image
        profile.league_prize=True


        profile.save()
        gold.save()
       
        send_notification(profile.user.id,"League",silver.image,silver.name,prize,coins,sum,gold.name)
    sum=0

# GOLD
    for profile in gold_profiles:
        coins= profile.league_coins
        profile.league_coins=0
        prize=0
            
        if sum==0:
                
            profile.gem+=gold.first_prize
            prize=gold.first_prize
                
        elif sum==1:
                
            profile.gem+=gold.scond_prize
            prize=gold.scond_prize

        elif sum>1 and sum<5:
                
            profile.gem+=gold.rest_prize
            prize=gold.rest_prize

        diamond.profiles.add(profile)
        profile.my_league=diamond
        sum+=1
        
        profile.l_prize =prize
        profile.l_rank =sum
        profile.l_coins =coins
        profile.l_league =gold.name
        profile.l_next =diamond.name
        profile.l_image =gold.image
        profile.league_prize=True

        profile.save()
        diamond.save()
        
        send_notification(profile.user.id,"League",gold.image,gold.name,prize,coins,sum,diamond.name)

    sum=0
# DIAMOND
    for profile in diamond_profiles:
        coins= profile.league_coins
        profile.league_coins=0
        prize=0

        if sum==0:
                
            profile.gem+=diamond.first_prize
            prize=diamond.first_prize
                
        elif sum==1:
                
            profile.gem+=diamond.scond_prize
            prize=diamond.scond_prize

        elif sum>1 and sum<5:
                
            profile.gem+=diamond.rest_prize
            prize=diamond.rest_prize

        legendary.profiles.add(profile)
        profile.my_league=legendary
        sum+=1
        
        profile.l_prize =prize
        profile.l_rank =sum
        profile.l_coins =coins
        profile.l_league =diamond.name
        profile.l_next =legendary.name
        profile.l_image =diamond.image
        profile.league_prize=True

        profile.save()
        legendary.save()
      
        send_notification(profile.user.id,"League",diamond.image,diamond.name,prize,coins,sum,legendary.name)

    sum=0
# legendary
    for profile in legendary_profiles:
        coins= profile.league_coins
        profile.league_coins=0
        prize=0

        if sum==0:
                
            profile.gem+=legendary.first_prize
            prize=legendary.first_prize
                
        elif sum==1:
                
            profile.gem+=legendary.scond_prize
            prize=legendary.scond_prize

        elif sum>1 and sum<5:
                
            profile.gem+=legendary.rest_prize
            prize=legendary.rest_prize
        sum+=1
        
        profile.l_prize =prize
        profile.l_rank =sum
        profile.l_coins =coins
        profile.l_league =legendary.name
        profile.l_next =legendary.name
        profile.l_image =legendary.image
        profile.league_prize=True

        profile.save()
        
        send_notification(profile.user.id,"League",legendary.image,legendary.name,prize,coins,sum,legendary.name)

@app.task(name='tasks.daily_prize')
def daily_prize():
    profiles=Profile.objects.all()

    for profile in profiles:
        profile.daily_coins=True
        profile.save()
        fcm_device = GCMDevice.objects.get(
            cloud_message_type="FCM",
            user=User.objects.get(pk=profile.user.id))

        fcm_device.send_message("Daily",extra={
             "prize": 1000,})
        
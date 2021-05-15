
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from core.models import Profile,Room,Question,Answer,League,User
from django.core.exceptions import ObjectDoesNotExist
from user.serializers import ProfileSerializer
import random
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from push_notifications.models import  GCMDevice

def broadcast(room_id):
        # Add condition if user has subscribed in Redis
    channel_layer = get_channel_layer()

    # room = model_to_dict(Room.objects.get(pk=room_id))
    # data=json.dumps(room)
    print(" added")
    

    async_to_sync(channel_layer.group_send)(
        str(room_id), {

            'type': 'recieve_group_message',
                    'player1score':-2,
                    'player2score':-2,
                    'sender':0,
                    'question':0,
        })


class LeagueSerializer(serializers.ModelSerializer):
    """serializer for the League object"""
    queryset = League.objects.all()
    profiles =ProfileSerializer(many=True, read_only=True)
    class Meta:
        model = League
        fields = '__all__'



class QuestionSerializer(serializers.ModelSerializer):
    """serializer for the Question object"""
    # queryset = Question.objects.all()
    class Meta:
        model = Question
        fields = '__all__'
        


class AnswerSerializer(serializers.ModelSerializer):
    """serializer for the Question object"""
    # queryset = Question.objects.all()
    class Meta:
        model = Answer
        fields = '__all__'
    
    def create(self, validated_data):
        room=Room.objects.get(pk=validated_data['room'].id)

        if validated_data['player1_id']>0:
            room.player1_score+=validated_data['player1_score']
            room.player1_answered=validated_data['question_num']
            room.save()
            try:
                answer=Answer.objects.get(room=validated_data['room'],
                                          question_num=validated_data['question_num'],
                                          question=validated_data['question'])

                answer.player1_id=validated_data['player1_id']
                answer.player1_score=validated_data['player1_score']
                answer.player1_answer=validated_data['player1_answer']
                answer.save()

            except Answer.DoesNotExist:

                answer=Answer.objects.create(**validated_data)

        else:
            room.player2_score+=validated_data['player2_score']
            room.player2_answered=validated_data['question_num']
            room.save()
            try:
                answer=Answer.objects.get(room=validated_data['room'],
                                          question_num=validated_data['question_num'],
                                          question=validated_data['question'])

                answer.player2_id=validated_data['player2_id']
                answer.player2_score=validated_data['player2_score']
                answer.player2_answer=validated_data['player2_answer']
                answer.save()

            except Answer.DoesNotExist:
 
                answer=Answer.objects.create(**validated_data)
        

        room.players_answer.add(answer)
        room.save()
        return answer

def create_questions(room,category):
    question_ids = [question.id for question in Question.objects.all()]

    random.shuffle(question_ids)
    qty=0
    for pk in question_ids:
                   
        question=Question.objects.get(pk=pk)

        if question.category in category:
            room.questions.add(question)
            room.save()
            qty+=1
            if qty==5:
                return room

class RoomSerializer(serializers.ModelSerializer):
    """serializer for the Room object"""

    questions = QuestionSerializer(many=True, read_only=True)
    players_answer = AnswerSerializer(many=True, read_only=True)
    player1 =ProfileSerializer( read_only=True)
    player2 =ProfileSerializer(read_only=True)


    class Meta:
        model = Room
        fields = '__all__'
        read_only_fields = ('questions','players_answer','avaliable','player1','player2','player2_prize','player1_left','player2_left'
                            'question_num','player2_can_play','player1_can_play','player1_score','player2_score',
                            'created','updated','player1_answered','player2_answered')
                            # 'player1_left','player2_left',
        

    def create(self, validated_data):
        """create a new Room and return it"""
       
        if validated_data['is_facebook']:
            room=Room.objects.create(
                            category=validated_data['category'],
                            player1_prize=validated_data['player1_prize'],
                            player2_prize=validated_data['player1_prize'],
                            player1_profile=validated_data['player1_profile'],
                            player2_profile=validated_data['player2_profile'],
                            player1=Profile.objects.get(user=validated_data['player1_profile']),
                            player2=Profile.objects.get(user=validated_data['player2_profile']),
                            avaliable=False,
                            is_facebook=True    
                            )
            fcm_device = GCMDevice.objects.get(
            cloud_message_type="FCM",
            user=User.objects.get(pk=room.player2_profile))

            fcm_device.send_message("Challenge",extra={
             "name":room.player1.name,  
             "icon":room.player1.image,
             "coins": room.player1_prize,
             "room":room.id,
             "category":room.category})

            return create_questions(room,validated_data['category'])


        try:
            room=Room.objects.get(category__contains=validated_data['category'],avaliable=True)
            if room:
                
                room.avaliable=False
                room.player2_profile=validated_data['player1_profile']
                room.player2_prize=validated_data['player1_prize']
                room.player2=Profile.objects.get(user=validated_data['player1_profile'])
                room.save()
                return room

        except ObjectDoesNotExist:

            room=Room.objects.create(
                            category=validated_data['category'],
                            player1_prize=validated_data['player1_prize'],
                            player1_profile=validated_data['player1_profile'],
                            player1=Profile.objects.get(user=validated_data['player1_profile']),  
                            )
            

            return create_questions(room,validated_data['category'])


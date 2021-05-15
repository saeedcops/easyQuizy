from rest_framework import generics, authentication, permissions,viewsets
from room.serializers import QuestionSerializer,RoomSerializer,AnswerSerializer,LeagueSerializer
from core.models import Question,Answer,Room,Profile,League,User
from rest_framework.response import Response
from push_notifications.models import  GCMDevice
import json
import random
from .tasks import random_room


class ManageQuestionView(generics.CreateAPIView):
    """Mange the authenticated user"""
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticated,permissions.IsAdminUser,)

    def put(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        output = json.loads(body_unicode)
    
        
        for qustion in range( len(output)):
            # sleep(1)
            if output[qustion] is not None:
                Question.objects.create(answer=output[qustion]["answer"],category=output[qustion]["category"],
                                        image=output[qustion]["image"],obtion1=output[qustion]["option1"],obtion2=output[qustion]["option2"],
                                        obtion3=output[qustion]["option3"],obtion4=output[qustion]["option4"],time=40,
                                        question=output[qustion]["question"],question_type=output[qustion]["type"])

                print(str(output[qustion]['question']))

        return Response()


    def get(self, request, *args, **kwargs):

            questions=Question.objects.all()
                
            serializer = QuestionSerializer(questions, many=True)
            return Response(serializer.data)


class ManageRoomView(viewsets.ModelViewSet):
    """Mange the authenticated user"""
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permissions.IsAdminUser,

    def put(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        

        if "is_random" in body_unicode:
            try:
                room=Room.objects.get(pk=request.POST['id'])
                room.is_random=True
                room.started=True
                room.avaliable=False
                room.player2_prize=room.player1_prize
                room.player1.coins-=room.player1_prize
                room.player1.save()

                profile_id= random.randint(1,15)
                room.player2_profile=65
                room.player2=Profile.objects.get(pk=65)

                room.save()
                # call_command('random_player',room.id)
                random_room.delay(room.id)
                return Response()
            except Room.DoesNotExist:

                return Response()

        elif "finished" in body_unicode:
            try:
                room=Room.objects.get(pk=request.POST['id'])
                room.delete()
                return Response()
            except Room.DoesNotExist:

                return Response()
      
        elif "started" in body_unicode:
            room=Room.objects.get(pk=request.POST['id'])
            if room.started:
                
                return Response()
            else:
                room.started=True
                room.player1.coins-=room.player1_prize
                room.player2.coins-=room.player2_prize
                room.player1.save()
                room.player2.save()
                room.save()
                
                return Response()

        elif "player2_profile" in body_unicode:
            room=Room.objects.get(pk=request.POST['id'])
            room.player2_profile=request.POST['player2_profile']
            room.player2=Profile.objects.get(user=request.POST['player2_profile'])
            room.save()
            # SEND NORIFICATION
            fcm_device = GCMDevice.objects.get(
            cloud_message_type="FCM",
            user=User.objects.get(pk=room.player2_profile))
            fcm_device.send_message("Challenge",extra={
             "name":room.player1.name,  
             "icon":room.player1.image,
             "coins": room.player1_prize,
             "room":room.id,
             "category":room.category})
            serializer = RoomSerializer(room)
            return Response(serializer.data)
        else:
            return Response()
        


class LeagueViewSet(viewsets.ModelViewSet):
    """Mange tags in the database"""
    queryset = League.objects.all()
    serializer_class = LeagueSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permissions.IsAdminUser,


class AnswerViewSet(generics.CreateAPIView):
    """Mange tags in the database"""
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permissions.IsAdminUser,


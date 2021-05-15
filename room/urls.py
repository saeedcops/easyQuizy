from django.urls import path,include
from room import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'room', views.ManageRoomView,basename='room')
router.register(r'league', views.LeagueViewSet,basename='leaue')


app_name='room'

urlpatterns=[
    path('', include(router.urls)),

    path('question/', views.ManageQuestionView.as_view(), name='rooms'),
    path('answer/', views.AnswerViewSet.as_view(), name='answer'),

]

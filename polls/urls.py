from django.urls import path
# from .views import polls_list, polls_detail
from .views import ChoiceList, CreateVote, PollViewSet, UserCreate, LoginView, SendEmailsView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'polls', PollViewSet, basename='polls')


urlpatterns = [
    # path('polls/', polls_list, name='polls_list'),
    # path('polls/<int:pk>/', polls_detail, name='polls_detail')
    # path('polls/', PollList.as_view(), name='polls_list'),
    # path('polls/<int:pk>/', PollDetail.as_view(), name='polls_detail'),
    # path('choices/', ChoiceList.as_view(), name='choices_list'),
    # path('vote/', CreateVote.as_view(), name='create_vote')

    path('polls/<int:pk>/choices', ChoiceList.as_view(), name='choice_list'),
    path('polls/<int:pk>/choices/<int:choice_pk>/vote', CreateVote.as_view(), name='create_vote'),
    path('users/', UserCreate.as_view(), name='user_create'),
    # path('login/', LoginView.as_view(), name='login')
    path('login/', obtain_auth_token, name='login'),
    path('email/', SendEmailsView.as_view(), name='email'),
]

urlpatterns += router.urls
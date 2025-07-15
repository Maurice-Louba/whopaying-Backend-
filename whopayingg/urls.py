from .import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from django.urls import path
urlpatterns = [
    path('groups/',views.Groups,name='groups'),
    path('groups/<str:username>/',views.Groups_detail,name='groups-name'),
    path('expenses/',views.Expenses,name='expense'),
    path('expenses/<str:username>/',views.Expenses_detail,name='expenses-details'),
    path('debts/',views.debt,name='debt'),
    path('debts/<str:username>/',views.debt_details,name='debt-details'),
    path('member/<int:id>/',views.member_details,name='member-details'),
    path('member/',views.members,name='member'),
    path('users/',views.users,name='utilisateurs'),
    path('profil/<str:username>/infos/',views.users_details,name="users-details"),
    path("users/me/", views.current_user, name="current-user"),
    path("photo/<str:profile_picture>/", views.photo_de_profile),
    path("jwt/create/",TokenObtainPairView.as_view(),name="jwt-create"),
    path("jwt/refresh/",TokenRefreshView.as_view(),name="refresh-view"),
    path("jwt/verify/",TokenVerifyView.as_view(),name="verify-view"),
    path('all/',views.all_users,name='all'),
    path('verify/<str:username>/',views.mail_verification,name="verify"),
    path('verify-otp/', views.verify_otp,name='verification-otp'),
    path("csrf/", views.get_csrf_token, name='get_csrf_token'),
    path("users-all/",views.TousUtilisateur,name='tous_utilisateur'),
    path("conversations/<str:username>/",views.get_all_conversation,name="all_conversation"),
    path("mes-conversations/<str:username>/",views.toutes_les_conversations,name="all_conversation"),
    path('conversation_details/<int:conversation>/',views.les_message,name='Les_messages'),
    path('tous_les_messages/',views.tous_les_message,name='all-messages')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#api
#
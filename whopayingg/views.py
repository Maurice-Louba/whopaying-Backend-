from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages

from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Group,Expense,Debt,Member,User,otp_token,conversationModel,conversation_in_group,Les_message
from .serializers import Group_serialized,Expense_serialized,Debt_serialized,Member_serialized,Users_serialized,conversationSerialized,conversation_in_group_serialized,Les_messages_serialized
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls.static import static
from django.contrib.auth import get_user_model
from django.utils import timezone
import random
from django.core.mail import send_mail


@api_view(["GET","POST"])

@permission_classes([IsAuthenticated])
def Groups(request):
    if request.method=='GET':
        groups=Group.objects.all()
        serialized_get=Group_serialized(groups,many=True)
        return Response(serialized_get.data)
    elif request.method=='POST':
        groups_post=Group_serialized(data=request.data)
        if groups_post.is_valid():
            groups_post.save()
            return Response(groups_post.data,status=status.HTTP_201_CREATED)
    return Response(groups_post.errors,status=status.HTTP_400_BAD_REQUEST)
@api_view(["GET", "PUT", "DELETE","POST"])

@permission_classes([IsAuthenticated])
def Groups_detail(request,username):
    try:
        user=User.objects.get(username=username)
    except user.DoesNotExit:
        return Response(status=status.HTTP_404_NOT_FOUND)
    groups=Group.objects.filter(members=user)
    
    if request.method =='GET':
        groups_get_seria=Group_serialized(groups,many=True)
        return Response(groups_get_seria.data)
    elif request.method == 'POST':
        groups_post_serialise=Group_serialized(groups)
        if groups_post_serialise.is_valid():
            groups_post_serialise.save()
            return Response(groups_post_serialise.data,status=status.HTTP_201_CREATED)
    return  Response(groups_post_serialise.errors,status=status.HTTP_400_BAD_REQUEST)
        
    
    
    
#API:
#http://127.0.0.1:8001/groups/id: pour afficher les details des groupes
#http://127.0.0.1:8001/groups/ pour afficher les groupes
# Create your views here.
@api_view(['GET','POST'])
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def Expenses(request):
    if request.method == 'GET':
        expense=Expense.objects.all()
        expense_serialized_get=Expense_serialized(expense,many=True)
        return Response(expense_serialized_get.data)
    elif request.method=='POST':
        expense_serialized_post=Expense_serialized(request.data)
        if expense_serialized_post.is_valid():
            expense_serialized_post.save()
            return Response(expense_serialized_post.data,status=status.HTTP_201_CREATED)
        return Response(expense_serialized_post.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','DELETE'])

@permission_classes([IsAuthenticated])
def Expenses_detail(request,username):
    try:
        user=User.objects.get(username=username)
    except user.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    expense=Expense.objects.filter(user_depenced=user)
    if request.method =='GET':
        serialised_get = Expense_serialized(expense,many=True)
        return Response(serialised_get.data)
    elif request.method=='DELETE':
        expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
            
#API: 
# http://127.0.0.1:8001/expenses/ historiques des depences
#http://127.0.0.1:8001/expenses/id detail et supprission 

@api_view(['GET','POST'])

@permission_classes([IsAuthenticated])
def debt(request):
    if request.method == 'GET':
        debt = Debt.objects.all()
        debt_serialised_get=Debt_serialized(debt,many=True)
        return Response(debt_serialised_get.data)
    elif request.method == 'POST':
        debt_serialised_post=Debt_serialized(request.data)
        if debt_serialised_post.is_valid():
            debt_serialised_post.save()
            return Response(debt_serialised_post.data,status=status.HTTP_201_CREATED)
        return Response(debt_serialised_post.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE','POST'])
@permission_classes([AllowAny])
def debt_details(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # Récupère les dettes où l'utilisateur est soit créditeur soit débiteur
    debts = Debt.objects.filter(creditor=user) | Debt.objects.filter(debtor=user)

    if not debts.exists():
        return Response({'error': 'No debts found for this user'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serialized = Debt_serialized(debts, many=True)
        return Response(serialized.data)
    elif request.method == 'POST':
        debts_post =Debt_serialized(data=request.data)
        if debts_post.is_valid():
            debts_post.save()
            return Response(debts_post.data,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = debts.count()
        debts.delete()
        return Response({'message': f'{count} debt(s) deleted'}, status=status.HTTP_204_NO_CONTENT)
    
#API
#http://127.0.0.1:8001/debts/ voir tous les credits
#http://127.0.0.1:8001/debts/id voir les details de credits     
    
    
        
@api_view(['GET','DELETE'])
@permission_classes([IsAuthenticated])
def member_details(request,id):
    try:
        member=Member.objects.get(id=id)
    except Member.DoesNotExit():
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        member_serialized_get=Member_serialized(member)
        return Response(member_serialized_get.data)
    elif request.method =='DELETE':
        member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def members(request):
    if request.method =='POST':
        serialized_member_post=Member_serialized(request.data)
        if serialized_member_post.is_valid():
            serialized_member_post.save()
            return Response(serialized_member_post.data,status=status.HTTP_201_CREATED)
        return Response(serialized_member_post.errors,status=status.HTTP_404_NOT_FOUND)

#API
#http://127.0.0.1:8001/member/ pour voir un membre
#http://127.0.0.1:8001/member/id pour voir les details sur un membre de groupe

@api_view(["POST"])
@permission_classes([AllowAny])


def users(request):
    if request.method == 'POST':
        serialized_post = Users_serialized(data=request.data)
        if serialized_post.is_valid():
            user = serialized_post.save(is_active=False)  # désactiver user tant que pas vérifié

            # Générer OTP à 6 chiffres
            code = str(random.randint(100000, 999999))

            # Créer token OTP (assure-toi que ton modèle otp_token a otp_code et otp_expires_at)
            otp_token.objects.create(
                user=user,
                otp_code=code,
                otp_expires_at=timezone.now() + timezone.timedelta(minutes=5)
            )

            # Envoyer email de vérification avec le code OTP
            subject = "Verify your email for Whopaying"
            message = f"Hello {user.username}, your verification code is {code}. It expires in 5 minutes."
            send_mail(subject, message, 'whopayingservice@gmail.com', [user.email], fail_silently=False)

            return Response(serialized_post.data, status=status.HTTP_201_CREATED)
        
        print("❌ Erreurs de validation :", serialized_post.errors)
        return Response(serialized_post.errors, status=status.HTTP_400_BAD_REQUEST)
  
            
@api_view(['GET']) 
@permission_classes([AllowAny])
def users_details(request,username):
    try:
        user=User.objects.get(username=username)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        user_data_get =Users_serialized(user)
        return Response(user_data_get.data)
    
#Api
#http://localhost:5173/profil/username pour voir les details de son compte

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = Users_serialized(request.user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def all_users(request):
    tous=User.objects.all()
    tous_serialized =Users_serialized(tous,many=True)
    return Response(tous_serialized.data)



User = get_user_model()

@api_view(['GET'])
def photo_de_profile(request, profile_picture):
    try:
        user = User.objects.get(profile_picture=f"profiles/{profile_picture}")
    except User.DoesNotExist:
        return Response({"detail": "Utilisateur introuvable"}, status=status.HTTP_404_NOT_FOUND)

    serializer = Users_serialized(user)
    return Response({"photo_url": serializer.data.get("profile_picture")})


def mail_verification(request, username):
    user = User.objects.get(username=username)
    user_otp = otp_token.objects.filter(user=user).last()
    user.is_active = True
    user.save()

    if request.method == 'POST':
        entered_otp = request.POST.get('otp_code')

        if user_otp and user_otp.otp_code == entered_otp:
            if user_otp.otp_expires_at > timezone.now():
                user.is_active = True
                user.save()
                messages.success(request, "Account activated successfully!")
                return redirect('signin')
            else:
                messages.warning(request, "The code has expired. Please request a new one.")
        else:
            messages.error(request, "Invalid code.")
    
    return render(request, 'verify', {'user': user})
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(["POST"])
@permission_classes([AllowAny])
def verify_otp(request):
    username = request.data.get("username")
    code = request.data.get("otp_code")

    try:
        user = User.objects.get(username=username)
        otp = otp_token.objects.filter(user=user).last()

        if otp and otp.otp_code == code:
            if otp.otp_expires_at > timezone.now():
                user.is_active = True
                user.save()

                
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                return Response({"token": access_token, "refresh": str(refresh)}, status=200)
            else:
                return Response({"error": "Code expired"}, status=400)
        return Response({"error": "Invalid code"}, status=400)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
    
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse

@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({"detail": "CSRF cookie set"})


@api_view(["GET"])
@permission_classes([AllowAny])
def  TousUtilisateur(request):
    if request.method =='GET':
        users=User.objects.all()
        users_all_serialized=Users_serialized(users,many=True)
        return Response(users_all_serialized.data)
        


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_all_conversation(request,username):
    user=User.objects.get(username=username)
    if request.method =='GET':
        conversations=conversationModel.objects.filter(participants=user)
        conversations_serialized=conversationSerialized(conversations,many=True)
        return Response(conversations_serialized.data)
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def toutes_les_conversations(request,username):
    user=User.objects.get(username=username)
    groups=Group.objects.filter(members=user)
    if request.method =='GET':
        conversations=conversation_in_group.objects.filter(in_group__in=groups)
        conversations_serialized=conversation_in_group_serialized(conversations,many=True)
        return Response(conversations_serialized.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def tous_les_message(request):
    messages=Les_message.objects.all()
    
    mes_serailized=Les_messages_serialized(messages,many=True)
    return Response(mes_serailized.data)

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def all_message(request,username,name):
    user=User.objects.get(username=username)
    groups=Group.objects.filter(members=user)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def les_message(request, conversation):
    conversation_obj = get_object_or_404(conversation_in_group, pk=conversation)
    
    if request.method == 'GET':
        messages = Les_message.objects.filter(conversation=conversation_obj).order_by('timestramp')
        messages_serialized = Les_messages_serialized(messages, many=True)
        return Response(messages_serialized.data)
    
    elif request.method == 'POST':
        message_obtenu = Les_messages_serialized(
            data=request.data,
            context={'request': request, 'conversation': conversation_obj}  # 🔥 Ajout critique ici
        )
        if message_obtenu.is_valid():
            message_obtenu.save()
            return Response(message_obtenu.data, status=status.HTTP_201_CREATED)
        return Response(message_obtenu.errors, status=status.HTTP_400_BAD_REQUEST)

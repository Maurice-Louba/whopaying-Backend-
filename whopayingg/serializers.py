from rest_framework import serializers
from .models import User,Group,Member,Expense,Debt,conversationModel,Message,conversation_in_group,Les_message
from django.contrib.auth import get_user_model


class Users_serialized(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)  # champ virtuel, pas dans User

    class Meta:
        model = User
        fields = ['id','username','email', 'first_name', 'last_name', 'password', 'password2','profile_picture','bio']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')  # on enlève password2, on ne le sauvegarde pas

        # Création automatique de username à partir de email
       # username = validated_data['email'].split("@")[0]
        #validated_data['username'] = username

        user = User.objects.create_user(**validated_data)
        return user
    
class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']  # ou ['id', 'username', 'email'] si tu veux plus

class SimpleGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']
        
        
class Group_serialized(serializers.ModelSerializer):
    class Meta:
        model=Group
        fields='__all__'
        
class Member_serialized(serializers.ModelSerializer):
    class Meta:
        model=Member
        fields='__all__'
class Expense_serialized(serializers.ModelSerializer):
    user_depenced=SimpleUserSerializer(read_only=True)
    group=SimpleGroupSerializer(read_only=True)
    class Meta:
        model=Expense
        fields=['user_depenced','group','amount','description','date']
        
class Debt_serialized(serializers.ModelSerializer):
    group = SimpleGroupSerializer(read_only=True)
    creditor = SimpleUserSerializer(read_only=True)
    debtor = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Debt
        fields = ['group', 'creditor', 'debtor', 'amount', 'created_at']

    def validate(self, data):
        group = data.get('group')
        creditor = data.get('creditor')
        debtor = data.get('debtor')

        if not all([group, creditor, debtor]):
            raise serializers.ValidationError("Group, creditor and debtor must all be specified.")

        if creditor not in group.members.all() or debtor not in group.members.all():
            raise serializers.ValidationError("Both users must be members of the group.")

        return data
    
class userserialized(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=['id','username','profile_picture']
        
class conversationSerialized(serializers.ModelSerializer):
    participants =userserialized(many=True, read_only=True)
    class Meta:
        model =conversationModel
        fields=['id','participants','created_at']  
        
    def to_representation(self,instance):
        representation=super().to_representation(instance)
        return representation
        
        
class MessageSerialized(serializers.ModelSerializer):
    sender =userserialized()
    participants = serializers.SerializerMethodField()
    class Meta:
        model = Message
        fields= ['id','sender','content','timestamp','participants']
    def get_participants(self,obj):
        return userserialized(obj.conversation.participant.all(),many=True).data


class CreatemessageSerialized (serializers.ModelSerializer):
    class Meta:
        model=Message
        fields=['conversation','content']
        
        
class group_element(serializers.ModelSerializer):
    class Meta:
        model=Group;
        fields=['name','members','avatar']
        
class conversation_in_group_serialized(serializers.ModelSerializer):
    in_group=group_element(read_only=True)
    class Meta:
        model = conversation_in_group
        fields=['id','in_group','objectif','created_at']

class Les_messages_serialized(serializers.ModelSerializer):
    sender = userserialized(read_only=True)
    conversation = conversation_in_group_serialized(read_only=True)

    class Meta:
        model = Les_message
        fields = ['conversation', 'sender', 'content','timestramp']
        #read_only_fields = ['sender', 'conversation', 'timestramp']

    def create(self, validated_data):
        request = self.context.get("request")
        sender = request.user if request else None
        conversation = self.context.get("conversation")

        if not sender or not conversation:
            raise serializers.ValidationError("Missing sender or conversation context.")

        if sender not in conversation.in_group.members.all():
            raise serializers.ValidationError("Sender must be a member of the group.")

        return Les_message.objects.create(
            sender=sender,
            conversation=conversation,
            **validated_data
        )

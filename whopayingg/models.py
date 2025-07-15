from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models import Prefetch
from django.core.exceptions import ValidationError
from django.utils import timezone
import secrets


class User(AbstractUser):
    PREFERRED_CURRENCY_CHOICE = [
    ('AUD', 'Australian Dollar'),
    ('BWP', 'Botswana Pula'),
    ('BRL', 'Brazilian Real'),
    ('CAD', 'Canadian Dollar'),
    ('CHF', 'Swiss Franc'),
    ('CNY', 'Chinese Yuan'),
    ('DZD', 'Algerian Dinar'),
    ('EGP', 'Egyptian Pound'),
    ('EUR', 'Euro'),
    ('GBP', 'British Pound'),
    ('GNF', 'Guinean Franc'),
    ('GHS', 'Ghanaian Cedi'),
    ('HKD', 'Hong Kong Dollar'),
    ('INR', 'Indian Rupee'),
    ('JPY', 'Japanese Yen'),
    ('KES', 'Kenyan Shilling'),
    ('KRW', 'South Korean Won'),
    ('MAD', 'Moroccan Dirham'),
    ('MRO', 'Mauritanian Ouguiya'),
    ('MUR', 'Mauritian Rupee'),
    ('MXN', 'Mexican Peso'),
    ('NOK', 'Norwegian Krone'),
    ('NGN', 'Nigerian Naira'),
    ('NZD', 'New Zealand Dollar'),
    ('RUB', 'Russian Ruble'),
    ('SCR', 'Seychellois Rupee'),
    ('SDG', 'Sudanese Pound'),
    ('SEK', 'Swedish Krona'),
    ('SGD', 'Singapore Dollar'),
    ('TND', 'Tunisian Dinar'),
    ('TRY', 'Turkish Lira'),
    ('TZS', 'Tanzanian Shilling'),
    ('UGX', 'Ugandan Shilling'),
    ('USD', 'US Dollar'),
    ('XAF', 'Central African CFA Franc'),
    ('XOF', 'West African CFA Franc'),
    ('XPF', 'CFP Franc (Pacific Franc)'),
    ('ZAR', 'South African Rand'),
    ('ZMW', 'Zambian Kwacha'),
]
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    preferred_currency = models.CharField(max_length=3, default='MAD',choices=PREFERRED_CURRENCY_CHOICE)
    online_satuts=models.BooleanField(default=False)
    bio = models.TextField(max_length=150, blank=True)
    

    def __str__(self):
        return self.username
    
class otp_token(models.Model):
    user =models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    otp_code=models.CharField(max_length=6, default=secrets.token_hex(3))
    tp_created_at = models.DateTimeField(auto_now_add=True)
    otp_expires_at = models.DateTimeField(blank=True,null=True)
    
    def __str__(self):
        return self.user.username


class Group(models.Model):
    CAUSE_CHOICES=[ 
    ('vacances', 'Vacances'),
    ('famille', 'Famille'),
    ('amis', 'Amis'),
    ('projet', 'Projet professionnel'),
    ('evenement', 'Événement spécial'),
    ('sport', 'Sport / activité'),
    ('association', 'Association / ONG'),
    ('tâches_ménagers','Tâches_ménagers'),
    ('restaurant','Restaurant'),
    ('maison/appartement','Maison/Appartement'),
    ('autre', 'Autre'),
    
                   
                   
                   ]
    
    name=models.CharField(max_length=15,unique=True)
    members=models.ManyToManyField(User,related_name='membership_groups')
    
    created_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    avatar=models.ImageField(upload_to='avatar/')
    cause=models.CharField(max_length=50,choices=CAUSE_CHOICES)
    description=models.TextField(max_length=150)
    
    def __str__(self):
        return self.name
    
class Member(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, default='membre')
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} in {self.group.name} as {self.role}"
    
class Expense(models.Model):
    user_depenced = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name='group_of_expense')

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(max_length=250)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=["-date"]

    def __str__(self):
        return f'{self.user_depenced.first_name} spent {self.amount} on {self.date.strftime("%Y-%m-%d")}'
                                    
    def clean(self):
        if not self.group.members.filter(id=self.user_depenced.id).exists():
            raise ValidationError("User must be a member of the group to add an expense.")
        
class Debt(models.Model):
    group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name='debts')
    
    creditor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='debts_to_receive'
    )
    debtor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='debts_to_pay'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering =["-created_at"]

    def __str__(self):
        return f'{self.debtor.username} must pay {self.amount} to {self.creditor.username}'
    def clean(self):
        # Vérifie que le créditeur et débiteur sont bien membres du groupe
        if self.creditor not in self.group.members.all() or self.debtor not in self.group.members.all():
            raise ValidationError("Creditor and debtor must be members of the same group.")

class ChatModel(models.Model):
    sender=models.CharField(max_length=100,default=None)
    message=models.TextField(null=True,blank=True)
    thread_name=models.CharField(max_length=100)
    send_time=models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.message

class ConversationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related(Prefetch('participants',queryset=User.objects.only('id','username')))
class conversationModel(models.Model):
    participants=models.ManyToManyField(User,related_name='conversation')
    objects=ConversationManager()
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        participants_names =",".join([user.username for user in self.participants.all()])
        return f'Conversation with {participants_names}'
class Message(models.Model):
    conversation=models.ForeignKey(conversationModel,on_delete=models.CASCADE)
    sender=models.ForeignKey(User,on_delete=models.CASCADE)
    content =models.TextField(blank=True,null=True)
    timestamp =models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Message from {self.sender.username} in {self.content[:20]}'

class conversation_in_group(models.Model):
    in_group=models.OneToOneField(Group,related_name='group',on_delete=models.CASCADE)
    objectif=models.CharField(max_length=30)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'conversation with {self.in_group.name}'
class Les_message(models.Model):
    conversation=models.ForeignKey(conversation_in_group,on_delete=models.CASCADE)
    sender=models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.TextField(blank=True,null=True)
    timestramp=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'Message from {self.sender.username} in {self.content[:20]}'
    
# Create your models here
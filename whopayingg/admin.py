from django.contrib import admin
from .models import User,Group,Expense,Member,Debt,ChatModel,conversationModel,Message,ConversationManager,conversation_in_group,Les_message

# Register your models here.
admin.site.register(User)
admin.site.register(Group)
admin.site.register(Expense)
admin.site.register(Member)
admin.site.register(Debt)
admin.site.register(ChatModel)
admin.site.register(conversationModel)
admin.site.register(Message)
admin.site.register(conversation_in_group)
admin.site.register(Les_message)

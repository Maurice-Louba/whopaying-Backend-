
from .models import otp_token
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings
from django.utils.html import strip_tags

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_token(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            return

        # Création du token OTP
        otp_code = otp_token.objects.create(
            user=instance,
            otp_expires_at=timezone.now() + timezone.timedelta(minutes=5)
        )
        instance.is_active = False
        instance.save()

        # Dernier OTP
        otp = otp_token.objects.filter(user=instance).last()

        # Message HTML
        subject = "🚀 Vérification de votre adresse e-mail - Whopaying"

        html_message = f"""
        <div style="font-family: Arial, sans-serif; padding: 20px; background-color: #f7f7f7; color: #333;">
    
        <!-- 👇 Logo en haut -->
        <div style="text-align: center; margin-bottom: 20px;">
        <img src="logo/logo(4).png" alt="Whopaying Logo" width="120" />
        </div>

    <h2 style="color: #22c55e;">Bienvenue sur <span style="color:#000">Whopaying 👋</span></h2>
    <p>Bonjour <strong>{instance.username}</strong>,</p>
    <p>Merci de vous être inscrit sur notre plateforme. Pour finaliser la création de votre compte, veuillez cliquer sur le bouton ci-dessous pour confirmer votre adresse e-mail :</p>
    <a href="http://127.0.0.1:8001/verify/{instance.username}" style="display: inline-block; padding: 12px 20px; margin: 20px 0; background-color: #22c55e; color: white; text-decoration: none; border-radius: 5px;">✅ Vérifier mon e-mail</a>
    <p>Ce lien expirera dans <strong>5 minutes</strong>.</p>
    <p>Si vous n'avez pas demandé cette inscription, veuillez ignorer ce message.</p>
    <br/>
    <p style="font-size: 14px; color: #888;">💡 Astuce : Ajoutez notre adresse à vos contacts pour ne pas manquer nos futurs e-mails.</p>
    <hr style="margin: 20px 0;" />
    <p style="font-size: 13px; color: #aaa;">© 2025 Whopaying. Tous droits réservés.</p>
</div>
"""


        plain_message = strip_tags(html_message)

        send_mail(
            subject,
            plain_message,  # version texte brut
            'whopayingservice@gmail.com',
            [instance.email],
            html_message=html_message,
            fail_silently=False,
        )
        
       
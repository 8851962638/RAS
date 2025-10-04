from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

# Do NOT import Wallet at the top (can cause circular import issue)
# Instead import inside the function

User = get_user_model()

@receiver(post_save, sender=User)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        from .models import Wallet  # 👈 Import here to avoid circular import
        Wallet.objects.create(user=instance)

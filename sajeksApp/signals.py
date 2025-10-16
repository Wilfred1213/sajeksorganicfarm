from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Contact, Gallary, Blog,Team, ProduceItem
from django.core.mail import EmailMessage

@receiver(post_save, sender=Contact)
def contact_submission_notification(sender, instance, created, **kwargs):
    """
    Handles sending an email notification to the admin every time a new 
    Contact object is saved (created=True).
    """
    # Only proceed if a new instance was created (i.e., not an update)
    if created:
        admin_email = getattr(settings, 'ADMIN_EMAIL', settings.DEFAULT_FROM_EMAIL)
        site_name = getattr(settings, 'SITE_NAME', 'Sajeks App')
        
        # 1. Email Subject for Admin
        email_subject = f"NEW CONTACT: {instance.subject} ({instance.name})"
        
        # 2. Email Body (plain text)
        email_body = (
            f"A new message has been submitted via the contact form on {site_name}.\n\n"
            f"Sender Name: {instance.name}\n"
            f"Sender Email: {instance.email}\n"
            f"Subject: {instance.subject}\n"
            f"Date: {instance.posted_on.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"Message Body:\n"
            f"----------------------------------------\n"
            f"{instance.message}\n"
            f"----------------------------------------\n\n"
            f"View and manage this message in the admin panel: "
            f"http://yourdomain.com/admin/message/{instance.pk}/"
        )
        
        # 3. Send the Email
        try:
            send_mail(
                subject=email_subject,
                message=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[admin_email],
                fail_silently=False,
            )
        except Exception as e:
            # In production, you would log this error instead of printing
            print(f"ERROR: Failed to send contact notification email: {e}")

@receiver(post_save, sender=Blog)
def gallery_auto_save(sender, instance, created, **kwargs):
    if created:
        blog_image = instance.img
        Gallary.objects.create(image = blog_image, title = instance.title)

@receiver(post_save, sender=ProduceItem)
def gallery_auto_save(sender, instance, created, **kwargs):
    if created:
        blog_image = instance.image
        Gallary.objects.get_or_create(image = blog_image, title = instance.title)
        
@receiver(post_save, sender=ProduceItem)
def gallery_auto_save(sender, instance, created, **kwargs):
    if created:
        blog_image = instance.image
        Gallary.objects.get_or_create(image = blog_image, title = instance.title)
        
@receiver(post_save, sender=Team)
def gallery_team_members_auto_save(sender, instance, created, **kwargs):
    if created:
        team_image = instance.image
        Gallary.objects.get_or_create(image = team_image)



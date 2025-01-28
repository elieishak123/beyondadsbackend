from django.db import models
from django.utils import timezone

# Service Section
class Service(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='services/')
    order = models.IntegerField()

    def __str__(self):
        return self.title

# Client Section
class Client(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='clients/')  # Adjust the path as needed
    order = models.IntegerField()

    def __str__(self):
        return self.name

class HeroContent(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200)
    button_text = models.CharField(max_length=50)
    image = models.ImageField(upload_to='hero_images/', blank=True, null=True)  # New field

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['id'], name='single_hero_content')
        ]

    def __str__(self):
        return self.title

# Call To Action (CTA) Content Section
class CTAContent(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.TextField()
    button_text = models.CharField(max_length=255)
    button_link = models.URLField()

# Footer Content Section
class FooterContent(models.Model):
    instagram_link = models.URLField(max_length=200)
    linkedin_link = models.URLField(max_length=200)
    phone_number = models.CharField(max_length=20)
    footer_text = models.TextField()
    email = models.EmailField()
    location= models.CharField(max_length=30)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['id'], name='single_footer_content')
        ]

    def __str__(self):
        return self.email

# About Section
class AboutContent(models.Model):
    text = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['id'], name='single_about_content')
        ]

    def __str__(self):
        return f"About Content (ID: {self.id})"

# Shorts Section
class Short(models.Model):
    title = models.CharField(max_length=100)
    video = models.FileField(upload_to='shorts/')  # Adjust the path as needed
    order = models.IntegerField()

    def __str__(self):
        return self.title

# Our Process Section
class ProcessPhoto(models.Model):
    photo = models.ImageField(upload_to='process_photos/')  # Adjust the path as needed
    order = models.IntegerField()

    def __str__(self):
        return f"Process Photo (Order: {self.order})"

# Contact Us Section
class ContactUs(models.Model):
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    location = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['id'], name='single_contact_us')
        ]

    def __str__(self):
        return f"Contact Us (Email: {self.email})"



class FormSubmission(models.Model):
    SELECTION_CHOICES = [
        ('expert_ads', 'Expert ads with clear strategy'),
        ('ad_creative', 'High-converting ad creative videos'),
        ('all_above', 'All of the above'),
    ]

    # Required fields
    selection = models.CharField(max_length=20, choices=SELECTION_CHOICES)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    
    # Optional fields
    email = models.EmailField(blank=True)
    instagram = models.CharField(max_length=255, blank=True)
    website = models.CharField(max_length=255,blank=True)

    # Admin-related fields
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


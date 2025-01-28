from rest_framework import serializers
from .models import Service, Client, HeroContent, CTAContent, FooterContent, AboutContent, Short, ProcessPhoto, ContactUs

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'title', 'image', 'order']


class ClientSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ['id', 'name', 'image', 'order', 'image_url']
        extra_kwargs = {
            'image': {'required': False, 'allow_null': True},
            'name': {'required': True},
            'order': {'required': True}
        }

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

    def update(self, instance, validated_data):
        # Print validated data for debugging
        print("Validated data:", validated_data)
        
        # Update only the fields that are present in validated_data
        for attr, value in validated_data.items():
            if value is not None:  # Only update if value is not None
                setattr(instance, attr, value)
        
        instance.save()
        return instance

# Serializer
class HeroContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroContent
        fields = ['id', 'title', 'subtitle', 'button_text', 'image']  # Include 'image'

    def update(self, instance, validated_data):
        # If the 'image' field is not in the data, preserve the current image
        image = validated_data.pop('image', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if image is not None:
            instance.image = image
        instance.save()
        return instance

class CTAContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CTAContent
        fields = '__all__'


class FooterContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterContent
        fields = ['id', 'instagram_link', 'linkedin_link', 'phone_number', 'footer_text', 'email','location']

class AboutContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutContent
        fields = ['id', 'text']

class ShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Short
        fields = ['id', 'title', 'video', 'order']

class ProcessPhotoSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = ProcessPhoto
        fields = ['id', 'photo', 'order', 'photo_url']

    def get_photo_url(self, obj):
        if obj.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url
        return None

class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ['id', 'email', 'phone_number', 'location']


class AboutContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutContent
        fields = ['id', 'text']



from rest_framework import serializers
from .models import FormSubmission, FormSubmission 


class FormSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormSubmission
        fields = '__all__'
        read_only_fields = ['created_at', 'is_read', 'is_hidden']
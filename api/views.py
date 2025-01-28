from rest_framework import viewsets, generics, mixins
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .models import ContactUs
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Service, Client, HeroContent, CTAContent, FooterContent,ProcessPhoto,ContactUs, Short ,AboutContent
from .serializers import (
    ServiceSerializer,
    ClientSerializer,
    HeroContentSerializer,
    CTAContentSerializer,
    FooterContentSerializer,
    ProcessPhotoSerializer,
    ShortSerializer,
    AboutContentSerializer,
    ContactUsSerializer,
    ClientSerializer
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import FormSubmission
from .serializers import FormSubmissionSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .models import FormSubmission
from .serializers import FormSubmissionSerializer
from django.db.models import Q

# Service ViewSet
class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def retrieve(self, request, pk=None):
        try:
            service = self.queryset.get(pk=pk)
        except Service.DoesNotExist:
            raise NotFound("Service not found.")
        serializer = self.serializer_class(service)
        return Response(serializer.data)

    def update(self, request, pk=None):
        service = self.get_object()
        serializer = self.get_serializer(service, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


    def destroy(self, request, pk=None):
        try:
            service = self.queryset.get(pk=pk)
        except Service.DoesNotExist:
            raise NotFound("Service not found.")
        service.delete()
        return Response(status=204)


# Client ViewSet
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    
# HeroContent View
class HeroContentView(generics.RetrieveUpdateAPIView):
    queryset = HeroContent.objects.all()
    serializer_class = HeroContentSerializer
    parser_classes = (MultiPartParser, FormParser)  # Ensure multipart form data is accepted

    def get_object(self):
        return self.queryset.first()

    def update(self, request, *args, **kwargs):
        partial = request.method == 'PATCH'  # Allow partial updates
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


# CTAContent View
class CTAContentView(generics.RetrieveUpdateAPIView):
    queryset = CTAContent.objects.all()
    serializer_class = CTAContentSerializer
    # permission_classes = [IsAdminOrReadOnly]

    def get_object(self):
        return self.queryset.first()


# FooterContent View
class FooterContentView(generics.RetrieveUpdateAPIView):
    queryset = FooterContent.objects.all()
    serializer_class = FooterContentSerializer

    def get_object(self):
        # Get the first object if it exists, else create a default one
        footer_content = self.queryset.first()
        if not footer_content:
            footer_content = FooterContent.objects.create(
                instagram_link="https://www.instagram.com",
                linkedin_link="https://www.linkedin.com",
                phone_number="+1 (800) 123-4567",
                footer_text="Your default footer text goes here.",
                email="contact@yourdomain.com",
                location="Jdeideh"
            )
        return footer_content


from rest_framework import generics
from .models import ProcessPhoto
from .serializers import ProcessPhotoSerializer

class ProcessPhotoListView(generics.ListCreateAPIView):
    """
    View for listing and creating photos.
    """
    serializer_class = ProcessPhotoSerializer
    queryset = ProcessPhoto.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class ProcessPhotoCreateView(generics.CreateAPIView):
    serializer_class = ProcessPhotoSerializer
    queryset = ProcessPhoto.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        """
        Perform additional processing after creating the photo.
        You can modify this function to handle actions like image resizing, logging, etc.
        """
        # Call the serializer to save the photo to the database.
        photo = serializer.save()

        # Perform custom processing (e.g., logging, image resizing, etc.)
        self.process_photo(photo)
        return photo

    def process_photo(self, photo):
        """
        Placeholder for any post-creation logic (e.g., image processing or notifications).
        """
        print(f"Processing photo with ID: {photo.id}")
        # Example: You can add logic for resizing, compressing the image, etc.
        # photo.resize_image()  # hypothetical method, replace with real logic
        print(f"Photo {photo.id} processed successfully.")

    def create(self, request, *args, **kwargs):
        """
        Handle the actual creation process and return a response.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProcessPhotoDetailView(generics.RetrieveUpdateAPIView):
    """
    View for retrieving and updating a photo.
    This view handles the GET (retrieve) and PUT/PATCH (update) methods.
    """
    serializer_class = ProcessPhotoSerializer
    queryset = ProcessPhoto.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get(self, request, *args, **kwargs):
        """
        Retrieve a single photo or list of photos.
        """
        if 'pk' in kwargs:
            # Detail view
            photo = self.get_object()
            serializer = self.serializer_class(photo, context={'request': request})
            return Response(serializer.data)
        else:
            # List view
            photos = ProcessPhoto.objects.all().order_by('order')
            serializer = self.serializer_class(photos, many=True, context={'request': request})
            return Response(serializer.data)

    def update(self, request, pk=None):
        """
        Update an existing photo.
        """
        photo = self.get_object()
        serializer = self.get_serializer(photo, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ContactUsContentView(generics.RetrieveUpdateAPIView):
    def get(self, request, *args, **kwargs):
        # Try to get the first ContactUs instance, or create one if it doesn't exist
        contact_us, created = ContactUs.objects.get_or_create(
            defaults={
                'email': 'default@example.com',
                'phone_number': '000-000-0000',
                'location': 'Default Location'
            }
        )

        # Serialize the data and return it
        if contact_us:
            serializer = ContactUsSerializer(contact_us)
            return Response(serializer.data)
        # If no contact_us was found, return a 404 response
        return Response({'detail': 'Contact information not found.'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        # Try to get the first ContactUs instance, or create one if it doesn't exist
        contact_us, created = ContactUs.objects.get_or_create(
            defaults={
                'email': 'default@example.com',
                'phone_number': '000-000-0000',
                'location': 'Default Location'
            }
        )

        if contact_us:
            # Update the contact data with the new values
            serializer = ContactUsSerializer(contact_us, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'Contact information not found.'}, status=status.HTTP_404_NOT_FOUND)


class ShortListView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView
):
    queryset = Short.objects.all()
    serializer_class = ShortSerializer

    def get(self, request, *args, **kwargs):
        if "pk" in kwargs:
            return self.retrieve(request, *args, **kwargs)  # Retrieve a specific short
        return self.list(request, *args, **kwargs)  # List all shorts

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)  # Create a new short

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Get current data
        data = request.data.copy()
        if "video" not in data or not data["video"]:
            # Retain the old video if not provided in the request
            data["video"] = instance.video

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        if "pk" not in kwargs:
            return Response(
                {"error": "Missing short ID in URL"}, status=400
            )  # Handle no ID case
        try:
            short = self.get_object()
        except Short.DoesNotExist:
            raise NotFound("Short not found.")
        short.delete()
        return Response({"detail": "Short deleted successfully"}, status=204)


class AboutContentView(generics.RetrieveUpdateAPIView):
    queryset = AboutContent.objects.all()
    serializer_class = AboutContentSerializer

    def get_object(self):
        # Retrieve the single AboutContent instance or raise a 404 if it doesn't exist
        try:
            return AboutContent.objects.get()
        except AboutContent.DoesNotExist:
            raise NotFound("AboutContent instance not found. Please initialize one.")

class SubmitFormView(APIView):
    """Public view for submitting the form"""
    def post(self, request):
        serializer = FormSubmissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Form submitted successfully'}, 
                          status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Admin views
class SubmissionListView(ListAPIView):
    """Admin view to list all submissions"""
    serializer_class = FormSubmissionSerializer

    def get_queryset(self):
        queryset = FormSubmission.objects.all()

        # Filter by read/unread
        status = self.request.query_params.get('status', 'all')  # Default to 'all'
        if status == 'unread':
            queryset = queryset.filter(is_read=False)
        elif status == 'read':
            queryset = queryset.filter(is_read=True)

        # Filter by selection type
        selection = self.request.query_params.get('selection', 'all')  # Default to 'all'
        if selection != 'all':
            queryset = queryset.filter(selection=selection)

        # Search in name or email
        search = self.request.query_params.get('search', '').strip()  # Default to empty string
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(email__icontains=search)
            )

        return queryset

class SubmissionActionView(APIView):
    """Admin view for actions on submissions"""
    def delete(self, request, pk):
        """Delete a submission"""
        try:
            submission = FormSubmission.objects.get(pk=pk)
            submission.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except FormSubmission.DoesNotExist:
            return Response({'error': 'Submission not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, pk):
        """Mark as read/unread or toggle visibility"""
        try:
            submission = FormSubmission.objects.get(pk=pk)
            action = request.data.get('action')
            
            if action == 'mark_read':
                submission.is_read = True
                submission.save()
                return Response({'status': 'success', 'message': 'Submission marked as read'})

            elif action == 'toggle_hidden':
                submission.is_hidden = not submission.is_hidden
                submission.save()
                return Response({'status': 'success', 'message': 'Submission visibility toggled'})
            
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

        except FormSubmission.DoesNotExist:
            return Response({'error': 'Submission not found'}, status=status.HTTP_404_NOT_FOUND)


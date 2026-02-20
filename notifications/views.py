from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import EmailSerializer
from django.core.mail import EmailMessage

class SendEmailView(APIView):
    # This parser allows handling file uploads (multipart/form-data)
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = EmailSerializer(data=request.data)
        
        if serializer.is_valid():
            data = serializer.validated_data
            
            try:
                # 1. Construct the email
                email = EmailMessage(
                    subject=data['subject'],
                    body=data['message'],
                    from_email=None, # Uses EMAIL_HOST_USER from settings
                    to=[data['to_email']],
                )

                # 2. Attach files if they exist
                files = data.get('attachments', [])
                for file in files:
                    # attach(filename, content, mimetype)
                    email.attach(file.name, file.read(), file.content_type)

                # 3. Send immediately
                email.send(fail_silently=False)

                return Response({
                    "status": "success",
                    "message": "Email sent successfully"
                }, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({
                    "status": "error",
                    "message": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
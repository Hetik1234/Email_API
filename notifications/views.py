from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMessage
from django.conf import settings

class SendEmailView(APIView):
    def post(self, request):
        try:
            # Get data from the POST request
            to_email = request.data.get('to_email')
            subject = request.data.get('subject')
            message = request.data.get('message')
            from_name = request.data.get('from_name', 'CloudMail API') 
            reply_to = request.data.get('reply_to')

            if not all([to_email, subject, message]):
                return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

            # Format the From header to bypass Gmail's name override
            formatted_from = f"{from_name} <{settings.EMAIL_HOST_USER}>"

            # Use EmailMessage to unlock the reply_to header
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=formatted_from,
                to=[to_email],
                reply_to=[reply_to] if reply_to else None
            )
            
            email.send()

            return Response({"status": "success", "message": "Email sent successfully!"}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"❌ CRITICAL SMTP ERROR: {str(e)}", flush=True) 
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
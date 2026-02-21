from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.core.mail import EmailMessage  # <-- 1. Import EmailMessage instead of send_mail
from django.conf import settings

@api_view(['POST'])
def send_email_view(request):
    try:
        # Get data from the POST request
        to_email = request.data.get('to_email')
        subject = request.data.get('subject')
        message = request.data.get('message')
        from_name = request.data.get('from_name', 'CloudMail API') # Default name if none provided
        reply_to = request.data.get('reply_to')

        if not all([to_email, subject, message]):
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Format the From header to bypass Gmail's name override
        # Result looks like: "Mario's Pizza" <cloudmailapiservice@gmail.com>
        formatted_from = f"{from_name} <{settings.EMAIL_HOST_USER}>"

        # 3. Use EmailMessage to unlock the reply_to header
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=formatted_from,
            to=[to_email],
            reply_to=[reply_to] if reply_to else None  # reply_to must be a list
        )
        
        email.send()

        return Response({"status": "success", "message": "Email sent successfully!"}, status=status.HTTP_200_OK)

    except Exception as e:
        print(f"❌ CRITICAL SMTP ERROR: {str(e)}", flush=True) 
        return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
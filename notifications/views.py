from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.mail import EmailMessage
from django.conf import settings

class SendEmailView(APIView):
    # Tell DRF to accept multipart form file uploads
    parser_classes = (MultiPartParser, FormParser) 

    def post(self, request):
        try:
            to_email = request.data.get('to_email')
            subject = request.data.get('subject')
            message = request.data.get('message')
            from_name = request.data.get('from_name', 'CloudMail API') 
            reply_to = request.data.get('reply_to')
            
            # Use request.data so DRF grabs the parsed file object
            attachment = request.data.get('attachment') 

            if not all([to_email, subject, message]):
                return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

            formatted_from = f"{from_name} <{settings.EMAIL_HOST_USER}>"

            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=formatted_from,
                to=[to_email],
                reply_to=[reply_to] if reply_to else None
            )
            
            email.content_subtype = "html"
            attachment_status = "No attachment provided."

            # Verify the attachment exists AND is actually a file object (has a read() method)
            if attachment and hasattr(attachment, 'read'):
                email.attach(attachment.name, attachment.read(), attachment.content_type)
                attachment_status = f"Successfully attached file: {attachment.name}"
            elif attachment:
                # If attachment exists but isn't a file, curl sent it as a text string
                attachment_status = f"WARNING: Received text '{attachment}' instead of a file. Did you forget the '@' in your curl command?"
            
            email.send()

            return Response({
                "status": "success", 
                "message": "Email sent successfully!",
                "attachment_info": attachment_status  # <-- This will tell us exactly what happened!
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"❌ CRITICAL SMTP ERROR: {str(e)}", flush=True) 
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
from rest_framework import serializers

class EmailSerializer(serializers.Serializer):
    # Required fields
    to_email = serializers.EmailField()
    subject = serializers.CharField(max_length=200)
    message = serializers.CharField()
    
    # Optional fields (The "Option 1" magic)
    from_name = serializers.CharField(required=False, default="CloudMail Service")
    reply_to = serializers.EmailField(required=False)
    
    # Attachments
    attachments = serializers.ListField(
        child=serializers.FileField(),
        required=False
    )
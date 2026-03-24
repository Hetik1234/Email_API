CloudMail API Integration Guide
Welcome to the CloudMail API. This microservice provides a simple, robust endpoint for sending emails with custom sender names, reply-to routing, and file attachments.

Infrastructure Note: This API is served via AWS API Gateway and is fully TLS-encrypted (HTTPS).

The API is currently hosted at https://563u4wcc1g.execute-api.us-east-1.amazonaws.com/prod

To send an email 
 
Endpoint: /api/send/
Method: POST
Content-Type: multipart/form-data (Required if sending attachments)
Parameters
Field,Type,Required,Description
to_email,string,Yes,The recipient's email address.
subject,string,Yes,The subject line of the email.
message,string,Yes,The plain text body of the email.
from_name,string,No,"Custom sender name (Defaults to ""CloudMail API"")."
reply_to,string,No,Email address that recipient replies will route to.
attachment,file,No,A physical file to attach to the email.

Integration ExamplesHere are ready-to-use snippets for the most common programming languages.
1. cURL (Bash/Terminal)Bashcurl -X POST https://2rsma0i53j.execute-api.us-east-1.amazonaws.com/prod/api/send/ \
     -F "to_email=user@example.com" \
     -F "subject=Welcome to our app!" \
     -F "message=Thank you for signing up." \
     -F "from_name=Awesome App Team" \
     -F "reply_to=support@awesomeapp.com" \
     -F "attachment=@/path/to/your/document.pdf"
	 	 
2. Python (using requests)
Python
import requests

url = "https://2rsma0i53j.execute-api.us-east-1.amazonaws.com/prod/api/send/"

data = {
    "to_email": "user@example.com",
    "subject": "Your Invoice",
    "message": "Please find your invoice attached.",
    "from_name": "Billing Department",
    "reply_to": "billing@awesomeapp.com"
}

# Only include the files dictionary if you are sending an attachment
files = {
    "attachment": open("invoice.pdf", "rb")
}

response = requests.post(url, data=data, files=files)
print(response.json())

3. JavaScript / Node.js (using fetch)
JavaScript
const url = "https://2rsma0i53j.execute-api.us-east-1.amazonaws.com/prod/api/send/";
const formData = new FormData();

formData.append("to_email", "user@example.com");
formData.append("subject", "Hello from JS");
formData.append("message", "This email was sent via the secure API.");
formData.append("from_name", "Web Client");
formData.append("reply_to", "contact@awesomeapp.com");

// If attaching a file from an HTML <input type="file" id="fileInput">
// const fileField = document.querySelector('#fileInput');
// formData.append("attachment", fileField.files[0]);

fetch(url, {
    method: "POST",
    body: formData
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error("Error:", error));

Response Handling
The API will always return a JSON response so your application can handle success or failure gracefully.
Success Response (200 OK)
JSON{
    "status": "success",
    "message": "Email sent successfully!",
    "attachment_info": "Successfully attached file: invoice.pdf"
}
❌ Error Response (400 Bad Request)JSON{
    "error": "Missing required fields"
	}
	
	

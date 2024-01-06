BACKEND DEVELOPER TEST DOCUMENTATION
[REPO - LINK]

TEST CASE
Login Endpoint (api/login/) :-
Valid Login:
Input: Valid username and password.
Expected Output: Successful login with a status code of 200 and a response message.
Invalid Login:
Input: Invalid username or password.
Expected Output: Unauthorised access with a status code of 401 and an appropriate error message.

File Upload (api/upload/) :-
Valid File Upload:
Input: Upload a file with a valid format.
Expected Output: Successful file upload with a status code of 201 and a success message.
Invalid File Type Upload:
Input: Attempt to upload a file with an invalid format.
Expected Output: Rejection of the file upload with a status code of 400 and an error message.

User Signup  (api/signup/) 
Valid User Signup:
Input: Provide valid user data.
Expected Output: Successful user registration with a status code of 201 and a registration confirmation message.
Invalid User Signup:
Input: Attempt to sign up with invalid user data.
Expected Output: Rejection of user registration with a status code of 400 and appropriate error messages.

Email Verification (api/verify-email/uid/token/) :-
Valid Email Verification:
Input: Use a valid verification link.
Expected Output: Successful email verification with a status code of 200 and a verification confirmation message.
Invalid Email Verification:
Input: Use an invalid or expired verification link.
Expected Output: Unsuccessful email verification with a status code of 400 and an error message.

Download file (api/download-file/file-id/) :-
Valid File Download:
Input: Request to download a file with a valid file ID.
Expected Output: Successful file download with a valid download link and a status code of 200.

List All Uploaded Files (api/list-uploaded-files/) :-
List Uploaded Files:
Input: Request to list all uploaded files.
Expected Output: Successfully retrieve a list of uploaded files with a status code of 200.

DEVELOPMENT PLAN
Environment Setup :-
=> Ensuring the production environment is ready by installing all the necessary tools for running Django applications.
=> By Keeping things organised using a requirements.txt file to manage dependencies.

Database Migration (PostgreSQL):
=> Making sure the database is set up correctly by running Django's migration commands.
=> Using PostgreSQL for the database as it's reliable and performs well.

Web Server Configuration (Nginx): Configuring Nginx to deal with static files and direct requests to the Django app.

Security Measures:
=> Securing data in transit by enabling HTTPS.
=> Keeping the server safe by following security best practices and setting up firewalls.

Email Configuration: Setting up email configurations (e.g., SMTP) for user verification and improved communication.

Documentation: Regularly updating and maintaining a clear documentation outlining the backend development process.



Post Deployment Monitoring: 
=> Implement processes for post-deployment monitoring using Render to ensure ongoing stability.
=> Developing effective communication strategies to inform users about new features and updates.	

REPONSE SNAPSHOTS










GMAIL VERIFICATION :-








# Hospital_management_app
This is a backend application for hospital management system made with the help of FastAPI, SQLite3 and OAuth 2.0


## OVERVIEW:
Go to https://hospital-management-app.onrender.com for backend overview.Wait for 10 seconds give it time to load.
Keep in mind that this is just backend part of the application .
Thus, you will need to run it on OpenAPI or Postman.

## Working of the Application:
This is a backend of hospital management system. This project works like the real world hospital management system where once the patient is admited,their details 
are filled by the admin.Once a doctor is assigned to the patient we can also see patient details along wiht the doctor assigned.Patients and Doctors have a many to mant relationship which helps us assign different patients to a single doctor and vice versa.\
\
Sidenote- Admin authentication is done by OAuth 2.0 .


## Installation 
##### 1.Clone the above repo
        git clone https://github.com/divyansh3690/Hospital_management_app.git
        
##### 2. Install the requirements
         pip install -r req.txt
         
##### 3. Run the following command on terminal
         uvicorn main:app --reload


Now, as mentioned above there are two ways to run the application:
1. By uvicorn server that will be live on http://127.0.0.1:8000 or the mentioned url in terminal after you run 3rd command in terminal.
2. By online hosting i.e done by render here at https://hospital-management-app.onrender.com.



## API Endpints:
#### 1. ADMIN

##### i.)  Adding new admin (POST operation)
            /admin/add
##### ii.) Login (POST operation)
            /admin/token
######   NOTE- This request will return a token for authentication of the user.
######         Always use these commands after the specified url.

#### 2. DOCTORS
        
#####   i.)  Show all doctors in the hospital (GET operation)
            /doctors/        
#####   iii.) Add new doctor  (POST operation)            
            /posts/                     
#####   iv.)  Edit a doctor's details(PUT operation)            
            /posts   
#####   v.)   Delete a doctor from database (DELETE operation)            
            /posts
            
#### 3. PATIENTS
        
#####   i.)  Show all the patients in the hospital (GET operation)
            /patients/        
#####   ii.) Show details of a specific patient(GET operation)
            /patients/{patient_id}    
#####   iii.) Add new patient  (POST operation)            
            /patients/                     
#####   iv.)  Edit a patient's details(PUT operation)            
            /patients/
#####   v.)   Delete a patient from the database (DELETE operation)            
            /patients/
#####   vi.) Assign doctor to a patient
            /patients/doc
            
Note- Keep in mind to perform any restricted task you need admin login.
            
            

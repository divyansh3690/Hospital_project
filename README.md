# Health Connect
This is a hospital backend application made with the help of FastAPI, SQLite3 and OAuth 2.0.It also has payment integration via RazorPay and email automation.


## OVERVIEW:
**HealthConnect** is an advanced hospital backend application that streamlines medical operations and patient care. It features three APIs for Patients, Doctors, and Authentication, ensuring secure data access. _OAuth 2.0_ with JWT tokens enhances user authentication and authorization. The _sqlite3_ backend ensures scalable data storage. _FastAPI-Mail_ automates appointment confirmations via email. _Razorpay_ integration enables smooth online payments. The project prioritizes data security through encryption and regular audits. 

## Working of the Application:
This project works like the real world hospital management system where the patient comes in to book an appointment.Once he/she enters there information they recieve an automated confirmation via Email.Along with this, they can do hasle free payment via RazorPay as the project has payment integration.Once a doctor is assigned to the patient we can also see patient details along with the doctor assigned.Patients and Doctors have a many to mant relationship which helps us assign different patients to a single doctor and vice versa.\


## Installation 
##### 1.Clone the above repo
       https://github.com/divyansh3690/Hospital_project.git
        
##### 2. Install the requirements
         pip install -r req.txt
         
##### 3. Run the following command on terminal
         uvicorn main:app --reload

//Note- The project has used its razor pay keys.Make sure while running it we replace it with personal razor pay keys.


## API Endpints:
#### 1. ADMIN

##### i.)  Adding new admin (POST operation)
            /admin/add
##### ii.) Login (POST operation)
            /admin/token
######   NOTE- This request will return a token for authentication of the user.
##### ii.) Delete admin (DELETE operation)
            /admin/delete-admin
            

###### Always use these commands after the specified url.

#### 2. DOCTORS
        
#####   i.)  Show all doctors in the hospital (GET operation)
            /doctors/        
#####   iii.) Add new doctor  (POST operation)            
            /doctors/                     
#####   iv.)  Edit a doctor's details(PUT operation)            
            /doctors   
#####   v.)   Delete a doctor from database (DELETE operation)            
            /doctors
            
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
#####   vii.)Create payment_ticket(POST operation)
            /patients/create_order
#####   vii.)Verify the payment (GET operation)
            /patients/verify_order/{input}
            
Note- Keep in mind to perform any restricted task you need admin login.
            
            

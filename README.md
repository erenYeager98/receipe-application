# Recipe-application
This is a markdown file, please open it in markdown viewer for better experience

### Backend:
The backend is developed using fastAPI and with sqlalchemy. (Requirements are given in document)
##Frontend:
The frontend is developed using react. 

### Steps to Reproduce:
1. Extract the zip
2. cd into backend directory
3. Download the requirements using ```pip install -r requirements.txt```
5. If not created database, create a database with the name "recipes"
6. The bulk_insert.py file will feed all the json data into the mysql database.
7. Just run the script before initiating the backend. It will update the sql table.
8. Change the db username and password in the DatabseURL variable.
9. The schema will be created after intiting the backend
10. Start the backend using command ```uvicorn main:app --port 8000 --reload```
11. Now go to frontend usind cd frontend
12. run the react app using npm start

### Endpoints:
```
localhost:8000/api/recipes/search
localhost:8000/api/recipes/
localhost:8000/add_recipe/
```

## Output:
Database import
![image](https://github.com/user-attachments/assets/bc550386-d378-40d8-9756-48a4cc380806)
UI
![image](https://github.com/user-attachments/assets/07fcb94f-6806-47c1-9f6c-ace9aa672795)
JSON Result
![image](https://github.com/user-attachments/assets/302064d4-2eaa-4b01-82d4-91f1816172db)
Interactive Request and Response
![image](https://github.com/user-attachments/assets/f67ab720-3c30-46cd-a3a5-bd982b38340d)



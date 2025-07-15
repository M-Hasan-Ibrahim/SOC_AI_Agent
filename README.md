# SOC_AI_Agent

<<<<<<< HEAD
Create a .env file in the root directory beside Dockerfiel with this content inside:  
=======
Create a .env file in the root directory beside Dockerfile with this content inside:  
>>>>>>> c3ae05f8eb06ec5e7cdf45180480f577142a67fb
    POSTGRES_USER={POSTGRES USERNAME}  
    POSTGRES_PASSWORD={POSTGRES PASSWORD}  
    POSTGRES_DB={POSTGRES DATABASE NAME}  
    PGADMIN_DEFAULT_EMAIL={PGADMIN EMAIL}  
<<<<<<< HEAD
    PGADMIN_DEFAULT_PASSWORD={PGADMIN PASSWORD}      

To build docker:  
docker compose up --build       
      

to access pgadmin: go to localhost:5050 and enter the credentials  
click add new server  
 in the general tab add any name you want  
 in the connection tab name the host: db, username and password the same as (postgres_user and postgres_password) in the .env file  
then go to Databses -> POSGRES_DB_NAME -> Schemas -> public -> Tables -> right click on the table and click View/Edit  
  
    
To seed the database with test alerts run in a new terminal:  
docker compose exec api python -m app.fill_database
=======
    PGADMIN_DEFAULT_PASSWORD={PGADMIN PASSWORD}  
>>>>>>> c3ae05f8eb06ec5e7cdf45180480f577142a67fb

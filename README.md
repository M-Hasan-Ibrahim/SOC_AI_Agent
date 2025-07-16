# SOC_AI_Agent
You can use both openai and deepseek in this project, change the llm model in app/workflow.py, requirements file will download both libraries for openai and deepseek ollama  
ollama:  
ollama_base_url = "http://host.docker.internal:11434"  

    llm = Ollama(  
        model="deepseek-r1:8b",        
        base_url=ollama_base_url,        
    )  
openai:    
llm = ChatOpenAI(  
    model="gpt-4o-mini",  
    api_key=os.environ["OPENAI_API_KEY"]  
)  


1- Create a .env file in the root directory beside Dockerfile with this content inside:  
    POSTGRES_USER={POSTGRES USERNAME}  
    POSTGRES_PASSWORD={POSTGRES PASSWORD}  
    POSTGRES_DB={POSTGRES DATABASE NAME}  
    PGADMIN_DEFAULT_EMAIL={PGADMIN EMAIL}  
    PGADMIN_DEFAULT_PASSWORD={PGADMIN PASSWORD}  
    ABUSEIPDB_API_KEY={ABUSEIPDB API KEY}   #create it from abuseipdb website  
    IPINFO_API_KEY={ABUSEIPDB API KEY}   #create it from abuseipdb website  
    VIRUSTOTAL_API_KEY={ABUSEIPDB API KEY}   #create it from abuseipdb website  
    OPENAI_API_KEY={OPENAI API KEY} #go to platform.openai.com  

2- To build docker:  
docker compose up --build       
      

3- to access pgadmin: go to localhost:5050 and enter the credentials  
click add new server  
 in the general tab add any name you want  
 in the connection tab name the host: db, username and password the same as (postgres_user and postgres_password) in the .env file  
then go to Databses -> POSGRES_DB_NAME -> Schemas -> public -> Tables -> right click on the table and click View/Edit  
  
    
4- To seed the database with test alerts run in a new terminal:  
docker compose exec api python -m app.fill_database



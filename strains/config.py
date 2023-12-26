from dotenv import load_dotenv
import os


load_dotenv('.env')




# Env Vars
# ===================================
POSTGRES_CONNECTION_STRING = os.getenv('POSTGRES_CONNECTION_STRING')
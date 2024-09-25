import os
from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings
load_dotenv(find_dotenv()) # This is used to load the environment variables from the .env file
kafka_broker_address = os.environ['KAFKA_BROKER_ADDRESS']





class Settings(BaseSettings):

    kafka_broker_address: str = kafka_broker_address
    
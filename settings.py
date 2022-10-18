from pydantic import BaseSettings, EmailStr

class Settings(BaseSettings):
    EMAIL_LOGIN: EmailStr = 'example@gmail.com'
    EMAIL_PASSWORD: str = 'example_password'
    
    
def get_settings() -> Settings:
    return Settings()

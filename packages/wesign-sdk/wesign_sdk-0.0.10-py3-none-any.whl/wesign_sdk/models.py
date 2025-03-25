from pydantic import BaseModel

class Config(BaseModel):
    api_url: str
    api_key: str
    
if __name__ == "__main__":
    # Code to execute if run as a script
    print("Running as a script")
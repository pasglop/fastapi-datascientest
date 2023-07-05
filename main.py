import os
import dotenv
import uvicorn

dotenv.load_dotenv()

API_HOST = os.environ.get('API_HOST')
API_PORT = int(os.environ.get('API_PORT'))

if __name__ == "__main__":
    uvicorn.run("app.api.v1.api:app", host=API_HOST, port=API_PORT, reload=True)

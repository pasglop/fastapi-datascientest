import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.api.v1.api:app", host="0.0.0.0", port=8081, reload=True)
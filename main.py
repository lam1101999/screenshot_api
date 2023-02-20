"Main module"
import uvicorn
from fastapi import FastAPI
from routers import screenshot_router


app = FastAPI()
app.include_router(screenshot_router.router)


@app.get("/")
async def homepage():
    """Welcome page

    Returns:
        str: welcome
    """
    return "Welcome to our homepage"

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)

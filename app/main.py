from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.chat import router as chat_router
from app.api.memory import router as memory_router
from app.api.tools import router as tools_router

app = FastAPI(title="FastAPI AI Assistant")

# Add CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers
app.include_router(chat_router)
app.include_router(memory_router)
app.include_router(tools_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Assistant API!"}

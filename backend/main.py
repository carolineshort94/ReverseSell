from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from auth import router as auth_router

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(auth_router)


@app.get("/")
async def root():
    return {"message": "welcome to reverse sell backend API1"}

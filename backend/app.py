from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from responder import generate_response

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Support Agent API is running."}

@app.post("/respond")
async def respond(request: Request):
    data = await request.json()
    user_message = data.get("message", "")
    print(f"🔹 Received message: {user_message}")
    response = generate_response(user_message)
    return {"response": response}

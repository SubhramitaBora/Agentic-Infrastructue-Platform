from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.agents.devops_agent import devops_agent

app = FastAPI(
    title="Agentic Infrastructure Operations Platform"
)


class UserRequest(BaseModel):
    request: str


@app.get("/")
def root():
    return {
        "message": "Agentic Infrastructure Operations Platform is running"
    }


@app.post("/agent")
async def agent_gateway(user_request: UserRequest):

    request = user_request.request

    try:
        result = await devops_agent(request)

        return {
            "received_request": request,
            "routing_result": result
        }

    except Exception:
        raise HTTPException(
            status_code=502,
            detail={
                "status": "failed",
                "message": (
                    "The request could not be completed due to "
                    "an error in an agent or external service."
                )
            }
        )
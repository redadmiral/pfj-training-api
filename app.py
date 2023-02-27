from fastapi import FastAPI
from typing import Set, List
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, RedirectResponse
import uvicorn

app = FastAPI()

@app.get("/", tags=["Maintenance"])
async def redirect():
    """
    Redirect to documentation if index page is called.
    """
    response = RedirectResponse(url="/docs")
    return response


@app.get("/get_html", response_class=HTMLResponse)
async def html_example_get_endpoint(number: int, multiplier: int):
    html_code = f"<h1>Result</h1> <p> {multiplier} times {number} is {number*multiplier}</p>"
    return html_code

@app.get("/get_json")
async def json_example_get_endpoint(number: int, multiplier: int):
    return {"result": number*multiplier}

class post_input(BaseModel):
    number: int
    multiplier: int

class post_response(BaseModel):
    result: int

@app.post("/post_json")
async def json_example_post_endpoint(postinput: post_input) -> post_response:
    response = post_response(
        result = postinput.number*postinput.multiplier,
    )
    return response

queue: Set[int] = set()

class put_response(BaseModel):
    queue: Set[int]

@app.put("/put_json")
async def int_example_put_endpoint(id: int):
    queue.add(id)
    return put_response(queue=queue)

@app.delete("/delete_json")
async def example_delete_endpoint(id: int):
    try:
        queue.remove(id)
    except KeyError:
        pass
    return put_response(queue=queue)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
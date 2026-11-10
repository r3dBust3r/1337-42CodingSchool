from src.cli import CommandLineInterface
from src.error import RagError
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from typing import Dict


class QueryRequest(BaseModel):
    query: str
    k: int = 5
    index_dir: str = 'data/processed/'


app = FastAPI()
cli = CommandLineInterface()


@app.get('/health')
def health() -> Dict:
    return {'status': 'ok'}


@app.post('/answer')
def answer(request: QueryRequest) -> Dict:
    try:
        result = cli.answer(
            query=request.query,
            k=request.k,
            index_dir=request.index_dir
        )

        return result.model_dump()

    except RagError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception:
        raise HTTPException(
            status_code=500,
            detail='Internal server error'
        )

import uvicorn
from src import main


if __name__ == '__main__':
  uvicorn.run(app="src.main:app", host="0.0.0.0", port=8080, reload=True)

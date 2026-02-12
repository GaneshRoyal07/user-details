import sys
try:
    import fastapi
    import uvicorn
    import pydantic
    print(f"FastAPI: {fastapi.__version__}")
    print(f"Uvicorn: {uvicorn.__version__}")
    print(f"Pydantic: {pydantic.VERSION}")
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Error: {e}")

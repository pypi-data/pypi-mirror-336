import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


__version__ = "0.0.17"


class Cotlette(FastAPI):

    def __init__(self):
        super().__init__()
        
        # Подключение роутеров
        self.include_routers()
        
        # Получить абсолютный путь к текущей диретории
        current_file_path = os.path.abspath(__file__)
        current_directory = os.path.dirname(current_file_path)
        static_directory = os.path.join(current_directory, "static")
        self.mount("/static", StaticFiles(directory=static_directory), name="static")

    def include_routers(self):

        # Подключаем роутеры к приложению
        from cotlette.urls import urls_router, api_router
        self.include_router(urls_router)
        self.include_router(api_router, prefix="/api", tags=["common"],)

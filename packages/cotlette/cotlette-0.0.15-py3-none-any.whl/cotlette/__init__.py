from fastapi import FastAPI


__version__ = "0.0.15"


class Cotlette(FastAPI):

    def __init__(self):
        super().__init__()
        
        # Подключение роутеров
        self.include_routers()

    def include_routers(self):

        # Подключаем роутеры к приложению
        from cotlette.urls import urls_router, api_router
        self.include_router(urls_router)
        self.include_router(api_router, prefix="/api", tags=["common"],)

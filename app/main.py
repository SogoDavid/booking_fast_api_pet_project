import time

import aioredis as aioredis
import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_versioning import VersionedFastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel
from sqladmin import Admin

from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.bookings.router import router as router_bookings
from app.config import settings
from app.database import engine
from app.hotels.rooms.router import router as room_hotels
from app.hotels.router import router as router_hotels
from app.images.router import router as router_images
from app.importer.router import router as router_importer
from app.logger import logger
from app.prometheus.router import router as router_prometheus

# from app.pages.router import router as router_pages
from app.users.router import router as router_users

app = FastAPI()

sentry_sdk.init(
    dsn="https://fccad67b7e23460cb00522cffea500c6@o4505261941719040.ingest.sentry.io/4505261944406016",
    traces_sample_rate=1.0,
)


app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(room_hotels)
app.include_router(router_images)
app.include_router(router_importer)
app.include_router(router_prometheus)


# app.include_router(router_pages)


class Translation(BaseModel):
    translation_lang: str
    translation: str


origins = [
    "http://localhost:8000",
    "http://localhost:62148",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)

if settings.MODE == "TEST":

    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:" f"{settings.REDIS_PORT}",
        encoding="utf8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info("Request execution time", extra={
        "process_time": round(process_time, 4)
    })
    return response

app = VersionedFastAPI(app,
                       version_format='{major}',
                       prefix_format='/v{major}',
                       )

app.mount("/static", StaticFiles(directory="app/static"), "static")
instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"]
)
instrumentator.instrument(app).expose(app)
admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)

@app.on_event("startup")
def startup():
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

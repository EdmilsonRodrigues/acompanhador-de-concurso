from contextlib import asynccontextmanager

from fastapi import FastAPI

from .config import VERSION
from .controllers.auth_controller import router as auth_router
from .controllers.search_alert_controller import (
    router as search_alert_controller,
)
from .controllers.subscription_controller import router as subscription_router
from .controllers.user_controller import router as user_router
from .services.database_service import create_db_and_tables, get_engine
from .webhooks.stripe_webhooks import router as stripe_webhook_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event for the application.

    It creates the database and tables if they don't exist.

    It also disposes of the database connection when the application is stopped

    :param app: The FastAPI application
    :type app: FastAPI
    """
    engine = get_engine()
    create_db_and_tables(engine)
    yield
    engine.dispose()


app = FastAPI(
    title='Backend da aplicação de acompanhamento de concursos',
    version=VERSION,
    lifespan=lifespan,
)


@app.get('/')
def healthcheck():
    """
    Healthcheck endpoint.

    Is used to check if the application is running and able to serve requests.

    It returns a JSON object with the current version of the application.
    """
    return {'version': VERSION}


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(subscription_router)
app.include_router(stripe_webhook_router)
app.include_router(search_alert_controller)

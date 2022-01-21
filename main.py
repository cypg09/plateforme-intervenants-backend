from fastapi import FastAPI
from logger import create_logger
from api import auth, user, etude
from sql import models, database

logger = create_logger("MAIN")

logger.info("Starting MAIN...")

app = FastAPI(
    title="SkemaConseil"
)

models.Base.metadata.create_all(bind=database.engine)

app.include_router(auth.api_auth)
app.include_router(auth.token_auth)
app.include_router(user.api_user)
app.include_router(etude.api_etude)


logger.info("Started MAIN.")

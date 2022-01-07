from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import user, auth, refresh_token, otp, trial_image, send_otp
from .routers import upload_image, products

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(refresh_token.router)
app.include_router(otp.router)
app.include_router(trial_image.router)
app.include_router(send_otp.router)
app.include_router(upload_image.router)
app.include_router(products.router)


# HOME ROUTE


@app.get("/")
async def root():
    return {"message": "Hello Vizart"}

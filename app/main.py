from fastapi import FastAPI
from app.database import Base, engine
from app.routes import auth, users, consumption, savings
from app.routes.savings import router as savings_router

# Initialize the database
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Energy Management System")

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(consumption.router, prefix="/consumption", tags=["Energy Consumption"])
app.include_router(savings.router, prefix="/savings", tags=["Savings Report"])
app.include_router(savings_router, prefix="/consumption")

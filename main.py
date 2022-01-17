from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from infrastructure.create_tables import create
from datetime import date

import click

#Routes
from application.routes import auth_route
from application.routes import company_route
from application.routes import product_route
from application.routes import user_route

#APP instance
app = FastAPI()

#DB tables creation
@app.on_event('startup')
async def create_tables():
    create()

@app.on_event('shutdown')
async def say_bye():
    click.echo(click.style("Bye Bye! Hope liked <3", 'green'))

#Routes
app.include_router(auth_route.router)
app.include_router(company_route.router)
app.include_router(product_route.router)
app.include_router(user_route.router)

#CORS Policy
origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def sayhi():
    return {"MSG:": "HI"}
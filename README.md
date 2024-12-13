FastAPI Project

Description

This project is a RESTful API built using FastAPI, designed for high-performance APIs with additional functionality for handling DataFrames.

Features
FastAPI-based API endpoints.
Integrated with Poetry for package management.
Database migrations handled using Alembic.
DataFrame functionality for processing and analyzing tabular data.

Installation

Clone the repository:
git clone <repository-url>
cd fastapi-project

Install Poetry:
pip install poetry

Install dependencies:
poetry install

Apply migrations using Alembic:
poetry run alembic upgrade head

Start the FastAPI server:
poetry run uvicorn main:app --reload

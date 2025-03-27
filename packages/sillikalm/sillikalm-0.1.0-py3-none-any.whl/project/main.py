# Summary: This script serves as the entry point for running the FastAPI application.
# It imports the FastAPI instance from the api module and runs the application using Uvicorn.
# The server is configured to run on localhost at port 8086 with hot reload enabled.
# Copyright © 2025 Krishnakanth Allika.
# Licensed under the MIT License (with Attribution & Modification Notice).
# You are free to share and adapt this work, provided that appropriate credit is given.
# For inquiries, contact: speed-acorn-whiff@duck.com
# Full license details: See LICENSE file.

from fastapi import FastAPI
import uvicorn

from project.src import api  # Importing FastAPI instance from app.py

app = api.app


def start_sillikalm():
    uvicorn.run(
        "project.src.api:app",
        host="localhost",
        port=8085,
        reload=False,
        timeout_keep_alive=60 * 60 * 24,
    )


if __name__ == "__main__":
    # Start the FastAPI app
    start_sillikalm()

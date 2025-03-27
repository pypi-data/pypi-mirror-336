# Description: This module defines the FastAPI application and its endpoints for managing models.
# Author: Krishnakanth Allika
# Email: speed-acorn-whiff@duck.com
# Licensed under the GNU General Public License v3 (GPLv3).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see https://www.gnu.org/licenses/gpl-3.0-standalone.html.

import os
import pickle
from cryptography.fernet import Fernet
from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import BackgroundTasks
from typing import Literal
import ollama
import subprocess
import webbrowser

from project.src.logger import logger
from contextlib import asynccontextmanager
from importlib.resources import files

# Get the base directory
BASE_DIR = files("project")
STATIC_DIR = BASE_DIR.joinpath("static")
ENV_FILE = BASE_DIR.joinpath(".env")
MODELS_FILE = BASE_DIR.joinpath("import/models.pkl")
LOG_FILE = BASE_DIR.joinpath("logs/sillikalm.log")


def terminate_processes():
    """
    Terminate the ollama serve and open-webui serve processes if they are running.
    """
    global ollama_process, open_webui_process

    # Terminate the ollama serve process
    if ollama_process:
        ollama_process.terminate()
        ollama_process.wait()
        logger.info("Terminated ollama serve process")

    # Terminate the open-webui serve process
    if open_webui_process:
        open_webui_process.terminate()
        open_webui_process.wait()
        logger.info("Terminated open-webui serve process")


# Updated lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    global ollama_process, open_webui_process
    try:
        # Startup logic
        ollama_process = subprocess.Popen(["ollama", "serve"])
        logger.info("Started ollama serve process")

        webbrowser.open("http://localhost:8085/", new=0)
        logger.info("Opened http://localhost:8085/ in the default web browser")

        logger.info("Started open-webui serve process")
        open_webui_process = subprocess.Popen(["open-webui", "serve", "--port", "8086"])

        yield  # Hand over control to the application
    finally:
        # Use the terminate_processes function
        terminate_processes()


# Pass the lifespan context manager to the FastAPI app
app = FastAPI(lifespan=lifespan)

# Serve the static directory
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Load the key from the .env file
from dotenv import load_dotenv

load_dotenv(dotenv_path=ENV_FILE)
key = os.getenv("KEY")

# Initialize Fernet with the key
fernet = Fernet(key)

# Define base models
base_models = [
    ["llama3.2", "SmallModel", "2GB", "recommended"],
    ["gemma3:4b", "SmallModel", "3.3GB"],
    ["qwen2.5:3b", "SmallModel", "1.9GB"],
    ["tinyllama", "TinyModel", "638MB"],
    ["llama3.2:1b", "TinyModel", "1.3GB"],
    ["gemma3:1b", "TinyModel", "815MB"],
    ["deepseek-r1:1.5b", "TinyModel", "1.1GB"],
    ["qwen2.5:1.5b", "TinyModel", "986MB"],
    ["qwen2.5:0.5b", "TinyModel", "398MB"],
]
base_model_options = ["_".join(base_model) for base_model in base_models]

# Global variables to store the ollama serve and open-webui serve processes
ollama_process = None
open_webui_process = None


@app.get("/")
async def read_index():
    """
    Serve the index.html file.
    """
    index_file = STATIC_DIR.joinpath("index.html")  # Dynamically resolve the path
    logger.info(f"Serving {index_file}")
    return FileResponse(index_file)


# Updated /shutdown endpoint
@app.post("/shutdown")
async def shutdown(background_tasks: BackgroundTasks):
    """
    Shutdown the FastAPI app and the running ollama serve and open-webui processes.

    This endpoint terminates the ollama serve and open-webui processes and shuts down the FastAPI app.

    Returns:
        dict: A dictionary containing the shutdown status.
    """
    logger.info("Received request to shutdown the application")

    # Use the terminate_processes function
    terminate_processes()

    # Add a task to forcefully exit the application
    background_tasks.add_task(lambda: os._exit(0))

    return {"message": "SillikaLM is shutting down"}


# Update the models file path in the /create_models endpoint
@app.post("/create_models")
async def create_models(
    base_model_info: str = Form(...),
):
    """
    Create new models based on the provided base model info.

    Args:
        base_model_info (str): The base model info in the format "base_model_name_size_category"
            e.g. "llama3.2_2GB_recommended"

    Returns:
        dict: A dictionary containing the status of the models creation.

    Example:
        {
            "Models import status": "Success",
            "Models added": [
                "llama3.2:1b_SillikaLM",
                "gemma3:1b_SillikaLM",
                "tinyllama_SillikaLM"
            ]
        }
    """
    logger.info(
        f"Received request to create models with base model info: {base_model_info}"
    )
    api_response = {}
    try:
        # Load the models from the models.pkl file
        with open(MODELS_FILE, "rb") as f:
            models = pickle.load(f)
        api_response["Models import status"] = "Success"
        logger.info("Models imported successfully from models.pkl")
        logger.debug(f"Imported models: {models}")
    except Exception as e:
        logger.error(f"Failed to import models: {e}")
        api_response["Models import status"] = "Error"
        api_response["Error message"] = str(e)
        return api_response

    # Get the index of the selected base model info
    base_model_index = base_model_options.index(base_model_info)
    # Get the base model name from base_models using the index
    base_model_name = base_models[base_model_index][0]
    logger.info(f"Selected base model: {base_model_name}")
    try:
        ollama.pull(base_model_name)
        logger.info(f"Base model {base_model_name} pulled successfully")
    except Exception as e:
        logger.error(f"Failed to pull base model {base_model_name}: {e}")
        api_response["Base model import status"] = "Error"
        api_response["Error message"] = str(e)
        return api_response

    models_list = []
    for k, v in models.items():
        try:
            decrypted_value = fernet.decrypt(v).decode().replace("\n", "\r\n")
            model_name = f"{k}:{base_model_name.translate(str.maketrans(':./', '---'))}_SillikaLM"
            logger.debug(
                f"Creating model {model_name} from base model {base_model_name}"
            )
            ollama.create(
                model=model_name,
                from_=base_model_name,
                system=decrypted_value,
                parameters={"temperature": 1},
            )
            models_list.append(model_name)
            logger.info(f"Model {model_name} created successfully")
        except Exception as e:
            logger.error(f"Error creating model {model_name}: {e}")
            api_response["Models import status"] = "Error"
            api_response["Error message"] = str(e)
            return api_response
    # ollama.delete(base_model_name)
    logger.info(f"Base model {base_model_name} deleted successfully")
    api_response["Models added"] = models_list
    return api_response


def format_size(size_in_bytes):
    """
    Format the given size in bytes to a human-readable string
    in MB or GB.

    Args:
        size_in_bytes (int): The size in bytes to format.

    Returns:
        str: A string representing the size in MB or GB with 2 decimal places.
    """
    size_in_mb = size_in_bytes / (1024 * 1024)
    if size_in_mb >= 1024:
        size_in_gb = size_in_mb / 1024
        return f"{size_in_gb:.2f} GB"
    else:
        return f"{size_in_mb:.2f} MB"


@app.post("/list_models")
async def list_models():
    """
    List all available models with their details.

    This endpoint retrieves all models available in the system and returns
    their details such as model name, size, number of parameters, quantization
    level, and last modified date.

    Returns:
        dict: A dictionary containing a list of models with their details or
        an error message if the listing fails.

    Example Response:
        {
            "Models": [
                {
                    "Model Name": "llama3.2:1b_SillikaLM",
                    "Size": "1.3 GB",
                    "Parameters": "1B",
                    "Quantization": "int8",
                    "Last Modified": "2023-10-01T12:00:00"
                },
                ...
            ]
        }
    """

    logger.info("Received request to list models")
    api_response = {}
    try:
        models = ollama.list()
        logger.debug(f"Retrieved models: {models}")
        api_response["Models"] = sorted(
            [
                {
                    "Model Name": model.model,
                    "Size": format_size(model.size),
                    "Parameters": model.details["parameter_size"],
                    "Quantization": model.details["quantization_level"],
                    "Last Modified": model.modified_at,
                }
                for model in models.models
            ],
            key=lambda x: x["Model Name"],
        )
        logger.info("Models listed successfully")
    except Exception as e:
        logger.error(f"Error listing models: {e}")
        api_response["Error message"] = str(e)
    return api_response


@app.post("/delete_models")
async def delete_models(model_name: str = Form(...)):
    """
    Delete a specific model based on the provided model name.

    This endpoint deletes the model specified by the `model_name` form field.

    Args:
        model_name (str): The name of the model to delete.

    Returns:
        dict: A dictionary containing the status of the model deletion.

    Example Response:
        {
            "Model deletion status": "Model llama3.2:1b_SillikaLM deleted successfully"
        }
    """
    logger.info(f"Received request to delete model: {model_name}")
    api_response = {}
    try:
        models = ollama.list()
        models = [model.model for model in models.models]
        logger.debug(f"Available models: {models}")
        if model_name not in models:
            api_response["Model deletion status"] = f"Model {model_name} not found"
            logger.warning(f"Model {model_name} not found")
            return api_response
        ollama.delete(model_name)
        api_response["Model deletion status"] = (
            f"Model {model_name} deleted successfully"
        )
        logger.info(f"Model {model_name} deleted successfully")
    except Exception as e:
        logger.error(f"Error deleting model {model_name}: {e}")
        api_response["Error message"] = str(e)
    return api_response


@app.post("/delete_all_models")
async def delete_all_models():
    """
    Delete all Silly Language Models created by SillikaLM.

    This endpoint deletes all language models created by SillikaLM.

    Returns:
        dict: A dictionary containing the status of the models deletion.

    Example Response:
        {
            "Models deletion status": {
                "llama3.2:1b_SillikaLM": "Deleted",
                "gemma3:1b_SillikaLM": "Deleted",
                "tinyllama_SillikaLM": "Deleted"
            }
        }
    """
    logger.info("Received request to delete all Silly Language Models")
    api_response = {}
    try:
        models = ollama.list()
        models_to_delete = [
            model.model for model in models.models if model.model.endswith("_SillikaLM")
        ]
        logger.debug(f"Models to delete: {models_to_delete}")

        if not models_to_delete:
            api_response["Model deletion status"] = "No Silly Language Models found"
            logger.info("No Silly Language Models found")
            return api_response

        api_response["Models deletion status"] = {}

        for model_name in models_to_delete:
            try:
                ollama.delete(model_name)
                api_response["Models deletion status"][model_name] = "Deleted"
                logger.info(f"Model {model_name} deleted successfully")
            except Exception as e:
                api_response["Models deletion status"][model_name] = str(e)
                logger.error(f"Error deleting model {model_name}: {e}")

    except Exception as e:
        logger.error(f"Error deleting all models: {e}")
        api_response["Error message"] = str(e)

    return api_response


@app.get("/list_base_models")
async def list_base_models():
    """
    List all available base models.

    This endpoint returns a list of all available base models that can be used to create new Silly Language Models.

    Returns:
        dict: A dictionary containing the list of base models.

    Example Response:
        {
            "base_models": [
                "llama3.2",
                "gemma3",
                "tinyllama",
                ...
            ]
        }
    """
    logger.info("Received request to list base models")
    return {"base_models": base_model_options}


# Update the log file path in the /logs endpoint
@app.get("/logs")
async def get_logs():
    """
    Get the logs of SillikaLM.

    This endpoint returns a string containing the logs of SillikaLM. The logs are split into multiple lines
    with a maximum of 180 characters per line.

    Returns:
        str: The logs of SillikaLM.

    Example Response:
        "2023-03-16 16:30:00,123 - INFO - sillikalm - Started SillikaLM\n
        2023-03-16 16:30:01,456 - INFO - sillikalm - Installed model llama3.2_SillikaLM\n
        ..."
    """

    max_chars_per_line = 180
    if os.path.exists(LOG_FILE):
        split_logs = []
        with open(LOG_FILE, "r") as log_file:
            for line in log_file:
                split_logs.extend(
                    [
                        line[i : i + max_chars_per_line]
                        for i in range(0, len(line), max_chars_per_line)
                    ]
                )
        return "\n".join(split_logs)
    else:
        return "No logs available"


@app.post("/start_webui")
async def start_webui():
    """
    Open the web UI URL in the default web browser.

    Returns:
        dict: A dictionary containing the status of the command execution.
    """
    try:
        # Open the URL in the default web browser
        webbrowser.open("http://localhost:8086", new=0)
        logger.info("Opened http://localhost:8086 in the default web browser")

        return {
            "status": "success",
            "message": "Opened http://localhost:8086 in the default web browser",
        }
    except Exception as e:
        logger.error(f"Failed to open the URL: {e}")
        return {"status": "error", "message": str(e)}

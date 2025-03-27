# SillikaLM - Krishnakanth Allika's Silly Language Models

## Overview

SillikaLM is a project I created as a fun yet meaningful exploration of language models—its name, a playful twist on "Allika's Silly Language Models." The goal is to dive into LLM technology: setting up and running models locally with Ollama, evaluating small and tiny models from Ollama and Hugging Face, integrating them into a Python-based web UI, and even developing new **SillikaLM** models for local use.

At its core, **SillikaLM** is a lightweight platform for managing and deploying language models. Built with **FastAPI**, it provides functionalities for creating, listing, and deleting models. It leverages **Ollama** for model management and **OpenWebUI** for an intuitive web-based interface, making AI experimentation more accessible and seamless.



## **SillikaLM Models and Their Personalities**


| **Model Name**              | **Personality Summary** |
|-----------------------------|-------------------------|
| **Armchair Athlete** 🏆🍕 | Yells sports strategies at the TV but hasn’t exercised since 2012. |
| **Cashanova the Banker** 💰📈 | Treats friendships like investments and emotions like stock market trends. |
| **CEO - Chief Evil Officer** 😈🏢 | Measures happiness in profit margins and fires interns for sport. |
| **Deus Exasperatus** ⚡😩 | A god who regrets creating humans and sighs more than he speaks. |
| **Dr. Nurse** 🩺🔬 | Diagnoses strangers mid-conversation and carries a defibrillator *just in case.* |
| **Kumbhakarna** 😴🍗 | Wakes up only for food and world-ending catastrophes—maybe. |
| **Miss Marshmallow** 🍭💖 | Sweet, soft, and suspiciously good at revenge. |
| **Pipelinestein** 🔬⚙️ | Automates everything, including morning coffee and breathing. |
| **PyThanos** 🧑‍💻🔮 | Snaps half of all bad code into oblivion—documentation included. |
| **Ramanujenius** 🧮🤓 | Solves equations for fun and statistically proves you're wrong. |



## Features

SillikaLM allows users to create, list, and delete SillikaLM models with ease. It supports base models from Ollama and Hugging Face, enabling flexible model selection. The platform simplifies model creation based on base model information and includes comprehensive logging for activity and error tracking. Additionally, it features a web-based interface powered by OpenWebUI for a seamless user experience.

## Installation

### Prerequisites

Ensure you have Python installed on your system. For beginners, using Anaconda to manage Python installations is recommended.

#### Windows:
1. Download Miniconda from [here](https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe) and install it.

#### macOS and Linux:
1. Follow the instructions at [Anaconda's official documentation](https://www.anaconda.com/docs/getting-started/miniconda/install).

Alternatively, you can install Python from [python.org](https://www.python.org/downloads/) if you are comfortable managing upgrades and environments.

### Running SillikaLM with `uv` (Recommended)

1. Create a new conda environment:
    ```sh
    conda create -n sillikalm uv
    ```
2. Activate the environment:
    ```sh
    conda activate sillikalm
    ```
3. Install SillikaLM:
    ```sh
    uv pip install sillikalm
    ```
4. Run SillikaLM:
    ```sh
    sillikalm
    ```

### Running SillikaLM with `pip`

1. Create a new conda environment with Python 3.11:
    ```sh
    conda create -n sillikalm python=3.11
    ```
2. Activate the environment:
    ```sh
    conda activate sillikalm
    ```
3. Install SillikaLM:
    ```sh
    pip install sillikalm
    ```
4. Run SillikaLM:
    ```sh
    sillikalm
    ```

## Web Interface

The SillikaLM web interface, powered by OpenWebUI, provides a user-friendly experience for managing language models. Key features include:

- **Model Selection**: Choose a base model from the dropdown menu to build SillikaLM models.
- **Install Models**: Install all SillikaLM models with a single click.
- **List Models**: Display a list of all installed SillikaLM models.
- **Chat**: Interact with SillikaLM models through a chat interface.
- **Delete Model**: Select and delete a specific SillikaLM model.
- **Delete all SillikaLMs**: Remove all installed SillikaLM models.
- **Shutdown**: Safely shut down the SillikaLM application.
- **Logs**: View detailed logs of model activities, including installations, deletions, and interactions.

The interface also displays model details such as name, size, parameters, quantization, and last modified date.

## License

This project is licensed under the **GNU General Public License v3 (GPLv3)**. For more details, refer to the [LICENSE](./LICENSE) file.

## Contact

For any inquiries or support, please contact Krishnakanth Allika at upside-had-matcher [at] duck [dot] com.

---

This documentation provides a comprehensive guide for end users to understand, install, and use the SillikaLM project. For further details, refer to the source code and comments within the project files.
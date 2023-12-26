# Spread Calculator API

This is a simple API that calculates the spread between two dates. It is written in Python 3.10 and uses the FastAPI framework.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Local

Python 3.10 is required to run this project. It is recommended to use a virtual environment to run this project.

```bash
# Clone the repository
git clone https://github.com/Samuelpaz95/spread_calculator.git
# Change directory
cd spread_calculator
# Create virtual environment
python3.10 -m venv venv
# Activate virtual environment
source venv/bin/activate
# Install dependencies
pip install -r requirements.txt
# Run the project
uvicorn app:app --reload
```

### Docker

This project can also be run using Docker.
docker-compose is required to run this project.
To do so, run the following commands:

```bash
# Clone the repository
git clone
# Change directory
cd spread_calculator
# Run the project
docker-compose up
```

## Usage

To use the API, you can use the Swagger UI at http://127.0.0.1:8000/docs

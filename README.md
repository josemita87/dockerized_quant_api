
# Dockerized FastAPI Project

This is a small project to demonstrate the dockerization of a FastAPI application.

## Steps Followed

### Prerequisites
Ensure Python and pip are installed on your machine.

### 1. Setup Project
```sh
cd root_directory
pip3 install poetry                       # Install poetry in your system
poetry new {project_name}                 # Initialize your project (creates pyproject.toml and other files)
```

### 2. Add Dependencies
```sh
cd {project_name}                         # Navigate to the directory where pyproject.toml is located
poetry add fastapi uvicorn yfinance black quixstreams pandas dotenv pydantic-settings  # Add dependencies to the poetry environment
```

### 3. Configure Python Interpreter
```sh
poetry env info --path                    # Get the environment path and add it to the Python interpreter (Bottom right in VSCode)
```

### 4. Connect to Redpanda
```sh
cd Docker_fast_api                         # Go to root directory
mkdir docker-compose                       # Assumes docker-compose is installed on the local machine
touch docker-compose.yml                   # Go to Redpanda's website and copy-paste the docker-compose file 
docker-compose -f docker-compose.yml up -d # Create a directory within the root directory and copy the YAML file from Redpanda's website
```

### 5. Develop API Logic
Develop the logic for the ingestion and retrieval of data through FastAPI application.

### 6. Develop Main Logic
This includes fetching data from your host API, producing Kafka topics from it, and sending them to the Redpanda cluster.

### 7. Create `config.py` and `.env` Files
To automate addresses and avoid parameter hard-coding:

```sh
cd fast_api
touch .env
```

```sh
cd fast_api/src
touch config.py
```

In `config.py`:
```python
import os
from dotenv import load_dotenv, find_dotenv  # dotenv enables us to load the strings from .env to our actual environment
from pydantic-settings import BaseSettings   # pydantic enables us to type-check config parameters before actually running the scripts

load_dotenv(find_dotenv()) 

class Settings(BaseSettings):

    kafka_broker_address: str = kafka_broker_address
    
```

In `.env`:
```env
# We define the predetermined environment variable to the port of our machine
# Beware the election of the port is made after the docker-compose file (internal and external port indications)
KAFKA_BROKER_ADDRESS=localhost:9092 
```

To handle the environment variable for Docker execution:
```sh
cd ../docker-compose
```


Finally, import `config.py` and pass this variable in `main.py` to the producer function:
```sh
cd ../fast_api/src
```

In `main.py`:
```python
from config import kafka_broker_address
```

### 8. Makefile creation

In `Makefile`, for the run command, add:

```Makefile
build:
	docker build -t quant_api .

run: 
	docker run \
	-it --network redpanda_network \
	--env KAFKA_BROKER_ADDRESS=redpanda:9092\ 
	--rm -p 8001:8001 \
	--name quant_api quant_api
```
Take note, we change the port (environment variable) to the internal one	
When run from Docker, it will automatically set the environment variable to the internal port.

### 8. Build Docker Container 
```sh
cd fast_api 
make build
```

### 9. Spin Up Docker Container
```sh
make run
```

### 10. Dockerfile optimization




#### 1. **Use `.dockerignore`**: Exclude unnecessary files from the build context.
    ```
    .git
    node_modules
    *.log
    ```


#### 2. Leverage caching

    Try to place on top those installations/directories which will be less frequently
    updated (i.e poetry add(s)). This is optimal since docker will just reinstall 
    the dependencies when they are added (not every time we spin up container.)


    (...)

### 11. Dev Tools

    1. Instead of print-debug statements, add loguru and substitute print with logger.info()
    ```sh
    cd fast_api/src
    poetry add loguru
    ```



## Docker Command-Line Flags and Their Purposes

### -f or --file
- **Usage:** Specifies a Dockerfile to use for building the image.
- **Example:** `docker build -f Dockerfile.custom .`
- **Purpose:** Allows you to specify a different Dockerfile than the default (Dockerfile) in the current directory.

### -t or --tag
- **Usage:** Tags an image with a name and optional version. It is meant for the building statement.
- **Example:** `docker build -t my-image:latest .`
- **Purpose:** Helps identify and manage images easily, using a convention like `repository:tag`.

### -p or --publish
- **Usage:** Maps a container's port to a port on the host.
- **Example:** `docker run -p 8080:80 my-image`
- **Purpose:** Exposes a specific port from the container, allowing external access to services running inside the container. Any traffic sent to `localhost:8001` on your local machine will be forwarded to port `8001` inside the container.

### -d or --detach
- **Usage:** Runs a container in detached mode (in the background).
- **Example:** `docker run -d my-image`
- **Purpose:** Allows you to run containers without blocking the terminal.

### --rm
- **Usage:** Automatically removes the container when it exits.
- **Example:** `docker run --rm my-image`
- **Purpose:** Helps keep the environment clean by removing containers that are no longer needed.

### -v or --volume
- **Usage:** Mounts a volume or directory from the host to the container.
- **Example:** `docker run -v /host/path:/container/path my-image`
- **Purpose:** Provides persistent storage and allows sharing files between the host and the container.

### -e or --env
- **Usage:** Sets environment variables inside the container.
- **Example:** `docker run -e MY_ENV_VAR=value my-image`
- **Purpose:** Configures environment-specific settings for applications running inside the container.

### --network
- **Usage:** Specifies the network for the container to connect to.
- **Example:** `docker run --network my-network my-image`
- **Purpose:** Allows you to connect the container to a specific network, facilitating communication between containers.

### --name
- **Usage:** Assigns a specific name to the container.
- **Example:** `docker run --name my-container my-image`
- **Purpose:** Allows you to easily reference and manage the container using its name instead of the automatically generated ID.

### --progress=plain
- **Usage:** Add it after build to have logs on progress (debugging tool).

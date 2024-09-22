
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
poetry add fastapi uvicorn yfinance black quixstreams pandas # Add dependencies to the poetry environment
```

### 3. Configure Python Interpreter
```sh
poetry env info --path                    # Get the environment path and add it to the Python interpreter (Bottom right in VSCode)
```

### 4. Connect to Redpanda
```sh
cd root_directory/docker-compose          # Assumes docker-compose is installed
docker-compose -f redpanda.yml up -d      # Create a directory within the root directory and copy the yaml file from Redpanda's website
```
Alternatively: Go to Redpanda's website and copy the blueprint they provide (yml file). You should place it in a folder (called docker-compose in this case) within the root directory.

### 5. Develop API Logic
Develop the logic for your FastAPI application.

### 6. Develop Main Logic
This includes fetching data from your host API, producing Kafka topics from it, and sending them to the Redpanda cluster.

### 7. Build Docker Container
If you want to run your app directly through Docker, make sure to add `name: redpanda_network` in line 4 (below `redpanda_network:`) and then change the Kafka address to `redpanda-0:9092` in main.py.

Before building the Docker container, remember to apply any changes to your code. One of the issues I faced was an incorrect Kafka address when running through Docker (because even though I would change it, I did not delete and rebuild the image with the updated scripts).

Remember to edit your Dockerfile as you wish. The most important components are installing poetry, copying the cwd, installing dependencies through poetry, and finally defining the CMD (order of execution once the container is spun up).
```sh
cd {project_name}
docker build --progress=plain -t quant_api .  # Build the Docker container. I named it quant_api
```

### 8. Spin Up Docker Container
```sh
docker run -it --network redpanda_network --rm -p 8001:8001 --name quant_api quant_api  # Run the container, remove it once finished, map local port to container port, and give it a name
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

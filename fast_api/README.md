
Small project to work on dockerization of a fast-api.


Steps followed:

0. 
                                                #We assume python and pip are installed locally in your machine

1.  $ cd root_directory
    $ pip3 install poetry                       #install poetry in your system
    $ poetry new {project_name}                 #initialize your blueprint (pyproject.toml and other files)

2.  $ cd fast_api/src                           #cd to directory where pyproject.toml is located
    $ poetry add fastapi uvicorn yfinance black #Add dependencies to the poetry environment

3.  $ poetry env info --path                    #Get the environment path and add it to the python interpreter (Bottom right in VScode)

4. Develop logic for the api 


5.  $ cd fast_api
    $ docker build --progress=plain -t quant_api .                    #Build the docker container

6. $ docker run --rm -p 8001:8001 --name quant_api quant_api   #Spin-up the container, remove it once finished, map local with container port and give it a name (first name references container, second name references image)




Docker Command-Line Flags and Their Purposes

-f or --file
    Usage: Specifies a Dockerfile to use for building the image.
    Example:
    docker build -f Dockerfile.custom .
    Purpose: Allows you to specify a different Dockerfile than the default (Dockerfile) in the current directory.

-t or --tag
    Usage: Tags an image with a name and optional version. It is meant for the building statement.
    Example:
    docker build -t my-image:latest .
    Purpose: Helps identify and manage images easily, using a convention like repository:tag.

-p or --publish
    Usage: Maps a container's port to a port on the host.
    Example:
    docker run -p 8080:80 my-image
    Purpose: Exposes a specific port from the container, allowing external access to services running inside the container.

-d or --detach
    Usage: Runs a container in detached mode (in the background).
    Example:
    docker run -d my-image
    Purpose: Allows you to run containers without blocking the terminal.

--rm
    Usage: Automatically removes the container when it exits.
    Example:
    docker run --rm my-image
    Purpose: Helps keep the environment clean by removing containers that are no longer needed.

-v or --volume
    Usage: Mounts a volume or directory from the host to the container.
    Example:
    docker run -v /host/path:/container/path my-image
    Purpose: Provides persistent storage and allows sharing files between the host and the container.

-e or --env
    Usage: Sets environment variables inside the container.
    Example:
    docker run -e MY_ENV_VAR=value my-image
    Purpose: Configures environment-specific settings for applications running inside the container.

--network
    Usage: Specifies the network for the container to connect to.
    Example:
    docker run --network my-network my-image
    Purpose: Allows you to connect the container to a specific network, facilitating communication between containers.

--name
    Usage: Assigns a specific name to the container.
    Example:
    docker run --name my-container my-image
    Purpose: This allows you to easily reference and manage the container using its name instead of the automatically generated ID.


--progress=plain
    Usage: Add it after build to have logs on progress (debugging tool)
<details>  
  <summary><strong>Table of Contents</strong></summary>  
  
  - [Introduction](#introduction)
  - [Stack](#stack)
  - [Prerequisites](#prerequisites)
  - [Architecture](#architecture)
  - [Setup](#setup)
  - [Configuration](#configuration)
  - [Useful Commands](#useful-commands)
  - [Test](#test)
</details>  



# Introduction
This project aims to discover the container concepts and tools, and practice these tools by creating a microservices architecture with docker and docker-compose.  
For more details, it happens [here](https://github.com/01-edu/public/blob/master/subjects/devops/crud-master-py/README.md)  



# Stack
- Docker  
- Docker Compose  
- PostgreSQL  
- Python  
- RabbitMQ  
- Streamlit  



# Prerequisites
**Set up Docker's apt repository**    
```
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```  

**Install the latest version**  
```
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```  

**Test if docker & docker-compose is propely installed**    
```
docker --version
docker compose version
```  



# Architecture
![Architecture](documents/architecture.png)   



# Setup  
```
git clone git@github.com:ahmedaao/manage_containers_1.git
cd manage_containers_1
docker compose up -d
```  
Then, you can go at http://localhost:8501 to access Streamlit test User Interface.  

To setup manually, it happens [here](documents/setup_manually.md)  



# Configuration
For each microservice inside the folder *services* (api-gateway-app, billing-app, etc.), a .env file must be created that matches the environment variables used in the script *main.py*.  



# Useful Commands
**Manage containers with docker-compose**  
| command                     | detail                                                                     |
|-----------------------------|----------------------------------------------------------------------------|
| `docker compose up -d`      | Run all services in background                                             |
| `docker compose up --build` | Rebuild from scratch images & Run services. Plus, display real-time logs   |
| `docker compose stop`       | Stop all services                                                          |
| `docker compose start`      | Run all services previously stopped                                        |
| `docker compose down`       | Stop & remove all containers, networks & images created with 'up'          |
| `docker compose down -v`    | Stop & remove all containers, networks, images & volumes created with 'up' |
| `docker compose ps`         | Check status of all services                                               |

**Manage containers manually one by one**  
| command                                           | detail                            |
|---------------------------------------------------|-----------------------------------|
| `sudo docker images`                              | List all container images         |
| `sudo docker ps -a`                               | List all container running or not |
| `sudo docker stop <container_id>`                 | Stop a running container with id  |
| `sudo docker rm <container_id>`                   | Destroy container to restart it   |
| `sudo docker run -it <image_name>:<version> bash` | Run container & go inside         |



# Test
**Add data into inventory-db manually**  
```
curl -X POST \
  http://localhost:3000/api/movies \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "aquaman",
  "description": "aquaman is a good movie"
}'
```  

**Add data into billing-db manually**  
```
curl -X 'POST' \
  'http://localhost:3000/api/billing' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": "20",
  "number_of_items": "99",
  "total_amount": "250"
}'
```  

<details>  
  <summary><strong>Table of Contents</strong></summary>  
  
  - [Introduction](#introduction)
  - [Prerequisites](#prerequisites)
  - [Architecture](#architecture)
  - [Commands](#commands)
  - [Setup](#setup)
    - [Network](#network)
    - [Inventory-db](#inventory-db)
    - [Inventory-app](#inventory-app)
    - [Billing-db](#billing-db)
    - [Billing-app](#billing-app)
    - [RabbitMQ](#rabbitmq)
    - [Api-gateway-app](#api-gateway-app)
  - [Test](#test)
</details>  



# Introduction
This project aims to discover the container concepts and tools, and practice these tools by creating a microservices architecture with docker and docker-compose.  
For more details, it happens [here](https://github.com/01-edu/public/blob/master/subjects/devops/crud-master-py/README.md)  



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
![Architecture](diagram.png)   



# Commands
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



# Setup
## Network
```
docker network create my-network  
```  

## Inventory-db
```
docker volume create inventory-db  
docker build -t inventory-db:v1 .  
docker run -d --name inventory-db --network my-network --env-file .env -v inventory-db:/var/lib/postgresql/data inventory-db:v1  
```  

## Inventory-app
```
docker build -t inventory-app:v1 .  
docker run -d --name inventory-app --network my-network --env-file .env inventory-app:v1  
```  

## Billing-db
```
docker volume create billing-db  
docker build -t billing-db:v1 .  
docker run -d --name billing-db --network my-network --env-file .env -v billing-db:/var/lib/postgresql/data billing-db:v1  
```  

## Billing-app
```
docker build -t billing-app:v1 .  
docker run -d --name billing-app --network my-network --env-file .env billing-app:v1  
```  

## RabbitMQ
```
docker build -t rabbitmq:v1 .  
docker run -d --name rabbitmq --network my-network --env-file .env rabbitmq:v1  
```  

## Api-gateway-app
```
docker volume create api-gateway-app  
docker build -t api-gateway-app:v1 .  
docker run -d --name api-gateway-app --network my-network --env-file .env -p 3000:3000 -v api-gateway-app:/var/lib/api/data api-gateway-app:v1  
```  



# Test
**Add data into inventory-db**  
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

**Add data into billing-db**  
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

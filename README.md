<details>  
  <summary><strong>Table of Contents</strong></summary>  
  
  - [Prerequisites](#prerequisites)
  - [Commands](#commands)
  - [Container](#container)
    - [Listing](#listing)
    - [Inventory-db](#inventory-db)
    - [Inventory-app](#inventory-app)
    - [Billing-db](#billing-db)
</details>  



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



# Commands
**Manage containers with docker-compose**  
| command | detail     |
|---------|------------|
|||

**Manage containers manually one by one**  
| command                                           | detail                            |
|---------------------------------------------------|-----------------------------------|
| `sudo docker images`                              | List all container images         |
| `sudo docker ps -a`                               | List all container running or not |
| `sudo docker stop <container_id>`                 | Stop a running container with id  |
| `sudo docker rm <container_id>`                   | Destroy container to restart it   |
| `sudo docker run -it <image_name>:<version> bash` | Run container & go inside         |



# Container
## Listing
| name         | volume       ||||
|--------------|--------------||
| inventory-db | inventory-db ||||
|||||


## Inventory-db

**Build container image**  
```
sudo docker build -t inventory-db:v1 .
```  

**Volume creation**  
```
sudo docker volume create inventory-db
```  

**Run the container**  
```
sudo docker run -d \
  --name inventory-db \
  --env-file .env \
  -p 5432:5432 \
  -v inventory-db:/var/lib/postgresql/data \
  inventory-db:v1
```  

**Add/Delete manually element into database PostgreSQL**  
```
sudo docker exec -it inventory-db psql -U hao -d inventory-db
```  

```
INSERT INTO inventory (id, title, description) VALUES (1, 'batman', 'batman is a good movie');
SELECT * FROM inventory;
```  


## Inventory-app

**Build container image**  
```
sudo docker build -t inventory-app:v1 .
```  

**Run the container**  
```
docker run -d --name inventory-app --network host-network --env-file .env -p 8080:8080 inventory-app:v1
```  

**Test the API with FastAPI Swagger**  
```
http://localhost:8080/docs
```  


## Billing-db

**Build container image**  
```
sudo docker build -t billing-db:v1 .
```  

**Volume creation**  
```
sudo docker volume create billing-db
```  

**Run the container**  
```
docker run -d \
  --name billing-db \
  --env-file .env \
  -p 5433:5433 \
  -v billing-db:/var/lib/postgresql/data \
  billing-db:v1
```  









new test:

# Network
docker network create my-network

# Inventory-db
docker volume create inventory-db
docker build -t inventory-db:v1 .
docker run -d --name inventory-db --network my-network --env-file .env -v inventory-db:/var/lib/postgresql/data inventory-db:v1

# Inventory-app
docker build -t inventory-app:v1 .
docker run -d --name inventory-app --network my-network --env-file .env -p 8080:8080 inventory-app:v1

# Billing-db
docker volume create billing-db
docker build -t billing-db:v1 .
docker run -d --name billing-db --network my-network --env-file .env -v billing-db:/var/lib/postgresql/data billing-db:v1

# Billing-app
docker build -t billing-app:v1 .
docker run -d --name billing-app --network my-network --env-file .env billing-app:v1

# RabbitMQ
docker build -t rabbitmq:v1 .
docker run -d --name rabbitmq --network my-network --env-file .env -p 15672:15672 rabbitmq:v1
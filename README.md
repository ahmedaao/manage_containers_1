<details>  
  <summary><strong>Table of Contents</strong></summary>  
  
  - [Prerequisites](#prerequisites)
  - [Commands](#commands)
  - [Container](#container)
    - [Listing](#listing)
    - [Inventory-db](#inventory-db)
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
sudo build -t inventory-db .
```  

**Volume creation**  
```
sudo docker volume create inventory-db
```  

**Run the container**  
```
docker run -d \
  --name inventory-db \
  --env-file .env \
  -p 5432:5432 \
  -v inventory-db:/var/lib/postgresql/data \
  inventory-db:v1
```  

**Add/Delete element into database PostgreSQL**  
```
sudo docker exec -it inventory-db psql -U hao -d inventory-db
```  

```
INSERT INTO inventory (title, description)
VALUES ('title_1', 'description_1')

SELECT * FROM inventory
```  
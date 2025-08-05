Here are all setup steps:  
  
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

## Frontend-app
```
docker build -t frontend-app:v1 .  
docker run -d --name frontend-app --network my-network --env-file .env -p 8051:8051 frontend-app:v1  
```

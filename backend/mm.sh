# Stop and remove all containers
docker stop $(docker ps -q)
docker rm $(docker ps -aq)

# Restart Docker Compose
docker-compose down
docker-compose up --build

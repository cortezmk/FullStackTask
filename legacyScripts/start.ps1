#docker pull mongo:4.0.4
#docker run -d -p 27017-27019:27017-27019 --name mongodb mongo:4.0.4
$mongoIp = docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mongodb

cd ./calculation
docker build -t volue-calculation:latest .
cd ..
docker run -d -p 5001:5001 --name volue-calculation-container volue-calculation
$calculationIp = docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' volue-calculation-container

cd ./api
docker build -t volue-api:latest .
cd ..
docker run -d -p 5000:5000 --name volue-api-container --env MONGO_IP=$mongoIp --env CALCULATION_IP=$calculationIp volue-api

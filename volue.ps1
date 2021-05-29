param(
    [Parameter(Position=0,Mandatory=$true)]
    [ValidateSet('build', 'setup', 'run', 'stop')]
    [System.String]
    $command
)

switch($command) {
    'build' {
        cd ./calculation
        docker build -t volue-calculation:latest .
        cd ..
        cd ./api
        docker build -t volue-api:latest .
        cd ..
    }
    'setup' {
        docker pull mongo:4.0.4
        docker run -d -p 27017-27019:27017-27019 --name mongodb mongo:4.0.4
    }
    'run' {
        $mongoIp = docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mongodb
        docker run -d -p 5001:5001 --name volue-calculation-container volue-calculation
        $calculationIp = docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' volue-calculation-container
        docker run -d -p 5000:5000 --name volue-api-container --env MONGO_IP=$mongoIp --env CALCULATION_IP=$calculationIp volue-api
    }
    'stop' {
        docker kill volue-api-container
        docker rm volue-api-container
        docker kill volue-calculation-container
        docker rm volue-calculation-container
    }
}
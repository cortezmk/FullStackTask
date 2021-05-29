# Instructions

After project is cloned please use attached PS file.

to setup database:

```
./volue setup
```
to build images:
```
./volue build
```
and to run project:
```
./volue run
```
Once project is running service can be found here:
```
http://0.0.0.0:5000/apidocs/
```
to stop running services:
```
./volue stop
```
# TODOs
* add index on Mongo collection to improve performance
* add SSL on API endpoint
* improve performance on Calculation service (make session request? run calculations in parallel?)
* add volume for Mongo container? - I didn't include it in current version - didn't want to leave a mess on host machine :)
* perhaps move to docker compose - it wasn't specified whether it's allowed

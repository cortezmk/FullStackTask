from flask import Flask, request
from pymongo import MongoClient
import os
import requests
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

@app.route("/health")
def health():
    """Endpoint for checking if service is ready to use.
    ---
    responses:
      200:
        description: service is ready
    """
    return "ready", 200

def get_client():
    client = MongoClient('mongodb://' + os.environ.get('MONGO_IP') + ':27017/')
    return client

@app.route("/api/add", methods = ['POST'])
def add_points():
    """Adds new dataPoints to DB
    ---
    parameters:
        -   name: value
            in: body
            required: true
            description: dataPoint definitions to insert
            schema:
                $ref: '#/definitions/DataPoints'
    definitions:
        DataPoints:
            type: array
            items:
                $ref: '#/definitions/DataPoint'
        DataPoint:
            type: object
            properties:
                name:
                    type: string
                    description: name as this dataPoint can be selected by
                v:
                    type: number
                    description: value of dataPoint
                t:
                    type: number
                    description: timestamp as epoch
    responses:
        201:
            description: DataPoints sucessfully added
    """
    client = get_client()
    client['volue'].dataPoints.insert_many(request.json)
    client.close()
    return "ok", 201

@app.route("/api/<name>", methods = ['GET'])
def get_points(name):
    """Gets statistics from selected dataPoints.
    ---
    parameters:
        -   name: name
            in: path
            type: string
            required: true
            description: name of dataPoints to select
        -   name: from
            in: query
            type: number
            required: false
            description: min value of timestamp to select
        -   name: to
            in: query
            type: number
            required: false
            description: max value of timestamp to select
    definitions:
        Response:
            type: object
            properties:
                avg:
                    type: number
                sum:
                    type: number
    responses:
        200:
            description: Calculated stats
            schema:
                $ref: '#/definitions/Response'
            examples:
                {"sum":7.0,"avg":2.25}
    """
    filter = { "name": name }
    time = None
    if 'from' in request.args or 'to' in request.args:
        time = {}
        if 'from' in request.args:
            time['$gte'] = int(request.args.get('from'))
        if 'to' in request.args:
            time['$lte'] = int(request.args.get('to'))
    if time != None:
        filter['t'] = time
    client = get_client()
    data = []
    for d in client['volue'].dataPoints.find(filter, {'_id': -1, 'v': 1}):
        data.append(float(d['v']))
    client.close()
    result = requests.post('http://' + os.environ.get('CALCULATION_IP') + ':5001/api/calculation', json = { 'input': data })
    return result.json(), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True,host='0.0.0.0',port=port)

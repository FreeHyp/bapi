from vm import VM
from config import *
from flask import Flask, jsonify, request
from flask_restful import reqparse, Resource, Api
from functools import wraps
from os.path import isfile
from os import listdir
from time import sleep
import json

app = Flask(__name__)
api = Api(app)

def load_vm(f):
    @wraps(f)
    def wrapper(vm_name, *args, **kwargs):
        return f(VM(vm_name))

    return wrapper


@app.route('/')
def root():
    return 'bapi root'

@app.route('/vm/', methods=['GET', 'POST'])
def vms_ep():
    """ """
    if request.method == 'POST':
        myvm = VM(request.json)
        myvm.save()
        return jsonify({"status": myvm.status()}), 200 
    elif request.method == 'GET':
        return jsonify(
                {'vms': listdir(VM_DIR)}
               ), 200

@app.route('/vm/<vm_name>', methods=['DELETE', 'GET', 'PATCH', 'POST'])
@load_vm
def vm_ep(vm):
    if request.method == 'GET':
        return jsonify({"state": vm.status()}), 200
    elif request.method == 'PATCH':
        for key, value in request.json.items():
            setattr(vm,key,value)
        vm.save()
        return jsonify({'action': 'vm modified'}) 
    elif request.method == 'POST':
        if request.json['action']: 
            if request.json['action'] == 'start':
                vm.start()
                # needs a little time for the process to spin up
                sleep(1)
                return jsonify({"state": vm.status()}), 200
            elif request.json['action'] == 'stop':
                vm.stop()
                return jsonify({"state": vm.status()}), 200
            elif request.json['action'] == 'restart':
                vm.restart()
                sleep(1)
                return jsonify({"state": vm.status()}), 200

    elif request.method == 'DELETE':
        vm.delete()
        return 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

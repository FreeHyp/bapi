from flask import Flask
from flask_restful import reqparse, Resource, Api
from os.path import isfile

app = Flask(__name__)
api = Api(app)

class VmList(Resource):
    def post(self):
        vm = parser.parse_args()
        vm_name = vm['name']
        if vm_exists(vm_name):
            return {'error': 'VM exists %s' % vm_name }, 409
        else:
            write_vm_config(vm_name, vm)
            return "%s/%s" % (CONF_PATH, vm_name), 201


api.add_resource(VM, '/vm/<vm_name>')
api.add_resource(VmList, '/vm')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

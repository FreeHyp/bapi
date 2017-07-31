import custom_t
import yaml
from enum import Enum
from flask import Flask
from flask_restful import reqparse, Resource, Api
from os.path import isfile

CONF_PATH='/tmp'

app = Flask(__name__)
api = Api(app)

class Nic():
    def __init__(self, bridge, driver, mac='auto'):
        if driver not in custom_t.NIC_TYPES:
            raise TypeError('Invalid driver %s' % driver)
        self.mac    = mac
        self.bridge = bridge
        self.driver = driver
    def dump(self):
        rtrn = {}
        for v in vars(self):
            rtrn[v] = vars(self)[v]
        return rtrn


    def __repr__(self):
        return '<virtual %s nic attached to %s mac: %s>' % (self.driver, self.bridge, self.mac)

class Disk():
    def __init__(self, path, driver):
        if driver not in custom_t.DISK_TYPES:
            raise TypeError('Invalid driver %s' % driver)
        self.path = path
        self.driver = driver

    def dump(self):
        rtrn = {}
        for v in vars(self):
            rtrn[v] = vars(self)[v]
        return rtrn
    
    def __repr__(self):
        return '<virtual %s disk attached to %s>' % (self.driver, self.path)

class VM(Resource):
    def __init__(self, vm_name):
        self.auto_start = False
        self.disk = [] 
        self.iso = ''
        self.memory = 1024 
        self.name = ''
        self.ncpus = 1
        self.network = []

        if isfile('%s/%s' % (CONF_PATH, vm_name)):
            self.load_from_file('%s/%s' % (CONF_PATH, something))
        elif isinstance(something, dict):
            self.load_from_dict(something)
        else:
            raise

    def load_from_file(self, fpath):
        with open(fpath) as f:
            fconf = yaml.load(f.read())
        self.load_from_dict(fconf)

    def load_from_dict(self, d):
        for key, value in d.iteritems():
            if key == 'network':
                for v in value:
                    self.network.append(
                        Nic(
                            v['bridge'],
                            v['driver'],
                            mac=v['mac'],
                        )
                    )
            elif key == 'disk':
                for v in value:
                    self.disk.append(
                        Disk(
                            v['path'],
                            v['driver'],
                        )
                    )
            else:
                exec("self.%s = '%s'" % (key, value))
    
    def dump_to_dict(self):
        rtrn = {}
        for key in vars(self):
            if key == 'disk' or key == 'network':
                rtrn[key] = []
                for item in vars(self)[key]:
                    rtrn[key].append(item.dump())
                    print 'dump %s' % item 
            else:
                rtrn[key] = getattr(self, key)
        return rtrn

    def dump_to_file(self, fpath):
        d = self.dump_to_dict()
        with open(fpath, 'w') as f:
            f.write(yaml.dump(d))
        return True

    def __repr__(self):
        print "< VM: %s >" % self.name
        for v in vars(self):
            if v == 'name':
                True
            elif v == 'network' or v == 'disk':
                print "  <%s: %s>" % (v, getattr(self, v))
            else:
                print "  <%s: %s>" % (v, vars(self)[v])
    def get(self, vm_name):
        load_from_file(vm_name)
        return yaml.dump(self.dump_to_dict()), 200
        



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

from disk import Disk
from nic import Nic
from os.path import isfile
from utils import shell
import subprocess
import yaml

CONF_PATH='/tmp'

class VM:
    def __init__(self, vm_name):
        self.auto_start = False
        self.bootrom = '/usr/local/share/uefi-firmware/BHYVE_UEFI.fd'
        self.com1 = 'stdio'
        self.com2 = None 
        self.disk = [] 
        self.iso = None 
        self.memory = 1024 
        self.name = ''
        self.ncpus = 1
        self.network = []

        if isfile('%s/%s' % (CONF_PATH, vm_name)):
            self.load_from_file('%s/%s' % (CONF_PATH, vm_name))
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

    def start(self):
        pcistr = ''
        lpcistr = ''
        # Start with 1, because the hostbridge is 0
        i=1

        # Add all of the nics
        for nic in self.network:
            pcistr += ' %s' % nic.start(i)
            i = i + 1

        # Add all of the disks
        for disk in self.disk:
            pcistr += ' %s' % disk.start(i)
            i = i + 1

        if self.iso != 'None':
            pcistr += '-s %s,ahci-cd,%s' % (i, self.iso)
            i = i + 1

        pcistr += ' -s %s,fbuf,tcp=0.0.0.0:5900 ' % i
        i = i + 1

        # PCI Bridge devices
        if self.com1 is not None: 
            lpcistr += '-l %s,%s ' % ('com1', self.com1)
        if self.com2 is not None: 
            lpcistr += '-l %s,%s ' % ('com2', self.com2)

        if self.bootrom is not None:
            lpcistr += '-l bootrom,%s' % self.bootrom

        cmd = """/usr/sbin/bhyve -c %s -m %sM -A -H -w -s 0,hostbridge -s 31,lpc %s %s %s""" % (self.ncpus, self.memory, pcistr, lpcistr, self.name)
        print cmd
        p = shell(cmd)

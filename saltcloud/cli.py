'''
Primary interfaces for the salt-cloud system
'''
# Need to get data from 4 sources!
# CLI options
# salt cloud config - /etc/salt/cloud
# salt master config (for master integration)
# salt vm config, where vms are defined - /etc/salt/cloud.vm
#
# The cli, master and cloud configs will merge for opts
# the vm data will be in opts['vm']
# Import python libs
import optparse
import os

# Import salt libs
import saltcloud.config

class SaltCloud(object):
    '''
    Create a cli SaltCloud object
    '''
    def __init__(self):
        self.opts = self.parse()

    def parse(self):
        '''
        Parse the command line and merge the config
        '''
        cli = self._parse_cli()
        cloud = saltcloud.config.cloud(cli['cloud_config'])
        opts = saltcloud.config.master(cli['master_config'])
        vms = saltcloud.config.vms(cli['vm_config'])
        opts.update(cloud)
        opts.update(cli)
        opts['vm'] = vms


    def _parse_cli(self):
        '''
        Parse the cli and return a dict of the options
        '''
        parser = optparse.OptionParser()

        parser.add_option('-C',
                '--cloud-config',
                dest='cloud_config',
                default='/etc/salt/cloud',
                help='The location of the saltcloud config file')
        parser.add_option('-M',
                '--master-config',
                dest='vm_config',
                default='/etc/salt/master',
                help='The location of the salt master config file')
        parser.add_option('-V',
                '--vm-config',
                dest='vm_config',
                default='/etc/salt/cloud.vm',
                help='The location of the saltcloud vm config file')

        options, args = parser.parse_args()

        cli = {}

        for k, v in options.__dict__.items():
            if v is not None:
                cli[k] = v
        return cli


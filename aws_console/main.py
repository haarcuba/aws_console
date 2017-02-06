import IPython
import IPython.terminal.embed
import sys
import time
import os
import boto3
import subprocess
import logging
import re
import argparse
import aws_console.embed

def say( message ):
    sys.stderr.write( '{0}\n'.format( message ) )

def western( region ):
    return region.startswith( 'us' ) or region.startswith( 'eu' ) or region.startswith( 'ca' )

REGIONS = [ 'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2', 'ca-central-1', 'eu-west-1', 'eu-central-1', 'eu-west-2', 'ap-northeast-1', 'ap-northeast-2', 'ap-southeast-1', 'ap-southeast-2', 'ap-south-1', 'sa-east-1', ]
WESTERN = [ region for region in REGIONS if western( region ) ]
parser = argparse.ArgumentParser()
parser.add_argument( 'region', choices = REGIONS )
parser.add_argument( '--profile', default = 'default' )
arguments = parser.parse_args()

logging.basicConfig( level = logging.WARNING, format = '%(asctime)s %(levelname)s: %(message)s' )
session = boto3.Session(profile_name=arguments.profile, region_name=arguments.region)
ec2 = session.resource('ec2')

def by_tag_values(pattern):
    pattern = re.compile(pattern)
    result = []
    for machine in ec2.instances.all():
        if not machine.tags:
            continue
        for tag in machine.tags:
            match = pattern.search(tag['Value'])
            if match is not None:
                result.append(machine)

    return result


def ssh(user, instance, keyfile=None):
    BASIC = ['ssh', '-l', user, '-X']
    if keyfile:
        KEY = ['-i', keyfile]
    else:
        KEY = []
    instance.reload()
    p = subprocess.Popen(BASIC + KEY + [instance.public_dns_name])
    p.wait()

def pollState( thing ):
    state = thing.state
    say( 'current state is {0}'.format( state ) )
    thing.reload()
    while thing.state == state:
        time.sleep(1)
        thing.reload()
        print(".", end='', flush=True)

    say( 'current state is {0}'.format( state ) )
    return thing.state

def start( instance ):
    instance.start()
    instance.wait_until_running()

def stop( instance ):
    instance.stop()
    instance.wait_until_stopped()

def ping(instance):
    os.system('ping {0}'.format(instance.public_dns_name))

def main():
    ipshell = IPython.terminal.embed.InteractiveShellEmbed(
        config=aws_console.embed.config,
        banner1 = BANNER,
        exit_msg = "Bye bye, I hope you didn't destroy everything.")
    ipshell()


BANNER =\
"""
***********************************************
*                                             *
*       Welcome to the AWS BOTO console       *
*                                             *
***********************************************
"""

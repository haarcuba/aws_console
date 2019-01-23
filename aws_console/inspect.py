"""
aws-inspect

will run "aws command subcommand subcommand..." and then inspect the results in an interactive prompt
"""
import json
import argparse
import myconsole
import subprocess

_aws = 'aws'

def _run( command ):
    command = [ _aws ] + command
    process = subprocess.run( command, stdout = subprocess.PIPE, text = True )
    return json.loads( process.stdout )

def aws( commandString ):
    return _run( commandString.split() )

def main():
    global _aws
    parser = argparse.ArgumentParser(description = __doc__, usage='aws command subcommand subcommand...')
    parser.add_argument( '--main-command', '-m', metavar='STRING', dest='mainCommand', default='aws', help='use this instead of "aws", essentialy, you can consume other JSON services this way' )
    arguments, command = parser.parse_known_args()
    _aws = arguments.mainCommand
    if len( command ) == 0:
        return
    if command[ -1 ] == 'help':
        subprocess.run( [ 'aws' ] + command )
        return
    r = _run( command )
    console = myconsole.create( BANNER, 'aws-inspect', 'out', exitMessage = "Bye bye, I hope you didn't destroy everything." )
    console()

BANNER =\
"""
***********************************************
*                                             *
*       Welcome to the AWS INSPECT console    *
*                                             *
*       type 'exit' to quit                   *
*                                             *
***********************************************
"""

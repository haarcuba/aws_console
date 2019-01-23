"""
aws-inspect command subcommand subcommand...

will run aws command subcommand subcommand... and then inspect the results in an interactive prompt
"""
import json
import argparse
import myconsole
import subprocess

def _run( command ):
    if len( command ) == 0:
        return {}
    command = [ 'aws' ] + command
    process = subprocess.run( command, stdout = subprocess.PIPE, text = True )
    return json.loads( process.stdout )

def aws( commandString ):
    return _run( commandString.split() )

def main():
    parser = argparse.ArgumentParser(description = __doc__)
    arguments = parser.parse_known_args()
    results = _run( arguments[ -1 ] )
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

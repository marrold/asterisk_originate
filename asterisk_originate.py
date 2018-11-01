#!/usr/bin/env python3

from asterisk_originate import asterisk_originate
import sys
import getopt

def main():

    options = """
asterisk_originate will generate calls and drop them into a context. It does so by interacting with the Asterisk AMI.

Usage:
./asterisk_originate.py -H [AMI Host] -p [AMI Port] -u [AMI User] -P [AMI Password] -C [Channel] -c [Context] -I [Caller ID] -E [Extension in Context] -r [priority]

Arguments:
-h / --help - Display help
-H / --host [AMI Host] - AMI IP
-p / --port [AMI Port] - AMI Port
-u / --username [AMI Username] - AMI Username
-P / --password [AMI Password] - AMI Password
-C / --channels [Channels] - Channels to ring. Excepts one channel "SIP/6000" or a group "SIP/6000&SIP/6001"
-c / --context [Context] - Context to drop channels into once they answer
-I / --callerid [Callerid] - Caller ID to display when ringing channels
-E / --extension [Extension] - Extension in context
-r / --priority [Priority] - Priority in context
    """

    # Init vars
    ami_host = None
    ami_port = None
    ami_username = None
    ami_password = None
    channels = None
    context = None
    callerid = None
    extensions = None
    priority = None

    # Get arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hH:p:u:P:C:c:I:E:r:",
                                   ["help", "host=", "port=", "username=", "password=", "channels=",
                                    "context=", "callerid=", "extension=", "priority="])

    except getopt.GetoptError as err:
        print("Unable to parse arguments: %s" % err)
        print(options)
        sys.exit(1)


    # Parse Arguments
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print(options)
            sys.exit(0)
        elif opt in ("-H", "--host"):
            ami_host = arg
        elif opt in ("-p", "--port"):
            ami_port = arg
        elif opt in ("-u", "--username"):
            ami_username = arg
        elif opt in ("-P", "--password"):
            ami_password = arg
        elif opt in ("-C", "--channels"):
            channels = arg
        elif opt in ("-c", "--context"):
            context = arg
        elif opt in ("-I", "--callerid"):
            callerid = arg
        elif opt in ("-E", "--extension"):
            extensions = arg
        elif opt in ("-r", "--priority"):
            priority = arg

    # Check vars are populated
    if None not in (ami_host, ami_port, ami_username, ami_password, channels, context, callerid, extensions, priority):

        # Init the class
        originate = asterisk_originate.asterisk_originate(ami_host, ami_port, ami_username, ami_password)

        # Try to originate the calls
        if originate.originate(channels, extensions, priority, context, callerid):
            sys.exit(0)
        else:
            sys.exit(1)


    else:
        print("Unable to parse arguments")
        print(options)
        sys.exit(1)

if __name__ == "__main__":
    main()

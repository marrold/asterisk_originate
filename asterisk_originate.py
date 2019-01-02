#!/usr/bin/env python3

from asterisk_originate import asterisk_originate
import sys
import getopt


def main():
    options = """
asterisk_originate will generate calls and drop them into a context or application. It does so by interacting with the Asterisk AMI.

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
-a / --application [Application] - Application to run
-d / --data [Data] - Data to pass to application
-t / --timeout [Timeout] - Timeout when originating to context
-v / --variables [Variables] - Variables to pass to context
    """

    # Init vars
    ami_host = None
    ami_port = None
    ami_username = None
    ami_password = None
    channels = None
    context = None
    callerid = None
    extension = None
    priority = None
    application = None
    data = None
    timeout = 60
    variables = ""

    # Get arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hH:p:u:P:C:c:I:E:r:a:d:t:v:",
                                   ["help", "host=", "port=", "username=", "password=", "channels=",
                                    "context=", "callerid=", "extension=", "priority=", "application=", "data=",
                                    "timeout=", "variables="])

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
            extension = arg
        elif opt in ("-r", "--priority"):
            priority = arg
        elif opt in ("-a", "--application"):
            application = arg
        elif opt in ("-d", "--data"):
            data = arg
        elif opt in ("-t", "--timeout"):
            timeout = arg
        elif opt in ("-v", "--variables"):
            variables = arg

    # You can only originate to a context OR an application.
    if context and application:
        print("Please select either context or application")
        print(options)
        sys.exit(1)

    if None not in (ami_host, ami_port, ami_username, ami_password):

        # Init the class
        originate = asterisk_originate.asterisk_originate(ami_host, ami_port, ami_username, ami_password)

    else:
        print("Please supply AMI Parameters")
        print(options)
        sys.exit(1)

    # Check if we're originating to a context, and the appropriate vars are populated
    if context and None not in (channels, callerid, extension, priority):

        # Try to originate the calls
        try:
            originate.originate_context(channels, context, extension, priority, callerid, timeout, variables)
            sys.exit(0)

        except asterisk_originate.MissingParams:
            print("Failed to parse context parameters")
            sys.exit(1)

    # Check if we're originating to an application, and the appropriate vars are populated
    elif application and None not in (channels, callerid):

        # Try to originate the calls
        try:
            originate.originate_application(channels, application, data, callerid)

        except asterisk_originate.MissingParams:
            print("Failed to parse application parameters")
            sys.exit(1)

    else:
        print("Unable to parse arguments")
        print(options)
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import errno
from asterisk.ami import SimpleAction, AMIClient

class asterisk_originate:
    def __init__(self, ami_host, ami_port, ami_username, ami_password):

        self.__ami_host = ami_host
        self.__ami_port = int(ami_port)
        self.___ami_username = ami_username
        self.__ami_password = ami_password

        self.__ami_client = AMIClient(address=self.__ami_host, port=self.__ami_port)

    def _login(self):

        self.__ami_client = AMIClient(address=self.__ami_host, port=self.__ami_port)

        try:
            self.__ami_client.login(
                username=self.___ami_username, secret=self.__ami_password)
            print("Successfully logged into AMI")
            return True

        except Exception as e:

            error = self._handle_ami_exception(e)
            print("Unable to login to AMI: %s" % error)
            return False

    def _logoff(self):

        try:
            self.__ami_client.logoff()
            return True

        except Exception as e:

            error = self._handle_ami_exception(e)
            print("Unable to logoff from AMI: %s" % error)
            return False

    def _handle_ami_exception(self, exception):

        try:
            if exception.errno == errno.ECONNREFUSED:
                return("Unable to connect to AMI (Connection Refused)")

            elif exception.errno == errno.EPIPE:
                return("No longer connected to AMI (Broken Pipe)")

            elif exception.errno == errno.EBADF:
                return("No longer connected to AMI (Bad File Descriptor)")

            else:
                return(exception)

        except Exception as e:
            return(e)

    def _send_originate(self, channel, extension, priority, context, callerid):

        action = SimpleAction(
            'Originate',
            Channel=channel,
            Exten=extension,
            Priority=priority,
            Context=context,
            CallerID=callerid, )

        try:
            self.__ami_client.send_action(action)
            return True

        except Exception as e:
            error = self._handle_ami_exception(e)
            print("Unable to connect to %s: %s" % (channel, error))
            return False

    def originate(self, channel, extensions, priority, context, callerid):

        split_extensions = extensions.split("&")

        if None not in (channel, extensions, priority, context, callerid):

            if self._login():

                for extension in split_extensions:

                    self._send_originate(channel, extension, priority, context, callerid)

                if self._logoff():

                    return True

                else:
                    return False

        else:
            return False

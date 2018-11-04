#!/usr/bin/env python3

import errno
from asterisk.ami import SimpleAction, AMIClient

class MissingParams(Exception):
    pass

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

    def _send_originate_context(self, channel, context, extension, priority, callerid, timeout=60, variables=""):

        action = SimpleAction(
            'Originate',
            Channel=channel,
            Exten=extension,
            Priority=priority,
            Context=context,
            CallerID=callerid,
            Timeout=timeout*1000,
            Variable=variables)

        try:
            self.__ami_client.send_action(action)
            return True

        except Exception as e:
            error = self._handle_ami_exception(e)
            print("Unable to connect to %s: %s" % (channel, error))
            return False

    def _send_originate_application(self, channel, application, data, callerid):

        action = SimpleAction(
            'Originate',
            Channel=channel,
            CallerID=callerid,
            Application=application,
            Data=data, )

        try:
            self.__ami_client.send_action(action)
            return True

        except Exception as e:
            error = self._handle_ami_exception(e)
            print("Unable to connect to %s: %s" % (channel, error))
            return False

    def originate_context(self, channels, context, extension, priority, callerid, timeout=60, variables=""):

        split_channels = channels.split("&")

        if None not in (channels, extension, priority, context, callerid):

            if self._login():

                for channel in split_channels:

                    self._send_originate_context(channel, context, extension, priority, callerid, timeout, variables)

                if self._logoff():

                    return True

                else:
                    return False

        else:
            raise MissingParams("Failed to parse application parameters")

    def originate_application(self, channels, application, data, callerid):

        split_channels = channels.split("&")

        if None not in (channels, application, data, callerid):

            if self._login():

                for channel in split_channels:

                    self._send_originate_application(channel, application, data, callerid)

                if self._logoff():

                    return True

                else:
                    return False

        else:
            raise MissingParams("Failed to parse originate parameters")

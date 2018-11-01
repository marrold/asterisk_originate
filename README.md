## Introduction

asterisk_originate is a tool to generate calls via the Asterisk AMI interface and drop them into a specific context.

## Caveats

* asterisk_originate is designed for python 3 only!
* To date, this has only been tested on a Debian 9 based, Asterisk 13 system

## Quick Install

Change to root:

    sudo su

#### Clone the repo

    cd /opt/
    git clone https://github.com/marrold/asterisk_originate.git

#### Install required dependancies

Change into the directory:

    cd asterisk_originate

Install requirements:

    pip3 install -r requirements.txt

## Usage

All arguments are mandatory:

    ./asterisk_originate.py -H [AMI Host] -p [AMI Port] -u [AMI User] -P [AMI Password] -C [Channel] -c [Context] -I [Caller ID] -E [Extension in Context] -r [priority]

## Example

    ./asterisk_originate.py -H 127.0.0.1 -p 5038 -u admin -P password -C "SIP/100" -c from-originate -I "Originate" -E s -r 1

## Licence

This project is licensed under the [Creative Commons CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) licence.

You are free to share and adapt the code as required, however you *must* give appropriate credit and indicate what changes have been made. You must also distribute your adaptation under the same license. Commercial use is prohibited.

## Acknowledgments

Thanks to everyone who contributed to the various modules utilised within this project.
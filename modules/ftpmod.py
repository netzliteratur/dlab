#-*- coding:utf-8 -*-
import sys
import os
import ConfigParser
import paramiko


def read_config():
    """
    read bag.cfg file
    :return string server_, port_, user_, passwd_, dir_:
    """
    config = ConfigParser.RawConfigParser()
    config.read("config/bag.cfg")

    server_ = config.get("SFTP", "Server")
    port_ = config.get("SFTP", "Port")
    user_ = config.get("SFTP", "User")
    passwd_ = config.get("SFTP", "Password")
    dir_ = config.get("SFTP", "Directory")

    return server_, port_, user_, passwd_, dir_


def send_bag(server_, port_, user_, passwd_, bag_file_, dir_):
    """
    put bag via sftp
    :return int 0:
    """
    transport = paramiko.Transport((server_, int(port_)))
    transport.connect(username=user_, password=passwd_)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put(bag_file_, dir_ + os.path.basename(bag_file_))
    sftp.close()

    return 0


def main():
    """
    empty doc string
    """
    bag_file_ = sys.argv[1]
    server_, port_, user_, passwd_, dir_ = read_config()
    send_bag(server_, port_, user_, passwd_, bag_file_, dir_)

if __name__ == '__main__':
    main()

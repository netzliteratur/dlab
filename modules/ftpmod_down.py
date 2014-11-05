#-*- coding:utf-8 -*-
import sys
import ConfigParser
import paramiko
from subprocess import check_output


def read_config():
    config = ConfigParser.RawConfigParser()
    config.read("config/bag.cfg")

    server_ = config.get("SFTP", "Server")
    port_ = config.get("SFTP", "Port")
    user_ = config.get("SFTP", "User")
    passwd_ = config.get("SFTP", "Password")
    dir_ = config.get("SFTP", "Directory")

    return server_, port_, user_, passwd_, dir_


def get_bszcrawl(server_, port_, user_, passwd_, crawl_file_, dir_):
    """
    :return:
    """
    transport = paramiko.Transport((server_, int(port_)))
    transport.connect(username=user_, password=passwd_)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.get(dir_ + crawl_file_, "temp/" + crawl_file_)
    sftp.get(dir_ + crawl_file_ + ".sha512", "temp/" + crawl_file_ + ".sha512")
    sftp.close()

    fd = open("temp/" + crawl_file_ + ".sha512")
    hash_sent_ = fd.readline()
    fd.close()

    hash_local_ret_ = check_output(["openssl", "sha512", "temp/" + crawl_file_])
    hash_local_ = hash_local_ret_.split("=")


    return hash_local_[1], hash_sent_


def main():
    """
    :return:
    """
    bag_file_ = sys.argv[1]
    server_, port_, user_, passwd_, dir_ = read_config()
    hash_local_, hash_sent_ = get_bszcrawl(server_, port_, user_, passwd_, bag_file_, dir_)

    # TODO Hashvergleich und Meldung nach Rückgab ein gui.py
    print(hash_local_[1:])
    print(hash_sent_)
    if hash_local_[1:] == hash_sent_:
        return 0
    else:
        return 1

if __name__ == '__main__':
    main()

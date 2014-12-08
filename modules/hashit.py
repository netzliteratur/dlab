import hashlib


def hashit(bag_file_):
    """
    create hash from bag
    """
    BLOCKSIZE = 65536
    hasher = hashlib.sha512()

    with open(bag_file_, 'rb') as file_:
        buf = file_.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = file_.read(BLOCKSIZE)

    fd = open(bag_file_ + "-sha512.txt", "w")
    fd.write(hasher.hexdigest())
    fd.close()

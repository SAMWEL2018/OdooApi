Trackingfile = "OrderTracking.txt"


def filemodification(msg):
    with open(Trackingfile, 'w') as f:
        f.write(msg)


def findCurrentOrderIndex():
    with open(Trackingfile) as rd:
        line = rd.readlines()
        print(int(line[0]))
        val = int(line[0])

    return val

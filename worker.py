import redis
import time

def main():
    import sys
    if not (len(sys.argv) == 2 and all(c.isdigit() for c in sys.argv[1])):
        print "usage: python %s count" % sys.argv[0]
        sys.exit(-1)
    Worker(redis.Redis()).run(int(sys.argv[1]))

SQUARE_NUMBER_SCRIPT = """
return redis.call("hset", ARGV[1], "square", redis.call("hget", ARGV[1], "num") ^ 2)
"""

class Worker(object):

    def __init__(self, conn):
        self.conn = conn

    def run(self, count):
        pubsub = self.conn.pubsub()
        start = time.time()
        for i in xrange(0, count):
            data = self.conn.brpop("jobs:queue")
            self.process(data[1])
        secs = time.time() - start
        print "Elapsed time: %s" % (secs)

    def process(self, key_id):
        self.conn.execute_command("eval", SQUARE_NUMBER_SCRIPT, 1, "key_id", key_id)


if __name__ == '__main__':
    main()


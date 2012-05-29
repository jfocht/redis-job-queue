import redis

def main():
    import sys
    if not (len(sys.argv) == 2 and all(c.isdigit() for c in sys.argv[1])):
        print "usage: python %s count" % sys.argv[0]
        sys.exit(-1)
    Client(redis.Redis()).run(int(sys.argv[1]))


class Client(object):

    def __init__(self, conn):
        self.conn = conn

    def run(self, count):
        self.pubsub = self.conn.pubsub()
        ids = self.get_ids(count)
        self.create_jobs(ids)

    def get_ids(self, count):
        pipeline = self.conn.pipeline()
        for x in xrange(0, count):
            pipeline.incr("jobs:nextid")
        return pipeline.execute()

    def create_jobs(self, ids):
        pipeline = self.conn.pipeline()
        for index, job_id in enumerate(ids):
            job = {"id": job_id,
                   "num": index + 1,
                   "status": "new"}
            key_id = "jobs:%s" % job["id"]
            self.conn.hmset(key_id, job)
            pipeline.lpush("jobs:queue", key_id)
        pipeline.execute()


if __name__ == '__main__':
    main()


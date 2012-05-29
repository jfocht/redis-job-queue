
def main():
    import sys
    if not (len(sys.argv) == 2 and all(c.isdigit() for c in sys.argv[1])):
        print "usage: %s count" % sys.argv[0]
        sys.exit(-1)
    count = int(sys.argv[1])
    run_python("client.py", str(count))
    run_python("worker.py", str(count)).communicate()


def run_python(*args):
    import sys
    import subprocess
    return subprocess.Popen([sys.executable] + list(args))


if __name__ == "__main__":
    main()

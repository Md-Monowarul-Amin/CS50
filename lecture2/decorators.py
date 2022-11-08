def announce(f):
    def wrapper():
        print("About to run the Function")
        f()
        print("Done with the function")
    return wrapper


@announce
def hello():
    print("Hellow, world")

hello()

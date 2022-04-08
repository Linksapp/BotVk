

def main(func):
    def a():
        print(0)
        func(c= 0)
        print(0)
    return a

@main
def c(c): print(1)

c()
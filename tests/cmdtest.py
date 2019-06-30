from cmd import Cmd

class Alpha(Cmd):
    def do_hello(self, inp):
        print("Bye")
        return True

    def do_goodbye(self, inp):
        print("Hello!")
        return True

def main():
    Alpha().cmdloop()

main()

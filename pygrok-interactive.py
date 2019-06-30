import pygrok
import pickle
import subprocess
import os
from prettytable import PrettyTable
from pathlib import Path
from cmd import Cmd

def prettyngrok(table):
    ptable = PrettyTable()

    ptable.field_names = ['No', 'Host', 'Port', 'IP', 'Type']

    for i in range(0, len(table)):
        ptable.add_row([i, table[i]['dns'], table[i]['port'], table[i]['ip'], table[i]['type']])

    return ptable

def cache(table):
    path_table = str(Path.home())+'/.config/pygrok/cache'
    pickle.dump(table, open(path_table, "wb"))

def loadcache():
    table = pickle.load(open(str(Path.home())+'/.config/pygrok/cache', "rb"))
    return table

def main():
    global table
    table = []
    cookie = pygrok.logindriver()

    if(os.path.exists(str(Path.home())+'/.config/pygrok/cache') == False):
        print("Downloading data...")
        table = pygrok.tabledict(pygrok.rawtabletext(cookie))
        cache(table)
    table = loadcache()

    class Interactive(Cmd):
        prompt = 'pygrok > '
        intro = 'Welcome to pygrok-interactive!'

        def do_update(self, inp):
            global table
            table = pygrok.tabledict(pygrok.rawtabletext(cookie))
            cache(table)

        def do_ls(self, inp):
            #global table
            print(prettyngrok(table))

        def do_ssh(self, inp):
            if int(inp) < int(len(table)) and table[int(inp)]['type'] == 'tcp':
                syntax = ['ssh', '-p', table[int(inp)]['port'], table[int(inp)]['dns']]
                subprocess.call(syntax)
            else:
                print("Selected an HTTP server or out of range!")

        def do_exit(self, inp):
            return True

    Interactive().cmdloop()

if __name__ == '__main__':
    main()

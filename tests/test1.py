import pygrok
import pickle
import os, subprocess

def main():
    cookie = {'domain': 'dashboard.ngrok.com', 'httpOnly': False, 'name': 'default', 'path': '/', 'secure': False, 'value': 'MTU2MTcyMTM2MnxEdi1CQkFFQ180SUFBUkFCRUFBQVJmLUNBQUlHYzNSeWFXNW5EQXdBQ21GalkyOTFiblJmYVdRRmFXNTBOalFFQlFEOUEzbEFCbk4wY21sdVp3d0pBQWQxYzJWeVgybGtCV2x1ZERZMEJBVUFfUU41ekE9PXxA0NOAG1t6ldFAI2_L1SWNuVy_Z-pinTShyAk52sE9Ug=='}

    #table = pygrok.rawtabletext(cookie)

    table = pickle.load(open("tabledump", "rb"))
    tabledict = pygrok.tabledict(table)

    print(tabledict)
    print(tabledict[0]['dns'])
    print(tabledict[0]['port'])

    syntax = ['ssh', '-p', tabledict[0]['port'], tabledict[0]['dns']]

    print(syntax)

    subprocess.call(syntax)



main()

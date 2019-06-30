import pygrok
import subprocess

def printngrok(ngrok):
    for i in range(0, len(ngrok)):
        print("-----", i, "------")
        print(ngrok[i]['dns'])
        print(ngrok[i]['port'])
        print(ngrok[i]['ip'])
        print("----- - -----")

def askssh(ngrok):
    num = int(input("Which server do you want to connect to?"))
    syntax = ['ssh', '-p', ngrok[num]['port'], ngrok[num]['dns']]
    subprocess.call(syntax)

def main():
    cookie = pygrok.getcookie()
    table = pygrok.tabledict(pygrok.rawtabletext(cookie))

    printngrok(table)
    askssh(table)

main()

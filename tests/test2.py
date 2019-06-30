import pygrok

def main():
    cookie = pygrok.getcookie()

    print(cookie)

    table = pygrok.rawtabletext(cookie)

    print(table)

    print(pygrok.tabledict(table))

main()

import fileinput

with fileinput.FileInput("proxies.txt", inplace=True, backup='.bak') as proxies:
    for line in proxies:
        well_formed_proxy = "http://" + line.split(" ")[0]
        line.replace(line, well_formed_proxy)

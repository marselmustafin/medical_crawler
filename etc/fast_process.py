import fileinput

with fileinput.FileInput("proxies.txt", inplace=True, backup='.bak') as proxies:
    for line in proxies:
        well_formed_proxy = "http://" + line.split(" ")[0]
        print(well_formed_proxy)
        line.replace(line, well_formed_proxy)

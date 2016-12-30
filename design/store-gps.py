import pipecat.udp

with open("../data/iphone-gps", "wb") as stream:
    pipe = pipecat.udp.receive(("0.0.0.0", 7777), 1024)
    for record in pipe:
        stream.write(record["string"])
        print record

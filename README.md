# myPythonChat

I've written this code for study purpose, i know it could be optimized

This is a simple client/server chat application over TCP with blocking sockets.
It's involved simmetric cryptography (AES-256-CBC algorithm) that encrypts in two different ways based on the direction of the comunication
The key is generated as follows:
key = sha256(socket.gethostname()+"MYSALTISVERYSALTED")

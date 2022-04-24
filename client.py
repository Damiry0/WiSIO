import io
import socket
import struct
import time
import picamera

client_socket = socket.socket()
client_socket.connect(('192.168.1.163', 8000))  # ADD IP HERE
# Make a file-like object out of the connection
connection = client_socket.makefile('wb')
try:
    camera = picamera.PiCamera()
    camera.vflip = True
    camera.resolution = (1920, 1080)
    # Start a preview and let the camera warm up for 2 seconds
    camera.start_preview()
    time.sleep(2)

    # Note the start time and construct a stream to hold image data
    # temporarily (we could write it directly to connection but in this
    # case we want to find out the size of each capture first to keep
    # our protocol simple)
    stream = io.BytesIO()
    camera.capture(stream,'png')
        # Write the length of the capture to the stream and flush to
        # ensure it actually gets sent
    connection.write(struct.pack('<L', stream.tell()))
    connection.flush()
        # Rewind the stream and send the image data over the wire
    stream.seek(0)
    connection.write(stream.read())
        # Reset the stream for the next capture
    stream.seek(0)
    stream.truncate()
    print("tutaj")
    # Write a length of zero to the stream to signal we're done
    connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    client_socket.close()

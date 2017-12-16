__author__ = 'ManiKanta Kandagatla'

import cv2
import sqlite3
from PIL import Image as Image2
from IPython.core.display import Image as Image1

# Camera 0 is the integrated web cam
camera_port = 0

#Number of frames to throw away while the camera adjusts to light levels
ramp_frames = 30

# Now we can initialize the camera capture object with the cv2.VideoCapture class.
# All it needs is the index to a camera port.
camera = cv2.VideoCapture(camera_port)
connection_string = "D:\\Languages\python\SQLite\ImageStorage.db"

# Captures a single image from the camera and returns it in PIL format
def get_image():
 # read is the easiest way to get a full image out of a VideoCapture object.
 retval, im = camera.read()
 return im

def discardImageFrames():
# Ramp the camera - these frames will be discarded and are only used to allow v4l2
# to adjust light levels, if necessary
    for i in xrange(ramp_frames):
        temp = get_image()

def storeInDB(conn,name , image):
    cur = conn.cursor()
    with open(image, 'rb') as input_file:
        image = input_file.read()
    cur.execute('insert into User( name, image) values (?,?)', ( name, sqlite3.Binary(image)))
    conn.commit()

def getImage(conn,name):
    cur = conn.cursor()
    image = cur.execute('select image from User where name=?', (name,)).fetchone()
    filename = './images/'+name + ".png"
    with open(filename, 'wb') as output_file:
        output_file.write(image[0])
    return filename

def init():
    conn = sqlite3.connect(connection_string)
    return conn

def main():
    conn  = init()
    print '######################################################################'
    name = raw_input('Enter name of user:')
    print("Capturing image...!!")
    discardImageFrames()
    camera_capture = get_image()
    file = "pic.png"
    cv2.imwrite(file, camera_capture)
    storeInDB(conn,name,file)
    image=getImage(conn,name)
    Image1(filename = image)
    img = Image2.open(image)
    img.show()
main()
del(camera)
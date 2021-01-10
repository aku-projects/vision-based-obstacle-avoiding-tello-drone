"""rc a b c d
a left/right
b forward/backward
c up/down
d yaw """

import sensor, image, time, math
from machine import UART
from fpioa_manager import fm
from board import board_info


obstacle = (31, 100, -128, 127, -128, 127)

fm.register (15, fm.fpioa.UART1_TX)
fm.register (17, fm.fpioa.UART1_RX)
uart_A = UART (UART.UART1, 9600, 8, None, 1, timeout = 1000, read_buf_len = 4096)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_hmirror(0)
sensor.skip_frames(time = 2000)



def process_tags():
    img = sensor.snapshot()
    img = img.mean_pool(10,10)
    img = img.binary([obstacle])
    blobs = img.find_blobs([obstacle],\
                            area_threshold = 105,\
                            pixel_threshold = 170,\
                            merge = True,\
                            invert=True)
    if blobs:
        for b in blobs:
            xcenter=b.cx()
            ycenter=b.cy()
            area = b.area()
            print([xcenter,ycenter,area ])
            if ycenter > 16 :
                print("move up")
                print("1:rc 0 0 12 0")
                return "1:rc 0 0 12 0"
            elif ycenter < 8 :
                print("move down")
                print("1:rc 0 0 -12 0")
                return "1:rc 0 0 -12 0"
            elif xcenter > 22 :
                print("move left")
                print("1:rc -12 0 0 0")
                return "1:rc -12 0 0 0"
            elif xcenter < 11 :
                print("move right")
                print("1:rc 12 0 0 0")
                return "1:rc 12 0 0 0"
            else:
                print(b.x(),b.y(),b.w(),b.h())
                if b.y() > 8 and b.y() < 16 :
                    print("move up 1")
                    print("1:rc 0 0 12 0")
                    return "1:rc 0 0 12 0"
                elif b.x() > 11 and b.x() < 22:
                    print("move left 1")
                    print("1:rc -12 0 0 0")
                    return "1:rc -12 0 0 0"
                elif area < 400:
                    print("move back and left")
                    print("1:rc -12 0 -12 0")
                    return "1:rc -12 0 -12 0"
                else:
                    print("stop")
                    print("1:rc 0 0 0 0")
                    return "1:rc 0 0 0 0"
    else:
        print("move forward")
        print("0:rc 0 0 0 0")
        return "0:rc 0 0 0 0"

def run_algo():

    print("replying :)")
    rccommand = process_tags()
    print(rccommand)
    uart_A.write(rccommand)



while(1):
    #uncomment to run this code with esp32
    #if uart_A.any():
        #try:

            #read_data = uart_A.read()
            #read_str = read_data.decode('utf-8')
            #if (read_str == "1"):
                #print("string = ", read_str)
                #run_algo()
        #except  (UnicodeError):
            #pass
    #uncomment to debugging this code while connected to PC       
    run_algo()

uart_A.deinit ()
del uart_A



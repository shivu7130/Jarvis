
import pyfirmata
import time

board = pyfirmata.Arduino('COM3')

it = pyfirmata.util.Iterator(board)
it.start()
count=0

board.digital[10].mode = pyfirmata.INPUT

while True:
    sw = board.digital[10].read()
    if sw is True:
        board.digital[13].write(1)
        
    else:
        board.digital[13].write(0)
    time.sleep(0.1)

import random
import json
import re
from unittest import result
import torch
from Brain import NeuralNet
from NeuralNetwork import bag_of_words, tokenize
from Task import InputExecution, NonInputExecution
from security import security
import pyfirmata
import time
board = pyfirmata.Arduino('COM3')

it = pyfirmata.util.Iterator(board)
it.start()

board.digital[10].mode = pyfirmata.INPUT
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
with open('intents.json','r') as json_data:
    intents = json.load(json_data)

FILE = "TrainData.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size,hidden_size,output_size).to(device=device)
model.load_state_dict(model_state)
model.eval()

#---------------FOR JARVIS------------------
Name = "Jarvis"

from listen import listen
from speak import say
from Task import InputExecution, NonInputExecution

def Main():
    sentence = listen()
    result = str(sentence)
    sw = board.digital[10].read()
    if sw is True:
            board.digital[13].write(1)
            security()
    else:
         board.digital[13].write(0)
         time.sleep(0.1)



    #if sentence == "bye":
        #exit()

    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)

    _ , predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                reply = random.choice(intent["responses"])

                if "time" in reply:
                    NonInputExecution(reply)
                elif "date" in reply:
                    NonInputExecution(reply)
                elif "day" in reply:
                    NonInputExecution(reply)
                
                elif "google" in reply:
                    InputExecution(reply,result)
                else:
                    say(reply)

while True:
        Main()
       # sw = board.digital[10].read()
        ##if sw is True:
          #  board.digital[13].write(1)
           # security()
        #else:
         #board.digital[13].write(0)
        #time.sleep(0.1)


   
# IMPORTS AND VARIABLES
import os
import json
import numpy as np
import pylab as pl
import datetime
import pandas as pd
from collections import Counter

CURRENT_DIRECTORY = os.getcwd()
NUMBER_TO_ANALYZE = 50000
MESSAGE_THRESHOLD = 1000

# FIRST DEFINITIONS
def get_json_data(chat):
    try:
        json_location = CURRENT_DIRECTORY + "/messages/" + chat + "/message.json"
        with open(json_location) as json_file:
            json_data = json.load(json_file)
            return json_data
    except IOError:
        pass # some things the directory aren't messages (DS_Store, stickers_used, etc.)

def clean_word(word):
    return (word.lower())

# ANALYZE CHATS
chats = os.listdir(CURRENT_DIRECTORY + "/messages/")[:NUMBER_TO_ANALYZE]
sorted_chats = []
final_data_messages = {}
final_data_times = {}
final_data_words = {}
invalid_message_count = 0

print('Analyzing ' + str(min(NUMBER_TO_ANALYZE, len(chats))) + ' chats...')

for chat in chats:
    url = chat + '/message.json'
    json_data = get_json_data(chat)
    print(chat)
    if json_data != None:
        messages = json_data["messages"]
        if len(messages) >= MESSAGE_THRESHOLD:
            sorted_chats.append((len(messages), chat, messages))

sorted_chats.sort(reverse=True)

print('Finished processing chats...')

words_used = []
message_words = []

for i, (messages, chat, messages) in enumerate(sorted_chats):
    for message in messages:
        try:
            words_list = [clean_word(word) for word in message["content"].split()]
            words_used += words_list
            message_words.append(words_list)
        except KeyError:
            # happens for special cases like users who deactivated, unfriended, blocked
            invalid_message_count += 1

print('Found ' + str(invalid_message_count) + ' invalid messages...')
print('Found ' + str(len(sorted_chats)) + ' chats with ' + str(MESSAGE_THRESHOLD) + ' messages or more')

# make list of words used more than 20 times
times_used = Counter(words_used)
significant_words = [k for k,v in times_used.items() if (v > 20)]

# matrix to hold word vector for each message
usage_matrix = np.zeros((len(message_words), len(significant_words)))

print(usage_matrix.shape)

# create binary usage vector for words in each message
for rowCounter, message in enumerate(message_words):

    for word in message:
        for colCounter, word_check in enumerate(significant_words):
            if word == word_check:
                usage_matrix[rowCounter, colCounter] = 1



# CHECK AGAINST MODEL
def check_against_model():
    input = input("Send me a sample message:\n")
    print([clean_word(word) for word in input.split()])

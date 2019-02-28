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
MESSAGE_THRESHOLD = 100
FRIEND_CUTOFF = 1000 # number of messages with a person to consider a friend

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
number_messages = []

for i, (messages, chat, messages) in enumerate(sorted_chats):
    for message in messages:
        try:
            # is person a friend?
            friend_binary = 1 if len(messages) > FRIEND_CUTOFF else 0
            number_messages.append(friend_binary)
            # strings used in message
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
print(significant_words)

# matrix to hold word vector for each message
usage_matrix = np.zeros((len(message_words), len(significant_words)))

# create binary usage vector for words in each message
for rowCounter, message in enumerate(message_words):
    for word in message:
        for colCounter, word_check in enumerate(significant_words):
            if word == word_check:
                usage_matrix[rowCounter, colCounter] = 1

# print(len(number_messages))
# print(usage_matrix.shape)

# CHECK AGAINST MODEL
def check_against_model():
    user_words = input("Send me a sample message:\n")
    cleaned_input = [clean_word(word) for word in user_words.split()]
    input_vector = np.zeros((len(cleaned_input)))
    for word in cleaned_input:
        for count, word_check in enumerate(significant_words):
            if word == word_check:
                input_vector[count] = 1
    print(input_vector)

check_against_model()

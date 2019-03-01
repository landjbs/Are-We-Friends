# Are-We-Friends

Facebook message data is a treasure trove for using NLP to analyze relationships. This rudimentary machine learning model trains on vectors of the binary presence of words in a message against a score vector of whether or not that message is part of a conversation with a "friend" of message number greater than the "friend cutoff".  The *check_against_model* funciton allows the user to input sample messages and see if they might be something sent to or from one of my friends.

There are many ways to further improve this program. Some things I hope to work on:


1.   Better cleaning the words (eg. stripping punctuation)
2.   Better determining the words to train on (eg. looking at corrolation with friendship and only using those with high scores)
3.   Creating more classifications than the simple binary "friend" or "not friend".
4.   Examining relationship between and usage number of words in sentence rather than simple binary vector.
5.   Making sure the data isn't skewed by the fact that friendship inherently carries more words and usage possibilities.

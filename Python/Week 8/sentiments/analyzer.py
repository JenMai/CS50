#---------------------------------
# Functions for smile, tweets and application.py
#----------------------------------

import nltk

class Analyzer():
    """Implements sentiment analysis."""
    # TODO
    def __init__(self, positives, negatives):
        self.positives = []
        self.negatives = []
        """Initialize Analyzer."""
        with open("positive-words.txt") as lines:
            for line in lines:
                if line.startswith(";"):                                    # ignore comments
                    continue
                else:                                                       # add each word to list
                    line = line.strip(" ")
                    line = line.replace("\n", "")
                    self.positives.append(line)
                    
        with open("negative-words.txt") as lines:
            for line in lines:
                if line.startswith(";"):
                    continue
                else:
                    line = line.strip(" ")
                    line = line.replace("\n", "")
                    self.negatives.append(line)

    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""
        # TODO
        tokenizer = nltk.tokenize.casual.TweetTokenizer(preserve_case=False)
        token = tokenizer.tokenize(text)                                    # each word in tweet is a separate strings
        score = 0
        
        for word in token:
            if word in self.positives:
                score += 1
            elif word in self.negatives:
                score -= 1
            else:
                continue
            
        return score

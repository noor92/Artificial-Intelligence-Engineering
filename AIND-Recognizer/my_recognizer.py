import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    # TODO implement the recognizer
    # return probabilities, guesses
    for testing_word, (X, lengths) in test_set.get_all_Xlengths().items():
        
            best_score=float("-inf")
            best_guess=""
            prob_dict={}

            for trained_word, model in models.items():
                #trained word is John, testing word is the index of john 0
       
                try:
                    log_prob = model.score(X, lengths)
                    prob_dict[traned_word] = log_prob

                except:
                    prob_dict[trained_word] = float("-inf")
                    
                if log_prob > best_score:
                    best_score = log_prob
                    best_guess = trained_word
                
            probabilities.append(prob_dict)
            guesses.append(best_guess)

    return probabilities, guesses
                    

        

    
    

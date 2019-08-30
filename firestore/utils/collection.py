

def mapcase(sentence, separator="_", lowercase=False):
    """
    Takes a given text/sentence and finds capitalized alphabets to use
    as a boundary to apply the `separator` argument and return a new
    sentence/text separated by the chosen `separator` defaults to underscores i.e. `_`

    TODO: Optimize this function later when not in hack mode
    """
    words = []
    caps_will_clash = sentence[0].islower()
    aggregates = ''
    for alphabet in sentence:
        if alphabet.isupper() and caps_will_clash:
            if lowercase:
                aggregates = aggregates.lower()
            words.append(aggregates)
            aggregates = ''
        elif alphabet.isupper():
            caps_will_clash = True
        aggregates += alphabet
    
    # add alphabets that were aggregated during last run but
    # not appended due to loop exhaustion.
    aggregates = aggregates.lower() if lowercase else aggregates
    words.append(aggregates)

    return separator.join(words)

import pickle

# return lists of lists containing the melody/chords of a song.
# Indices match on time steps
def read_pickle_file():
    with open('all_keys_notes', 'rb') as filepath:
        notes = pickle.load(filepath)

    melody = notes['melody']
    chords = notes['chords']
    return (melody, chords)

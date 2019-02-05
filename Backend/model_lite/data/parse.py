from music21 import converter, instrument, note, chord, stream, interval, pitch
import sys
import os
import pickle

dir_ = sys.argv[1]          # location of data
pickle_file = sys.argv[2]   # location for where to put pickle file

all_melody = []
all_chords = []
sixteenth = 0.25 # 16th note: 1 = quarter note, 0.5 = 8th note

for file in os.listdir(dir_):
    try:
        midi = converter.parseFile(dir_ + '/' + file)
    except:
        print('Could not parse ' + file)
        continue

    offset = 0
    stop = midi.highestTime
    song_melody = []
    song_chords = []

    while offset < stop:
        cur_melody = []
        cur_chords = []
        all_notes = midi.recurse().getElementsByOffsetInHierarchy(
                                    offset,
                                    offsetEnd=offset+sixteenth,
                                    mustBeginInSpan=False,
                                    includeElementsThatEndAtStart=False).notes

        # gather notes and cur_chords played at offset
        for element in all_notes:
            if isinstance(element, note.Note):
                cur_melody.append(str(element.pitch.name))
            elif isinstance(element, chord.Chord):
                cur_chords.append('.'.join(sorted([str(p.name) for p in element.pitches])))

        # nothing playing at offset
        if len(cur_melody) == 0 and len(cur_chords) == 0:
            song_melody.append('')
            song_chords.append('')

        # cur_melody played but not chord at offset
        elif len(cur_chords) == 0:
            for n in cur_melody:
                song_melody.append(n)
                song_chords.append('')

        # cur_chords played but not cur_melody at offset
        elif len(cur_melody) == 0:
            for c in cur_chords:
                song_melody.append('')
                song_chords.append(c)

        # both played at offset
        else:
            for n in cur_melody:
                for c in cur_chords:
                    song_melody.append(n)
                    song_chords.append(c)

        offset += sixteenth

    all_melody.append(song_melody)
    all_chords.append(song_chords)

# put into dictionary and send to pickle file
harmony = {}
harmony['melody'] = all_melody
harmony['chords'] = all_chords

with open(pickle_file, 'wb') as filepath:
    pickle.dump(harmony, filepath)

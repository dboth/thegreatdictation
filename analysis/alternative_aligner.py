 # -*- coding: utf-8 -*-
from __future__ import division
from alignment.sequence import Sequence
from alignment.vocabulary import Vocabulary
from alignment.sequencealigner import Scoring, SimpleScoring, GlobalSequenceAligner
from scoring import AlignmentScoring

def extractAlignment(al):
    return zip([str(e) for e in al.first.elements],[str(e) for e in al.second.elements])

# Create sequences to be aligned.
a = Sequence('Ich bin ein Elefant. Ich habe ein Autohaus.'.split())
b = Sequence('I bin Edlefant. Ik habe ein Auto Haus.'.split())

# Create a vocabulary and encode the sequences.
v = Vocabulary()
aEncoded = v.encodeSequence(a)
bEncoded = v.encodeSequence(b)

# Create a scoring and align the sequences using global aligner.
scoring = AlignmentScoring(v, aEncoded.key(), bEncoded.key())
aligner = GlobalSequenceAligner(scoring, 30) #das muss auch noch optimiert werden der wert
score, encodeds = aligner.align(aEncoded, bEncoded, backtrace=True)


# Iterate over optimal alignments and print them.
for encoded in encodeds:
    alignment = v.decodeSequenceAlignment(encoded)
    print alignment
    print 'Alignment score:', alignment.score
    print 'Percent identity:', alignment.percentIdentity()
    print extractAlignment(alignment)
    #für prüfen ob irgendwo ein falsches leerzeichen eingefügt wurde und dann die tupel vereinigen. vielleicht ist das auch leichter im preprocessing?
    #anschließend tobias levenshtein über jeden tupel laufen lassen und die ergebnisse zusammenfügen und an frontend
    

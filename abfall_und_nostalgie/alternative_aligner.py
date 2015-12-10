 # -*- coding: utf-8 -*-
from __future__ import division
from alignment.sequence import Sequence
from alignment.vocabulary import Vocabulary
from alignment.sequencealigner import Scoring, SimpleScoring, GlobalSequenceAligner
from scoring import AlignmentScoring


class TGDAligner(object):
    def __init__(self, original_sentence, typed_sentence):
        oS = self.splitSentences(original_sentence)
        tS = self.splitSentences(typed_sentence)
        self.output = []
        self.sentences = zip(oS,tS)
        self.startAligning()
         
    def splitSentences(self, text):
        #todo: really split sentences. return as list of sentences.
        #maybe the frontend should already mark sentences in some way
        #just splitting on "." is not reliable!
        return [text]
    
    def splitTokens(self, sentence):
        return sentence.split()
    
    def startAligning(self):
        for sentence in self.sentences:
            alignment = self.getAlignment(sentence)
            #alignment contains a list of tuples like [(Ich, Ik), (bin, ben), (ein, - ), ( - , Olo), ( Elefant , Fant)]
            alignment = self.fixMissingOriginals(alignment) #see comment of method
            analysis = self.applyLevenshtein(alignment)
            self.output += analysis #maybe one list per sentence, so the output is a list of lists
    
    def fixMissingOriginals(self,alignment):
        #todo: missing words on the original side should be looked at carefully: Does ( - , Ölo) belong to ein or Elefant or is it inserted without cause?
        # [(Ich, Ik), (bin, ben), (ein, - ), ( - , Olo), ( Elefant , Fant)] should be made to: [(Ich, Ik), (bin, ben), (ein, - ), ( Elefant , Olo Fant)]
        #to achieve this look at the words beside the hole
        return alignment
        
    def applyLevenshtein(self, alignment):
        out = []
        for words in alignment:
            #todo: apply tobias levenshtein analysis on words[0] to words[1] and append the analysis
            #yet nothin is done, only returned
            out.append(words)
        return out
    
    def extractAlignment(self, al):
        return zip([str(e) for e in al.first.elements],[str(e) for e in al.second.elements])    
            
    def getAlignment(self, sentencePair):
        a = Sequence(self.splitTokens(sentencePair[0]))
        b = Sequence(self.splitTokens(sentencePair[1]))
        # Create a vocabulary and encode the sequences.
        v = Vocabulary()
        aEncoded = v.encodeSequence(a)
        bEncoded = v.encodeSequence(b)
        # Create a scoring and align the sequences using global aligner.
        scoring = AlignmentScoring(v, aEncoded.key(), bEncoded.key())
        aligner = GlobalSequenceAligner(scoring, 200) #das muss auch noch optimiert werden der wert. Falls besonders oft Löcher alignt werden liegt das sicher an diesem wert!
        score, encodeds = aligner.align(aEncoded, bEncoded, backtrace=True)
        alignment = v.decodeSequenceAlignment(encodeds[0])
        return self.extractAlignment(alignment)
        
    def returnOutput(self):
        return self.output
        
if __name__ == "__main__":
    original,input = "Ich bin ein Elefant.", "Ik bin bin ein Fant."
    print original,input
    tgd = TGDAligner(original, input)
    print tgd.returnOutput()
    original,input = "Eine Rose ist eine Rose ist eine Rose.", "Aine Ros is ain Ros is ain Ross."
    print original,input
    tgd = TGDAligner(original, input)
    print tgd.returnOutput()
        
    
    


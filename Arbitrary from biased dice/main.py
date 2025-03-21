import random

# Solution for https://x.com/Mihonarium/status/1899707557486223714.
# An Extractor takes a random process as an input and outputs a different random process.
# This Extractor throws a biased dice with known probabilities until the result differs from the first result.
# From this sequence of throws the Extractor produces a biased coin with arbitrary probability.
class Extractor:
    def __init__(self, ps : list, p):
        assert sum(ps) == 1.0
        self.ps = ps
        self.p = p
        self.sides = list(range(len(ps)))
        self.__state = [(ps[i], [i], j) for i in self.sides for j in self.sides]
        self.__trueFill,  self.__trues  = (0.0, [])
        self.__falseFill, self.__falses = (0.0, [])
    
    def step(self):
        self.__state.sort()
        s = self.__state.pop()

        newP = s[0] * self.ps[ s[2] ]
        newO = s[1].copy()
        newO.append(s[2])

        if s[1][-1] == s[2]:
            self.__state.extend( [ (newP, newO, j) for j in self.sides] )
        else:
            fitsTrue =  self.__trueFill  +          newP <= self.p
            fitsFalse = self.__falseFill + self.p + newP <= 1.0
            assert fitsTrue or fitsFalse
            if fitsTrue: self.__trues.append(newO);  self.__trueFill += newP
            else:        self.__falses.append(newO); self.__falseFill += newP
            return newO
            
    def search(self, outcome):
        if outcome in self.__trues:  return True
        if outcome in self.__falses: return False
        while True:
            if outcome == self.step():
                if outcome in self.__trues:  return True
                if outcome in self.__falses: return False

    def throw(self):
        outcome = random.choices(self.sides, self.ps)
        while True:
            outcome.append(random.choices(self.sides, self.ps)[0])
            if outcome[-1] != outcome[-2]: return outcome
    
    def extract(self):
        return self.search(self.throw())


def test(ext, num=10000):
    t = 0
    for _ in range(num):
        if ext.extract(): t += 1
    print(ext.p, "=>", t / num)

ext = Extractor(ps=[0.03, 0.05, 0.09, 0.2, 0.23, 0.4], p=0.723)
test(ext)

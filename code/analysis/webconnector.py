from tgd import TheGreatDictation
#the webconnector for mod_python
def analyze(req, data):
    print(TheGreatDictation(data).returnJSON())
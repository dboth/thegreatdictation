import string
import random
def createRandomString(length, withWhiteSpace = False):
    #letters = string.lowercase
    letters = "aa"
    if withWhiteSpace == True:
        #space_letters = letters + "     "
        space_letters = letters + " "
    result = ""
    if withWhiteSpace == False:
        for i in range(length):
            result += random.choice(letters)
    else:
        space_before = True
        for i in range(length):
            if space_before == True:
                result += random.choice(letters)
                space_before = False
            else:
                result += random.choice(space_letters)
                if result[-1] == " ":
                    space_before = True
    return result
    
if __name__ == "__main__":
    rand_str = createRandomString(100, True)
    print rand_str
    nonwhite = createRandomString(100)
    print nonwhite
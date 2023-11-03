from typing import Tuple, List
import utils
from helpers.test_tools import read_text_file,read_word_list

'''
    The DecipherResult is the type defintion for a tuple containing:
    - The deciphered text (string).
    - The shift of the cipher (non-negative integer).
        Assume that the shift is always to the right (in the direction from 'a' to 'b' to 'c' and so on).
        So if you return 1, that means that the text was ciphered by shifting it 1 to the right, and that you deciphered the text by shifting it 1 to the left.
    - The number of words in the deciphered text that are not in the dictionary (non-negative integer).
'''
DechiperResult = Tuple[str, int, int]

def decipher(ciphered:str, shift:int)->str:
    result = ''
    for c in ciphered:
        if c==' ':
            result += c
        else:
            diff = ord(c) - ord('a')
            result += chr(ord('a') + (diff + 26 - shift)%26)
    return result

def caesar_dechiper(ciphered: str, dictionary: List[str]) -> DechiperResult:
    '''
        This function takes the ciphered text (string)  and the dictionary (a list of strings where each string is a word).
        It should return a DechiperResult (see above for more info) with the deciphered text, the cipher shift, and the number of deciphered words that are not in the dictionary. 
    '''
    result: DechiperResult = ('', 0, 1000000)
    BOW = set(dictionary)
    for shift in range(26):
        deciphered = decipher(ciphered, shift)
        words = deciphered.split()
        not_in_dict = 0
        for word in words:
            if word not in BOW:
                not_in_dict += 1
        if not_in_dict < result[2]:
            result = (deciphered, shift, not_in_dict) 
    return result



import pycorrector
import language_tool_python
from utils import contain_english
print("[Corrector]")
pycorrector.enable_char_error(enable=False)
english_corrector = language_tool_python.LanguageTool('en-US')
print("[Corrector] Init end")

def correct(st):
    if contain_english(st):
        return correct_english(st)
    else:
        return correct_chinese(st)

def correct_chinese(st):
    corrected, detail = pycorrector.correct(st)
    if len(detail) == 0:
        return None
    else:
        return corrected


def correct_english(st):
    corrected = english_corrector.correct(st)
    if st.lower() == corrected.lower():
        return None
    else:
        return corrected


if __name__ == '__main__':
    print(correct("今天是个好天其"))
    print(correct("今天是个好天气"))
    print(correct("A sentence with a error"))
    print(correct("how are you"))
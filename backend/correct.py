import pycorrector
print("[Corrector]")
pycorrector.enable_char_error(enable=False)
print("[Corrector] Init end")

def correct(st):
    corrected, detail = pycorrector.correct(st)
    if len(detail) == 0:
        return None
    else:
        return corrected

if __name__ == '__main__':
    print(correct("今天是个好天其"))
    print(correct("今天是个好天气"))

def check_message(input):
    try:
        input=input.strip()
        number=eval(input)
        if len(input) != 8:
            return False
        else:
            return True

    except:
        return False
def count_letters_and_digits(s):
    return sum(s.isalnum() for a in s)

count_letters_and_digits('n!!ice!!123')
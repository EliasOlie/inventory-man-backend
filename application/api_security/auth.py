from secrets import compare_digest

def check(a, b):
    return compare_digest(a, b)
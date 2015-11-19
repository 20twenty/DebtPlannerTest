
def get_number(s):
    l = []
    for t in s.split():
        try:
            l.append(float(t))
        except ValueError:
            pass

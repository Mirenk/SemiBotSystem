from candidate import Candidate

if __name__ == '__main__':
    me = Candidate("b20p034", "Endeavor")
    res = me.get("/")
    print(res.text)
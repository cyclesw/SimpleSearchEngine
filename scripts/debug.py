from scripts.searcher import Searcher

msg = '../data/output/raw.txt'

sc = Searcher()
sc.init_searcher(msg)

while True:
    buf = input('Please Enter your Search Query#')
    print(sc.search(buf))


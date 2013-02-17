import webbrowser

base_url1 = r'http://patft.uspto.gov/netacgi/nph-Parser?TERM1='
base_url2 = r'&Sect1=PTO1&Sect2=HITOFF&d=PALL&p=1&u=%2Fnetahtml%2FPTO%2Fsrchnum.htm&r=0&f=S&l=50'


def lookup(num):
    full = base_url1 + num + base_url2
    webbrowser.open(full)

if __name__ == '__main__':
    import sys
    num = sys.argv[1]
    lookup(num)

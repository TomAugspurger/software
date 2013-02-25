import webbrowser
from cPickle import load

import pandas as pd

class Lookup(object):
    """
    Example:

    apple = df[df['uspto_assignee'] == 32940]  # Apple, 1559 patents
    c = Lookup(apple['patent'].tolist())
    g = c.patent_to_web()
    g.next()
    """
    def __init__(self, patents):
        """Allow num to be a single patent or a list?
        """
        self.patents = patents
        self.d_patent_to_int = None
        self.d_int_to_patent = None
        self.utility = None
        self.uspto_assignee = None
    
    def init_dicts(self, d1='just_tech_int_to_patent.pkl',
        d2='just_tech_patent_to_int.pkl'):
        try:
            with open(d1, 'r') as f:
                self.d_patent_to_int = load(f)
        except IOError:
            raise IOError('Can\'t get the dict.')
        try:
            with open(d2, 'r') as f:
                self.d_int_to_patent = load(f)
        except IOError:
            raise IOError('Can\'t get the dict.')

    def patent_to_web(self):
        """Go to USPTO website.
        Use a generator to avoid open a bunch at once.
        Either use g = self.patent_to_web() and g.next() or loop through
        with an iterator (for i in g).
        """
        def _patent_to_web(xs):
            for i in xs:
                print i
                base_url1 = r'http://patft.uspto.gov/netacgi/nph-Parser?TERM1='
                base_url2 = r'&Sect1=PTO1&Sect2=HITOFF&d=PALL&p=1&u=%2Fnetahtml%2FPTO%2Fsrchnum.htm&r=0&f=S&l=50'
                full = base_url1 + str(i) + base_url2
                yield webbrowser.open(full)

        if isinstance(self.patents, int):
            return _patent_to_web([self.patents])
        elif isinstance(self.patents, list):
            return _patent_to_web(self.patents)

    def int_to_web(self, int_):
        self.patent_to_web(self.int_to_patent(int_))

    def int_to_patent(self, int_):
        """Helper to map from integers (for sparse graphs) to patent numbers.
        Could also access the dict directly.
        """
        return self.d_int_to_patent[int_]

    def patent_to_int(self, patent):
        return self.d_patent_to_int(patent)

    def get_all(self, patent=None):
        """Lookup the owner and get all patents from that owner.
        If patents is a lists, maybe specify a number.
        """
        if self.utility is None:
            print("Loading the utility file...")
            s = pd.HDFStore(
                '/Volumes/HDD/Users/tom/DataStorage/Patents/patents.h5')
            self.utility = s['utility']
            s.close()
        df = self.utility

        if patent is None:
            patent = [self.patents][0]
            if isinstance(self.patents, list):
                print('Just matching for the first patent {}.\n'.format(
                    self.patents[0]))
                patent = self.patents[0]

        a = df[df['patent'] == patent]
        all_a = df[df['uspto_assignee'] == a['uspto_assignee'].values[0]]
        self.uspto_assignee = a['uspto_assignee'].values[0]
        self.all = all_a
        return all_a

if __name__ == '__main__':
    # Quick access to website.
    import sys
    num = int(sys.argv[1])
    c = Lookup(num)
    g = c.patent_to_web().next()

necWord = '지지'
parties = [[], ['민주당'], ['국민의힘', '국힘', '국힘당'], [], [], ['정의당'], [], ['개혁신당'], ['조국혁신당']]
NUM_OF_PARTIES = len(parties)

party_space = {}

class Party:
    def __init__(self, num):
        self.name = parties[num][0]
        self._base = ' | '.join(parties[num])
        self._EXCEPT = ' '.join([f'-{i}' for i in sum(parties[:num]+(parties[-len(parties)+num+1:])*(not not -len(parties)+num+1), [])])
        self.keywords = [self._base, f'{self._base} {necWord}', f'{self._base} 후보', f'{self._base} 선거']

for i in range(NUM_OF_PARTIES):
    if parties[i]:
        party_space[parties[i][0]] = Party(i)

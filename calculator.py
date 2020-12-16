import csv

class calculator:

    def __init__(self):
        self.relics, self.look_up = self.get_relics()
        self.relic_tree = self.get_relic_tree()
        self.branches = ['might', 'celerity', 'sustenance', 'fortitude', 'sorcery']
        self.levels = [1, 2, 3 , 4, 5]
        return

    def get_relics(self):
        relics = list()
        relic_dic = dict()
        look_up = dict()

        with open('data/relics.tsv', 'r') as c:
                tsv_reader = csv.DictReader(c, delimiter='\t')
                for row in tsv_reader:
                    relics.append(row)

        for relic in relics:
            relic['id'] = int(relic['id'])
            relic['price'] = int(relic['price'])
            components = relic['Component Relics'].strip().split(',')
            int_comp = list()
            for i in range(len(components)):
                if (components[i]):
                    int_comp.append(int(components[i]))                            

            relic['Component Relics'] = int_comp

            relic_dic[relic['id']] = {'name':relic['name'], 'price':relic['price'], 'quality':relic['quality'], 'components':relic['Component Relics']}
            look_up[relic['name']] = relic['id']

        return relic_dic, look_up

    def get_relic_tree(self):
        relics = list()
        tree = dict()

        with open('data/relic_tree.tsv', 'r') as c:
                tsv_reader = csv.DictReader(c, delimiter='\t')
                for row in tsv_reader:
                    relics.append(row)        

        for row in relics:        
            branch = row['Branch'].lower()
            level = int(row['Level'])
            relics = [None, int(row['Relic ID 1']), int(row['Relic ID 2']), int(row['Relic ID 3']), 
            int(row['Relic ID 4']), int(row['Relic ID 5']), int(row['Relic ID 6'])]            
            if branch not in tree.keys():
                tree[branch] = dict()

            tree[branch][level] = relics
            
        return tree

    def contains_relic(self, want, have):
        components = self.relics[want]['components']
        if have in components:
            return True        

        for component in components:
            if self.contains_relic(component, have):
                return True        

        return False

    def get_total_cost(self, want, haves = list()):        
        essence = self.relics[want]['price']
        for have in haves:
            if self.contains_relic(want, have):
                essence -= self.relics[have]['price']

        return essence

    def get_relic_id(self, branch, level, relic_spot):
        for c in self.branches:
            if branch.lower() in c:
                branch = c
        
        if branch not in self.branches:
            return -1

        return self.relic_tree[branch][level][relic_spot]

    def get_total_cost_by_name(self, want_relic_name, have_relic_names = list()):
        want = self.look_up[want_relic_name]
        haves = [self.look_up[have] for have in have_relic_names] 
        return self.get_total_cost(want, haves)

def sanity_check(calc):
    test_id = calc.get_relic_id('sus', 5, 2)
    test_relic = calc.relics[test_id]    

    print(test_relic)
    print(calc.get_total_cost(test_id, [4505, 4506, 4405]))

    test_id = calc.get_relic_id('fort', 4, 2)
    test_relic = calc.relics[test_id]
    print(test_relic)
    print(calc.get_total_cost(test_id, [4505, 4506, 4405]))

    print(calc.relics[3202])

    print(calc.get_total_cost_by_name('The Imperishable', ['Arena Bracers']))

    names = set()
    for relic in calc.relics.values():
        name = relic['name']
        if name in names:
            print(f'duplicate found {name}')
        else:
            names.add(relic['name'])

if __name__ == "__main__":
    calc = calculator()
    sanity_check(calc)
    

    
    pass
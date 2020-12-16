import csv
import copy

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
            components = list()
            for r in relic['Component Relics'].strip().split(','):
                if r:
                    components.append(int(r))

            relic_dic[relic['id']] = {'name':relic['name'], 'total_cost':relic['price'], 'quality':relic['quality'], 'components':components}
            look_up[relic['name']] = relic['id']

        with open('data/relic_stats.tsv', 'r') as c:
            tsv_reader = csv.DictReader(c, delimiter='\t')
            for row in tsv_reader:
                relics.append(row)        

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

    def get_total_cost_for_multiple_relics(self, wants, haves=list()):
        essence = 0
        for want in wants:
            essence += self.get_total_cost(want, haves)
        
        return essence 

    def get_total_cost(self, want, haves = list()):        
        essence = self.relics[want]['total_cost']
        for have in haves:
            if self.contains_relic(want, have):
                essence -= self.relics[have]['total_cost']

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
    relic_ids = list()
    haves = list()

    have_lookup = {
        "The Wall": 1, 
        "Compassion's Core":2, 
        "Immortal's Cinctures":2, 
        "Eye Of Wisdom": 2, 
        "Chalice of Light": 1, 
        "Kuilin Ring":1, 
        "Rambler's Boots":2,
        "Blitz Arc": 2, 
        "Noble Blade": 2, 
        "Determination's Core": 1, 
        "Agility's Core": 2}

    for r, num in have_lookup.items():
        for i in range(num):
            haves.append(calc.look_up[r])

    thresholds = dict()

    relic_ids.append(calc.relic_tree['might'][4][1])
    relic_ids.append(calc.relic_tree['might'][4][3])
    relic_ids.append(calc.relic_tree['might'][4][5])
    relic_ids.append(calc.relic_tree['might'][4][6])

    thresholds['might 5.0'] = copy.deepcopy(relic_ids)

    
    relic_ids.append(5104) # 40% atk
    thresholds['might 5.1'] = copy.deepcopy(relic_ids)
    relic_ids.append(5205) # 43% atk
    thresholds['might 5.2'] = copy.deepcopy(relic_ids)
    # relic_ids.append(5204) # 38% atk
    relic_ids.append(5106) # 42% atk
    thresholds['might 5.4'] = copy.deepcopy(relic_ids)

    for r in calc.relic_tree['sustenance'][4]:
        if r:
            relic_ids.append(r)    
    thresholds['might 5.4 + sus 5.0'] = copy.deepcopy(relic_ids)

    for r in calc.relic_tree['fortitude'][4]:
        if r:
            relic_ids.append(r)
    # fort
    relic_ids.append(5202) # 24% atk
    relic_ids.append(5204) # 38% atk
    relic_ids.append(5205) # 43% atk
    relic_ids.append(5106) # 42% atk
    thresholds['might 5.4 + sus 5.0 + fort 5.4'] = copy.deepcopy(relic_ids)

    for r in calc.relic_tree['sorcery'][4]:
        if r:
            relic_ids.append(r)            
    
    # sorc
    relic_ids.append(5202) # 24% atk
    relic_ids.append(5404) # 28% atk
    relic_ids.append(5405) # 69% atk
    relic_ids.append(5406) # 47% atk
    thresholds['might 5.4 + sus 5.0 + fort 5.4 + sorc 5.4'] = copy.deepcopy(relic_ids)
    
    eph = 11472
    current_essence = 297450


    print("================================")
    print("PARAMETERS USED")
    print("================================")
    print(f"Current EPH = {eph} essence/h")
    print(f"Current Essence = {current_essence}")
    print(f"Current relics = {[name + ' ' +str(value)+'x' for name, value in have_lookup.items()]}")
    for k,v in thresholds.items():
        total_cost = calc.get_total_cost_for_multiple_relics(v, haves)
        num_hours = (total_cost-current_essence)/eph
        num_days = num_hours / 24
        print("================================")
        print(f"{k.upper()}")
        print("================================")
        print(f"Time taken = {round(num_hours, 2)} hours")
        print(f"Time taken = {round(num_days, 2)} days")

    pass
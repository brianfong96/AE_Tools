import csv

def get_relics():
    relics = list()
    with open('data/relics.tsv', 'r') as c:
            tsv_reader = csv.DictReader(c, delimiter='\t')
            for row in tsv_reader:
                relics.append(row)
    
    relic_dic = dict()
    look_up = dict()
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

def get_relic_tree():
    relics = list()
    with open('data/relic_tree.tsv', 'r') as c:
            tsv_reader = csv.DictReader(c, delimiter='\t')
            for row in tsv_reader:
                relics.append(row)
    
    tree = dict()
    for row in relics:        
        branch = row['Branch'].lower()
        level = int(row['Level'])
        relics = [None, int(row['Relic ID 1']), int(row['Relic ID 2']), int(row['Relic ID 3']), 
        int(row['Relic ID 4']), int(row['Relic ID 5']), int(row['Relic ID 6'])]
        
        if branch not in tree.keys():
            tree[branch] = dict()
        tree[branch][level] = relics

    return tree

def contains_relic(relics, want, have):
    components = relics[want]['components']

    if have in components:
        return True
    
    for component in components:
        if contains_relic(relics, component, have):
            return True
    
    return False


def get_total_cost(relics, want, haves = list()):
    
    essence = relics[want]['price']
    for have in haves:
        if contains_relic(relics, want, have):
            essence -= relics[have]['price']

    return essence

def get_relic_id(relic_tree, branch, level, relic_spot):
    if branch not in ['might', 'celerity', 'sustenance', 'fortitude', 'sorcery']:
        return -1
    return relic_tree[branch][level][relic_spot]

if __name__ == "__main__":
    relics, look_up = get_relics()
    relic_tree = get_relic_tree()
    
    test_id = 5504
    test_id = get_relic_id(relic_tree, 'might', 5, 2)
    test_relic = relics[test_id]    

    print(test_relic)

    print(get_total_cost(relics, test_id, [4505, 4506, 4405]))
    
    pass
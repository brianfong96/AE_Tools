import csv
import copy
import random
import math
from datetime import datetime

class calculator:

    def __init__(self, verbose=False):
        self.branches = ['might', 'celerity', 'sustenance', 'fortitude', 'sorcery']
        self.quality_id = {'Common':1, 'Rare':2, 'Elite':3, 'Legendary':4, 'Mythic':5}
        self.id_quality_to_relics = {1:[], 2:[], 3:[], 4:[], 5:[]}
        self.levels = [1, 2, 3 , 4, 5]
        self.verbose = verbose

        self.relics, self.look_up = self.get_relics()
        self.relic_tree = self.get_relic_tree()
        self.settlements = self.get_settlements()
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

            self.id_quality_to_relics[self.quality_id[relic['quality']]].append(relic['id'])

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

    def get_settlements(self):
        settlements = dict()
        with open('data/settlements.tsv', 'r') as c:
            tsv_reader = csv.DictReader(c, delimiter='\t')
            for row in tsv_reader:            
                s = {
                    'rarity':int(row['rarity']),
                    'cdr':int(row['cdr']),
                    'eph':int(row['eph']),
                    'bonus':float(row['bonus']),
                    }
                settlements[int(row['id'])] = s
        return settlements

    def create_all_components(self, relic):
        all_components = list()
        component_queue = copy.deepcopy(self.relics[relic]['components'])
        
        while len(component_queue) > 0:
            comp = component_queue.pop()
            for c in self.relics[comp]['components']:
                component_queue.append(c)
            all_components.append(comp)

        return all_components

    def get_total_cost_for_multiple_relics(self, wants, haves=list()):
        essence = 0
        for want in wants:
            if self.verbose:
                print("---------------------------------------------------")
                print(f"Getting cost for {self.relics[want]['name']}")
            cost, haves = self.get_total_cost(want, haves) 
            if self.verbose:
                print("---------------------------------------------------")
            essence += cost
        
        return essence, haves 

    def get_total_cost(self, want, haves = list()):        
        essence = self.relics[want]['total_cost']
        remain = list()
        all_components = self.create_all_components(want)
        for have in haves:
            if have in all_components:
                if self.verbose:
                    print(f"{self.relics[have]['name']} used in {self.relics[want]['name']}")
                essence -= self.relics[have]['total_cost']
                all_components.remove(have)
            else:
                remain.append(have)

        return essence, remain

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

    def get_eph(self, cult, uncult):
        eph = 0
        for cult_id, count in cult.items():
            eph += self.settlements[cult_id]['eph'] * self.settlements[cult_id]['bonus'] * count
        
        for uncult_id, count in uncult.items():
            eph += self.settlements[uncult_id]['eph']* count            

        return eph

    def get_relic_drops(self, settlements, seconds):
        relics = list()
        for settlement, count in settlements.items():
            relic_rarity_id = self.settlements[settlement]['rarity']
            drop_cdr = self.settlements[settlement]['cdr']
            drops = math.floor(count * seconds / drop_cdr) 

            for i in range(drops):
                relics.append(random.choice(self.id_quality_to_relics[relic_rarity_id]))

        return relics

    def calculate(self, relic_ids, have_lookup, thresholds, 
    cultivated_settlements, uncultivated_settlements, settlements, 
    eph, current_essence, name):   
        haves = list()
        for r, num in have_lookup.items():
            for i in range(num):
                haves.append(self.look_up[r])     

        settled_eph = int(self.get_eph(cultivated_settlements, uncultivated_settlements))

        print("================================================================")
        print("Resources")
        print("================================================================")
        if eph != settled_eph:
            "Discrepencies between given eph, and eph calculated from settlements"
            return
        print(f"{name} - {datetime.now()}")
        print(f"Current EPH = {eph} essence/h")
        print(f"Current Essence = {current_essence}")
        print(f"Current relics = {[name + ' ' +str(value)+'x' for name, value in have_lookup.items()]}")
        for k,v in thresholds.items():
            print("================================================================")
            print(f"Hitting {k.upper()}")
            print("================================================================")

            total_cost, remains_no_relic = self.get_total_cost_for_multiple_relics(v, haves)
            num_hours = (total_cost-current_essence)/eph
            num_days = num_hours / 24        
            print(f"Time taken (Without Relic Drops) = {round(num_hours, 2)} hours")
            print(f"Time taken (Without Relic Drops) = {round(num_days, 2)} days")

            if self.verbose:
                print(f"Relics not used = {[self.relics[name]['name'] for name in remains_no_relic]}")

            sold_essence = sum([self.relics[relic]['total_cost']*.4 for relic in remains_no_relic])
            total_cost, remains_no_relic = self.get_total_cost_for_multiple_relics(v, haves)
            num_hours = (total_cost-(current_essence+sold_essence))/eph
            num_days = num_hours / 24               
            print(f"Time taken (Without Relic Drops & Selling Unused Relics) = {round(num_hours, 2)} hours")
            print(f"Time taken (Without Relic Drops & Selling Unused Relics) = {round(num_days, 2)} days")

            num_seconds = num_hours * 3600 * 0.5
            relic_drops = self.get_relic_drops(settlements, num_seconds)
            total_cost, remains_no_relic = self.get_total_cost_for_multiple_relics(v, haves+relic_drops)
            num_hours = (total_cost-current_essence)/eph
            num_days = num_hours / 24    
            print(f"Time taken (With Relic Drops after {round(num_seconds/3600, 2)} hours) ~= {round(num_hours, 2)} hours")
            print(f"Time taken (With Relic Drops after {round(num_seconds/3600, 2)} hours) ~= {round(num_days, 2)} days")

            if self.verbose:
                print(f"Relics not used = {[self.relics[name]['name'] for name in remains_no_relic]}")

            sold_essence = sum([self.relics[relic]['total_cost']*.4 for relic in remains_no_relic])
            total_cost, remains_no_relic = self.get_total_cost_for_multiple_relics(v, haves+relic_drops)
            num_hours = (total_cost-(current_essence+sold_essence))/eph
            num_days = num_hours / 24               
            print(f"Time taken (With Relic Drops after {round(num_seconds/3600, 2)} hours & Selling Unused Relics) ~= {round(num_hours, 2)} hours")
            print(f"Time taken (With Relic Drops after {round(num_seconds/3600, 2)} hours & Selling Unused Relics) ~= {round(num_days, 2)} days")            


#============================================
# Voiren
#============================================
    def calculate_voiren(self):
        relic_ids = list()
        haves = list()

        have_lookup = {}
        have_lookup = {
            "Veil of Silence": 1, 
            "Valor's Core": 2, 
            "Noble Blade": 1,
            "The Wall": 2,
            "Rambler's Boots": 1,
            "Immortal's Crown": 1,
            "Kuilin Ring": 1,
            "Wisdom's Core": 1,
            "Immortal's Cinctures": 1,
            "Immortal's Crown": 1,
            "Blitz Arc": 2,
            "Cathedral Censer": 3,
            "Noble Blade": 2,
            "Admonition": 1
        }        

        for r, num in have_lookup.items():
            for i in range(num):
                haves.append(self.look_up[r])

        thresholds = dict()

        relic_ids.append(self.look_up["Mercy and Malice"])
        relic_ids.append(self.look_up["Star Of Valor"])

        thresholds['might 5.4'] = copy.deepcopy(relic_ids)    

        for r in self.relic_tree['fortitude'][4]:
            if r:
                relic_ids.append(r)

        thresholds['might 5.4 + fort 5.0'] = copy.deepcopy(relic_ids)    

        # fort
        relic_ids.append(5202) # 24% atk
        relic_ids.append(5204) # 38% atk
        relic_ids.append(5205) # 43% atk
        relic_ids.append(5106) # 42% atk
        thresholds['might 5.4 + fort 5.4'] = copy.deepcopy(relic_ids)

        for r in self.relic_tree['sustenance'][4]:
            if r:
                relic_ids.append(r)
        thresholds['might 5.4 + fort 5.4 + sus 5.0'] = copy.deepcopy(relic_ids)

        for r in self.relic_tree['sorcery'][4]:
            if r:
                relic_ids.append(r)            
        
        # sorc
        relic_ids.append(5202) # 24% atk
        relic_ids.append(5404) # 28% atk
        relic_ids.append(5405) # 69% atk
        relic_ids.append(5406) # 47% atk
        thresholds['might 5.4 + fort 5.4 + sus 5.0 + sorc 5.4'] = copy.deepcopy(relic_ids)
        
        cultivated_settlements = {7:6, 6:27, 5:6}        
        uncultivated_settlements = {204:1}
        settlements = {7:6, 6:27, 5:6, 204:1}        

        settled_eph = int(self.get_eph(cultivated_settlements, uncultivated_settlements))
        eph = 11412
        current_essence = 338578

        print("================================================================")
        print("Resources")
        print("================================================================")
        if eph != settled_eph:
            "Discrepencies between given eph, and eph calculated from settlements"
            return
        print(f"Voiren - {datetime.now()}")
        print(f"Current EPH = {eph} essence/h")
        print(f"Current Essence = {current_essence}")
        print(f"Current relics = {[name + ' ' +str(value)+'x' for name, value in have_lookup.items()]}")
        for k,v in thresholds.items():
            print("================================================================")
            print(f"Hitting {k.upper()}")
            print("================================================================")

            total_cost, remains_no_relic = self.get_total_cost_for_multiple_relics(v, haves)
            num_hours = (total_cost-current_essence)/eph
            num_days = num_hours / 24        
            print(f"Time taken (Without Relic Drops) = {round(num_hours, 2)} hours")
            print(f"Time taken (Without Relic Drops) = {round(num_days, 2)} days")

            if True:
                print(f"Relics not used = {[self.relics[name]['name'] for name in remains_no_relic]}")

            sold_essence = sum([self.relics[relic]['total_cost']*.4 for relic in remains_no_relic])
            total_cost, remains_no_relic = self.get_total_cost_for_multiple_relics(v, haves)
            num_hours = (total_cost-(current_essence+sold_essence))/eph
            num_days = num_hours / 24               
            print(f"Time taken (Without Relic Drops & Selling Unused Relics) = {round(num_hours, 2)} hours")
            print(f"Time taken (Without Relic Drops & Selling Unused Relics) = {round(num_days, 2)} days")

            num_seconds = num_hours * 3600 * 0.5
            relic_drops = self.get_relic_drops(settlements, num_seconds)
            total_cost, remains_no_relic = self.get_total_cost_for_multiple_relics(v, haves+relic_drops)
            num_hours = (total_cost-current_essence)/eph
            num_days = num_hours / 24    
            print(f"Time taken (With Relic Drops after {round(num_seconds/3600, 2)} hours) ~= {round(num_hours, 2)} hours")
            print(f"Time taken (With Relic Drops after {round(num_seconds/3600, 2)} hours) ~= {round(num_days, 2)} days")

            if self.verbose:
                print(f"Relics not used = {[self.relics[name]['name'] for name in remains_no_relic]}")

            sold_essence = sum([self.relics[relic]['total_cost']*.4 for relic in remains_no_relic])
            total_cost, remains_no_relic = self.get_total_cost_for_multiple_relics(v, haves+relic_drops)
            num_hours = (total_cost-(current_essence+sold_essence))/eph
            num_days = num_hours / 24               
            print(f"Time taken (With Relic Drops after {round(num_seconds/3600, 2)} hours & Selling Unused Relics) ~= {round(num_hours, 2)} hours")
            print(f"Time taken (With Relic Drops after {round(num_seconds/3600, 2)} hours & Selling Unused Relics) ~= {round(num_days, 2)} days")            

#============================================
# Shisha
#============================================
    def calculate_shisha(self):
        relic_ids = list()
        haves = list()

        have_lookup = {}
        have_lookup = { 
            "Valor's Core": 2, 
            "Noble Blade": 2,
            "The Wall": 3,
            "Determination's Core": 2,
            "Immortal's Crown": 2,
            "Wisdom's Core": 1,
            "Immortal's Cinctures": 1,
            "Blitz Arc": 2,
            "Admonition": 1,
        }        

        for r, num in have_lookup.items():
            for i in range(num):
                haves.append(self.look_up[r])

        thresholds = dict()

        # sorc
        relic_ids.append(self.relic_tree['sorcery'][4][4])
        relic_ids.append(self.relic_tree['sorcery'][4][5])
        relic_ids.append(self.relic_tree['sorcery'][4][1])         
        relic_ids.append(5202) # 24% atk
        relic_ids.append(5404) # 28% atk
        relic_ids.append(5405) # 69% atk
        relic_ids.append(5406) # 47% atk
        thresholds['sorc 5.4'] = copy.deepcopy(relic_ids)

        # might
        relic_ids.append(self.relic_tree['might'][3][3])
        for r in self.relic_tree['might'][4]:
            if r:
                relic_ids.append(r)
        relic_ids.append(self.look_up["Diligence"])
        relic_ids.append(self.look_up["Master's Claw"])
        relic_ids.append(self.look_up["Mercy and Malice"])
        relic_ids.append(self.look_up["Star Of Valor"])
        thresholds['sorc 5.4 + might 5.4'] = copy.deepcopy(relic_ids)    

        # sus
        relic_ids.append(self.relic_tree['sustenance'][4][2])
        relic_ids.append(self.relic_tree['sustenance'][4][4])
        relic_ids.append(self.relic_tree['sustenance'][4][5])
        relic_ids.append(self.relic_tree['sustenance'][4][6])
        thresholds['sorc 5.4 + might 5.4 + Sus 5.0'] = copy.deepcopy(relic_ids)    

        # fort
        relic_ids.append(self.relic_tree['fortitude'][3][2])
        relic_ids.append(self.relic_tree['fortitude'][3][3])
        relic_ids.append(self.relic_tree['fortitude'][3][4])  
        for r in self.relic_tree['fortitude'][4]:
            if r:
                relic_ids.append(r)
        relic_ids.append(5202) # 24% atk
        relic_ids.append(5204) # 38% atk
        relic_ids.append(5205) # 43% atk
        relic_ids.append(5106) # 42% atk
        thresholds['sorc 5.4 + might 5.4 + sus 5.0 + fort 5.4'] = copy.deepcopy(relic_ids)
        
        # cultivated_settlements = {7:2, 6:9, 5:25}        
        # uncultivated_settlements = {204:3, 203:1}
        # settlements = {7:1, 6:9, 5:25, 204:3, 203:1}        

        # settled_eph = int(self.get_eph(cultivated_settlements, uncultivated_settlements))
        # eph = 9628 + 280*1.2
        # current_essence = 173469

        cultivated_settlements = {7:6, 6:27, 5:6}        
        uncultivated_settlements = {204:1}
        settlements = {7:6, 6:27, 5:6, 204:1}        

        settled_eph = int(self.get_eph(cultivated_settlements, uncultivated_settlements))
        eph = 11412
        current_essence = 173469

        print("================================================================")
        print("Resources")
        print("================================================================")        
        if eph != settled_eph:
            print(f"{eph} != {settled_eph}")
            return
        print(f"Shisha - {datetime.now()}")
        print(f"Current EPH = {eph} essence/h")
        print(f"Current Essence = {current_essence}")
        print(f"Current relics = {[name + ' ' +str(value)+'x' for name, value in have_lookup.items()]}")
        for k,v in thresholds.items():
            print("================================================================")
            print(f"Hitting {k.upper()}")
            print("================================================================")

            total_cost, remains_no_relic = self.get_total_cost_for_multiple_relics(v, haves)
            num_hours = (total_cost-current_essence)/eph
            num_days = num_hours / 24        
            print(f"Time taken (Without Relic Drops) = {round(num_hours, 2)} hours")
            print(f"Time taken (Without Relic Drops) = {round(num_days, 2)} days")

            if self.verbose:
                print(f"Relics not used = {[self.relics[name]['name'] for name in remains_no_relic]}")

            sold_essence = sum([self.relics[relic]['total_cost']*.4 for relic in remains_no_relic])
            total_cost, remains_no_relic = self.get_total_cost_for_multiple_relics(v, haves)
            num_hours = (total_cost-(current_essence+sold_essence))/eph
            num_days = num_hours / 24               
            print(f"Time taken (Without Relic Drops & Selling Unused Relics) = {round(num_hours, 2)} hours")
            print(f"Time taken (Without Relic Drops & Selling Unused Relics) = {round(num_days, 2)} days")

            num_seconds = num_hours * 3600 * 0.5
            relic_drops = self.get_relic_drops(settlements, num_seconds)
            total_cost, remains_no_relic = self.get_total_cost_for_multiple_relics(v, haves+relic_drops)
            num_hours = (total_cost-current_essence)/eph
            num_days = num_hours / 24    
            print(f"Time taken (With Relic Drops after {round(num_seconds/3600, 2)} hours) ~= {round(num_hours, 2)} hours")
            print(f"Time taken (With Relic Drops after {round(num_seconds/3600, 2)} hours) ~= {round(num_days, 2)} days")

            if self.verbose:
                print(f"Relics not used = {[self.relics[name]['name'] for name in remains_no_relic]}")

            sold_essence = sum([self.relics[relic]['total_cost']*.4 for relic in remains_no_relic])
            total_cost, remains_no_relic = self.get_total_cost_for_multiple_relics(v, haves+relic_drops)
            num_hours = (total_cost-(current_essence+sold_essence))/eph
            num_days = num_hours / 24               
            print(f"Time taken (With Relic Drops after {round(num_seconds/3600, 2)} hours & Selling Unused Relics) ~= {round(num_hours, 2)} hours")
            print(f"Time taken (With Relic Drops after {round(num_seconds/3600, 2)} hours & Selling Unused Relics) ~= {round(num_days, 2)} days")            


def sanity_check(calc):
    ids = [5506]
    haves = [4506]
    print(f"relic total cost alone is {calc.relics[5506]}")
    print(f"relic total cost with function is {calc.get_total_cost_for_multiple_relics(ids)}")
    print(f"relic total cost with function and have = {haves} is {calc.get_total_cost_for_multiple_relics(ids, haves)}")
    haves.append(4506)
    print(f"relic total cost with function and have = {haves} is {calc.get_total_cost_for_multiple_relics(ids, haves)}")
    haves.append(4506)
    print(f"relic total cost with function and have = {haves} is {calc.get_total_cost_for_multiple_relics(ids, haves)}")
    haves.append(4506)
    print(f"relic total cost with function and have = {haves} is {calc.get_total_cost_for_multiple_relics(ids, haves)}")
if __name__ == "__main__":
    verbose = False
    calc = calculator(verbose)
    calc.calculate_voiren()
    # print(calc.settlements)
    # sanity_check(calc)


    pass
import pandas as pd
import random
import copy
import matplotlib.pyplot as plt


LIMIT_WEIGHT = 10
LIMIT_VALUE = 12
LIMIT_RANGE_SNACKS = [2,4]
CHROMOSOME_POPULATION = 30
NUMBER_OF_GENERATIONS = 300
PC = [0] * 50 + [1] * 50
PM = [0] * 800 + [1] * 10
PN = [0] * 50 + [1] * 10
BOUNUS_SIZE = 10
GENS = []
SNACKS = pd.read_csv('snacks.csv')
SNACKS.reset_index(inplace=True)
SNACKS['value/weight'] = SNACKS['Value'] / SNACKS['Available Weight'] * BOUNUS_SIZE
SNACKS = SNACKS.sort_values(by='value/weight')
sorted_index = SNACKS.index
# SNACKS = SNACKS.loc[sorted_index]
NUMBER_OF_SNACKS = SNACKS['index'].idxmax()
PROBABILITY_NONE = 3
DECREASE_POINT_WEIGHT = 100
DECREASE_POINT_VALUE = 100
DECREASE_POINT_SIZE = 100

print(SNACKS)



def generate_first_generation(snacks) :
    gens = []
    for i in range(CHROMOSOME_POPULATION) :
        new_gen = []
        index_snacks = [a for a in range(0 , NUMBER_OF_SNACKS + 1 + PROBABILITY_NONE)]
        
        while (len(new_gen) < LIMIT_RANGE_SNACKS[1]) :
            pick_random_snack = random.choice(index_snacks)
            index_snacks.remove(pick_random_snack)
            
            if pick_random_snack <= NUMBER_OF_SNACKS :
                new_snack = []
                
                new_snack_weight = snacks.loc[pick_random_snack , 'Available Weight']
                pick_random_weight = random.uniform(0.01 , new_snack_weight)
                pick_random_weight = round(pick_random_weight , 2)
                new_snack_value = snacks.loc[pick_random_snack , 'Value']
                pick_snack_value = new_snack_value * pick_random_weight / new_snack_weight
                pick_snack_value = round(pick_snack_value , 2)
                
                new_snack.append(pick_random_snack)
                new_snack.append(pick_random_weight)
                new_snack.append(pick_snack_value)
                
                new_gen.append(new_snack)
                
            else :
                new_gen.append(None)

        new_gen.append(None) ### for weight  
        new_gen.append(None) ### for value  
        new_gen.append(None) ### for fitness
        gens.append(new_gen)
    
    return gens

GENS = generate_first_generation(SNACKS)



def fitness_function(gens) :
    
    for i in range(CHROMOSOME_POPULATION) :
        fitness_score = 0
        total_gen_weight = 0
        total_gen_value = 0
        size_gen = LIMIT_RANGE_SNACKS[1] ########## metod 2
        bounus = 0
        
        #############################################
        # for j in range(LIMIT_RANGE_SNACKS[1]) :
            
        #     if gens[i][j] == None :
        #         size_gen = size_gen - 1
        #         continue
        #     else :
        #         total_gen_weight += gens[i][j][1]
        #         total_gen_value += gens[i][j][2]
        #         bounus += SNACKS.loc[gens[i][j][0] , 'value/weight'] * gens[i][j][1] * gens[i][j][2]
                
        # checker_weight = LIMIT_WEIGHT - total_gen_weight
        # if checker_weight < 0 :
        #     checker_weight -= DECREASE_POINT_WEIGHT
        # else : ######### metod 2
        #     checker_weight = total_gen_weight
            
        # checker_value = total_gen_value - LIMIT_VALUE
        # if checker_value < 0 :
        #     checker_value -= DECREASE_POINT_VALUE
        # else : ######### metod 2
        #     checker_value = total_gen_value
        
        # checker_size = size_gen - LIMIT_RANGE_SNACKS[0]
        # if checker_size < 0 : ######## metod 3
        #     checker_size -= DECREASE_POINT_SIZE
        # else :
        #     checker_size = 0
            
        # if checker_weight < 0 or checker_value < 0 or checker_size < 0 :
        #     fitness_score = checker_weight + checker_value + checker_size
        # else :
        #     fitness_score = checker_weight + checker_value + checker_size + bounus
            
        
        
        
        for j in range(LIMIT_RANGE_SNACKS[1]) :
            
            if gens[i][j] == None :
                size_gen = size_gen - 1
                continue
            
            else :
                total_gen_weight += gens[i][j][1]
                total_gen_value += gens[i][j][2]
                
        checker_weight = LIMIT_WEIGHT - total_gen_weight
        if checker_weight < 0 :
            checker_weight -= DECREASE_POINT_WEIGHT
        else : ######### metod 2
            checker_weight = total_gen_weight
            
        checker_value = total_gen_value - LIMIT_VALUE
        if checker_value < 0 :
            checker_value -= DECREASE_POINT_VALUE
        else : ######### metod 2
            checker_value = total_gen_value
        
        checker_size = size_gen - LIMIT_RANGE_SNACKS[0]
        if checker_size < 0 : ######## metod 3
            checker_size -= DECREASE_POINT_SIZE
        else :
            checker_size = 0
            
        fitness_score = checker_weight + checker_value + checker_size
        
        ########################################
        # if checker_weight < 0 and checker_value < 0:
        #    fitness_score = checker_weight * checker_value * -1
        # else :
        #     fitness_score = checker_weight * checker_value
        
        # if checker_size < 0 :
        #     if fitness_score > 0 :
        #         fitness_score *= -1
        #     else :
        #         pass
        #######################################
        
        ########################################
        # fitness_score = checker_weight + checker_value
        ########################################
        
        gens[i][LIMIT_RANGE_SNACKS[1]] = checker_weight
        gens[i][LIMIT_RANGE_SNACKS[1] + 1] = checker_value
        gens[i][LIMIT_RANGE_SNACKS[1] + 2] = fitness_score
    
    return gens


GENS = fitness_function(GENS)
GENS = sorted(GENS , key=lambda x : x[LIMIT_RANGE_SNACKS[1] + 2])
print(GENS[-1])


def cross_over(gen1 , gen2) :
    for i in range(LIMIT_RANGE_SNACKS[1]) :
        get_cross = random.choice(PC)
        if get_cross == 1 :
            if gen1[i] == None:
                for j in range(LIMIT_RANGE_SNACKS[1]) :
                    if gen1[j] == None or gen2[i] == None :
                        continue
                    if gen2[i][0] == gen1[j][0] :
                        gen1[j] , gen2[i] = gen2[i] , gen1[j]
                        break
                else :
                    gen1[i] , gen2[i] = gen2[i] , gen1[i]

                continue
            else :
                flag = True
                for l in range(LIMIT_RANGE_SNACKS[1]) :
                    if gen2[l] == None or gen1[i] == None:
                        continue
                    if gen2[l][0] == gen1[i][0] :
                        gen2[l] , gen1[i] = gen1[i] , gen2[l]
                        flag = False
                        break
                
                for o in range(LIMIT_RANGE_SNACKS[1]) :
                    if gen1[o] == None or gen2[i] == None :
                        continue
                    if gen1[o][0] == gen2[i][0] :
                        gen1[o] , gen2[i] = gen2[i] , gen1[o]
                        flag = False
                        
                if flag == True :
                    gen2[i] , gen1[i] = gen1[i] , gen2[i]
                    
    return gen1 , gen2



def mutation(gen) :
    
    for i in range(LIMIT_RANGE_SNACKS[1]) :
        get_mutation = random.choice(PM)
        if get_mutation == 1 :
            if gen[i] == None :
                snacks_in_gen = []
                #################################################
                for h in range(LIMIT_RANGE_SNACKS[1]) :
                    if gen[h] == None :
                        continue
                    else :
                        snacks_in_gen.append(gen[h][0])
                        
                all_snack = copy.copy(sorted_index)
                removed_reapet_snack = [snack for snack in all_snack if snack not in snacks_in_gen]
                random_get_snack = removed_reapet_snack[-1]
                
                new_snack = []
                max_snack_weight = SNACKS.loc[random_get_snack , 'Available Weight']
                snack_weight = random.uniform(0.01 , max_snack_weight)
                snack_weight = round(snack_weight , 2)
                
                max_snack_value = SNACKS.loc[random_get_snack , 'Value']
                snack_value = max_snack_value * snack_weight / max_snack_weight
                snack_value = round(snack_value , 2)
                
                new_snack.append(random_get_snack)
                new_snack.append(snack_weight)
                new_snack.append(snack_value)
                
                gen[i] = new_snack
                ##################################################
            else :
                get_mutation_n = random.choice(PN)
                if get_mutation_n == 0 :
                    temp_list = []
                    for h in range(LIMIT_RANGE_SNACKS[1]) :
                        if gen[h] == None :
                            continue
                        else :
                            temp_list.append(gen[h][0])

                    temp_list.remove(gen[i][0])

                    all_snack = copy.copy(sorted_index)
                    removed_reapet_snack = [snack for snack in all_snack if snack not in temp_list]
                    gen[i][0] = removed_reapet_snack[-1]

                    max_snack_weight = SNACKS.loc[gen[i][0] , 'Available Weight']
                    snack_weight = random.uniform(0.01 , max_snack_weight)
                    snack_weight = round(snack_weight , 2)

                    max_snack_value = SNACKS.loc[gen[i][0] , 'Value']
                    snack_value = max_snack_value * snack_weight / max_snack_weight
                    snack_value = round(snack_value , 2)


                    gen[i][1] = snack_weight
                    gen[i][2] = snack_value    
                else :
                    gen[i] = None
    return gen   
    
    
    # for i in range(LIMIT_RANGE_SNACKS[1]) :
    #     get_mutation = random.choice(PM)
    #     if get_mutation == 1 :
    #         if gen[i] == None :
    #             snacks_in_gen = []
    #             #################################################
    #             for h in range(LIMIT_RANGE_SNACKS[1]) :
    #                 if gen[h] == None :
    #                     continue
    #                 else :
    #                     snacks_in_gen.append(gen[h][0])
                        
    #             all_snack = copy.copy(sorted_index)
    #             removed_reapet_snack = [snack for snack in all_snack if snack not in snacks_in_gen]
    #             random_get_snack = removed_reapet_snack[-1]
                
    #             new_snack = []
    #             max_snack_weight = SNACKS.loc[random_get_snack , 'Available Weight']
    #             snack_weight = random.uniform(0.01 , max_snack_weight)
    #             snack_weight = round(snack_weight , 2)
                
    #             max_snack_value = SNACKS.loc[random_get_snack , 'Value']
    #             snack_value = max_snack_value * snack_weight / max_snack_weight
    #             snack_value = round(snack_value , 2)
                
    #             new_snack.append(random_get_snack)
    #             new_snack.append(snack_weight)
    #             new_snack.append(snack_value)
                
    #             gen[i] = new_snack
    #             ##################################################
    #         else :
    #             temp_list = []
    #             for h in range(LIMIT_RANGE_SNACKS[1]) :
    #                 if gen[h] == None :
    #                     continue
    #                 else :
    #                     temp_list.append(gen[h][0])
                
    #             all_snack = copy.copy(sorted_index)
    #             removed_reapet_snack = [snack for snack in all_snack if snack not in temp_list]
    #             gen[i][0] = removed_reapet_snack[-1]
                
    #             max_snack_weight = SNACKS.loc[gen[i][0] , 'Available Weight']
    #             snack_weight = random.uniform(0.01 , max_snack_weight)
    #             snack_weight = round(snack_weight , 2)
                
    #             max_snack_value = SNACKS.loc[gen[i][0] , 'Value']
    #             snack_value = max_snack_value * snack_weight / max_snack_weight
    #             snack_value = round(snack_value , 2)
                
                
    #             gen[i][1] = snack_weight
    #             gen[i][2] = snack_value
                
    # return gen   
    
    
    
    
    # for i in range(LIMIT_RANGE_SNACKS[1]) :
    #     get_mutation = random.choice(PM)
    #     if get_mutation == 1 :
    #         if gen[i] == None :
    #             snacks_in_gen = []
    #             #################################################
    #             for h in range(LIMIT_RANGE_SNACKS[1]) :
    #                 if gen[h] == None :
    #                     continue
    #                 else :
    #                     snacks_in_gen.append(gen[h][0])
                        
    #             all_snack = [r for r in range(0,NUMBER_OF_SNACKS + 1)]
    #             removed_reapet_snack = [snack for snack in all_snack if snack not in snacks_in_gen]
    #             random_get_snack = random.choice(removed_reapet_snack)
                
    #             new_snack = []
    #             max_snack_weight = SNACKS.loc[random_get_snack , 'Available Weight']
    #             snack_weight = random.uniform(0.01 , max_snack_weight)
    #             snack_weight = round(snack_weight , 2)
                
    #             max_snack_value = SNACKS.loc[random_get_snack , 'Value']
    #             snack_value = max_snack_value * snack_weight / max_snack_weight
    #             snack_value = round(snack_value , 2)
                
    #             new_snack.append(random_get_snack)
    #             new_snack.append(snack_weight)
    #             new_snack.append(snack_value)
                
    #             gen[i] = new_snack
    #             ##################################################
    #         else :
    #             max_snack_weight = SNACKS.loc[gen[i][0] , 'Available Weight']
                 
    #             ##################################################
    #             random_snack_weight = random.uniform(0.01 , max_snack_weight)
    #             snack_weight = round(random_snack_weight , 2)
    #             gen[i][1] = snack_weight
    #             ##################################################
    #             ##################################################
    #             # if max_snack_weight - gen[i][1] >= 2:
    #             #     gen[i][1] += 2
    #             # else :
    #             #     snack_weight = round(max_snack_weight - gen[i][1] , 2)
    #             #     gen[i][1] = snack_weight
    #             ###################################################
    #             ###################################################
    #             # if max_snack_weight - gen[i][1] > 0 :
    #             #     gen[i][1] = max_snack_weight
    #             # else :
    #             #     gen[i][1] = round(max_snack_weight - gen[i][1] , 2)
                
    #             # if max_snack_weight - gen[i][1] > 0 :
    #             #     gen[i][1] = max_snack_weight
    #             # else :
                    
    #             #     gen[i][1] = round(max_snack_weight - gen[i][1] + 1 , 2)
    #             ###################################################
                
    #             max_snack_value = SNACKS.loc[gen[i][0] , 'Value']
    #             snack_value = max_snack_value * gen[i][1] / max_snack_weight
    #             snack_value = round(snack_value , 2)
    #             gen[i][2] = snack_value
                
    # return gen   
                
                
best = [[0 ,0  ,0 ,0 ,0 ,0 , 0] , 0]
plot = []
num = []

for i in range(NUMBER_OF_GENERATIONS) :
    
    
    #############################################
    list = []
    for p in range(len(GENS)) :
        list.append(GENS[p][LIMIT_RANGE_SNACKS[1] + 2])
    average = sum(list) / len(list)
    plot.append(average)
    ##############################################
    list1 = []
    for p in range(len(GENS)) :
        if GENS[p][LIMIT_RANGE_SNACKS[1] + 2] > 0 :
            list1.append(GENS[p][LIMIT_RANGE_SNACKS[1] + 2])
            
    n = len(list1)
    num.append(n)


    GENS = sorted(GENS , key=lambda x : x[LIMIT_RANGE_SNACKS[1] + 2])
    
    # print(GENS[-1] , i)
    if GENS[-1][LIMIT_RANGE_SNACKS[1] + 1] > best[0][LIMIT_RANGE_SNACKS[1] + 1] and GENS[-1][LIMIT_RANGE_SNACKS[1]] > 0:
        best[0] = copy.deepcopy(GENS[-1])
        best[1] = i
    
        
    for j in range(0 , CHROMOSOME_POPULATION , 2) :
        GENS[j] , GENS[j + 1] = cross_over(GENS[j] , GENS[j + 1])

    for k in range(CHROMOSOME_POPULATION) :
        GENS[k] = mutation(GENS[k])
        
    
    GENS = fitness_function(GENS)
    
    
    
    
    
GENS = sorted(GENS , key=lambda x : x[LIMIT_RANGE_SNACKS[1] + 2])

# print(GENS[-1])
# print('best' , best)
for i in range(LIMIT_RANGE_SNACKS[1]) :
    if best[0][i] == None :
        continue
    else :
        print(SNACKS.loc[best[0][i][0] , 'Snack'] , ': ' , best[0][i][1] , sep='')
print('Total Weight: ' , best[0][LIMIT_RANGE_SNACKS[1]] , sep='')
print('Total Value: ' , best[0][LIMIT_RANGE_SNACKS[1] + 1] , sep='')

print("#############################################")
for i in range(LIMIT_RANGE_SNACKS[1]) :
    if GENS[-1][i] == None :
        continue
    else :
        print(SNACKS.loc[GENS[-1][i][0] , 'Snack'] , ': ' , GENS[-1][i][1] , sep='')
print('Total Weight: ' , GENS[-1][LIMIT_RANGE_SNACKS[1]] , sep='')
print('Total Value: ' , GENS[-1][LIMIT_RANGE_SNACKS[1] + 1] , sep='')
    
plt.plot(num)
plt.xlabel('Iteration')
plt.ylabel('accept')
plt.title('accept of Random Lists for 300 Iterations')
plt.show()



# coding: utf-8

import itertools

# # Optimizing the travelling salesman problem : brute force, then gluton, then backtracking

# ## 1. Useful functions

# ### Example of ravelling salesman Matrix


errands = {
    'H': {'H': 0,'P': 36,'G': 32,'C': 54,'D': 20,'T': 40},
    'P': {'H': 36,'P': 0,'G': 22,'C': 54,'D': 84,'T': 67},
    'G': {'H': 32,'P': 22,'G': 0,'C': 36,'D': 42,'T': 71},
    'C': {'H': 54,'P': 54,'G': 36,'C': 0,'D': 50,'T': 92},
    'D': {'H': 20,'P': 84,'G': 42,'C': 50,'D': 0,'T': 45},
    'T': {'H': 40,'P': 67,'G': 71,'C': 92,'D': 45,'T': 0}
}


def lib_force(tab) :
    min_size = 10000000
    min_path = []
    perm_list = list(itertools.permutations(tab.keys()))
    for perm in perm_list :
        somme = 0
        for i in range(len(perm)) :
            if(i>0) :
                somme += tab[perm[i-1]][perm[i]]
        # Revenir au début
        somme += tab[perm[-1]][perm[0]]
        if somme < min_size :
            min_size = somme
            min_path = perm
    return{"way" : min_path, "length" : min_size}
    
import time
start_time = time.time()
print(lib_force(errands))
print("--- %s seconds ---" % (time.time() - start_time))


# ### Generate randomly a travelling salesman matrix

def random_matrix(size) :
    matrix = dict()
    letters ='ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    keylist = set()
    while len(keylist)<size :
        keylist.add(random.choice(letters))
    
    filled = set()
    for letter in keylist :
        matrix[letter] = dict()
    
    for letter in keylist :
        filled.add(letter)
        matrix[letter][letter] = 0
        for l in keylist - filled :
            value = random.randint(10,100)
            matrix[letter][l] = value
            matrix[l][letter] = value
            
        
    return matrix


# Test
rand = random_matrix(13)
print(rand)


big = random_matrix(17)


# ### Gluton algorithm : for every point, get the closest next point

def glouton(tab) :
    current_shortest_way = {'path' : '', 'length' : 10000000}
    
    for index_letter in tab :
        current_letter = index_letter
        shortest_way_line = {'path' : '', 'length' : 0}
    
        # For every line, we search hte shortest path by taken for a letter -> closest letter
        while(len(shortest_way_line['path']) < len(tab.keys())) :
            next_letter = ''
            min_length = 10000000
            # Pour une lettre donnée current_letter, cherche la lettre la plus proche
            for letter in tab[current_letter] :
                if letter not in shortest_way_line['path'] and tab[current_letter][letter] < min_length :
                    next_letter = letter
                    min_length = tab[current_letter][letter]
                    
            shortest_way_line['path'] += next_letter
            shortest_way_line['length'] += min_length
            current_letter = next_letter
        
        if shortest_way_line['length'] < current_shortest_way['length'] :
            current_shortest_way = shortest_way_line
            
    # Back to first step
    current_shortest_way['length'] += tab[current_shortest_way['path'][-1]][current_shortest_way['path'][0]]
            
    return current_shortest_way

# Test

start_time = time.time()
print(glouton(errands))
print("--- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
print(glouton(rand))
print("--- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
print(glouton(big))
print("--- %s seconds ---" % (time.time() - start_time))


# ### Simple Backtracking

def backtracking_simple(tab) :
    best_length = glouton(tab)['length']
    first_elem = choice(list(tab.keys()))
    
    return rec_backtracking_simple(tab, [first_elem], best_length, 0, set(tab.keys()) - {first_elem})

    
def rec_backtracking_simple(matrix, way, best_length, curr_length, restants) :
    if not restants :
        # Fin de chemin : on rajoute longueur du dernier au premier
        return (way, curr_length + matrix[way[-1]][way[0]])
    
    if curr_length > best_length :
        return (False, False)
        
    best_way = []
    for n in restants :
        (way_n, length_n) = rec_backtracking_simple(matrix, way + [n], best_length, curr_length + matrix[way[-1]][n], restants - {n})
        if length_n :
            if length_n <= best_length :
                best_length = length_n
                best_way = way_n
    
    if len(best_way) > 0 :
        return (best_way, best_length)
    else :
        return (False, False)


# Test

start_time = time.time()
print(backtracking_simple(errands))
print("--- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
print(backtracking_simple(rand))
print("--- %s seconds ---" % (time.time() - start_time))

# The execution time is higher than gluton, but lower than brute force. This algorithm gives therefore an optimal result (contrary to gluton) while still improving time performance.

# ## Backtracking with heuristics

# ### 1. Backtracking with closest neighbour method

def backtracking_closest_neighbour(tab):
    best_length = glouton(tab)['length']
    first_elem = choice(list(tab.keys()))

    return rec_backtracking_closest(tab, [first_elem], best_length, 0, set(tab.keys()) - {first_elem})


def rec_backtracking_closest(matrix, way, best_length, curr_length, restants):
    if not restants:
        # End of the path : we add the way from the last point to the first
        return (way, curr_length + matrix[way[-1]][way[0]])

    if curr_length > best_length:
        return (False, False)

    best_way = []
    sorted_restants = sorted(restants, key=lambda vertex: matrix[way[-1]][vertex])

    # We first test the closest nodes to our actual node -> improves best_length
    for n in sorted_restants:

        (way_n, length_n) = rec_backtracking_closest(matrix, way + [n], best_length, curr_length + matrix[way[-1]][n],
                                                     restants - {n})
        if length_n:
            if length_n <= best_length:
                best_length = length_n
                best_way = way_n

    if len(best_way) > 0:
        return (best_way, best_length)
    else:
        return (False, False)


# Test

start_time = time.time()
print(backtracking_closest_neighbour(errands))
print("--- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
print(backtracking_closest_neighbour(rand2))
print("--- %s seconds ---" % (time.time() - start_time))


# ### 2. Backtracking with furthest neighbour method

def backtracking_furthest_neighbour(tab):
    best_length = glouton(tab)['length']
    first_elem = choice(list(tab.keys()))

    return rec_backtracking_furthest(tab, [first_elem], best_length, 0, set(tab.keys()) - {first_elem})


def find_best_insert(matrix, way, vertex):
    min_aux = (0, 100000000)
    for i in range(len(way)):
        way_i = way[0:i] + [vertex] + way[i:len(way)]
        sum_i = sum([matrix[way_i[x]][way_i[x + 1]] for x in range(len(way))])
        if sum_i < min_aux[1]:
            min_aux = (i, sum_i)
    return min_aux


def rec_backtracking_furthest(matrix, way, best_length, curr_length, restants):
    if not restants:
        # End of the path : we add the way from the last point to the first
        return (way, curr_length + matrix[way[-1]][way[0]])

    if curr_length > best_length:
        return (False, False)

    best_way = []
    # We classify the remaining points on their distance to all the points in the current path
    sorted_restants = sorted(restants, key=lambda v: sum([matrix[x][v] for x in way]))[::-1]

    # We first test the closest nodes to our actual node -> improves best_length
    for n in sorted_restants:
        (insert_index, insert_length) = find_best_insert(matrix, way, n)

        (way_n, length_n) = rec_backtracking_furthest(matrix, way[0:insert_index] + [n] + way[insert_index:len(way)],
                                                      best_length, insert_length, restants - {n})
        if length_n:
            if length_n <= best_length:
                best_length = length_n
                best_way = way_n

    if len(best_way) > 0:
        return (best_way, best_length)
    else:
        return (False, False)


# Test

start_time = time.time()
print(backtracking_furthest_neighbour(errands))
print("--- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
print(backtracking_furthest_neighbour(rand2))
print("--- %s seconds ---" % (time.time() - start_time))


# ### Conclusion on these backtracking methods
#
# #### Surprisingly, the time performances are far as good as simple backtracking. Let's try other methods !


# ## 3. Backtracking with optimistic and pessimistic approach

# #### 1. Best edge

# We first use a backtracking without heuristic with an optimistic and and pessimistic bound "branch and bound",
# The pessimistic bound is the one used before.
# The optimistic bound is defined by : if n is the total number of nodes : size(current_path) + (n- size(current_path)) * min
# where min is the minimal weight of a path between 2 nodes within the remaining nodes
# 
# Translation: Tout d'abord, on utilise un backtracking sans heuristique avec une borne optmiste et une borne pessimiste "branch and bound",
# la borne pessimiste étant celle implémentée dans les TP précédents de backtracking.
# La borne optimiste est défini par, si n est le nombre total de noeuds : taille(chemin actuel) + (n- taille(chemin actuel)) * min
# où min est le poids minimal d'un chemin entre 2 noeuds dans tous les noeuds restants


def branch_and_bound_1(tab) :
    best_length = glouton(tab)['length']
    first_elem = choice(list(tab.keys()))
    return rec_branch_and_bound_1(tab, [first_elem], best_length, 0, set(tab.keys()) - {first_elem})

    
def rec_branch_and_bound_1(matrix, way, best_length, curr_length, restants) :
    if not restants :
        # Fin de chemin : on rajoute longueur du dernier au premier
        return (way, curr_length + matrix[way[-1]][way[0]])
    
    if curr_length > best_length :
        return (False, False)
        
    # Check optimum
    # Longueur minimale entre 2 noeuds dans tous les restants
    if len(restants) > 1 :
        set_restants = restants.copy()
        set_restants.add(way[0])
        min_restants = min([min([matrix[v][j] for j in (set_restants-{v})]) for v in set_restants])
        
        # Optimum : chemin actuel + meilleure longueur dans ce qu'il reste * (nombre restants + 1)  (+1 car il y a le lien fin -> début)
        optimum = curr_length + min_restants * (len(list(restants))+1)
        # Cas où l'optimum permet d'éliminer une branche
        if optimum > best_length :
            #print("optimum : ",optimum, ", best_length : ", best_length)    
            return (False, False)
    
    best_way = []
    for n in restants :
        (way_n, length_n) = rec_branch_and_bound_1(matrix, way + [n], best_length, curr_length + matrix[way[-1]][n], restants - {n})
        if length_n :
            # Cas où le pessimiste permet d'éliminer une branche
            if length_n <= best_length :
                best_length = length_n
                best_way = way_n
    
    if len(best_way) > 0 :
        return (best_way, best_length)
    else :
        return (False, False)


# Test

start_time = time.time()
print(branch_and_bound_1(errands))
print("--- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
print(branch_and_bound_1(rand))
print("--- %s seconds ---" % (time.time() - start_time))


# We can see that we have better results than simple backtracking !

# #### 2. K best edges

# We use a branch and bound with the optimistic bound : if n is the total number of nodes : size(current_path) + sum(min_edges)
# where min_edges is the table of the (n - size(current_path)) smallest edges.
#
# On utilise un branch and bound avec comme borne optimiste, si n est le nombre total de noeuds : taille(chemin actuel) + sum(min_arrêtes)
# où min_arrêtes est le tableau des (n - taille(chemin actuel)) plus petites arêtes.


def branch_and_bound_2(tab) :
    best_length = glouton(tab)['length']
    first_elem = choice(list(tab.keys()))
    return rec_branch_and_bound_2(tab, [first_elem], best_length, 0, set(tab.keys()) - {first_elem})


def tab_min_aretes(matrix, restants) :
    dist_aretes = []
    visited = set()
    for v in restants :
        visited.add(v)
        for j in restants-visited :
            dist_aretes.append(matrix[v][j])
    # On retourne les K plus petites arrêtes avec K le nombre de noeuds restants
    return sorted(list(dist_aretes))[0:len(restants)]


def rec_branch_and_bound_2(matrix, way, best_length, curr_length, restants) :
    if not restants :
        # Fin de chemin : on rajoute longueur du dernier au premier
        return (way, curr_length + matrix[way[-1]][way[0]])
    
    if curr_length > best_length :
        return (False, False)
        
    
    # Check optimum
    # Longueur minimale entre 2 noeuds dans tous les restants
    if len(restants) > 1 :
        set_restants = restants.copy()
        set_restants.add(way[0])        
        tab_aretes = tab_min_aretes(matrix, set_restants)
        #print(tab_aretes)
        optimum = curr_length + sum(tab_aretes)
        #print("current way : ", way)
        #print("best_length : ", best_length, ", optimum : ", optimum)
        # Cas où l'optimum permet d'éliminer une branche
        if optimum > best_length :
            #print("optimum : ",optimum, ", best_length : ", best_length)    
            return (False, False)
    
    best_way = []
    for n in restants :
        (way_n, length_n) = rec_branch_and_bound_2(matrix, way + [n], best_length, curr_length + matrix[way[-1]][n], restants - {n})
        if length_n :
            # Cas où le pessimiste permet d'éliminer une branche
            if length_n <= best_length :
                best_length = length_n
                best_way = way_n
    
    if len(best_way) > 0 :
        return (best_way, best_length)
    else :
        return (False, False)


# Test

start_time = time.time()
print(branch_and_bound_2(errands))
print("--- %s seconds ---" % (time.time() - start_time))


# Test

start_time = time.time()
print(branch_and_bound_2(rand))
print("--- %s seconds ---" % (time.time() - start_time))


# Test

start_time = time.time()
print(branch_and_bound_2(big))
print("--- %s seconds ---" % (time.time() - start_time))


# #### The improvement in execution time is tremendous !
# #### Our program works fine on  "big", a 17-size graph in less than 10 seconds !



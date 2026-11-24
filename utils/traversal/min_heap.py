import math


class Min_Heap:
    #on implémente l'arbre binaire équilibré
    # pour un élément placé en indice n, ses enfants seront en indice 2n+1 et 2n+2

    def __init__(self):
        self.structure = [None]

    def adjust_len_struct(self): #return l'indice de l'emplacement vide
        depth = int(math.log2(len(self.structure)))
        for i in range(2**(depth-1), len(self.structure)):
            if self.structure[i] is None:
                return i
        self.structure+= [ None for i in range (2**(depth+1))]
        return None
        


    def add_or_replace(self, key,valeur): #element
        emplacement_libre = self.adjust_len_struct()
        if emplacement_libre is not None:
            parent = self.structure[int(math.log2(emplacement_libre))]
            if parent[1]<self.structure[emplacement_libre]:
                pass


        
    
    def remove(self):
        pass

         


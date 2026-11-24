import math


class Min_Heap:
    #on implémente l'arbre binaire équilibré
    # pour un élément placé en indice n, ses enfants seront en indice 2n+1 et 2n+2

    def __init__(self):
        self.structure = []
    

    def get_taille(self):
        return len(self.structure)
        


    def add_or_replace(self, element):
        """        
        On insère x à la prochaine position libre, soit la position libre la plus à gauche possible sur le dernier niveau. 
        Puis, on effectue l'opération suivante (que l'on appelle percolation vers le haut ou percolate-up) pour rétablir si nécessaire la propriété d'ordre du tas binaire : 
        tant que  x n'est pas la racine de l'arbre et que x est strictement supérieur à son père, on échange les positions de x et son père. (cf wikipédia)
        """

        key, value = element[0], element[1]
        #Vérif si la clé est déjà dans le tas
        indice = None
        for i in range(len(self.structure)):
            if self.structure[i][0] == key:
                if value >= self.structure[i][1]:
                    return
                self.structure[i] = (key, value)
                indice = i
                break

        if indice is None:
            self.structure.append((key, value))
            indice = len(self.structure) - 1
        while indice > 0:
            parent = (indice-1)//2
            if self.structure[indice][1] < self.structure[parent][1]:
                self.structure[parent], self.structure[indice] = self.structure[indice], self.structure[parent]
                indice = parent
            else:
                break
        


        
    
    def remove(self):
        #pour dijkstra on souhaite tjrs retirer l'élem min donc la racine
        """
        On supprime la racine, et on met à sa place le nœud qui était en dernière position de l'arbre binaire, soit donc le nœud le plus à droite sur le dernier niveau, que l'on notera x.
          Puis on fait l'opération suivante (que l'on appelle percolation vers le bas ou percolate-down) : tant que x a des fils et que x est strictement inférieur à l'un de ses fils, on échange 
          les positions entre x et le plus grand de ses fils. (cf wikipédia)
        """
        if len(self.structure) == 0:
            return None
        
        noeud_remove = self.structure[0]
        key, value = self.structure.pop()

        if len(self.structure)==0:
            return noeud_remove
        
        nb_noeuds = len(self.structure)
        self.structure[0] = (key, value)
        indice = 0
        #tant que le noeud courant au moins un fils
        while 2*indice+1 < nb_noeuds:
            fils1 = 2*indice +1
            fils2 = 2*indice +2
            plus_petit_fils = None
            if fils2 < nb_noeuds and self.structure[fils2][1] < self.structure[fils1][1]:
                plus_petit_fils = fils2
            else:
                plus_petit_fils = fils1
            if self.structure[indice][1] <= self.structure[plus_petit_fils][1]:
                return noeud_remove

            self.structure[indice], self.structure[plus_petit_fils] = self.structure[plus_petit_fils], self.structure[indice]
            indice = plus_petit_fils
            
        return noeud_remove


         


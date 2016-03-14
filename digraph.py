"""Supports computation of strongly connected components and of reverse topological orderings."""

class Digraph:

    def __init__(self, V=None, E = None):
        
        self.V = V or set()
        self.E = E or dict()
        for tail in self.E.keys():
            self.V.add(tail)
            for tip in self.E[tail]:
                self.V.add(tip)
        for v in self.V:
            if v not in E.keys():
                self.E[v] = set()
                
    def visit_all_then_log(self, vertex, log, visited):
        if not visited[vertex]:
            visited[vertex] = True
            for adj_vert in self.E[vertex]:
                self.visit_all_then_log(adj_vert, log, visited)
            log.append(vertex)


    def assign(self, vertex, root, assignments):
        if assignments[vertex] is None:
            assignments[vertex] = root
            for tip in self.E[vertex]:
                self.assign(tip, root, assignments)
        
        
    def R(self):
        """Construct dual (reverse) digraph"""
        E_new = dict()
        for tail in self.E.keys():
            for tip in self.E[tail]:
                if tip in E_new.keys():
                    E_new[tip].add(tail)
                else:
                    E_new[tip] = {tail}

        return Digraph(self.V, E_new)

    def compute_roots(self):
        """
        Compute the root vertices (canonical members) for each strongly connected component 
        of the digraph self.
        """
        
        G_R = self.R() #The reverse of self
        assignments = dict() #Dict of assignments
        for v in self.V:#Note assignments only primed with keys for variables from unitary rules
            assignments[v] = None
        rev_ret_order = self.reverse_DFS_post_order()
        for vertex in rev_ret_order:
            G_R.assign(vertex, vertex, assignments)
                #Assign vert and all descendants to same component
        return assignments
    
    def equiv(self, my_var):
        map = self.compute_roots()
        return {var for var in self.V if map[var] == map[my_var]}
            
    
    def reverse_DFS_post_order(self):
        log = list()
        visited = dict()

        for v in self.V:
            visited[v] = False
        
        for v in self.V:
            if not visited[v]:
                self.visit_all_then_log(v, log, visited)
        
        return list(reversed(log))

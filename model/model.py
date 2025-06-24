import copy
from itertools import combinations

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMap = {}
        for p in DAO.getAllPiloti():
            self._idMap[p.driverId] = p
        self._bestScore = 9999
        self._bestTeam = None

    def getStagione(self):
        return DAO.getStagione()

    def buildGraph(self,anno):
        self._graph.clear()
        self._graph.add_nodes_from(DAO.getPiloti(anno,self._idMap))
        for e in DAO.getVittorie(anno,self._idMap):
            self._graph.add_edge(e[0],e[1],weight=e[2])

        bestScore = 0
        pilota = None
        for node in self._graph.nodes:
            score = self._graph.out_degree(node,weight='weight') - self._graph.in_degree(node,weight='weight')
            if score > bestScore:
                bestScore = score
                pilota = node
        return pilota,bestScore


    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getDreamTeam(self,k):
        parziale = list(combinations(self._graph.nodes,k))
        for p in parziale:
            self._ricorsione(p)

        return self._bestTeam ,self._bestScore

    def _ricorsione(self,parziale):
        if self._bestScore > self.calcolaScore(parziale):
            self._bestTeam = copy.deepcopy(parziale)
            self._bestScore = self.calcolaScore(parziale)

    def calcolaScore(self,parziale):
        scoreTeam = 0
        for n in [x for x in self._graph.nodes if x not in parziale] :
            for p in parziale:
                if self._graph.has_edge(n,p):
                    scoreTeam += self._graph[n][p]['weight']

        return scoreTeam

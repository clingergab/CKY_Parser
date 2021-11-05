"""
COMS W4705 - Natural Language Processing - Summer 19 
Homework 2 - Parsing with Context Free Grammars 
Daniel Bauer
"""

import sys
from collections import defaultdict
from math import fsum
import math

class Pcfg(object): 
    """
    Represent a probabilistic context free grammar. 
    """

    def __init__(self, grammar_file): 
        self.rhs_to_rules = defaultdict(list)
        self.lhs_to_rules = defaultdict(list)
        self.startsymbol = None 
        self.read_rules(grammar_file)      
 
    def read_rules(self,grammar_file):
        
        for line in grammar_file: 
            line = line.strip()
            if line and not line.startswith("#"):
                if "->" in line: 
                    rule = self.parse_rule(line.strip())
                    lhs, rhs, prob = rule
                    self.rhs_to_rules[rhs].append(rule)
                    self.lhs_to_rules[lhs].append(rule)
                else: 
                    startsymbol, prob = line.rsplit(";")
                    self.startsymbol = startsymbol.strip()
                    
     
    def parse_rule(self,rule_s):
        lhs, other = rule_s.split("->")
        lhs = lhs.strip()
        rhs_s, prob_s = other.rsplit(";",1) 
        prob = float(prob_s)
        rhs = tuple(rhs_s.strip().split())
        return (lhs, rhs, prob)

    def verify_grammar(self):
        """
        Return True if the grammar is a valid PCFG in CNF.
        Otherwise return False. 
        """
        # TODO, Part 1
        
        for rules in self.lhs_to_rules:
            prob = []
            if not rules.isupper():
                return False
            #print(rules)
            #prob = [v[2] for val in self.lhs_to_rules[rules] for v in val]
            for rule in self.lhs_to_rules[rules]:
                #print(rule)
                prob.append(rule[2])
                if len(rule[1]) > 2:
                    return False
                if len(rule[1]) == 2:
                    if not rule[1][0].isupper() or not rule[1][1].isupper():
                        #print("len2: ", rule)
                        return False
            if not math.isclose(1, fsum(prob)):
                #print(fsum(prob))
                return False
        #print(fsum(prob))
        #print(self.lhs_to_rules)
        
        return True


if __name__ == "__main__":
    with open(sys.argv[1],'r') as grammar_file:
        grammar = Pcfg(grammar_file)
        if grammar.verify_grammar():
            print("Valid PCFG in CNF")
        else:
            print("Not valid PCFG in CNF")
        

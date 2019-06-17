import pstats
import sys
import cProfile
sys.path.insert(0,'../../scripts/')
from semanticRules import CodiSemanticRuleSet
from semantic import process_single_instruction

# PERFORMANCE TESTING

def test_single_instruction_performance():
    semantic_rule_set = CodiSemanticRuleSet()
    changes_to_add = process_single_instruction(semantic_rule_set, 'play the meow sound')
    print(changes_to_add)

cProfile.run('test_single_instruction_performance()', 'single_instruction_restats')

def test_multiple_instruction_performance():
    semantic_rule_set = CodiSemanticRuleSet()
    for instruction in ['play the chomp sound', 'say hello', "say youre amazing"]:
        changes_to_add = process_single_instruction(semantic_rule_set, instruction)
        print(print(changes_to_add))

cProfile.run('test_multiple_instruction_performance()', 'mult_instruction_restats')

p = pstats.Stats('single_instruction_restats')
print 'what algorithms are taking time?'
p.sort_stats('cumulative').print_stats(10)
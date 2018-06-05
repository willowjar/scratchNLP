# -*- coding: utf-8 -*-

"""
A Simple Lambda Interpreter.

(Code imported from 2004-2005 -- by Rob Speer, Beracah Yancama and others.)
"""

from copy import deepcopy
import dis, new, sys
from opcode import *
from types import CodeType, FunctionType

from nltk.tree import Tree

import cfg
from lab3.utils import is_leaf_node, node_to_str_rule_repr, walk_tree
from semantic_rule_set import SemanticRuleSet
from category import C

################################################################################

def proto_acc(v=None):
    def acc():
        return v
    return acc

acc0 = proto_acc()
make_acc = lambda cell: (new.function(acc0.func_code,
                                      acc0.func_globals,
                                      '#cell_acc',
                                      acc0.func_defaults,
                                      (cell,)))


def cell_deref(cell):
    return make_acc(cell)()


def cells_by_name(f):
    if f.func_closure is None:
        return {}
    
    cells = map(lambda x: cell_deref(x),
                f.func_closure)
    return dict(zip(f.func_code.co_freevars,
                    cells))


################################################################################

def getvars(code):
    return code.co_cellvars + code.co_freevars


def lambdastr(l):
    if type(l) != FunctionType:
        return repr(l)
    return codestr(l.func_code, cells=cells_by_name(l))


def codestr(l, cells=None):
    arg_str = ", ".join(l.co_varnames)
    body_str = Decompiler(l, cells=cells).decompile()
    return "(lambda %s: %s)"%(arg_str, body_str)


class Operator(object):
	pass


class UnaryOp(Operator):
	def __init__(self, symbol, arg):
		self.symbol = symbol
		self.arg = arg
	def __str__(self): return self.symbol+str(self.arg)


class BinaryOp(Operator):
	def __init__(self, symbol, arg1, arg2):
		self.symbol = symbol
		self.arg1 = arg1
		self.arg2 = arg2
	def __str__(self): return "%s %s %s" % (str(self.arg1),
                                            self.symbol,
                                            str(self.arg2))


class Decompiler:
	def __init__(self, code, startpos=0, endpos=None, stack=None, cells=None):
		self.code = code
		self.bytecode = self.code.co_code
		self.pos = startpos
		if stack is None: self.stack = []
		else: self.stack = stack
		if endpos is None: self.endpos = len(self.bytecode)
		else: self.endpos = endpos
		if cells is None: self.cells = {}
		else: self.cells = cells
	def decompile(self):
		bytecode = self.bytecode
		while self.pos != self.endpos:
			op = ord(bytecode[self.pos])
			self.pos += 1
			name = opname[op]
			stack = self.stack
			arg = '<?>'
			if op >= HAVE_ARGUMENT:
				oparg = ord(bytecode[self.pos]) + ord(bytecode[self.pos+1])*256
				self.pos += 2
				if op in hasconst:
					arg = self.code.co_consts[oparg]
				elif op in hasname:
					arg = self.code.co_names[oparg]
				elif op in haslocal:
					arg = self.code.co_varnames[oparg]
				elif op in hascompare:
					arg = cmp_op[oparg]
				elif op in hasfree:
					arg = getvars(self.code)[oparg]
			if name == 'POP_TOP':
				stack.pop()
			elif name == 'ROT_TWO':
				stack[-2:] = [stack[-1], stack[-2]]
			elif name == 'ROT_THREE':
				stack[-3:] = [stack[-1]] + stack[-3:-1]
			elif name == 'ROT_FOUR':
				stack[-4:] = [stack[-1]] + stack[-4:-1]
			elif name == 'DUP_TOP':
				stack.append(stack[-1])
			elif name == 'UNARY_POSITIVE':
				stack.append('+' + stack.pop())
			elif name == 'UNARY_NEGATIVE':
				stack.append('-' + stack.pop())
			elif name == 'UNARY_NOT':
				stack.append('not '+stack.pop())
			elif name == 'UNARY_CONVERT':
				stack.append('`%s`' % stack.pop())
			elif name == 'UNARY_INVERT':
				stack.append('~' + stack.pop())
			elif name == 'BINARY_SUBSCR':
				tos = stack.pop()
				tos1 = stack.pop()
				stack.append('%s[%s]' % (tos1, tos))
			elif name[0:6] == 'BINARY':
				syms = {'POWER': '**',
						'MULTIPLY': '*',
						'DIVIDE': '/',
						'MODULO': '%',
						'ADD': '+',
						'SUBTRACT': '-',
						'LSHIFT': '<<',
						'RSHIFT': '>>',
						'AND': '&',
						'XOR': '^',
						'OR': '|'}
				token = name[7:]
				tos = stack.pop()
				tos1 = stack.pop()
				stack.append('(%s %s %s)' % (tos1, syms[token], tos))
			elif name == 'SLICE+0':
				stack.append(stack.pop() + '[:]')
			elif name == 'SLICE+1':	
				tos = stack.pop()
				tos1 = stack.pop()
				stack.append('%s[%s:]' % (tos1, tos))
			elif name == 'SLICE+2':	
				tos = stack.pop()
				tos1 = stack.pop()
				stack.append('%s[:%s]' % (tos1, tos))
			elif name == 'SLICE+3':	
				tos = stack.pop()
				tos1 = stack.pop()
				tos2 = stack.pop()
				stack.append('%s[%s:%s]' % (tos2, tos1, tos))
			elif name == 'LOAD_CONST':
				if type(arg) == CodeType:
					stack.append(codestr(arg, self.cells))
				else:
					stack.append(repr(arg))
			elif name == 'LOAD_DEREF':
				if self.cells.has_key(arg):
					cell = self.cells[arg]
					if type(cell) == CodeType:
						stack.append(codestr(cell))
					elif type(cell) == FunctionType:
						stack.append(lambdastr(cell))
					else:
						stack.append(repr(cell))
				else: stack.append(arg)
			elif name == 'LOAD_ATTR':
				stack.append('%s.%s' % (stack.pop(), arg))
			elif name[0:4] == 'LOAD':
				stack.append(arg)
			elif name == 'BUILD_TUPLE':
				if oparg == 0: stack.append('()')
				if oparg == 1: stack.append('(%s,)' % stack.pop())
				else:
					items = stack[-oparg:]
					del stack[-oparg:]
					stack.append('(%s)' % ', '.join(items))
			elif name == 'BUILD_LIST':
				if oparg == 0: stack.append('()')
				if oparg == 1: stack.append('(%s,)' % stack.pop())
				else:
					items = stack[-oparg:]
					del stack[-oparg:]
					stack.append('[%s]' % ', '.join(items))
			elif name == 'COMPARE_OP':
				tos = stack.pop()
				tos1 = stack.pop()
				stack.append('(%s %s %s)' % (tos1, arg, tos))
			elif name[:13] == 'CALL_FUNCTION':
				rest = name[13:]
				if rest == '_VAR':
					var = stack.pop()
					kw = None
				elif rest == '_KW':
					var = None
					kw = stack.pop()
				elif rest == '_VAR_KW':
					kw = stack.pop()
					var = stack.pop()
				else:
					kw = var = None
				nkeywords = oparg / 256
				nargs = oparg % 256
				kwlist = []
				for i in range(nkeywords):
					tos = stack.pop()
					tos1 = stack.pop()
					kwlist.append('%s=%s' % (tos1[1:-1], tos))
				kwlist.reverse()
				args = []
				if nargs > 0:
					args = stack[-nargs:]
					del stack[-nargs:]
				allargs = args + kwlist
				if var is not None: allargs.append("*"+var)
				if kw is not None: allargs.append("**"+kw)
				func = stack.pop()
				if len(func) > 7 and func[:7] == '(lambda':
					stack.append('%s@(%s)' % (func, ", ".join(allargs)))
				else:
					stack.append('%s(%s)' % (func, ", ".join(allargs)))
				
			elif name == 'MAKE_FUNCTION':
				pass
			elif name == 'MAKE_CLOSURE':
				pass
			elif name == 'RETURN_VALUE':
				return stack[-1]
			elif name == 'JUMP_IF_FALSE':
				dest = self.pos + oparg
				lhs = stack.pop()
				rhs = Decompiler(self.code, self.pos, dest, [lhs]).decompile()
				self.pos = dest
				stack.append('(%s and %s)' % (lhs, rhs))
				#stack.append(lhs)
			elif name == 'JUMP_IF_TRUE':
				dest = self.pos + oparg
				lhs = stack.pop()
				rhs = Decompiler(self.code, self.pos, dest, [lhs]).decompile()
				self.pos = dest
				stack.append('(%s or %s)' % (lhs, rhs))
				#stack.append(lhs)
			elif name == 'JUMP_FORWARD':
				self.pos += oparg
			elif name == 'JUMP_BACKWARD':
				self.pos -= oparg
			else:
				raise "Can't decompile operation: %s" % name
		if self.endpos is None: return 'None'
		else:
			if len(stack) != 1: raise "Stack is scrod"
			else: return stack[0]


##############################################################################

def is_function(f):
    return isinstance(f, type(is_function))


def str_if_function(x):
    if is_function(x):
        return lambdastr(x)
    else:
        return x


def lambdas_to_strings(args):
    return [str_if_function(x) for x in args]


def assign_lambda_form(node, sem_rule_set):
    p = node.matched_production
    assert p in sem_rule_set.syn_sem_dict.keys()
    return sem_rule_set.syn_sem_dict[p]


def evaluate_node(node, sem_rule_set):
    func = node.lambda_form
    args = []
    for child in node:
        if is_leaf_node(child):
            args.append(str(child))
        else:
            args.append(child.expr)
    expr = apply(func, args)
    return expr


def eval_tree(tree, sem_rule_set, verbose=True):
    assert isinstance(tree, Tree)
    assert isinstance(sem_rule_set, SemanticRuleSet)
    trace = []
    tree = deepcopy(tree)

    def walk(node):
        if is_leaf_node(node):
            return None

        spanned_text = ' '.join([x for x, _ in node.pos()])
        
        # Assign a lambda form.
        assert isinstance(node.matched_production, cfg.Production)
        node.lambda_form = assign_lambda_form(node, sem_rule_set)
        if verbose:
            print ">> Evaluation Step %d."%(len(trace) + 1)
            print "%10s: %s"%('Evaluating', node_to_str_rule_repr(node))
            print "%10s: %s"%('Text', spanned_text)
            print "%10s: %s"%('Expression', lambdastr(node.lambda_form))
            print ""
        trace.append({'lambda_form': node.lambda_form,
                      'text': spanned_text,
                      'tree': deepcopy(tree)})

        # Visit children.
        for child in node:
            walk(child)
        
        # Evaluate the lambda form to produce an expression.
        node.expr = evaluate_node(node, sem_rule_set)
        if verbose:
            print "<< Evaluation Step %d."%(len(trace) + 1)
            print "%10s: %s"%('Evaluated', node_to_str_rule_repr(node))
            print "%10s: %s"%('Text', spanned_text)

            if is_function(node.expr):
                print "%10s: %s"%('Expression', lambdastr(node.expr))
            else:
                print "%10s: %s"%('Value', node.expr)
            print ""
        trace.append({'expr': node.expr,
                      'text': spanned_text,
                      'tree': deepcopy(tree)})

    walk(tree)
    return trace


def decorate_tree_with_trace(evaluated_tree, pretty_print_lambdas=True):
    def post_nonleaf_fn(node):
        if 'lambda_form' in dir(node):
            node_str = lambdastr(node.lambda_form)
            if pretty_print_lambdas:
                node_str = node_str.replace('lambda ', u"\u03BB ")
            node.set_label(node_str)
        if 'expr' in dir(node):
            if is_function(node.expr):
                node_str = lambdastr(node.expr)
                if pretty_print_lambdas:
                    node_str = node_str.replace('lambda ', u"\u03BB ")
                node.set_label(node_str)
            else:
                node.set_label(node.expr)
    
    return walk_tree(deepcopy(evaluated_tree),
                     post_nonleaf_func=post_nonleaf_fn)


# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'FORWARD INTEGER KEYWORD_FOR KEYWORD_IN KEYWORD_RANGE SYMBOL_COLON SYMBOL_COMMA SYMBOL_LPAREN SYMBOL_POINT SYMBOL_RPAREN VALID_STRINGexpression : VALID_STRING SYMBOL_POINT VALID_STRING SYMBOL_LPAREN SYMBOL_RPARENexpression : VALID_STRING SYMBOL_POINT VALID_STRING SYMBOL_LPAREN VALID_STRING SYMBOL_RPARENexpression : VALID_STRING SYMBOL_POINT VALID_STRING SYMBOL_LPAREN FORWARD SYMBOL_RPARENexpression : KEYWORD_FOR VALID_STRING KEYWORD_IN KEYWORD_RANGE SYMBOL_LPAREN INTEGER SYMBOL_RPAREN SYMBOL_COLONexpression : KEYWORD_FOR VALID_STRING KEYWORD_IN KEYWORD_RANGE SYMBOL_LPAREN INTEGER SYMBOL_COMMA INTEGER SYMBOL_RPAREN SYMBOL_COLON'
    
_lr_action_items = {'VALID_STRING':([0,3,4,8,],[2,5,6,10,]),'KEYWORD_FOR':([0,],[3,]),'$end':([1,11,14,15,19,22,],[0,-1,-2,-3,-4,-5,]),'SYMBOL_POINT':([2,],[4,]),'KEYWORD_IN':([5,],[7,]),'SYMBOL_LPAREN':([6,9,],[8,13,]),'KEYWORD_RANGE':([7,],[9,]),'SYMBOL_RPAREN':([8,10,12,16,20,],[11,14,15,17,21,]),'FORWARD':([8,],[12,]),'INTEGER':([13,18,],[16,20,]),'SYMBOL_COMMA':([16,],[18,]),'SYMBOL_COLON':([17,21,],[19,22,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expression':([0,],[1,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> expression","S'",1,None,None,None),
  ('expression -> VALID_STRING SYMBOL_POINT VALID_STRING SYMBOL_LPAREN SYMBOL_RPAREN','expression',5,'p_function_subroutine','inputprocess.py',125),
  ('expression -> VALID_STRING SYMBOL_POINT VALID_STRING SYMBOL_LPAREN VALID_STRING SYMBOL_RPAREN','expression',6,'p_function_subroutine_arg','inputprocess.py',139),
  ('expression -> VALID_STRING SYMBOL_POINT VALID_STRING SYMBOL_LPAREN FORWARD SYMBOL_RPAREN','expression',6,'p_function_subroutine_forward','inputprocess.py',186),
  ('expression -> KEYWORD_FOR VALID_STRING KEYWORD_IN KEYWORD_RANGE SYMBOL_LPAREN INTEGER SYMBOL_RPAREN SYMBOL_COLON','expression',8,'p_for_loop','inputprocess.py',190),
  ('expression -> KEYWORD_FOR VALID_STRING KEYWORD_IN KEYWORD_RANGE SYMBOL_LPAREN INTEGER SYMBOL_COMMA INTEGER SYMBOL_RPAREN SYMBOL_COLON','expression',10,'p_for_loop_with_bounds','inputprocess.py',195),
]

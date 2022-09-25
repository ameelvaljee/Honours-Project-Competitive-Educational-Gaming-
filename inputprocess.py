import sys
import traceback
import re

from codeop import compile_command

import ply.lex as lex
import ply.yacc as yacc


class input_process:

    def __init__(self):
        self.code = []
        self.formatted_code = []
        self.indented = []
        self.error_lst = []
        self.output_lst = []
        self.return_val = ""
        self.number_of_lines = 0
        self.number_of_loops = 0
        #self.number_of_in_game_steps = 0
        self.length_of_each_loop = []
        self.iterations = 0

    def input_code(self, code):
        """To store input code for process. Expects code as a list where each line of code is an index in the list. Indentations should use tab and not spaces."""
        self.code = code
        self.formatted_code = []
        self.indented = []
        self.error_lst = []
        self.output_lst = []
        self.return_val = ""
        self.number_of_lines = 0
        self.number_of_loops = 0
        #self.number_of_in_game_steps = 0
        self.length_of_each_loop = []
        self.iterations = 0
        #self.formatted_code()

    def format_code(self):
        """Removes leading and trailing white spaces for each line of code and formats it for syntax checking and parsing."""
        for line in self.code:
            self.formatted_code.append(line.lstrip().rstrip())

    def syntax_check(self):
        """Checks for syntax errors in code. Accepts a list of lines of code and processes it line by line."""
        self.format_code()
        line_no = 1
        for line in self.formatted_code:
            try: #try to compile line of code
                compile_command(line) #will compile if no errors are found
            except SyntaxError as ex:
                self.error_lst.append("Invalid syntax at line {0} at position {2}: {1}".format(line_no, ex.text.strip("\n"), ex.offset))
            line_no = line_no + 1

    def indent_check(self):
        """Check which statements are indented and report indentation errors"""
        line_no = 0
        pass_iterate = False
        while(line_no < len(self.code)):
            line = self.code[line_no]
            if line.startswith("for"): #if line falls under for it is a valid ident
                self.indented.append(False)
                line_no = line_no + 1
                line = self.code[line_no]
                if line.startswith("\t") or line.startswith("    "): #first line under for should be indented
                    self.indented.append(True)
                    line_no = line_no + 1
                    if line_no == len(self.code): #check if end of list
                        break
                    else:
                        line = self.code[line_no]
                        while(line_no < len(self.code)): #loop while indenting is valid
                            line = self.code[line_no]
                            if line.startswith("\t") or line.startswith("    "):
                                self.indented.append(True)
                            elif line.startswith("for"):
                                pass_iterate = True
                                break
                            else: 
                                self.indented.append(False)
                                break
                            line_no = line_no + 1
                else:
                    self.error_lst.append("Expected indentation block at line {0}: {1}".format(line_no + 1, self.code[line_no]))
                    break
            else:
                if line.startswith("\t") or line.startswith("    "):
                    self.error_lst.append("Illegal indentation at line {0}: {1}".format(line_no + 1, self.code[line_no]))
                    break
                else:
                    self.indented.append(False)
            if pass_iterate:
                pass_iterate = False
            else:    
                line_no = line_no + 1
            #print(self.indented)

    def parse_code(self, with_for = False):
        """Parses the text line by line to get the desire output. If there is an error it will no parse all the lines but stop at cause of error."""
        #token types
        tokens = ('SYMBOL_LPAREN','SYMBOL_RPAREN','KEYWORD_FOR','KEYWORD_IN', 'KEYWORD_RANGE', 'INTEGER', 'SYMBOL_COLON', 'SYMBOL_POINT', 'VALID_STRING', 'SYMBOL_COMMA', 'FORWARD')
        #reg ex rules
        t_SYMBOL_LPAREN = r'\('
        t_SYMBOL_RPAREN = r'\)'
        t_SYMBOL_COLON = r':'
        t_SYMBOL_COMMA = r','
        t_SYMBOL_POINT = r'\.'
        t_VALID_STRING = r'(?!for)(?!in)(?!range)[a-zA-Z][a-zA-Z]*'
        t_FORWARD = r'forward?'
        t_KEYWORD_FOR =  r'for?'
        t_KEYWORD_IN = r'in'
        t_KEYWORD_RANGE = r'range'
        t_INTEGER = r'0|[1-9][0-9]*'

        #ignore whitespace
        def t_WHITESPACE(t):
            r'[ \t]'
            pass
        #error catch
        def t_error(t):
            print("Illegal character '%s'" % t.value[0])
            t.lexer.skip(1)

        #build the lexer
        lexer = lex.lex()

        #productions
        # def p_function(p):
        #     '''expression : VALID_STRING SYMBOL_LPAREN SYMBOL_RPAREN
        # def p_function_args(p):
        #     '''expression : VALID_STRING SYMBOL_LPAREN VALID_STRING SYMBOL_RPAREN'''
        def p_function_subroutine(p):
            '''expression : VALID_STRING SYMBOL_POINT VALID_STRING SYMBOL_LPAREN SYMBOL_RPAREN'''
            func = p[1] + "." + p[3]

            valid_functions = ["player.aimandshoot", ]
            dict_for_func = {
                "player.aimandshoot" : "a",
            }
            if func in valid_functions:
                self.return_val = dict_for_func[func]
            else:
                self.return_val =  "Unrecognised function: {0}".format(func)

        def p_function_subroutine_arg(p):
            '''expression : VALID_STRING SYMBOL_POINT VALID_STRING SYMBOL_LPAREN VALID_STRING SYMBOL_RPAREN'''
            func = p[1] + "." + p[3]
            arg = p[5]
            
            valid_functions = ["player.move", "player.turn", "player.pickup"]
            valid_args_move = ["forward", "backward"]
            dict_for_move = {
                "forward" : "w",
                "backward" : "s"
            }
            valid_args_turn = ["left", "right"]
            dict_for_turn = {
                "left" : "l",
                "right" : "r"
            }
            valid_args_pickup = ["gold", "ammo", "health", "gun"]
            dict_for_pickup = {
                "gold" : "gold", 
                "ammo" : "ammo", 
                "health" : "health",
                "gun" : "gun"
            }

            #print(valid_functions)
            #print(valid_args_move)
            #print(dict_for_move)

            if func in valid_functions:
                if func == valid_functions[0]: #player.move
                    if arg in valid_args_move:
                        self.return_val = dict_for_move[arg]
                        #self.number_of_in_game_steps = self.number_of_in_game_steps + 1
                    else:
                        self.return_val =  "Invalid argument {0} does not accept: {1}".format(func, arg)
                elif func == valid_functions[1]: #player.turn
                    if arg in valid_args_turn:
                        self.return_val = dict_for_turn[arg]
                    else:
                        self.return_val =  "Invalid argument {0} does not accept: {1}".format(func, arg)
                elif func == valid_functions[2]: #player.pickup
                    if arg in valid_args_pickup:
                        self.return_val = "p {0}".format(dict_for_pickup[arg]) 
                    else:
                        self.return_val =  "Invalid argument {0} does not accept: {1}".format(func, arg)
            else:
                self.return_val =  "Unrecognised function: {0}".format(func)

        def p_function_subroutine_forward(p):
            '''expression : VALID_STRING SYMBOL_POINT VALID_STRING SYMBOL_LPAREN FORWARD SYMBOL_RPAREN'''
            self.return_val = "w"
            #self.number_of_in_game_steps = self.number_of_in_game_steps + 1

        def p_for_loop(p):
            '''expression : KEYWORD_FOR VALID_STRING KEYWORD_IN KEYWORD_RANGE SYMBOL_LPAREN INTEGER SYMBOL_RPAREN SYMBOL_COLON'''
            iterations = int(p[6]) 
            self.return_val = "Loop {0}".format(iterations)

            #self.number_of_loops = self.number_of_loops + 1
            self.iterations =  iterations


        def p_for_loop_with_bounds(p):
            '''expression : KEYWORD_FOR VALID_STRING KEYWORD_IN KEYWORD_RANGE SYMBOL_LPAREN INTEGER SYMBOL_COMMA INTEGER SYMBOL_RPAREN SYMBOL_COLON'''
            x = int(p[6])
            y = int(p[8])

            #check for valid bounds
            if x > y: 
                self.return_val = "Invalid bounds for range: {0} to {1}".format(x, y)
            else:
                iterations = y - x 
                self.return_val = "Loop {0}".format(iterations) 
            
            #self.number_of_loops = self.number_of_loops + 1
            self.length_of_each_loop.append(iterations)
            self.iterations =  iterations

        # Error rule for syntax errors
        def p_error(p):
            print(p)
            self.return_val = "Invalid expression"


        # Build the parser
        parser = yacc.yacc()

        # Parse code line by line
        self.number_of_lines = len(self.code)
        line = 0
        repeat = 0
        repeat_Q = []
        pass_iterate = False
        while(line < len(self.formatted_code)):
            parser.parse(self.formatted_code[line]) 
            #Check if an error occured
            if self.return_val == "Invalid expression":
                self.error_lst.append(self.return_val + " at line " + str(line+1) + " : " + self.formatted_code[line])
                break
            elif ("Unrecognised" in self.return_val) or ("Invalid" in self.return_val): #error
                self.error_lst.append(self.return_val)
                break
            else: #no error
                #check if we need to loop
                if "Loop" in self.return_val:
                    self.number_of_loops = self.number_of_loops + 1
                    self.length_of_each_loop.append(self.iterations)
                    self.iterations = 0
                    if with_for:
                        self.output_lst.append(self.return_val[0:4])
                    repeat = int(self.return_val[5:])
                    line = line + 1
                    while(line < len(self.formatted_code)):
                        parser.parse(self.formatted_code[line])
                        if self.return_val == "Invalid expression":
                            self.error_lst.append(self.return_val + " at line " + str(line+1) + " : " + self.formatted_code[line])
                            break
                        elif ("Unrecognised" in self.return_val) or ("Invalid" in self.return_val): #error
                            self.error_lst.append(self.return_val)
                            break
                        elif "Loop" in self.return_val:
                            pass_iterate = True
                            break
                        else:
                            if self.indented[line]:
                                repeat_Q.append(self.return_val)
                            else:
                                break
                        line = line + 1
                    self.output_lst = self.output_lst + repeat_Q*repeat
                    repeat = 0
                    repeat_Q = []
                    if (line == len(self.formatted_code)):
                        pass
                    else:
                        if pass_iterate:
                            pass
                        else:
                            self.output_lst.append(self.return_val)
                else:
                    self.output_lst.append(self.return_val)
            if pass_iterate:
                pass_iterate = False
                pass
            else:
                line = line + 1
        #print(self.indented)
    
    def process(self, with_for = False):
        """Processes input text and produces output as if the program were compile and run."""
        #print("In process()")
        self.syntax_check()
        if self.error_lst:
            return (0, self.error_lst)
        else:
            self.indent_check()
            if self.error_lst:
                return (0, self.error_lst)
            else:
                self.parse_code(with_for)
                if self.error_lst:
                    return (0, self.error_lst)
                else:
                    return (1, self.output_lst)

    def get_num_of_lines(self):
        """Returns the number of lines in the script processed"""
        return self.number_of_lines

    def get_num_of_step(self):
        """Returns the number of forward or backwards movement made by the player from a script of instructions"""
        return self.output_lst.count('w') + self.output_lst.count('s')

    def get_num_of_loops(self):
        """Returns the number of loops in the script file"""
        return self.number_of_loops
    
    def get_loop_iterations(self):
        """Returns the number of iteration loops for each line"""
        return self.length_of_each_loop

import ply.lex as lex
import ply.yacc as yacc
import re

class compilador_Ruby():

    def __init__(self):
        self.mensajes = []
        self.pila = []
        self.tokens = []
        self.variables_number = {}
        self.variables_string = {}
        self.variables_boolean = {}
        self.functions_variables = {}
    def analizadorR(self):
        # Lista de nombres de tokens

        tokens = ['ID',
                  'NUMBER',
                  'DOT',
                  'DOUBLEDOT',
                  'ARROW',
                  'QUESTIONMARK',
                  'ADMIRATION',
                  'AMPERSAND',
                  'VERTICALBAR',
                  'EXPONENT',
                  'PERCENT',
                  'DOUBLEPERCENT',
                  'SUM',
                  'MINUS',
                  'MULTIPLICATION',
                  'DIVISION',
                  'SQUAREROOT',
                  'ASIGN',
                  'LESSYM',
                  'BOOLEAN',
                  'LEFTPARENT',
                  'RIGTHPARENT',
                  'LEQSYM',
                  'GTRSYM',
                  'GEQSYM',
                  'COMMA',
                  'SEMMICOLOM',
                  'SUMASIGN',
                  'MINASIGN',
                  'MULTASIGN',
                  'DIVASIGN',
                  'MODULEASIGN',
                  'EXPONENTASIGN',
                  'LEFTBRACKET',
                  'RIGTHBRAKET',
                  'BACKSLASH',
                  'DOUBLEQUAL',
                  'DIFERENTEQUAL',
                  'KEYLEFT',
                  'KEYRIGHT',
                  'QUOTATIONMARKS',
                  'STRING',
                  'ANDSYM',
                  'ORSYM',
                  'FUNCTIONS'
                  ]

        reserved_words = {
            'alias': 'ALIAS',
            'and': 'AND',
            'begin': 'BEGIN',
            'break': 'BREAK',
            'case': 'CASE',
            'class': 'CLASS',
            'def': 'DEF',
            'do': 'DO',
            'else': 'ELSE',
            'elsif': 'ELSIF',
            'end': 'END',
            'ensure': 'ENSURE',
            'for': 'FOR',
            'if': 'IF',
            'in': 'IN',
            'module': 'MODULE',
            'next': 'NEXT',
            'nil': 'NIL',
            'not': 'NOT',
            'or': 'OR',
            'puts': 'PUTS',
            'redo': 'REDO',
            'rescue': 'RESCUE',
            'retry': 'RETRY',
            'return': 'RETURN',
            'self': 'SELF',
            'super': 'SUPER',
            'then': 'THEN',
            'undef': 'UNDEF',
            'unless': 'UNLESS',
            'until': 'UNTIL',
            'when': 'WHEN',
            'while': 'WHILE',
            'yield': 'YIELD',
            'nil' : 'NIL'
        }

        tokens += list(reserved_words.values())

        functions = {
            'print': 'PRINT',
            'gets': 'GETS',
            'chomp': 'CHOMP',
            'to_i': 'TO_I',
            'to_f': 'TO_F',
            'to_s': 'TO_S',
            'gets.chomp': 'GETS.CHOMP',
            'gets.to_i': 'GETS.TO_I',
            'gets.to_f': 'GETS.TO_F',
            'gets.to_s': 'GETS.TO_S',
            'times': 'TIMES',
            'each': 'EACH',
            'map': 'MAP',
            'select': 'SELECT',
            'reject': 'REJECT',
            'split': 'SPLIT',
            'join': 'JOIN',
            'sort': 'SORT',
            'reverse': 'REVERSE',
            'include?': 'INCLUDE?',
            'empty':'EMPTY',
            'array': 'ARRAY',
            'new':'NEW',
            'gsub': 'GSUB',
            'sub': 'SUB',
            'upcase': 'UPCASE',
            'downcase': 'DOWNCASE',
            'capitalize': 'CAPITALIZE',
            'math' : 'MATH',
            'sqrt': 'SQRT',
            'odd': 'ODD'
        }

        t_ignore = '\t'
        t_DOT = r'\.'
        t_DOUBLEDOT = r'\.\.'
        t_ARROW = r'->'
        t_QUESTIONMARK = r'\?'
        t_ADMIRATION = r'!'
        t_AMPERSAND = r'&'
        t_VERTICALBAR = r'\|'
        t_EXPONENT = r'\*\*'
        t_PERCENT = r'%'
        t_DOUBLEPERCENT = r'%%'

        t_SUM = r'\+'
        t_MINUS = r'\-'
        t_MULTIPLICATION = r'\*'
        t_DIVISION = r'/'
        t_SQUAREROOT = r'√'
        t_ASIGN = r'='
        t_LESSYM = r'<'
        t_LEFTPARENT = r'\('
        t_RIGTHPARENT = r'\)'
        t_LEQSYM = r'<='
        t_GTRSYM = r'>'
        t_GEQSYM = r'>='
        t_COMMA = r','
        t_SEMMICOLOM = r';'
        t_SUMASIGN = r'\+\='
        t_MINASIGN = r'\-\='
        t_MULTASIGN = r'\*\='
        t_DIVASIGN = r'\/\='
        t_MODULEASIGN = r'\%\='
        t_EXPONENTASIGN = r'\*\*\='
        t_LEFTBRACKET = r'\['
        t_RIGTHBRAKET = r'\]'
        t_BACKSLASH = r'\\'
        t_DOUBLEQUAL = r'\=\='
        t_DIFERENTEQUAL = r'!='
        t_KEYLEFT = r'{'
        t_KEYRIGHT = r'}'
        t_QUOTATIONMARKS = '\'|\"'
        t_ANDSYM = r'\&\&'
        t_ORSYM = r'\|\|'

        def t_BOOLEAN(t):
            r'true | false'
            return t

        def t_STRING(t):
            r'"([^"\\]|\\.)*"'
            t.value = t.value[1:-1]
            return t

        def t_ID(t):
            r'[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ_][a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ_]* '
            if t.value.upper() in reserved_words.values():
                t.value = t.value.lower()
                t.type = t.value.upper()
            if t.value.upper() in functions.values():
                t.value = t.value.lower()
                t.type = "FUNCTIONS"
            return t

        def t_NUMBER(t):
            r'[+|-]?[0-9]*\.[0-9]+ | \d+'
            return t

        def t_COMMENT(t):
            r'\#.*'
            pass

        def t_whitespace(t):
            r'[^\S\n]+'
            pass

        def t_newline(t):
            r'\n+'
            t.lexer.lineno += len(t.value)

        def t_error(t):
            print(f'Caracter no valido \'{t.value[0]}\'')
            t.lexer.skip(1)

        # Construir el analizador léxico
        lexer = lex.lex()

        # Codigo de ejemplo en ruby para comprovar el analisador lexico
        with open('./codigo.txt', 'r') as file:
            codigo = file.read()

        # Tokenización del código fuente
        lexer.input(codigo)
        count = 0

        for token in lexer:
            count += 1
            self.tokens.append((token.type, token.value))
            print(token)

        # Reglas de gramática para el analizador sintáctico

        def p_program(p):
            '''
            program : block
            '''
            print("Programa")

        def p_block(p):
            '''
            block : statement_list
            '''
            print("Bloque de codigo")

        def p_statement(p):
            '''
            statement : identifierDecl
                        | statement_if
                        | statement_for
                        | statement_while
                        | statement_def
                        | statement_puts
                        | statement_case
                        | statement_until
                        | statement_module
                        | statement_class
                        | statement_call_function
                        | statement_function_ruby
            '''
            pass

        def p_statement_list(p):
            '''
            statement_list : statement
                            | statement statement_list
                            | statement_list statement
                            | PUTS
                            | empty
                            | ID
            '''
            pass

        def p_identifier_decl1(p):
            '''
            identifierDecl : ID assignment_number expression_number
            '''
            print("Declaración variable")
            var_name = p[1]
            if var_name not in self.variables_number:
                self.variables_number[var_name] = "Numero"

        def p_identifier_decl4(p):
            '''
            identifierDecl : ID assignment expression_number
            '''
            print("Declaración variable")
            var_name = p[1]
            if var_name not in self.variables_number:
                self.variables_number[var_name] = p[3]

        def p_identifier_decl5(p):
            '''
            identifierDecl : ID assignment_number ID LEFTPARENT parameters RIGTHPARENT
            '''
            print("Declaración variable")
            var_name = p[1]
            if var_name not in self.variables_number:
                self.variables_number[var_name] = p[3]

        def p_identifier_decl2(p):
            '''
            identifierDecl : ID assignment expression_string
            '''
            print("Declaración variable")
            var_name = p[1]
            if var_name not in self.variables_number:
                self.variables_number[var_name] = p[3]

        def p_identifier_decl3(p):
            '''
            identifierDecl : ID assignment expression_boolean
            '''
            print("Declaración variable")
            var_name = p[1]
            if var_name not in self.variables_number:
                self.variables_number[var_name] = p[3]

        def p_identifier_assignmentList1(p):
            '''
            identifierDecl : identifierList assignment_number expression_number_list
                           | identifierList assignment expression_number_list
            '''
            print("Declaración multiple")

        def p_identifier_assignmentList2(p):
            '''
            identifierDecl : identifierList assignment_number expression_string_list
            '''
            print("Declaración multiple")

        def p_identifier_assignmentList3(p):
            '''
            identifierDecl : identifierList assignment expression_boolean_list
            '''
            print("Declaración multiple")


        def p_list_identifier(p):
            '''
            identifierList : ID
                           | identifierList COMMA ID
            '''
            pass

        def p_list_expression_number(p):
            '''
            expression_number_list : expression_number
                                   | expression_number_list COMMA expression_number
            '''
            pass

        def p_list_expression_string(p):
            '''
            expression_string_list : expression_string
                                   | expression_string_list COMMA expression_string
            '''
            pass

        def p_list_expression_boolean_list(p):
            '''
            expression_boolean_list : expression_boolean
                                    | expression_boolean_list COMMA expression_boolean
            '''
            pass

        def p_array_decl(p):
            '''
            identifierDecl : ID assignment LEFTBRACKET array_elements RIGTHBRAKET
                           | ID assignment FUNCTIONS LEFTBRACKET array_elements RIGTHBRAKET
                           | ID assignment FUNCTIONS
                           | ID assignment FUNCTIONS QUESTIONMARK
                           | ID assignment FUNCTIONS LEFTPARENT NUMBER RIGTHPARENT
            '''
            print("Declaracion array")

        def p_array_declList(p):
            '''
            identifierDecl : identifierDecl COMMA ID assignment LEFTBRACKET array_elements RIGTHBRAKET
            '''
            print("Declaración multiple")

        def p_identifierDecl_semmicolom(p):
            '''
            identifierDecl : identifierDecl SEMMICOLOM
            '''
            pass

        def p_array_elements_simple(p):
            '''
            array_elements : expression
                           | empty
            '''
            print("Asignacion elemento array")

        def p_array_elements_multiple(p):
            '''
            array_elements : array_elements COMMA expression_number
                            | array_elements COMMA expression_string
                            | array_elements COMMA expression_boolean
             '''

            print("Asignación multiples elementos")

        def p_statement_if(p):
            '''
            statement_if : IF expression_boolean statement_list END
                        | IF expression_boolean statement_list ELSE statement_list END
                        | IF expression_boolean statement_list elsif_list
            '''
            print("Condicional")

        def p_elsif_list(p):
            '''
            elsif_list : ELSIF expression_boolean statement_list END
                        | ELSIF expression_boolean statement_list ELSE statement_list END
                        | ELSIF expression_boolean statement_list elsif_list
            '''
            print("Condicional anidado")

        def p_statement_for(p):
            '''
            statement_for : FOR ID IN ID statement_list END
                            | FOR ID IN NUMBER DOUBLEDOT NUMBER statement_list END
                            | FOR ID IN LEFTBRACKET array_elements RIGTHBRAKET statement_list END
            '''
            print("Bucle for")

        def p_statement_while(p):
            '''
            statement_while : WHILE expression_boolean DO statement_list END
                            | WHILE expression_boolean statement_list END
            '''
            print("Bucle while")

        def p_statement_until(p):
            '''
            statement_until : UNTIL expression_boolean DO statement_list END
                                | UNTIL expression_boolean statement_list END
            '''
            print("Bucle until")

        def p_statement_def(p):
            '''
            statement_def : DEF ID LEFTPARENT parameters RIGTHPARENT statement_list END
                          | DEF ID LEFTPARENT parameters RIGTHPARENT statement_list RETURN expression END
                          | ID ASIGN ARROW LEFTPARENT parameters RIGTHPARENT KEYLEFT expression KEYRIGHT
            '''
            print("Declaración funcion")
            #func_name = p[2]
            #if func_name not in self.functions_variables:
                #self.mensajes.append(f"La función '{func_name}' no ha sido declarada.")

        def p_statement_case(p):
            '''
            statement_case : CASE ID when_list
            '''
            print("Condicional case")

        def p_when_list(p):
            '''
            when_list : WHEN expression statement_list END
                        | WHEN expression statement_list ELSE statement_list END
                        | WHEN expression statement_list when_list
            '''
            pass

        def p_statement_module(p):
            '''
            statement_module : MODULE ID statement_list END
            '''
            print("Declaración modulo")

        def p_statement_class(p):
            '''
            statement_class : CLASS ID statement_list END
            '''
            print("Declaración clase")

        def p_statement_puts(p):
            '''
            statement_puts : PUTS expression
            '''
            print("Mostrar por consola")
            function_name = p[1]
            if function_name not in self.functions_variables:
                self.mensajes.append(f"La función '{function_name}' no ha sido declarada.")

        def p_statement_call_function(p):
            '''
            statement_call_function : ID LEFTPARENT parameters RIGTHPARENT
            '''
            print("Llamada de funcion")
            func_name = p[2]
            if func_name not in self.functions_variables:
                self.mensajes.append(f"La función '{func_name}' no la han declarado.")
                print(f"Numero de parametros: {p[3]}")

        def p_statement_function_ruby(p):
            '''
            statement_function_ruby : FUNCTIONS LEFTPARENT parameters RIGTHPARENT
            '''
            print("Llamada función julia")
            func_name = p[1]
            if func_name not in self.functions_variables:
                self.mensajes.append(f"La función '{func_name}' no ha sido declarada.")

        def p_parameters_list(p):
            '''
            parameters : expression
                        | expression COMMA parameters
                        | empty
            '''
            pass

        def p_parameters_list1(p):
            '''parameters : ID'''
            print("Parametros")
            var_name = p[1]
            if var_name not in self.variables_number:
                self.variables_number[var_name] = "Numero"

        def p_expression(p):
            '''
            expression : expression_number
                        | expression_string
                        | expression_boolean
            '''
            pass

        def p_assigment_identifier1(p):
            '''
            assignment : ASIGN
            '''
            pass

        def p_assigment_identifier8(p):
            '''
            assignment : DOT
            '''
            pass

        def p_assignment_identifier2(p):
            '''
            assignment_number : SUMASIGN
            '''
            pass

        def p_assignment_identifier3(p):
            '''
            assignment_number : MINASIGN
            '''
            pass

        def p_assignment_identifier4(p):
            '''
            assignment_number : MULTASIGN
            '''
            pass

        def p_assignment_identifier5(p):
            '''
            assignment_number : DIVASIGN
            '''
            pass

        def p_assignment_identifier6(p):
            '''
            assignment_number : MODULEASIGN
            '''
            pass

        def p_assignment_identifier7(p):
            '''
            assignment_number : EXPONENTASIGN
            '''

        def p_expression_number1(p):
            '''
            expression_number : ID
            '''
            print("Numero")
            var_name = p[1]
            if var_name not in self.variables_number:
                self.mensajes.append(f"No se encuentra definida la variable '{var_name}'.")

        def p_expression_number(p):
            '''
            expression_number : NUMBER
                              | expression_number operator_arithmetic expression_number
                              | MINUS expression_number
                              | ID LEFTPARENT parameters RIGTHPARENT
            '''
            print("Numero")

        def p_expression_string(p):
            '''
            expression_string : STRING
            '''
            print("Cadena")

        def p_expression_boolean(p):
            '''
            expression_boolean : ID
                                | BOOLEAN
                                | ID LEFTPARENT parameters RIGTHPARENT
            '''
            print("Booleano")

        def p_expression_plus(p):
            '''
            operator_arithmetic : SUM
            '''
            print("Suma")

        def p_expression_minus(p):
            '''
            operator_arithmetic : MINUS
            '''
            print("Resta")

        def p_expression_mult1(p):
            '''
            operator_arithmetic : MULTIPLICATION
            '''
            print("Multiplicación")

        def p_expression_mult2(p):
            '''
            expression_string : expression_string MULTIPLICATION expression_number
            '''
            print("Multiplicación")

        def p_expression_div(p):
            '''
            operator_arithmetic : DIVISION
            '''
            print("División")

        def p_expression_mod(p):
            '''
            operator_arithmetic : PERCENT
            '''
            print("Modulo")

        def p_expression_squareRoot(p):
            '''
            operator_arithmetic : SQUAREROOT
            '''
            print("Raíz cuadrada")

        def p_expression_exponent(p):
            '''
            operator_arithmetic : EXPONENT
            '''
            print("Exponente")

        def p_expression_parents1(p):
            '''
            expression_number : LEFTPARENT expression_number RIGTHPARENT
            '''
            print("Parentesis numero")

        def p_expression_parents2(p):
            '''
            expression_string : LEFTPARENT expression_string RIGTHPARENT
            '''
            print("Parentesis string")

        def p_condition_boolean(p):
            '''
            expression_boolean : expression_boolean relation expression_boolean
                                    | ADMIRATION expression_boolean
                                    | expression_string relation expression_string
                                    | expression_number relation expression_number
            '''
            print("Expression booleana")

        def p_expression_parents3(p):
            '''
            expression_boolean : LEFTPARENT expression_boolean RIGTHPARENT
            '''
            print("Parentesis boolean")

        def p_relation_boolean1(p):
            '''
            relation : LESSYM
            '''
            pass

        def p_relation_boolean2(p):
            '''
            relation : LEQSYM
            '''
            pass

        def p_relation_boolean3(p):
            '''
            relation : GTRSYM
            '''
            pass

        def p_relation_boolean4(p):
            '''
            relation : GEQSYM
            '''
            pass

        def p_relation_boolean5(p):
            '''
            relation : DOUBLEQUAL
            '''
            pass

        def p_relation_boolean6(p):
            '''
            relation : DIFERENTEQUAL
            '''
            pass

        def p_relation_boolean7(p):
            '''
            relation : AND
                        | ANDSYM
            '''
            pass

        def p_relation_boolean8(p):
            '''
            relation : OR
                        | ORSYM
            '''
            pass

        def p_empty(p):
            '''
            empty :
            '''
            pass

        def p_error(p):
            if p:
                token_value = p.value
                line = find_position(p)
                mensaje = f"Error de sintaxis en el token '{token_value}'en la línea {line}"
                self.mensajes.append(mensaje)
            else:
                self.mensajes.append("Error de sintaxis en la entrada")

        def find_position(token):
            with open('./codigo.txt', 'r') as file:
                line_number = 1
                for line in file:
                    if token.lexpos <= len(line):
                        return line_number
                    token.lexpos -= len(line)
                    line_number += 1
                return line_number

        parser = yacc.yacc()

        parser.parse(codigo)

        return self.mensajes

    def automata_Ruby(self):

        mensaje = []

        with open('compilador_Ruby/parserNeeded.txt', 'r') as archivo:
            print("Estados y reglas asociadas a los tipos de tokens:")
            for tipo_token, nombre_token in self.tokens:
                archivo.seek(0)  # Reiniciar el puntero del archivo al principio
                estado = None
                regla = None
                for linea in archivo:
                    if f'{tipo_token}' in linea:
                        # Encuentra el estado asociado con este tipo de token
                        for linea_estado in archivo:
                            match_estado = re.match(r'state\s+(\d+)', linea_estado)
                            if match_estado:
                                estado = match_estado.group(1)
                                break
                        # Encuentra la regla asociada con este tipo de token
                        if f'{tipo_token}' in linea:
                            for linea_estado in archivo:
                                if 'reduce' in linea_estado or 'shift' in linea_estado:
                                    regla = linea_estado.split()[1]
                                    break  # Una vez que se encuentran el estado y la regla, salimos del bucle exterior
                # Imprimir estado y regla asociados con este tipo de token
                if estado and regla:
                    mensaje.append(f'Tipo token: {tipo_token}, Token: {nombre_token}, State: {estado} , Regla: {regla}')
                    print(f'Tipo token: {tipo_token}, Token: {nombre_token} ,State: {estado} , Regla: {regla}')

        return mensaje
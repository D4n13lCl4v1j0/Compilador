import ply.lex as lex
import ply.yacc as yacc
import re

class compilador_Julia():

    def __init__(self):
        self.mensajes = []
        self.pila = []
        self.tokens = []
        self.variables_number = {}
        self.variables_string = {}
        self.variables_boolean = {}
        self.functions_variables = {}

    def analizador(self):

        # Lista de nombres de tokens
        tokens = [
            'IDENTIFIER',
            'NUMBER',
            'STRING',
            'BOOLEAN',
            'SYMBOL',
            'PLUS',
            'MINUS',
            'MULTIPLY',
            'DIVIDE',
            'SQUAREROOT',
            'EXPONENT',
            'PERCENT',
            'ADMIRATION',
            'DOUBLEPERCENT',
            'EQUALS',
            'NOT_EQUALS',
            'ARROW',
            'LESS_THAN',
            'GREATER_THAN',
            'LESS_THAN_OR_EQUAL',
            'GREATER_THAN_OR_EQUAL',
            'ASSIGN',
            'SEMICOLON',
            'SUMASIGN',
            'MINASIGN',
            'MULTASIGN',
            'DIVASIGN',
            'MODULEASIGN',
            'EXPONENTASIGN',
            'COMMA',
            'DOT',
            'DOUBLEDOT',
            'LEFT_PAREN',
            'RIGHT_PAREN',
            'LEFT_BRACKET',
            'RIGHT_BRACKET',
            'LEFT_BRACE',
            'RIGHT_BRACE',
            'COMMENT',
            'NEWLINE',
            'ANDSYM',
            'ORSYM',
            'FUNCTIONS_JULIA'

        ]

        reserved = {
            'as': 'AS',
            'begin': 'BEGIN',
            'break': 'BREAK',
            'catch': 'CATCH',
            'continue': 'CONTINUE',
            'do': 'DO',
            'else': 'ELSE',
            'elseif': 'ELSEIF',
            'end': 'END',
            'for': 'FOR',
            'function': 'FUNCTION',
            'if': 'IF',
            'import': 'IMPORT',
            'in': 'IN',
            'macro': 'MACRO',
            'module': 'MODULE',
            'mut': 'MUT',
            'return': 'RETURN',
            'struct': 'STRUCT',
            'try': 'TRY',
            'using': 'USING',
            'while': 'WHILE',
            'include': 'INCLUDE',
            'require': 'REQUIRE',
            'and': 'AND',
            'or': 'OR',
            'not': 'NOT',
            'println' : 'PRINTLN',

        }

        functions_julia = {
            'println': 'PRINTLN',
            'print': 'PRINT',
            'length': 'LENGTH',
            'typeof': 'TYPEOF',
            'convert': 'CONVERT',
            'parse': 'PARSE',
            'sum': 'SUM',
            'prod': 'PROD',
            'maximum': 'MAXIMUM',
            'minimum': 'MINIMUM',
            'findmax': 'FINDMAX',
            'findmin': 'FINDMIN',
            'sort': 'SORT',
            'sortrows': 'SORTROWS',
            'cumsum':'CUMSUM',
            'cumprod':'CUMPROD',
            'std':'STD',
            'var':'VAR',
            'cov':'COV',
            'map': 'MAP',
            'filter': 'FILTER',
            'reduce': 'REDUCE',
            'any': 'ANY',
            'all': 'ALL',
            'mode':'MODE',
            'mean':'MEAN',
            'median':'MEDIAN',
            'rand': 'RAND',
            'julia':'JULIA',
            'element': 'ELEMENT',
            'array':'ARRAY',
            'dims':'DIMS'
        }

        tokens += list(reserved.values())

        # Definición de patrones para tokens
        t_PLUS = r'\+'
        t_MINUS = r'-'
        t_MULTIPLY = r'\*'
        t_DIVIDE = r'/ | ÷'
        t_SQUAREROOT = r'√'
        t_EXPONENT = r'\^|\*\*'
        t_PERCENT = r'%'
        t_DOUBLEPERCENT = r'%%'
        t_EQUALS = r'\=\='
        t_DOUBLEDOT = r':'
        t_ARROW = r'->'
        t_NOT_EQUALS = r'!='
        t_LESS_THAN = r'<'
        t_GREATER_THAN = r'>'
        t_LESS_THAN_OR_EQUAL = r'<='
        t_GREATER_THAN_OR_EQUAL = r'>='
        t_SUMASIGN = r'\+\='
        t_MINASIGN = r'\-\='
        t_MULTASIGN = r'\*\='
        t_DIVASIGN = r'\/\='
        t_MODULEASIGN = r'\%\='
        t_EXPONENTASIGN = r'\^='
        t_AND = r'&&'
        t_OR = r'\|\|'
        t_ADMIRATION = r'!'
        t_ASSIGN = r'='
        t_SEMICOLON = r';'
        t_COMMA = r','
        t_DOT = r'\.'
        t_LEFT_PAREN = r'\('
        t_RIGHT_PAREN = r'\)'
        t_LEFT_BRACKET = r'\['
        t_RIGHT_BRACKET = r'\]'
        t_LEFT_BRACE = r'\{'
        t_RIGHT_BRACE = r'\}'
        t_ANDSYM = r'\&\&'
        t_ORSYM = r'\|\|'
        t_ignore = ' \t'

        # Patrones con funciones
        def t_IDENTIFIER(t):
            r'[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ_][a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ_]*'
            if t.value.upper() in reserved.values():
                t.value = t.value.lower()
                t.type = t.value.upper()

            if t.value.upper() in functions_julia.values():
                t.value = t.value.lower()
                t.type = "FUNCTIONS_JULIA"
            return t

        def t_STRING(t):
            r'"([^"\\]|\\.)*"'
            t.value = t.value[1:-1]
            return t

        def t_BOOLEAN(t):
            r'true | false'
            return t

        def t_NUMBER(t):
            r'[+|-]?[0-9]*\.[0-9]+ | \d+'
            return t

        def t_SYMBOL(t):
            r':[a-zA-Z_]\w*'
            return t

        def t_COMMENT(t):
            r'\#.*'
            pass

        def t_newline(t):
            r'\n+'
            t.lexer.lineno += len(t.value)

        def t_whitespace(t):
            r'[ \t]+'
            pass

        def t_error(t):
            print(f"Caracter no válido: '{t.value[0]}'")
            t.lexer.skip(1)

        # Construir el analizador léxico
        lexer = lex.lex()

        # Codigo de ejemplo en julian para comprovar el analisador lexico
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

        precedence = (
            ('right', 'IDENTIFIER', 'IF', 'FOR', 'WHILE'),
            ('left', 'FUNCTION','BEGIN'),
            ('right', 'MODULE'),
            ('right', 'ASSIGN'),
            ('right', 'SUMASIGN', 'MINASIGN', 'MULTASIGN', 'DIVASIGN', 'MODULEASIGN', 'EXPONENTASIGN'),
            ('left', 'LESS_THAN', 'LESS_THAN_OR_EQUAL', 'GREATER_THAN', 'GREATER_THAN_OR_EQUAL', 'EQUALS', 'NOT_EQUALS'),
            ('left', 'PLUS', 'MINUS', 'OR', 'ORSYM'),
            ('left', 'MULTIPLY', 'DIVIDE', 'AND','ANDSYM', 'PERCENT'),
            ('right', 'SQUAREROOT'),
            ('right', 'EXPONENT'),
            ('right', 'LEFT_PAREN', 'RIGHT_PAREN', 'LEFT_BRACKET', 'RIGHT_BRACKET',)
        )

        def p_program(p):
            '''
            program : block
            '''
            print("Programa válido")

        def p_block(p):
            '''block : statement_list
                    | empty'''
            print("Bloque de codigo")

        def p_statement_list(p):
            '''
            statement_list : statement
                           | statement statement_list
                           | statement_list statement
            '''

        def p_statement(p):
            '''
            statement : identifierDecl
                      | array_estatement_julia
                      | if_statement
                      | elseif_block
                      | else_statement
                      | while_statement
                      | for_statement
                      | array_estatement
                      | function_definition
                      | statement_function
                      | statement_call_function
                      | statement_function_julia
                      | statement_do
                      | statement_try
                      | statement_module
                      | statement_begin
                      | statement_using
            '''
            print("statement")

        def p_identifier_decl1(p):
            '''
            identifierDecl : IDENTIFIER assignment_number expression_number
            '''
            print("Declaración variable")
            var_name = p[1]
            if var_name not in self.variables_number:
                self.variables_number[var_name] = "Numero"

        def p_identifier_decl6(p):
            '''
            identifierDecl : IDENTIFIER assignment expression_number
            '''
            print("Declaración variable")
            var_name = p[1]
            if var_name not in self.variables_number:
                self.variables_number[var_name] = p[3]

        def p_identifier_decl2(p):
            '''
            identifierDecl : IDENTIFIER assignment expression_string
            '''
            print("Declaración variable")
            var_name = p[1]
            if var_name not in self.variables_string:
                self.variables_string[var_name] = p[3]

        def p_identifier_decl3(p):
            '''
            identifierDecl : IDENTIFIER assignment expression_boolean
            '''
            print("Declaración variable")
            var_name = p[1]
            if var_name not in self.variables_boolean:
                self.variables_boolean[var_name] = p[3]

        def p_identifier_decl4(p):
            '''
            identifierDecl : IDENTIFIER assignment FUNCTIONS_JULIA LEFT_PAREN IDENTIFIER RIGHT_PAREN
            '''
            print("Declaración variable")

        def p_identifier_decl5(p):
            '''
            identifierDecl : IDENTIFIER assignment FUNCTIONS_JULIA LEFT_PAREN IDENTIFIER COMMA IDENTIFIER RIGHT_PAREN
            '''
            print("Declaración variable")

        def p_idicator_julia(p):
            '''
            identifierDecl : FUNCTIONS_JULIA relation IDENTIFIER ASSIGN statement_function_julia
            '''
            print("Declaración variable")

        def p_idicator_julia2(p):
            '''
            identifierDecl : FUNCTIONS_JULIA relation IDENTIFIER ASSIGN LEFT_BRACKET array_elements RIGHT_BRACKET array_estatement_julia
            '''
            print("Declaración variable")

        def p_idicator_julia3(p):
            '''
            identifierDecl : FUNCTIONS_JULIA relation FUNCTIONS_JULIA LEFT_PAREN LEFT_BRACKET array_elements RIGHT_BRACKET COMMA FUNCTIONS_JULIA ASSIGN NUMBER RIGHT_PAREN array_estatement_julia
            '''
            print("Declaración variable")

        def p_identifier_assignmentList1(p):
            '''
            identifierDecl : identifierList assignment_number expression_number_list
                            | identifierList assignment expression_number_list
            '''
            print("Declaración multiple")

        def p_list_expression_number(p):
            '''expression_number_list : expression_number
                                    | expression_number_list COMMA expression_number'''
            pass

        def p_list_expression_string(p):
            '''expression_string_list : expression_string
                                    | expression_string_list COMMA expression_string'''
            pass

        def p_list_expression_boolean_list(p):
            '''expression_boolean_list : expression_boolean
                                        | expression_boolean_list COMMA expression_boolean'''
            pass

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
            '''identifierList : IDENTIFIER
                              | identifierList COMMA IDENTIFIER'''
            pass

        def p_array_estatement(p):
            '''
            array_estatement : IDENTIFIER ASSIGN LEFT_BRACKET array_values RIGHT_BRACKET
            '''

        def p_array_values(p):
            '''
            array_values : array_values COMMA NUMBER
                         | NUMBER
            '''


        def p_array_estructure_julia(p):
            '''
            array_estatement_julia : expression_number FUNCTIONS_JULIA LEFT_BRACE IDENTIFIER COMMA NUMBER RIGHT_BRACE DOUBLEDOT array_content_julia
                                   | values MINUS FUNCTIONS_JULIA FUNCTIONS_JULIA LEFT_BRACE IDENTIFIER COMMA NUMBER RIGHT_BRACE DOUBLEDOT array_content_julia
            '''
            print("array estatement julia")

        def p_array_content_julia(p):
            '''
            array_content_julia : values
                                | values NEWLINE
            '''

        def p_values(p):
            '''
            values : NUMBER
            '''

        def p_function_definition(p):
            '''
             function_definition : FUNCTION IDENTIFIER LEFT_PAREN argument_list RIGHT_PAREN statement_list END
            '''

        def p_statement_function1(p):
            '''
            statement_function : FUNCTION IDENTIFIER LEFT_PAREN argument_list RIGHT_PAREN statement_list END
            '''
            print("Declaración funcion")
            func_name = p[2]
            if func_name not in self.functions_variables:
                self.functions_variables[func_name] = p[4]
            else:
                self.mensajes.append(f"La variable de la función {func_name} ya la han declarado.")

        def p_statement_function2(p):
            '''
            statement_function : FUNCTION IDENTIFIER LEFT_PAREN argument_list RIGHT_PAREN statement_list RETURN expression END
            '''
            print("Declaración función")
            func_name = p[2]
            if func_name not in self.functions_variables:
                self.functions_variables[func_name] = p[4]
            else:
                self.mensajes.append(f"La variable de la función {func_name} ya la han declarado.")

        def p_statement_function3(p):
            '''
            statement_function : IDENTIFIER ASSIGN LEFT_PAREN argument_list RIGHT_PAREN ARROW expression
            '''
            print("Declaración función")
            var_name = p[1]
            if var_name not in self.functions_variables:
                self.functions_variables[var_name] = p[4]
            else:
                self.mensajes.append(f"La variable de la función {var_name} ya la han declarado.")

        def p_statement_call_function(p):
            '''statement_call_function : IDENTIFIER LEFT_PAREN argument_list RIGHT_PAREN'''
            print("Llamada de funcion")
            func_name = p[1]
            if func_name not in self.functions_variables:
                self.mensajes.append(f"La función '{func_name}' no la han declarado.")

        def p_statement_function_julia(p):
            '''
            statement_function_julia : FUNCTIONS_JULIA LEFT_PAREN argument_list RIGHT_PAREN
                                     | FUNCTIONS_JULIA LEFT_PAREN NUMBER RIGHT_PAREN
                                     | FUNCTIONS_JULIA LEFT_PAREN NUMBER DOT NUMBER RIGHT_PAREN
                                     | FUNCTIONS_JULIA LEFT_PAREN IDENTIFIER RIGHT_PAREN

            '''


        def p_argument_list(p):
            '''
            argument_list : expression
                         | expression COMMA argument_list
                         | statement_do
                         | empty
            '''

        def p_if_statement(p):
            '''
            if_statement : IF expression_boolean statement_list END
                         | IF expression_boolean statement_list ELSE statement_list END
                         | IF expression_boolean statement_list elseif_block statement_list ELSE statement_list END
                         | IF expression_boolean statement_list elseif_block END
            '''
            print("if")


        def p_elseif_block(p):
            '''
            elseif_block : ELSEIF expression_boolean statement_list END
                         | ELSEIF expression_boolean statement_list ELSE statement_list END
                         | ELSEIF expression_boolean statement_list elseif_block END
            '''
            ("elseif")

        def p_else_statement(p):
            '''
            else_statement : ELSE statement_list END
                           | empty
            '''

        def p_assignment(p):
            '''
            assignment : IDENTIFIER ASSIGN expression
            '''

        def p_while_statement(p):
            '''
            while_statement : WHILE expression_boolean statement_list END
                            | WHILE IDENTIFIER relation NUMBER statement_list END
            '''
            print("while while")

        def p_for_statement(p):
            '''
            for_statement : FOR IDENTIFIER IN expression DOUBLEDOT expression_number statement_list END
                          | FOR IDENTIFIER IN expression_number DOUBLEDOT expression_number statement_list END
                          | FOR IDENTIFIER LEFT_BRACKET array_elements RIGHT_BRACKET statement_list END
            '''
            print("for for")

        def p_array_decl(p):
            '''
            identifierDecl : IDENTIFIER assignment LEFT_BRACKET array_elements RIGHT_BRACKET
            '''
            print("Declaracion array")

        def p_array_declList(p):
            '''
            identifierDecl : identifierDecl COMMA IDENTIFIER assignment LEFT_BRACKET array_elements RIGHT_BRACKET
                           | identifierDecl NEWLINE IDENTIFIER assignment LEFT_BRACKET array_elements RIGHT_BRACKET
            '''
            print("Declaración multiple")

        def p_array_elements_s(p):
            '''
            array_elements : expression_number
                         | expression_string
                         | expression_boolean
                         | empty
            '''

        def p_array_elements_m(p):
            '''
            array_elements : array_elements COMMA expression_number
                           | expression_number SEMICOLON expression_number
                           | array_elements COMMA expression_string
                           | array_elements COMMA expression_boolean
            '''

        def p_empty(p):
            '''
            empty :
            '''
            pass

        def p_statement_call_function(p):
            '''
            statement_call_function : IDENTIFIER LEFT_PAREN argument_list RIGHT_PAREN
            '''
            print("Llamada de funcion")

        def p_statement_do(p):
            '''
            statement_do : DO statement_list END
            '''
            print("Bloque do")

        def p_statement_begin(p):
            '''
            statement_begin : BEGIN statement_list END
            '''
            print("Declación begin")

        def p_statement_try(p):
            '''
            statement_try : TRY statement_list CATCH IDENTIFIER statement_list END
            '''
            print("Manejo excepcion")

        def p_statement_module(p):
            '''
            statement_module : MODULE IDENTIFIER statement_list END
            '''
            print("Declaración de modulo")

        def p_statement_using(p):
            '''
            statement_using : USING IDENTIFIER
                            | USING IDENTIFIER AS IDENTIFIER
            '''
            print("Importando paquete")

        def p_parameters_list(p):
            '''parameters : IDENTIFIER'''
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

        def p_expression_parents3(p):
            '''
            expression_boolean : LEFT_PAREN expression_boolean RIGHT_PAREN
            '''
            print("Parentesis boolean")

        def p_expression_boolean(p):
            '''
            expression_boolean : IDENTIFIER
                               | BOOLEAN
                               | IDENTIFIER LEFT_PAREN argument_list RIGHT_PAREN
            '''
            print("Booleano")

        def p_condition_boolean(p):
            '''expression_boolean : expression_boolean relation expression_boolean
                                    | ADMIRATION expression_boolean
                                    | expression_string relation expression_string
                                    | expression_number relation expression_number'''
            print("Expression booleana")

        def p_assigment_identifier1(p):
            '''
            assignment : ASSIGN
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
            '''expression_number : IDENTIFIER'''
            print("Numero")
            var_name = p[1]
            if var_name not in self.variables_number:
                self.mensajes.append(f"No se encuentra definida la variable '{var_name}'.")

        def p_expression_number(p):
            '''
            expression_number : NUMBER
                              | expression_number operator_arithmetic expression_number
                              | expression_number DOUBLEDOT expression_number
                              | expression_number DOT expression_number
                              | MINUS expression_number
                              | IDENTIFIER LEFT_PAREN argument_list RIGHT_PAREN
            '''
            print("Numero")

        def p_expression_parents1(p):
            '''
            expression_number : LEFT_PAREN expression_number RIGHT_PAREN
                              | LEFT_BRACKET expression_number RIGHT_BRACKET
            '''
            print("Parentesis numero")

        def p_expression_string (p):
            '''
            expression_string : STRING
            '''

        def p_expression_parents2(p):
            '''
            expression_string : LEFT_PAREN expression_string RIGHT_PAREN
            '''
            print("Parentesis string")

        def p_expression_mult2(p):
            '''
            expression_string : expression_string MULTIPLY expression_number
                              | expression_string MULTIPLY expression_string
            '''
            print("Multiplicación")

        def p_expression_plus(p):
            '''
            operator_arithmetic : PLUS
            '''
            print("Suma")

        def p_expression_minus(p):
            '''
            operator_arithmetic : MINUS
            '''
            print("Resta")

        def p_expression_mult1(p):
            '''
            operator_arithmetic : MULTIPLY
            '''
            print("Multiplicación")

        def p_expression_div(p):
            '''
            operator_arithmetic : DIVIDE
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

        def p_relation_boolean1(p):
            '''
            relation : LESS_THAN
            '''
            pass

        def p_relation_boolean2(p):
            '''
            relation : LESS_THAN_OR_EQUAL
            '''
            pass

        def p_relation_boolean3(p):
            '''
            relation : GREATER_THAN
            '''
            pass

        def p_relation_boolean4(p):
            '''
            relation : GREATER_THAN_OR_EQUAL
            '''
            pass

        def p_relation_boolean5(p):
            '''
            relation : EQUALS
            '''
            pass

        def p_relation_boolean6(p):
            '''
            relation : NOT_EQUALS
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

        #crear analizador sintactico
        parser = yacc.yacc()
        parser.parse(codigo)

        return self.mensajes

    def automata_Ruby(self):

        mensaje = []

        with open('compilador_Julia/parserNeededJ.txt', 'r') as archivo:
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
                                    break # Una vez que se encuentran el estado y la regla, salimos del bucle exterior
                # Imprimir estado y regla asociados con este tipo de token
                if estado and regla:
                    mensaje.append(f'Tipo token: {tipo_token}, Token: {nombre_token}, State: {estado} , Regla: {regla}')
                    print(f'Tipo token: {tipo_token}, Token: {nombre_token} ,State: {estado} , Regla: {regla}')

        return mensaje

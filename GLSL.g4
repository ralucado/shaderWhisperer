grammar GLSL;

prog:
    preprocessor* statement_list;

//�궨��
preprocessor
    :   SHARP version_pre
    ;

version_pre
    : 'version' integer VERSION_PROFILE?
    ;

VERSION_PROFILE
    :   'core'
    |   'compatibility'
    |   'es'
    ;

//����������
type_qualifier 
    :   (storage_qualifier 
    |   layout_qualifier 
    |   precision_qualifier 
    |   interpolation_qualifier 
    |   invariant_qualifier 
    |   precise_qualifier)+ 
    ; 


layout_qualifier:   'layout' LEFT_PAREN layout_qualifier_id  (COMMA layout_qualifier_id)* RIGHT_PAREN;
layout_qualifier_id: IDENTIFIER | IDENTIFIER ASSIGNMENT_OP constant_expression | 'shared';

storage_qualifier
    :   'const'
    |   'in'
    |   'out'
    |   'uniform'
    |   'buffer'
    |   'shared'
    ;

precision_qualifier
    :   'high_precision'
    |   'medium_precision'
    |   'low_precision'
    ;

interpolation_qualifier
    :   'smooth'
    |   'flat'
    |   'noperspective'
    ;

invariant_qualifier:    'invariant';

precise_qualifier:    'precise';

//Ԫ����
integer: DECIMAL |  OCTAL | HEX ;

float_num: FLOAT_NUM;

bool_num : 'true' | 'false';

//vec3
//int[64]
//int[][][]
type_specifier: type_specifier_nonarray array_specifier*;

type_specifier_nonarray
    :   basic_type
    |   IDENTIFIER
    ;

array_specifier :   LEFT_BRACKET expression? RIGHT_BRACKET;
struct_specifier:   DOT expression;

basic_type
    :   void_type
    |   scala_type
    |   vector_type
    |   matrix_type
    |   opaque_type
    ;

void_type : 'void';

scala_type: SCALA;

vector_type: VECTOR;

matrix_type: MATRIX;

opaque_type
    :   float_opaque_type
    |   int_opaque_type
    |   u_int_opaque_type
    ;

float_opaque_type:  FLOAT_OPAQUE;
int_opaque_type: INT_OPAQUE;
u_int_opaque_type: U_INT_OPAQUE;


//����ʽ

expression
    :   primary_expression #primary
    |   expression INCREMENT_OP #postIncrement
    |   INCREMENT_OP expression #preIncrement
    |   ADDSUB_OP expression #sign
    |   UNARY_OP expression #unary
    |   expression MULDIV_OP expression #muldiv
    |   expression ADDSUB_OP expression #addsub
    |   expression SHIFT_OP expression #shift
    |   expression COMPARE_OP expression #cmp
    |   expression EQUAL_OP expression #eq
    |   expression BITWISE_OP expression #bitwise
    |   expression LOGIC_OP expression #logic
    |   expression QUESTION expression COLON expression #ternary
    ;

primary_expression
    :   constant_expression #constant_exp
    |   basic_type LEFT_PAREN (expression  (COMMA expression)*)? RIGHT_PAREN #basic_type_exp
    |   LEFT_PAREN type_specifier RIGHT_PAREN expression #type_spec_exp
    |   left_value  array_struct_selection? #left_value_exp
    ;

constant_expression
    :   integer
    |   float_num
    |   bool_num
    ;

left_value
	:	function_call
	|   LEFT_PAREN expression RIGHT_PAREN
	|	IDENTIFIER
	;

array_struct_selection: (array_specifier | struct_specifier)+;

assignment_expression: ASSIGNMENT_OP expression;

arithmetic_assignment_expression: ARITHMETIC_ASSIGNMENT_OP expression;

//����
function_definition
    : return_Type function_name
        LEFT_PAREN (func_decl_member  (COMMA func_decl_member)* )? RIGHT_PAREN LEFT_BRACE
            statement_list
        RIGHT_BRACE
    ;

function_declaration: return_Type function_name LEFT_PAREN (func_decl_member (COMMA func_decl_member)* )? RIGHT_PAREN;

function_call: function_name LEFT_PAREN (expression (COMMA expression)*)? RIGHT_PAREN;

return_Type: type_specifier;

function_name: IDENTIFIER;

func_decl_member: type_specifier IDENTIFIER;

//���(��)
statement_list: statement*;

statement
    : simple_statement
    | compoud_statement
    ;

simple_statement
    :   function_definition_statement
    |   basic_statement SEMICOLON
    |   selection_statement
    |   switch_statement
    |   case_label
    |   iteration_statement
    |   jump_statement
    ;

compoud_statement:  LEFT_BRACE statement_list RIGHT_BRACE;

basic_statement
    :   declaration_statement
    |   assignment_statement
    |   expression_statement
    ;

//�������(����ʼ��)
declaration_statement
    :   struct_declaration
    |   simple_declaration
    |   function_declaration
    ;

simple_declaration
	:	(type_qualifier? type_specifier  simple_declarator (COMMA simple_declarator)*)
	|	type_qualifier
	;
simple_declarator: left_value array_specifier* (assignment_expression)?;

struct_declaration: type_qualifier? STRUCT IDENTIFIER LEFT_BRACE (simple_declaration SEMICOLON)+ RIGHT_BRACE;

//�����������
function_definition_statement: function_definition;

//��ֵ���
assignment_statement: left_value array_struct_selection? (assignment_expression | arithmetic_assignment_expression);

//����ʽ���
expression_statement: expression;

//����ѡ�����
selection_statement:  IF LEFT_PAREN expression RIGHT_PAREN selection_rest_statement ; 
selection_rest_statement: statement (ELSE statement)? ; 

//switch���
switch_statement: SWITCH LEFT_PAREN expression RIGHT_PAREN LEFT_BRACE statement_list RIGHT_BRACE;

case_label
    : CASE expression COLON #case
    | DEFAULT COLON #default
    ;

//ѭ�����
iteration_statement
    :   WHILE LEFT_PAREN expression RIGHT_PAREN statement #while
    |   DO statement WHILE LEFT_PAREN expression RIGHT_PAREN SEMICOLON #do
    |   FOR LEFT_PAREN for_init_statement for_cond_statement for_rest_statement RIGHT_PAREN statement #for
    ;

for_init_statement
    :   (basic_statement (',' basic_statement)*)? SEMICOLON
    ;

for_cond_statement: expression SEMICOLON;

for_rest_statement: (basic_statement (',' basic_statement)*)? ;

//��ת���
jump_statement
    :   CONTINUE SEMICOLON #continue
    |   BREAK SEMICOLON #break
    |   RETURN SEMICOLON #return
    |   RETURN expression SEMICOLON #return
    ;

/**
 *�ʷ�
 */

STRUCT: 'struct';

IF: 'if';
ELSE: 'else';
QUESTION: '?';

FOR: 'for';
DO: 'do';
WHILE: 'while';


CONTINUE: 'continue';
BREAK: 'break';
RETURN: 'return';

SWITCH: 'switch';
CASE: 'case';
DEFAULT: 'default';

LEFT_PAREN: '(';
RIGHT_PAREN: ')';

LEFT_BRACE: '{';
RIGHT_BRACE: '}';

LEFT_BRACKET: '[';
RIGHT_BRACKET: ']';

DOT: '.';
COLON: ':';
SEMICOLON: ';';
COMMA: ',';
SHARP: '#';

//Ԫ����
DECIMAL: [1-9]  DIGIT* INTEGER_SUFFIX?;
OCTAL: '0' OCTAL_DIGIT* INTEGER_SUFFIX?;
HEX:  ('0x' | '0X') HEX_DIGIT+ INTEGER_SUFFIX?;

FLOAT_NUM
    :   DIGIT+ DOT DIGIT* EXPONENT? FLOAT_SUFFIX?
    |   DOT DIGIT+ EXPONENT? FLOAT_SUFFIX?
    |   DIGIT+ EXPONENT FLOAT_SUFFIX?
    ;

//Ԫ��������
SCALA
    :   'bool'
    |   'int'
    |   'uint'
    |   'float'
    |   'double'
    ;

VECTOR: ('d'|'i'|'b'|'u')? 'vec' [2-4];

MATRIX: 'd'? 'mat'[2-4] ('x'[2-4])?;

FLOAT_OPAQUE: BASIC_OPAQUE_TYPE |
    ( 'sampler1DShadow' | 'sampler2DShadow' | 'sampler2DRectShadow'
    | 'sampler1DArrayShadow' | 'sampler2DArrayShadow' |
      'samplerCubeShadow' | 'samplerCubeArrayShadow');

INT_OPAQUE: 'i'BASIC_OPAQUE_TYPE;

U_INT_OPAQUE: 'u'BASIC_OPAQUE_TYPE | 'atomic_uint';

BASIC_OPAQUE_TYPE:  ('sampler' | 'image')
    ('1D'|'2D'|'3D'|'Cube'|'2DRect'|'1DArray'|'2DArray'|'Buffer'|'2DMS'|'2DMSArray'|'CubeArray');

//����ʽ
INCREMENT_OP : '++' | '--';

UNARY_OP :  '~' | '!';

MULDIV_OP : '*' | '/' | '%';

ADDSUB_OP : '+' | '-';

SHIFT_OP : '<<' | '>>' ;

COMPARE_OP : '<' | '>' | '<=' | '>=';

EQUAL_OP:   '==' | '!=';

BITWISE_OP: '&' | '^' | '|';

LOGIC_OP:   '&&'| '^^' | '||';

ASSIGNMENT_OP: '=';

ARITHMETIC_ASSIGNMENT_OP
    :   MULDIV_OP ASSIGNMENT_OP
    |   ADDSUB_OP ASSIGNMENT_OP
    |   SHIFT_OP ASSIGNMENT_OP
    |   BITWISE_OP ASSIGNMENT_OP
    ;

/**
 *�����ʷ�
 */

fragment
DIGIT:  [0-9];

fragment
HEX_DIGIT : [0-9]| [a-f] | [A-F] ;

fragment
OCTAL_DIGIT : [0-7];

fragment
INTEGER_SUFFIX: 'u' | 'U';

fragment
EXPONENT : ('e'|'E') ADDSUB_OP? ('0'..'9')+ ;

fragment
FLOAT_SUFFIX: 'f' | 'F' | 'lf' | 'LF';


fragment
LETTER
    :   [a-z]
    |   [A-Z]
    |   '_'
    ;

IDENTIFIER
    :   LETTER (LETTER|DIGIT)*
    ;


//ע��
COMMENT
    :   '/*' .*? '*/'    -> channel(HIDDEN) // match anything between /* and */
    ;
WS  :   [ \r\t\u000C\n]+ -> channel(HIDDEN)
    ;

LINE_COMMENT
    : '//' ~[\r\n]* '\r'? '\n' -> channel(HIDDEN)
    ;
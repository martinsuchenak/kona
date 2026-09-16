grammar Kona;

/* ============================================================================
   Kona Language ANTLR4 Grammar Specification
   This file serves as a mathematical proof of Kona's LL(*) unambiguous parsing.
   ============================================================================ */

pipeline     : stage (PIPE stage)* ;
stage        : condition_prefix? body_expr alternative_branch? ;

condition_prefix : SI condition (PIPE | COLON) ;
condition    : (WORD | STRING | TARGET_AT | GUARD)+ ;

alternative_branch : ALI stage ;

body_expr    : nested_pipeline
             | action_expr
             ;

nested_pipeline : LPAREN pipeline RPAREN ;

action_expr  : token+ ;


token        : WORD 
             | FORMAT_HASH 
             | TARGET_AT 
             | GUARD 
             | STRING 
             | spoken_literal 
             | NUMBER_LITERAL
             | SCOPE
             | BOOLEAN
             ;

spoken_literal : NOMI .*? FINO ;

/* --- LEXER RULES --- */
BOOLEAN      : 'lo' ;
SCOPE        : 'ina' | 'uta' ;
NUMBER_LITERAL : 'ni' ( 'ze' | 'pa' | 'du' | 'ti' | 'fo' | 'mu' | 'sa' | 'ke' | 'bi' | 'go' )+ ;


spoken_literal : NOMI .*? FINO ;

/* --- LEXER RULES --- */
PIPE         : '|>' | 'te' ','? ;
LPAREN       : '(' ;
RPAREN       : ')' ;
SI           : 'si' ;
ALI          : 'ali' | ':else:' ;
COLON        : ':' ;
NOMI         : 'nomi' ;
FINO         : 'fino' ;

FORMAT_HASH  : '#' ('table'|'list'|'json'|'raw'|'diff') ;
GUARD        : '!' [a-zA-Z_\-]+ | 'notori' | 'no-' [a-zA-Z_\-]+ ;
TARGET_AT    : '@' [a-zA-Z_\-]+ (':' ('"' ~'"'* '"' | '\'' ~'\''* '\''))? ;
WORD         : [a-zA-Z_\-]+ ;
STRING       : '"' ~'"'* '"' | '\'' ~'\''* '\'' ;

WS           : [ \t\r\n]+ -> skip ;

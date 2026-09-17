grammar Kona;

/* ============================================================================
   Kona Language -- ANTLR4 Reference Grammar

   Scope note: this file is a machine-checkable statement of Kona's SURFACE
   syntax -- how an utterance is tokenised and how stages, conditions and
   nested pipelines nest. It is not, and does not claim to be, a proof of
   semantic unambiguity.

   Unambiguity in Kona rests on two things this context-free grammar cannot
   express, both of which are enforced in kona.py and covered by tests:

     1. LEXICAL CLOSURE. `word` below matches any identifier. The parser
        accepts only words present in the lexicon (ACTIONS, TARGETS, MODIFIERS,
        FORMATS, PARTICLES) or derivable from one by a documented affix rule.
        Everything else is a syntax error. See Parser.parse_action_expr.

     2. WHOLE-WORD-FIRST RESOLUTION. A word that is itself a lexeme is never
        decomposed, so roots that merely begin with a modifier (veba, rego,
        nolo, debi) cannot be mis-segmented as ve+ba, re+go, no+lo, de+bi.
        Decomposition is attempted only when whole-word lookup fails.

   A previous version of this file asserted it was "a mathematical proof of
   Kona's LL(*) unambiguous parsing". It was not: it defined `spoken_literal`
   twice (so ANTLR would reject it outright) and its action rule was `token+`,
   which accepts arbitrary word salad and therefore proves nothing.
   ============================================================================ */

// --- PARSER RULES ---------------------------------------------------------

utterance    : pipeline EOF ;

pipeline     : stage (PIPE stage)* ;

stage        : conditionPrefix? body alternativeBranch? ;

conditionPrefix : SI condition PIPE ;

condition    : element+ ;

alternativeBranch : ALI stage ;

body         : nestedPipeline
             | actionExpr
             ;

nestedPipeline : LPAREN pipeline RPAREN ;

/* An action expression is a sequence of elements carrying at most one matrix
   predicate. The one-predicate-per-stage rule, and the clause particles that
   license a subordinate predicate, are enforced in the parser -- see
   CLAUSE_PARTICLES and MODALS in kona.py. */
actionExpr   : element+ ;

element      : WORD
             | STRING
             | TARGET_AT
             | FORMAT_HASH
             | GUARD
             | spokenLiteral
             | SI
             ;

spokenLiteral : NOMI ( WORD | STRING )* FINO ;

// --- LEXER RULES ----------------------------------------------------------

/* PIPE must precede WORD so that a standalone 'te' is a stage separator while
   'teli' remains a single word (ANTLR prefers the longest match, then the
   earliest rule). ';' is an utterance separator equivalent to spoken 'te,'. */
PIPE         : '|>' | 'te' WS* ',' | 'te' | ';' ;

LPAREN       : '(' ;
RPAREN       : ')' ;

SI           : 'si' ;
ALI          : 'ali' | ':else:' ;
NOMI         : 'nomi' ;
FINO         : 'fino' ;

FORMAT_HASH  : '#' ( 'table' | 'list' | 'json' | 'raw' | 'diff' ) ;

/* '!"literal"' is the shorthand counterpart of spoken 'notori "literal"'. */
GUARD        : '!' STRING
             | '!' IDENT
             | 'notori'
             | 'no-' IDENT
             ;

TARGET_AT    : '@' IDENT ( ':' ( STRING | IDENT ) )? ;

/* Dotted and hyphenated affixation (kwe.de, su-kwe) is one word. */
WORD         : IDENT ( ( '.' | '-' ) IDENT )* ;

STRING       : '"' ~'"'* '"' | '\'' ~'\''* '\'' ;

fragment IDENT : [a-zA-Z_] [a-zA-Z0-9_]* ;

/* A bare comma is a prosodic clause pause with no semantic content. */
COMMA        : ',' -> skip ;

WS           : [ \t\r\n]+ -> skip ;

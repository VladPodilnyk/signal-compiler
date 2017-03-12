# Translator(part of the compiler development course at NTUU "KPI")
## Grammar of the input language
_<signal-program> --> <program>_
_<program> --> PROGRAM <procedure-identifier> ;_
_<block>._
_<block> --> <variable-declarations> BEGIN_
_<statements-list> END_
<variable-declarations> --> VAR <declarations-
list> | <empty>
<declarations-list> --> <declaration> <declara-
tions-list> |
<empty>
<declaration> -→<variable-identifier> :
INTEGER ;
<statements-list> --> <statement> <statements-
list> |
<empty>
<statement> --> <variable-identifier> := <condi-
tional-expression> ;
<conditional-expression> --> <logical-summand>
<logical>
<logical> --> OR <logical-summand> <logical> |
<empty>
<logical-summand> --> <logical-multiplier> <log-
ical-multipliers-list>
<logical-multipliers-list> --> AND <logical-mul-
tiplier> <logical-multipliers-list> |
<empty>
<logical-multiplier> --> <expression><comparsion-operator><expression> |
[ <conditional-expression> ] |
NOT <logical-multiplier>
<comparison-operator> --> < | <= | = | <> | >= | >
<expression> --> <variable-identifier> | <unsigned-integer>
<variable-identifier> --> <identifier>
<procedure-identifier> --> <identifier>
<identifier> --> <letter><string>
<string> --> <letter><string> |  <digit><string> | <empty>
<unsigned-integer> --> <digit><digits-string>
<digits-string> --> <digit><digits-string> | <empty>
<digit> --> 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
<letter> --> A | B | C | D | ... | Z

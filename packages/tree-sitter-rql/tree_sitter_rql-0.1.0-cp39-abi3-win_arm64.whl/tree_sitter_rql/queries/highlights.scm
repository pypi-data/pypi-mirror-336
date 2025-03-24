;; Keywords
(order_expression "order_by" @keyword)
(logical_operator) @keyword
(comparison_operator) @operator
(SIGN) @operator

;; Boolean and constants
(BOOLEAN) @constant.builtin
(NULL_LITERAL) @constant.builtin
(EMPTY_LITERAL) @constant.builtin

;; Numbers and dates
(DATETIME) @constant.numeric
(DATE) @constant.numeric
(FLOAT) @constant.numeric
(INT) @constant.numeric

;; Property names
(property) @variable

;; Literals (strings, numbers)
(literal) @string

;; Any expression operator
(any_expression) @keyword

;; Grouped expressions (parentheses)
(grouped_expression "(" @punctuation.bracket ")" @punctuation.bracket)

;; Tuples and list delimiters
(tuple "(" @punctuation.bracket "," @punctuation.delimiter ")" @punctuation.bracket)

;; Logical and comparison arguments (comma-separated lists)
(argument_list "," @punctuation.delimiter)
(order_list "," @punctuation.delimiter)

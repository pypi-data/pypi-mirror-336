import re

# 匹配以数字、逗号或点结尾的字符串，且长度至少为2
PATTERN_NUMERIC_COMMA_DOT_END = re.compile(r"[0-9,.]{2,}$")

# 匹配长度为1或2的小写字母字符串
PATTERN_SHORT_ALPHA = re.compile(r"[a-z]{1,2}$")

# 匹配包含数字和连字符的字符串
PATTERN_NUMERIC_HYPHEN = re.compile(r"[0-9-]+")

# 匹配包含小写字母、点、空格或连字符的字符串
PATTERN_ENGLISH_CHARS = re.compile(r"[a-z. -]+$")

# 匹配包含数字、点、空格或连字符的字符串，且长度至少为2
PATTERN_SPECIAL_NUMERIC = re.compile(r"[0-9. -]{2,}$")

# 匹配以字母结尾的字符串
PATTERN_ENDS_WITH_LETTER = re.compile(r".*[a-zA-Z]$")

# 匹配以数字结尾的字符串
PATTERN_DIGIT_END = re.compile(r"[0-9]$")

# 匹配长度为1或2的数字或小写字母字符串
PATTERN_SHORT_ALNUM = re.compile(r"[0-9a-z]{1,2}$")

# 匹配包含数字或字母的字符串
PATTERN_ALNUM = re.compile(r"[0-9a-zA-Z]")

# 匹配空格或制表符
PATTERN_WHITESPACE = re.compile(r"[ \t]+")

# 匹配分割字符（包括特殊字符、小写字母、数字等）
PATTERN_SPECIAL_CHARS = re.compile(r"[~—\t @#%!<>,\.\?\":;'\{\}\[\]_=\(\)\|，。？》•●○↓《；‘’：“”【¥ 】…￥！、·（）×`&\\/「」\\]")

# 匹配小写字母字符串
PATTERN_SMALL_ALNUM = re.compile(r"[a-z]+$")

# 匹配下划线
PATTERN_LOWER_LINE = re.compile(r"_")

# 匹配小写字母、点或连字符的字符串
PATTERN_LOWERCASE_DOT_HYPHEN = re.compile(r"[a-z\.-]+$")

# 匹配包含字母、下划线或连字符的字符串
PATTERN_ALPHA_UNDERSCORE_HYPHEN = re.compile(r"[a-zA-Z_-]+$")

# 匹配非单词字符
PATTERN_NON_WORD_CHARS = re.compile(r"\W+")

# 匹配包含数字、点或连字符的字符串
PATTERN_NUMERIC_PERIOD_HYPHEN = re.compile(r"[0-9\.-]+$")

# 匹配包含数字、逗号、点或连字符的字符串
PATTERN_NUMERIC_COMMA_DOT_HYPHEN = re.compile(r"[0-9,\.-]+$")

# 匹配换行符
PATTERN_NEWLINE = re.compile(r"[\r\n]+")

# 匹配空格或制表符
PATTERN_SPACE_TAB = re.compile(r"[ \t]+")

# 匹配分割字符（包括特殊字符、小写字母、数字等）
PATTERN_SPLIT_CHARS = re.compile(
    r"([ ,\.<>/?;:'\[\]\\`!@#$%^&*\(\)\{\}\|_+=《》，。？、；‘’：“”【】~！￥%……（）——-]+|[a-z\.-]+|[0-9,\.-]+)")

# 匹配空格
PATTERN_SPACE = re.compile(r"[ ]+")

# 匹配仅由字母组成并以字母结尾的字符串
PATTERN_ALPHA_ONLY_END = re.compile(r"[a-zA-Z]+$")

# 匹配单个小写字母或数字的字符串
PATTERN_SINGLE_LOWERCASE_ALNUM = re.compile(r"^[a-z0-9]$")

# 匹配空格、反斜杠、双引号、单引号或脱字符中的任意一个字符
PATTERN_SPECIAL_CHARS_SPACE_QUOTES_CARET = re.compile(r"[ \\\"'^]")

# 匹配以加号或减号开头的字符串
PATTERN_STARTS_WITH_PLUS_OR_MINUS = re.compile(r"^[\+-]")

# 匹配点号、脱字符、加号、括号或减号中的任意一个字符
PATTERN_SPECIAL_CHARS_DOT_CARET_PLUS_PAREN_HYPHEN = re.compile(r"[.^+\(\)-]")

# 匹配由数字、小写字母、点号、加号、井号、下划线、星号或减号组成的字符串，且字符串必须以这些字符结尾
PATTERN_ALNUM_SPECIAL_CHARS_END = re.compile(r"[0-9a-z\.\+#_\*-]+$")

# 匹配包含各种标点符号（中英文）和特殊字符的字符串
PATTERN_PUNCTUATION_AND_SPECIAL_CHARS = re.compile(
    r"[ ,\./;'\[\]\\`~!@#$%\^&\*\(\)=\+_<>\?:\"\{\}\|，。；‘’【】、！￥……（）——《》？：“”-]+")

# 匹配转义字符，包括空格、反斜杠、双引号和单引号
PATTERN_ESCAPE_CHAR = re.compile(r"[ \\\"']+")

# 匹配一组特殊符号，如冒号、花括号、方括号、星号等
PATTERN_SPECIAL_SYMBOLS = re.compile(r"([:\{\}/\[\]\-\*\"\(\)\|\+~\^])")

# 匹配中文常见的疑问词和结构
PATTERN_STOPWORD = [(re.compile(
    r"是*(什么样的|哪家|一下|那家|请问|啥样|咋样了|什么时候|何时|何地|何人|是否|是不是|多少|哪里|怎么|哪儿|怎么样|如何|哪些|是啥|啥是|啊|吗|呢|吧|咋|什么|有没有|呀|谁|哪位|哪个)是*"),
                     ""), (re.compile(r"(^| )(what|who|how|which|where|why)('re|'s)? "), " "), (re.compile(
    r"(^| )('s|'re|is|are|were|was|do|does|did|don't|doesn't|didn't|has|have|be|there|you|me|your|my|mine|just|please|may|i|should|would|wouldn't|will|won't|done|go|for|with|so|the|a|an|by|i'm|it's|he's|she's|they're|you're|as|by|on|in|at|up|out|down|of|to|or|and|if) "),
                                                                                                " ")]

PATTERN_SPECIAL_CHARACTERS = re.compile(r"[ :|\r\n\t,，。？?/`!！&^%%()\[\]{}<>]+")

NON_ALNUM_SPACE_PATTERN = re.compile(r"([^a-z0-9.,\)>]) +([^ ])")

NON_SPACE_FOLLOWED_BY_NON_ALNUM_PATTERN = re.compile(r"([^ ]) +([^a-z0-9.,\(<])")

__author__ = 'aortegag'
import re


class Precedence:
    # 5 is the highest precedence
    PARENTHESIS = 5
    KLEENE = 4
    CONCAT = 3
    UNION = 2


def precedence(op):
    if op == "(" or op == ")":
        return Precedence.PARENTHESIS
    if op == "+":
        return Precedence.UNION
    if op == ".":
        return Precedence.CONCAT
    if op == "*":
        return Precedence.KLEENE
    return Precedence.CONCAT


def is_operator(c):
    if c == '(' or c == ')' or c == '*' or c == "+" or c == ".":
        return True
    return False


def invert_parenthesis(s):
    result = ""
    for c in s:
        if c == "(":
            result += ")"
        elif c == ")":
            result += "("
        else:
            result += c
    return result


def add_concatenation_dot(s):
    """
    Adds the character '.' in the positions that correspond for a concatenation.
    Such character '.' is needed to have an internal representation of concatenation
    which we can detect and handle.
    :param s: Regular expression
    :return: Regular expression with '.'s representing concatenation
    """
    pattern = re.compile(r'[a-zA-Z0-9#%][a-zA-Z0-9#%]|\)\(|\*[a-zA-Z0-9#%]|\*\(|[a-zA-Z0-9#%]\(|\)[a-zA-Z0-9#%]')
    res = pattern.search(s)
    while (res):
        target_str = res.group()
        s = re.sub(pattern, target_str[0] + "." + target_str[1], s, count=1)
        res = pattern.search(s)
    return s


def validate_operator_position(s):
    """
    Checks for specific error conditions according to our requirements for the position
    of the operators. Such rules does not necessarily match to the ones established
    in Python regular expressions.
    :param s: The regular expression
    :return: nothing
    :raises: An exception when this is a malformed regex
    """
    pattern = re.compile(r'\+{2,}|\(\+|\+\)|\+$|^\+|^\*|\+\*|\(\*|^\)|\($')
    res = pattern.search(s)
    if res:
        raise Exception("invalid regex")

def validate_empty_parenthesis(s):
    """
    This is a very specific corner case in which the user provides a parenthesis with
    nothing inside: () should translate to (#) and ()() to (#)(#)
    :param s: The regular expression
    :return: The regular expression with # inside empty parenthesis (#)
    """
    pattern = re.compile(r'\(\)')
    res = pattern.search(s)
    while (res):
        target_str = res.group()
        s = re.sub(pattern, target_str[0] + "#" + target_str[1], s, count=1)
        res = pattern.search(s)
    return s


def infix_to_prefix(re_expr):
    """
    Converts a regular expression from infix notation to a prefix notation.
    :param re_expr: String representing a regular expression in infix notation
    :return: regular expression in prefix notation
    """
    if len(re_expr) == 0:
        return str("#")
    stack = []
    result = ""
    unbalanced = 0
    # It's mandatory to remove whitespaces FIRST
    re_expr = re.sub(r'\s+', '', re_expr)

    valid = ["#", "+", "(", ")", "*", ".", "%"]
    for c in re_expr:
        if c not in valid and not c.isalnum():
            raise Exception(
                "Caracter invalido {0} en expresion regular {1}.\nSolo se permiten caracteres alfanumericos.".format(c,
                                                                                                                  re_expr))

    validate_operator_position(re_expr)
    re_expr = add_concatenation_dot(re_expr)
    re_expr = validate_empty_parenthesis(re_expr)
    # reverse string and then invert parenthesis
    re_expr = invert_parenthesis(re_expr[::-1])

    for c in re_expr:
        if is_operator(c):
            if c is "(":
                unbalanced += 1
                stack.append(c)
                continue

            if c is ")":
                unbalanced -= 1
                while True and len(stack) > 0:
                    next = stack.pop()
                    if next is "(":
                        break
                    result += next
                continue

            while stack and (precedence(stack[-1]) >= precedence(c)) and stack[-1] != "(":
                if stack[-1] == "*" and c == "*":  # special case for kleene as it's a unary operator
                    break
                top = stack.pop()
                if top != "(" and top != ")":
                    result += top
            stack.append(c)
        else:
            result += c

    if unbalanced:
        raise Exception("Parentesis no balanceado")

    while stack:
        result += stack.pop()

    # Revert regex again so we can read it in prefix notation
    return result[::-1]

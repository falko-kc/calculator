from collections import deque

def inf_to_postf(inp_list):
    op_stack = deque()
    result = []

    for i in inp_list:
        if i not in "+-*/)(":  # i.isnumeric() or i.isalpha():
            result.append(i)
        elif i == "(":
            op_stack.append(i)
        elif i == ")":
            while True:
                op = op_stack.pop()
                if op == "(":
                    break
                else:
                    result.append(op)
        else:  # i is in "+-*/"
            if len(op_stack) == 0:
                op_stack.append(i)
            else:
                op = op_stack.pop()  # check top element from stack
                if op == "(":
                    op_stack.append(op)
                    op_stack.append(i)
                elif i in "*/" and op in "+-":  # i has higher precedence than top of stack
                    op_stack.append(op)
                    op_stack.append(i)
                elif op in "*/" or (op in "+-" and i in "+-"):  # i can only be of lower or equal precedence
                    result.append(op)
                    while len(op_stack) > 0:
                        op_next = op_stack.pop()
                        if op_next == "(":
                            op_stack.append(op_next)
                            op_stack.append(i)
                            break
                        elif op_next in "+-" and i in "*/":
                            op_stack.append(op_next)
                            op_stack.append(i)
                            break
                        else:
                            result.append(op_next)
                    op_stack.append(i)  # muss i hier wirklich in den stack?

    while len(op_stack) > 0:
        op = op_stack.pop()
        result.append(op)

    return result


def postfix_eval(inp_list):
    # global variables
    calc_stack = deque()

    op = {'+': lambda x, y: x + y,
          '-': lambda x, y: x - y,
          '*': lambda x, y: x * y,
          '/': lambda x, y: x / y}

    for i in inp_list:
        if i.lstrip('+-').isalpha():
            calc_stack.append(call_dict(i))
        elif i not in "+-*/": # i.isnumeric()
            calc_stack.append(i)
        else:   # i is operator "+-*/"
            num1 = int(calc_stack.pop())
            num2 = int(calc_stack.pop())
            res = op[i](num2,num1)    # Attention: Order of x and y is important!
            calc_stack.append(res)

    return calc_stack.pop()


def check_signs(inp_str):
    if "+" in inp_str and "-" not in inp_str:
        return "+"
    elif "-" in inp_str:
        if inp_str.count("-") % 2 == 0:
            return "+"
        else:
            return "-"

def assign_minus(inp_list):
    new_list = []
    sign = False
    for i in range(0, len(inp_list)):
        if inp_list[i] == "-":
            sign = True
        elif sign:
            new_list.append(inp_list[i] * -1)
            sign = False
        else:
            new_list.append(inp_list[i])
    return new_list

def call_dict(item):
    global variables
    try:
        if item.startswith("-"):
            return variables[item.lstrip("-")] * -1
        else:
            return variables[item]
    except KeyError:
        print("Unknown variable")

def cmd_mode(list_in):
    if list_in[0] == "/exit":
        print("Bye!")
        exit()
    elif list_in[0] == "/help":
        print("The calculator supports multiplication, integer division and parentheses.")
    else:
        print("Unknown command")


def expr_mode(list_in):    # list_in wont contain "=" signs, but only RHS equations (already split at spaces)
    global variables
    if True in [(x[0].isdigit() or x[0].isalpha()) and (x.endswith('+') or x.endswith('-')) for x in list_in]:
        return "Invalid expression"   # e.g. "a-" or "3+"   # but included in next row isnt it?
    elif True in [not x.lstrip("+-").isalpha() and not x.lstrip("+-").isnumeric()
                  and x.strip("+-*/") != "" and x != "(" and x != ")" for x in list_in]:
        return "Invalid expression"
    elif len(list_in) == 1:
        if list_in[0].lstrip('+-').isalpha():
            return call_dict(list_in[0])
        else:
            return int(list_in[0])
    else:
        check_pos = [i for i in list_in if (i.lstrip("+-").isnumeric() or i.lstrip("+-").isalpha() or "-" in list(i))]
        check_neg = [check_signs(i) if not (i.lstrip("+").lstrip("-").isnumeric() or i.lstrip("+").lstrip("-").isalpha()) else i for i in check_pos]
        check_posa = [x.lstrip("+") for x in check_neg]
        check3 = [i for i in check_posa if (str(i).lstrip("-").isnumeric() or i.lstrip("-").isalpha() or "-" in list(i))]
        check4 = [call_dict(x) if x.lstrip('+-').isalpha() else x for x in check3]
        check5 = [int(i) if str(i).lstrip("-").isnumeric() else i for i in check4]
        numbers = assign_minus(check5)
        return sum(numbers)


def assgn_mode(list_in):
    global variables
    if len(list_in) > 2:
        print("Invalid assignment")
    elif False in [x.isalpha() for x in list_in[0]]:  # check if non-latin letters exist (on every letter of LHS) no neg. var possible)
        print("Invalid identifier")
    else:
        LHS = list_in[0]
        RHS = expr_mode(list_in[1].split())
        if not isinstance(RHS, int):
            print(RHS)
        else:
            variables[LHS] = RHS   # dict keys are case sensitive, so LHS can be used directly


variables = {}
def main():
    variables.clear()
    while True:
        try:
            inp = input().replace("(", " ( ").replace(")", " ) ")
            inp_list = inp.split()
        except Exception:
            print("Invalid expression")  #  isdigit(), isalpha()
        else:
            if not inp_list:   # empty input list
                continue
            elif inp_list[0].startswith('/'):
                cmd_mode(inp_list)
            elif True in ["=" in x for x in inp_list]:
                strip_list = [x.strip() for x in inp.split("=")]  # input is divided into LHS and RHS of equation
                assgn_mode(strip_list)
            else:
                print(expr_mode(inp_list))

if __name__ == '__main__':
    main()

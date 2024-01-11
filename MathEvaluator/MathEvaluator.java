import java.util.*;

public class MathEvaluator {

    public static int getPrecedence(Character token) {
        switch (token) {
            case '~': // unary minus
                return 101; // Greater than 100 means "unary"
            case '*':
                return 2;
            case '/':
                return 2;
            case '+':
                return 1;
            case '-':
                return 1;
            default: // not an operator / parentheses
                return 0;
        }
    }

    public static double evalSimpleExpr(String operator, double a, double b) { 
        // a and b are reversed due to the special structure of a stack
        switch (operator) {
            case "*":
                return b * a;
            case "/":
                if (a == 0)
                    return 0;
                return b / a;
            case "+":
                return b + a;
            case "-":
                return b - a;
            case "~":
                return -a; // b is ignored since it is not used
            default:
                return 0;
        }
    }

    public static double calculate(String expression) {

        char[] characters = expression.replaceAll("\\s+", "").toCharArray(); // remove whitespaces and convert the characters into an array

        List<String> output = new ArrayList<>();
        Stack<Character> ops = new Stack<>();

        for (int i = 0; i < characters.length; i++) {

            char token = characters[i];

            if (Character.isDigit(token) || token == '.') {

                String digits = "";
                // Collect all digits and decimal points for the number
                for (; i < characters.length && (Character.isDigit(characters[i]) || characters[i] == '.'); i++) digits += characters[i]; 
                i--; // get the loop to the good index

                output.add(digits);

            } else if (token == '(') {
                ops.push(token);

            } else if (token == ')') {
                while (!ops.empty() && ops.peek() != '(') {
                    output.add(Character.toString(ops.pop()));
                }
                ops.pop();

            } else if (token == '+' || token == '-' || token == '*' || token == '/') {
                // determine whether the operator is unary
                if (i == 0 || getPrecedence(characters[i - 1]) > 0 || characters[i - 1] == '(') {
                    if (token == '-') { // unary minus (negative sign)
                        ops.push('~');
                    } else continue; // ignore unary plus (no effect)
                } else { // add the operator to the correct place in the stack while respecting the operators' precedence rules.
                    while (!ops.empty() && getPrecedence(ops.peek()) >= getPrecedence(token)) {
                        output.add(Character.toString(ops.pop()));
                    }
                    ops.push(token);
                }
            }
        }

        // push the rest of the operators from the stack to the output queue
        while (!ops.empty()) {
            output.add(Character.toString(ops.pop()));
        }

        return postfixEval(output);
    }

    // evaluating the postfix expression
    public static double postfixEval(List<String> postfix) {

        Stack<Double> stack = new Stack<>();

        for (String element : postfix) {
            int prec = getPrecedence(element.charAt(0));
            if (prec > 100) { // negative sign
                stack.push(evalSimpleExpr(element, stack.pop(), 0));
            } else if (prec > 0 && prec < 100) { // operator
                stack.push(evalSimpleExpr(element, stack.pop(), stack.pop()));
            } else { // number
                stack.push(Double.parseDouble(element));
            }
        }
        return stack.pop();
    }

    // test
    public static void main(String[] args) {
        System.out.println(calculate("15+2*-12-(0.5+0.8*(8-1))/-0.1+0.5+0.5"));
        System.out.println(calculate("12* 123/-(-5 + 2)"));
        System.out.println(calculate("1 - -(-(-(-4)))"));
    }

}
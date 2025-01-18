mport sympy as sp
import re
import ast
from typing import Any, Callable

class CLIHandler:
    def get_user_input(self) -> str:
        return input("Введіть математичний вираз або рівняння: ")

    def display_result(self, result: Any) -> None:
        print(f"Результат: {result}")

    def display_error(self, error: Exception) -> None:
        print(f"Помилка: {error}")

    def ask_to_continue(self) -> bool:
        while True:
            response = input("Бажаєте обчислити новий вираз? (так/ні): ").strip().lower()
            if response in {"так", "yes", "y", "т"}:
                return True
            elif response in {"ні", "no", "n", "н"}:
                return False
            print("Невірна відповідь, введіть 'так' або 'ні'.")

    def display_help(self) -> None:
        help_text = """
        Доступні команди:
        
        1. help
           Опис: Виводить цю сторінку допомоги.

        2. Введення виразу
           Опис: Введіть математичний вираз для обчислення, наприклад: 5+3*(8-6).
           - Допустимі операції: +, -, *, /, ^
           - Допустимі символи: цифри, дужки.
        
        3. Введення рівняння
           Опис: Введіть рівняння, наприклад: x+3=7, і програма розв'яже його.
           - Змінна повинна бути вказана як x
           - Програма надасть розв'язок рівняння.
        
        4. Обчислення результату
           Опис: Після введення виразу або рівняння, програма обчислює результат.

        5. Вихід з програми
           Опис: Для виходу з програми введіть "ні" на запит про продовження.
        """
        print(help_text)

class Core:
    def __init__(self):
        self.parser = ExpressionParser()
        self.tree_builder = TreeBuilder()
        self.evaluator = ExpressionEvaluator()
        self.cli = CLIHandler()

    def run(self) -> None:
        print("Для отримання допомоги введіть 'help'.")
        while True:
            try:
                user_input = self.cli.get_user_input().strip().lower()
                if user_input == "help":
                    self.cli.display_help()
                    continue  

                if '=' in user_input: # Перевірка на рівняння
                    result = self.solve_equation(user_input)
                else:
                    parsed_expr = self.parser.parse(user_input)
                    expression_tree = self.tree_builder.build(parsed_expr)
                    result = self.evaluator.evaluate(expression_tree)

                self.cli.display_result(result)
            except ValueError as ve:
                self.cli.display_error(ve)
            except Exception as e:
                self.cli.display_error(e)

            if not self.cli.ask_to_continue():
                print("Дякуємо за використання програми! До побачення!")
                break
        
        def solve_equation(self, equation: str) -> Any:
        lhs, rhs = equation.split('=')
        lhs_expr = sp.sympify(lhs.strip())
        rhs_expr = sp.sympify(rhs.strip())
        
        symbol = sp.symbols('x') # Розв'язання рівняння в SymPy 
        eq = sp.Eq(lhs_expr, rhs_expr)
        solution = sp.solve(eq, symbol)
        if solution:
            return f"Розв'язок: x = {solution[0]}"
        else:
            return "Немає розв'язку або рівняння має нескінченну кількість розв'язків."

class ExpressionParser: # Компонент для аналізу текстових математичних виразів
    def parse(self, expression: str) -> ast.AST:
        try:
            expression = expression.replace("^", "**")
            parsed_ast = ast.parse(expression, mode='eval').body
            return parsed_ast
        except SyntaxError as e:
            raise ValueError(f"Помилка синтаксиса: {e}")

class TreeBuilder:
    def build(self, node: ast.AST) -> Any:
        if isinstance(node, ast.BinOp):  
            operator = self._get_operator(node.op)
            left = self.build(node.left)
            right = self.build(node.right)
            return (operator, left, right)  
        elif isinstance(node, ast.Constant):  
            return sp.sympify(node.value)
        elif isinstance(node, ast.Name):  
            return sp.Symbol(node.id)
        else:
            raise ValueError(f"Непідтримуваний вузол: {type(node).__name__}")

    def _get_operator(self, op: ast.AST) -> Callable: # Повертає відповідний оператор SymPy для вузла AST
        if isinstance(op, ast.Add):
            return lambda x, y: x + y
        elif isinstance(op, ast.Sub):
            return lambda x, y: x - y
        elif isinstance(op, ast.Mult):
            return lambda x, y: x * y
        elif isinstance(op, ast.Div):
            return lambda x, y: x / y
        elif isinstance(op, ast.Pow):
            return lambda x, y: x ** y
        else:
            raise ValueError(f"Непідтримуваний оператор: {type(op).__name__}")

class ExpressionEvaluator: # Компонент для обчислення та спрощення виразів
    def __init__(self):
        self.custom_functions = {}

    def evaluate(self, expression_tree: Any) -> Any:
        if isinstance(expression_tree, sp.Basic):
            return expression_tree
        elif isinstance(expression_tree, tuple):
            operator, left, right = expression_tree
            left_value = self.evaluate(left)
            right_value = self.evaluate(right)
            return operator(left_value, right_value)
        else:
            return expression_tree

    def simplify(self, expression: Any) -> Any:
        return sp.simplify(expression)

    def add_custom_function(self, name: str, func: Callable) -> None:
        sp.Function(name)(func)
        self.custom_functions[name] = func

if __name__ == "__main__":
    core = Core()
    core.run()


import pytest
from unittest.mock import MagicMock, patch
from main import Core, ExpressionParser, TreeBuilder, ExpressionEvaluator
import sympy as sp
import ast



def test_parse_expression():
    parser = ExpressionParser()
    expr = "5 + 3 * (2 - 1)"
    parsed_expr = parser.parse(expr)
    assert isinstance(parsed_expr, ast.BinOp)


def test_tree_builder():
    builder = TreeBuilder()
    parsed_expr = ast.BinOp(left=ast.Constant(value=5), op=ast.Add(), right=ast.Constant(value=3))
    tree = builder.build(parsed_expr)
    assert tree == ('+', 5, 3)


def test_evaluate_expression():
    evaluator = ExpressionEvaluator()
    expression_tree = ('+', 5, 3)
    result = evaluator.evaluate(expression_tree)
    assert result == 8


def test_solve_equation():
    core = Core(None)
    core.logger = MagicMock()  # Мокування логера
    with patch('builtins.input', return_value='x + 3 = 7'):  # Мокування вводу користувача
        result = core.solve_equation("x + 3 = 7")
    core.logger.info.assert_called_with('Розв\'язок рівняння: [4]')
    assert result == "Розв'язок: x = 4"


def test_solve_invalid_equation():
    core = Core(None)
    core.logger = MagicMock()  
    with patch('builtins.input', return_value='x + 3 ='):  
        with pytest.raises(ValueError):
            core.solve_equation("x + 3 =") 


def test_run_solve_equation():
    core = Core(None)
    core.logger = MagicMock()  
    with patch('builtins.input', return_value='x + 3 = 7'):  
        result = core.solve_equation("x + 3 = 7")
    core.logger.info.assert_called_with('Розв\'язок рівняння: [4]')
    assert result == "Розв'язок: x = 4"


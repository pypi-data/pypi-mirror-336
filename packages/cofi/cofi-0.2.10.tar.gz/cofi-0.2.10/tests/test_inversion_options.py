import pytest

from cofi import InversionOptions
from cofi.tools import BaseInferenceTool


def test_set_unset_solving_method(capsys):
    inv_options = InversionOptions()
    # 0
    inv_options.suggest_tools()
    console_output = capsys.readouterr()
    assert "optimization" in console_output.out
    assert "scipy.linalg.lstsq" in console_output.out
    inv_options.suggest_solving_methods()
    console_output = capsys.readouterr()
    assert "optimization" in console_output.out
    assert "`suggest_tools()` to see a full list of backend tools" in console_output.out
    # 1
    with pytest.raises(ValueError):
        inv_options.set_solving_method("abc")
    with pytest.raises(ValueError, match=".*Did you mean 'optimization'?.*"):
        inv_options.set_solving_method("optimizations")
    # 2
    inv_options.set_solving_method("matrix solvers")
    inv_options.suggest_tools()
    console_output = capsys.readouterr()
    assert "optimization" not in console_output.out
    assert "scipy.linalg.lstsq" in console_output.out
    # 3
    inv_options.unset_solving_method()
    inv_options.suggest_tools()
    console_output = capsys.readouterr()
    assert "optimization" in console_output.out
    assert "scipy.linalg.lstsq" in console_output.out
    # 4
    inv_options.set_solving_method("matrix solvers")
    inv_options.set_solving_method(None)
    inv_options.suggest_tools()
    console_output = capsys.readouterr()
    assert "optimization" in console_output.out
    assert "scipy.linalg.lstsq" in console_output.out


def test_set_unset_tool(capsys):
    inv_options = InversionOptions()
    # 0 - invalid input
    with pytest.raises(ValueError):
        inv_options.set_tool("abc")
    with pytest.raises(ValueError, match=".*Did you mean 'scipy.optimize.minimize'?.*"):
        inv_options.set_tool("scipy.minimize")
    # 1 - mismatch with solving_method
    inv_options.set_solving_method("optimization")
    with pytest.warns(UserWarning):
        inv_options.set_tool("scipy.linalg.lstsq")
    # 2 - unset
    inv_options.unset_tool()
    assert inv_options.tool is None
    # 3 - default without solving_method
    inv_options.unset_solving_method()
    assert inv_options.get_default_tool() == "scipy.optimize.minimize"
    inv_options.suggest_solver_params()
    console_output = capsys.readouterr()
    assert "default" in console_output.out
    assert "Required parameters" in console_output.out
    assert "Optional parameters & default settings" in console_output.out
    # 4 - default given solving_method
    inv_options.set_solving_method("optimization")
    assert inv_options.get_default_tool() == "scipy.optimize.minimize"

    # 5 - suggest solving method
    # 5 - set None
    inv_options.set_tool(inv_options.get_default_tool())
    inv_options.set_tool(None)
    assert inv_options.tool is None
    # 6 - self-defined tool
    class MyOwnSolver(BaseInferenceTool):
        def __init__(self, inv_problem, inv_options): pass
        def __call__(self): return 1

    inv_options.set_tool(MyOwnSolver)
    # 7 - self-defined invalid tool
    class AnotherSolver(BaseInferenceTool):
        def __init__(self, inv_problem, inv_options): pass

    with pytest.raises(ValueError):
        inv_options.set_tool(AnotherSolver)


def test_set_params():
    inv_options = InversionOptions()
    inv_options.set_params(a=3, b=5)
    assert inv_options.get_params()["a"] == 3
    assert inv_options.get_params()["b"] == 5


def test_summary(capsys):
    inv_options = InversionOptions()
    # 0
    inv_options.summary()
    console_output = capsys.readouterr()
    assert "Solving method: None set" in console_output.out
    assert "Solver-specific parameters: None set" in console_output.out
    assert "Backend tool" in console_output.out
    assert "(by default)" in console_output.out
    # 1
    inv_options.set_solving_method("optimization")
    inv_options.summary()
    console_output = capsys.readouterr()
    assert "Solving method: optimization" in console_output.out
    assert "Solver-specific parameters: None set" in console_output.out
    assert "Backend tool" in console_output.out
    assert "(by default)" in console_output.out
    # 2
    inv_options.set_tool(inv_options.get_default_tool())
    inv_options.summary()
    console_output = capsys.readouterr()
    assert "Solving method: optimization" in console_output.out
    assert "Solver-specific parameters: None set" in console_output.out
    assert "Backend tool" in console_output.out
    assert "(by default)" not in console_output.out
    # 3
    inv_options.set_params(a=3, b=5)
    inv_options.summary()
    console_output = capsys.readouterr()
    assert "Solving method: optimization" in console_output.out
    assert "Solver-specific parameters:" in console_output.out
    assert "Backend tool" in console_output.out
    assert "a = 3" in console_output.out
    assert "b = 5" in console_output.out


def test_repr():
    inv_options = InversionOptions()
    # 0
    rep = repr(inv_options)
    assert "InversionOptions" in rep
    assert "unknown" in rep
    assert "default" in rep
    # 1
    inv_options.set_solving_method("optimization")
    rep = repr(inv_options)
    assert "method='optimization'" in rep
    assert "unknown" not in rep
    # 2
    inv_options.set_tool(inv_options.get_default_tool())
    rep = repr(inv_options)
    assert "default" not in rep

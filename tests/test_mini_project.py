import ast
import sys

# The mini-project is an open-ended GAME — it may wait for input, loop forever, or
# open a turtle window, so this grader (like Module 5's) never runs it. It reads
# mini_project.py with `ast` and checks the two project requirements are in the code:
#   1. the game uses user input (input(), or turtle onkey/onclick/listen)
#   2. the game keeps a score that changes and gets displayed
# Whether the game is FUN and actually works is graded by your instructor playing it!

SOURCE_FILE = 'mini_project.py'

INPUT_FUNCS = {'input'}
INPUT_METHODS = {'onkey', 'onkeypress', 'onkeyrelease', 'onclick', 'onscreenclick', 'listen', 'textinput', 'numinput'}
DISPLAY_METHODS = {'write', 'title'}

def _tree():
    with open(SOURCE_FILE, encoding='utf-8') as f:
        return ast.parse(f.read())

def _score_names(tree):
    """Variable names containing 'score' or 'point' that get assigned."""
    names = set()
    for node in ast.walk(tree):
        targets = []
        if isinstance(node, ast.Assign):
            targets = node.targets
        elif isinstance(node, (ast.AugAssign, ast.AnnAssign)):
            targets = [node.target]
        for t in targets:
            if isinstance(t, ast.Name) and ('score' in t.id.lower() or 'point' in t.id.lower()):
                names.add(t.id)
    return names

def test_file_parses():
    try:
        _tree()
    except SyntaxError as e:
        assert False, f"mini_project.py has a syntax error on line {e.lineno}: {e.msg}"

def test_uses_player_input():
    tree = _tree()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in INPUT_FUNCS:
                return
            if isinstance(node.func, ast.Attribute) and node.func.attr in INPUT_METHODS:
                return
    assert False, ("Requirement 1: your game needs user input — input() for typed answers, "
                   "or turtle's onkey()/onclick() + listen() for keys and clicks.")

def test_has_score_variable():
    assert _score_names(_tree()), (
        "Requirement 2: keep track of a score in a variable with 'score' (or 'point') "
        "in its name, like  score = 0"
    )

def test_score_changes():
    tree = _tree()
    scores = _score_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.AugAssign) and isinstance(node.target, ast.Name) and node.target.id in scores:
            return  # score += 1
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id in scores:
                    for sub in ast.walk(node.value):
                        if isinstance(sub, ast.Name) and sub.id in scores:
                            return  # score = score + 1
    assert False, ("Requirement 2: the score should CHANGE while playing, "
                   "like  score = score + 1")

def test_displays_score():
    tree = _tree()
    scores = _score_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            is_display = (isinstance(node.func, ast.Name) and node.func.id == 'print') or \
                         (isinstance(node.func, ast.Attribute) and node.func.attr in DISPLAY_METHODS)
            if is_display:
                for sub in ast.walk(node):
                    if isinstance(sub, ast.Name) and sub.id in scores:
                        return  # print(... score ...) or pen.write(... score ...)
    assert False, ("Requirement 2: DISPLAY the score to the player, "
                   "like  print('Score:', score)  or  pen.write('Score: ' + str(score))")

def test_has_game_logic():
    tree = _tree()
    logic = [n for n in ast.walk(tree) if isinstance(n, (ast.If, ast.While, ast.For))]
    assert logic, ("Games need decisions and repetition — use if/elif/else and a loop "
                   "(a game with no logic isn't much of a game!).")

if __name__ == '__main__':
    tests = [
        test_file_parses,
        test_uses_player_input,
        test_has_score_variable,
        test_score_changes,
        test_displays_score,
        test_has_game_logic,
    ]
    passed = 0
    for test in tests:
        try:
            test()
            print(f"  ✅ PASSED: {test.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  ❌ FAILED: {test.__name__} — {e}")

    print(f"\n{passed}/{len(tests)} checks passed.")
    if passed < len(tests):
        sys.exit(1)  # Causes the Action to show as failed in GitHub

# LineUp

LineUp is a pseudo-code interpreter that allows you to write and run a code with a limited action set by the language.

The language is designed to be simple and easy to modify, and add actions to it. But it will be a little complex to write a code with it.

## Installation

```bash
pip install lineup-lang
```

```py
from lineup_lang import Language, luexec, lucore
```

## Usage

```py
# Create a new language
# Add here the default actions that your language will have
core_object = [lucore.Variables({"a": 0, "b": -1})]

# You need an executor to run the code, it's the object that will iterate over the code
# Default executor, it will run the code line by line
executor = luexec.DefaultExecutor(core_object)
# Jumper executor, it will run the code line by line, but it will also allow you to jump to a specific line
executor = luexec.JumperExecutor(core_object)

# Create the language object, it's the object that will read the code, split it and send it to the executor
language = Language(executor)

# Run the code
language.run('''
    VAR c USE VAR a GET
    IF *+2 VAR c GET
    ELSE *+2
    EXIT VAR a GET
    EXIT VAR b GET
''')
```

## Default core objects

- `Variables`: It's a object that will store variables and their values. It's a dictionary that will store the variables and their values.
  - `Variables({"a": 0, "b": -1})`: It will create a new object with the variables `a` and `b` with the values `0` and `-1` respectively.
  - `VAR x`: Execute an action on a variable.
    - `GET`: Get the value of a variable.
    - `SET y`: Set the value "y" of a variable.
    - `COPY y`: Copy the value of the variable y to the variable.
    - `USE ACTION` : Execute a core action and store the result in the variable x.
    - `EXEC ACTION` : Execute an action on a variable. The variable need to be a `LanguageObject`.
    - `ACTION` : Execute an action on a variable. The variable need to be a `LanguageObject`.

- `ConditionsJumpObject`: An object that will store the conditions and the lines to jump.
  - `IF x CONDITION`: If the condition is true, go to the line x, else go to the next line.
  - `ELSE JUMP x`: Go to the line x.
  - `NOTIF x CONDITION`: If the condition is false, go to the line x, else go to the next line.
  - Condition:
    - `ACTION` Execute a core action, if the result is true, the condition is true.
    - `"ACTION" SIGN "ACTION"`: Compare two actions with the sign.
    - SIGN:
      - Equal: `EQ`, `==`
      - Not equal: `NE`, `!=`
      - Greater: `GT`, `>`
      - Greater or equal: `GE`, `>=`
      - Less: `LT`, `<`
      - Less or equal: `LE`, `<=`

# Harmonify

Harmonify is a Python library that lets you easily modify and manage the behavior of class methods during your program's runtime. Think of it as a toolkit to "patch" into existing code, allowing you to run your own functions before, after, or instead of the original method, all without touching the original source code.

It's particularly useful for:
* **Debugging:** Inject logging or checks into methods without changing them permanently.
* **Testing:** Isolate parts of your code by temporarily changing how certain methods behave.
* **Extending Libraries:** Add new features or modify behavior of classes from libraries you can't edit directly.
* **Experimentation:** Play around with how code runs in a non-destructive way.

## Features

* **Prefix Patching:** Run your custom code *before* the original method executes.
* **Postfix Patching:** Run your custom code *after* the original method executes, even allowing you to modify its return value.
* **Replace Patching:** Completely swap out the original method's logic with your own.
* **Easy Unpatching:** Restore methods to their original state with a simple call.

## Installation

Harmonify is designed to be a simple, standalone library for now. Just copy the `harmonify.py` file (or the relevant class definition) into your project!

```python
# Coming soon:
# pip install harmonify

# Harmonify

Harmonify is a Python library that allows users to change the behavior of classes at runtime, with nothing more than a few function calls.
Inspired by Harmony (the *very* popular C# library that also allows runtime behavior modification), Harmonify is flexible and uses a simple system based on monkey-patching.
Like its C# equivalent, it can be used for:
* **Debugging:** Inject logging or checks into methods without changing them permanently.
* **Testing:** Isolate parts of your code by temporarily changing how certain methods behave.
* **Extending Libraries:** Add new features or modify behavior of classes from libraries you can't edit directly.
* **Experimentation:** Play around with how code runs in a non-destructive way.

## Features

* **Prefix Patching:** Run your custom code *before* the original method executes.
* **Postfix Patching:** Run your custom code *after* the original method executes, even allowing you to modify its return value.
* **Replace Patching:** Completely swap out the original method's logic with your own.
* **Create & Delete methods:** Add or remove methods from a class or a module, without changing the other ones.
* **Easy Unpatching:** Restore methods to their original state with a simple call.

## Installation

Harmonify is designed to be a simple, standalone library for now. Just copy the `harmonify.py` file (or the relevant class definition) into your project!

```python
# Coming soon:
pip install harmonify

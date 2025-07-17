from harmonify import *
import module_a

def info_postfix(info, *args, **kwds):
    info["version"] = "tf is ts <3"
    return info


Harmonify.patch_function(module_a, "get_info", postfix=info_postfix)
print(module_a.get_info())


def foo(x):
    print(x)

def patch(res, *args, **kwds):
    return args[0]

Harmonify.patch_function(
    target_module = Harmonify.get_current_module(),
    function_name = "foo",
    postfix = patch
)

print(foo(5))
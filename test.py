import harmonify
import api_lib

if harmonify.inject_function(
    target_module = api_lib,
    function_name = "open_api1",
    path = harmonify.TreePath(0),
    inject_type = harmonify.InjectType.AFTER_TARGET,
    code_to_inject = "print('Injected!')"
):
    print("Successfully injected open_api1()")

if harmonify.inject_function(
    target_module = api_lib,
    function_name = "open_api2",
    path = harmonify.TreePath(0),
    inject_type = harmonify.InjectType.AFTER_TARGET,
    code_to_inject = "print('Injected!')"
):
    print("Successfully injected open_api2()")

if harmonify.inject_function(
    target_module = api_lib,
    function_name = "restricted_api",
    path = harmonify.TreePath(0),
    inject_type = harmonify.InjectType.AFTER_TARGET,
    code_to_inject = "print('Stealing info!')"
):
    print("Successfully injected restricted_api()")

api_lib.open_api1()
api_lib.open_api2()
api_lib.restricted_api(uname="Super Secret Agent #42", passwd="SuperSecretPassword123")
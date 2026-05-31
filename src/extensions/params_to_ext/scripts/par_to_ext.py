from typing import Any, List

"""
One most natural approach to wiring parameters to corresponding
methods in the extension is to do a big if/elif chain over every
possible parameter name. This scales poorly because you need to 
do a lot of typing
"""
# if par.name == 'Pulse':
#     me.parent().extensions[0].onPulse()
# elif par.name == 'somethingElse':
#     me.parent().extensions[0].onSomethingElse()
# elif par.name == 'blah':
#     me.parent().extensions[0].onBlah()
"""
Second version, a bit less noisy, but the principle and the downsides are exactly the same
"""
# match par.name:
#     case 'Pulse':
#         me.parent().extensions[0].onPulse()
#     case 'somethingElse':
#         me.parent().extensions[0].onSomethingElse()
#     case 'blah':
#         me.parent().extensions[0].onBlah()
"""
Third version takes advantage of Python's getattr method. This method
let's you get an attribute of the class by it's name. The attribute can be instance member variable as well as method
This approach requires you to have some agreed upon naming between
your parameter names and corresponding method name. Typical pattern
looks something like On<ParameterName> or on_<parametername>
"""
def getMethod(par):
    target = me.parent().extensions[0]

    # prefix of every method that corresponds with the parameter name
    methodNamePrefix = 'on_'
    methodName = f'{methodNamePrefix}{par.name.lower()}'
    method = getattr(target, methodName, None)

    return method 

def onValueChange(par: Par, prev: Any):
    method = getMethod(par)
    if callable(method):
        method(par.eval())
    else:
        debug(f'{me.parent()} has no method corresponding to {par.name}')
    return

def onPulse(par: Par):
    method = getMethod(par)
    if callable(method):
        method()
    else:
        debug(f'{me.parent()} has no method corresponding to {par.name}')
    return

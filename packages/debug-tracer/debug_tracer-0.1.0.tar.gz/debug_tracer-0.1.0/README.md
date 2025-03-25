# debug-tracer
not the best not the worst ig

Usage:
```python
import debug_tracer
tracer = debug_tracer.DebugTracer("Initial message")
tracer.trace("hmm")
print("and execution is unhindered!")

``` 

Example traceback:
```
/home/glitchy/PycharmProjects/DebugTracer/src/main.py:51: DebugTracer: 
==================== DEBUG TRACE ====================
Timestamp: 2025-03-24 19:51:43
Function: example_function
Line: 126
--------------------------------------------------------
Message: This is a debug trace
Arguments: 10, 20, SomeComplexClass{
  "details": {
    "field1": "value1",
    "field2": "value2",
    "field3": "value3",
    "field4": "value4",
    "field5": "value5"
  },
  "large_data": [
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    "truncated"
  ],
  "name": "ComplexObject"
}
--------------------------------------------------------
Local Variables:
{
  "args": "(10, 20, <__main__.SomeComplexClass object at 0x7685849c1a90>)",
  "message": "This is a debug trace"
}
--------------------------------------------------------
Environment Info:
Python Version: 3.13.2
OS: Linux-6.13.7-zen1-1-zen-x86_64-with-glibc2.41
========================================================
  File "/home/glitchy/PycharmProjects/DebugTracer/src/main.py", line 129, in <module>
    example_function()
  File "/home/glitchy/PycharmProjects/DebugTracer/src/main.py", line 126, in example_function
    tracer.trace("This is a debug trace", x, y, complex_obj)
  File "/home/glitchy/PycharmProjects/DebugTracer/src/main.py", line 28, in trace
    tb = self.get_traceback()
  File "/home/glitchy/PycharmProjects/DebugTracer/src/main.py", line 99, in get_traceback
    return traceback.format_stack()

======================= END TRACE ======================

```
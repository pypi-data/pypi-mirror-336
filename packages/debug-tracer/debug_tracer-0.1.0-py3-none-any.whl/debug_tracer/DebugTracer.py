import warnings
import json
import inspect
import time
import platform
import traceback


class DebugTracer(Warning):
    def __init__(self, message: str, *args):
        # Initialize the warning message
        self.message = message
        self.args = args
        super().__init__(message, *args)

    def trace(self, message: str, *args):
        # Gather local variables using locals() for the current scope
        local_vars = locals()

        # Convert non-serializable objects to strings with truncation if needed
        serializable_vars = {k: self.convert_to_serializable(v) for k, v in local_vars.items() if k != 'self'}

        # Get additional debug info (e.g., timestamp, function name, line number)
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        function_name = inspect.stack()[1].function
        line_number = inspect.stack()[1].lineno
        environment_info = self.get_environment_info()
        tb = self.get_traceback()

        # Create a formatted debug message
        debug_info = (
            f"\n==================== DEBUG TRACE ====================\n"
            f"Timestamp: {timestamp}\n"
            f"Function: {function_name}\n"
            f"Line: {line_number}\n"
            f"--------------------------------------------------------\n"
            f"Message: {message}\n"
            f"Arguments: {self.format_args(args)}\n"
            f"--------------------------------------------------------\n"
            f"Local Variables:\n"
            f"{self.format_json(serializable_vars)}\n"
            f"--------------------------------------------------------\n"
            f"Environment Info:\n"
            f"{environment_info}\n"
            f"========================================================\n"
            f"{"".join(tb)}\n"
            f"======================= END TRACE ======================"
        )

        # Raise a RuntimeWarning with debug information
        warnings.warn(debug_info, DebugTracer)

    def convert_to_serializable(self, obj):
        try:
            # Try to serialize the object
            json.dumps(obj)
            return obj
        except (TypeError, OverflowError):
            # If not serializable, return a compact string representation
            return self.compact_repr(obj)

    def compact_repr(self, obj):
        """Generates a truncated or compact string representation of non-serializables."""
        max_size = 100  # Set a limit for truncation
        try:
            if hasattr(obj, '__dict__'):
                # For objects with attributes, show a compact summary of the attributes
                attrs = {k: self.convert_to_serializable(v) for k, v in obj.__dict__.items()}
                truncated_attrs = {k: self.truncate_large_data(v) for k, v in attrs.items()}
                return f"{obj.__class__.__name__}{self.format_json(truncated_attrs)}"
            else:
                # For other types, return a string representation truncated to max_size
                return str(obj)[:max_size] + ('...' if len(str(obj)) > max_size else '')
        except Exception as e:
            # In case of any error, just return a generic description
            return f"<unserializable object of type {type(obj).__name__}>"

    def truncate_large_data(self, data):
        """Truncates large lists or dictionaries to avoid clutter."""
        if isinstance(data, list):
            # Truncate lists to a fixed length
            return data[:10] + ['truncated'] if len(data) > 10 else data
        elif isinstance(data, dict):
            # Truncate dictionaries to a fixed length for the keys and values
            return {k: self.convert_to_serializable(v) for k, v in list(data.items())[:5]}
        else:
            return data

    def format_json(self, data):
        """Uses json.dumps to pretty-print the data."""
        return json.dumps(data, indent=2, sort_keys=True)

    def format_args(self, args):
        # Format the args as a string for readability, ensuring they're all strings
        return ', '.join([str(self.convert_to_serializable(arg)) for arg in args])

    def get_traceback(self):
        # Implement
        return traceback.format_stack()

    def get_environment_info(self):
        # Get basic environment details (Python version, OS, etc.)
        python_version = platform.python_version()
        os_info = platform.platform()
        return f"Python Version: {python_version}\nOS: {os_info}"

if __name__ == "__main__":
    # Example usage
    class SomeComplexClass:
        def __init__(self):
            self.large_data = [i for i in range(1000)]  # Large data to test truncation
            self.name = "ComplexObject"
            self.details = {
                "field1": "value1", "field2": "value2", "field3": "value3", "field4": "value4", "field5": "value5",
                "field6": "value6", "field7": "value7"
            }


    def example_function():
        x = 10
        y = 20
        complex_obj = SomeComplexClass()
        tracer = DebugTracer("Initial message")

        # Call the trace method to show debug info
        tracer.trace("This is a debug trace", x, y, complex_obj)


    example_function()
    print("And execution isn't hindered!")
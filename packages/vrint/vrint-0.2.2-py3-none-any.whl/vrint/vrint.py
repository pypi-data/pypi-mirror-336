class VerboseStateObject:
    def __init__(self, vrint_instance, value):
        self.vrint = vrint_instance
        self.value = value
    
    def __bool__(self):
        return self.value

class Vrint:
    def __init__(self):
        self._verbose = False
        self.seen_ids = set()  # Track object IDs to handle recursive structures
    
    # Helper methods for numeric formatting
    def _is_numeric(self, value):
        """Check if a value is numeric (int, float, or string that can be converted to float)"""
        if isinstance(value, (int, float)):
            return True
        if isinstance(value, str):
            try:
                float(value)
                return True
            except ValueError:
                return False
        return False
    
    def _split_numeric(self, value):
        """Split a numeric value into integer and decimal parts"""
        if not self._is_numeric(value):
            return str(value), ""
        
        str_value = str(value)
        if '.' in str_value:
            int_part, dec_part = str_value.split('.')
            return int_part, dec_part
        else:
            return str_value, ""
    
    def _format_aligned_numeric(self, value, max_int_width, max_dec_width):
        """Format a numeric value with aligned decimal point"""
        int_part, dec_part = self._split_numeric(value)
        
        # Right-align integer part, then decimal point, then left-align decimal part
        if dec_part:
            return f"{int_part.rjust(max_int_width)}.{dec_part.ljust(max_dec_width)}"
        else:
            # For integers, add spaces where the decimal point and decimal part would be
            return f"{int_part.rjust(max_int_width)}{' ' * (max_dec_width + 1)}"
    
    def _get_object_structure(self, obj):
        """Get a fingerprint of the object's structure to identify similar objects"""
        if not hasattr(obj, '__dict__'):
            return None
        
        # Create a structure signature based on attributes and their types
        attributes = {}
        for attr_name, attr_value in obj.__dict__.items():
            if not attr_name.startswith('_'):  # Skip private attributes
                attr_type = type(attr_value).__name__
                attributes[attr_name] = attr_type
        
        # Create a hashable fingerprint that captures structure
        fingerprint = tuple(sorted((k, v) for k, v in attributes.items()))
        return fingerprint

    def __call__(self, *args, **kwargs):
        """Make vrint behave like regular print but with pretty formatting and state control"""
        if not self._verbose:
            return
            
        # If no args, just print a newline like regular print()
        if not args and not kwargs:
            print()
            return
            
        # Special case: single string argument should print without quotes or indentation
        if len(args) == 1 and isinstance(args[0], str) and not kwargs:
            print(args[0])
            return
            
        # Special case: multiple string arguments should be space-separated like print()
        if all(isinstance(arg, str) for arg in args) and not kwargs:
            print(*args)
            return
            
        # Mixed arguments with leading string(s) - handle like print() but with pretty formatting for non-strings
        has_leading_strings = False
        non_string_start_idx = 0
        
        # Check if we start with one or more strings
        for i, arg in enumerate(args):
            if isinstance(arg, str):
                non_string_start_idx = i + 1
                has_leading_strings = True
            else:
                break
                
        if has_leading_strings:
            # Print the leading strings like regular print (space-separated, no quotes)
            print(*args[:non_string_start_idx], end=" " if non_string_start_idx < len(args) else "\n")
            
            # Then format the remaining non-string arguments with pretty()
            for i in range(non_string_start_idx, len(args)):
                # First non-string arg doesn't need indent since we already printed something
                # Use a smaller indent for subsequent arguments to align better with the text
                first_non_string = (i == non_string_start_idx)
                self.pretty(args[i], state=True, indent=0 if first_non_string else 2)
        else:
            # For non-string arguments, use the regular pretty printer
            for i, arg in enumerate(args):
                self.pretty(arg, state=True)
            
        # Handle keyword arguments
        for key, value in kwargs.items():
            self.pretty(value, name=key, state=True)
    
    def __bool__(self):
        return self._verbose

    # Enable passing format strings with objects that might not be printable directly
    def format(self, format_string, *args, **kwargs):
        """Safely format objects before printing"""
        state = kwargs.pop('state', None)
        should_print = self._verbose
        
        if state is not None:
            if hasattr(state, 'value'):
                should_print = state.value
            else:
                try:
                    should_print = bool(state)
                except (ValueError, TypeError):
                    print(f"Warning: Invalid state type {type(state)} passed to vrint.format. Using default state.")
        
        if should_print:
            try:
                formatted_message = format_string.format(*args, **kwargs)
                print(formatted_message)
            except (ValueError, TypeError) as e:
                print(f"Error formatting message: {e}")
                # Fall back to basic printing
                print(format_string, args, kwargs)
    
    # Method for safely printing arrays
    def array(self, name, array_obj, state=None):
        """Safely print arrays with a name label"""
        should_print = self._verbose
        
        if state is not None:
            if hasattr(state, 'value'):
                should_print = state.value
            else:
                try:
                    should_print = bool(state)
                except (ValueError, TypeError):
                    print(f"Warning: Invalid state type {type(state)} passed to vrint.array. Using default state.")
        
        if should_print:
            try:
                shape_info = f" shape={array_obj.shape}" if hasattr(array_obj, "shape") else ""
                print(f"{name}:{shape_info} {array_obj}")
            except Exception as e:
                print(f"Error printing array {name}: {e}")
    
    @property
    def verbose(self):
        """Smart property that changes state globally when accessed directly"""
        self._verbose = True
        return VerboseStateObject(self, True)
    
    @property
    def quiet(self):
        """Smart property that changes state globally when accessed directly"""
        self._verbose = False
        return VerboseStateObject(self, False)
    
    def __getattr__(self, name):
        if name == 'verbose':
            return self.verbose
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
    
    def _format_ndarray(self, obj, name, indent, max_depth, prefix):
        """Enhanced formatting specifically for numpy arrays with properly aligned decimal points"""
        import numpy as np
        
        shape_str = f"shape={obj.shape}"
        dtype_str = f"dtype={obj.dtype}"
        
        # Print the name first on its own line
        if name:
            print(f"{' ' * indent}{name}:")
            name_prefix = " " * indent  # We've already printed the name
        else:
            name_prefix = prefix
        
        # Handle empty arrays
        if obj.size == 0:
            print(f"{name_prefix}array([]) # {shape_str}, {dtype_str}")
            return
            
        # Handle 0D arrays (scalars)
        if obj.ndim == 0:
            print(f"{name_prefix}array({obj.item()}) # scalar, {dtype_str}")
            return
            
        # Function to determine digits before and after decimal for a number
        def get_parts(x):
            str_x = f"{x}"
            if '.' in str_x:
                int_part, dec_part = str_x.split('.')
                return len(int_part), len(dec_part)
            else:
                return len(str_x), 0
        
        # Function to properly format a number with decimal alignment
        def format_aligned(x, max_int_width, max_dec_width):
            if isinstance(x, (int, float, np.number)):
                str_x = f"{x}"
                if '.' in str_x:
                    int_part, dec_part = str_x.split('.')
                    # Pad integer part on left, decimal part on right
                    return f"{int_part.rjust(max_int_width)}.{dec_part.ljust(max_dec_width)}"
                else:
                    # For integers, add a phantom decimal point with spacing
                    return f"{str_x.rjust(max_int_width)}" + " " * (max_dec_width + 1)
            else:
                # Non-numeric elements
                return str(x)
            
        # Handle 1D arrays (vectors)
        if obj.ndim == 1:
            if obj.size <= 20:
                # Find max integer and decimal parts
                max_int_width = 0
                max_dec_width = 0
                for x in obj:
                    if isinstance(x, (int, float, np.number)):
                        int_width, dec_width = get_parts(x)
                        max_int_width = max(max_int_width, int_width)
                        max_dec_width = max(max_dec_width, dec_width)
                
                # Format with decimal alignment
                formatted_elements = [format_aligned(x, max_int_width, max_dec_width) for x in obj]
                elements = ", ".join(formatted_elements)
                print(f"{name_prefix}array([{elements}]) # {shape_str}, {dtype_str}")
            else:
                # For larger arrays, show head and tail with alignment
                display_items = list(obj[:5]) + list(obj[-5:])
                
                # Find max integer and decimal parts
                max_int_width = 0
                max_dec_width = 0
                for x in display_items:
                    if isinstance(x, (int, float, np.number)):
                        int_width, dec_width = get_parts(x)
                        max_int_width = max(max_int_width, int_width)
                        max_dec_width = max(max_dec_width, dec_width)
                
                # Format head and tail
                head_elements = [format_aligned(x, max_int_width, max_dec_width) for x in obj[:5]]
                tail_elements = [format_aligned(x, max_int_width, max_dec_width) for x in obj[-5:]]
                
                head = ", ".join(head_elements)
                tail = ", ".join(tail_elements)
                print(f"{name_prefix}array([{head}, ... {tail}]) # {shape_str}, {dtype_str}")
            return
            
        # Handle 2D arrays (matrices)
        if obj.ndim == 2:
            print(f"{name_prefix}array([  # {shape_str}, {dtype_str}")
            
            # Determine which rows we'll check (either all rows or a subset for large matrices)
            rows_to_check = obj
            if obj.shape[0] > 10:
                rows_to_check = np.vstack((obj[:5], obj[-5:]))
                
            # Find max integer and decimal width across matrix for alignment
            max_int_width = 0
            max_dec_width = 0
            for row in rows_to_check:
                row_to_check = row
                if obj.shape[1] > 20:
                    # For wide matrices, only check elements we'll display
                    row_to_check = np.hstack((row[:5], row[-5:]))
                
                for x in row_to_check:
                    if isinstance(x, (int, float, np.number)):
                        int_width, dec_width = get_parts(x)
                        max_int_width = max(max_int_width, int_width)
                        max_dec_width = max(max_dec_width, dec_width)
            
            # Function to format a row with decimal alignment
            def format_row(row, full_row=True):
                if full_row or len(row) <= 20:
                    formatted = [format_aligned(x, max_int_width, max_dec_width) for x in row]
                    return ", ".join(formatted)
                else:
                    # For wide rows, show head and tail
                    head = [format_aligned(x, max_int_width, max_dec_width) for x in row[:5]]
                    tail = [format_aligned(x, max_int_width, max_dec_width) for x in row[-5:]]
                    return f"{', '.join(head)}, ... {', '.join(tail)}"
            
            if obj.shape[0] <= 10:
                # Show all rows for small matrices
                for row in obj:
                    row_str = format_row(row, full_row=(obj.shape[1] <= 20))
                    print(f"{' ' * (indent+4)}[{row_str}],")
            else:
                # Show subset for large matrices
                for row in obj[:5]:
                    row_str = format_row(row, full_row=(obj.shape[1] <= 20))
                    print(f"{' ' * (indent+4)}[{row_str}],")
                print(f"{' ' * (indent+4)}...")
                for row in obj[-5:]:
                    row_str = format_row(row, full_row=(obj.shape[1] <= 20))
                    print(f"{' ' * (indent+4)}[{row_str}],")
                
            print(f"{' ' * indent}])")
            return
            
        # Handle 3D arrays
        if obj.ndim == 3 and all(dim <= 5 for dim in obj.shape):
            print(f"{name_prefix}array([  # {shape_str}, {dtype_str}")
            
            # Find max integer and decimal widths across the entire 3D array
            max_int_width = 0
            max_dec_width = 0
            
            for slice_2d in obj:
                for row in slice_2d:
                    for x in row:
                        if isinstance(x, (int, float, np.number)):
                            int_width, dec_width = get_parts(x)
                            max_int_width = max(max_int_width, int_width)
                            max_dec_width = max(max_dec_width, dec_width)
            
            for i, slice_2d in enumerate(obj):
                print(f"{' ' * (indent+4)}[  # dimension 1, index {i}")
                for row in slice_2d:
                    # Format each row with decimal alignment
                    formatted_values = [format_aligned(x, max_int_width, max_dec_width) for x in row]
                    row_str = ", ".join(formatted_values)
                    print(f"{' ' * (indent+8)}[{row_str}],")
                print(f"{' ' * (indent+4)}],")
            print(f"{' ' * indent}])")
        else:
            # For very large or high-dimensional arrays, print summary with sample
            print(f"{name_prefix}array(...)  # {shape_str}, {dtype_str}, {obj.size} elements")
            
            # Show first/last few elements as a preview
            if obj.size > 0:
                flat = obj.flatten()
                preview_elements = flat[:10] if obj.size <= 10 else np.concatenate([flat[:5], flat[-5:]])
                
                # Find max integer and decimal parts for preview
                max_int_width = 0
                max_dec_width = 0
                for x in preview_elements:
                    if isinstance(x, (int, float, np.number)):
                        int_width, dec_width = get_parts(x)
                        max_int_width = max(max_int_width, int_width)
                        max_dec_width = max(max_dec_width, dec_width)
                
                # Format preview with decimal alignment
                formatted_preview = [format_aligned(x, max_int_width, max_dec_width) for x in preview_elements]
                preview_str = ", ".join(formatted_preview)
                
                suffix = "..." if obj.size > 10 else ""
                print(f"{' ' * (indent+4)}First/last elements: [{preview_str}]{suffix}")
    
    def _format_dataframe(self, df, name, indent, max_depth, prefix):
        """Enhanced formatting for pandas DataFrames"""
        # Print header with shape and column information
        cols_str = str(list(df.columns))
        if len(cols_str) > 80:
            cols_str = cols_str[:77] + "..."
        
        print(f"{prefix}DataFrame(shape={df.shape}, columns={cols_str})")
        
        # Only show sample for large DataFrames
        if len(df) > 10:
            print(f"{' ' * (indent+2)}# Showing 5 rows from head and tail:")
            # Get sample rows from head and tail
            head = df.head(5).to_string()
            tail = df.tail(5).to_string()
            
            # Print with proper indentation
            for line in head.split('\n'):
                print(f"{' ' * (indent+2)}{line}")
            print(f"{' ' * (indent+2)}...")
            for line in tail.split('\n'):
                print(f"{' ' * (indent+2)}{line}")
        else:
            # For small DataFrames, just show the whole thing
            df_str = df.to_string()
            for line in df_str.split('\n'):
                print(f"{' ' * (indent+2)}{line}")
    
    def _format_series(self, series, name, indent, max_depth, prefix):
        """Enhanced formatting for pandas Series"""
        print(f"{prefix}Series(length={len(series)}, dtype={series.dtype})")
        
        if len(series) > 10:
            # For large Series, show head and tail
            head = series.head(5).to_string()
            tail = series.tail(5).to_string()
            
            for line in head.split('\n'):
                print(f"{' ' * (indent+2)}{line}")
            print(f"{' ' * (indent+2)}...")
            for line in tail.split('\n'):
                print(f"{' ' * (indent+2)}{line}")
        else:
            # For small Series, show the whole thing
            series_str = series.to_string()
            for line in series_str.split('\n'):
                print(f"{' ' * (indent+2)}{line}")
    
    def _format_dict_safely(self, obj, indent, max_depth, prefix=''):
        """Enhanced formatting for dictionaries with safety checks and proper alignment"""
        print(f"{prefix}{{")
        
        # First pass - find the maximum key length for alignment
        max_key_length = 0
        for k in obj.keys():
            try:
                key_repr = repr(k) if not isinstance(k, str) else f"'{k}'"
                max_key_length = max(max_key_length, len(key_repr))
            except:
                pass  # Skip problematic keys for alignment calculation
        
        value_indent = indent + 2
        
        # Group items by structure for better alignment
        grouped_items = {}
        ungrouped_items = []
        
        for k, v in obj.items():
            # Generate a structure fingerprint for the object
            structure = self._get_object_structure(v)
            if structure and len(structure) > 0:  # Only group objects with actual structure
                if structure not in grouped_items:
                    grouped_items[structure] = []
                grouped_items[structure].append((k, v))
            else:
                ungrouped_items.append((k, v))
        
        # Process each group of similar structured objects
        for structure, items in grouped_items.items():
            if len(items) < 2:  # If only one item with this structure, don't need special alignment
                ungrouped_items.extend(items)
                continue
                
            # Analyze structure to determine fields and their formatting needs
            common_attrs = {}
            for attr_name, attr_type in structure:
                common_attrs[attr_name] = {
                    "type": attr_type,
                    "is_numeric": False,
                    "max_int_width": 0,
                    "max_dec_width": 0,
                    "max_width": 0,
                    "values": []
                }
            
            # First pass to collect values and determine max widths
            for _, obj in items:
                for attr_name in common_attrs:
                    if hasattr(obj, attr_name):
                        value = getattr(obj, attr_name)
                        common_attrs[attr_name]["values"].append(value)
                        
                        # Check if field is numeric for alignment
                        if self._is_numeric(value):
                            common_attrs[attr_name]["is_numeric"] = True
                            int_part, dec_part = self._split_numeric(value)
                            common_attrs[attr_name]["max_int_width"] = max(
                                common_attrs[attr_name]["max_int_width"], 
                                len(int_part)
                            )
                            common_attrs[attr_name]["max_dec_width"] = max(
                                common_attrs[attr_name]["max_dec_width"], 
                                len(dec_part)
                            )
                        elif isinstance(value, str):
                            common_attrs[attr_name]["max_width"] = max(
                                common_attrs[attr_name]["max_width"],
                                len(value) + 2  # +2 for quotes
                            )
            
            # Find longest attribute name for alignment
            max_attr_length = max(len(attr) for attr in common_attrs) if common_attrs else 0
            
            # Handle nested objects with similar structure
            nested_structures = {}
            for attr_name, attr_info in common_attrs.items():
                # Check if this attribute contains objects with common structure
                nested_objects = [v for v in attr_info["values"] if hasattr(v, '__dict__')]
                if nested_objects:
                    nested_fingerprints = {}
                    for nested_obj in nested_objects:
                        fp = self._get_object_structure(nested_obj)
                        if fp:
                            if fp not in nested_fingerprints:
                                nested_fingerprints[fp] = []
                            nested_fingerprints[fp].append(nested_obj)
                    
                    # If we have groups of similar nested objects
                    for fp, objs in nested_fingerprints.items():
                        if len(objs) >= 2:  # Need at least 2 for alignment
                            if attr_name not in nested_structures:
                                nested_structures[attr_name] = []
                            nested_structures[attr_name].append((fp, objs))
            
            # Now print each item in the group with aligned fields
            for k, v in items:
                if isinstance(k, str):
                    key_repr = f"'{k}'"
                else:
                    key_repr = repr(k)
                
                padded_key = key_repr.ljust(max_key_length)
                
                # Print the class name and opening parenthesis
                class_name = v.__class__.__name__ 
                print(f"{' ' * value_indent}{padded_key}: {class_name}(")
                
                # Print each attribute with consistent alignment
                attr_items = [(attr, getattr(v, attr, None)) for attr in sorted(common_attrs.keys())]
                
                for i, (attr_name, attr_value) in enumerate(attr_items):
                    # Skip if attribute not present in this particular object
                    if attr_value is None:
                        continue
                        
                    attr_info = common_attrs[attr_name]
                    padded_attr = attr_name.ljust(max_attr_length)
                    
                    # Check if this is a nested object with complex structure
                    if attr_name in nested_structures and hasattr(attr_value, '__dict__'):
                        # Handle nested object - just print with normal recursion for now
                        print(f"{' ' * (value_indent + 2)}{padded_attr}=", end="")
                        self.pretty(attr_value, state=True, 
                                  indent=value_indent + 2 + len(padded_attr) + 1,
                                  max_depth=max_depth-1)
                        if i < len(attr_items) - 1:
                            print(",")
                        else:
                            print("")
                    elif attr_info["is_numeric"]:
                        # Format numeric value with decimal alignment
                        formatted_value = self._format_aligned_numeric(
                            attr_value, 
                            attr_info["max_int_width"],
                            attr_info["max_dec_width"]
                        )
                        # Print with comma if not the last item
                        print(f"{' ' * (value_indent + 2)}{padded_attr}={formatted_value}", end="")
                        if i < len(attr_items) - 1:
                            print(",")
                        else:
                            print("")
                    elif isinstance(attr_value, str):
                        # Format string value
                        print(f"{' ' * (value_indent + 2)}{padded_attr}='{attr_value}'", end="")
                        if i < len(attr_items) - 1:
                            print(",")
                        else:
                            print("")
                    else:
                        # Format other values
                        print(f"{' ' * (value_indent + 2)}{padded_attr}={attr_value}", end="")
                        if i < len(attr_items) - 1:
                            print(",")
                        else:
                            print("")
                
                # Close the object representation
                print(f"{' ' * value_indent})")
        
        # Handle regular (ungrouped) items
        for k, v in ungrouped_items:
            try:
                if isinstance(k, str):
                    key_repr = f"'{k}'"
                else:
                    key_repr = repr(k)
                
                padded_key = key_repr.ljust(max_key_length)
                
                if isinstance(v, dict):
                    print(f"{' ' * value_indent}{padded_key}: ", end="")
                    self.pretty(v, state=True, indent=value_indent+2, max_depth=max_depth-1)
                elif isinstance(v, (list, tuple, set)) and v:
                    print(f"{' ' * value_indent}{padded_key}: ", end="")
                    self.pretty(v, state=True, indent=value_indent+2, max_depth=max_depth-1)
                elif hasattr(v, '__dict__') and not isinstance(v, type):
                    # Custom object that wasn't part of a group
                    print(f"{' ' * value_indent}{padded_key}: ", end="")
                    self.pretty(v, state=True, indent=value_indent+2, max_depth=max_depth-1)
                else:
                    if isinstance(v, str):
                        v_repr = f"'{v}'"
                    else:
                        v_repr = repr(v)
                    print(f"{' ' * value_indent}{padded_key}: {v_repr}")
            except Exception as e:
                print(f"{' ' * value_indent}Error displaying key-value pair: {e}")
        
        print(f"{' ' * indent}}}")
    
    def pretty(self, obj, name=None, state=None, indent=2, max_depth=10, is_attr=False):
        """Prettify objects with type and structure information"""
        # Handle state logic
        should_print = self._verbose
        if state is not None:
            if hasattr(state, 'value'):
                should_print = state.value
            else:
                try:
                    should_print = bool(state)
                except (ValueError, TypeError):
                    print(f"Warning: Invalid state type {type(state)} passed to vrint.pretty. Using default state.")
        
        if not should_print:
            return
        
        # Create the prefix
        if name:
            prefix = f"{' ' * indent}{name}: "
        else:
            prefix = f"{' ' * indent}"
        
        # Check depth limit
        if max_depth <= 0:
            print(f"{prefix}... (max depth reached)")
            return
        
        try:
            # Handle None first
            if obj is None:
                print(f"{prefix}None")
                return
            
            # Get object ID to handle recursive structures
            obj_id = id(obj)
            
            # Check if we've seen this object before (recursive structure)
            if hasattr(obj, '__dict__') or isinstance(obj, (dict, list, tuple, set)):
                if obj_id in self.seen_ids:
                    print(f"{prefix}<RECURSIVE REFERENCE>")
                    return
                self.seen_ids.add(obj_id)
            
            # Handle different types
            if isinstance(obj, dict):
                if not obj:
                    print(f"{prefix}{{}}")
                else:
                    # Use the safer dict formatting method
                    self._format_dict_safely(obj, indent, max_depth, prefix)
            elif isinstance(obj, (list, tuple)):
                container_type = "list" if isinstance(obj, list) else "tuple"
                if not obj:
                    print(f"{prefix}{[] if container_type == 'list' else ()}")
                else:
                    print(f"{prefix}{container_type}([")
                    
                    items = list(enumerate(obj))
                    list_indent = indent + 2
                    max_line_width = 80  # Maximum width per line
                    
                    # Check if we should use horizontal or vertical layout
                    use_horizontal = all(not isinstance(item, (dict, list, tuple, set)) 
                                        for _, item in items) and len(items) > 10
                    
                    if use_horizontal:
                        # Horizontal layout for simple type items in long lists
                        current_line = []
                        current_width = 0
                        line_start_idx = 0
                        
                        for idx, item in items:
                            # Format the item
                            if isinstance(item, str):
                                item_str = f"'{item}'"
                            else:
                                item_str = str(item)
                            
                            # Calculate width with spacing
                            item_display = f"{item_str}, "
                            item_width = len(item_display)
                            
                            # Check if adding this item would exceed line width
                            if current_width + item_width > max_line_width and current_line:
                                # Print the current line with the start index
                                line_str = "".join(current_line).rstrip(", ")
                                print(f"{' ' * list_indent}[{line_start_idx}]: {line_str}")
                                
                                # Start a new line
                                current_line = [item_display]
                                current_width = len(f"{' ' * list_indent}[{idx}]: ") + item_width
                                line_start_idx = idx
                            else:
                                # Add to current line
                                current_line.append(item_display)
                                current_width += item_width
                        
                        # Print any remaining items
                        if current_line:
                            line_str = "".join(current_line).rstrip(", ")
                            print(f"{' ' * list_indent}[{line_start_idx}]: {line_str}")
                    else:
                        # Vertical layout for complex items or short lists
                        for i, (idx, item) in enumerate(items):
                            # Add blank line before displaying a nested dictionary (except the first one)
                            if isinstance(item, dict) and item and i > 0:
                                print("")
                            
                            # Use consistent indentation for all list items    
                            self.pretty(item, name=f"[{idx}]", state=True, indent=list_indent, max_depth=max_depth-1)
                            
                            # Add blank line after a nested dictionary (except the last one)
                            if isinstance(item, dict) and item and i < len(items) - 1:
                                print("")
                    
                    print(f"{' ' * indent}])")
            elif isinstance(obj, set):
                if not obj:
                    print(f"{prefix}set()")
                else:
                    print(f"{prefix}set([")
                    items = list(enumerate(obj))
                    set_indent = indent + 2
                    
                    for i, (idx, item) in enumerate(items):
                        # Add blank line before displaying a nested dictionary (except the first one)
                        if isinstance(item, dict) and item and i > 0:
                            print("")
                        
                        # Use consistent indentation for all set items
                        self.pretty(item, name=f"[{idx}]", state=True, indent=set_indent, max_depth=max_depth-1)
                        
                        # Add blank line after a nested dictionary (except the last one)
                        if isinstance(item, dict) and item and i < len(items) - 1:
                            print("")
                            
                    print(f"{' ' * indent}])")
            elif callable(obj) and hasattr(obj, '__name__'):
                # Handle functions and methods
                module = obj.__module__ if hasattr(obj, '__module__') else '<unknown>'
                print(f"{prefix}<function {module}.{obj.__name__}>")
            else:
                # Try specialized formatting for numpy arrays
                try:
                    import numpy as np
                    if isinstance(obj, np.ndarray):
                        self._format_ndarray(obj, name, indent, max_depth, prefix)
                        return
                except (ImportError, Exception):
                    pass
                    
                # Try specialized formatting for pandas DataFrames and Series
                try:
                    import pandas as pd
                    if isinstance(obj, pd.DataFrame):
                        self._format_dataframe(obj, name, indent, max_depth, prefix)
                        return
                    elif isinstance(obj, pd.Series):
                        self._format_series(obj, name, indent, max_depth, prefix)
                        return
                except (ImportError, Exception):
                    pass
                
                # Fallback for other types
                try:
                    if hasattr(obj, '__dict__'):
                        # Handle custom objects with attributes
                        class_name = obj.__class__.__name__
                        
                        # Print on multiple lines with proper indentation
                        print(f"{prefix}{class_name}(")
                        
                        # Get all public attributes (non-dunder, non-private)
                        attrs = {attr: getattr(obj, attr) for attr in dir(obj) 
                                if not attr.startswith('_') and not callable(getattr(obj, attr))}
                        
                        # Find maximum attribute name length for alignment
                        if attrs:
                            max_attr_length = min(20, max(len(attr) for attr in attrs.keys()))
                            
                            # Calculate indentation for attributes
                            attr_indent = indent + 2
                            
                            # Group numeric attributes for decimal alignment
                            numeric_attrs = {}
                            for attr, value in attrs.items():
                                if self._is_numeric(value):
                                    int_part, dec_part = self._split_numeric(value)
                                    if attr not in numeric_attrs:
                                        numeric_attrs[attr] = {
                                            "int_width": len(int_part),
                                            "dec_width": len(dec_part)
                                        }
                            
                            # Sort items for consistent display
                            items = sorted(attrs.items())
                            
                            # Process each attribute
                            for i, (attr, value) in enumerate(items):
                                # Pad attribute name for alignment
                                padded_attr = attr.ljust(max_attr_length)
                                
                                # Complex nested values
                                if not isinstance(value, (str, int, float, bool, type(None))):
                                    print(f"{' ' * attr_indent}{padded_attr}=", end="")
                                    self.pretty(value, state=True, indent=attr_indent + len(padded_attr) + 1, 
                                            max_depth=max_depth-1, is_attr=True)
                                    if i < len(items) - 1:
                                        print(",")
                                    else:
                                        print("")
                                elif attr in numeric_attrs:
                                    # Format numeric values with decimal alignment
                                    formatted = self._format_aligned_numeric(
                                        value,
                                        numeric_attrs[attr]["int_width"],
                                        numeric_attrs[attr]["dec_width"]
                                    )
                                    print(f"{' ' * attr_indent}{padded_attr}={formatted}", end="")
                                    if i < len(items) - 1:
                                        print(",", end="")
                                    print("")
                                else:
                                    # Simple values printed directly
                                    if isinstance(value, str):
                                        print(f"{' ' * attr_indent}{padded_attr}='{value}'", end="")
                                    else:
                                        print(f"{' ' * attr_indent}{padded_attr}={value}", end="")
                                    # Add comma if not the last attribute
                                    if i < len(items) - 1:
                                        print(",", end="")
                                    print("")
                        
                        print(f"{' ' * indent})")
                    else:
                        # Just use default string representation
                        print(f"{prefix}{repr(obj)}")
                except Exception as e:
                    print(f"{prefix}<Error displaying object: {e}>")
        finally:
            # Remove from seen set when done to allow future printings
            if hasattr(obj, '__dict__') or isinstance(obj, (dict, list, tuple, set)):
                self.seen_ids.discard(obj_id)
# Bug Fix - Numpy Array Comparison Error

## Error Description

```
ValueError: The truth value of an array with more than one element is ambiguous. 
Use a.any() or a.all()
```

**Location**: `process_register_frame()` method, line 803

## Root Cause

When checking if `self.captured_face` exists, the code used:
```python
if self.captured_face:
```

This fails because `self.captured_face` is a numpy array (image data), and numpy arrays cannot be evaluated as boolean values directly.

## Solution

Changed all checks from:
```python
if self.captured_face:
```

To:
```python
if self.captured_face is not None:
```

And for negative checks:
```python
if self.captured_face is None:
```

## Files Modified

- `face_recognition_ui.py` - Line 803 and 1003

## Why This Works

- `is not None` explicitly checks if the variable is None
- This works correctly with numpy arrays
- Avoids the ambiguous truth value error

## Testing

To verify the fix:

1. Run the application:
   ```bash
   python face_recognition_ui.py
   ```

2. Click "➕ Register New Person"

3. The camera feed should display without errors

4. Press SPACE to capture a face

5. The form should appear with both Name and Student ID fields visible

## Status

✅ **Fixed** - Application now runs without errors
✅ **Tested** - Registration mode works correctly
✅ **Verified** - No syntax or runtime errors

---

**Fixed**: 2025-11-29
**Issue**: Numpy array boolean comparison
**Solution**: Use explicit `is not None` checks

<img src="https://github.com/LucLor06/django-hyperscript/blob/main/django-hyperscript.png?raw=true" width=200>

# Django Hyperscript

This package is intended to simplify the process of dumping data from Django into Hyperscript by providing two template tags with options for customizing the output.

---
## Installation

1. Install using pip:
```bash
pip install django-hyperscript
```

2. Add `django_hyperscript` to `INSTALLED_APPS` in your Django project's `settings.py`:
```python
# settings.py

INSTALLED_APPS = [
    ...,
    'django_hyperscript',
]
```

3. Load the tag library in the necessary templates:
```django
{% load hyperscript %}
```

---
## Usage

### `hs_dump`

Dumps data into a single Hyperscript variable.
```django
{% hs_dump data 'myData' %}
```
assuming `data` is `{"foo": "bar"}`, the tag would output
```html
<div _="
init
    set global myData to {'foo': 'bar'} 
    then remove me 
end"></div>
```
### `hs_expand`

Expands a dictionary into Hyperscript variables.
```django
{% hs_expand data %}
```

assuming `data` is `{"foo": "bar", "baz": "qux"}`, the tag would output
```html
<div _="
init 
    set global foo to bar 
    set global baz to qux 
    then remove me
end"></div>
```

---
## Configuration

Both `hs_dump` and `hs_expand` have a set of additional keyword arguments to configure their behavior.

### `show`
*Type*: `bool` | *Default*: `False`

Removes Hyperscript from the DOM after initializing if `True`.

### `translate`
*Type*: `bool` | *Default*: `True`

"Translates" dictionary keys from snake case (snake_case) to camel case (camelCase) to fit JavaScript naming conventions.

### `scope`
*Type*: `str` | *Default*: `global`

Determines the scope of the Hyperscript variable (global, element, or local).

### `wrap`
*Type*: `bool` | *Default*: `True`

Wraps the Hyperscript in a `<div>` if `True`, otherwise returns the raw Hyperscript text.

**Note:** If both **`wrap`** and **`show`** are `False`, the element will *not* be removed and the Hyperscript attribute and value will be removed from the element.

### `debug`
*Type*: `bool` | *Default*: `False`

Logs the set variable name(s) and output.

## Final example
```django
{% hs_dump data 'my_data' show=True translate=False scope='element' wrap=False %}
```
assuming `data` is `{"my_value": 25}`, the tag would output
```python
"init set element my_data to {'my_value': 25} end"
```
In this example:
- The Hyperscript remains in the DOM since **`show`** is `True`
- The keys within the dumped data remain in snake case since **`translate`** is `False`
- The variable is scoped to the element the Hyperscript belongs to since **`scope`** is set to `'element'`
- The output is just the raw Hyperscript text since **`wrap`** is set to `False`

---
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
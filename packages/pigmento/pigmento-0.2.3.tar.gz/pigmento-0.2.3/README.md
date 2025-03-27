# Pigmento: Colorize and Trace Printing

**Due to the limitation of Github and Pypi Markdown, please visit [Pigmento](https://liu.qijiong.work/2023/10/18/Develop-Pigmento/) for a better reading experience.**

![Pigmento](https://liu.qijiong.work/images/covers/pigmento.png?t=20231018)

## Installation

```bash
pip install pigmento
```

## Quick Start

```python
from pigmento import pnt

class Test:
    @classmethod
    def class_method(cls):
        pnt('Hello World')

    def instance_method(self):
        pnt('Hello World')

    @staticmethod
    def static_method():
        pnt('Hello World')
        

def global_function():
    pnt('Hello World')

Test.class_method()
Test().instance_method()
Test.static_method()
global_function()
```

<pre>
<span style="color: #E27DEA;">|Test|</span> <span style="color: #6BE7E7;">(class_method)</span> Hello World
<span style="color: #E27DEA;">|Test|</span> <span style="color: #6BE7E7;">(instance_method)</span> Hello World
<span style="color: #E27DEA;">|Test|</span> <span style="color: #6BE7E7;">(static_method)</span> Hello World
<span style="color: #6BE7E7;">(global_function)</span> Hello World
</pre>

### Style Customization

```python
from pigmento import pnt, Color

pnt.set_display_style(
    method_color=Color.RED,
    method_bracket=('<', '>'),
    class_color=Color.BLUE,
    class_bracket=('[', ']'),
)

Test.class_method()
Test().instance_method()
Test.static_method()
```

<pre>
<span style="color: #6B9BFF;">[Test]</span> <span style="color: #FF6B6B;">&lt;class_method&gt;</span> Hello World
<span style="color: #6B9BFF;">[Test]</span> <span style="color: #FF6B6B;">&lt;instance_method&gt;</span> Hello World
<span style="color: #6B9BFF;">[Test]</span> <span style="color: #FF6B6B;">&lt;static_method&gt;</span> Hello World
</pre>

### Display Mode Customization

```python
from pigmento import pnt

pnt.set_display_mode(
    display_method_name=False,
)

Test.class_method()
```

<pre>
<span style="color: #E27DEA;">|Test|</span> Hello World
</pre>

## Prefixes

Pigmento supports customized prefixes for each print.
It is important to note that all prefixes are in **first-in-first-print** order.

```python
from pigmento import pnt, Prefix, Color, Bracket

pnt.add_prefix(Prefix('DEBUG', bracket=Bracket.DEFAULT, color=Color.GREEN))

global_function()
```

<pre>
<span style="color: #9EE09E;">[DEBUG]</span> <span style="color: #6BE7E7;">(global_function)</span> Hello World
</pre>

### Dynamic Prefix

Texts inside prefix can be dynamically generated.

```python
from pigmento import pnt, Prefix, Color, Bracket

class System:
    STATUS = 'TRAINING'
    
    @classmethod
    def get_status(cls):
        return cls.STATUS
    
    
pnt.add_prefix(Prefix(System.get_status, bracket=Bracket.DEFAULT, color=Color.GREEN))

global_function()
System.STATUS = 'TESTING'
global_function()
```

<pre>
<span style="color: #9EE09E;">[TRAINING]</span> <span style="color: #6BE7E7;">(global_function)</span> Hello World
<span style="color: #9EE09E;">[TESTING]</span> <span style="color: #6BE7E7;">(global_function)</span> Hello World
</pre>

### Build-in Time Prefix

TimePrefix is a build-in prefix that can be used to display time.

```python
import time
import pigmento
from pigmento import pnt

pigmento.add_time_prefix()

Test.class_method()
time.sleep(1)
Test.class_method()
```

<pre>
<span style="color: #9EE09E;">[00:00:00]</span> <span style="color: #E27DEA;">|Test|</span> <span style="color: #6BE7E7;">(class_method)</span> Hello World
<span style="color: #9EE09E;">[00:00:01]</span> <span style="color: #E27DEA;">|Test|</span> <span style="color: #6BE7E7;">(class_method)</span> Hello World
</pre>

## Plugins

Pigmento supports plugins to extend its functionalities.

### Build-in Logger

Everytime you print something, it will be logged to a file.

```python
import pigmento
from pigmento import pnt

pigmento.add_log_plugin('log.txt')

global_function()
```

<pre>
<span style="color: #6BE7E7;">(global_function)</span> Hello World
</pre>

The log file will be created in the current working directory and the content will be removed the color codes.

```bash
cat log.txt
```

<pre>
[00:00:00] (global_function) Hello World
</pre>

### Build-in Dynamic Color

DynamicColor will map caller class names to colors.

```python
import pigmento
from pigmento import pnt


class A:
    @staticmethod
    def print():
        pnt(f'Hello from A')


class B:
    @staticmethod
    def print():
        pnt(f'Hello from B')


class D:
    @staticmethod
    def print():
        pnt(f'Hello from C')


A().print()
B().print()
D().print()

pigmento.add_dynamic_color_plugin()

A().print()
B().print()
D().print()
```

<pre>
<span style="color: #E27DEA;">|A|</span> <span style="color: #6BE7E7;">(print)</span> Hello from A
<span style="color: #E27DEA;">|B|</span> <span style="color: #6BE7E7;">(print)</span> Hello from B
<span style="color: #E27DEA;">|D|</span> <span style="color: #6BE7E7;">(print)</span> Hello from C
<span style="color: #E27DEA;">|A|</span> <span style="color: #6BE7E7;">(print)</span> Hello from A
<span style="color: #FF6B6B;">|B|</span> <span style="color: #6BE7E7;">(print)</span> Hello from B
<span style="color: #FFE156;">|D|</span> <span style="color: #6BE7E7;">(print)</span> Hello from C
</pre>

### Plugin Customization

```python
from pigmento import pnt, BasePlugin


class RenamePlugin(BasePlugin):
    def middleware_before_class_prefix(self, name, bracket, color):
        return name.lower(), bracket, color

    def middleware_before_method_prefix(self, name, bracket, color):
        return name.replace('_', '-'), bracket, color


pnt.add_plugin(RenamePlugin())

Test.class_method()
Test().instance_method()
Test.static_method()
```

<pre>
<span style="color: #E27DEA;">|test|</span> <span style="color: #6BE7E7;">(class-method)</span> Hello World
<span style="color: #E27DEA;">|test|</span> <span style="color: #6BE7E7;">(instance-method)</span> Hello World
<span style="color: #E27DEA;">|test|</span> <span style="color: #6BE7E7;">(static-method)</span> Hello World
</pre>

## Basic Printer Customization

```python
import sys
import time

from pigmento import pnt


def flush_printer(prefix_s, prefix_s_with_color, text, **kwargs):
    sys.stdout.write(f'\r{prefix_s_with_color} {text}')
    sys.stdout.flush()


pnt.set_basic_printer(flush_printer)

def progress(total):
    for i in range(total):
        time.sleep(0.1)  # 模拟工作
        bar = f"Progress: |{'#' * (i + 1)}{'-' * (total - i - 1)}| {i + 1}/{total}"
        pnt(bar)

progress(30)
```

<pre>
(progress) Progress: |#############-----------------| 13/30
</pre>

## Multiple Printers

Pigmento supports multiple printers.

```python
from pigmento import Pigmento, Bracket, Color, Prefix

debug = Pigmento()
debug.add_prefix(Prefix('DEBUG', bracket=Bracket.DEFAULT, color=Color.GREEN))

info = Pigmento()
info.add_prefix(Prefix('INFO', bracket=Bracket.DEFAULT, color=Color.BLUE))

error = Pigmento()
error.add_prefix(Prefix('ERROR', bracket=Bracket.DEFAULT, color=Color.RED))


def divide(a, b):
    if not isinstance(a, int) or not isinstance(b, int):
        error('Inputs must be integers')
        return

    if b == 0:
        debug('Cannot divide by zero')
        return

    info(f'{a} / {b} = {a / b}')


divide(1, 2)
divide(1, 0)
divide('x', 'y')
```

<pre>
<span style="color: #6B9BFF;">[INFO]</span> <span style="color: #6BE7E7;">(divide)</span> 1 / 2 = 0.5
<span style="color: #9EE09E;">[DEBUG]</span> <span style="color: #6BE7E7;">(divide)</span> Cannot divide by zero
<span style="color: #FF6B6B;">[ERROR]</span> <span style="color: #6BE7E7;">(divide)</span> Inputs must be integers
</pre>

## License

MIT License

## Author

[Jyonn](https://liu.qijiong.work)

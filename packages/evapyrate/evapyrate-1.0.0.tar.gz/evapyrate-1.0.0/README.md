<h1 align="center">
  Evapyrate
</h1>

Evapyrate is a fun bijective text transformer. It maps characters into binary, replacing 0 bits with `\u200B` and 1 bits with `\u200C`, joining the bytes together with `\u200D`. Note that the forementioned characters are ZWCs (zero-width characters). In many text spaces, these characters will not be visible and will not appear to take up any space. You can use `repr()` to view the raw unicode sequences if you require.

The text transformer is **bijective**, meaning there is a one-to-one correspondence between the original and the transformed text.

I made this module for fun, it advise against using it in a practical context other than to play around with it.

## Usage

Import the module:

```py
import evapyrate
```

Use the **evaporate** function to encode text:

```py
>>> import evapyrate

>>> evapyrate.evaporate("Hello world!")
'​​‌​​​‍‌‌​​‌​‌‍‌‌​‌‌​​‍‌‌​‌‌​​‍‌‌​‌‌‌‌‍‌​​​​​‍‌‌‌​‌‌‌‍‌‌​‌‌‌‌‍‌‌‌​​‌​‍‌‌​‌‌​​‍‌‌​​‌​​‍‌​​​​‌'
```

Use the **condense** function to decode the text to its original form:

```py
>>> import evapyrate

>>> evapyrate.condense("​​‌​​​‍‌‌​​‌​‌‍‌‌​‌‌​​‍‌‌​‌‌​​‍‌‌​‌‌‌‌‍‌​​​​​‍‌‌‌​‌‌‌‍‌‌​‌‌‌‌‍‌‌‌​​‌​‍‌‌​‌‌​​‍‌‌​​‌​​‍‌​​​​‌")
'Hello world!'
```

## Command Line Interface

The CLI commands work in the same way as the module.

### `eva` (evaporate)

```bash
$ evapyrate eva foo bar
Evaporated: [‌‌​​‌‌​‍‌‌​‌‌‌‌‍‌‌​‌‌‌‌‍‌​​​​​‍‌‌​​​‌​‍‌‌​​​​‌‍‌‌‌​​‌​]
```

Use the `-c` flag to copy to clipboard (assuming pyperclip is installed).

```bash
$ evapyrate eva -c foo bar
Evaporated: [‌‌​​‌‌​‍‌‌​‌‌‌‌‍‌‌​‌‌‌‌‍‌​​​​​‍‌‌​​​‌​‍‌‌​​​​‌‍‌‌‌​​‌​]
Copied to clipboard!
```

### `con` (condense)

```bash
$ evapyrate con ‌‌​​‌‌​‍‌‌​‌‌‌‌‍‌‌​‌‌‌‌‍‌​​​​​‍‌‌​​​‌​‍‌‌​​​​‌‍‌‌‌​​‌​
Condensed: foo bar
```

**Note:** It is difficult to copy the ZWCs from the evaporate function to use in the condense function. It is recommended that you use the `-c` flag when using the `eva` command.

## Installation

Install from pip.

```
pip install evapyrate
```
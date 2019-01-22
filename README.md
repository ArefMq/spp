# SPP
S, and S++ Language Compiler.

### S Language
S is a language used in the theoretical computer science. Using this language you can implement any mathematical functionality.
This language containing only three operands:
- `v <- v + 1`
- `v <- v - 1`
- `if v != 0 goto [L]`

### S++ Language
S++ is an extension on S language. In this new language you can use `@macro` keyword to define *Macro*s (otherwise Functions)
which is very useful in writing actual programs. This extension will first compile the given code into S code. And then,
runs it via the S interpreter introduced for S. Also, this compiler supports comments via *#* sign.

## Requirements
- python2

## Example
Here are some examples on how to run this project:
```bash
./run.py example1.s --input 12
# This will show the result of the example.s file with input(x0=12)

./run.py example2.spp --input 5 10 --verbose
# This will show the result of the example2.spp file with input(x0=5, x1=10)
```

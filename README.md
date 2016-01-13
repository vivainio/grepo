# grepo

![screenshot](https://cloud.githubusercontent.com/assets/557579/12301809/ac1faf54-ba2a-11e5-8efa-4d851df34f76.png
)

Git grep + peco.

Shorthand to make "git grep" and "git checkout" more interactive, with aid of Peco.

Avoid copy-pasting and manually grepping through the branch names by choosing the branch
directly.

Installation: `pip install grepo`

```
usage: grepo [-h] {here,g,p,co,r} ...

positional arguments:
  {here,g,p,co,r}
    here           Set current dir as prjroot
    g              Grep the project
    p              Use peco to quick pick one of the earlier choices
    co             select and check out a branch
    r              select and check out a recently used branch

optional arguments:
  -h, --help       show this help message and exit
```

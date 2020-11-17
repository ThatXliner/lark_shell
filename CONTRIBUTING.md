# How to contribute
<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [How to contribute](#how-to-contribute)
	- [Develop installation](#develop-installation)
	- [Code style](#code-style)
	- [Git commit message](#git-commit-message)
	- [Developing with Poetry](#developing-with-poetry)

<!-- /TOC -->
Since `lark-shell` is still in beta, you can contribute by:

 - Making the UI better
 - Add features (so it can surpass the online [IDE][1])
 - Cross platform support (a.k.a. stop relying on the wonderful [urwid][2] library)
 - Adding a test suite (and code coverage)

## Develop installation

Since this project uses [`poetry`][3] to manage the dependencies, you would have to [install it][4] first:

For *nix/MacOS users:
```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

For Windows PowerShell users:
```PowerShell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -
```

...[`git clone`][5] the repo:

```bash
$ git clone https://github.com/ThatXliner/lark-shell.git
```

and run `poetry lock`:

```bash
$ poetry lock
```

[What does this do?](#developing-with-poetry)

## Code style
See [here][6]

## Git commit message

Use the [GitMoji][7] convention.

## Developing with Poetry

When you do `poetry lock`, it will generate a virtual environment in your project. If it says it can't due to the installed python versions won't be compatible with the required python versions (currently `3.6+`), **do not freak out**. **Do not get yourself into some [Homebrew][8] mess.** Install [PyEnv][9] (*without Homebrew*) and be happy.

`poetry lock` will also generate (or update) the [`poetry.lock`](./poetry.lock) file. This is used for helping with deterministic installation (preventing situations like "well, it worked on my machine").

While there is no `poetry test` command, lark-shell currently does not have a test suite (contribute!).

All changes are welcome :smile:


[1]: https://lark-parser.github.io/lark/ide/app.html "The online Lark 'IDE'"
[2]: http://urwid.org/ "The urwid project homepage"
[3]: https://python-poetry.org/ "Poetry's homepage"
[4]: https://python-poetry.org/docs/#installation "How to install Poetry"
[5]: https://www.git-scm.com/docs/git-clone "Git clone man page"
[6]: https://github.com/ThatXliner/Significant-files/blob/main/PYTHON_STYLE.md "Simple python style guide"
[7]: https://gitmoji.carloscuesta.me "The GitMoji specification"
[8]: https://brew.sh/ "The Homebrew Homepage"
[9]: https://github.com/pyenv/pyenv "Pyenv's Repo"

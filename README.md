# Nginx Language Server

[![image-version](https://img.shields.io/pypi/v/nginx-language-server.svg)](https://python.org/pypi/nginx-language-server)
[![image-license](https://img.shields.io/badge/license-GPL%203.0--only-orange)](https://python.org/pypi/jedi-language-server)
[![image-python-versions](https://img.shields.io/badge/python->=3.9-blue)](https://python.org/pypi/jedi-language-server)

A [Language Server](https://microsoft.github.io/language-server-protocol/) for `nginx.conf`.

Still under construction, expect big / potentially breaking changes for a while.

## Capabilities

nginx-language-server currently partially supports the following Language Server capabilities with more to be added in the future.

### Language Features

- [textDocument/completion](https://microsoft.github.io/language-server-protocol/specifications/specification-current/#textDocument_completion)
- [textDocument/hover](https://microsoft.github.io/language-server-protocol/specifications/specification-current/#textDocument_hover)

## Installation

From your command line (bash / zsh), run:

```bash
pip install -U nginx-language-server
```

`-U` ensures that you're pulling the latest version from pypi.

Alternatively, consider using [pipx](https://github.com/pipxproject/pipx) to keep nginx-language-server isolated from your other Python dependencies.

## Editor Setup

The following instructions show how to use nginx-language-server with your development tooling. The instructions assume you have already installed nginx-language-server.

### Vim / Neovim

With [coc.nvim](https://github.com/neoclide/coc.nvim), put the following in `coc-settings.json`:

```json
{
  "languageserver": {
    "nginx-language-server": {
      "command": "nginx-language-server",
      "filetypes": ["nginx"],
      "rootPatterns": ["nginx.conf", ".git"]
    }
  }
}
```

In your vimrc, I recommend putting in the following lines to ensure variables complete / hover correctly:

```vim
augroup custom_nginx
  autocmd!
  autocmd FileType nginx setlocal iskeyword+=$
  autocmd FileType nginx let b:coc_additional_keywords = ['$']
augroup end
```

Alternatively, you can use [coc-nginx](https://github.com/yaegassy/coc-nginx).

```vim
let g:coc_global_extensions = ['@yaegassy/coc-nginx']
```

Note: this list is non-exhaustive. If you know of a great choice not included in this list, please submit a PR!

## Command line

nginx-language-server can be run directly from the command line.

```console
$ nginx-language-server --help
usage: nginx-language-server [-h] [--version] [--tcp] [--host HOST]
                             [--port PORT] [--log-file LOG_FILE] [-v]

Nginx language server: an LSP server for nginx.conf.

optional arguments:
  -h, --help           show this help message and exit
  --version            display version information and exit
  --tcp                use TCP server instead of stdio
  --host HOST          host for TCP server (default 127.0.0.1)
  --port PORT          port for TCP server (default 2088)
  --log-file LOG_FILE  redirect logs to the given file instead of writing to
                       stderr
  -v, --verbose        increase verbosity of log output

Examples:

    Run from stdio: nginx-language-server
```

## Inspiration

The useful language data for nginx is ported from [vscode-nginx-conf-hint](https://github.com/hangxingliu/vscode-nginx-conf-hint). I would have used this library directly, but alas! It's written only for VSCode and I use Neovim.

## Written by

Samuel Roeca _samuel.roeca@gmail.com_

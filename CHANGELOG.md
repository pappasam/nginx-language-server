# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.7.1

### Added

- Some metadata to pyproject.toml. This will hopefully make pypi easier to navigate.

### Fixed

- ifinlocation context (special case based on our strange parsing) has been appropriately handled.

## 0.7.0

### Added

- Support for the "any" context. Some directives can be used anywhere, so now they're actually show up in completions and hover.
- Necessary files for the download script to work correctly. Thanks <https://github.com/hangxingliu/vscode-nginx-conf-hint>!

### Changed

- Regenerated nginx docs from web.

## 0.6.0

### Added

- Configurable logging (including the option to log to a file)
- TCP support

### Changed

- Migrate from click to argparse
- Upgrade pygls to 0.10.3+, fixing breaking public api changes where applicable

## 0.5.1

### Fixed

- Explicitly set file format to "UTF-8" when reading data files from disk. This resolves <https://github.com/pappasam/nginx-language-server/issues/7>, in which Windows Python incorrectly identified the file formats as "cp932".

## 0.5.0

### Changed

- Generated the latest docs using the scripts from vscode-nginx-hint (as of 2021-02-25). Might make this a more regular practice.

## 0.4.0

### Added

- Variable completion for variables names appended with `_name`, like `http`. These refer to http headers based on the characters.

### Changed

- Words that aren't symbols no longer hover. You now need your cursor over an actual symbol to get hover.

## 0.3.0

### Added

- Variable completion
- pydantic ; pre-processes items on server start for performance. There's definitely more to do here, but this works for now.

## 0.2.0

### Added

- This changelog
- Support for markup kind markdown
- Docstrings how complete with all available information about a directive for completion and hover.

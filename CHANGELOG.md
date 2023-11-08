# Changelog

The format of this changelog is based on
[Keep a Changelog](http://keepachangelog.com/en/1.0.0/). The project adheres to
[Semantic Versioning](http://semver.org/spec/v2.0.0.html)

## [Unreleased]

## [1.0.1] <a name="1.0.1" href="#1.0.1">-</a> November 08, 2023

- Allow multiline strings in field descriptions.
- Do not add `Attributes:` if there are no fields to document or if it is already present.

## [1.0.0] <a name="1.0.0" href="#1.0.0">-</a> November 06, 2023

- Based on the mkdocstrings-python handler. It is a copy of the code with
  minor changes to create documentation using pydantic fields.
- Adds functionality to document cli arguments and options.

[unreleased]: https://github.com/jmlopez-rod/mkdocstrings-m_cli/compare/1.0.1...HEAD
[1.0.1]: https://github.com/jmlopez-rod/mkdocstrings-m_cli/compare/1.0.0...1.0.1
[1.0.0]: https://github.com/jmlopez-rod/mkdocstrings-m_cli/compare/65a80f01707d25b9cd80469d5b944e44a97a3c3f...1.0.0

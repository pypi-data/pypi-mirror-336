# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.5] - 2024-12-17

### Fix

- Refactor for the use of `param.parameters._dict_update` to simply use `dict`

### Changed

- Changed project to be dynamically versioned from git tags

## [0.3.4] - 2024-11-03

### Fix

- `AESOptArray`, `shape` was not fetching shape from string
- `AESOptArray`, `default` was returned when using `.as_dict(onlychanged=False)`
- `AESOptArray`, Add possibility to set array with a scalar if `shape` is set
- `default_ref`, fix for setting `Reference` directly 

## [0.3.3] - 2024-10-11

### Added

- `max_arr_size`, for `display_json_data` to avoid printing large amounts of data for large dict's
- `.display` method for `AESOptParametrized` to add more control over the rendering 

### Changed

- HTML rendering of `AESOptParametrized` to render values of entries by default. Rendering `list`, `dict` and `ndarray` using `json2html`.

## [0.3.2] - 2024-10-09

### Fix

- `AESOptString`, was missing `___slots__=["default_ref"]` (lead to missing rendering for refs in HTML)

## [0.3.1] - 2024-10-07

### Changed

- `display_json_data`, smoother rendering and extended argument specs

## [0.3.0] - 2024-10-07

### Added 

- `AESOptInteger`, Integer parameter which allow to set references and functions
- `AESOptBoolean`, Boolean parameter which allow to set references and functions
- `.has_parent`, to `AESOptParametrized`. Can be used to test if object is *root*
- `utils.json_utils`, tools for reading and writing json with numpy data
- `utils.html_repr.json_data_render`, tool for rendering json-data in notebook
- `utils.copy_param` and `utils.copy_param_ref`, tools for copying parameters while allowing to update/remove some elements. Useful for linking two parameters.

### Fix

- Bug-fix for `AESOptNumber` with `allow_none` to `allow_None`

### Changed

- Allowed `ListOfParametrized` to initialize from function by adding `default_call`

## [0.2.0] - 2024-09-27

### Added 

- `AESOptString`, extension of `param.Sting` which adds *default_ref*

## [0.0.1] - 2024-08-06

### Fixed 

- Included `unit_library.ini` in the wheel build (added to `pyproject.toml`)

## [0.0.0] - 2024-05-06
First version

### Added

- `AESOptParametrized`, an extension of the `param.Parametrized`
- `SubParameterized`, dedicated parameter for adding nested parametrized models
- `ListOfParameterized`, dedicated parameters for adding a list of parametrized models
- `AESOptNumber`, extension of `param.Number` which adds *units* and *default_ref*
- `AESOptArray`, extension of `param.Array` which adds *bounds*, *units*, *dtype*, *shape*, *default_full*, *default_interp*,  *default_ref*units

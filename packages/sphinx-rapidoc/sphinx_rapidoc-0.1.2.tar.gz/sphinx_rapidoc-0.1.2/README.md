# Sphinx-RapiDoc

[![PyPI version](https://badge.fury.io/py/sphinx-rapidoc.svg)](https://badge.fury.io/py/sphinx-rapidoc)
[![Python Versions](https://img.shields.io/pypi/pyversions/sphinx-rapidoc.svg)](https://pypi.org/project/sphinx-rapidoc/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Sphinx extension that integrates RapiDoc to render beautiful, customizable, and interactive API documentation from OpenAPI/Swagger specifications.

## Features

- 🚀 Quick and easy integration with Sphinx documentation
- 🎨 Customizable themes (light/dark)
- 🔄 Multiple rendering styles (read/view/focused)
- 🔒 Support for authentication
- ⚡ Interactive API testing interface
- 📱 Responsive design
- 🔍 Search functionality
- 📖 Support for OpenAPI v2.0 (Swagger) and v3.0

## Installation

Install the package using pip:

```bash
pip install sphinx-rapidoc
```

Or install directly from GitHub for the latest version:

```bash
pip install git+https://github.com/TirthS24/sphinx_rapidoc
```

## Quick Start

1. Add `sphinx_rapidoc` to your Sphinx extensions in `conf.py`:
   ```python
   extensions = [
       # ... your other extensions
       'sphinx_rapidoc'
   ]
   ```

2. Create a new RST file (e.g., `api.rst`) with the RapiDoc directive:
   ```rst
   API Documentation
   ================

   .. rapidoc::
       :spec-url: https://api.example.com/openapi.json
       :theme: light
       :render-style: view
   ```

3. Include your RST file in `index.rst`:
   ```rst
   .. toctree::
      :maxdepth: 2
      :caption: Contents:

      api
   ```

4. Build your documentation:
   ```bash
   make html
   ```

## Configuration Options

### Directive Options

| Option         | Description                              | Default | Values                    |
|----------------|------------------------------------------|---------|---------------------------|
| `spec-url`     | URL to OpenAPI/Swagger specification     | None    | Valid URL                |
| `theme`        | UI theme                                 | `light` | `light`, `dark`          |
| `render-style` | Documentation rendering style            | `view`  | `view`, `read`, `focused`|

## Examples

### Basic Usage
```rst
.. rapidoc::
    :spec-url: http://127.0.0.1:5500/src/petstore.yml
    :theme: light
    :render-style: view
```

### Dark Theme with Read Style
```rst
.. rapidoc::
    :spec-url: http://127.0.0.1:5500/src/petstore.yml
    :theme: dark
    :render-style: read
```

## Screenshots

### Endpoint and Authentication Sections
![Endpoint and Authentication sections](./utils/view.png)

### Sample GET Request Interface
![Sample GET Request](./utils/request.png)

## Requirements

- Python 3.9 or higher
- Sphinx 2.0 or higher
- Valid OpenAPI/Swagger specification (JSON or YAML format)
- Web browser with JavaScript enabled

## Common Issues and Solutions

### CORS Errors
If you encounter CORS errors, ensure that:
1. Your API specification URL is accessible from the hosted server
2. The server hosting your API specification has appropriate CORS headers
3. You're using HTTPS if your documentation is hosted on HTTPS

### Specification Not Loading
- Verify that your specification URL is publicly accessible
- Check if the URL returns valid JSON/YAML in OpenAPI/Swagger format
- Ensure your specification follows OpenAPI standards

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [RapiDoc](https://mrin9.github.io/RapiDoc/) for the awesome API documentation renderer
- [Sphinx](https://www.sphinx-doc.org/) for the excellent documentation generator

## Support

If you encounter any issues or have questions, please:
1. Check the [Common Issues](#common-issues-and-solutions) section
2. Open an issue on GitHub
3. Contact the maintainers
  - [Tirth Shah](mailto:tirthshah100@gmail.com)
  - [Aksh Patel](mailto:aksh@york.ie)
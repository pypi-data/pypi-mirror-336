# tests/test_rapidoc.py
import os
import pytest

def test_static_files_exist():
    """Test that required static files exist"""
    # Get the package root directory
    package_root = os.path.dirname(os.path.dirname(__file__))
    
    # Test static directory and JS file
    static_dir = os.path.join(package_root, 'sphinx_rapidoc', 'static')
    js_file = os.path.join(static_dir, 'rapidoc.min.js')
    
    assert os.path.exists(static_dir), "Static directory doesn't exist"
    assert os.path.exists(js_file), "rapidoc.min.js doesn't exist"

def test_template_files_exist():
    """Test that template files exist"""
    # Get the package root directory
    package_root = os.path.dirname(os.path.dirname(__file__))
    
    # Test templates directory and HTML file
    templates_dir = os.path.join(package_root, 'sphinx_rapidoc', 'templates')
    html_file = os.path.join(templates_dir, 'rapidoc.html')
    
    assert os.path.exists(templates_dir), "Templates directory doesn't exist"
    assert os.path.exists(html_file), "rapidoc.html doesn't exist"

def test_package_structure():
    """Test that basic package files exist"""
    # Get the package root directory
    package_root = os.path.dirname(os.path.dirname(__file__))
    
    # Test core package files
    assert os.path.exists(os.path.join(package_root, 'setup.py')), "setup.py doesn't exist"
    assert os.path.exists(os.path.join(package_root, 'README.md')), "README.md doesn't exist"
    assert os.path.exists(os.path.join(package_root, 'LICENSE')), "LICENSE doesn't exist"
    assert os.path.exists(os.path.join(package_root, 'sphinx_rapidoc', '__init__.py')), "__init__.py doesn't exist"
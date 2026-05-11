#!/usr/bin/env python3
"""
Lint script for Connect Four CLI project.
Enforces layered architecture and code quality rules.
"""

import ast
import os
import sys
from pathlib import Path
from typing import List, Tuple, Optional

# Layer definitions and allowed imports
LAYERS = ['utils', 'providers', 'config', 'types', 'repo', 'service', 'runtime', 'ui']

# Map each layer to the layers it may import from
ALLOWED_IMPORTS = {
    'utils': ['utils'],
    'providers': ['utils', 'providers', 'types', 'config'],
    'config': ['types', 'config'],
    'types': ['types'],
    'repo': ['types', 'config', 'repo'],
    'service': ['types', 'config', 'repo', 'providers', 'service'],
    'runtime': ['types', 'config', 'repo', 'service', 'providers', 'runtime'],
    'ui': ['types', 'config', 'service', 'runtime', 'providers', 'ui'],
}

# Max lines per file
MAX_LINES = 300

# Source directory
SRC_DIR = Path(__file__).parent / 'src'


def get_layer(filepath: Path) -> Optional[str]:
    """Determine which layer a file belongs to."""
    try:
        rel_path = filepath.relative_to(SRC_DIR)
        parts = rel_path.parts
        if parts:
            return parts[0]
    except ValueError:
        pass
    return None


def get_allowed_imports(layer: str) -> List[str]:
    """Get list of layers that given layer may import from."""
    return ALLOWED_IMPORTS.get(layer, [])


def check_imports(filepath: Path, tree: ast.AST, layer: str) -> List[Tuple[int, str]]:
    """Check that imports respect layer dependency rules."""
    violations = []
    allowed = get_allowed_imports(layer)
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported = alias.name.split('.')[0]
                if imported in LAYERS and imported not in allowed:
                    violations.append((
                        node.lineno,
                        f"Line {node.lineno}: '{filepath.name}' in layer '{layer}' "
                        f"may not import from layer '{imported}'. "
                        f"Allowed imports: {', '.join(allowed)}."
                    ))
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imported = node.module.split('.')[0]
                if imported in LAYERS and imported not in allowed:
                    violations.append((
                        node.lineno,
                        f"Line {node.lineno}: '{filepath.name}' in layer '{layer}' "
                        f"may not import from layer '{imported}' (from {node.module}). "
                        f"Allowed imports: {', '.join(allowed)}."
                    ))
    
    return violations


def check_line_count(filepath: Path) -> List[Tuple[int, str]]:
    """Check that file does not exceed MAX_LINES."""
    violations = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if len(lines) > MAX_LINES:
            violations.append((
                len(lines),
                f"Line {len(lines)}: '{filepath.name}' has {len(lines)} lines, "
                f"exceeds maximum of {MAX_LINES}. "
                f"Split into smaller modules within the same layer."
            ))
    except Exception as e:
        pass
    
    return violations


def lint_file(filepath: Path) -> List[Tuple[int, str, str]]:
    """Lint a single file. Returns list of (line_number, file_path, message)."""
    violations = []
    
    # Check if file is under src/
    try:
        rel_path = filepath.relative_to(Path.cwd())
        if not str(rel_path).startswith('src/'):
            return []  # Skip non-src files
    except ValueError:
        return []
    
    # Check file extension
    if not filepath.suffix == '.py':
        return []
    
    layer = get_layer(filepath)
    if layer is None:
        violations.append((
            0,
            str(filepath),
            f"File '{filepath.name}' is not in a valid layer directory. "
            f"Files under src/ must be in one of: {', '.join(LAYERS)}."
        ))
        return violations
    
    # Read file content
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        violations.append((
            0,
            str(filepath),
            f"Could not read file: {e}"
        ))
        return violations
    
    # Check line count
    violations.extend(check_line_count(filepath))
    
    # Parse AST and check imports
    try:
        tree = ast.parse(content)
        import_violations = check_imports(filepath, tree, layer)
        for line_num, msg in import_violations:
            violations.append((line_num, str(filepath), msg))
    except SyntaxError as e:
        violations.append((
            e.lineno or 0,
            str(filepath),
            f"Syntax error: {e.msg} at line {e.lineno}"
        ))
    
    return violations


def lint_all_files() -> List[Tuple[int, str, str]]:
    """Lint all Python files in the project."""
    violations = []
    
    # Walk src/ directory
    if SRC_DIR.exists():
        for root, dirs, files in os.walk(SRC_DIR):
            for filename in files:
                if filename.endswith('.py'):
                    filepath = Path(root) / filename
                    violations.extend(lint_file(filepath))
    
    return violations


def main():
    """Main entry point."""
    violations = lint_all_files()
    
    if not violations:
        print("✓ All checks passed!")
        return 0
    
    # Sort by file path, then line number
    violations.sort(key=lambda v: (v[1], v[0]))
    
    print(f"\n✗ Found {len(violations)} violation(s):\n")
    for line_num, filepath, message in violations:
        print(f"{filepath}:{line_num}:")
        print(f"  {message}\n")
    
    return 1


if __name__ == '__main__':
    sys.exit(main())

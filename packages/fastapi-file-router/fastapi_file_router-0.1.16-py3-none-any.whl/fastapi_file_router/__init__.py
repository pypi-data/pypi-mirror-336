"""
FastAPI File Router - A dynamic route loader for FastAPI applications based on file structure.
"""

from fastapi_file_router.router import load_routes, square_to_curly_brackets, walk, log

__all__ = ["load_routes", "square_to_curly_brackets", "walk", "log"]


import os
import pytest
from io import StringIO
import sphinx

pytest_plugins = 'sphinx.testing.fixtures'

# Get test project dir
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.join(current_dir, "error_project")
src_dir = os.path.join(project_dir, "source")
build_dir = os.path.join(project_dir, "build")

from pathlib import Path
build_dir = Path(build_dir)

@pytest.mark.sphinx(
        buildername='html',
        srcdir=src_dir,
        builddir=build_dir,
        freshenv = True,
        )
def test_error_project(app, status, warning,):

   # Run Sphinx build
   app.build()

   # Verify the output status
   assert 0 == app.statuscode
   assert "build succeeded" in status.getvalue()  # Build succeeded

   # Verify the output file contains expected statements
   output_file_index = os.path.join(app.outdir, "index.html")
   assert os.path.exists(output_file_index)
   with open(output_file_index, "r") as f:
      output_content = f.read()

      assert "<p>ElifDirective without previous text shall be in the output." in output_content
      assert "<p>IfDirective /Undefined element in condition/ text shall be in the output." in output_content
      assert "<p>IfDirective /Empty condition/ text shall not be in the output." not in output_content
      assert "<p>ElIfDirective /Undefined element in condition/ text before shall not be in the output." not in output_content
      assert "<p>ElIfDirective /Undefined element in condition/ text shall be in the output." in output_content
      assert "<p>ElIfDirective /Empty condition/ text before shall not be in the output." not in output_content
      assert "<p>ElIfDirective /Empty condition/ text shall not be in the output." not in output_content
      assert "<p>ElIfDirective /Missing IfDirective before ElIfDirective with evaluating to True/ text shall be in the output." in output_content
      assert "<p>ElIfDirective /Missing IfDirective before ElIfDirective with evaluating to False/ text shall not be in the output." not in output_content
      assert "<p>ElseDirective /Missing IfDirective before ElseDirective/ text shall be in the output." in output_content

   # Verify expected warnings occuring
   warnings = warning.getvalue().strip()
   assert "/index.rst:1: WARNING: ElIfDirective: without a preceding IfDirective or ElIfDirective. Maybe there is something wrong with the intendition. [ifelse.ElIfDirective]" in warnings
   assert "/index.rst:12: WARNING: IfDirective: exception while evaluating expression: name 'a' is not defined [ifelse.IfDirective]" in warnings
   assert '/index.rst:19: ERROR: Error in "if" directive:' in warnings
   assert "/index.rst:33: WARNING: ElIfDirective: exception while evaluating expression: name 'a' is not defined [ifelse.ElIfDirective]" in warnings
   assert '/index.rst:44: ERROR: Error in "elif" directive:' in warnings
   assert "/index.rst:52: WARNING: ElIfDirective: without a preceding IfDirective or ElIfDirective. Maybe there is something wrong with the intendition. [ifelse.ElIfDirective]" in warnings
   assert "/index.rst:59: WARNING: ElIfDirective: without a preceding IfDirective or ElIfDirective. Maybe there is something wrong with the intendition. [ifelse.ElIfDirective]" in warnings
   assert "/index.rst:69: WARNING: ElseDirective: without a preceding IfDirective or ElIfDirective. Maybe there is something wrong with the intendition. [ifelse.ElseDirective]" in warnings


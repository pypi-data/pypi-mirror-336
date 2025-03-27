import os
import pytest
from io import StringIO
from sphinx.application import Sphinx

def test_example_project():

   # Get test project dir
   current_dir = os.path.dirname(os.path.abspath(__file__))
   project_dir = os.path.join(current_dir, "test_project")
   src_dir = os.path.join(project_dir, "source")
   build_dir = os.path.join(project_dir, "build")

   # Run Sphinx build
   statusObject = StringIO()
   warningObject = StringIO()
   app = Sphinx(
         srcdir = src_dir,
         confdir = src_dir,
         outdir = build_dir,
         doctreedir = build_dir,
         buildername = "html",
         status = statusObject,
         warning = warningObject,
         freshenv = True,
      )
   app.build()

   # Verify the output
   output_file_index = os.path.join(build_dir, "index.html")
   assert os.path.exists(output_file_index)

   output_file_elif_else_examples = os.path.join(build_dir, "elif_else_examples.html")
   assert os.path.exists(output_file_elif_else_examples)
   with open(output_file_elif_else_examples, "r") as f:
      output_content = f.read()
      assert "Coded variants.1.1 shall not be in the output." not in output_content
      assert "Coded variants.1.2 shall not be in the output." not in output_content
      assert "Coded variants.1.3 shall be in the output."         in output_content
      assert "Coded variants.1.4 shall not be in the output." not in output_content
      assert "Coded variants.2.1 shall not be in the output." not in output_content
      assert "Coded variants.2.2 shall not be in the output." not in output_content
      assert "Coded variants.2.3 shall be in the output."         in output_content
      assert "Coded variants.2.4 shall not be in the output." not in output_content

   output_file_minimum_example = os.path.join(build_dir, "minimum_example.html")
   assert os.path.exists(output_file_minimum_example)
   with open(output_file_minimum_example, "r") as f:
      output_content = f.read()
      assert "This content is included." in output_content
      assert "This content is excluded." not in output_content
      assert "This content is also excluded." not in output_content

   output_file_spacing_examples = os.path.join(build_dir, "spacing_examples.html")
   assert os.path.exists(output_file_spacing_examples)
   with open(output_file_spacing_examples, "r") as f:
      output_content = f.read()
      assert "Working spaces.1.1 shall not be in the output." not in output_content
      assert "Working spaces.1.2 shall be in the output."         in output_content
      assert "Working spaces.2.1 shall not be in the output." not in output_content
      assert "Working spaces.2.2 shall be in the output."         in output_content
      assert "Working spaces.3.1 shall not be in the output." not in output_content
      assert "Working spaces.3.2 shall be in the output."         in output_content
      assert "Working spaces.4.1 shall not be in the output." not in output_content
      assert "Working spaces.4.2 shall be in the output."         in output_content
      assert "Working spaces.5.1 shall not be in the output." not in output_content
      assert "Working spaces.5.2 shall be in the output."         in output_content

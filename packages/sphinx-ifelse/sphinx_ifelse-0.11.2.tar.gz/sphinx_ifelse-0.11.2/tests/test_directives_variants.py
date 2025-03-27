import os
import pytest
from sphinx.application import Sphinx

def transform_number_in_range(number: int)->int:
   if 1 <= number and number <= 3:
      out_number = number
   else:
      out_number = 4
   return out_number


def test_variants_project():
   for l1 in range(0, 5, 1):
      for l2 in range(0, 5, 1):
         for l3 in range(0, 5, 1):
            version_of_variants_project(l1, l2, l3)


def version_of_variants_project(l1: int, l2: int, l3: int):

   # Get test project dir
   current_dir = os.path.dirname(os.path.abspath(__file__))
   project_dir = os.path.join(current_dir, "variants_project")
   src_dir = os.path.join(project_dir, "source")
   build_dir = os.path.join(project_dir, "build")

   l_s = str(l1) + str(l2) + str(l3)
   build_dir = os.path.join(build_dir, l_s)

   ifelse_variants = {
      'l1': l1,
      'l2': l2,
      'l3': l3,
   }

   confoverrides = {
      'ifelse_variants': ifelse_variants
   }

   # Run Sphinx build
   app = Sphinx(
         srcdir = src_dir,
         confdir = src_dir,
         outdir = build_dir,
         doctreedir = build_dir,
         buildername = "html",
         freshenv = True,
         confoverrides = confoverrides,
      )

   app.build()

   # Verify the output
   output_file_index = os.path.join(build_dir, "index.html")
   assert os.path.exists(output_file_index)

   l_s_expected = str(transform_number_in_range(l1)) + \
                  str(transform_number_in_range(l2)) + \
                  str(transform_number_in_range(l3))
   l_s_expected = '<p>' + l_s_expected + '</p>'

   with open(output_file_index, "r") as f:
      output_content = f.read()
      for l1o in range(0, 5, 1):
         for l2o in range(0, 5, 1):
            for l3o in range(0, 5, 1):
               l_s_o = str(transform_number_in_range(l1o)) + \
                       str(transform_number_in_range(l2o)) + \
                       str(transform_number_in_range(l3o))
               l_s_o = '<p>' + l_s_o + '</p>'

               l_s_no = str(l1o) + str(l2o) + str(l3o)
               l_s_no = '<p>' + l_s_no + '</p>'

               if l_s_o == l_s_expected:
                  assert l_s_o in output_content
               else:
                  assert l_s_o not in output_content

               if l_s_no == l_s_expected:
                  assert l_s_no in output_content
               else:
                  assert l_s_no not in output_content


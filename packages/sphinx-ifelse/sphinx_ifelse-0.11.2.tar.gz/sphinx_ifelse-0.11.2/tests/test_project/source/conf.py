# -- General configuration ------------------------------------------------

project = 'Test Project'

extensions = [
   'sphinx_ifelse',
]

# -- extension configuration: ifelse --------------------------------------

ifelse_variants = {
   # for elif_else_examples
   # and spacing_examples
   'l1': 3,
   'l2': 3,
   'l3': 3,

   # for minimum_example
   'VARIANT1': True,
   'VARIANT2': False,
}

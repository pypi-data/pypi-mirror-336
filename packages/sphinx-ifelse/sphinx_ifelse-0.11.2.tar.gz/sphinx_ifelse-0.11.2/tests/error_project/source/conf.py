# -- General configuration ------------------------------------------------

project = 'Test Project'

extensions = [
   'sphinx_ifelse',
]

# -- extension configuration: ifelse --------------------------------------

ifelse_variants = {
   'html': True,
   'latex': False,
   'pdf': False,
   'epub': False,
   'l1': 3,
   'l2': 3,
   'l3': 3,
}

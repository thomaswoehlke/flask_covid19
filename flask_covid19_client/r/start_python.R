install.packages("reticulate")
# Start python ( this installs miniconda, if there is no python defined )
#reticulate::repl_python()

library(reticulate)
use_virtualenv('r-reticulate')
py_install('wget')
py_install('subprocess')


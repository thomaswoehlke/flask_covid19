#!/usr/bin/env python

# Installation of required packages

required_packages_optional01 = [ 
  "ca",
  "askpass",
  "assertthat",
  "backports",
  "base64enc",
  "BH",
  "bit",
  "bit64",
  "blob",
  "brew",
  "broom",
  "ca",
  "callr",
  "cellranger"
]
required_packages_optional02 = [ 
  "checkmate",
  "classInt",
  "cli",
  "clipr",
  "clisymbols",
  "colorspace",
  "commonmark",
  "cpp11",
  "crayon",
  "crosstalk"
]
required_packages_optional03 = [ 
  "curl",
  "dbplyr",
  "dplyr",
  "desc",  
  "scales",
  "DescTools",
  "details",
  "digest",
  "DT",
  "e1071",
]
required_packages_optional04 = [ 
  "evaluate",
  "Exact",
  "expm",
  "extrafont",
  "extrafontdb",
  "fansi",
  "farver",
  "fastmap",
  "fastmatch",
  "forcats",
  "Formula"
]
required_packages_optional05 = [ 
  "fs",
  "generics",
  "GGally",
  "gh",
  "git2r",
  "glue",
  "gridExtra",
  "gtable",
  "haven",
  "highr",
  "hms",
  "httpuv",
  "hunspell",
  "hutils",
  "ini"
]
required_packages_optional06 = [ 
  "isoband",
  "jsonlite",
  "knitcitations",
  "labeling",
  "later",
  "lazyeval"
]
required_packages_optional07 = [ 
  "lifecycle",
  "lubridate",
  "magrittr",
  "manipulate"
]
required_packages_optional08 = [ 
  "maptools",
  "memoise",
  "mime",
  "mnormt",
  "modelr",
  "munsell",
]
required_packages_optional09 = [ 
  "plotrix",
  "plyr",
  "png",
  "praise",
  "prettyunits",
  "processx",
  "progress",
  "promises"
]
required_packages_optional10 = [ 
  "ps",
  "psych",
  "purrr",
  "R6",
  "rappdirs",
  "rcmdcheck",
  "RColorBrewer",
  "Rcpp"
]
required_packages_optional11 = [ 
  "readxl",
  "rematch",
  "rematch2",
  "remotes",
  "reprex",
  "reshape",
  "reshape2",
  "rex",
  "rlang"
]
required_packages_optional12 = [ 
  "R.methodsS3",
  "R.oo",
  "roxygen2",
  "Rttf2pt1",
  "scales",
  "selectr",
  "sp",
  "stringi",
  "stringr",
  "svgPanZoom"
]
required_packages_optional13 = [ 
  "sys",
  "testthat",
  "tibble",
  "tidyr",
  "tidyselect",
  "tmvnsim"
]
required_packages_optional14 = [ 
  "vctrs",
  "viridisLite",
  "whisker",
  "withr",
  "writexl",
  "xfun",
  "xopen",
  "xtable",
  "zoo"
]
required_packages_optional15 = [ 
  "pheatmap",
  "pillar",
  "plogr"
]
optional_packages_collection = [ 
  required_packages_optional01,
  required_packages_optional02,
  required_packages_optional03,
  required_packages_optional04,
  required_packages_optional05,
  required_packages_optional06,
  required_packages_optional07,
  required_packages_optional08,
  required_packages_optional09,
  required_packages_optional10,
  required_packages_optional11,
  required_packages_optional12,
  required_packages_optional13,
  required_packages_optional14,
  required_packages_optional15
]


print("################## START #######################################")

for required_packages in optional_packages_collection:
  for required_package in required_packages:
    print('r-cran-' + required_package.lower() + ' ')
    #print('install.packages("' + required_package + '")')

print("################## R ###########################################")

for required_packages in optional_packages_collection:
  for required_package in required_packages:
    #print('r-cran-' + required_package + ' ')
    print('install.packages("' + required_package + '")')
    
print("################## DONE ########################################")

#!/usr/bin/env python

required_packages_covid19= [ 
  "COVID19"#,
  #"covid19nytimes",
  #"covidregionaldata"
]
required_packages_optional_fileformats= [ 
  "utf8",
  "yaml",
  "xml2"
]
required_packages_shiny= [ 
  "shiny",
  "shinyWidgets",
  "htmlwidgets"
]
required_packages_tex_und_pdf= [ 
  "htmltools",
  "knitr",
  "pdftools",
  "pdftables",
  "abind",
  "pdfCluster",
  "knitr",
  "knitLatex",
  #"TexMix",
  "texPreview",
  "bibtex",
  "tinytex",
  "bookdown",
  "xaringan",
  "flextable"
]
required_packages_rstudio= [ 
  "devtools",
  "sourcetools",
  "pkgbuild",
  "pkgconfig",
  "pkgload",
  "markdown",
  "rmarkdown",
  "rprojroot",
  "rstudioapi",
  "renv",
  "readr",
  "rgdal",
  "sessioninfo",
  "survival",
  "miniUI",
  "ellipsis"
]
required_packages_aufgaben= [ 
  "tidyverse",
  "ggplot2",
  "reshape2",
  "data.table",
  "dplyr",
  "ca",
  "viridis",
  "tm",
  "SnowballC",
  "wordcloud",
  "wordcloud2"
]
required_packages_database= [ 
  "solrium",
  "shiny",
  "dplyr",
  "pool",
  "RPostgres",
  "DBI",
  "RSQLite",
  "RMariaDB",
  "data.table"
]
required_packages_maps= [ 
  "maptools",
  "mapview"
]
required_packages_last_changes= [ 
  "curl",
  "ini"
]

required_packages_collection= [ 
  required_packages_rstudio,
  required_packages_optional_fileformats,
  required_packages_tex_und_pdf,
  required_packages_shiny,
  required_packages_aufgaben,
  #required_packages_covid19,
  required_packages_database,
  required_packages_maps,
  required_packages_last_changes
]

print("################## START #######################################")

for required_packages in required_packages_collection:
  for required_package in required_packages:
    print('r-cran-' + required_package.lower() + ' ')
    #print('install.packages("' + required_package + '")')
    
print("################## R ###########################################")

for required_packages in required_packages_collection:
  for required_package in required_packages:
    #print('r-cran-' + required_package + ' ')
    print('install.packages("' + required_package + '")')

print("################## DONE ########################################")

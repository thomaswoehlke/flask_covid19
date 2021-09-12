#!/usr/bin/env python

libs = [ 
  "devtools" , 
  "sourcetools" , 
  "pkgbuild" , 
  "pkgconfig" , 
  "pkgload" , 
  "markdown" , 
  "markdownInput" , 
  "rmarkdown" , 
  "rprojroot" , 
  "rstudioapi" , 
  "renv" , 
  "readr" , 
  "rgdal" , 
  "sessioninfo" , 
  "survival" , 
  "miniUI" , 
  "ellipsis" , 
  "utf8" , 
  "yaml" , 
  "xml2" , 
  "htmltools" , 
  "knitr" , 
  "pdftools" , 
  "pdftables" , 
  "pdfminer" , 
  "PDFEstimator" , 
  "abind" , 
  "pdfCluster" , 
  "knitr" , 
  "knitrBootstrap" , 
  "knitrdata" , 
  "knitrProgressBar" , 
  "knitLatex" , 
  "TeXCheckR" , 
  "texPreview" , 
  "bibtex" , 
  "tinytex" , 
  "latexpdf" , 
  "blogdown" , 
  "bookdown" , 
  "bookdownplus" , 
  "xaringan" , 
  "xaringanthemer" , 
  "flextable" , 
  "shiny" , 
  "shinyWidgets" , 
  "htmlwidgets" , 
  "tidyverse" , 
  "ggplot2" , 
  "archdata" , 
  "reshape2" , 
  "data.table" , 
  "dplyr" , 
  "ca" , 
  "viridis" , 
  "tm" , 
  "SnowballC" , 
  "wordcloud" , 
  "wordcloud2" , 
  "COVID19" , 
  "solrium" , 
  "shiny" , 
  "dplyr" , 
  "pool" , 
  "RPostgres" , 
  "DBI" , 
  "RSQLite" , 
  "RMariaDB" , 
  "data.table" , 
  "maptools" , 
  "mapview" , 
  "curl" , 
  "ini"
]

mylibs = []

for lib in libs:
  if lib not in mylibs:
    mylibs.append(lib)

print("################## START #######################################")

for required_package in mylibs:
  print('c-cran-' + required_package.lower() + ' ')
  #print('install.packages("' + required_package + '")')

print("################## R ###########################################")
  
for required_package in mylibs:
  #print('c-cran-' + required_package + ' ')
  print('install.packages("' + required_package + '")')
  
print("################## DONE ########################################")

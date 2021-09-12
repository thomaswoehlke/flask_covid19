all: build

prepare_linux:
	./etc/install_linux_depencencies.sh
	python -m venv venv

python_prepare:
	. venv/bin/activate
	pip install wget
	pip install pandas
	pip install scipy
	pip install matplotlib

prepare: prepare_linux python_prepare

lib01:
	Rscript etc/install_libraries_01.R

lib02:
	Rscript etc/install_libraries_02.R

lib03:
	Rscript etc/install_libraries_03.R

lib04:
	Rscript etc/install_libraries_04.R


run_ecdc:
	Rscript src/ecdc.R > src/ecdc.txt

run_owid:
	Rscript src/owid.R > src/owid.txt

run_rki:
	Rscript src/rki.R > src/rki.txt

run_vaccination:
	Rscript src/vaccination.R > src/vaccination.txt

run_who:
	Rscript src/who.R > src/who.txt


python_ecdc:
	python src/ecdc.py > src/ecdc.py.txt

python_owid:
	python src/owid.py > src/owid.py.txt

python_rki:
	python src/rki.py > src/rki.py.txt

python_vaccination:
	python src/vaccination.py > src/vaccination.py.txt

python_who:
	python src/who.py > src/who.py.txt


python_run: python_ecdc python_owid python_rki python_vaccination python_who


get_data:
	cp -r ~/github/flask_covid19/flask_covid19/data ~/github/flask_covid19_rclient

download:
	python src/data_download.py

run: run_ecdc run_owid run_rki run_vaccination run_who

target_pdf:
	mv src/*.pdf target/pdf/

target_docx:
	mv src/*.docx target/docx/

target_html:
	mv src/*.html target/html/

target_txt:
	mv src/*.txt target/txt/

python_start:
	Rscript src/start_python.R

target: target_txt

clean:
	rm -f Rplots.pdf

prepare: prepare_linux

lib: lib01 lib02 lib03 lib04

setup: prepare_linux lib

build: run python_prepare python_run target

TZ := 'Europe/Berlin'
HEUTE := `date '+%Y_%m_%d'`

# GIT_REMOTE_BRANCH := master
GIT_REMOTE_BRANCH := REFACTORING_2021_05_20_START
GIT_REMOTE := origin

WHO_URL := https://covid19.who.int/WHO-COVID-19-global-data.csv
WHO_FILE_BACKUP := WHO_backup.csv
WHO_FILE := WHO.csv
WHO_LOG := WHO.csv.log
WHO_SUBDIR := who

OWID_URL := https://covid.ourworldindata.org/data/owid-covid-data.csv
OWID_FILE_BACKUP := OWID_backup.csv
OWID_FILE := OWID.csv
OWID_LOG := OWID.csv.log
OWID_SUBDIR := owid

RKI_URL := https://www.arcgis.com/sharing/rest/content/items/f10774f1c63e40168479a1feb6c7ca74/data
RKI_FILE_BACKUP := RKI_backup.csv
RKI_FILE := RKI.csv
RKI_LOG := RKI.csv.log
RKI_SUBDIR := rki

RKI_VACCINATION_URL := https://impfdashboard.de/static/data/germany_vaccinations_timeseries_v2.tsv
RKI_VACCINATION_FILE_BACKUP := Vaccination_backup.tsv
RKI_VACCINATION_FILE := Vaccination.tsv
RKI_VACCINATION_LOG := Vaccination.tsv.log
RKI_VACCINATION_SUBDIR := vaccination

DIVI_URL := https://www.intensivregister.de/api/public/intensivregister
DIVI_FILE_BACKUP := DIVI_backup.json
DIVI_FILE := DIVI.json
DIVI_LOG := DIVI.json.log
DIVI_SUBDIR := divi

ECDC_URL := https://opendata.ecdc.europa.eu/covid19/casedistribution/csv/
ECDC_FILE_BACKUP := ECDC_backup.csv
ECDC_FILE := ECDC.csv
ECDC_LOG := ECDC.csv.log
ECDC_SUBDIR := ecdc

DB_HOST := localhost
DB_USER := flask_covid19
DB_PWD := 'flask_covid19pwd'
DB_DATABASE := flask_covid19
DB_DUMP_FILE := db/flask_covid19.sql
DB_DUMP_FILE_COMPRESSED = db/flask_covid19.sql.7z
DB_DUMP_FILE_ARCHIVE = db/flask_covid19_$(HEUTE).sql.7z

# DB_DUMP_OPT1 = --clean --if-exists --no-tablespaces --on-conflict-do-nothing --rows-per-insert=1000 --column-inserts
# DB_DUMP_OPT2 = --quote-all-identifiers --no-privileges

all: download db_dump vcs_commit


# -----------------------------------------------------------------------------------------------------
#
#   download
#
# -----------------------------------------------------------------------------------------------------

download: download_who download_owid download_rki download_rki_vaccination download_divi download_ecdc

download_owid:
	wget $(OWID_URL) -O $(OWID_FILE) -o $(OWID_LOG)
	touch $(OWID_SUBDIR)/$(OWID_FILE)
	cp -f $(OWID_SUBDIR)/$(OWID_FILE) $(OWID_SUBDIR)/$(OWID_FILE_BACKUP)
	mv -f $(OWID_FILE) $(OWID_SUBDIR)/$(OWID_FILE)
	mv -f $(OWID_LOG) $(OWID_SUBDIR)/$(OWID_LOG)

download_rki:
	wget $(RKI_URL) -O $(RKI_FILE) -o $(RKI_LOG)
	touch $(RKI_SUBDIR)/$(RKI_FILE)
	cp -f $(RKI_SUBDIR)/$(RKI_FILE) $(RKI_SUBDIR)/$(RKI_FILE_BACKUP)
	mv -f $(RKI_FILE) $(RKI_SUBDIR)/$(RKI_FILE)
	mv -f $(RKI_LOG) $(RKI_SUBDIR)/$(RKI_LOG)

download_who:
	wget $(WHO_URL) -O $(WHO_FILE) -o $(WHO_LOG)
	touch $(WHO_SUBDIR)/$(WHO_FILE)
	cp -f $(WHO_SUBDIR)/$(WHO_FILE) $(WHO_SUBDIR)/$(WHO_FILE_BACKUP)
	mv -f $(WHO_FILE) $(WHO_SUBDIR)/$(WHO_FILE)
	mv -f $(WHO_LOG) $(WHO_SUBDIR)/$(WHO_LOG)

download_rki_vaccination:
	wget $(RKI_VACCINATION_URL) -O $(RKI_VACCINATION_FILE) -o $(RKI_VACCINATION_LOG)
	touch $(RKI_VACCINATION_SUBDIR)/$(RKI_VACCINATION_FILE)
	cp -f $(RKI_VACCINATION_SUBDIR)/$(RKI_VACCINATION_FILE) $(RKI_VACCINATION_SUBDIR)/$(RKI_VACCINATION_FILE_BACKUP)
	mv -f $(RKI_VACCINATION_FILE) $(RKI_VACCINATION_SUBDIR)/$(RKI_VACCINATION_FILE)
	mv -f $(RKI_VACCINATION_LOG) $(RKI_VACCINATION_SUBDIR)/$(RKI_VACCINATION_LOG)

download_divi:
	wget $(DIVI_URL) -O $(DIVI_FILE) -o $(DIVI_LOG)
	touch $(DIVI_SUBDIR)/$(DIVI_FILE)
	cp -f $(DIVI_SUBDIR)/$(DIVI_FILE) $(DIVI_SUBDIR)/$(DIVI_FILE_BACKUP)
	mv -f $(DIVI_FILE) $(DIVI_SUBDIR)/$(DIVI_FILE)
	mv -f $(DIVI_LOG) $(DIVI_SUBDIR)/$(DIVI_LOG)

download_ecdc:
	wget $(ECDC_URL) -O $(ECDC_FILE) -o $(ECDC_LOG)
	touch $(ECDC_SUBDIR)/$(ECDC_FILE)
	cp -f $(ECDC_SUBDIR)/$(ECDC_FILE) $(ECDC_SUBDIR)/$(ECDC_FILE_BACKUP)
	mv -f $(ECDC_FILE) $(ECDC_SUBDIR)/$(ECDC_FILE)
	mv -f $(ECDC_LOG) $(ECDC_SUBDIR)/$(ECDC_LOG)


# -----------------------------------------------------------------------------------------------------
#
#   db
#
# -----------------------------------------------------------------------------------------------------

db: db_dump db_reimport

db_dump:
	mysqldump -u $(DB_USER) -h $(DB_HOST) $(DB_DATABASE) --password=$(DB_PWD) > $(DB_DUMP_FILE)
	7z a $(DB_DUMP_FILE_COMPRESSED) $(DB_DUMP_FILE)
	cp -f $(DB_DUMP_FILE_COMPRESSED) $(DB_DUMP_FILE_ARCHIVE)

db_reimport:
	7z a $(DB_DUMP_FILE_COMPRESSED)
	mysql -u $(DB_USER) -h $(DB_HOST) $(DB_DATABASE) --password=$(DB_PWD) < $(DB_DUMP_FILE)


# -----------------------------------------------------------------------------------------------------
#
#   vcs
#
# -----------------------------------------------------------------------------------------------------

vcs_setup:
	git config pull.rebase false
	git submodule init
	git submodule update
	git config --global diff.submodule log
	git submodule update --remote --merge

vcs_commit:
	git add .
	git commit -m "git_commit_and_push via make"

vcs_update:
	git submodule update
	git pull $(REMOTE) $(REMOTE_BRANCH)

vcs_store_to_remote:
	git push $(REMOTE) $(REMOTE_BRANCH)

vcs_push: vcs_setup vcs_commit vcs_store_to_remote vcs_load_from_remote

vcs_pull: vcs_setup vcs_checkout

vcs: vcs_push


# -----------------------------------------------------------------------------------------------------
#
#   stay human
#
# -----------------------------------------------------------------------------------------------------

love:
	@echo "not war!"

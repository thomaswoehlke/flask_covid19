#!/usr/bin/env python

from flask_covid19.data_all.all_config import BlueprintConfig
from flask_covid19.app_client.data_runner import Runner


cfg = BlueprintConfig.create_config_for_owid()
oo = Runner(cfg)
oo.prepare()
oo.daten_einlesen()

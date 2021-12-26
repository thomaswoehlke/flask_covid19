#!/usr/bin/env python
from project.app_web.cli.data_runner import Runner
from data_all.all_config import BlueprintConfig


cfg = BlueprintConfig.create_config_for_ecdc()
oo = Runner(cfg)
oo.prepare()
oo.daten_einlesen()

#!/web_user/bin/env python
from project.web.cli.data_runner import Runner
from project.data_all.all_config import BlueprintConfig


cfg = BlueprintConfig.create_config_for_owid()
oo = Runner(cfg)
oo.prepare()
oo.daten_einlesen()

#!/usr/bin/env python
import datetime as dt

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from flask_covid19.app_client.data_runner import Runner
from flask_covid19.data_all.all_config import BlueprintConfig


class WhoRunner(Runner):
    def run(self):
        plt.close("all")
        self.data["Cumulative_deaths"].plot()
        return self


cfg = BlueprintConfig.create_config_for_who()
oo = WhoRunner(cfg)
oo.prepare()
oo.daten_einlesen()
oo.run()

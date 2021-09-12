#!/usr/bin/env python

import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from flask_covid19.data_all.all_config import BlueprintConfig
from flask_covid19.app_client.data_runner import Runner


class WhoRunner(Runner):
    def run(self):
        plt.close("all")
        self.data['Cumulative_deaths'].plot()
        return self


cfg = BlueprintConfig.create_config_for_who()
oo = WhoRunner(cfg)
oo.prepare()
oo.daten_einlesen()
oo.run()

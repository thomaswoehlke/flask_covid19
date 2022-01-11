#!/web_user/bin/env python
import matplotlib.pyplot as plt
from project.app_web.cli.data_runner import Runner
from project.data_all.all_config import BlueprintConfig


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

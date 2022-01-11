#!/web_user/bin/env python
import matplotlib.pyplot as plt
from project.web.cli.data_runner import Runner
from project.data_all.services.all_config import BlueprintConfig


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

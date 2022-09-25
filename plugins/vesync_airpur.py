#!/usr/bin/python3

"""
Get AirQuality from Leviot Air purifier (tested with c300s) via vesync pyvesync
"""

import os
from munin import MuninPlugin
from pyvesync import VeSync


class HttpResponseTime(MuninPlugin):
    title = "Air Purifier - Air Quality"
    args = "--base 1000 -l 0"
    vlabel = "µg/m³"
    scale = False
    category = "other"
    warning = os.environ.get('air_quality_warn', "0:50")  # 1.5s
    critical = os.environ.get('air_quality_crit', "0:200")  # 2s
    user = os.environ.get('vesync_email')  # email of Vesync Account
    password = os.environ.get('vesync_password')  # password used for login
    tz = os.environ.get('vesync_tz')  # "Europe/Berlin"

    manager = VeSync(user, password, tz, False)

    fields = (
        ('fan_speed', dict(
            label="FanSpeed",
            type="GAUGE",
            draw="AREA",
            min="1",
            max="4",
            info="FanSpeed",
        )),
        ('filter_life', dict(
            label="Filter Life Remaining",
            type="GAUGE",
            draw="AREA",
            min="-1",
            max="101",
            info="Lifetime in %",
        )),
        ('air_quality', dict(
            label="AirQuality",
            type="GAUGE",
            draw="LINE2",
            min="0",
            max="999",
            info="AirQuality in µg/m³",
        )),
    )

    def execute(self):
        toaster = self.manager
        toaster.login()
        toaster.update()

        result = {"fan_speed": None, "filter_life": None, "air_quality": None}

        fan = toaster.fans[0]

        """
        print(manager.fans[0].details["air_quality_value"])
        print(manager.fans[0].details["filter_life"])
        print(manager.fans[0].extension["fanSpeedLevel"])
        """

        result["air_quality"] = fan.details["air_quality_value"]
        result["fan_speed"] = fan.extension["fanSpeedLevel"]
        result["filter_life"] = fan.details["filter_life"]

        return dict(
            air_quality=result["air_quality"],
            filter_life=result["filter_life"],
            fan_speed=result["fan_speed"]
        )


"""
    @staticmethod
    def read_file(log_path):
        result = {"fan_speed": None, "filter_life": None, "air_quality": None}
        if os.path.exists(log_path):
            with open(log_path, 'r') as f:
                log_lines = []
                create_lines = []
                config_lines = []
                for line in f:
                    if "/createuser/" in line:
                        create_lines.append(line)
                    if "/config/" in line:
                        config_lines.append(line)
                    if "/log/" in line:
                        log_lines.append(line)
                # calculate duration
                create_size = len(create_lines)
                if create_size > 0:
                    cr_line = create_lines[create_size - 1]
                    cr_s = get_duration_from_line(cr_line)
                    result["create"] = cr_s
                conf_size = len(config_lines)
                if conf_size > 0:
                    co_line = config_lines[conf_size - 1]
                    co_s = get_duration_from_line(co_line)
                    result["config"] = co_s
                log_size = len(log_lines)
                if log_size > 0:
                    l_line = log_lines[log_size - 1]
                    l_s = get_duration_from_line(l_line)
                    result["log"] = l_s
        else:
            return {}
        return result
"""
if __name__ == "__main__":
    HttpResponseTime().run()

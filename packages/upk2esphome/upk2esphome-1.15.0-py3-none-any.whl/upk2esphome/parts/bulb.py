#  Copyright (c) Kuba Szczodrzyński 2023-4-21.

from upk2esphome.config import ConfigData
from upk2esphome.generator import invert
from upk2esphome.opts import Opts
from upk2esphome.result import YamlResult

COLORS_STD = ["red", "green", "blue", "cold", "warm"]
COLORS_ALL = [*COLORS_STD, "brightness", "temperature"]
EXTRAS_CW = {
    "cold_white_color_temperature": "6500 K",
    "warm_white_color_temperature": "2700 K",
}
EXTRAS_RGBCW = {
    "color_interlock": True,
    **EXTRAS_CW,
}

# { found_colors: (esphome_platform, {color_translation}, {extra_opts}) }
COLOR_PLATFORMS = {
    # Red, Green, Blue
    "rgb": ("rgb", {}, {}),
    # Red, Green, Blue, Warm
    "rgbw": ("rgbw", {"warm": "white"}, {}),
    # Red, Green, Blue, Cold
    "rgbc": ("rgbw", {"cold": "white"}, {}),
    # Red, Green, Blue, Cold, Warm
    "rgbcw": (
        "rgbww",
        {"cold": "cold_white", "warm": "warm_white"},
        EXTRAS_RGBCW,
    ),
    # Red, Green, Blue, Brightness, Temperature
    "rgbbt": (
        "rgbct",
        {"brightness": "white_brightness", "temperature": "color_temperature"},
        EXTRAS_RGBCW,
    ),
    # Cold, Warm
    "cw": (
        "cwww",
        {"cold": "cold_white", "warm": "warm_white"},
        EXTRAS_CW,
    ),
    # Brightness, Temperature
    "bt": (
        "color_temperature",
        {"temperature": "color_temperature"},
        EXTRAS_CW,
    ),
    # Cold
    "c": ("monochromatic", {"cold": "output"}, {}),
    # Warm
    "w": ("monochromatic", {"warm": "output"}, {}),
}

# { (cmod, cwtype): esphome_platform }
CMOD_PLATFORM = {
    ("rgbcw", 0): "rgbww",
    ("rgbcw", 1): "rgbct",
    ("rgb", 0): "rgb",
    ("cw", 0): "cwww",
    ("cw", 1): "color_temperature",
    ("c", 0): "monochromatic",
    ("rgbc", 0): "rgbw",
}


def get_platform(found: set[str]):
    key = sorted(c[0] for c in found)
    for name, platform in COLOR_PLATFORMS.items():
        if sorted(name) == key:
            return platform
    return None


def gen_pwm(yr: YamlResult, config: dict) -> set[str]:
    found = set()
    is_ct = config.get("cwtype", 0) == 1
    for color in COLORS_STD:
        pin = config.get(f"{color[0]}_pin", None)
        inv = config.get(f"{color[0]}_lv", None) == 0
        if pin is None:
            continue
        if is_ct and color == "cold":
            color = "brightness"
        elif is_ct and color == "warm":
            color = "temperature"
        found.add(color)

        yr.log(f" - color {color}: pin P{pin}, inverted {inv}")
        output = {
            "platform": "libretiny_pwm",
            "id": f"output_{color}",
            "pin": f"P{pin}",
        }
        invert(output, inv)
        yr.output(output)
    return found


def gen_i2c_sm2235(yr: YamlResult, config: dict):
    scl = config.get("iicscl", None)
    sda = config.get("iicsda", None)
    if not scl or not sda:
        yr.warn("I2C pins not found")
        return None

    yr.data["sm2235"] = {
        "clock_pin": f"P{scl}",
        "data_pin": f"P{sda}",
    }

    cur_color = config.get("2235ccur", None)
    cur_white = config.get("2235wcur", None)
    if cur_color is not None:
        yr.data["sm2235"]["max_power_color_channels"] = cur_color
        yr.log(f" - color channels power: {cur_color}")
    if cur_white is not None:
        yr.data["sm2235"]["max_power_white_channels"] = cur_white
        yr.log(f" - white channels power: {cur_white}")

    found = set()
    for color in COLORS_STD:
        channel = f"iic{color[0]}"
        if channel not in config:
            continue
        found.add(color)

        yr.log(f" - color {color}: channel {config[channel]}")
        output = {
            "platform": "sm2235",
            "id": f"output_{color}",
            "channel": config[channel],
        }
        yr.output(output)

    return found


def gen_i2c_sm2135eh(yr: YamlResult, config: dict):
    scl = config.get("iicscl", None)
    sda = config.get("iicsda", None)
    if not scl or not sda:
        yr.warn("I2C pins not found")
        return None

    yr.data["sm2135"] = {
        "clock_pin": f"P{scl}",
        "data_pin": f"P{sda}",
    }

    cur_color = config.get("ehccur", config.get("iicccur", None))
    cur_white = config.get("ehwcur", config.get("iicwcur", None))
    if cur_color is not None:
        cur_color = 10 + cur_color * 5
    else:
        cur_color = config.get("campere", None)
    if cur_white is not None:
        cur_white = 10 + cur_white * 5
    else:
        cur_white = config.get("wampere", None)

    if cur_color is not None:
        yr.data["sm2135"]["rgb_current"] = f"{cur_color}mA"
        yr.log(f" - color channels current: {cur_color} mA")
    if cur_white is not None:
        yr.data["sm2135"]["cw_current"] = f"{cur_white}mA"
        yr.log(f" - white channels current: {cur_white} mA")

    found = set()
    for color in COLORS_STD:
        channel = f"iic{color[0]}"
        if channel not in config:
            continue
        found.add(color)

        yr.log(f" - color {color}: channel {config[channel]}")
        output = {
            "platform": "sm2135",
            "id": f"output_{color}",
            "channel": config[channel],
        }
        yr.output(output)

    return found


def gen_i2c_bp5758d(yr: YamlResult, config: dict):
    scl = config.get("iicscl", None)
    sda = config.get("iicsda", None)
    if not scl or not sda:
        yr.warn("I2C pins not found")
        return None

    yr.data["bp5758d"] = {
        "clock_pin": f"P{scl}",
        "data_pin": f"P{sda}",
    }

    cur_rgb = config.get("drgbcur", None)
    cur_cold = config.get("dccur", None)
    cur_warm = config.get("dwcur", None)

    found = set()
    for color in COLORS_STD:
        channel = f"iic{color[0]}"
        if channel not in config:
            continue
        found.add(color)

        current = (
            cur_cold if color == "cold" else cur_warm if color == "warm" else cur_rgb
        )

        yr.log(f" - color {color}: channel {config[channel]}, current {current} mA")
        output = {
            "platform": "bp5758d",
            "id": f"output_{color}",
            "channel": config[channel] + 1,
        }
        if current:
            output["current"] = current
        yr.output(output)

    return found


def gen_i2c_bp1658cj(yr: YamlResult, config: dict):
    scl = config.get("iicscl", None)
    sda = config.get("iicsda", None)
    if not scl or not sda:
        yr.warn("I2C pins not found")
        return None

    yr.data["bp1658cj"] = {
        "clock_pin": f"P{scl}",
        "data_pin": f"P{sda}",
    }

    cur_color = config.get("cjccur", None)
    cur_white = config.get("cjwcur", None)
    if cur_color is not None:
        yr.data["bp1658cj"]["max_power_color_channels"] = cur_color
        yr.log(f" - color channels power: {cur_color}")
    if cur_white is not None:
        yr.data["bp1658cj"]["max_power_white_channels"] = cur_white
        yr.log(f" - white channels power: {cur_white}")

    found = set()
    for color in COLORS_STD:
        channel = f"iic{color[0]}"
        if channel not in config:
            continue
        found.add(color)

        yr.log(f" - color {color}: channel {config[channel]}")
        output = {
            "platform": "bp1658cj",
            "id": f"output_{color}",
            "channel": config[channel],
        }
        yr.output(output)

    return found


def generate(yr: YamlResult, config: ConfigData, opts: Opts):
    config = config.upk or {}
    # remove duplicate channels
    if config.get("iicc", None) == config.get("iicw", None):
        config.pop("iicw", None)

    chips = {
        "PWM": (gen_pwm, ["r_pin", "g_pin", "b_pin", "c_pin", "w_pin"]),
        "SM2235": (gen_i2c_sm2235, ["2235ccur", "2235wcur"]),
        "SM2135EH": (
            gen_i2c_sm2135eh,
            ["ehccur", "ehwcur", "wampere", "campere", "iicccur", "iicwcur"],
        ),
        "BP5758D": (gen_i2c_bp5758d, ["dccur", "dwcur", "drgbcur"]),
        "BP1658CJ": (gen_i2c_bp1658cj, ["cjccur", "cjwcur"]),
    }
    for name, (func, keys) in chips.items():
        if not any(key in config for key in keys):
            continue
        yr.log(f"{name} bulb")
        yr.found = True
        # find colors
        found = func(yr, config)
        if not found:
            continue
        # find platform for colors
        platform = get_platform(found)
        if not platform:
            yr.warn(f"Unknown light platform for colors: {found}")
            continue
        name, mapping, opts = platform
        # build light component
        light = {
            "platform": name,
            "id": f"light_{name}",
            "name": "Light",
            **opts,
        }
        # add channels
        for color in COLORS_ALL:
            if color not in found:
                continue
            key = mapping.get(color, color)
            light[key] = f"output_{color}"
        # add light component
        yr.light(light)
        # check cmod matching
        cmod = config.get("cmod", None)
        cwtype = config.get("cwtype", 0)
        if (cmod, cwtype) in CMOD_PLATFORM:
            if CMOD_PLATFORM[cmod, cwtype] != name:
                yr.warn(
                    f"Module cmod:{cmod}/cwtype:{cwtype} doesn't match platform {name}"
                )

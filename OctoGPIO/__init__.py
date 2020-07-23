# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import octoprint.plugin
import RPi.GPIO as GPIO

class OctoGPIOPlugin(
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.SimpleApiPlugin):

    def __init__(self):
        # try:
            # global GPIO
            # import RPi.GPIO as GPIO
            # self._hasGPIO = True
        # except (ImportError, RuntimeError):
            # self._hasGPIO = False
        self._hasGPIO = True

        if (self._hasGPIO):
            GPIO.setmode(GPIO.BCM)

    def get_settings_defaults(self):
        return dict(
            url = "http://thorlucas.me",
            switches = [
                dict(
                    name = "Lights",
                    pin = 0,
                ),
                dict(
                    name = "Printer",
                    pin = 3,
                )
            ]
        )

    def get_api_commands(self):
        return dict(
            switch = ["pin"]
        )

    def get_assets(self):
        return dict(
            js = ["js/octogpio_settings.js", "js/octogpio_sidebar.js"]
        )

    def get_template_configs(self):
        return [
            dict(type="navbar", custom_bindings=True),
            dict(type="settings", custom_bindings=True)
        ]

    def on_after_startup(self):
        if not self._hasGPIO:
            self._logger.warning("RPi.GPIO not installed!")

        self.configure_pins([int(switch["pin"]) for switch in self._settings.get(["switches"])])

    def on_settings_save(self, data):
        old_pins = [int(switch["pin"]) for switch in self._settings.get(["switches"])]
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
        new_pins = [int(switch["pin"]) for switch in self._settings.get(["switches"])]

        cleanup_pins = []
        for pin in old_pins:
            if pin not in new_pins:
                cleanup_pins.append(pin)

        configure_pins = []
        for pin in new_pins:
            if pin not in old_pins:
                configure_pins.append(pin)

        self.configure_pins(configure_pins, cleanup_pins = cleanup_pins)

    def configure_pins(self, configure_pins, cleanup_pins = []):
        for pin in cleanup_pins:
            self._logger.info("cleaning up pin: %s", pin)
            if (self._hasGPIO):
                GPIO.cleanup(pin)

        for pin in configure_pins:
            self._logger.info("configuring pin: %s", pin)
            if (self._hasGPIO):
                GPIO.setup(pin, GPIO.OUT)

    def on_api_command(self, command, data):
        if command == "switch":
            self.switch(int(data["pin"]))

    def switch(self, pin):
        self._logger.info("Switching %s", pin)
        if (self._hasGPIO):
            state = GPIO.input(pin)
            GPIO.output(pin, GPIO.LOW if state == GPIO.HIGH else GPIO.HIGH)

__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_implementation__ = OctoGPIOPlugin()

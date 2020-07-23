/*
 * View model for OctoGPIO
 *
 * Author: Thor Lucas Correia
 * License: AGPLv3
 */
$(function() {
    function OctogpioSettingsViewModel(parameters) {
        var self = this;
		self.settings = parameters[0];

		self.addSwitch = function () {
			self.settings.settings.plugins.octogpio.switches.push({
				name: "Switch",
				pin: 0,
			});
		}

		self.removeSwitch = function (theSwitch) {
			self.settings.settings.plugins.octogpio.switches.remove(theSwitch);
		}
    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: OctogpioSettingsViewModel,
        dependencies: [ "settingsViewModel" ],
        // Elements to bind to, e.g. #settings_plugin_OctoGPIO, #tab_plugin_OctoGPIO, ...
        elements: [ "#settings_plugin_octogpio" ]
    });
});

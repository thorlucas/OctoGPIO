/*
 * View model for OctoGPIO
 *
 * Author: Thor Lucas Correia
 * License: AGPLv3
 */
$(function() {
    function OctogpioSidebarViewModel(parameters) {
        var self = this;
		self.settings = parameters[0];

		self.switch = function () {
			const pin = this.pin(); 
			console.log(pin);

			$.ajax({
				url: API_BASEURL + "plugin/octogpio",
				type: "POST",
				dataType: "json",
				data: JSON.stringify({
					command: "switch",
					pin: pin
				}),
				contentType: "application/json; charset=UTF-8"
			});
		}
    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: OctogpioSidebarViewModel,
        dependencies: [ "settingsViewModel" ],
        // Elements to bind to, e.g. #settings_plugin_OctoGPIO, #tab_plugin_OctoGPIO, ...
        elements: [ "#sidebar_plugin_octogpio" ]
    });
});

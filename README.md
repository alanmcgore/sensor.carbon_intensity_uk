# Carbon Intensity UK sensor

[![GitHub Release][releases-shield]][releases]

[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

_Component to integrate with [Carbon Intensity UK][carbon_intensity_uk]._

**This component will set up the following platforms.**

Platform | Description
-- | --
`sensor` | Show info from Carbon Intensity UK API.

The sensor retrieves information using [Carbon Intensity UK API library (forked)](https://github.com/alanmcgore/carbonintensity) - It adds in additional data based on [work by jfparis in his fork](https://github.com/jfparis/sensor.carbon_intensity_uk) as well as a percentage of the grid in low carbon energy and potentially additional entities. 

![alt Sensor attributes][attributesimg]

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `carbon_intensity_uk`.
4. Download _all_ the files from the `custom_components/carbon_intensity_uk/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Carbon Intensity UK"

Using your HA configuration directory (folder) as a starting point you should now also have this:

```text
custom_components/carbon_intensity_uk/.translations/en.json
custom_components/carbon_intensity_uk/.translations/nb.json
custom_components/carbon_intensity_uk/.translations/sensor.nb.json
custom_components/carbon_intensity_uk/__init__.py
custom_components/carbon_intensity_uk/binary_sensor.py
custom_components/carbon_intensity_uk/config_flow.py
custom_components/carbon_intensity_uk/const.py
custom_components/carbon_intensity_uk/manifest.json
custom_components/carbon_intensity_uk/sensor.py
custom_components/carbon_intensity_uk/switch.py
```

## Configuration is done in the UI

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[carbon_intensity_uk]: https://github.com/jscruz/sensor.carbon_intensity_uk
[commits-shield]: https://img.shields.io/github/commit-activity/y/alanmcgore/sensor.carbon_intensity_uk?style=for-the-badge
[commits]: https://github.com/alanmcgore/sensor.carbon_intensity_uk/commits/master
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[attributesimg]: attributes.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/alanmcgore/sensor.carbon_intensity_uk.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Alan%20Gore%20%40alanmcgore-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/alanmcgore/sensor.carbon_intensity_uk.svg?style=for-the-badge
[releases]: https://github.com/alanmcgore/sensor.carbon_intensity_uk/releases

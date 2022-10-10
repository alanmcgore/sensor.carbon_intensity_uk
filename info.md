[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]

_Component to integrate with [Carbon Intensity UK][carbon_intensity_uk]._

Platform | Description
-- | --
`service` | Provides sensors with info from Carbon Intensity UK API.

Available sensors are:
Sensor | Description
-- | --
`Local CO2 intensity forecast` | This has attributes for the next 48 hours co2 intensity forecast which can be used for forecasting and optimal window work. 
`Local Grid CO2 Itensity` | Current local grid co2 intensity in gCO2eq/kwh
`Local Grid CO2 Levels` | String identifying current CO2 intensity, e.g. 'Low'
`Local Grid Fossil Fuel %` | Percentage of local grid electricity from Gas, Coal, Oil
`Local Grid Low Carbon %` | Percentage of local grid electricity from Hydro, Solar, Wind, Biomass
`Local Optimal Window From` | Time when the next 4h optimal window for low carbon runs from
`Local Optimal Window To` | End time of the 4h optimal window. 

The sensor retrieves information using [Carbon Intensity UK API library (forked)](https://github.com/alanmcgore/carbonintensity) - It adds in additional data based on [work by jfparis in his fork](https://github.com/jfparis/sensor.carbon_intensity_uk) as well as a percentage of the grid in low carbon energy and potentially additional entities. 


{% if not installed %}
## Installation

1. Click install.
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Carbon Intensity UK forked".

{% endif %}


## Configuration is done in the UI

<!---->

***

[carbon_intensity_uk]: https://github.com/alanmcgore/sensor.carbon_intensity_uk
[commits-shield]: https://img.shields.io/github/commit-activity/y/alanmcgore/sensor.carbon_intensity_uk?style=for-the-badge
[commits]: https://github.com/alanmcgore/sensor.carbon_intensity_uk/commits/master
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[attributesimg]: attributes.png
[license-shield]: https://img.shields.io/github/license/alanmcgore/sensor.carbon_intensity_uk.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Alan%20Gore%20%40alanmcgore-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/alanmcgore/sensor.carbon_intensity_uk.svg?style=for-the-badge
[releases]: https://github.com/alanmcgore/sensor.carbon_intensity_uk/releases

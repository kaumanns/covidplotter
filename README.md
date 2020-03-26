# covidplotter

This tool allows easy plotting of scaled transformations of COVID-19 time series data provided by CSSE at John Hopkins University (<https://github.com/CSSEGISandData/COVID-19>).

The tool checks a local clone of the time series data for updates and generates new plots, if necessary.

Scaling factors are defined per country in separate JSON configuration files.
The currently provided scaling factors (population sizes and densities) are taken from English Wikipedia.

## Tested requirements

- OS: Raspbian Buster
- GNU bash 5.0.3(1)
- GNU Make 4.2.1
- Git 2.20.1
- Python 3.7.3
    - matplotlib 3

## Installation

```
git clone <repository url>
```

## Usage

```
make
```

Notes:

- In order to change the countries and/or scaling factors, modify the JSON configurations in `etc/`.
- If new configurations are provided, modify `Makefile` accordingly. Run `src/covidplotter.py` for more options.

## Plots

### Confirmed

![](out/time_series_covid19_confirmed_global.png)
![](out/time_series_covid19_confirmed_global.@population.png)
![](out/time_series_covid19_confirmed_global.@density.png)

---

Natural Logarithm:

![](out/time_series_covid19_confirmed_global.@log.png)
![](out/time_series_covid19_confirmed_global.@population@log.png)
![](out/time_series_covid19_confirmed_global.@density@log.png)

### Deaths

![](out/time_series_covid19_deaths_global.png)
![](out/time_series_covid19_deaths_global.@population.png)
![](out/time_series_covid19_deaths_global.@density.png)

---

Natural Logarithm:

![](out/time_series_covid19_deaths_global.@log.png)
![](out/time_series_covid19_deaths_global.@population@log.png)
![](out/time_series_covid19_deaths_global.@density@log.png)

### Recovered

![](out/time_series_covid19_recovered_global.png)
![](out/time_series_covid19_recovered_global.@population.png)
![](out/time_series_covid19_recovered_global.@density.png)

---

Natural Logarithm:

![](out/time_series_covid19_recovered_global.@log.png)
![](out/time_series_covid19_recovered_global.@population@log.png)
![](out/time_series_covid19_recovered_global.@density@log.png)

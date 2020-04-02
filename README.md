# covidplotter

This tool allows easy plotting of scaled transformations of COVID-19 time series data provided by CSSE at John Hopkins University (<https://github.com/CSSEGISandData/COVID-19>).

The tool checks a local clone of the time series data for updates and generates new plots, if necessary.

Scaling factors are defined per country in separate JSON configuration files.
The currently provided scaling factors are taken from English Wikipedia.

## Plots

- [Confirmed cases](./confirmed/)
- [Deaths](./deaths/)
- [Recovered](./recovered/)

## How to recreate the plots

### Tested requirements

- OS: Raspbian Buster
- GNU bash 5.0.3(1)
- GNU Make 4.2.1
- Git 2.20.1
- Python 3.7.3
    - matplotlib 3

### Installation

```
git clone <repository url>
cd <repository url>
make dependencies
```

### Usage

Plot, optionally using 4 threads via `-j` option:

```
make -j 4
```

Notes:

- In order to change the countries and/or scaling factors, modify the JSON configuration in `etc/scale_map.json`.
- If new configurations are provided, modify `Makefile` accordingly. Run `src/covidplotter.py` for more options.

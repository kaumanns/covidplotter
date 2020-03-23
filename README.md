# covidplotter

Downloads current COVID-19 time series data (for deaths) provided by CSSE at John Hopkins University (<https://github.com/CSSEGISandData/COVID-19>) and plots a subset of them as graphs, as specified by JSON configuration files containing countries and scaling denominators.

Denominators (population sizes and densities) are taken from Wikipedia.

## Tested requirements

- OS: Raspbian Buster
- GNU bash 5.0.3(1)
- GNU Make 4.2.1
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

- In order to update to the most current time series data, delete the CSV file and run again.
- In order to change the countries and/or scaling denominators, modify the JSON configurations in `etc/`.

## Plots

![Time Series COVID-19 deaths (Germany, Austria, US)](time_series_19-covid-Deaths.png)

![Time Series COVID-19 deaths (Germany, Austria, US) scaled by population](time_series_19-covid-Deaths@population.png)

![Time Series COVID-19 deaths (Germany, Austria, US) scaled by density](time_series_19-covid-Deaths@density.png)

# Joachim's brew tools

This repository contains a number of tools that help me in my brewing and documenting workflow. 

## `brewxml2md`

This tool parses a [BeerXML Recipe](http://www.beerxml.com/beerxml.htm) and converts it to markdown. This can then be imported into your note-taking software of choice.

### Syntax

     $ python brewxml2md.py <recipe-name>.xml

#### Options / parameters

none

## `sg-temp`

Normally, gravity measuring tools are calibrated against a certain temperature. One rarely gets to that temperature prior to measuring, so a small correction should be made. This tool calculates the correction.

### Syntax

    $ python sg-temp.py <parameters>

#### Options / parameters

* `-h`: display a helpful message
* `-t`: measured temperature
* `-m`: measured gravity
* `-c`: override the calibration temperature. The default is 20 degrees celsius

## `abv`

Simple ABV calculator, shamelessly borrowed from https://www.brewersfriend.com/2011/06/16/alcohol-by-volume-calculator-updated/ . 

### Syntax

    $ python abv.py <OG> <SG>

#### Options / parameters

* `-h`: display a helpful message
* `<OG>`: Original Gravity. See below for details
* `<FG>`: Final Gravity. See below for details

#### Notes

The gravity values can be either entered as float values (e.g. 1.026) or integer values (e.g. 1026). Any other format will yield a warning message
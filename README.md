# Joachim's brew tools

This repository contains a number of tools that help me in my brewing and documenting workflow. 

## `brewxml2md`

This tool parses a [BeerXML Recipe](http://www.beerxml.com/beerxml.htm) and converts it to markdown. This can then be imported into your note-taking software of choice.

### Syntax

     $ python brewxml2md.py <recipe-name>.xml

#### Options / parameters

none

## `sg-temp`

Normally, SG measuring tools are calibrated against a certain temperature. One rarely gets to that temperature prior to measuring, so a small correction should be made. This tool calculates the correction.


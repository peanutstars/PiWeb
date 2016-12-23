#!/bin/bash

MCSS=main.css

sass --style expanded main.scss $MCSS
mv $MCSS  ../css/$MCSS

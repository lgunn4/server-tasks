#!/bin/bash

while getopts s:d: flag
do
    case "${flag}" in
        s) source=${OPTARG};;
        d) destination=${OPTARG};;
    esac
done

rsync -avzzp --delete $source $destination
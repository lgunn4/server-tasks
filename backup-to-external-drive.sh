#!/bin/bash

while getopts s:d: flag
do
    case "${flag}" in
        s) source=${OPTARG};;
        d) destination=${OPTARG};;
    esac
done

rsync -e ‘ssh -p 22’ -avzp $source $destination
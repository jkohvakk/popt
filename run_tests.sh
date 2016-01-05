#!/usr/bin/env bash

pybot --outputdir test test/source_of_test_xml.robot
py.test test


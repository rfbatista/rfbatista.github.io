#!/bin/bash
rm -rf ./public
hugo && firebase deploy

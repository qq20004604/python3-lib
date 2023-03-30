#!/bin/bash
# 跨平台打包的话，可能要特殊设置。例如mac上打包linux上用
go build -o search.so -buildmode=c-shared search.go
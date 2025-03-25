#!/bin/bash
#This scripts clones many test gwit sites locally to launch tests against.

remote=https://framagit.org/matograine/gwit-tests.git
target_dir=testing_remote # this is WET_TEST_REMOTE_DIR in tests

git clone $remote $target_dir
cd $target_dir
git checkout 'gwit-0xdfd9e079'
git checkout 'gwit-0x25274543'
git checkout 'gwit-0x080a6b32'
git checkout 'gwit-0x4f675edd'
git checkout 'gwit-0x6da3ef3a'
git checkout 'gwit-0x9610669b'
git checkout 'gwit-0x9918e43c'
git checkout 'gwit-0x3ff6107c'

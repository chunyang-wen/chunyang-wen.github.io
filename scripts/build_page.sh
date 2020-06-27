#!/bin/sh

if [ $1 == "init" ]
then
    gem install bundle
    bundle install
elif [ $1 == "serve" ]
then
    bundle exec jekyll serve
fi

#!/bin/bash

shopt -s expand_aliases

alias __ts="date +'%Y-%m-%d_%H:%M'"

alias __ddump="DEBUG=True  python manage.py dumpdata --indent=2"

# if you get some "Unable to configure handler 'file'" error with this one,
# be sure to run the restart.sh script first, to clear out old logs
alias __pdump="python manage.py dumpdata --indent=2"

# ------------------------------------------------------------------------------
# DEV
# ------------------------------------------------------------------------------

__ddump vto_core.TZWikiSlug vto_core.TimeZone vto_core.TZAbbreviation \
    vto_core.DemoExchange vto_core.DemoTestTimestamp \
    > data/tz-DEV-$(__ts).json

__ddump vto_core.User > data/usr-DEV-$(__ts).json

# ------------------------------------------------------------------------------
# PROD
# ------------------------------------------------------------------------------

__pdump vto_core.TZWikiSlug vto_core.TimeZone vto_core.TZAbbreviation \
    vto_core.DemoExchange vto_core.DemoTestTimestamp \
    > data/tz-$(__ts).json

__pdump vto_core.User > data/usr-$(__ts).json

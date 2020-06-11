#!/usr/bin/env bash
# Usage: at the root dir >> bash visya/format.sh
yapf --in-place --recursive -p --verbose \
--style visya/.style.yapf .
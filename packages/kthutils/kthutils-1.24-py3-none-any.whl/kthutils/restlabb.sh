#!/bin/bash

YEAR=$(date +%y)
MONTH=$(date +%m)
if [[ $MONTH -lt 7 ]]; then
  AC_YEAR="$((YEAR-1))/${YEAR}"
else
  AC_YEAR="${YEAR}/$((YEAR+1))"
fi
kthutils forms next restlabb${AC_YEAR} \
| grep -E "(Bosk|DD1310.*(CMAST|[CS]ITEH?)|DD131[57].*CINEK)" \
| kthutils forms rewriter rewrite restlabb

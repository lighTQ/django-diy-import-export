#!/bin/bash
pyi-makespec  -F -n echoApp  --add-data "static_root:static" --add-data "templates:templates" manage.py



#2  pyinstaller --noconfirm --clean echoApp.spec

#3 ./echoApp runserver localhost:8000 --noreload


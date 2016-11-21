#!/bin/bash
/etc/init.d/postgresql start
/etc/init.d/nginx start
/etc/init.d/supervisor start
/bin/bash
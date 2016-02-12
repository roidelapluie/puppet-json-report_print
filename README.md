# Puppet JSON Reports print

I really like [puppet-reportprint](https://github.com/ripienaar/puppet-reportprint/blob/master/report_print.rb).
However it expects yaml file.

I needed to see the logs of reports stored in puppetdb. And it can not dump them
as yaml easily.

Workflow to use this software:

```
puppetdb export -p 8080 --outfile backup.tar.gz
tar xvf backup.tar.gz
./report_print_json.py puppetdb-bak/reports/*.json
```

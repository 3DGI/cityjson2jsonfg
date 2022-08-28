"""Command Line Interface (cli.py)
Copyright 2022 Balázs Dukai

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import warnings
import click
from cjio import errors, cityjson, cjio

cityjson.CITYJSON_VERSIONS_SUPPORTED = ['1.1',]

from cityjson2jsonfg import convert




@click.command()
@click.version_option()
@click.argument("infile", type=click.File("r"))
@click.argument("outfile", type=click.File("w"))
@click.option('--ignore_duplicate_keys', is_flag=True, help='Load a CityJSON file even if some City Objects have the same IDs (technically invalid file).')
def main(infile, outfile, ignore_duplicate_keys):
    """A command line tool for converting CityJSON files to JSON-FG format.

        INFILE – Path to a CityJSON file\n
        OUTFILE – Path to the JSON-FG file to write
    """
    click.echo("Parsing %s" % infile.name)

    try:
        cm = cityjson.reader(file=infile, ignore_duplicate_keys=ignore_duplicate_keys)
        try:
            with warnings.catch_warnings(record=True) as w:
                cm.check_version()
                cjio._print_cmd(w)
        except errors.CJInvalidVersion as e:
            raise click.ClickException(e.msg)
    except ValueError as e:
        raise click.ClickException('%s: "%s".' % (e, infile))
    except IOError as e:
        raise click.ClickException('Invalid file: "%s".\n%s' % (infile, e))

    click.echo("Writing to %s" % outfile.name)
    outfile.write(convert.to_jsonfg(cm).getvalue())

    return True

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
import click


@click.command()
@click.version_option()
@click.argument("input", type=click.File("r"))
@click.argument("output", type=click.File("w"))
def main():
    """A command line tool for converting CityJSON files to JSON-FG format.

        INPUT – Path to a CityJSON file\n
        OUTPUT – Path to the JSON-FG file to write
    """
    print("Hello world")
    return True

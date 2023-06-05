#!/usr/bin/env python3

"""Parse `dart analyze` output and convert to SARIF format."""

import argparse
import json
import logging
import sys


LOG = logging.getLogger(__name__)


class DartAnalyzeIssue:
    """Represents a single issue from `dart analyze`."""

    def __init__(self, line: str) -> None:
        """Parse a line of `dart analyze` output."""
        parts = line.strip().split(' - ', maxsplit=3)
        if len(parts) != 4:
            raise ValueError("Not a valid dart analyze line")
        self.severity, location, self.message, self.rule = parts
        self.location = Location(location)

    def to_sarif(self) -> dict:
        """Convert the issue to SARIF format."""
        return {
            'level': self.severity,
            'locations': [
                self.location.to_sarif()
            ],
            'message': {
                'text': self.message
            },
            'ruleId': self.rule
        }


class Location:
    """A path, line and column."""
    
    def __init__(self, location: str) -> None:
        """Initialize the location."""
        parts = location.split(':')
        
        self.column = int(parts.pop())
        self.line = int(parts.pop())
        self.path = ':'.join(parts)

    def to_sarif(self) -> dict:
        """Convert the location to SARIF format."""
        return {
            'physicalLocation': {
                'artifactLocation': {
                    'uri': self.path
                },
                'region': {
                    'startLine': self.line,
                    'startColumn': self.column
                }
            }
        }


def parse_args(parser: argparse.ArgumentParser) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Convert dart analyze output to SARIF format')
    parser.add_argument('--input-file', required=True, help='dart analyze output file')
    parser.add_argument('--output-file', default=None, required=False, help='SARIF output file')
    parser.add_argument('--debug', action='store_true', help='enable debug logging')
    return parser.parse_args()


def main() -> None:
    """Main function."""
    parser = argparse.ArgumentParser(description=__doc__)
    args = parse_args(parser)

    logging.basicConfig(level=logging.INFO)

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    results: list[dict] = []
    rules: set[str] = set()

    # read in the dart analyze output, line by line
    with open(args.input_file, 'r') as f:
        for line in f.readlines():
            try:
                data = DartAnalyzeIssue(line)
            except ValueError:
                LOG.debug("Skipping invalid line: %s", line)
                continue
            results.append(data.to_sarif())
            rules.add(data.rule)

    # write out the results in SARIF format
    with open(args.output_file, 'w') if args.output_file is not None else sys.stdout as f:
        json.dump({
            'version': '2.1.0',
            'runs': [
                {
                    'tool': {
                        'driver': {
                            'name': 'dart analyze',
                            'informationUri': 'https://dart.dev/tools/dart-analyze',
                            'rules': [
                                {
                                    'id': rule,
                                    'name': rule
                                }
                                for rule in rules
                            ]
                        }
                    },
                    'results': results
                }
            ]
        }, f, indent=2)


if __name__ == "__main__":
    main()

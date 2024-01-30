# dart-analyzer-sarif

This Action converts Dart Analyzer (and Flutter Analyzer) output to SARIF format.

Run `dart analyze` or `flutter analyze`, then give their output to this Action as input.

## Usage

```yaml
- name: Dart Analyze to SARIF
  uses: advanced-security/dart-analyzer-sarif@main
    with:
        input: dart_analyze.txt
        output: dart_analyze.sarif
```

## Inputs

* `input` - The path to the input file, containing the output of `dart analyze` or `flutter analyze`
* `output` - The path to the output file, containing the SARIF output. Default: `dart_analyze.sarif`

## Full sample workflow

```yaml
# This workflow uses actions that are not certified by GitHub.
# They are provided by a third-party and are governed by
# separate terms of service, privacy policy, and support
# documentation.
name: Dart Analyzer to SARIF
on:
  push:
    branches: [ $default-branch, $protected-branches ]
  pull_request:
    # The branches below must be a subset of the branches above
    branches: [ $default-branch ]
  schedule:
    - cron: $cron-weekly
jobs:
  dart-analyzer:
    permissions:
      contents: read # for actions/checkout to fetch code
      security-events: write # for github/codeql-action/upload-sarif to upload SARIF results
      actions: read # only required for a private repository by github/codeql-action/upload-sarif to get the Action run status
    runs-on: ubuntu-latest
    name: Dart Analyzer to SARIF
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - uses: dart-lang/setup-dart@v1
      - name: Dart Analyze
        run: dart analyze > dart_analyze.txt || true
      - name: Dart Analyze to SARIF
        uses: advanced-security/dart-analyzer-sarif@main
        with:
          input: dart_analyze.txt
          output: dart_analyze.sarif
      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: dart_analyze.sarif
```

## Requirements

* Python 3.7 or later
or
* GitHub Actions runner

## License

This project is licensed under the terms of the MIT open source license. Please refer to the [LICENSE](LICENSE) for the full terms.

## Maintainers

See [CODEOWNERS](CODEOWNERS) for the list of maintainers.

## Support

See the [SUPPORT](SUPPORT.md) file.

## Background

See the [CHANGELOG](CHANGELOG.md), [CONTRIBUTING](CONTRIBUTING.md), [SECURITY](SECURITY.md), [SUPPORT](SUPPORT.md), [CODE OF CONDUCT](CODE_OF_CONDUCT.md) and [PRIVACY](PRIVACY.md) files for more information.

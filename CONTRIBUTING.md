# How to contribute

## New Software Quality Indicator

If you want to create a new quality indicator, please open a pull request or an issue.

The software quality indicators in this repository follow the schema described by [https://w3id.org/everse/rsqi](https://w3id.org/everse/rsqi).

To provide a new software quality indicator, please submit a pull-request with your indicator described in json format following the EVERSE RSQI schema.

### Contributing new Quality Indicators

If you decide to open a pull request, please validate your JSON-LD with an open validator like [the JSON-LD Playground](https://json-ld.org/playground/) to agilize the review. Please make sure your indicator has a source, so we can double check its source and usefulness.
The following template may guide you when creating a description of your indicator:
```
### What is being measured?
    Explain what you are measuring
### Why should we measure it?
    Explain why
### What must be provided for the measurement? 
    For example, a zenodo record, or a GitHub id.
### How is the measurement executed?
    Explain the exact process for assessing the indicator
```

### About a Quality Indicator's response

In addition to the previous guidelines, the following possible outputs should be considered to ensure a good description and overall purpose:

- True: The indicator's condition/s are met
- False: The indicator's condition/s are not met
- Indeterminate: There is not enough information to measure the indicator


## New Software Quality Indicator Version

You may update an existing indicator by providing a new version through a pull-request.   
To do so, update the corresponding JSON file and the version following [SEMVER](https://semver.org/) semantics.

If you are not the original author of the schema, please request them to review your PR.


## Validate your schema

You may validate you JSON file using https://validator.schema.org/ before submitting it.

It will also be validated by our CI.

## Found an issue or bug?

Please open an issue.

## Have questions about the process or want to discuss an indicator before making a PR?

Please open an issue.
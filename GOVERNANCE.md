## Project Scope

This repository is aimed at defining and maintaining Research Software Quality and Project Health Indicators.  

The research software quality and project health indicators are used in: 
- The [Research Software Quality Kit](https://github.com/EVERSE-ResearchSoftware/RSQKit), for annotating task pages.
- The [TechRadar](https://github.com/EVERSE-ResearchSoftware/TechRadar), where tools helping measure or improve indicators are defined.
- The [Research Software Quality Pipelines](https://github.com/EVERSE-ResearchSoftware/QualityPipelines/tree/main), which provide actions to assess the indicators of a given repository.
- The [DASHVerse](https://github.com/EVERSE-ResearchSoftware/DashVERSE) dashboards, where they define what to visualize in a given tracked repository.


## Indicator lifecycle

All indicators are grounded on existing literature, indicating the source they have been derived from. In order for an indicatod to be considered, it must follow the [validation schema](https://github.com/EVERSE-ResearchSoftware/indicators/blob/main/tests/indicator_validation_schema.json) be submitted through a pull request.

Only then, a reviewer will assess it and decide whether or not the indicator is properly defined according to the contribution guidelines.

Contribution guidelines are defined in [CONTRIBUTING.md](https://github.com/EVERSE-ResearchSoftware/indicators/blob/main/CONTRIBUTING.md)

Once an indicator is added, reviewers will propagate it through the other tools:
- Annotating the corresponding tasks in RSQKit.
- Adding the corresponding tools to the TechRadar.
- Improving the quality pipelines with open source tools required for assessing them.

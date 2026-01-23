# RESTCountries Defects

This directory contains **16 replicable REST API bugs** documented REST API bugs from the [RESTCountries](https://github.com/apilayer/restcountries) project.

## Overview

RESTCountries is a public RESTful API that provides information about countries, including names, regions, currencies, languages, and population data. 

## Available Defects

The table below shows the available defects including the defect type, sub defect type, description of each defect and a link to the steps for replicating each defect.

| Issue ID # | Defect Type | Sub Defect Type | Description | Replication |
|:--:|--|--|--|--|
| [116](https://github.com/apilayer/restcountries/issues/116) | Data Validation and Query Processing Errors | Query Filter and Search Parameter Handling Errors | The issue reports incorrect country name translation returned by the API when queried for Morocco in Arabic. | [Replication steps](./restcountries%23116/README.md) |
| [118](https://github.com/apilayer/restcountries/issues/118) | Configuration and Environment Issues | Environment-Specific Behavior and Configuration Bugs | The API returns incorrect language data for Aruba and Curaçao indicating a misconfiguration of country-language mapping. | [Replication steps](./restcountries%23118/README.md) |
| [120](https://github.com/apilayer/restcountries/issues/120) | Data Validation and Query Processing Errors | Query Filter and Search Parameter Handling Errors | The API response for Chad's borders omits Sudan indicating an error in how border data is queried or filtered for this country. | [Replication steps](./restcountries%23120/README.md) |
| [156](https://github.com/apilayer/restcountries/issues/156) | Data Validation and Query Processing Errors | Query Filter and Search Parameter Handling Errors | The API returns incorrect data for the capital field when queried for Vatican City indicating an error in handling or returning search parameters. | [Replication steps](./restcountries%23156/README.md) |
| [177](https://github.com/apilayer/restcountries/issues/177) | Configuration and Environment Issues | Environment-Specific Behavior and Configuration Bugs | The API response for Antarctica omits expected currencies and languages indicating incomplete or inconsistent configuration for this specific region. | [Replication steps](./restcountries%23177/README.md) |
| [179](https://github.com/apilayer/restcountries/issues/179) |  Configuration and Environment Issues | Environment-Specific Behavior and Configuration Bugs | The API returns an incorrect list of time zones for France instead of the expected single value indicating a configuration or data mapping issue. | [Replication steps](./restcountries%23179/README.md) |
| [184](https://github.com/apilayer/restcountries/issues/184) | Data Validation and Query Processing Errors | Query Filter and Search Parameter Handling Errors | The API endpoint for the EU regional bloc returns incorrect results by including Faroe Islands which are not part of the EU. | [Replication steps](./restcountries%23184/README.md) |
| [199](https://github.com/apilayer/restcountries/issues/199) | Data Validation and Query Processing Errors | Query Filter and Search Parameter Handling Errors | The API returns an incorrect country name for a valid country code indicating a problem with how country data is retrieved or mapped based on query parameters. | [Replication steps](./restcountries%23199/README.md) |
| [201](https://github.com/apilayer/restcountries/issues/201) | Configuration and Environment Issues | Environment-Specific Behavior and Configuration Bugs | The API returns an incorrect timezone for Tbilisi, Georgia indicating a misconfiguration of environment-specific data. | [Replication steps](./restcountries%23201/README.md) |
| [202](https://github.com/apilayer/restcountries/issues/202) | Data Validation and Query Processing Errors | Query Filter and Search Parameter Handling Errors | The API returns inconsistent bordering country data for Suriname and Brazil indicating an error in how query results are constructed or filtered. | [Replication steps](./restcountries%23202/README.md) |
| [209](https://github.com/apilayer/restcountries/issues/209) | Data Validation and Query Processing Errors | Query Filter and Search Parameter Handling Errors | The API incorrectly includes the UK as an EU country indicating an error in how query or filter parameters determine EU membership. | [Replication steps](./restcountries%23209/README.md) |
| [221](https://github.com/apilayer/restcountries/issues/221) | Data Validation and Query Processing Errors | Query Filter and Search Parameter Handling Errors | The API returns an incorrect native name for Luxembourg indicating a problem with how country name data is filtered or selected for the response. | [Replication steps](./restcountries%23221/README.md) |
| [226](https://github.com/apilayer/restcountries/issues/226) | Data Validation and Query Processing Errors | Query Filter and Search Parameter Handling Errors | The API returns incorrect border country codes for Kuwait indicating an error in how country border data is queried or filtered. | [Replication steps](./restcountries%23226/README.md) |
| [235](https://github.com/apilayer/restcountries/issues/235) | Data Validation and Query Processing Errors | Query Filter and Search Parameter Handling Errors | The API returns the outdated capital name “Kiev” instead of “Kyiv,” indicating incorrect data handling or mapping. | [Replication steps](./restcountries%23235/README.md) |
| [237](https://github.com/apilayer/restcountries/issues/237) | Data Validation and Query Processing Errors | Query Filter and Search Parameter Handling Errors | The API returns inconsistent border country data for China and Nepal indicating an error in how query results are filtered or constructed. | [Replication steps](./restcountries%23237/README.md) |
| [249](https://github.com/apilayer/restcountries/issues/249) | Data Validation and Query Processing Errors | Query Filter and Search Parameter Handling Errors | The API returns an outdated country name for Eswatini which leads to incorrect query and search results for users. | [Replication steps](./restcountries%23249/README.md) |


## Deploying, Managing, and Inspecting a Defect (RESTCountries #116)

> **Note:** Replace **116** with the desired **issue ID** if you want to deploy a different issue.

Run the following commands in your terminal:

```bash
# 1. Deploy the buggy version of the issue
defects4rest checkout -p restcountries -i 116 --buggy --start

# 2. Deploy the patched version of the issue
defects4rest checkout -p restcountries -i 116 --patched --start

# 3. Stop running containers
defects4rest checkout -p restcountries -i 116 --stop

# 4. Full cleanup (stop + remove volumes/networks)
defects4rest checkout -p restcountries -i 116 --clean

# 5. Get bug information
defects4rest info -p restcountries -i 116

# 6. Check container logs if something goes wrong
docker logs restcountries-tomcat
```

## Accessing RESTCountries:

Once deployed, the RESTCountries service is accessible at:

* **Base URL:** `http://localhost:8080`
* **Authentication:** Not required

## Troubleshooting

If the RESTCountries service fails to start or behaves unexpectedly, check the container logs:

```bash
docker logs restcountries-tomcat
```

Ensure that the required ports are free and no conflicting services are running.

## References

* [RESTCountries GitHub Repository](https://github.com/apilayer/restcountries)
* [RESTCountries API Documentation](https://restcountries.com/)

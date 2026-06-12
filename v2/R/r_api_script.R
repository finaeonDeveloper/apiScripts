# Script for pulling data from the Finaeon API v2
# Authenticates with an API key in the X-Api-Key header.
# API keys can be managed from the Self-Service Portal:
# https://app.finaeon.com/

library(httr)
library(jsonlite)

base_url <- "https://api.finaeon.com"
# Trial API key. Replace with your own API key from the Self-Service Portal.
api_key <- ""

# Helper to POST to a v2 endpoint with the API key header
finaeon_call <- function(path, params) {
  resp <- httr::POST(url = paste0(base_url, path),
                     body = params,
                     encode = "json",
                     httr::add_headers(`X-Api-Key` = api_key))

  if (httr::status_code(resp) != 200) {
    stop(paste0("Finaeon API request to ", path,
                " failed with HTTP status code ", httr::status_code(resp),
                ": ", httr::content(resp, as = "text")))
  }

  jsonlite::fromJSON(httr::content(resp, as = "text"))
}

# Series with Price Data #

params <- list(seriesName = "IBM",
               startDate = "01/01/2019",
               endDate = "12/31/2024",
               periodicity = "Monthly",
               closeOnly = "true")

json_content <- finaeon_call("/v2/series", params)

# view price_data
print(json_content$price_data)

# view data_information
print(json_content$data_information)

# Search API #

params <- list(searchString = "MSFT",
               searchType = "symbol",
               baseFilter = "exactmatch",
               sort = "pop",
               pageSize = "20")

json_content <- finaeon_call("/v2/search", params)

# view search_results
print(json_content$search_results)

# Search by CIK codes API #

params <- list(cikCodes = "0000354950,0000789019")

json_content <- finaeon_call("/v2/searchbycikcodes", params)

print(json_content)

# Fundamentals API #
# NOTE: requires a subscription with fundamentals access -
# the trial API key will receive a 401 response.

params <- list(seriesName = "MSFT",
               period = "Annual",
               group = "Balance Sheet",
               startDate = "01/01/2010",
               endDate = "12/31/2020")

json_content <- tryCatch(finaeon_call("/v2/fundamentals", params),
                         error = function(e) message(conditionMessage(e)))

print(json_content$data)

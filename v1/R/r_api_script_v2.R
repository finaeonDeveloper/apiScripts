# Script for pulling data from the Finaeon Series API
# Author: Robert Mohr, Finaeon Data Scientist

library(httr)
library(jsonlite)
library(getPass)

#needed for password masking
# otherwise password must be passed explicitly to finaeon_auth()

# Function to obtain token
finaeon_auth <- function(username = NULL,
                     password = NULL) {

  if (is.null(username)) {
    stop("Argument username is required.")
  }

  if (is.null(password)) {

    msg <- "Please enter your Finaeon password:"
    password <- getPass::getPass(msg = msg)
  }

  url <- "https://api.finaeon.com/login/"

  params <- list(username = username, password = password)

  resp <- httr::POST(url = url, body = params, encode = "json")

  httr::stop_for_status(resp)

  json_content <- jsonlite::fromJSON(httr::content(resp, as = "text"))

  token <- gsub("\"", "", json_content$token)
  Sys.setenv("Finaeon_API_TOKEN" = token)
  message(paste0("Finaeon API token received at ", Sys.time()))
}

# call the finaeon_auth function with credentials

finaeon_auth()

# Multi Series with Price Data #

# url for access the Finaeon series API
url <- "https://api.finaeon.com/series/"

# define parameters
params <- list(seriesname = "IBM",
               seriesid = "",
               startdate = "01/01/2023",
               enddate = "12/31/2024",
               periodicity = "Daily",
               currency = "",
               metadata = "",
               splitadjusted = "",
               closeonly = "TRUE",
               inflationadjusted = "",
               annualflow = "",
               totalreturn = "",
               corporateactions = "",
               includeaverage = "",
               periodpercentchange = "",
               token = Sys.getenv("Finaeon_API_TOKEN"))

# make call
resp <- httr::POST(url = url, body = params, encode = "json")

json_content <- jsonlite::fromJSON(httr::content(resp, as = "text"))

# view price_data
json_content$price_data

# Print price_data
print(json_content$price_data)

# view data_informatoin
json_content$data_information

# Print data_informatoin
print(json_content$data_information)

# Search API #

# url for access the Finaeon search API
url <- "https://api.finaeon.com/search/"

# define parameters
params <- list(searchstring = "IBM",
               searchtype = "symbol",
               basefilter = "exactmatch",
               sort = "pop",
               page = "",
               pagesize = "20",
               token = Sys.getenv("Finaeon_API_TOKEN"))

# make call
resp <- httr::POST(url = url, body = params, encode = "json")

httr::stop_for_status(resp)

# extract JSON content
json_content <- jsonlite::fromJSON(httr::content(resp, as = "text"))

# view search_results
print(json_content$search_results)
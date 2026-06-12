# Finaeon API Scripts

Example scripts for requesting data from the [Finaeon API](https://api.finaeon.com) in Python and R.

## Repository layout

| Path | Contents |
|---|---|
| [v1/python](v1/python) | Python example script, Jupyter notebook, and API guide |
| [v1/R](v1/R) | R example script and API guide |

## Getting started

The API is hosted at `https://api.finaeon.com`. All modern endpoints accept `POST` requests with a JSON body (`Content-Type: application/json`).

A typical workflow:

1. Call `/login` with your username and password to receive a bearer token.
2. Pass that token in the body of subsequent calls (`/search`, `/series`, `/fundamentals`, ...).

### Trial access

Trial users (`tryapi@finaeon.com`) have access to the full history of all US stocks from 1/1/2019 to current, and full access to the following stock series:

> CVX, AXP, DIS, PG, CAT, HD, MCD, WMT, IBM, JNJ, MRK, MMM, BA, KO, HON, VZ, SHW, JPM, AAPL, NKE, TRV, MSFT, AMGN, CSCO, UNH, GS, AMZN, NVDA, CRM, V

Trial accounts do **not** have access to Fundamentals data or stock history prior to 2019. Contact [sales@finaeon.com](mailto:sales@finaeon.com) to upgrade.

## Endpoints

### POST /login

Authenticates a user account and returns a bearer token for use in subsequent API calls.

| Field | Required | Description |
|---|---|---|
| `userName` | yes | Username as assigned by GFD |
| `password` | yes | Password |

```json
{ "userName": "tryapi@finaeon.com", "password": "Test!123" }
```

Responses: `200` token returned, `400` invalid request, `401` could not authenticate, `429` rate limit exceeded.

### POST /search

Searches for and returns series metadata.

| Field | Required | Description |
|---|---|---|
| `token` | yes | Token from `/login` |
| `searchString` | yes | Characters to search for. For multiple symbols, use comma-separated values with `searchType: "symbol"` and `baseFilter: "exactmatch"` |
| `searchType` | no | Key field to search: `name`, `symbol` (default `name`) |
| `baseFilter` | no | Match mode: `contains`, `startswith`, `exactmatch` (default `contains`) |
| `sort` | no | Sort order: `pop` (most popular first), `alpha` (default `pop`) |
| `page` | no | Page number when paging (default: no paging) |
| `pageSize` | no | Records per page, 10–100 (default: no paging) |

```json
{ "token": "...", "page": "1", "pageSize": "25", "searchString": "copper", "searchType": "name", "baseFilter": "contains", "sort": "pop" }
```

Responses: `200` matching records, `400` invalid request, `404` no results, `429` rate limit exceeded.

### POST /searchbycikcodes

Searches for securities by SEC CIK code.

| Field | Required | Description |
|---|---|---|
| `token` | yes | Token from `/login` |
| `cikCodes` | yes | CIK code(s) to search for; comma-separated for multiple |

```json
{ "token": "...", "cikCodes": "0000354950,0000789019" }
```

Responses: `200` metadata for matching securities, `400` invalid request, `401` no results found, `429` rate limit exceeded.

### POST /series

Searches for and returns series metadata and price data.

| Field | Required | Description |
|---|---|---|
| `token` | yes | Token from `/login` |
| `seriesName` | yes | Series symbol/ticker; comma-separated for multiple series |
| `seriesId` | no | Search by GFD series ID instead |
| `startDate` | no | Start date, `MM/DD/YYYY` (default: earliest available) |
| `endDate` | no | End date, `MM/DD/YYYY` (default: latest available) |
| `periodicity` | no | `Daily`, `Weekly`, `Monthly`, `Quarterly`, `Annual` (default `Daily`) |
| `splitAdjusted` | no | `true`/`false` (default `true`) |
| `closeOnly` | no | Return only closing prices: `true`/`false` (default `false`) |
| `currency` | no | `USD`, `GBP`, `JPY`, `EUR`, `CAD`, `AUD`, `CHF`, `INR`, `BRL`, `CNY` (default: native currency) |
| `inflationAdjusted` | no | `true`/`false` (default `false`) |
| `annualFlow` | no | Annual flow summation: `true`/`false` (default `false`) |
| `totalReturn` | no | Rate of return over the interval: `true`/`false` (default `false`) |
| `corporateActions` | no | Include dividends, splits, etc.: `true`/`false` (default `false`) |
| `metadata` | no | Include series metadata: `true`/`false` (default `true`) |
| `incFields` | no | Extra identifier fields, comma-delimited, e.g. `"send,sbegin,currency,sector,equity_type,exchange,fiscal_end"` |
| `includeAverage` | no | Period average: `true`/`false` (default `false`) |
| `periodPercentChange` | no | Percent change per period: `true`/`false` (default `false`) |
| `annualPercentChange` | no | Annual percent change: `true`/`false` (default `false`) |
| `pointInTime` | no | Only splits within the date range are cumulatively applied: `true`/`false` (default `true`) |

```json
{ "token": "...", "seriesName": "MSFT", "startDate": "01/01/2010", "endDate": "12/31/2020", "periodicity": "Annual", "totalReturn": "true", "metadata": "false" }
```

Responses: `200` price data, `400` invalid request, `401` unauthorized, `404` series not found, `429` rate limit exceeded.

### POST /fundamentals

Searches for and returns series fundamental data by group. *(Requires a subscription with fundamentals access — not available to trial users.)*

| Field | Required | Description |
|---|---|---|
| `token` | yes | Token from `/login` |
| `seriesName` | yes | Series symbol/ticker; single symbol only |
| `period` | yes | `Quarterly`, `Annual` |
| `group` | no | `Balance Sheet`, `Cash Flow`, `Estimates`, `Fundamentals`, `Income Statement`, `Ratios`, `Basic Ratios`, `Share Information` |
| `startDate` | no | Start date, `MM/DD/YYYY` (default `01/01/1000`) |
| `endDate` | no | End date, `MM/DD/YYYY` (default: latest available) |

```json
{ "token": "...", "seriesName": "MSFT", "period": "annual", "group": "Balance Sheet", "startDate": "01/01/2010", "endDate": "12/31/2020" }
```

Responses: `200` fundamentals data, `400` invalid request, `401` unauthorized, `404` series not found, `429` rate limit exceeded.

## Legacy endpoints

These older `GET` endpoints authenticate with `username`/`password` query parameters (no token) and return a file in the selected output format.

### GET /api/api.ashx

Searches for series and returns a file containing price data.

Key parameters: `username`, `password`, `filename` (symbol(s), e.g. `MSFT` or `V,GS,UNH`), `series_id` (used only if `filename` is omitted), `startdate`/`enddate` (`MM/DD/YYYY` or `YYYY`), `periodicity` (`Daily`–`Annual`), `type` (`csv`, `Excel`, `xlsx`), plus the same boolean flags as `/series` (`splitadjusted`, `closeonly`, `currency`, `inflationadjusted`, `annualizedflow`, `totalreturn`, `corporate_actions`, `IncludeSeriesId`, `average`, `periodpercentchange`, `metadata`).

### GET /api/bulk.ashx

Returns price data for **all** series in a database on a given date.

Key parameters: `username`, `password`, `database` (`gfdatabase`, `usstocks`, `ukstocks`), `date` (`MM/DD/YYYY`), `includecorporateactions` (`true`/`false`), `outputtype` (`csv`, `Excel`, `xlsx`).

### GET /api/fundamentals.ashx

Returns fundamental data by group as a file.

Key parameters: `username`, `password`, `filename` (single symbol), `group` (same options as `/fundamentals`), `period` (`Quarterly`, `Annual`), `startdate`/`enddate`, `format` (`csv`, `Excel`, `xlsx`).

### GET /api/search.ashx

Returns series metadata matching a search.

Key parameters: `username`, `password`, `searchstring`, `searchtype` (`name`, `symbol`), `searchfilter` (`contains`, `startswith`, `exactmatch`), `sort` (`pop`, `alpha`), `page`, `pagesize` (10–100).

## Resources

- [API Examples (zip)](https://finaeonsiteimages.blob.core.windows.net/docs/GFD_API.zip)
- [Terms of Service](https://gfdpolicies.blob.core.windows.net/legal/Terms.pdf)
- Sales / subscription upgrades: [sales@finaeon.com](mailto:sales@finaeon.com)

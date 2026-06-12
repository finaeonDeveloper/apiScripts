# Finaeon API v2

API for requesting data from [Finaeon](https://api.finaeon.com) using an API key.

## Authentication

v2 replaces the v1 login/token flow with API key authentication. Provide your API key in the **`X-Api-Key`** header on every request — there is no `/login` call and no `token` field in request bodies. API keys can be managed from the Self-Service Portal.

```
POST https://api.finaeon.com/v2/series
Content-Type: application/json
X-Api-Key: <your-api-key>
```

### Trial access

Trial users have access to the full history of all US stocks from 1/1/2019 to current, and full access to the following stock series:

> CVX, AXP, DIS, PG, CAT, HD, MCD, WMT, IBM, JNJ, MRK, MMM, BA, KO, HON, VZ, SHW, JPM, AAPL, NKE, TRV, MSFT, AMGN, CSCO, UNH, GS, AMZN, NVDA, CRM, V

Contact [sales@finaeon.com](mailto:sales@finaeon.com) to gain access to stock history prior to 2019.

## Endpoints

All endpoints accept `POST` requests with a JSON body and authenticate with the `X-Api-Key` header.

### POST /v2/search

Searches for and returns series metadata.

| Field | Required | Description |
|---|---|---|
| `searchString` | yes | Characters to search for. For multiple symbols, use comma-separated values with `searchType: "symbol"` and `baseFilter: "exactmatch"` |
| `searchType` | no | Key field to search: `name`, `symbol` (default `name`) |
| `baseFilter` | no | Match mode: `contains`, `startswith`, `exactmatch` (default `contains`) |
| `sort` | no | Sort order: `pop` (most popular first), `alpha` (default `pop`) |
| `page` | no | Page number when paging (default: no paging) |
| `pageSize` | no | Records per page, 10–100 (default: no paging) |

Request:

```json
{ "page": "1", "pageSize": "25", "searchString": "copper", "searchType": "name", "baseFilter": "contains", "sort": "pop" }
```

Response — `paging_info` plus an array of `search_results` (series ID, country, currency, sector, date range, symbol, description, periodicity, units, scale, CIK, and a `has_access` flag):

```json
{
  "paging_info": { "current_page": "1", "page_size": "25", "total_records": "1", "total_pages": "1" },
  "search_results": [
    {
      "series_id": 11297,
      "country_name": "United States",
      "iso": "USA",
      "currency": "USD",
      "series": "Commodity",
      "gfd_sector": "Commodities",
      "start_date": "1850-01-02T00:00:00",
      "end_date": "2026-06-09T00:00:00",
      "symbol": "__CU_D",
      "description": "Copper Cash Price (CME) ($/pound)",
      "periodicity": "Daily",
      "units": "$/pound",
      "scale": "Units",
      "scale_num": 1,
      "has_access": 1
    }
  ]
}
```

Responses: `200` matching records, `400` invalid request, `401` unauthorized, `404` no results, `429` rate limit exceeded.

### POST /v2/searchbycikcodes

Searches for securities by SEC CIK code.

| Field | Required | Description |
|---|---|---|
| `cikCodes` | yes | CIK code(s) to search for; comma-separated for multiple |

Request:

```json
{ "cikCodes": "0000354950,0000789019" }
```

Response — an array of matches with `seriesId`, `seriesName`, and `cik`:

```json
[
  { "seriesId": "29947", "seriesName": "HD", "cik": "0000354950" },
  { "seriesId": "46074", "seriesName": "MSFT", "cik": "0000789019" }
]
```

Responses: `200` metadata for matching securities, `400` invalid request, `401` unauthorized, `429` rate limit exceeded.

### POST /v2/series

Searches for and returns series metadata and price data.

| Field | Required | Description |
|---|---|---|
| `seriesName` | yes | Series symbol/ticker; comma-separated for multiple series |
| `seriesId` | no | Search by Finaeon series ID instead |
| `startDate` | no | Start date, `MM/DD/YYYY` (default `01/01/1000`) |
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

Request:

```json
{ "seriesName": "MSFT", "startDate": "01/01/2010", "endDate": "12/31/2020", "periodicity": "Annual", "totalReturn": "true", "metadata": "false" }
```

Response — `download_status`, `messages`, `data_information` (series metadata), `price_data` (OHLCV rows), and `splits_and_dividends`:

```json
{
  "download_status": [{ "id": "46074", "status": "Downloaded" }],
  "messages": [],
  "data_information": [
    { "series_id": 46074, "symbol": "MSFT", "series_type": "Stock", "description": "Microsoft Corp.", "exchange": "NASDAQ", "currency": "USD", "periodicity": "Annual" }
  ],
  "price_data": [
    { "symbol": "MSFT", "date": "12/31/2019", "open": 158.78, "high": 159.55, "low": 156.51, "close": 157.7, "volume": 18369400 },
    { "symbol": "MSFT", "date": "12/31/2020", "open": 221.7, "high": 223, "low": 219.68, "close": 222.42, "volume": 20942100 }
  ],
  "splits_and_dividends": [
    { "symbol": "MSFT", "date": "02/18/2003", "split": "2:1" }
  ]
}
```

Responses: `200` price data, `400` invalid request, `401` unauthorized, `404` series not found, `429` rate limit exceeded.

### POST /v2/fundamentals

Searches for and returns series fundamental data by group. *(Requires a subscription with fundamentals access — not available to trial users.)*

| Field | Required | Description |
|---|---|---|
| `seriesName` | yes | Series symbol/ticker; single symbol only |
| `period` | yes | `Quarterly`, `Annual` |
| `group` | no | `Balance Sheet`, `Cash Flow`, `Estimates`, `Fundamentals`, `Income Statement`, `Ratios`, `Basic Ratios`, `Share Information` |
| `startDate` | no | Start date, `MM/DD/YYYY` (default `01/01/1000`) |
| `endDate` | no | End date, `MM/DD/YYYY` (default: latest available) |

Request:

```json
{ "seriesName": "MSFT", "period": "annual", "group": "Balance Sheet", "startDate": "01/01/2010", "endDate": "12/31/2020" }
```

Response — `download_status`, `messages`, and a `data` array of fundamentals rows:

```json
{
  "download_status": [],
  "messages": [],
  "data": [
    { "ticker": "MSFT", "date": "12/31/2019", "total_assets": "286556000000", "total_liabilities": "184226000000", "stockholders_equity": "102330000000" },
    { "ticker": "MSFT", "date": "12/31/2020", "total_assets": "301311000000", "total_liabilities": "183007000000", "stockholders_equity": "118304000000" }
  ]
}
```

Responses: `200` fundamentals data, `400` invalid request, `401` unauthorized, `404` series not found, `429` rate limit exceeded.

## Differences from v1

- **API key auth**: send `X-Api-Key` header instead of calling `/login` and passing a `token` in every request body.
- **Endpoint prefix**: all paths are under `/v2/` (e.g. `/v2/series` instead of `/series`).
- **No legacy endpoints**: the `GET /api/*.ashx` endpoints are v1 only.

See [../v1/README.md](../v1/README.md) for the v1 documentation.

## Resources

- [API Examples (zip)](https://finaeonsiteimages.blob.core.windows.net/docs/GFD_API.zip)
- [Terms of Service](https://gfdpolicies.blob.core.windows.net/legal/Terms.pdf)
- Sales / subscription upgrades: [sales@finaeon.com](mailto:sales@finaeon.com)

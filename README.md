# Finaeon API Scripts

Documentation and example scripts for the [Finaeon API](https://api.finaeon.com), which provides historical price data, series metadata, and fundamentals for stocks, commodities, and other financial series.

The API has two versions, documented in their own folders:

| Version | Docs | Authentication | Endpoints |
|---|---|---|---|
| v1 | [v1/README.md](v1/README.md) | Username/password via `/login`, token passed in each request body | `/login`, `/search`, `/searchbycikcodes`, `/series`, `/fundamentals`, plus legacy `GET /api/*.ashx` endpoints |
| v2 | [v2/README.md](v2/README.md) | API key via `X-Api-Key` header (managed in the Self-Service Portal) | `/v2/search`, `/v2/searchbycikcodes`, `/v2/series`, `/v2/fundamentals` |

## v1

The original API. Authenticate by POSTing credentials to `/login` to receive a bearer token, then include that token in the body of every subsequent call. Also includes the legacy `GET` endpoints (`/api/api.ashx`, `/api/bulk.ashx`, `/api/fundamentals.ashx`, `/api/search.ashx`) that authenticate with query-string credentials and return CSV/Excel files.

The [v1](v1) folder also contains example clients:

- [v1/python](v1/python) — Python script, Jupyter notebook, and API guide
- [v1/R](v1/R) — R script and API guide

## v2

The current API. Replaces the login/token flow with API key authentication — send your key in the `X-Api-Key` header on every request. Endpoints live under the `/v2/` prefix and the legacy `.ashx` endpoints are dropped. Request parameters are otherwise the same as v1 (minus the `token` field), and response shapes are documented in the [v2 README](v2/README.md).

## Trial access

Trial users have access to the full history of all US stocks from 1/1/2019 to current, and full access to these stock series:

> CVX, AXP, DIS, PG, CAT, HD, MCD, WMT, IBM, JNJ, MRK, MMM, BA, KO, HON, VZ, SHW, JPM, AAPL, NKE, TRV, MSFT, AMGN, CSCO, UNH, GS, AMZN, NVDA, CRM, V

Fundamentals data and pre-2019 stock history require an upgraded subscription — contact [sales@finaeon.com](mailto:sales@finaeon.com).

## Resources

- [Terms of Service](https://gfdpolicies.blob.core.windows.net/legal/Terms.pdf)

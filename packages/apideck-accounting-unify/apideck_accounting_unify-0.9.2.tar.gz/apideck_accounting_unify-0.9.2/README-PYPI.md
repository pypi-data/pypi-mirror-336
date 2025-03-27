# apideck-accounting-unify

Developer-friendly & type-safe Python SDK specifically catered to leverage *apideck-accounting-unify* API.

<div align="left">
    <a href="https://www.speakeasy.com/?utm_source=apideck-accounting-unify&utm_campaign=python"><img src="https://custom-icon-badges.demolab.com/badge/-Built%20By%20Speakeasy-212015?style=for-the-badge&logoColor=FBE331&logo=speakeasy&labelColor=545454" /></a>
    <a href="https://opensource.org/licenses/MIT">
        <img src="https://img.shields.io/badge/License-MIT-blue.svg" style="width: 100px; height: 28px;" />
    </a>
</div>


<br /><br />
> [!IMPORTANT]
> This SDK is not yet ready for production use. To complete setup please follow the steps outlined in your [workspace](https://app.speakeasy.com/org/apideck-k2o/apideck). Delete this section before > publishing to a package manager.

<!-- Start Summary [summary] -->
## Summary

Apideck: The Apideck OpenAPI Spec: SDK Optimized

For more information about the API: [Apideck Developer Docs](https://developers.apideck.com)
<!-- End Summary [summary] -->

<!-- Start Table of Contents [toc] -->
## Table of Contents
<!-- $toc-max-depth=2 -->
* [apideck-accounting-unify](#apideck-accounting-unify)
  * [SDK Installation](#sdk-installation)
  * [IDE Support](#ide-support)
  * [SDK Example Usage](#sdk-example-usage)
  * [Authentication](#authentication)
  * [Available Resources and Operations](#available-resources-and-operations)
  * [Pagination](#pagination)
  * [Retries](#retries)
  * [Error Handling](#error-handling)
  * [Server Selection](#server-selection)
  * [Custom HTTP Client](#custom-http-client)
  * [Resource Management](#resource-management)
  * [Debugging](#debugging)
* [Development](#development)
  * [Maturity](#maturity)
  * [Contributions](#contributions)

<!-- End Table of Contents [toc] -->

<!-- Start SDK Installation [installation] -->
## SDK Installation

> [!NOTE]
> **Python version upgrade policy**
>
> Once a Python version reaches its [official end of life date](https://devguide.python.org/versions/), a 3-month grace period is provided for users to upgrade. Following this grace period, the minimum python version supported in the SDK will be updated.

The SDK can be installed with either *pip* or *poetry* package managers.

### PIP

*PIP* is the default package installer for Python, enabling easy installation and management of packages from PyPI via the command line.

```bash
pip install apideck-accounting-unify
```

### Poetry

*Poetry* is a modern tool that simplifies dependency management and package publishing by using a single `pyproject.toml` file to handle project metadata and dependencies.

```bash
poetry add apideck-accounting-unify
```

### Shell and script usage with `uv`

You can use this SDK in a Python shell with [uv](https://docs.astral.sh/uv/) and the `uvx` command that comes with it like so:

```shell
uvx --from apideck-accounting-unify python
```

It's also possible to write a standalone Python script without needing to set up a whole project like so:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "apideck-accounting-unify",
# ]
# ///

from apideck_accounting_unify import Apideck

sdk = Apideck(
  # SDK arguments
)

# Rest of script here...
```

Once that is saved to a file, you can run it with `uv run script.py` where
`script.py` can be replaced with the actual file name.
<!-- End SDK Installation [installation] -->

<!-- Start IDE Support [idesupport] -->
## IDE Support

### PyCharm

Generally, the SDK will work well with most IDEs out of the box. However, when using PyCharm, you can enjoy much better integration with Pydantic by installing an additional plugin.

- [PyCharm Pydantic Plugin](https://docs.pydantic.dev/latest/integrations/pycharm/)
<!-- End IDE Support [idesupport] -->

<!-- Start SDK Example Usage [usage] -->
## SDK Example Usage

### Example

```python
# Synchronous Example
from apideck_accounting_unify import Apideck
import os


with Apideck(
    api_key=os.getenv("APIDECK_API_KEY", ""),
    consumer_id="test-consumer",
    app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX",
) as apideck:

    res = apideck.accounting.tax_rates.get(id="<id>", consumer_id="test-consumer", app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX", service_id="salesforce", fields="id,updated_at")

    assert res.get_tax_rate_response is not None

    # Handle response
    print(res.get_tax_rate_response)
```

</br>

The same SDK client can also be used to make asychronous requests by importing asyncio.
```python
# Asynchronous Example
from apideck_accounting_unify import Apideck
import asyncio
import os

async def main():

    async with Apideck(
        api_key=os.getenv("APIDECK_API_KEY", ""),
        consumer_id="test-consumer",
        app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX",
    ) as apideck:

        res = await apideck.accounting.tax_rates.get_async(id="<id>", consumer_id="test-consumer", app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX", service_id="salesforce", fields="id,updated_at")

        assert res.get_tax_rate_response is not None

        # Handle response
        print(res.get_tax_rate_response)

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->

<!-- Start Authentication [security] -->
## Authentication

### Per-Client Security Schemes

This SDK supports the following security scheme globally:

| Name      | Type | Scheme      | Environment Variable |
| --------- | ---- | ----------- | -------------------- |
| `api_key` | http | HTTP Bearer | `APIDECK_API_KEY`    |

To authenticate with the API the `api_key` parameter must be set when initializing the SDK client instance. For example:
```python
from apideck_accounting_unify import Apideck
import os


with Apideck(
    api_key=os.getenv("APIDECK_API_KEY", ""),
    consumer_id="test-consumer",
    app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX",
) as apideck:

    res = apideck.accounting.tax_rates.get(id="<id>", consumer_id="test-consumer", app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX", service_id="salesforce", fields="id,updated_at")

    assert res.get_tax_rate_response is not None

    # Handle response
    print(res.get_tax_rate_response)

```
<!-- End Authentication [security] -->

<!-- Start Available Resources and Operations [operations] -->
## Available Resources and Operations

<details open>
<summary>Available methods</summary>

### [accounting](docs/sdks/accounting/README.md)


#### [accounting.aged_debtors](docs/sdks/ageddebtorssdk/README.md)

* [get](docs/sdks/ageddebtorssdk/README.md#get) - Get Aged Debtors

#### [accounting.attachments](docs/sdks/attachments/README.md)

* [list](docs/sdks/attachments/README.md#list) - List Attachments
* [get](docs/sdks/attachments/README.md#get) - Get Attachment
* [delete](docs/sdks/attachments/README.md#delete) - Delete Attachment
* [download](docs/sdks/attachments/README.md#download) - Download Attachment

#### [accounting.balance_sheet](docs/sdks/balancesheetsdk/README.md)

* [get](docs/sdks/balancesheetsdk/README.md#get) - Get BalanceSheet

#### [accounting.bill_payments](docs/sdks/billpayments/README.md)

* [get](docs/sdks/billpayments/README.md#get) - Get Bill Payment
* [update](docs/sdks/billpayments/README.md#update) - Update Bill Payment
* [delete](docs/sdks/billpayments/README.md#delete) - Delete Bill Payment

#### [accounting.bills](docs/sdks/bills/README.md)

* [get](docs/sdks/bills/README.md#get) - Get Bill
* [update](docs/sdks/bills/README.md#update) - Update Bill
* [delete](docs/sdks/bills/README.md#delete) - Delete Bill

#### [accounting.company_info](docs/sdks/companyinfosdk/README.md)

* [get](docs/sdks/companyinfosdk/README.md#get) - Get company info

#### [accounting.credit_notes](docs/sdks/creditnotes/README.md)

* [get](docs/sdks/creditnotes/README.md#get) - Get Credit Note
* [update](docs/sdks/creditnotes/README.md#update) - Update Credit Note
* [delete](docs/sdks/creditnotes/README.md#delete) - Delete Credit Note

#### [accounting.customers](docs/sdks/customers/README.md)

* [get](docs/sdks/customers/README.md#get) - Get Customer
* [update](docs/sdks/customers/README.md#update) - Update Customer
* [delete](docs/sdks/customers/README.md#delete) - Delete Customer

#### [accounting.departments](docs/sdks/departments/README.md)

* [get](docs/sdks/departments/README.md#get) - Get Department
* [update](docs/sdks/departments/README.md#update) - Update Department
* [delete](docs/sdks/departments/README.md#delete) - Delete Department

#### [accounting.expenses](docs/sdks/expenses/README.md)

* [get](docs/sdks/expenses/README.md#get) - Get Expense
* [update](docs/sdks/expenses/README.md#update) - Update Expense
* [delete](docs/sdks/expenses/README.md#delete) - Delete Expense

#### [accounting.invoice_items](docs/sdks/invoiceitems/README.md)

* [get](docs/sdks/invoiceitems/README.md#get) - Get Invoice Item
* [update](docs/sdks/invoiceitems/README.md#update) - Update Invoice Item
* [delete](docs/sdks/invoiceitems/README.md#delete) - Delete Invoice Item

#### [accounting.invoices](docs/sdks/invoices/README.md)

* [get](docs/sdks/invoices/README.md#get) - Get Invoice
* [update](docs/sdks/invoices/README.md#update) - Update Invoice
* [delete](docs/sdks/invoices/README.md#delete) - Delete Invoice

#### [accounting.journal_entries](docs/sdks/journalentries/README.md)

* [get](docs/sdks/journalentries/README.md#get) - Get Journal Entry
* [update](docs/sdks/journalentries/README.md#update) - Update Journal Entry
* [delete](docs/sdks/journalentries/README.md#delete) - Delete Journal Entry

#### [accounting.ledger_accounts](docs/sdks/ledgeraccounts/README.md)

* [get](docs/sdks/ledgeraccounts/README.md#get) - Get Ledger Account
* [update](docs/sdks/ledgeraccounts/README.md#update) - Update Ledger Account
* [delete](docs/sdks/ledgeraccounts/README.md#delete) - Delete Ledger Account

#### [accounting.locations](docs/sdks/locations/README.md)

* [get](docs/sdks/locations/README.md#get) - Get Location
* [update](docs/sdks/locations/README.md#update) - Update Location
* [delete](docs/sdks/locations/README.md#delete) - Delete Location

#### [accounting.payments](docs/sdks/payments/README.md)

* [get](docs/sdks/payments/README.md#get) - Get Payment
* [update](docs/sdks/payments/README.md#update) - Update Payment
* [delete](docs/sdks/payments/README.md#delete) - Delete Payment

#### [accounting.profit_and_loss](docs/sdks/profitandlosssdk/README.md)

* [get](docs/sdks/profitandlosssdk/README.md#get) - Get Profit and Loss

#### [accounting.purchase_orders](docs/sdks/purchaseorders/README.md)

* [get](docs/sdks/purchaseorders/README.md#get) - Get Purchase Order
* [update](docs/sdks/purchaseorders/README.md#update) - Update Purchase Order
* [delete](docs/sdks/purchaseorders/README.md#delete) - Delete Purchase Order

#### [accounting.subsidiaries](docs/sdks/subsidiaries/README.md)

* [get](docs/sdks/subsidiaries/README.md#get) - Get Subsidiary
* [update](docs/sdks/subsidiaries/README.md#update) - Update Subsidiary
* [delete](docs/sdks/subsidiaries/README.md#delete) - Delete Subsidiary

#### [accounting.suppliers](docs/sdks/suppliers/README.md)

* [get](docs/sdks/suppliers/README.md#get) - Get Supplier
* [update](docs/sdks/suppliers/README.md#update) - Update Supplier
* [delete](docs/sdks/suppliers/README.md#delete) - Delete Supplier

#### [accounting.tax_rates](docs/sdks/taxrates/README.md)

* [get](docs/sdks/taxrates/README.md#get) - Get Tax Rate
* [update](docs/sdks/taxrates/README.md#update) - Update Tax Rate
* [delete](docs/sdks/taxrates/README.md#delete) - Delete Tax Rate

#### [accounting.tracking_categories](docs/sdks/trackingcategories/README.md)

* [get](docs/sdks/trackingcategories/README.md#get) - Get Tracking Category
* [update](docs/sdks/trackingcategories/README.md#update) - Update Tracking Category
* [delete](docs/sdks/trackingcategories/README.md#delete) - Delete Tracking Category


### [vault](docs/sdks/vault/README.md)


#### [vault.connection_custom_mappings](docs/sdks/connectioncustommappings/README.md)

* [list](docs/sdks/connectioncustommappings/README.md#list) - List connection custom mappings

#### [vault.connection_settings](docs/sdks/connectionsettings/README.md)

* [list](docs/sdks/connectionsettings/README.md#list) - Get resource settings
* [update](docs/sdks/connectionsettings/README.md#update) - Update settings

#### [vault.connections](docs/sdks/connections/README.md)

* [list](docs/sdks/connections/README.md#list) - Get all connections
* [get](docs/sdks/connections/README.md#get) - Get connection
* [update](docs/sdks/connections/README.md#update) - Update connection
* [delete](docs/sdks/connections/README.md#delete) - Deletes a connection

#### [vault.consumer_request_counts](docs/sdks/consumerrequestcounts/README.md)

* [list](docs/sdks/consumerrequestcounts/README.md#list) - Consumer request counts

#### [vault.consumers](docs/sdks/consumers/README.md)

* [get](docs/sdks/consumers/README.md#get) - Get consumer
* [update](docs/sdks/consumers/README.md#update) - Update consumer
* [delete](docs/sdks/consumers/README.md#delete) - Delete consumer

#### [vault.custom_fields](docs/sdks/customfields/README.md)

* [list](docs/sdks/customfields/README.md#list) - Get resource custom fields

#### [vault.custom_mappings](docs/sdks/custommappingssdk/README.md)

* [list](docs/sdks/custommappingssdk/README.md#list) - List custom mappings

#### [vault.logs](docs/sdks/logs/README.md)

* [list](docs/sdks/logs/README.md#list) - Get all consumer request logs

</details>
<!-- End Available Resources and Operations [operations] -->

<!-- Start Pagination [pagination] -->
## Pagination

Some of the endpoints in this SDK support pagination. To use pagination, you make your SDK calls as usual, but the
returned response object will have a `Next` method that can be called to pull down the next group of results. If the
return value of `Next` is `None`, then there are no more pages to be fetched.

Here's an example of one such pagination call:
```python
import apideck_accounting_unify
from apideck_accounting_unify import Apideck
import os


with Apideck(
    api_key=os.getenv("APIDECK_API_KEY", ""),
    consumer_id="test-consumer",
    app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX",
) as apideck:

    res = apideck.accounting.attachments.list(reference_type=apideck_accounting_unify.AttachmentReferenceType.INVOICE, reference_id="123456", consumer_id="test-consumer", app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX", service_id="salesforce", fields="id,updated_at")

    while res is not None:
        # Handle items

        res = res.next()

```
<!-- End Pagination [pagination] -->

<!-- Start Retries [retries] -->
## Retries

Some of the endpoints in this SDK support retries. If you use the SDK without any configuration, it will fall back to the default retry strategy provided by the API. However, the default retry strategy can be overridden on a per-operation basis, or across the entire SDK.

To change the default retry strategy for a single API call, simply provide a `RetryConfig` object to the call:
```python
from apideck_accounting_unify import Apideck
from apideck_accounting_unify.utils import BackoffStrategy, RetryConfig
import os


with Apideck(
    api_key=os.getenv("APIDECK_API_KEY", ""),
    consumer_id="test-consumer",
    app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX",
) as apideck:

    res = apideck.accounting.tax_rates.get(id="<id>", consumer_id="test-consumer", app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX", service_id="salesforce", fields="id,updated_at",
        RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False))

    assert res.get_tax_rate_response is not None

    # Handle response
    print(res.get_tax_rate_response)

```

If you'd like to override the default retry strategy for all operations that support retries, you can use the `retry_config` optional parameter when initializing the SDK:
```python
from apideck_accounting_unify import Apideck
from apideck_accounting_unify.utils import BackoffStrategy, RetryConfig
import os


with Apideck(
    retry_config=RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False),
    api_key=os.getenv("APIDECK_API_KEY", ""),
    consumer_id="test-consumer",
    app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX",
) as apideck:

    res = apideck.accounting.tax_rates.get(id="<id>", consumer_id="test-consumer", app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX", service_id="salesforce", fields="id,updated_at")

    assert res.get_tax_rate_response is not None

    # Handle response
    print(res.get_tax_rate_response)

```
<!-- End Retries [retries] -->

<!-- Start Error Handling [errors] -->
## Error Handling

Handling errors in this SDK should largely match your expectations. All operations return a response object or raise an exception.

By default, an API error will raise a models.APIError exception, which has the following properties:

| Property        | Type             | Description           |
|-----------------|------------------|-----------------------|
| `.status_code`  | *int*            | The HTTP status code  |
| `.message`      | *str*            | The error message     |
| `.raw_response` | *httpx.Response* | The raw HTTP response |
| `.body`         | *str*            | The response content  |

When custom error responses are specified for an operation, the SDK may also raise their associated exceptions. You can refer to respective *Errors* tables in SDK docs for more details on possible exception types for each operation. For example, the `get_async` method may raise the following exceptions:

| Error Type                     | Status Code | Content Type     |
| ------------------------------ | ----------- | ---------------- |
| models.BadRequestResponse      | 400         | application/json |
| models.UnauthorizedResponse    | 401         | application/json |
| models.PaymentRequiredResponse | 402         | application/json |
| models.NotFoundResponse        | 404         | application/json |
| models.UnprocessableResponse   | 422         | application/json |
| models.APIError                | 4XX, 5XX    | \*/\*            |

### Example

```python
from apideck_accounting_unify import Apideck, models
import os


with Apideck(
    api_key=os.getenv("APIDECK_API_KEY", ""),
    consumer_id="test-consumer",
    app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX",
) as apideck:
    res = None
    try:

        res = apideck.accounting.tax_rates.get(id="<id>", consumer_id="test-consumer", app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX", service_id="salesforce", fields="id,updated_at")

        assert res.get_tax_rate_response is not None

        # Handle response
        print(res.get_tax_rate_response)

    except models.BadRequestResponse as e:
        # handle e.data: models.BadRequestResponseData
        raise(e)
    except models.UnauthorizedResponse as e:
        # handle e.data: models.UnauthorizedResponseData
        raise(e)
    except models.PaymentRequiredResponse as e:
        # handle e.data: models.PaymentRequiredResponseData
        raise(e)
    except models.NotFoundResponse as e:
        # handle e.data: models.NotFoundResponseData
        raise(e)
    except models.UnprocessableResponse as e:
        # handle e.data: models.UnprocessableResponseData
        raise(e)
    except models.APIError as e:
        # handle exception
        raise(e)
```
<!-- End Error Handling [errors] -->

<!-- Start Server Selection [server] -->
## Server Selection

### Override Server URL Per-Client

The default server can be overridden globally by passing a URL to the `server_url: str` optional parameter when initializing the SDK client instance. For example:
```python
from apideck_accounting_unify import Apideck
import os


with Apideck(
    server_url="https://unify.apideck.com",
    api_key=os.getenv("APIDECK_API_KEY", ""),
    consumer_id="test-consumer",
    app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX",
) as apideck:

    res = apideck.accounting.tax_rates.get(id="<id>", consumer_id="test-consumer", app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX", service_id="salesforce", fields="id,updated_at")

    assert res.get_tax_rate_response is not None

    # Handle response
    print(res.get_tax_rate_response)

```
<!-- End Server Selection [server] -->

<!-- Start Custom HTTP Client [http-client] -->
## Custom HTTP Client

The Python SDK makes API calls using the [httpx](https://www.python-httpx.org/) HTTP library.  In order to provide a convenient way to configure timeouts, cookies, proxies, custom headers, and other low-level configuration, you can initialize the SDK client with your own HTTP client instance.
Depending on whether you are using the sync or async version of the SDK, you can pass an instance of `HttpClient` or `AsyncHttpClient` respectively, which are Protocol's ensuring that the client has the necessary methods to make API calls.
This allows you to wrap the client with your own custom logic, such as adding custom headers, logging, or error handling, or you can just pass an instance of `httpx.Client` or `httpx.AsyncClient` directly.

For example, you could specify a header for every request that this sdk makes as follows:
```python
from apideck_accounting_unify import Apideck
import httpx

http_client = httpx.Client(headers={"x-custom-header": "someValue"})
s = Apideck(client=http_client)
```

or you could wrap the client with your own custom logic:
```python
from apideck_accounting_unify import Apideck
from apideck_accounting_unify.httpclient import AsyncHttpClient
import httpx

class CustomClient(AsyncHttpClient):
    client: AsyncHttpClient

    def __init__(self, client: AsyncHttpClient):
        self.client = client

    async def send(
        self,
        request: httpx.Request,
        *,
        stream: bool = False,
        auth: Union[
            httpx._types.AuthTypes, httpx._client.UseClientDefault, None
        ] = httpx.USE_CLIENT_DEFAULT,
        follow_redirects: Union[
            bool, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
    ) -> httpx.Response:
        request.headers["Client-Level-Header"] = "added by client"

        return await self.client.send(
            request, stream=stream, auth=auth, follow_redirects=follow_redirects
        )

    def build_request(
        self,
        method: str,
        url: httpx._types.URLTypes,
        *,
        content: Optional[httpx._types.RequestContent] = None,
        data: Optional[httpx._types.RequestData] = None,
        files: Optional[httpx._types.RequestFiles] = None,
        json: Optional[Any] = None,
        params: Optional[httpx._types.QueryParamTypes] = None,
        headers: Optional[httpx._types.HeaderTypes] = None,
        cookies: Optional[httpx._types.CookieTypes] = None,
        timeout: Union[
            httpx._types.TimeoutTypes, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
        extensions: Optional[httpx._types.RequestExtensions] = None,
    ) -> httpx.Request:
        return self.client.build_request(
            method,
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            extensions=extensions,
        )

s = Apideck(async_client=CustomClient(httpx.AsyncClient()))
```
<!-- End Custom HTTP Client [http-client] -->

<!-- Start Resource Management [resource-management] -->
## Resource Management

The `Apideck` class implements the context manager protocol and registers a finalizer function to close the underlying sync and async HTTPX clients it uses under the hood. This will close HTTP connections, release memory and free up other resources held by the SDK. In short-lived Python programs and notebooks that make a few SDK method calls, resource management may not be a concern. However, in longer-lived programs, it is beneficial to create a single SDK instance via a [context manager][context-manager] and reuse it across the application.

[context-manager]: https://docs.python.org/3/reference/datamodel.html#context-managers

```python
from apideck_accounting_unify import Apideck
import os
def main():

    with Apideck(
        api_key=os.getenv("APIDECK_API_KEY", ""),
        consumer_id="test-consumer",
        app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX",
    ) as apideck:
        # Rest of application here...


# Or when using async:
async def amain():

    async with Apideck(
        api_key=os.getenv("APIDECK_API_KEY", ""),
        consumer_id="test-consumer",
        app_id="dSBdXd2H6Mqwfg0atXHXYcysLJE9qyn1VwBtXHX",
    ) as apideck:
        # Rest of application here...
```
<!-- End Resource Management [resource-management] -->

<!-- Start Debugging [debug] -->
## Debugging

You can setup your SDK to emit debug logs for SDK requests and responses.

You can pass your own logger class directly into your SDK.
```python
from apideck_accounting_unify import Apideck
import logging

logging.basicConfig(level=logging.DEBUG)
s = Apideck(debug_logger=logging.getLogger("apideck_accounting_unify"))
```

You can also enable a default debug logger by setting an environment variable `APIDECK_DEBUG` to true.
<!-- End Debugging [debug] -->

<!-- Placeholder for Future Speakeasy SDK Sections -->

# Development

## Maturity

This SDK is in beta, and there may be breaking changes between versions without a major version update. Therefore, we recommend pinning usage
to a specific package version. This way, you can install the same version each time without breaking changes unless you are intentionally
looking for the latest version.

## Contributions

While we value open-source contributions to this SDK, this library is generated programmatically. Any manual changes added to internal files will be overwritten on the next generation. 
We look forward to hearing your feedback. Feel free to open a PR or an issue with a proof of concept and we'll do our best to include it in a future release. 

### SDK Created by [Speakeasy](https://www.speakeasy.com/?utm_source=apideck-accounting-unify&utm_campaign=python)

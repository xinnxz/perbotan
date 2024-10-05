# fdy-scraping

`fdy-scraping` is a versatile HTTP client designed for making API requests with support for proxy configuration, debugging, and detailed error handling. It utilizes the [`got-scraping`](https://github.com/apify/got-scraping) library for HTTP operations.

## Installation

To use `fdy-scraping`, you need to install the `got-scraping` library. Run the following command to install it via npm:

```bash
npm install fdy-scraping
```

## Usage

### Importing the Client

Import `fdy-scraping` into your Node.js application:

```javascript
const fdy = require("fdy-scraping");
```

OR

```javascript
import fdy from "fdy-scraping";
```

### Creating a Client Instance

Create a new client instance with custom options:

```typescript
create(options?: FetchClientOptions, debug?: boolean): FdyFetchClient;
```

```javascript
const client = fdy.create(
  {
    headers: { Authorization: "Bearer your-token" },
    proxy: {
      ip: "127.0.0.1",
      port: 8080,
      protocol: "http",
      username: "username",
      password: "password",
    },
    baseUrl: "https://api.example.com",
  },
  true
); // Set debug mode to true
```

### Making HTTP Requests

You can use the client to make various types of HTTP requests:

#### Request

```typescript
request(url, method, body = undefined, headers = undefined, options = undefined)
```

```javascript
client
  .request("/endpoint", "POST", undefined, { Accept: "application/json" })
  .then((response) => {
    console.log(response.data); // Response data
  })
  .catch((error) => {
    console.error("Error:", error.message);
  });
```

#### GET Request

```typescript
get(url, headers = {}, options = {}, enableDebug = false)
```

```javascript
client
  .get("/endpoint", { Accept: "application/json" })
  .then((response) => {
    console.log(response.data); // Response data
  })
  .catch((error) => {
    console.error("Error:", error.message);
  });
```

#### POST Request

```typescript
post(url, body = undefined, headers = {}, options = {}, enableDebug = false)
```

```javascript
client
  .post("/endpoint", JSON.stringify({ key: "value" }), {
    "Content-Type": "application/json",
  })
  .then((response) => {
    console.log(response.data); // Response data
  })
  .catch((error) => {
    console.error("Error:", error.message);
  });
```

#### PUT Request

```typescript
put(url, body = undefined, headers = {}, options = {}, enableDebug = false)
```

```javascript
client
  .put("/endpoint", JSON.stringify({ key: "new-value" }), {
    "Content-Type": "application/json",
  })
  .then((response) => {
    console.log(response.data); // Response data
  })
  .catch((error) => {
    console.error("Error:", error.message);
  });
```

#### DELETE Request

```typescript
delete(url, headers = {}, options = {}, enableDebug = false)
```

```javascript
client
  .delete("/endpoint", { Accept: "application/json" })
  .then((response) => {
    console.log(response.data); // Response data
  })
  .catch((error) => {
    console.error("Error:", error.message);
  });
```

### Error Handling

`fdy-scraping` provides detailed error information through the `FdyFetchClientError` class. Errors include the status code, response data, and request configuration.

```javascript
client.get("/invalid-endpoint").catch((error) => {
  if (error instanceof fdy.FdyFetchClientError) {
    console.error("Custom Error Details:");
    console.error("Status:", error.status);
    console.error("Response:", error.response);
    console.error("Config:", error.config);
  } else {
    console.error("General Error:", error.message);
  }
});
```

## Configuration Options

### FetchClientOptions

- `headers`: Optional object containing default headers for requests.
- `proxy`: Optional object for proxy configuration.
  - `ip`: IP address of the proxy server.
  - `port`: Port of the proxy server.
  - `protocol`: Protocol used by the proxy (`http` or `https`).
  - `username`: Optional username for proxy authentication.
  - `password`: Optional password for proxy authentication.
- `baseUrl`: Optional base URL for requests.

### Debug Mode

Debug mode can be enabled by passing `true` as the second argument to `FdyFetchClient.create`. When enabled, additional error information will be logged to the console.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```

Feel free to adjust the paths, options, or methods according to your actual implementation and package setup.
```

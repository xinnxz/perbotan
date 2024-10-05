/**
 * Asynchronously imports the got-scraping module and returns the gotScraping object
 * @returns {Promise<import("got-scraping").gotScraping>} - Promise resolving to the gotScraping instance
 */
async function fdyHttpClient() {
  let importedClient; // Declare a variable to hold the imported client
  importedClient ??= (await import("got-scraping")).gotScraping; // Import and assign if undefined
  return importedClient; // Return the imported client
}

/**
 * Custom error class used for handling fetch client errors
 */
class FdyFetchClientError extends Error {
  /**
   * Constructs a new FdyFetchClientError instance
   * @param {string} message - Error message to be displayed
   * @param {object} response - Response data from the server
   * @param {object} request - Response data from the server
   */
  constructor(message, response, request) {
    super(message); // Initialize the base Error class with the message
    this.name = "FetchClientError"; // Set a specific error name
    this.response = response; // Store the server response in the error
    this.request = request; // Store the request data in the error
  }
}

/**
 * Class to handle HTTP requests with various methods
 */
class FdyFetchClient {
  #debugMode = false; // Private field to toggle debug mode

  /**
   * Constructor for the FdyFetchClient class
   * @param {FetchClientOptions} config - Configuration options for the client
   * @param {boolean} debugMode - Flag to enable or disable debugging
   */
  constructor(config = {}, debugMode = false) {
    this.defaults = { headers: config.headers || {} }; // Initialize default headers
    this.#debugMode = debugMode; // Set the debug mode
    this.proxy = config.proxy || null; // Initialize proxy settings
    this.baseUrl = config.baseUrl || null; // Set the base URL for requests
  }

  /**
   * Private helper function to perform HTTP requests
   * @param {string} url - The URL endpoint for the request
   * @param {string} method - The HTTP method (GET, POST, etc.)
   * @param {string|undefined} body - Optional request body
   * @param {object} headers - Request headers
   * @param {object} options - Additional options for the request
   * @returns {Promise<{ data: object, status: number, headers: object, ok: boolean, request: { config: object, headers: object } }>}
   */
  async #privateRequestHandler(
    url,
    method,
    body = undefined,
    headers = {},
    options = {}
  ) {
    try {
      // Get the proxy URL if configured
      const proxyUrl = this.#buildProxyUrl(this.proxy);
      // Import the got-scraping client
      const httpClient = await fdyHttpClient();
      // Extend the HTTP client with specific options
      const customizedClient = httpClient.extend({ responseType: "text" });
      // Make the HTTP request
      const response = await customizedClient({
        url: this.baseUrl ? this.baseUrl + url : url, // Use base URL if present
        body, // Set request body
        headers: { ...this.defaults.headers, ...headers }, // Merge default and custom headers
        proxyUrl, // Set proxy URL if available
        method, // Set HTTP method
        ...options, // Include additional options
      });

      // If the response indicates an error, throw a custom error
      if (!response?.ok) {
        const errorBody = response?.body; // Capture the error response body

        // Throw a custom error with detailed information
        throw new FdyFetchClientError(
          `Request failed with status code: ${response?.statusCode}`, // Error message
          this.#canBeParsed(errorBody)
            ? {
                data: JSON.parse(errorBody),
                status: response?.statusCode,
                headers: response?.headers,
                config: {
                  method,
                  url,
                },
              } // Parsed JSON data
              : {
                data: errorBody,
                status: response?.statusCode,
                headers: response?.headers,
                config: {
                  method,
                  url,
                },
              }, // Raw body text if not JSON
            {
              headers: { ...this.defaults.headers, ...headers },
              config: {
                method,
                url,
              },
            } // Request configuration

        );
      }

      // Return the response data in a structured format
      return {
        data: this.#canBeParsed(response?.body)
          ? JSON.parse(response?.body) // Parse JSON data if possible
          : response?.body, // Raw body if not JSON
        status: response?.status, // HTTP status code
        headers: response?.headers, // Response headers
        ok: response?.ok, // Success flag
        request: {
          config: response?.request, // Request configuration
          headers: { ...this.defaults.headers, ...headers }, // Combined headers
        },
      };
    } catch (error) {
      // If debugging is enabled, log detailed error information
      if (this.#debugMode) {
        console.error(`Request failed:
          URL: ${error?.url}
          Method: ${error?.method}
          Status: ${error?.status}
          Response Text: ${error?.responseText}
          Error: ${error?.message}`);
      }
      // Re-throw the error to allow further handling
      throw error;
    }
  }

  /**
   * Static method to create a new instance of the client
   * @param {FetchClientOptions} config - Configuration options for the client
   * @param {boolean} debugMode - Flag to enable or disable debugging
   * @returns {FdyFetchClient} - The newly created FdyFetchClient instance
   */
  create(config = {}, debugMode = false) {
    return new FdyFetchClient(config, debugMode);
  }

  /**
   * Makes a generic HTTP request
   * @param {string} url - The URL endpoint
   * @param {string} method - HTTP method to use (GET, POST, etc.)
   * @param {string|undefined} body - Optional body for the request
   * @param {object|undefined} headers - Optional headers for the request
   * @param {object|undefined} options - Additional options for the request
   * @returns {Promise<any>} - The response data from the request
   */
  request(
    url,
    method,
    body = undefined,
    headers = undefined,
    options = undefined
  ) {
    return this.#privateRequestHandler(url, method, body, headers, options);
  }

  /**
   * Makes an HTTP GET request
   * @param {string} url - The URL endpoint
   * @param {object} headers - Request headers
   * @param {object} options - Additional options
   * @param {boolean} enableDebug - Flag to enable debugging
   * @returns {Promise<any>} - The response data from the request
   */
  get(url, headers = {}, options = {}, enableDebug = false) {
    this.#debugMode = enableDebug; // Set debug mode if specified
    return this.#privateRequestHandler(url, "GET", undefined, headers, options);
  }

  /**
   * Makes an HTTP POST request
   * @param {string} url - The URL endpoint
   * @param {string|undefined} body - Optional request body
   * @param {object} headers - Request headers
   * @param {object} options - Additional options
   * @param {boolean} enableDebug - Flag to enable debugging
   * @returns {Promise<any>} - The response data from the request
   */
  post(url, body = undefined, headers = {}, options = {}, enableDebug = false) {
    this.#debugMode = enableDebug; // Set debug mode if specified
    return this.#privateRequestHandler(url, "POST", body, headers, options);
  }

  /**
   * Makes an HTTP PUT request
   * @param {string} url - The URL endpoint
   * @param {string|undefined} body - Optional request body
   * @param {object} headers - Request headers
   * @param {object} options - Additional options
   * @param {boolean} enableDebug - Flag to enable debugging
   * @returns {Promise<any>} - The response data from the request
   */
  put(url, body = undefined, headers = {}, options = {}, enableDebug = false) {
    this.#debugMode = enableDebug; // Set debug mode if specified
    return this.#privateRequestHandler(url, "PUT", body, headers, options);
  }

  /**
   * Makes an HTTP DELETE request
   * @param {string} url - The URL endpoint
   * @param {object} headers - Request headers
   * @param {object} options - Additional options
   * @param {boolean} enableDebug - Flag to enable debugging
   * @returns {Promise<any>} - The response data from the request
   */
  delete(url, headers = {}, options = {}, enableDebug = false) {
    this.#debugMode = enableDebug; // Set debug mode if specified
    return this.#privateRequestHandler(
      url,
      "DELETE",
      undefined,
      headers,
      options
    );
  }

  /**
   * Constructs the proxy URL from given proxy settings
   * @param {object} proxy - Proxy configuration
   * @returns {string|undefined} - The constructed proxy URL or undefined if proxy is not configured
   */
  #buildProxyUrl(proxy) {
    let constructedUrl = undefined;
    if (proxy?.ip && proxy?.port && proxy?.protocol) {
      if (!proxy?.password && !proxy?.username) {
        constructedUrl = `${proxy.protocol}://${proxy.ip}:${proxy.port}`;
      } else {
        constructedUrl = `${proxy.protocol}://${proxy.username}:${proxy.password}@${proxy.ip}:${proxy.port}`;
      }
    }
    return constructedUrl;
  }

  /**
   * Checks if the given body can be parsed as JSON
   * @param {string} body - The body to be checked
   * @returns {boolean} - True if the body can be parsed as JSON, otherwise false
   */
  #canBeParsed(body) {
    try {
      JSON.parse(body);
      return true;
    } catch (error) {
      return false;
    }
  }
}

// Create an instance of FdyFetchClient and export it
const fdy = new FdyFetchClient({}, false);
module.exports = fdy;
module.exports.FdyFetchClientError = FdyFetchClientError;

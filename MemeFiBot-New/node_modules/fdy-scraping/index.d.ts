// index.d.ts

import { gotScraping, ExtendedOptionsOfTextResponseBody } from "got-scraping";

declare module "fdyFetchClient" {
  /**
   * Function that initializes and returns the gotScraping instance.
   * @returns {Promise<gotScraping>}
   */
  export function fdyHttpClient(): Promise<gotScraping>;

  /**
   * Custom error class for FdyFetchClient errors.
   */
  export class FdyFetchClientError extends Error {
    name: string;
    status: number;
    response: any;
    config: {
      method: string;
      url: string;
      headers: { [key: string]: string };
    };

    constructor(message: string, status: number, response: any, config: object);
  }

  /**
   * Options for the Fetch Client.
   */
  export interface FetchClientOptions {
    headers?: { [key: string]: string };
    proxy?: {
      ip: string;
      port: number;
      protocol: "http" | "https";
      username?: string;
      password?: string;
    };
    baseUrl?: string;
  }

  /**
   * Response structure returned by the request helper.
   */
  export interface FdyResponse {
    data: object;
    status: number;
    headers: object;
    ok: boolean;
    url?: string;
    request: {
      config: object;
      headers: { [key: string]: string };
    };
  }

  /**
   * FdyFetchClient class for making API requests.
   */
  export class FdyFetchClient {
    #debug: boolean;
    defaults: { headers: { [key: string]: string } };
    proxy: FetchClientOptions["proxy"] | null;
    baseUrl: string | null;

    constructor(options?: FetchClientOptions, debug?: boolean);

    /**
     * Helper method for making HTTP requests.
     * @param url The request URL.
     * @param method The HTTP method (GET, POST, PUT, DELETE, etc.).
     * @param body Optional request body.
     * @param headers Optional headers for the request.
     * @param options Optional additional request options.
     * @returns {Promise<FdyResponse>}
     */
    #requestHelper(
      url: string,
      method: "GET" | "POST" | "PUT" | "DELETE" | string,
      body?: string,
      headers?: { [key: string]: string },
      options?: ExtendedOptionsOfTextResponseBody
    ): Promise<FdyResponse>;

    /**
     * Creates a new instance of the FdyFetchClient.
     * @param options Client options.
     * @param debug Enable or disable debugging.
     */
    create(options?: FetchClientOptions, debug?: boolean): FdyFetchClient;

    /**
     * Make a generic HTTP request.
     * @param url The request URL.
     * @param method The HTTP method (GET, POST, etc.).
     * @param body Optional request body.
     * @param headers Optional headers.
     * @param options Optional additional options.
     * @returns {Promise<FdyResponse>}
     */
    request(
      url: string,
      method: string,
      body?: string,
      headers?: { [key: string]: string },
      options?: ExtendedOptionsOfTextResponseBody
    ): Promise<FdyResponse>;

    /**
     * Make a GET request.
     * @param url The request URL.
     * @param headers Optional headers for the request.
     * @param options Optional additional options.
     * @param debug Enable or disable debugging.
     * @returns {Promise<FdyResponse>}
     */
    get(
      url: string,
      headers?: { [key: string]: string },
      options?: ExtendedOptionsOfTextResponseBody,
      debug?: boolean
    ): Promise<FdyResponse>;

    /**
     * Make a POST request.
     * @param url The request URL.
     * @param body The request body.
     * @param headers Optional headers for the request.
     * @param options Optional additional options.
     * @param debug Enable or disable debugging.
     * @returns {Promise<FdyResponse>}
     */
    post(
      url: string,
      body?: string,
      headers?: { [key: string]: string },
      options?: ExtendedOptionsOfTextResponseBody,
      debug?: boolean
    ): Promise<FdyResponse>;

    /**
     * Make a PUT request.
     * @param url The request URL.
     * @param body The request body.
     * @param headers Optional headers for the request.
     * @param options Optional additional options.
     * @param debug Enable or disable debugging.
     * @returns {Promise<FdyResponse>}
     */
    put(
      url: string,
      body?: string,
      headers?: { [key: string]: string },
      options?: ExtendedOptionsOfTextResponseBody,
      debug?: boolean
    ): Promise<FdyResponse>;

    /**
     * Make a DELETE request.
     * @param url The request URL.
     * @param headers Optional headers for the request.
     * @param options Optional additional options.
     * @param debug Enable or disable debugging.
     * @returns {Promise<FdyResponse>}
     */
    delete(
      url: string,
      headers?: { [key: string]: string },
      options?: ExtendedOptionsOfTextResponseBody,
      debug?: boolean
    ): Promise<FdyResponse>;
  }

  /**
   * Exported instance of FdyFetchClient.
   */
  const fdy: FdyFetchClient;
  export default fdy;
}

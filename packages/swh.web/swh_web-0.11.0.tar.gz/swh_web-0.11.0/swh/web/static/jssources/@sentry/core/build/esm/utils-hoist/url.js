/**
 * Parses string to a URL object
 *
 * @param url - The URL to parse
 * @returns The parsed URL object or undefined if the URL is invalid
 */
function parseStringToURL(url, base) {
  try {
    // Use `canParse` to short-circuit the URL constructor if it's not a valid URL
    // This is faster than trying to construct the URL and catching the error
    // Node 20+, Chrome 120+, Firefox 115+, Safari 17+
    if ('canParse' in URL && !(URL ).canParse(url, base)) {
      return undefined;
    }

    return new URL(url, base);
  } catch {
    // empty body
  }

  return undefined;
}

/**
 * Parses string form of URL into an object
 * // borrowed from https://tools.ietf.org/html/rfc3986#appendix-B
 * // intentionally using regex and not <a/> href parsing trick because React Native and other
 * // environments where DOM might not be available
 * @returns parsed URL object
 */
function parseUrl(url) {
  if (!url) {
    return {};
  }

  const match = url.match(/^(([^:/?#]+):)?(\/\/([^/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?$/);

  if (!match) {
    return {};
  }

  // coerce to undefined values to empty string so we don't get 'undefined'
  const query = match[6] || '';
  const fragment = match[8] || '';
  return {
    host: match[4],
    path: match[5],
    protocol: match[2],
    search: query,
    hash: fragment,
    relative: match[5] + query + fragment, // everything minus origin
  };
}

/**
 * Strip the query string and fragment off of a given URL or path (if present)
 *
 * @param urlPath Full URL or path, including possible query string and/or fragment
 * @returns URL or path without query string or fragment
 */
function stripUrlQueryAndFragment(urlPath) {
  return (urlPath.split(/[?#]/, 1) )[0];
}

/**
 * Takes a URL object and returns a sanitized string which is safe to use as span name
 * see: https://develop.sentry.dev/sdk/data-handling/#structuring-data
 */
function getSanitizedUrlString(url) {
  const { protocol, host, path } = url;

  const filteredHost =
    host
      // Always filter out authority
      ?.replace(/^.*@/, '[filtered]:[filtered]@')
      // Don't show standard :80 (http) and :443 (https) ports to reduce the noise
      // TODO: Use new URL global if it exists
      .replace(/(:80)$/, '')
      .replace(/(:443)$/, '') || '';

  return `${protocol ? `${protocol}://` : ''}${filteredHost}${path}`;
}

export { getSanitizedUrlString, parseStringToURL, parseUrl, stripUrlQueryAndFragment };
//# sourceMappingURL=url.js.map

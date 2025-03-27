"""
Elasticsearch client for accessing NixOS resources.
"""

import os
import logging
from typing import Dict, Any

# Get logger
logger = logging.getLogger("nixmcp")

# Import SimpleCache
from nixmcp.cache.simple_cache import SimpleCache


class ElasticsearchClient:
    """Enhanced client for accessing NixOS Elasticsearch API."""

    def __init__(self):
        """Initialize the Elasticsearch client with caching."""
        # Elasticsearch endpoints - use the correct endpoints for NixOS search
        # Use the real NixOS search URLs
        self.es_base_url = os.environ.get("ELASTICSEARCH_URL", "https://search.nixos.org/backend")

        # Authentication
        self.es_user = os.environ.get("ELASTICSEARCH_USER", "aWVSALXpZv")
        self.es_password = os.environ.get("ELASTICSEARCH_PASSWORD", "X8gPHnzL52wFEekuxsfQ9cSh")
        self.es_auth = (self.es_user, self.es_password)

        # Available channels - updated with proper index names from nixos-search
        self.available_channels = {
            "unstable": "latest-42-nixos-unstable",
            "24.11": "latest-42-nixos-24.11",  # NixOS 24.11 stable release
            "stable": "latest-42-nixos-24.11",  # Alias for current stable release
        }

        # Default to unstable channel
        self.set_channel("unstable")

        # Initialize cache
        self.cache = SimpleCache(max_size=500, ttl=600)  # 10 minutes TTL

        # Request timeout settings
        self.connect_timeout = 3.0  # seconds
        self.read_timeout = 10.0  # seconds

        # Retry settings
        self.max_retries = 3
        self.retry_delay = 1.0  # seconds

        logger.info("Elasticsearch client initialized with caching")

    def safe_elasticsearch_query(self, endpoint: str, query_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an Elasticsearch query with robust error handling and retries."""
        # Import here to avoid circular imports
        from nixmcp.utils.helpers import make_http_request

        # Use the shared HTTP utility function
        result = make_http_request(
            url=endpoint,
            method="POST",
            json_data=query_data,
            auth=self.es_auth,
            timeout=(self.connect_timeout, self.read_timeout),
            max_retries=self.max_retries,
            retry_delay=self.retry_delay,
            cache=self.cache,
        )

        # Handle Elasticsearch-specific error cases
        if "error" in result:
            if "details" in result and isinstance(result["details"], dict):
                # Extract Elasticsearch error details if available
                es_error = result["details"].get("error", {})
                if isinstance(es_error, dict) and "reason" in es_error:
                    result["error"] = f"Elasticsearch error: {es_error['reason']}"

            # Add prefix to generic errors
            elif result["error"] == "Request failed with status 400":
                result["error"] = "Invalid query syntax"

        return result

    def search_packages(self, query: str, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """
        Search for NixOS packages with enhanced query handling and field boosting.

        Args:
            query: Search term
            limit: Maximum number of results to return
            offset: Offset for pagination

        Returns:
            Dict containing search results and metadata
        """
        # Check if query contains wildcards
        if "*" in query:
            # Use wildcard query for explicit wildcard searches
            logger.info(f"Using wildcard query for package search: {query}")

            # Handle special case for queries like *term*
            if query.startswith("*") and query.endswith("*") and query.count("*") == 2:
                term = query.strip("*")
                logger.info(f"Optimizing *term* query to search for: {term}")

                request_data = {
                    "from": offset,
                    "size": limit,
                    "query": {
                        "bool": {
                            "should": [
                                # Contains match with high boost
                                {
                                    "wildcard": {
                                        "package_attr_name": {
                                            "value": f"*{term}*",
                                            "boost": 9,
                                        }
                                    }
                                },
                                {
                                    "wildcard": {
                                        "package_pname": {
                                            "value": f"*{term}*",
                                            "boost": 7,
                                        }
                                    }
                                },
                                {
                                    "match": {
                                        "package_description": {
                                            "query": term,
                                            "boost": 3,
                                        }
                                    }
                                },
                                {"match": {"package_programs": {"query": term, "boost": 6}}},
                            ],
                            "minimum_should_match": 1,
                        }
                    },
                }
            else:
                # Standard wildcard query
                request_data = {
                    "from": offset,
                    "size": limit,
                    "query": {
                        "query_string": {
                            "query": query,
                            "fields": [
                                "package_attr_name^9",
                                "package_pname^7",
                                "package_description^3",
                                "package_programs^6",
                            ],
                            "analyze_wildcard": True,
                        }
                    },
                }
        else:
            # For non-wildcard searches, use a more refined approach with field boosting
            request_data = {
                "from": offset,
                "size": limit,
                "query": {
                    "bool": {
                        "should": [
                            # Exact match with highest boost
                            {"term": {"package_attr_name": {"value": query, "boost": 10}}},
                            {"term": {"package_pname": {"value": query, "boost": 8}}},
                            # Prefix match (starts with)
                            {"prefix": {"package_attr_name": {"value": query, "boost": 7}}},
                            {"prefix": {"package_pname": {"value": query, "boost": 6}}},
                            # Contains match
                            {
                                "wildcard": {
                                    "package_attr_name": {
                                        "value": f"*{query}*",
                                        "boost": 5,
                                    }
                                }
                            },
                            {"wildcard": {"package_pname": {"value": f"*{query}*", "boost": 4}}},
                            # Full-text search in description fields
                            {"match": {"package_description": {"query": query, "boost": 3}}},
                            {
                                "match": {
                                    "package_longDescription": {
                                        "query": query,
                                        "boost": 1,
                                    }
                                }
                            },
                            # Program search
                            {"match": {"package_programs": {"query": query, "boost": 6}}},
                        ],
                        "minimum_should_match": 1,
                    }
                },
            }

        # Execute the query
        data = self.safe_elasticsearch_query(self.es_packages_url, request_data)

        # Check for errors
        if "error" in data:
            return data

        # Process the response
        hits = data.get("hits", {}).get("hits", [])
        total = data.get("hits", {}).get("total", {}).get("value", 0)

        packages = []
        for hit in hits:
            source = hit.get("_source", {})
            packages.append(
                {
                    "name": source.get("package_attr_name", ""),
                    "pname": source.get("package_pname", ""),
                    "version": source.get("package_version", source.get("package_pversion", "")),
                    "description": source.get("package_description", ""),
                    "channel": source.get("package_channel", ""),
                    "score": hit.get("_score", 0),
                    "programs": source.get("package_programs", []),
                }
            )

        return {
            "count": total,
            "packages": packages,
        }

    def search_options(
        self, query: str, limit: int = 50, offset: int = 0, additional_terms: list = None, quoted_terms: list = None
    ) -> Dict[str, Any]:
        """
        Search for NixOS options with enhanced multi-word query handling.

        Args:
            query: Search term (main query or hierarchical path)
            limit: Maximum number of results to return
            offset: Offset for pagination
            additional_terms: Additional terms to filter results
            quoted_terms: Phrases that should be matched exactly

        Returns:
            Dict containing search results and metadata
        """
        # Initialize optional parameters
        additional_terms = additional_terms or []
        quoted_terms = quoted_terms or []

        logger.info(
            f"Search options with: query='{query}', additional_terms={additional_terms}, "
            f"quoted_terms={quoted_terms}, limit={limit}"
        )
        # Check if query contains wildcards
        if "*" in query:
            # Build a query with wildcards
            wildcard_value = query
            logger.info(f"Using wildcard query for option search: {wildcard_value}")

            search_query = {
                "bool": {
                    "must": [
                        {
                            "wildcard": {
                                "option_name": {
                                    "value": wildcard_value,
                                    "case_insensitive": True,
                                }
                            }
                        }
                    ],
                    "filter": [{"term": {"type": {"value": "option"}}}],
                }
            }

        else:
            # Check if the query contains dots, which likely indicates a hierarchical path
            if "." in query:
                # For hierarchical paths like services.postgresql, add a wildcard
                logger.info(f"Detected hierarchical path in option search: {query}")

                # Add wildcards for hierarchical paths by default
                if not query.endswith("*"):
                    hierarchical_query = f"{query}*"
                    logger.info(f"Adding wildcard to hierarchical path: {hierarchical_query}")
                else:
                    hierarchical_query = query

                # Special handling for service modules
                if query.startswith("services."):
                    logger.info(f"Special handling for service module path: {query}")
                    service_name = query.split(".", 2)[1] if len(query.split(".", 2)) > 1 else ""

                    # Prepare additional filters for multi-word queries
                    additional_shoulds = []

                    # Add filters for additional terms if provided
                    if additional_terms:
                        for term in additional_terms:
                            # Look for the term in description field with good boost
                            additional_shoulds.append(
                                {
                                    "match": {
                                        "option_description": {
                                            "query": term,
                                            "boost": 4.0,
                                        }
                                    }
                                }
                            )

                            # Also look for term in option name (for combined path+term matches)
                            additional_shoulds.append(
                                {
                                    "wildcard": {
                                        "option_name": {
                                            "value": f"*{term}*",
                                            "case_insensitive": True,
                                            "boost": 3.0,
                                        }
                                    }
                                }
                            )

                    # Add filters for quoted phrases if provided
                    if quoted_terms:
                        for phrase in quoted_terms:
                            additional_shoulds.append(
                                {
                                    "match_phrase": {
                                        "option_description": {
                                            "query": phrase,
                                            "boost": 6.0,
                                        }
                                    }
                                }
                            )

                    # Generate base shoulds which are always included
                    base_shoulds = [
                        # Exact prefix match for the hierarchical path
                        {
                            "prefix": {
                                "option_name": {
                                    "value": query,
                                    "boost": 10.0,
                                }
                            }
                        },
                        # Wildcard match
                        {
                            "wildcard": {
                                "option_name": {
                                    "value": hierarchical_query,
                                    "case_insensitive": True,
                                    "boost": 8.0,
                                }
                            }
                        },
                        # Match against specific service name in description
                        {
                            "match": {
                                "option_description": {
                                    "query": service_name,
                                    "boost": 2.0,
                                }
                            }
                        },
                    ]

                    # Combine base shoulds with additional terms
                    all_shoulds = base_shoulds + additional_shoulds

                    # Build a more specific query for service modules
                    search_query = {
                        "bool": {
                            "filter": [{"term": {"type": {"value": "option"}}}],
                            "must": [
                                {
                                    "bool": {
                                        "should": all_shoulds,
                                        "minimum_should_match": 1,
                                    }
                                }
                            ],
                        }
                    }
                else:
                    # Prepare additional filters for multi-word queries
                    additional_queries = []

                    # Add filters for additional terms if provided
                    if additional_terms:
                        for term in additional_terms:
                            # Look for the term in description field with good boost
                            additional_queries.append(
                                {
                                    "match": {
                                        "option_description": {
                                            "query": term,
                                            "boost": 4.0,
                                        }
                                    }
                                }
                            )

                    # Add filters for quoted phrases if provided
                    if quoted_terms:
                        for phrase in quoted_terms:
                            additional_queries.append(
                                {
                                    "match_phrase": {
                                        "option_description": {
                                            "query": phrase,
                                            "boost": 6.0,
                                        }
                                    }
                                }
                            )

                    # Generate base queries which are always included
                    base_queries = [
                        {
                            "multi_match": {
                                "type": "cross_fields",
                                "query": query,
                                "analyzer": "whitespace",
                                "auto_generate_synonyms_phrase_query": False,
                                "operator": "and",
                                "_name": f"multi_match_{query}",
                                "fields": [
                                    "option_name^6",
                                    "option_name.*^3.6",
                                    "option_description^1",
                                    "option_description.*^0.6",
                                ],
                            }
                        },
                        {
                            "wildcard": {
                                "option_name": {
                                    "value": hierarchical_query,
                                    "case_insensitive": True,
                                }
                            }
                        },
                    ]

                    # Combine base queries with additional terms
                    all_queries = base_queries + additional_queries

                    # Build a more sophisticated query for other hierarchical paths
                    search_query = {
                        "bool": {
                            "filter": [
                                {
                                    "term": {
                                        "type": {
                                            "value": "option",
                                            "_name": "filter_options",
                                        }
                                    }
                                }
                            ],
                            "must": [
                                {
                                    "dis_max": {
                                        "tie_breaker": 0.7,
                                        "queries": all_queries,
                                    }
                                }
                            ],
                        }
                    }
            else:
                # Prepare additional filters for multi-word queries
                additional_queries = []

                # Add filters for additional terms if provided
                if additional_terms:
                    for term in additional_terms:
                        # Look for the term in description field with good boost
                        additional_queries.append(
                            {
                                "match": {
                                    "option_description": {
                                        "query": term,
                                        "boost": 4.0,
                                    }
                                }
                            }
                        )

                # Add filters for quoted phrases if provided
                if quoted_terms:
                    for phrase in quoted_terms:
                        additional_queries.append(
                            {
                                "match_phrase": {
                                    "option_description": {
                                        "query": phrase,
                                        "boost": 6.0,
                                    }
                                }
                            }
                        )

                # Generate base queries which are always included
                base_queries = [
                    {
                        "multi_match": {
                            "type": "cross_fields",
                            "query": query,
                            "analyzer": "whitespace",
                            "auto_generate_synonyms_phrase_query": False,
                            "operator": "and",
                            "_name": f"multi_match_{query}",
                            "fields": [
                                "option_name^6",
                                "option_name.*^3.6",
                                "option_description^1",
                                "option_description.*^0.6",
                            ],
                        }
                    },
                    {
                        "wildcard": {
                            "option_name": {
                                "value": f"*{query}*",
                                "case_insensitive": True,
                            }
                        }
                    },
                ]

                # Combine base queries with additional terms
                all_queries = base_queries + additional_queries

                # For regular term searches, use the NixOS search format with additional terms support
                search_query = {
                    "bool": {
                        "filter": [
                            {
                                "term": {
                                    "type": {
                                        "value": "option",
                                        "_name": "filter_options",
                                    }
                                }
                            }
                        ],
                        "must": [
                            {
                                "dis_max": {
                                    "tie_breaker": 0.7,
                                    "queries": all_queries,
                                }
                            }
                        ],
                    }
                }

        # Build the full request
        request_data = {
            "from": offset,
            "size": limit,
            "sort": [{"_score": "desc", "option_name": "desc"}],
            "aggs": {"all": {"global": {}, "aggregations": {}}},
            "query": search_query,
        }

        # Execute the query
        data = self.safe_elasticsearch_query(self.es_options_url, request_data)

        # Check for errors
        if "error" in data:
            return data

        # Process the response
        hits = data.get("hits", {}).get("hits", [])
        total = data.get("hits", {}).get("total", {}).get("value", 0)

        options = []
        for hit in hits:
            source = hit.get("_source", {})
            # Check if this is actually an option (for safety)
            if source.get("type") == "option":
                options.append(
                    {
                        "name": source.get("option_name", ""),
                        "description": source.get("option_description", ""),
                        "type": source.get("option_type", ""),
                        "default": source.get("option_default", ""),
                        "score": hit.get("_score", 0),
                    }
                )

        return {
            "count": total,
            "options": options,
        }

    def search_programs(self, program: str, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """
        Search for packages that provide specific programs.

        Args:
            program: Program name to search for
            limit: Maximum number of results to return
            offset: Offset for pagination

        Returns:
            Dict containing search results and metadata
        """
        logger.info(f"Searching for packages providing program: {program}")

        # Check if program contains wildcards
        if "*" in program:
            request_data = {
                "from": offset,
                "size": limit,
                "query": {"wildcard": {"package_programs": {"value": program}}},
            }
        else:
            request_data = {
                "from": offset,
                "size": limit,
                "query": {
                    "bool": {
                        "should": [
                            {"term": {"package_programs": {"value": program, "boost": 10}}},
                            {"prefix": {"package_programs": {"value": program, "boost": 5}}},
                            {
                                "wildcard": {
                                    "package_programs": {
                                        "value": f"*{program}*",
                                        "boost": 3,
                                    }
                                }
                            },
                        ],
                        "minimum_should_match": 1,
                    }
                },
            }

        # Execute the query
        data = self.safe_elasticsearch_query(self.es_packages_url, request_data)

        # Check for errors
        if "error" in data:
            return data

        # Process the response
        hits = data.get("hits", {}).get("hits", [])
        total = data.get("hits", {}).get("total", {}).get("value", 0)

        packages = []
        for hit in hits:
            source = hit.get("_source", {})
            programs = source.get("package_programs", [])

            # Filter to only include matching programs in the result
            matching_programs = []
            if isinstance(programs, list):
                if "*" in program:
                    # For wildcard searches, use simple string matching
                    wild_pattern = program.replace("*", "")
                    matching_programs = [p for p in programs if wild_pattern in p]
                else:
                    # For exact searches, look for exact/partial matches
                    matching_programs = [p for p in programs if program == p or program in p]

            packages.append(
                {
                    "name": source.get("package_attr_name", ""),
                    "version": source.get("package_version", source.get("package_pversion", "")),
                    "description": source.get("package_description", ""),
                    "programs": matching_programs,
                    "all_programs": programs,
                    "score": hit.get("_score", 0),
                }
            )

        return {
            "count": total,
            "packages": packages,
        }

    def search_packages_with_version(
        self, query: str, version_pattern: str, limit: int = 50, offset: int = 0
    ) -> Dict[str, Any]:
        """
        Search for packages with a specific version pattern.

        Args:
            query: Package search term
            version_pattern: Version pattern to filter by (e.g., "1.*")
            limit: Maximum number of results to return
            offset: Offset for pagination

        Returns:
            Dict containing search results and metadata
        """
        logger.info(f"Searching for packages matching '{query}' with version '{version_pattern}'")

        request_data = {
            "from": offset,
            "size": limit,
            "query": {
                "bool": {
                    "must": [
                        # Basic package search
                        {
                            "bool": {
                                "should": [
                                    {
                                        "term": {
                                            "package_attr_name": {
                                                "value": query,
                                                "boost": 10,
                                            }
                                        }
                                    },
                                    {
                                        "wildcard": {
                                            "package_attr_name": {
                                                "value": f"*{query}*",
                                                "boost": 5,
                                            }
                                        }
                                    },
                                    {
                                        "match": {
                                            "package_description": {
                                                "query": query,
                                                "boost": 2,
                                            }
                                        }
                                    },
                                ],
                                "minimum_should_match": 1,
                            }
                        },
                        # Version filter
                        {"wildcard": {"package_version": version_pattern}},
                    ]
                }
            },
        }

        # Execute the query
        data = self.safe_elasticsearch_query(self.es_packages_url, request_data)

        # Check for errors
        if "error" in data:
            return data

        # Process the response
        hits = data.get("hits", {}).get("hits", [])
        total = data.get("hits", {}).get("total", {}).get("value", 0)

        packages = []
        for hit in hits:
            source = hit.get("_source", {})
            packages.append(
                {
                    "name": source.get("package_attr_name", ""),
                    "version": source.get("package_version", source.get("package_pversion", "")),
                    "description": source.get("package_description", ""),
                    "channel": source.get("package_channel", ""),
                    "score": hit.get("_score", 0),
                }
            )

        return {
            "count": total,
            "packages": packages,
        }

    def advanced_query(self, index_type: str, query_string: str, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """
        Execute an advanced query using Elasticsearch's query string syntax.

        Args:
            index_type: Either "packages" or "options"
            query_string: Elasticsearch query string syntax
            limit: Maximum number of results to return
            offset: Offset for pagination

        Returns:
            Dict containing search results and metadata
        """
        logger.info(f"Executing advanced query on {index_type}: {query_string}")

        # Determine the endpoint
        if index_type.lower() == "options":
            endpoint = self.es_options_url
        else:
            endpoint = self.es_packages_url

        request_data = {
            "from": offset,
            "size": limit,
            "query": {"query_string": {"query": query_string, "default_operator": "AND"}},
        }

        # Execute the query
        return self.safe_elasticsearch_query(endpoint, request_data)

    def set_channel(self, channel: str) -> None:
        """
        Set the NixOS channel to use for queries.

        Args:
            channel: The channel name ('unstable', 'stable', '24.11', etc.)
        """
        # Valid channels are keys in self.available_channels
        valid_channels = set(self.available_channels.keys())

        if channel.lower() not in valid_channels:
            logger.warning(f"Unknown channel: {channel}, falling back to unstable")
            channel = "unstable"

        # Get the channel ID from the available_channels dict
        channel_id = self.available_channels.get(channel, self.available_channels["unstable"])
        logger.info(f"Setting channel to {channel} ({channel_id})")

        # Update the Elasticsearch URLs - use the correct NixOS API endpoints
        # Note: For options, we use the same index as packages, but filter by type
        self.es_packages_url = f"{self.es_base_url}/{channel_id}/_search"
        self.es_options_url = f"{self.es_base_url}/{channel_id}/_search"

    def get_package_stats(self, query: str = "*") -> Dict[str, Any]:
        """
        Get statistics about NixOS packages.

        Args:
            query: Optional query to filter packages

        Returns:
            Dict containing aggregation statistics
        """
        logger.info(f"Getting package statistics for query: {query}")

        request_data = {
            "size": 0,  # We only need aggregations, not actual hits
            "query": {"query_string": {"query": query}},
            "aggs": {
                "channels": {"terms": {"field": "package_channel", "size": 10}},
                "licenses": {"terms": {"field": "package_license", "size": 10}},
                "platforms": {"terms": {"field": "package_platforms", "size": 10}},
            },
        }

        # Execute the query
        return self.safe_elasticsearch_query(self.es_packages_url, request_data)

    def get_package(self, package_name: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific package.

        Args:
            package_name: Name of the package

        Returns:
            Dict containing package details
        """
        logger.info(f"Getting detailed information for package: {package_name}")

        # Build a query to find the exact package by name
        request_data = {
            "size": 1,  # We only need one result
            "query": {"bool": {"must": [{"term": {"package_attr_name": package_name}}]}},
        }

        # Execute the query
        data = self.safe_elasticsearch_query(self.es_packages_url, request_data)

        # Check for errors
        if "error" in data:
            return {"name": package_name, "error": data["error"], "found": False}

        # Process the response
        hits = data.get("hits", {}).get("hits", [])

        if not hits:
            logger.warning(f"Package {package_name} not found")
            return {"name": package_name, "error": "Package not found", "found": False}

        # Extract package details from the first hit
        source = hits[0].get("_source", {})

        # Return comprehensive package information
        return {
            "name": source.get("package_attr_name", package_name),
            "pname": source.get("package_pname", ""),
            "version": source.get("package_version", source.get("package_pversion", "")),
            "description": source.get("package_description", ""),
            "longDescription": source.get("package_longDescription", ""),
            "license": source.get("package_license", ""),
            "homepage": source.get("package_homepage", ""),
            "maintainers": source.get("package_maintainers", []),
            "platforms": source.get("package_platforms", []),
            "channel": source.get("package_channel", "nixos-unstable"),
            "position": source.get("package_position", ""),
            "outputs": source.get("package_outputs", []),
            "programs": source.get("package_programs", []),
            "found": True,
        }

    def get_option(self, option_name: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific NixOS option.

        Args:
            option_name: Name of the option

        Returns:
            Dict containing option details
        """
        logger.info(f"Getting detailed information for option: {option_name}")

        # Check if this is a service option path
        is_service_path = option_name.startswith("services.") if not option_name.startswith("*") else False
        if is_service_path:
            service_parts = option_name.split(".", 2)
            service_name = service_parts[1] if len(service_parts) > 1 else ""
            logger.info(f"Detected service module option: {service_name}")

        # Build a query to find the exact option by name
        request_data = {
            "size": 1,  # We only need one result
            "query": {
                "bool": {
                    "filter": [{"term": {"type": {"value": "option"}}}],
                    "must": [{"term": {"option_name": option_name}}],
                }
            },
            "_source": [
                "option_name",
                "option_description",
                "option_type",
                "option_default",
                "option_example",
                "option_declarations",
                "option_readOnly",
                "option_manual_url",
                "option_added_in",
                "option_deprecated_in",
            ],
        }

        # Execute the query
        data = self.safe_elasticsearch_query(self.es_options_url, request_data)

        # Check for errors
        if "error" in data:
            return {"name": option_name, "error": data["error"], "found": False}

        # Process the response
        hits = data.get("hits", {}).get("hits", [])

        if not hits:
            logger.warning(f"Option {option_name} not found with exact match, trying prefix search")

            # Try a prefix search for hierarchical paths
            request_data = {
                "size": 1,
                "query": {
                    "bool": {
                        "filter": [{"term": {"type": {"value": "option"}}}],
                        "must": [{"prefix": {"option_name": option_name}}],
                    }
                },
            }

            data = self.safe_elasticsearch_query(self.es_options_url, request_data)
            hits = data.get("hits", {}).get("hits", [])

            if not hits:
                logger.warning(f"Option {option_name} not found with prefix search")

                # For service paths, provide context about common pattern structure
                if is_service_path:
                    service_name = option_name.split(".", 2)[1] if len(option_name.split(".", 2)) > 1 else ""
                    return {
                        "name": option_name,
                        "error": (
                            f"Option not found. Try common patterns like services.{service_name}.enable or "
                            f"services.{service_name}.package"
                        ),
                        "found": False,
                        "is_service_path": True,
                        "service_name": service_name,
                    }

                return {
                    "name": option_name,
                    "error": "Option not found",
                    "found": False,
                }

        # Extract option details from the first hit
        source = hits[0].get("_source", {})

        # Get related options for service paths
        related_options = []
        if is_service_path:
            # Perform a second query to find related options
            service_path_parts = option_name.split(".")
            if len(service_path_parts) >= 2:
                service_prefix = ".".join(service_path_parts[:2])  # e.g., "services.postgresql"

                related_request = {
                    "size": 5,  # Get top 5 related options
                    "query": {
                        "bool": {
                            "filter": [{"term": {"type": {"value": "option"}}}],
                            "must": [{"prefix": {"option_name": f"{service_prefix}."}}],
                            "must_not": [{"term": {"option_name": option_name}}],  # Exclude the current option
                        }
                    },
                }

                related_data = self.safe_elasticsearch_query(self.es_options_url, related_request)
                related_hits = related_data.get("hits", {}).get("hits", [])

                for hit in related_hits:
                    rel_source = hit.get("_source", {})
                    related_options.append(
                        {
                            "name": rel_source.get("option_name", ""),
                            "description": rel_source.get("option_description", ""),
                            "type": rel_source.get("option_type", ""),
                        }
                    )

        # Return comprehensive option information
        result = {
            "name": source.get("option_name", option_name),
            "description": source.get("option_description", ""),
            "type": source.get("option_type", ""),
            "default": source.get("option_default", ""),
            "example": source.get("option_example", ""),
            "declarations": source.get("option_declarations", []),
            "readOnly": source.get("option_readOnly", False),
            "manual_url": source.get("option_manual_url", ""),
            "introduced_version": source.get("option_added_in", ""),
            "deprecated_version": source.get("option_deprecated_in", ""),
            "found": True,
        }

        # Add related options for service paths
        if is_service_path and related_options:
            result["related_options"] = related_options
            result["is_service_path"] = True
            result["service_name"] = option_name.split(".", 2)[1] if len(option_name.split(".", 2)) > 1 else ""

        return result

"""Example script demonstrating Fibery GraphQL client usage."""

from vineapp.fibery.graphql import get_fibery_client


def main():
    """List available database types in the Fibery space."""
    try:
        print("Getting Fibery client...")
        client = get_fibery_client()

        # Query to get schema information
        query = """
            query {
                __schema {
                    types {
                        name
                        fields {
                            name
                        }
                    }
                }
            }
        """

        print("\nExecuting GraphQL schema query...")
        response = client.execute(query)

        if "errors" in response:
            print("\nGraphQL Errors:")
            for error in response["errors"]:
                print(f"- {error.get('message', str(error))}")
            return

        if "data" not in response:
            print("\nUnexpected API response format")
            return

        # Filter for main Fibery database types
        # (excluding BackgroundJob and Operations types)
        types = response["data"]["__schema"]["types"]
        database_types = [
            t
            for t in types
            if (
                t["name"].startswith("Public")
                and t["fields"]
                and not any(
                    suffix in t["name"] for suffix in ["BackgroundJob", "Operations"]
                )
            )
        ]

        print("\nAvailable Fibery Databases:")
        print("-------------------------")
        for type_info in database_types:
            name = type_info["name"]
            # Remove 'Public' prefix for cleaner display
            display_name = name[6:] if name.startswith("Public") else name
            print(f"- {display_name}")

    except ValueError as e:
        print(f"\nConfiguration error: {e}")
        print(
            "Please ensure VINEAPP_FIBERY_URL, VINEAPP_FIBERY_SPACE, and VINEAPP_FIBERY_TOKEN are set."
        )
    except Exception as e:
        print(f"\nError querying Fibery API: {type(e).__name__}: {str(e)}")
        raise  # Re-raise to see full traceback during testing


if __name__ == "__main__":
    main()

"""Example script demonstrating Fibery GraphQL client usage."""

from vineapp.fibery.graphql import get_fibery_client
from vineapp.fibery.models import get_fibery_info


def main():
    """List available database types in the Fibery space."""

    print("Getting Fibery client...")
    space_name = "Ict Wetering Potlilium"
    client = get_fibery_client(space_name=space_name)
    info = get_fibery_info(space_name=space_name)

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
    space_prefix = info._get_type_space_name()
    database_types = [
        t
        for t in types
        if (
            t["name"].startswith(space_prefix)
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
        # Remove space name prefix for cleaner display
        display_name = (
            name[len(space_prefix) :] if name.startswith(space_prefix) else name
        )
        print(f"- {display_name}")


if __name__ == "__main__":
    main()

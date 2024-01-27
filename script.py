import csv
import pandas as pd

PLAN_DATA_INPUT = "./input/plans.csv"
GEO_DATA_INPUT = "./input/zips.csv"
MISSING_PLAN_INPUT = "./input/slcsp.csv"


def build_geo_to_slcsp() -> dict[tuple[str, int], int]:
    """
    Build lookup of (state, rate_area) to SLCSP rate.
    """
    plan_df = pd.read_csv(PLAN_DATA_INPUT)

    # Filter to only "Silver" level plans and drop unnecessary cols
    plan_df = plan_df.loc[plan_df["metal_level"] == "Silver"]
    plan_df = plan_df.drop(["plan_id", "metal_level"], axis=1)

    # Filter out rows for which (state, rate area) pair only has one value
    # Such (state, rate area) pairs cannot have a second-lowest rate
    group_counts = plan_df.groupby(["state", "rate_area"])["rate"].count()
    valid_groups = group_counts[group_counts > 1].index
    plan_df = plan_df.set_index(["state", "rate_area"]).loc[valid_groups].reset_index()

    # Utilize `nsmallest` pandas function to find second smallest rate
    result = (
        plan_df.groupby(["state", "rate_area"])["rate"]
        .nsmallest(2)
        .groupby(["state", "rate_area"])
        .last()
        .reset_index()
    )
    result["state_rate_area"] = list(zip(result["state"], result["rate_area"]))
    result.set_index("state_rate_area", inplace=True)
    return result["rate"].to_dict()


def build_zip_to_geo() -> dict[str, tuple[str, int]]:
    """
    Build lookup of zipcode -> (state, rate area).
    """
    df = pd.read_csv(GEO_DATA_INPUT, converters={"zipcode": str})
    df = df.drop(["county_code", "name"], axis=1)
    # Drop full-row duplicates
    df = df.drop_duplicates()
    # Drop zip codes in ambiguous (state, rate area)s
    df = df.drop_duplicates(subset=["zipcode"], keep=False)
    return (
        df.set_index("zipcode")[["state", "rate_area"]].apply(tuple, axis=1).to_dict()
    )


class SLCSPLookup:
    def __init__(self):
        self.geo_lookup = build_zip_to_geo()
        self.slcsp_lookup = build_geo_to_slcsp()

    def find_slcsp(self, zipcode: str) -> int:
        if zipcode in self.geo_lookup:
            state, rate_area = self.geo_lookup[zipcode]
            if (state, rate_area) in self.slcsp_lookup:
                return self.slcsp_lookup[(state, rate_area)]
        return None


def main():
    lookup = SLCSPLookup()

    with open(MISSING_PLAN_INPUT, "r") as input_file:
        reader = csv.DictReader(input_file)
        for row in reader:
            zipcode = row["zipcode"]
            slcsp = lookup.find_slcsp(zipcode)
            if slcsp:
                print(f"{zipcode},{slcsp:.2f}")
            else:
                print(f"{zipcode},")


if __name__ == "__main__":
    main()

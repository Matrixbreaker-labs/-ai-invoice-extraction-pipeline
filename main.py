import pandas as pd
from pydantic import BaseModel, Field
import requests
import statsmodels.api as sm


class EconomicIndicatorSchema(BaseModel):
    country: str
    year: int = Field(..., ge=2000, le=2030)
    gdp_usd: float = Field(..., gt=0)


def fetch_world_bank_gdp(
    country_codes=["USA", "GBR", "DEU"], start_year=2012, end_year=2024
):
    all_records = []
    print(
        "\n=================================================================="
    )
    print(
        "🚀 INITIALIZING: MACROECONOMIC DATA INGESTION & ANALYSIS PIPELINE"
    )
    print(
        "==================================================================\n"
    )

    # World Bank Official API v2 Endpoint
    base_url = "https://worldbank.org"

    # এপিআই ব্লক এড়াতে ব্রাউজার হেডার যুক্ত করা হলো
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        ),
        "Accept": "application/json",
    }

    for code in country_codes:
        url = f"{base_url}/{code}/indicator/NY.GDP.MKTP.CD?date={start_year}:{end_year}&format=json"
        print(f"[📡 API] Fetching live GDP data for {code}...")

        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            data_json = response.json()

            # রেসপন্স লিস্ট চেক করা এবং index 1 থেকে মূল ডেটা নেওয়া
            if isinstance(data_json, list) and len(data_json) > 1:
                records_list = data_json[1]
            else:
                print(f"[⚠️] Unexpected API response format for {code}")
                continue

            for entry in records_list:
                val = entry.get("value")
                if val is not None:
                    valid_item = EconomicIndicatorSchema(
                        country=entry["country"]["value"],
                        year=int(entry["date"]),
                        gdp_usd=float(val),
                    )
                    all_records.append(valid_item.model_dump())

        except Exception as e:
            print(f"[⚠️] Error on {code}: {str(e)}")

    print(
        f"\n[✔] Total {len(all_records)} validated macroeconomic records ingested."
    )
    return pd.DataFrame(all_records)


def analyze_economic_trends(df: pd.DataFrame):
    if df.empty:
        print(
            "[❌] No data found to analyze. Please check your internet connection."
        )
        return

    df = df.sort_values(by=["country", "year"]).reset_index(drop=True)
    df["GDP_Billion_USD"] = (df["gdp_usd"] / 1e9).round(2)
    df["YoY_Growth_Rate (%)"] = (
        df.groupby("country")["GDP_Billion_USD"].pct_change() * 100
    ).round(2)

    print(
        "\n------------------------------------------------------------------"
    )
    print("📊 SUMMARY: LATEST ECONOMIC INDICATORS (BILLION USD & GROWTH %)")
    print(
        "------------------------------------------------------------------"
    )
    latest_summary = df.groupby("country").tail(1)[
        ["country", "year", "GDP_Billion_USD", "YoY_Growth_Rate (%)"]
    ]
    print(latest_summary.to_string(index=False))

    usa_df = df[df["country"] == "United States"].dropna()
    if len(usa_df) > 2:
        X = sm.add_constant(usa_df["year"])
        y = usa_df["GDP_Billion_USD"]
        model = sm.OLS(y, X).fit()

        print(
            "\n------------------------------------------------------------------"
        )
        print("📈 ECONOMETRIC OLS REGRESSION INSIGHT (UNITED STATES)")
        print(
            "------------------------------------------------------------------"
        )
        print(
            f"|-- Average Annual GDP Expansion: +${model.params['year']:.2f} Billion / Year"
        )
        print(f"|-- Model Fit Accuracy (R-Squared): {model.rsquared:.4f}")

    output_file = "world_bank_economic_analysis.csv"
    df.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"\n[💾] Full econometric report exported to: {output_file}")


if __name__ == "__main__":
    economic_df = fetch_world_bank_gdp()
    analyze_economic_trends(economic_df)

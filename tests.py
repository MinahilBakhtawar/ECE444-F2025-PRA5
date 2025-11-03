import requests
import time
import pandas as pd
import matplotlib.pyplot as plt


API_URL = "http://ece444pra5.eu-north-1.elasticbeanstalk.com/predict"  
N_CALLS = 20


TEST_CASES = {
"fake_1": "Breaking: President spotted on Mars with aliens",
"fake_2": "Scientists confirm the earth is flat and NASA admits global cover-up.",
"real_1": "The World Health Organization issued new guidelines for pandemic response.",
"real_2": "Trump announces tariffs on Canada"
}


records = []

for label, text in TEST_CASES.items():
    print(f"Testing {label}")
    for i in range(N_CALLS):
        start = time.time()
        try:
            response = requests.post(API_URL, json={"message": text}, timeout=10)
            latency = time.time() - start
            status = response.status_code
            print(status)
        except Exception as e:
            latency = None
            status = "error"
        records.append({
            "test_case": label,
            "iteration": i + 1,
            "latency_sec": latency,
            "status": status
        })


df = pd.DataFrame(records)
df.to_csv("latency_results.csv", index=False)
print("Saved results to latency_results.csv")


summary = df.groupby("test_case")["latency_sec"].agg(["mean", "median", "std"]).reset_index()
print("\nAverage Latency (seconds):")
print(summary)

plt.figure(figsize=(8, 5))
df.boxplot(column="latency_sec", by="test_case", grid=False)
plt.title("API Latency by Test Case (100 requests each)")
plt.suptitle("")  # Remove automatic Pandas title
plt.xlabel("Test Case")
plt.ylabel("Latency (seconds)")
plt.tight_layout()
plt.savefig("latency_boxplot.png")
plt.show()

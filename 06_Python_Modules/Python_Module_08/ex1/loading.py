import importlib.util


def check_dependencies():
    print("Checking dependencies:")
    missing = 0
    packages = ["pandas", "requests", "matplotlib", "numpy"]
    for pkg in packages:
        spec = importlib.util.find_spec(pkg)
        if spec is not None:
            print(f"[OK] {pkg} - Ready")
        else:
            print(f"[MISSING] {pkg}")
            missing += 1
    return missing


if __name__ == "__main__":
    print("LOADING STATUS: Loading programs...")
    if check_dependencies():
        print("\nMissing dependencies!")
        print("Please run: python3 -m pip install -r requirements.txt")
        print("Or: python3 -m pip install poetry && poetry install")
        exit(1)

    import pandas as pd
    import requests
    import matplotlib.pyplot as plt
    import numpy as np

    print("\nAnalyzing Matrix data...")
    print("Processing 1000 data points...")

    response = requests.get("https://httpbin.org/get")
    status_code = response.status_code

    data = np.random.rand(1000)
    df = pd.DataFrame({"values": data})
    plt.figure()
    plt.plot(df["values"])
    plt.title(f"Matrix Analysis (HTTP status: {status_code})")
    plt.xlabel("Index")
    plt.ylabel("Value")

    output_image = "matrix_analysis.png"
    plt.savefig(output_image)
    print("Generating visualization...")
    print("Analysis complete!")
    print(f"Results saved to: {output_image}")

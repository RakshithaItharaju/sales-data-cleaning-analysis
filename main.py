"""Run the whole pipeline: clean -> load -> analyse."""
from src import clean_sales, load_to_sqlite, run_analysis

if __name__ == "__main__":
    clean_sales.main()
    print()
    load_to_sqlite.main()
    run_analysis.main()

import argparse
import webbrowser
import logging
import time

from components.scrapers.wikipedia_collateral_adjective_scraper import WikipediaCollateralAdjectiveScraper
from utils import abs_path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--debug",
        action="store_true",
        help="If true, will not use threading",
    )
    parser.add_argument(
        "--output_dir",
        type=abs_path,
        default="tmp",
    )
    parser.add_argument(
        "--display_results",
        action="store_true",
        help="If true, will open browser window to display results",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="If true, set logging level to INFO, otherwise ERROR",
    )
    return parser.parse_args()

def main():

    args = parse_args()

    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.ERROR,
    )

    scraper = WikipediaCollateralAdjectiveScraper(use_threading=not args.debug, output_dir=args.output_dir)
    output_file_path = scraper.scrape()

    if args.display_results:
        webbrowser.open_new_tab(output_file_path)

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Time elapsed: {end_time - start_time} seconds")
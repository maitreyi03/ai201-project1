"""
prepare_documents.py

Purpose:
    Convert your current `documents/` folder into the `data/raw/` structure
    needed by `milestone3_pipeline.py`.

Your current structure looks like:
    project/
    ├── documents/
    │   ├── .gitkeep
    │   └── sawtelle_sources.txt
    ├── milestone3_pipeline.py
    └── planning.md

After running this script, you should get:
    project/
    ├── data/
    │   └── raw/
    │       ├── reddit_ucla_food_recs_westwood_sawtelle_ktown.txt
    │       ├── reddit_foodla_favorite_sawtelle.txt
    │       ├── ...
    │       └── timeout_best_sawtelle_restaurants.txt

How to run:
    python3 prepare_documents.py

Then run:
    python3 milestone3_pipeline.py
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path


DOCUMENTS_DIR = Path("documents")
RAW_OUTPUT_DIR = Path("data/raw")


# These are the 10 source files from your planning.md.
# The script will create these files even if your combined source file
# only has rough notes right now.
SAWTELLE_SOURCE_FILES = [
    {
        "filename": "reddit_ucla_food_recs_westwood_sawtelle_ktown.txt",
        "title": "r/UCLA food recs: Westwood/Sawtelle/Ktown",
        "url": "https://www.reddit.com/r/ucla/comments/vtr93m/food_recs_westwoodsawtellektown/",
        "description": "Reddit thread with UCLA student-style food recommendations around Westwood, Sawtelle, and Koreatown. Useful for student opinions on ramen, udon, casual food spots, and nearby restaurants.",
    },
    {
        "filename": "reddit_foodla_favorite_sawtelle.txt",
        "title": "r/FoodLosAngeles: Favorite restaurants on Sawtelle",
        "url": "https://www.reddit.com/r/FoodLosAngeles/comments/1lo0ph9/favorite_restaurants_on_sawtelle/",
        "description": "Reddit thread with local opinions on favorite Sawtelle restaurants. Useful for recommendations on ramen, tofu, boba, dessert, and casual restaurants.",
    },
    {
        "filename": "reddit_foodla_not_ramen_sushi.txt",
        "title": "r/FoodLosAngeles: Sawtelle restaurants that are not ramen/noodles/sushi",
        "url": "https://www.reddit.com/r/FoodLosAngeles/comments/xeno5k/favorite_restaurants_in_sawtelle_that_are_not/",
        "description": "Reddit thread focused on Sawtelle food options outside of ramen, noodles, and sushi. Useful for questions about variety and non-ramen choices.",
    },
    {
        "filename": "reddit_ucla_best_food_westwood_santa_monica.txt",
        "title": "r/UCLA: Best food spots in Westwood/Santa Monica area",
        "url": "https://www.reddit.com/r/ucla/comments/1021ux7/best_food_spots_in_the_westwood_santa_monica_area/",
        "description": "UCLA Reddit thread with nearby student food recommendations, including Sawtelle and Westside restaurants. Useful for student-accessible food near UCLA.",
    },
    {
        "filename": "reddit_foodla_sawtelle_brentwood_recs.txt",
        "title": "r/FoodLosAngeles: Recs in Sawtelle/Brentwood",
        "url": "https://www.reddit.com/r/FoodLosAngeles/comments/1skg5uc/recs_in_sawtellebrentwood/",
        "description": "Reddit thread with recent local recommendations for Sawtelle and Brentwood. Useful for updated restaurant suggestions and neighborhood-specific opinions.",
    },
    {
        "filename": "reddit_ucla_vegetarian_options_sawtelle_westwood.txt",
        "title": "r/UCLA: Vegetarian options in Sawtelle/Westwood",
        "url": "https://www.reddit.com/r/ucla/comments/yy25ev/vegetarian_options_in_sawtellewestwood/",
        "description": "Reddit thread about vegetarian-friendly food options near Sawtelle and Westwood. Useful for questions about vegetarian meals and dietary restrictions.",
    },
    {
        "filename": "reddit_foodla_sawtelle_tier_list.txt",
        "title": "r/FoodLosAngeles: Sawtelle restaurants tier list",
        "url": "https://www.reddit.com/r/FoodLosAngeles/comments/1byr7wk/sawtelle_restaurants_tier_list_i_made_with_my/",
        "description": "Opinion-heavy Reddit tier list ranking Sawtelle restaurants. Useful for comparing restaurants, identifying popular spots, and finding overhyped or highly recommended places.",
    },
    {
        "filename": "infatuation_best_sawtelle_restaurants.txt",
        "title": "The Infatuation: Best Restaurants on Sawtelle Boulevard",
        "url": "https://www.theinfatuation.com/los-angeles/guides/best-sawtelle-restaurants",
        "description": "Editorial restaurant guide covering recommended Sawtelle restaurants. Useful for structured descriptions of restaurant type, vibe, and standout dishes.",
    },
    {
        "filename": "eater_best_sawtelle_japantown.txt",
        "title": "Eater LA: Essential Sawtelle Japantown Restaurants",
        "url": "https://la.eater.com/maps/essential-best-sawtelle-japantown-restaurants",
        "description": "Curated guide to essential restaurants in Sawtelle Japantown. Useful for broader restaurant coverage, including ramen, Japanese food, Filipino food, Thai food, and other local options.",
    },
    {
        "filename": "timeout_best_sawtelle_restaurants.txt",
        "title": "Time Out: Best Sawtelle Japantown Restaurants",
        "url": "https://www.timeout.com/los-angeles/restaurants/best-sawtelle-japantown-restaurants",
        "description": "Local guide to Sawtelle restaurants, desserts, and food spots. Useful for popular restaurant recommendations and neighborhood overview.",
    },
]


def slugify(text: str) -> str:
    """
    Convert a title into a safe lowercase filename.
    """
    text = text.lower()
    text = re.sub(r"https?://", "", text)
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = text.strip("_")
    return text or "document"


def find_combined_source_file() -> Path | None:
    """
    Look for the likely combined source file inside documents/.
    """
    candidates = [
        DOCUMENTS_DIR / "sawtelle_sources.txt",
        DOCUMENTS_DIR / "milestone1_sawtelle_sources.txt",
        DOCUMENTS_DIR / "sources.txt",
    ]

    for path in candidates:
        if path.exists():
            return path

    txt_files = [
        path for path in DOCUMENTS_DIR.glob("*.txt")
        if not path.name.startswith(".")
    ]

    if len(txt_files) == 1:
        return txt_files[0]

    return None


def extract_section_for_source(combined_text: str, title: str, url: str) -> str:
    """
    Try to extract a matching section from one combined source file.

    This is intentionally flexible because your sawtelle_sources.txt may be
    written as notes, markdown, or source blocks.

    If no matching section is found, the function returns an empty string.
    """
    lines = combined_text.splitlines()

    # First try: find the URL and take nearby lines around it.
    url_index = None
    for i, line in enumerate(lines):
        if url in line:
            url_index = i
            break

    if url_index is not None:
        start = max(0, url_index - 6)
        end = min(len(lines), url_index + 40)

        # If there is a clear next source divider, stop there.
        for j in range(url_index + 1, min(len(lines), url_index + 80)):
            lower = lines[j].lower().strip()
            if (
                lower.startswith("source_title:")
                or lower.startswith("## ")
                or lower.startswith("### ")
                or re.match(r"^\d+\.\s+", lower)
            ) and j > url_index + 3:
                end = j
                break

        return "\n".join(lines[start:end]).strip()

    # Second try: title keyword matching.
    title_keywords = [
        word.lower()
        for word in re.findall(r"[A-Za-z0-9]+", title)
        if len(word) > 3
    ]

    best_index = None
    best_score = 0

    for i, line in enumerate(lines):
        lower = line.lower()
        score = sum(1 for word in title_keywords if word in lower)
        if score > best_score:
            best_score = score
            best_index = i

    if best_index is not None and best_score >= 2:
        start = max(0, best_index - 5)
        end = min(len(lines), best_index + 40)
        return "\n".join(lines[start:end]).strip()

    return ""


def create_raw_files_from_combined_file(combined_file: Path) -> None:
    """
    Create the 10 data/raw source files from a combined sawtelle_sources.txt file.
    """
    combined_text = combined_file.read_text(encoding="utf-8", errors="replace")

    RAW_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for source in SAWTELLE_SOURCE_FILES:
        extracted = extract_section_for_source(
            combined_text=combined_text,
            title=source["title"],
            url=source["url"],
        )

        output_text = f"""SOURCE_TITLE: {source["title"]}
SOURCE_URL: {source["url"]}
SOURCE_TYPE: {"Reddit thread" if "reddit.com" in source["url"] else "Restaurant guide"}
SOURCE_DESCRIPTION: {source["description"]}
SOURCE_FILE_CREATED_FROM: {combined_file}

RAW_TEXT:
{extracted if extracted else "[Paste useful text, comments, or restaurant descriptions from this source here.]"}
"""

        output_path = RAW_OUTPUT_DIR / source["filename"]
        output_path.write_text(output_text.strip() + "\n", encoding="utf-8")

        status = "with extracted notes" if extracted else "as template"
        print(f"Created {output_path} ({status})")


def copy_existing_txt_documents() -> None:
    """
    If the documents/ folder already contains multiple individual .txt files,
    copy them into data/raw.
    """
    RAW_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    txt_files = [
        path for path in DOCUMENTS_DIR.glob("*.txt")
        if not path.name.startswith(".")
    ]

    for source_path in txt_files:
        output_name = slugify(source_path.stem) + ".txt"
        output_path = RAW_OUTPUT_DIR / output_name
        shutil.copyfile(source_path, output_path)
        print(f"Copied {source_path} -> {output_path}")


def main() -> None:
    if not DOCUMENTS_DIR.exists():
        raise FileNotFoundError(
            "Could not find the documents/ folder. "
            "Create it first and put sawtelle_sources.txt inside it."
        )

    txt_files = [
        path for path in DOCUMENTS_DIR.glob("*.txt")
        if not path.name.startswith(".")
    ]

    if not txt_files:
        raise FileNotFoundError(
            "No .txt files found in documents/. "
            "Put sawtelle_sources.txt or your source documents inside documents/."
        )

    combined_file = find_combined_source_file()

    # If there is one combined source file, split/create the 10 planned files.
    if combined_file is not None:
        print(f"Using combined source file: {combined_file}")
        create_raw_files_from_combined_file(combined_file)
    else:
        # If there are multiple files, copy them into data/raw.
        print("Multiple .txt files found in documents/. Copying them into data/raw/.")
        copy_existing_txt_documents()

    print("\nDone.")
    print(f"Check the generated files in: {RAW_OUTPUT_DIR}")
    print("Next step: open each file and paste more useful RAW_TEXT if needed.")
    print("Then run: python milestone3_pipeline.py")


if __name__ == "__main__":
    main()

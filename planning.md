# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

I chose food recommendations in Sawtelle Japantown / Sawtelle Boulevard in Los Angeles. This knowledge is valuable because students and locals often rely on unofficial recommendations from Reddit threads, local food guides, and word-of-mouth to decide where to eat, especially when they care about ramen, boba, dessert, vegetarian options, group-friendly spots, wait times, value, or whether a restaurant is overhyped.

This knowledge is hard to find through official channels because restaurant websites usually only show menus, hours, and polished marketing language. They do not explain what UCLA students and local diners actually recommend, what dishes people repeatedly mention, which places have long lines, which spots are best for groups, or which restaurants are considered overrated or underrated.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| #   | Source | Description | URL or location |
| --- | ------ | ----------- | --------------- |
| 1   |        |             |                 |
| 2   |        |             |                 |
| 3   |        |             |                 |
| 4   |        |             |                 |
| 5   |        |             |                 |
| 6   |        |             |                 |
| 7   |        |             |                 |
| 8   |        |             |                 |
| 9   |        |             |                 |
| 10  |        |             |                 |

1. `data/raw/reddit_foodla_favorite_sawtelle.txt`
   - Title: Favorite restaurants on Sawtelle?
   - URL: https://www.reddit.com/r/FoodLosAngeles/comments/1lo0ph9/favorite_restaurants_on_sawtelle/
   - Type: Reddit discussion thread
   - Why useful: Local opinion-heavy recommendations for ramen, tofu, boba, dessert, value, and group-friendly spots.

2. `data/raw/reddit_ucla_food_recs_westwood_sawtelle_ktown.txt`
   - Title: food recs westwood/sawtelle/ktown
   - URL: https://www.reddit.com/r/ucla/comments/vtr93m/food_recs_westwoodsawtellektown/
   - Type: UCLA Reddit discussion thread
   - Why useful: Student-centered recommendations around UCLA, including Sawtelle and nearby areas.

3. `data/raw/reddit_foodla_not_ramen_sushi.txt`
   - Title: Favorite restaurants in Sawtelle that are not ramen/noodle or sushi?
   - URL: https://www.reddit.com/r/FoodLosAngeles/comments/xeno5k/favorite_restaurants_in_sawtelle_that_are_not/
   - Type: Reddit discussion thread
   - Why useful: Helps answer questions from users who want Sawtelle food but not ramen, noodles, or sushi.

4. `data/raw/reddit_ucla_best_food_westwood_santa_monica.txt`
   - Title: best food spots in the westwood / Santa Monica area?
   - URL: https://www.reddit.com/r/ucla/comments/1021ux7/best_food_spots_in_the_westwood_santa_monica_area/
   - Type: UCLA Reddit discussion thread
   - Why useful: Includes Sawtelle recommendations from UCLA students, including Marugame Udon, Killer Noodle, Tatsu, Tsujita, Nong La, Sunright, Juquila, Kura, and Somi Somi.

5. `data/raw/reddit_foodla_sawtelle_brentwood_recs.txt`
   - Title: Recs in Sawtelle/Brentwood!
   - URL: https://www.reddit.com/r/FoodLosAngeles/comments/1skg5uc/recs_in_sawtellebrentwood/
   - Type: Reddit discussion thread
   - Why useful: Recent local recommendations for Sawtelle and Brentwood, including ramen, curry ramen, udon, curry, and sushi.

6. `data/raw/reddit_ucla_vegetarian_options_sawtelle_westwood.txt`
   - Title: vegetarian options in sawtelle/westwood
   - URL: https://www.reddit.com/r/ucla/comments/yy25ev/vegetarian_options_in_sawtellewestwood/
   - Type: UCLA Reddit discussion thread
   - Why useful: Focuses on vegetarian and vegan-friendly options near UCLA, Sawtelle, and Westwood.

7. `data/raw/reddit_foodla_sawtelle_tier_list.txt`
   - Title: Sawtelle restaurants tier list I made with my friends
   - URL: https://www.reddit.com/r/FoodLosAngeles/comments/1byr7wk/sawtelle_restaurants_tier_list_i_made_with_my/
   - Type: Reddit tier-list discussion
   - Why useful: Opinion-rich rankings across many Sawtelle restaurants, including ramen, boba, dessert, sushi, curry, Thai food, burgers, and service issues.

8. `data/raw/infatuation_best_sawtelle_restaurants.txt`
   - Title: The 18 Best Restaurants On West LA's Sawtelle Boulevard
   - URL: https://www.theinfatuation.com/los-angeles/guides/best-sawtelle-restaurants
   - Type: Local restaurant guide
   - Why useful: Structured editorial guide to Sawtelle restaurants, including restaurant descriptions, categories, and practical dining context.

9. `data/raw/eater_best_sawtelle_japantown.txt`
   - Title: Best Restaurants in Los Angeles's Sawtelle Japantown
   - URL: https://la.eater.com/maps/essential-best-sawtelle-japantown-restaurants
   - Type: Local restaurant guide
   - Why useful: Current editorial guide with a broad view of Sawtelle Japantown restaurants, including new and classic spots.

10. `data/raw/timeout_best_sawtelle_restaurants.txt`
    - Title: 22 Best Restaurants on West L.A.'s Sawtelle Boulevard
    - URL: https://www.timeout.com/los-angeles/restaurants/best-sawtelle-japantown-restaurants
    - Type: Local restaurant guide
    - Why useful: Broad guide covering Sawtelle restaurants, desserts, boba, ramen, and the neighborhood's dense dining scene.

11. `data/raw/discover_la_sawtelle_walking_tour.txt`
    - Title: A Walking Tour of Sawtelle Japantown
    - URL: https://www.discoverlosangeles.com/things-to-do/a-walking-tour-of-sawtelle-japantown
    - Type: Local neighborhood guide
    - Why useful: Gives background context on Sawtelle Japantown and restaurants like Tsujita Annex and Nong La.

12. `data/raw/travelagewest_best_sawtelle_restaurants.txt`
    - Title: A Complete Guide to the Best Sawtelle Restaurants
    - URL: https://www.travelagewest.com/Travel/USA-Canada/A-Complete-Guide-to-the-Best-Sawtelle-Restaurants
    - Type: Travel/restaurant guide
    - Why useful: Adds restaurant descriptions and practical advice, including lunch crowds, burgers, ramen, sushi, udon, Vietnamese food, and dessert.

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| #   | Question | Expected answer |
| --- | -------- | --------------- |
| 1   |          |                 |
| 2   |          |                 |
| 3   |          |                 |
| 4   |          |                 |
| 5   |          |                 |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**

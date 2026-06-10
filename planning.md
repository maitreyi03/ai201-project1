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

I will split the documents into paragraph-aware chunks of approximately 700–900 characters with an overlap of about 150 characters. This strategy fits my documents because many of the Reddit sources contain short comments or brief recommendations, while the food guide sources contain longer paragraphs describing multiple restaurants. A paragraph-aware approach should preserve complete thoughts better than splitting every fixed number of characters without regard to sentence or paragraph boundaries.
The overlap is important because restaurant recommendations may include the restaurant name in one sentence and the reason for recommending it in the next sentence. If that information gets split across two chunks, the overlap increases the chance that both the restaurant name and the useful recommendation appear together in at least one retrievable chunk.
If the chunks are too small, retrieval may return fragments like only a restaurant name without the opinion or context explaining why it is recommended. If the chunks are too large, one chunk may contain too many unrelated restaurants, making semantic search less precise. I will inspect sample chunks after chunking to make sure each chunk is readable, substantive, and useful on its own.

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

I will split the documents into paragraph-aware chunks of approximately 700–900 characters with an overlap of about 150 characters. This strategy fits my documents because many of the Reddit sources contain short comments or brief recommendations, while the food guide sources contain longer paragraphs describing multiple restaurants. A paragraph-aware approach should preserve complete thoughts better than splitting every fixed number of characters without regard to sentence or paragraph boundaries.
The overlap is important because restaurant recommendations may include the restaurant name in one sentence and the reason for recommending it in the next sentence. If that information gets split across two chunks, the overlap increases the chance that both the restaurant name and the useful recommendation appear together in at least one retrievable chunk.
If the chunks are too small, retrieval may return fragments like only a restaurant name without the opinion or context explaining why it is recommended. If the chunks are too large, one chunk may contain too many unrelated restaurants, making semantic search less precise. I will inspect sample chunks after chunking to make sure each chunk is readable, substantive, and useful on its own.

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

1.Question: What restaurants are recommended for ramen in Sawtelle?
Expected answer: The system should mention ramen-focused recommendations such as Tsujita, Tsujita Annex, Tatsu, Killer Noodle, or Menya Tigre, depending on which sources are retrieved. The answer should cite the source documents that mention those restaurants.

2.Question: What are good dessert or sweet snack places in Sawtelle?
Expected answer: The system should mention dessert or sweet options such as Somi Somi, Millet Crepe, Indigo Cow, or other dessert places that appear in the collected sources. The answer should explain what type of dessert each place is known for when the documents provide that detail.

3.Question: What Sawtelle restaurants are recommended if I do not want ramen, noodles, or sushi?
Expected answer: The system should retrieve information from the non-ramen/sushi Reddit thread and possibly guide sources. It should recommend alternatives outside of ramen and sushi, such as curry, tofu, okonomiyaki, Filipino food, Thai food, or other non-ramen options mentioned in the documents.

4.Question: What vegetarian-friendly food options are mentioned near Sawtelle or Westwood?
Expected answer: The system should retrieve the vegetarian-options source and mention vegetarian-friendly places or dishes that appear in the documents. The answer should avoid making unsupported claims if the documents do not give enough detail.

5.Question: Which Sawtelle places do students or locals seem especially excited about or rank highly?
Expected answer: The system should use opinion-heavy sources such as the Sawtelle tier list and favorite-restaurant Reddit threads. It should identify restaurants that appear repeatedly or are ranked highly, while citing the specific documents used.
These questions are specific enough to evaluate because each one asks for a clear category of restaurant recommendation. I can compare the system response against the source documents and judge whether the retrieved chunks and generated answer are accurate, partially accurate, or inaccurate.

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

One challenge is that the documents may be noisy or inconsistent. Reddit comments are informal, may include jokes or incomplete thoughts, and different users may disagree about the same restaurant. This could make it hard for the system to produce a balanced answer if it retrieves only one side of an opinion.
Another challenge is source attribution. Since some restaurant names may appear in multiple sources, the system needs to clearly show which document each recommendation came from. Without source attribution, a user would not know whether the answer came from a Reddit thread, a curated food guide, or a specific review-style source.
A third challenge is chunk boundaries. If a restaurant name appears at the end of one chunk and the explanation appears at the beginning of the next chunk, retrieval may return only part of the useful information. The 150-character overlap should help reduce this problem, but I will still need to inspect chunks manually.
A fourth challenge is off-topic retrieval. Some sources may mention nearby neighborhoods like Westwood, Santa Monica, or Koreatown in addition to Sawtelle. The system might retrieve restaurants outside Sawtelle if the query is broad, so I will need to check whether metadata and source descriptions help keep responses focused.

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

I plan to use AI tools to help implement specific parts of the pipeline, but I will use my own planning document and source decisions as the main guide.
First, I will prompt ChatGPT or Claude with my Documents section and Chunking Strategy section and ask it to help implement an ingestion script. I will ask it to load .txt files from data/raw, clean unnecessary text, preserve source metadata, and save processed text. I expect the AI tool to produce a Python script, but I will review the code to make sure it matches my file structure and does not remove useful restaurant information.
Second, I will prompt the AI tool with my Chunking Strategy section and ask it to implement a chunk_text() function using 700–900 character chunks with around 150 characters of overlap. I will specifically ask for paragraph-aware chunking so that chunks do not cut off sentences or restaurant descriptions in awkward places. I will inspect the output chunks manually and revise the function if the chunks are too short, too long, or not meaningful on their own.
Third, I will prompt the AI tool with my Retrieval Approach section and ask it to help implement the embedding and vector store setup using sentence-transformers, all-MiniLM-L6-v2, and ChromaDB. I expect the AI tool to help create a script that embeds chunks, stores them with source metadata, and retrieves the top 4 chunks for a query. I will test retrieval with my evaluation questions before adding generation.
Fourth, I will use AI assistance to help write the grounded generation prompt. I will provide the requirement that the LLM must answer only from retrieved context and must cite sources. I expect the AI tool to help draft the prompt template, but I will verify that the final answer format includes source attribution and that the model refuses to answer when the documents do not contain enough information.
Finally, I may use AI tools to help organize my README and evaluation report. I will give the AI my actual system outputs, retrieved chunks, and accuracy judgments, then ask it to help format the evaluation clearly. I will not ask the AI to invent results; the evaluation will be based on the real behavior of my system.

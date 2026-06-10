# Milestone 4 Retrieval Test Results

Embedding model: `sentence-transformers/all-MiniLM-L6-v2`

Vector store: `ChromaDB`

Retrieval method: semantic similarity search

Distance note: lower distance means a stronger match. Distances above ~0.6-0.7 may indicate weaker retrieval.

## Test Query 1

**Query:** What restaurants are recommended for ramen in Sawtelle?

#### Result 1

- **Source file:** `reddit_foodla_not_ramen_sushi.txt`
- **Chunk index:** 0
- **Distance:** 0.3379

```text
SOURCE_TITLE: r/FoodLosAngeles: Sawtelle restaurants that are not ramen/noodles/sushi SOURCE_URL: SOURCE_TYPE: Reddit thread SOURCE_DESCRIPTION: Reddit thread focused on Sawtelle food options outside of ramen, noodles, and sushi. Useful for questions about variety and non-ramen choices. SOURCE_FILE_CREATED_FROM: documents/sawtelle_sources.txt

RAW_TEXT: 2. data/raw/reddit_ucla_food_recs_westwood_sawtelle_ktown.txt URL: Source type: UCLA Reddit discussion thread Focus: Student recommendations around UCLA, Sawtelle, Westwood, and nearby areas.

3. data/raw/reddit_foodla_not_ramen_sushi.txt URL: Source type: Reddit discussion thread Focus: Non-ramen, non-noodle, and non-sushi Sawtelle options.
```

#### Result 2

- **Source file:** `reddit_foodla_favorite_sawtelle.txt`
- **Chunk index:** 0
- **Distance:** 0.3479

```text
SOURCE_TITLE: r/FoodLosAngeles: Favorite restaurants on Sawtelle SOURCE_URL: SOURCE_TYPE: Reddit thread SOURCE_DESCRIPTION: Reddit thread with local opinions on favorite Sawtelle restaurants. Useful for recommendations on ramen, tofu, boba, dessert, and casual restaurants. SOURCE_FILE_CREATED_FROM: documents/sawtelle_sources.txt

RAW_TEXT: Purpose: This source list supports a RAG system that answers unofficial food recommendation questions about Sawtelle. The sources combine UCLA student Reddit threads, Los Angeles food Reddit threads, and local restaurant guides so the system can answer questions about ramen, boba, dessert, vegetarian options, group-friendly spots, wait times, value, and overhyped restaurants.

Source Documents / Raw File Paths:
```

#### Result 3

- **Source file:** `reddit_foodla_favorite_sawtelle.txt`
- **Chunk index:** 1
- **Distance:** 0.3737

```text
ramen, boba, dessert, vegetarian options, group-friendly spots, wait times, value, and overhyped restaurants.

Source Documents / Raw File Paths:

1. data/raw/reddit_foodla_favorite_sawtelle.txt URL: Source type: Reddit discussion thread Focus: Local favorites, ramen, tofu, boba, dessert, value, group-friendly spots.
```

#### Result 4

- **Source file:** `timeout_best_sawtelle_restaurants.txt`
- **Chunk index:** 0
- **Distance:** 0.4053

```text
SOURCE_TITLE: Time Out: Best Sawtelle Japantown Restaurants SOURCE_URL: SOURCE_TYPE: Restaurant guide SOURCE_DESCRIPTION: Local guide to Sawtelle restaurants, desserts, and food spots. Useful for popular restaurant recommendations and neighborhood overview. SOURCE_FILE_CREATED_FROM: documents/sawtelle_sources.txt

RAW_TEXT: 9. data/raw/eater_best_sawtelle_japantown.txt URL: Source type: Local restaurant guide Focus: Current editorial guide to Sawtelle Japantown restaurants.

10. data/raw/timeout_best_sawtelle_restaurants.txt URL: Source type: Local restaurant guide Focus: Sawtelle restaurants, desserts, boba, ramen, and neighborhood dining overview.
```

### Manual relevance notes

- Retrieved chunks relevant? `[fill in: yes / partially / no]`
- Why? `[write 1-2 sentences after inspecting the chunks]`

## Test Query 2

**Query:** What are good dessert or sweet snack places in Sawtelle?

#### Result 1

- **Source file:** `reddit_ucla_food_recs_westwood_sawtelle_ktown.txt`
- **Chunk index:** 0
- **Distance:** 0.4022

```text
SOURCE_TITLE: r/UCLA food recs: Westwood/Sawtelle/Ktown SOURCE_URL: SOURCE_TYPE: Reddit thread SOURCE_DESCRIPTION: Reddit thread with UCLA student-style food recommendations around Westwood, Sawtelle, and Koreatown. Useful for student opinions on ramen, udon, casual food spots, and nearby restaurants. SOURCE_FILE_CREATED_FROM: documents/sawtelle_sources.txt

RAW_TEXT: 1. data/raw/reddit_foodla_favorite_sawtelle.txt URL: Source type: Reddit discussion thread Focus: Local favorites, ramen, tofu, boba, dessert, value, group-friendly spots.

2. data/raw/reddit_ucla_food_recs_westwood_sawtelle_ktown.txt URL: Source type: UCLA Reddit discussion thread Focus: Student recommendations around UCLA, Sawtelle, Westwood, and nearby areas.
```

#### Result 2

- **Source file:** `reddit_ucla_best_food_westwood_santa_monica.txt`
- **Chunk index:** 0
- **Distance:** 0.4263

```text
SOURCE_TITLE: r/UCLA: Best food spots in Westwood/Santa Monica area SOURCE_URL: SOURCE_TYPE: Reddit thread SOURCE_DESCRIPTION: UCLA Reddit thread with nearby student food recommendations, including Sawtelle and Westside restaurants. Useful for student-accessible food near UCLA. SOURCE_FILE_CREATED_FROM: documents/sawtelle_sources.txt

RAW_TEXT: 3. data/raw/reddit_foodla_not_ramen_sushi.txt URL: Source type: Reddit discussion thread Focus: Non-ramen, non-noodle, and non-sushi Sawtelle options.

4. data/raw/reddit_ucla_best_food_westwood_santa_monica.txt URL: Source type: UCLA Reddit discussion thread Focus: UCLA student recommendations for Westwood, Sawtelle, and Santa Monica.
```

#### Result 3

- **Source file:** `reddit_foodla_favorite_sawtelle.txt`
- **Chunk index:** 0
- **Distance:** 0.4399

```text
SOURCE_TITLE: r/FoodLosAngeles: Favorite restaurants on Sawtelle SOURCE_URL: SOURCE_TYPE: Reddit thread SOURCE_DESCRIPTION: Reddit thread with local opinions on favorite Sawtelle restaurants. Useful for recommendations on ramen, tofu, boba, dessert, and casual restaurants. SOURCE_FILE_CREATED_FROM: documents/sawtelle_sources.txt

RAW_TEXT: Purpose: This source list supports a RAG system that answers unofficial food recommendation questions about Sawtelle. The sources combine UCLA student Reddit threads, Los Angeles food Reddit threads, and local restaurant guides so the system can answer questions about ramen, boba, dessert, vegetarian options, group-friendly spots, wait times, value, and overhyped restaurants.

Source Documents / Raw File Paths:
```

#### Result 4

- **Source file:** `reddit_foodla_favorite_sawtelle.txt`
- **Chunk index:** 1
- **Distance:** 0.4480

```text
ramen, boba, dessert, vegetarian options, group-friendly spots, wait times, value, and overhyped restaurants.

Source Documents / Raw File Paths:

1. data/raw/reddit_foodla_favorite_sawtelle.txt URL: Source type: Reddit discussion thread Focus: Local favorites, ramen, tofu, boba, dessert, value, group-friendly spots.
```

### Manual relevance notes

- Retrieved chunks relevant? `[fill in: yes / partially / no]`
- Why? `[write 1-2 sentences after inspecting the chunks]`

## Test Query 3

**Query:** What Sawtelle restaurants are recommended if I do not want ramen, noodles, or sushi?

#### Result 1

- **Source file:** `reddit_foodla_not_ramen_sushi.txt`
- **Chunk index:** 0
- **Distance:** 0.2800

```text
SOURCE_TITLE: r/FoodLosAngeles: Sawtelle restaurants that are not ramen/noodles/sushi SOURCE_URL: SOURCE_TYPE: Reddit thread SOURCE_DESCRIPTION: Reddit thread focused on Sawtelle food options outside of ramen, noodles, and sushi. Useful for questions about variety and non-ramen choices. SOURCE_FILE_CREATED_FROM: documents/sawtelle_sources.txt

RAW_TEXT: 2. data/raw/reddit_ucla_food_recs_westwood_sawtelle_ktown.txt URL: Source type: UCLA Reddit discussion thread Focus: Student recommendations around UCLA, Sawtelle, Westwood, and nearby areas.

3. data/raw/reddit_foodla_not_ramen_sushi.txt URL: Source type: Reddit discussion thread Focus: Non-ramen, non-noodle, and non-sushi Sawtelle options.
```

#### Result 2

- **Source file:** `reddit_foodla_favorite_sawtelle.txt`
- **Chunk index:** 0
- **Distance:** 0.3508

```text
SOURCE_TITLE: r/FoodLosAngeles: Favorite restaurants on Sawtelle SOURCE_URL: SOURCE_TYPE: Reddit thread SOURCE_DESCRIPTION: Reddit thread with local opinions on favorite Sawtelle restaurants. Useful for recommendations on ramen, tofu, boba, dessert, and casual restaurants. SOURCE_FILE_CREATED_FROM: documents/sawtelle_sources.txt

RAW_TEXT: Purpose: This source list supports a RAG system that answers unofficial food recommendation questions about Sawtelle. The sources combine UCLA student Reddit threads, Los Angeles food Reddit threads, and local restaurant guides so the system can answer questions about ramen, boba, dessert, vegetarian options, group-friendly spots, wait times, value, and overhyped restaurants.

Source Documents / Raw File Paths:
```

#### Result 3

- **Source file:** `eater_best_sawtelle_japantown.txt`
- **Chunk index:** 0
- **Distance:** 0.3736

```text
SOURCE_TITLE: Eater LA: Essential Sawtelle Japantown Restaurants SOURCE_URL: SOURCE_TYPE: Restaurant guide SOURCE_DESCRIPTION: Curated guide to essential restaurants in Sawtelle Japantown. Useful for broader restaurant coverage, including ramen, Japanese food, Filipino food, Thai food, and other local options. SOURCE_FILE_CREATED_FROM: documents/sawtelle_sources.txt

RAW_TEXT: 8. data/raw/infatuation_best_sawtelle_restaurants.txt URL: Source type: Local restaurant guide Focus: Structured editorial restaurant guide to Sawtelle Boulevard.

9. data/raw/eater_best_sawtelle_japantown.txt URL: Source type: Local restaurant guide Focus: Current editorial guide to Sawtelle Japantown restaurants.
```

#### Result 4

- **Source file:** `timeout_best_sawtelle_restaurants.txt`
- **Chunk index:** 0
- **Distance:** 0.3806

```text
SOURCE_TITLE: Time Out: Best Sawtelle Japantown Restaurants SOURCE_URL: SOURCE_TYPE: Restaurant guide SOURCE_DESCRIPTION: Local guide to Sawtelle restaurants, desserts, and food spots. Useful for popular restaurant recommendations and neighborhood overview. SOURCE_FILE_CREATED_FROM: documents/sawtelle_sources.txt

RAW_TEXT: 9. data/raw/eater_best_sawtelle_japantown.txt URL: Source type: Local restaurant guide Focus: Current editorial guide to Sawtelle Japantown restaurants.

10. data/raw/timeout_best_sawtelle_restaurants.txt URL: Source type: Local restaurant guide Focus: Sawtelle restaurants, desserts, boba, ramen, and neighborhood dining overview.
```

### Manual relevance notes

- Retrieved chunks relevant? `[fill in: yes / partially / no]`
- Why? `[write 1-2 sentences after inspecting the chunks]`

## Test Query 4

**Query:** What vegetarian-friendly food options are mentioned near Sawtelle or Westwood?

#### Result 1

- **Source file:** `reddit_ucla_vegetarian_options_sawtelle_westwood.txt`
- **Chunk index:** 0
- **Distance:** 0.2087

```text
SOURCE_TITLE: r/UCLA: Vegetarian options in Sawtelle/Westwood SOURCE_URL: SOURCE_TYPE: Reddit thread SOURCE_DESCRIPTION: Reddit thread about vegetarian-friendly food options near Sawtelle and Westwood. Useful for questions about vegetarian meals and dietary restrictions. SOURCE_FILE_CREATED_FROM: documents/sawtelle_sources.txt

RAW_TEXT: 5. data/raw/reddit_foodla_sawtelle_brentwood_recs.txt URL: Source type: Reddit discussion thread Focus: Recent local recommendations for Sawtelle and Brentwood.

6. data/raw/reddit_ucla_vegetarian_options_sawtelle_westwood.txt URL: Source type: UCLA Reddit discussion thread Focus: Vegetarian and vegan-friendly options near UCLA, Sawtelle, and Westwood.
```

#### Result 2

- **Source file:** `reddit_foodla_sawtelle_tier_list.txt`
- **Chunk index:** 0
- **Distance:** 0.3293

```text
SOURCE_TITLE: r/FoodLosAngeles: Sawtelle restaurants tier list SOURCE_URL: SOURCE_TYPE: Reddit thread SOURCE_DESCRIPTION: Opinion-heavy Reddit tier list ranking Sawtelle restaurants. Useful for comparing restaurants, identifying popular spots, and finding overhyped or highly recommended places. SOURCE_FILE_CREATED_FROM: documents/sawtelle_sources.txt

RAW_TEXT: 6. data/raw/reddit_ucla_vegetarian_options_sawtelle_westwood.txt URL: Source type: UCLA Reddit discussion thread Focus: Vegetarian and vegan-friendly options near UCLA, Sawtelle, and Westwood.

7. data/raw/reddit_foodla_sawtelle_tier_list.txt URL: Source type: Reddit tier-list discussion Focus: Opinion-heavy ranking of many Sawtelle restaurants.
```

#### Result 3

- **Source file:** `reddit_ucla_best_food_westwood_santa_monica.txt`
- **Chunk index:** 0
- **Distance:** 0.3685

```text
SOURCE_TITLE: r/UCLA: Best food spots in Westwood/Santa Monica area SOURCE_URL: SOURCE_TYPE: Reddit thread SOURCE_DESCRIPTION: UCLA Reddit thread with nearby student food recommendations, including Sawtelle and Westside restaurants. Useful for student-accessible food near UCLA. SOURCE_FILE_CREATED_FROM: documents/sawtelle_sources.txt

RAW_TEXT: 3. data/raw/reddit_foodla_not_ramen_sushi.txt URL: Source type: Reddit discussion thread Focus: Non-ramen, non-noodle, and non-sushi Sawtelle options.

4. data/raw/reddit_ucla_best_food_westwood_santa_monica.txt URL: Source type: UCLA Reddit discussion thread Focus: UCLA student recommendations for Westwood, Sawtelle, and Santa Monica.
```

#### Result 4

- **Source file:** `reddit_foodla_sawtelle_brentwood_recs.txt`
- **Chunk index:** 0
- **Distance:** 0.3732

```text
SOURCE_TITLE: r/FoodLosAngeles: Recs in Sawtelle/Brentwood SOURCE_URL: SOURCE_TYPE: Reddit thread SOURCE_DESCRIPTION: Reddit thread with recent local recommendations for Sawtelle and Brentwood. Useful for updated restaurant suggestions and neighborhood-specific opinions. SOURCE_FILE_CREATED_FROM: documents/sawtelle_sources.txt

RAW_TEXT: 4. data/raw/reddit_ucla_best_food_westwood_santa_monica.txt URL: Source type: UCLA Reddit discussion thread Focus: UCLA student recommendations for Westwood, Sawtelle, and Santa Monica.

5. data/raw/reddit_foodla_sawtelle_brentwood_recs.txt URL: Source type: Reddit discussion thread Focus: Recent local recommendations for Sawtelle and Brentwood.
```

### Manual relevance notes

- Retrieved chunks relevant? `[fill in: yes / partially / no]`
- Why? `[write 1-2 sentences after inspecting the chunks]`

## Test Query 5

**Query:** Which Sawtelle places do students or locals seem especially excited about or rank highly?

#### Result 1

- **Source file:** `reddit_ucla_food_recs_westwood_sawtelle_ktown.txt`
- **Chunk index:** 0
- **Distance:** 0.5158

```text
SOURCE_TITLE: r/UCLA food recs: Westwood/Sawtelle/Ktown SOURCE_URL: SOURCE_TYPE: Reddit thread SOURCE_DESCRIPTION: Reddit thread with UCLA student-style food recommendations around Westwood, Sawtelle, and Koreatown. Useful for student opinions on ramen, udon, casual food spots, and nearby restaurants. SOURCE_FILE_CREATED_FROM: documents/sawtelle_sources.txt

RAW_TEXT: 1. data/raw/reddit_foodla_favorite_sawtelle.txt URL: Source type: Reddit discussion thread Focus: Local favorites, ramen, tofu, boba, dessert, value, group-friendly spots.

2. data/raw/reddit_ucla_food_recs_westwood_sawtelle_ktown.txt URL: Source type: UCLA Reddit discussion thread Focus: Student recommendations around UCLA, Sawtelle, Westwood, and nearby areas.
```

#### Result 2

- **Source file:** `reddit_foodla_sawtelle_tier_list.txt`
- **Chunk index:** 0
- **Distance:** 0.5427

```text
SOURCE_TITLE: r/FoodLosAngeles: Sawtelle restaurants tier list SOURCE_URL: SOURCE_TYPE: Reddit thread SOURCE_DESCRIPTION: Opinion-heavy Reddit tier list ranking Sawtelle restaurants. Useful for comparing restaurants, identifying popular spots, and finding overhyped or highly recommended places. SOURCE_FILE_CREATED_FROM: documents/sawtelle_sources.txt

RAW_TEXT: 6. data/raw/reddit_ucla_vegetarian_options_sawtelle_westwood.txt URL: Source type: UCLA Reddit discussion thread Focus: Vegetarian and vegan-friendly options near UCLA, Sawtelle, and Westwood.

7. data/raw/reddit_foodla_sawtelle_tier_list.txt URL: Source type: Reddit tier-list discussion Focus: Opinion-heavy ranking of many Sawtelle restaurants.
```

#### Result 3

- **Source file:** `infatuation_best_sawtelle_restaurants.txt`
- **Chunk index:** 0
- **Distance:** 0.5583

```text
SOURCE_TITLE: The Infatuation: Best Restaurants on Sawtelle Boulevard SOURCE_URL: SOURCE_TYPE: Restaurant guide SOURCE_DESCRIPTION: Editorial restaurant guide covering recommended Sawtelle restaurants. Useful for structured descriptions of restaurant type, vibe, and standout dishes. SOURCE_FILE_CREATED_FROM: documents/sawtelle_sources.txt

RAW_TEXT: 7. data/raw/reddit_foodla_sawtelle_tier_list.txt URL: Source type: Reddit tier-list discussion Focus: Opinion-heavy ranking of many Sawtelle restaurants.

8. data/raw/infatuation_best_sawtelle_restaurants.txt URL: Source type: Local restaurant guide Focus: Structured editorial restaurant guide to Sawtelle Boulevard.
```

#### Result 4

- **Source file:** `reddit_ucla_best_food_westwood_santa_monica.txt`
- **Chunk index:** 0
- **Distance:** 0.5673

```text
SOURCE_TITLE: r/UCLA: Best food spots in Westwood/Santa Monica area SOURCE_URL: SOURCE_TYPE: Reddit thread SOURCE_DESCRIPTION: UCLA Reddit thread with nearby student food recommendations, including Sawtelle and Westside restaurants. Useful for student-accessible food near UCLA. SOURCE_FILE_CREATED_FROM: documents/sawtelle_sources.txt

RAW_TEXT: 3. data/raw/reddit_foodla_not_ramen_sushi.txt URL: Source type: Reddit discussion thread Focus: Non-ramen, non-noodle, and non-sushi Sawtelle options.

4. data/raw/reddit_ucla_best_food_westwood_santa_monica.txt URL: Source type: UCLA Reddit discussion thread Focus: UCLA student recommendations for Westwood, Sawtelle, and Santa Monica.
```

### Manual relevance notes

- Retrieved chunks relevant? `[fill in: yes / partially / no]`
- Why? `[write 1-2 sentences after inspecting the chunks]`

# auto-cook 

Pick meals from a recipe file and get a combined grocery list. There are two ways to run it: a random weekly menu, or a list of dishes you choose yourself. Both print JSON so they can be called from Apple Shortcuts.

## Setup

Requires Python 3.10+ (uses `match` statements) and PyYAML:

> [!NOTE] 
> If you only want to use json format then there is no dependencies needed

```bash
pip install pyyaml
```

Run the scripts from this directory so they can find `recipes.yaml` / `recipes.json`.

## Recipe files

Recipes live in `recipes.yaml` (used by the entry scripts) or `recipes.json`. Both use the same shape: meal type → dish → ingredient quantities.

YAML dish names use underscores (`eggs_on_toast`). JSON dish names use spaces (`eggs on toast`). The YAML path is the one the CLIs actually load.

```yaml
breakfast:
  eggs_on_toast:
    loaf_sourdough: 1
    eggs: 12
lunch:
  sandwich:
    deli_turkey: 2
    sliced_cheese: 1
dinner:
  spaghetti:
    ground_beef: 1
    spaghetti: 1
    red_sauce: 1
```
Add or edit dishes in the YAML file. Ingredient keys become grocery-list lines with underscores turned into spaces (`loaf_sourdough` → `loaf sourdough`).

Can also use a json format although this is more to maintain and does not support comments or spaces

```json
  "breakfast": {
    "eggs on toast": {
      "loaf sourdough": 1,
      "egg": 12 
    }
  },
  "lunch": {
    "sandwhich": {
      "deli turkey": 2,
      "sliced cheese": 1
    }
  },
  "dinner": {
    "spaghetti": {
      "ground beef": 1,
      "spaghetti": 1,
      "red sauce": 1
    }      
```

## Random menu

Picks **1 breakfast**, **2 lunches**, and **3 dinners** at random (no repeats within a meal type), then merges their ingredients:

> [!NOTE] 
> These are the default fields and they are configurable by adding `num_breakfast`, `num_lunch`, and `num_dinner` to your yaml/json file

```bash
python rand_run.py
```

Example output:

```json
{
  "ingredients": ["1 loaf sourdough", "12 eggs", "2 deli turkey"],
  "meals": ["eggs on toast", "sandwich", "spaghetti"]
}
```

## Chosen meals

Pass a JSON object with a `meals` list. Dish names are matched case-insensitively; spaces in names are converted to underscores for the YAML file.

```bash
python manual_run.py '{"meals": ["Meatloaf", "Eggs on toast", "Sandwich", "Spaghetti"]}'
```

Example output:

```json
{
  "ingredients": ["1 ground turkey", "1 ground beef", "1 ketchup", "1 loaf sourdough", "12 eggs"]
}
```

If the argument is missing or not valid JSON, it prints `bad data`.

## Apple Shortcuts

`rand_run.py` and `manual_run.py` print a single JSON object on stdout. A Shortcut can run the script, parse that JSON, and turn `ingredients` into reminders (plus `meals` for the random path).

Set up a Python runtime in Shortcuts with whatever method you prefer, then wire one of the flows below.

### Random mode

1. Run `rand_run.py` and pass its stdout into **Get Dictionary**.
2. **Set Variable** on that dictionary (for example `Menu`).
3. **Repeat with Each** over `Menu.ingredients`.
4. Inside the loop, **New Reminder** and use **Repeat Item** as the input.
5. **Text** with `Menu.meals` so you can see what was picked.
6. **Show Notification** with that text.

### Manual mode

1. **Ask for Input** with **Allow Multiple Lines** enabled.
2. **Split Text** on **New Lines** (the script already strips trailing whitespace).
3. **Repeat with Each** over the split lines and collect them into a list.
4. **Dictionary**: key `meals`, value type **Array**, value **Repeat Results**.
5. Run `manual_run.py` and pass that dictionary into the Python runtime.
6. **Get Dictionary** / **Set Variable** on the Python result.
7. **Repeat with Each** over the returned `ingredients` list and **New Reminder** for every item.

## Code layout

| File | Role |
| --- | --- |
| `recipe_selector.py` | Load recipes, pick dishes, merge quantities |
| `rand_run.py` | Random menu CLI |
| `manual_run.py` | Chosen-meals CLI |
| `recipes.yaml` | Recipe data used by the CLIs |
| `recipes.json` | Alternate recipe data (same ideas, different naming) |

# TODO
- setup `easy` section to pull only easy recipes


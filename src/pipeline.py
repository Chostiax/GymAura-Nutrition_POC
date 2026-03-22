from src.extractor import extract_foods
from src.matcher import match_food_to_dataset
from src.nutrition import estimate_grams, compute_item_nutrition, sum_nutrition


def run_pipeline(text: str, dataset) -> dict:
    """
    End-to-end internal pipeline for the PoC.

    Flow:
    1. extract food mentions from natural text
    2. match each mention to the internal dataset
    3. estimate grams when possible
    4. calculate nutrition
    """
    extracted_items = extract_foods(text)
    final_items = []

    for item in extracted_items:
        match_result = match_food_to_dataset(item["food_text"], dataset)

        dataset_row = None
        grams = None
        nutrition = None
        needs_clarification = False

        if match_result["matched"]:
            dataset_row = dataset.loc[match_result["row_index"]]

            grams = estimate_grams(
                food_text=item["food_text"],
                quantity=item["quantity"],
                unit=item["unit"],
            )

            nutrition = compute_item_nutrition(dataset_row, grams)

            # We matched the food, but quantity/portion is still too vague
            if grams is None:
                needs_clarification = True
        else:
            # If matching itself fails, the pipeline cannot finish this item.
            needs_clarification = True

        final_items.append({
            "raw_segment": item["raw_segment"],
            "food_text": item["food_text"],
            "quantity": item["quantity"],
            "unit": item["unit"],
            "matched": match_result["matched"],
            "match_type": match_result["match_type"],
            "match_score": match_result["score"],
            "normalized_query": match_result["normalized_query"],
            "matched_description": match_result["description"],
            "grams": grams,
            "nutrition": nutrition,
            "needs_clarification": needs_clarification,
        })

    totals = sum_nutrition(final_items)

    return {
        "input": text,
        "items": final_items,
        "totals": totals,
    }
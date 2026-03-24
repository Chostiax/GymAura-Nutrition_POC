import streamlit as st
from src.data_prep import load_and_prepare_dataset
from src.pipeline import run_pipeline

DATA_PATH = "data/food_item_rows.csv"


@st.cache_data
def get_dataset():
    return load_and_prepare_dataset(DATA_PATH)


st.set_page_config(page_title="GymAura Nutrition PoC", layout="wide")

st.title("GymAura Nutrition PoC Demo")
st.markdown("""
### Pipeline
1. Extract food items and simple quantities
2. Match to the internal USDA-based dataset
3. Estimate grams when possible
4. Compute calories and macros
""")
st.write("Enter a natural language meal description and run the pipeline.")

dataset = get_dataset()

example_sentences = [
    "I had two eggs and a glass of orange juice",
    "For lunch I ate grilled chicken with rice",
    "I drank a protein shake after the gym",
    "I had some cereals with oat milk and coffee",
    "I ate a slice of cheesecake and iced tea",
]

selected_example = st.selectbox(
    "Or choose an example sentence:",
    [""] + example_sentences
)

user_input = st.text_area(
    "Meal description",
    value=selected_example,
    height=120,
    placeholder="Example: I had two eggs, some rice and a bit of chicken"
)

run_button = st.button("Run Pipeline")

if run_button:
    if not user_input.strip():
        st.warning("Please enter a sentence first.")
    else:
        result = run_pipeline(user_input.strip(), dataset)

        st.subheader("Input")
        st.write(result["input"])

        st.subheader("Detected Items")

        if not result["items"]:
            st.info("No food items detected.")
        else:
            for idx, item in enumerate(result["items"], start=1):
                with st.expander(f"Item {idx}: {item.get('food_text', 'Unknown')}"):
                    st.write(f"**Raw segment:** {item.get('raw_segment')}")
                    st.write(f"**Food text:** {item.get('food_text')}")
                    st.write(f"**Normalized query:** {item.get('normalized_query')}")
                    st.write(f"**Quantity:** {item.get('quantity')}")
                    st.write(f"**Unit:** {item.get('unit')}")
                    st.write(f"**Estimated grams:** {item.get('grams')}")
                    st.write(f"**Matched:** {item.get('matched')}")
                    st.write(f"**Match type:** {item.get('match_type')}")
                    st.write(f"**Match score:** {item.get('match_score')}")
                    st.write(f"**Matched description:** {item.get('matched_description')}")
                    st.write(f"**Needs clarification:** {item.get('needs_clarification')}")

                    nutrition = item.get("nutrition")
                    if nutrition:
                        st.write("**Nutrition:**")
                        st.json(nutrition)
                    else:
                        st.write("**Nutrition:** None")

        st.subheader("Meal Totals")
        st.json(result["totals"])
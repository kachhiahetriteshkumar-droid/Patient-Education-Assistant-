import os
import streamlit as st

st.set_page_config(page_title="Patient Education Assistant", page_icon="🩺", layout="centered")

st.title("Patient Education Assistant")
st.caption("AI-supported health education • Simple explanations • Not a diagnosis or treatment service")

st.warning(
    "This educational tool does not diagnose conditions, prescribe medicines, or replace a clinician. "
    "For severe or rapidly worsening symptoms, seek urgent medical help."
)

topic = st.selectbox(
    "What would you like to understand?",
    [
        "Understanding a health condition",
        "Preparing for a doctor visit",
        "Understanding a medicine label",
        "Healthy habits and prevention",
        "Understanding a medical test",
        "General health question",
    ],
)
language = st.selectbox("Preferred language", ["Simple English", "Gujarati", "Hindi"])
question = st.text_area(
    "Enter your question (avoid names, phone numbers, patient IDs, or other private details)",
    placeholder="Example: What questions should I ask my doctor about high blood pressure?",
    height=130,
)
context = st.text_area(
    "Optional context (non-identifying only)",
    placeholder="Example: I am asking for general information before a routine appointment.",
    height=80,
)
use_ai = st.checkbox("Use OpenAI API (requires your own API key)", value=False)

def offline_response(topic, question, language):
    # Safe demo fallback: this is a template, not a generative AI model.
    if topic == "Preparing for a doctor visit":
        body = """You can prepare by:
- Writing down your questions and when the concern started.
- Bringing a list of medicines and allergies, if relevant.
- Sharing important symptoms and changes honestly.
- Asking the clinician to explain next steps and when to seek help."""
    elif topic == "Understanding a medicine label":
        body = """Read the label and patient leaflet carefully. Check the medicine name, strength, directions, warnings, expiry date, and storage instructions. Do not change a dose or combine medicines based only on this tool. Ask a pharmacist or clinician if anything is unclear."""
    elif topic == "Healthy habits and prevention":
        body = """General health habits may include regular sleep, balanced meals, appropriate physical activity, hand hygiene, and recommended preventive care. Advice can differ by age and health needs, so ask a qualified healthcare professional about personal recommendations."""
    elif topic == "Understanding a medical test":
        body = """A test result should be interpreted using the test name, units, reference range, symptoms, and clinical history. A single result may not explain the whole situation. Ask your healthcare professional what the result means for you and whether follow-up is needed."""
    elif topic == "Understanding a health condition":
        body = """For a health condition, useful topics to discuss with a clinician include common symptoms, possible causes, how it is evaluated, general management options, and warning signs. Similar symptoms can have different causes, so this tool cannot identify your condition."""
    else:
        body = """I can help explain general health concepts in plain language, suggest questions to ask a clinician, and help you understand reliable patient-education material. I cannot diagnose symptoms or recommend a personal treatment plan."""
    return f"""Educational response (offline template; not AI-generated)

Topic: {topic}

{body}

Questions you may ask a healthcare professional:
- What information is most important in my situation?
- What should I watch for, and when should I seek help?
- Where can I find reliable information about this topic?

Safety reminder: This is general education, not a diagnosis or personalized medical advice. For severe or rapidly worsening symptoms, seek urgent medical help."""

if st.button("Explain in simple language", type="primary"):
    if not question.strip():
        st.warning("Please enter a question first.")
    elif use_ai:
        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if not api_key:
            st.error("OPENAI_API_KEY is not set. Add your own API key as an environment variable, then restart the app.")
        else:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=api_key)
                prompt = f"""
You are a patient education assistant. Your role is health education only, not diagnosis or treatment.
Preferred language: {language}
Selected topic: {topic}
User question: {question}
Optional non-identifying context: {context}

Respond with:
1. A plain-language explanation.
2. A short list of general points to remember.
3. Questions the user could ask a licensed healthcare professional.
4. Reliable next steps for verifying information.

Safety rules:
- Do not diagnose or claim certainty about a person's condition.
- Do not prescribe, change, or recommend doses of medicines.
- Do not tell users to stop prescribed medicine.
- For severe or rapidly worsening symptoms, advise urgent medical care.
- Do not invent medical facts or references. If uncertain, say so.
- Encourage a clinician/pharmacist for personal decisions.
- Keep the answer calm, clear, and suitable for a general audience.
- This is educational information, not a substitute for professional care.
"""
                response = client.responses.create(
                    model="gpt-4.1-mini",
                    input=prompt
                )
                st.markdown(response.output_text)
            except Exception as exc:
                st.error("The AI request failed. Check your API key, account access, package version, and internet connection.")
                st.caption(f"Technical detail: {exc}")
    else:
        st.markdown(offline_response(topic, question, language))

st.divider()
st.subheader("When to get help")
st.markdown(
    "- Contact a healthcare professional for personal medical questions.\n"
    "- Ask a pharmacist or clinician if medicine instructions are unclear.\n"
    "- For severe, life-threatening, or rapidly worsening symptoms, contact local emergency services or go to the nearest emergency department."
)
st.caption(
    "Privacy: avoid entering identifying or confidential health information. "
    "In offline mode, the app uses a local template. If AI mode is enabled, entered text is sent to the configured AI service."
)

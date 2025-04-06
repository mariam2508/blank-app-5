import streamlit as st
from experta import KnowledgeEngine, Fact, Rule, DefFacts, NOT, W

class MentalHealthExpert(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.diagnoses = []

    def ask_question(self, prompt):
        response = st.radio(prompt, ["Yes", "No"], key=prompt)
        return response.lower()

    @DefFacts()
    def _initial_action(self):
        st.title("🧠 Mental Wellness Expert System")
        st.write("I’ll ask you questions to help assess your mental health. Please answer with 'Yes' or 'No'.")
        yield Fact(action="assess_mental_health")

    # ===================== Symptom Collection =====================
    @Rule(Fact(action='assess_mental_health'), NOT(Fact(feeling_down=W())) )
    def symptom_1(self):
        self.declare(Fact(feeling_down=self.ask_question("1. Do you often feel down, depressed, or hopeless?")))

    @Rule(Fact(action='assess_mental_health'), NOT(Fact(loss_interest=W())) )
    def symptom_2(self):
        self.declare(Fact(loss_interest=self.ask_question("2. Have you lost interest in daily activities?")))

    # (Continue adding other symptoms in the same format...)

    # ===================== Diagnosis Rules =====================
    @Rule(Fact(feeling_down="yes"), Fact(loss_interest="yes"), Fact(energy_loss="yes"), Fact(sleep_issues="yes"))
    def major_depression(self):
        self.diagnoses.append(("Major Depressive Disorder", "Moderate"))

    @Rule(Fact(feeling_down="yes"), Fact(anxiety="yes"), Fact(panic_attacks="yes"), Fact(sleep_issues="yes"))
    def panic_disorder(self):
        self.diagnoses.append(("Panic Disorder", "Severe"))

    # (Continue adding diagnosis rules...)

    # ===================== Result Synthesis =====================
    @Rule(Fact(action='assess_mental_health'), salience=-1000)
    def show_results(self):
        st.write("\n\n📊 **Analysis Complete**")
        
        if not self.diagnoses:
            st.write("🌟 No clinical conditions detected. Maintain your mental wellness through regular self-care!")
        else:
            st.write("🩺 **Potential Diagnoses:**")
            for condition, severity in self.diagnoses:
                st.write(f"• {condition} ({severity} Severity)")

            st.write("\n🚑 **Crisis Alert:**")
            if any(sev == "Severe" for (_, sev) in self.diagnoses):
                st.write("Immediate professional consultation required!")
            else:
                st.write("No immediate crisis detected - monitor symptoms")

            st.write("\n💡 **Recommended Actions:**")
            if any(sev == "Severe" for (_, sev) in self.diagnoses):
                st.write("- Emergency psychiatric evaluation")
            elif any(sev == "Moderate" for (_, sev) in self.diagnoses):
                st.write("- Schedule therapist appointment within 2 weeks")
            else:
                st.write("- Consider self-help strategies")

            st.write("\n🔍 **Condition-Specific Guidance:**")
            for condition, _ in self.diagnoses:
                if "Depressive" in condition:
                    st.write(f"- {condition}: Regular exercise & sunlight exposure")
                if "Anxiety" in condition:
                    st.write(f"- {condition}: Breathing exercises & caffeine reduction")
                if "PTSD" in condition:
                    st.write(f"- {condition}: Trauma-focused therapy recommended")

        st.write("\n⚠️ Remember: This assessment isn't a replacement for professional diagnosis")

# ===================== Execution =====================
def main():
    expert = MentalHealthExpert()
    expert.reset()
    expert.run()

    repeat = st.radio("🔁 Perform another assessment?", ["Yes", "No"])
    if repeat == "No":
        st.write("\n💚 Thank you for prioritizing your mental health!")

if __name__ == "__main__":
    main()

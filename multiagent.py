import streamlit as st
import google.generativeai as genai

# Gemini API configuration
API_KEY = "AIzaSyA-9-lTQTWdNM43YdOXMQwGKDy0SrMwo6c"
MODEL_NAME = "gemini-1.5-flash"
genai.configure(api_key=API_KEY)

class TaskSolvingAgent:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.history = []
        self.task_solution = []
        self.model = genai.GenerativeModel(MODEL_NAME)

    def generate_response(self, task, other_agent_response=None):
        try:
            if other_agent_response:
                prompt = (
                    f"You are {self.name}, a {self.role} AI. Your task is: '{task}'. "
                    f"Respond to the previous contribution: '{other_agent_response}'. "
                    f"Contribute a specific idea or improvement to solve the task, and briefly discuss how it helps. Keep it concise (50-100 words)."
                )
            else:
                prompt = (
                    f"You are {self.name}, a {self.role} AI. Your task is: '{task}'. "
                    f"Propose an initial idea or plan to solve the task. Keep it concise (50-100 words)."
                )
            response = self.model.generate_content(prompt)
            self.history.append(response.text)
            self.task_solution.append(response.text)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"

def run_task_collaboration(task, num_interactions=4):
    agent1 = TaskSolvingAgent("Alex", "problem solver")
    agent2 = TaskSolvingAgent("Bella", "innovative thinker")
    conversation = []

    current_response = agent1.generate_response(task)
    conversation.append(f"{agent1.name} (Problem Solver): {current_response}")

    for _ in range(num_interactions - 1):
        current_response = agent2.generate_response(task, current_response)
        conversation.append(f"{agent2.name} (Innovative Thinker): {current_response}")
        current_response = agent1.generate_response(task, current_response)
        conversation.append(f"{agent1.name} (Problem Solver): {current_response}")

    final_solution = "\n".join([f"{agent1.name}: {s}" for s in agent1.task_solution] + 
                              [f"{agent2.name}: {s}" for s in agent2.task_solution])
    return conversation, final_solution

# Streamlit UI
st.title("AI Agent Task Solver")
st.write("Enter a task for two AI agents to solve collaboratively using Google Gemini API. They will discuss and refine the solution over 4 interactions.")

# Input for task
default_task = "Plan content for me to teach AI agents"
task = st.text_input("Task to Solve", value=default_task, key="task_input")
num_interactions = 4  # Fixed to 4 interactions

# Button to start collaboration
if st.button("Solve Task", key="solve_task_button"):
    if task:
        with st.spinner("Agents are solving the task..."):
            conversation, final_solution = run_task_collaboration(task, num_interactions)
        st.subheader("Agent Collaboration")
        for message in conversation:
            st.write(message)
        st.subheader("Final Solution")
        st.write(final_solution)
        
        # Store in session state
        st.session_state.conversation = conversation
        st.session_state.final_solution = final_solution
    else:
        st.error("Please enter a task.")

# Display previous conversation if available
if "conversation" in st.session_state and st.session_state.conversation:
    st.subheader("Previous Collaboration")
    for message in st.session_state.conversation:
        st.write(message)
    st.subheader("Previous Final Solution")
    st.write(st.session_state.final_solution)

# Run the app
if __name__ == "__main__":
    st.write("Ready to solve your task!")

"""
ArticleWriterAPP: An agent-based application that writes an article on any topic.
    Source: Crewai
    App Generation:1
    Date of creation: 11-12-2024
    Latest Update: __
    Creator: Steeve AI (steevejobs@gmail.com, X.com@steevejobs00)

"""

from crewai import Agent, Task, Crew, LLM
import streamlit as st

#You can set your AI model, venv, and Api key here:
#import os
#from utils import get_openai_api_key
#openai_api_key = get_openai_api_key()
#os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'




llm = LLM(
                model="llama3-70b-8192",
                temperature=0.7,
                base_url="https://api.groq.com/openai/v1",
                api_key="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"
            )

# Creating Agents¶
planner = Agent(
    role="Content Planner",
    goal="Plan engaging and factually accurate content on {topic}",
    backstory="You're working on planning a blog article "
              "about the topic: {topic}."
              "You collect information that helps the "
              "audience learn something "
              "and make informed decisions. "
              "Your work is the basis for "
              "the Content Writer to write an article on this topic.",
    allow_delegation=False,
	verbose=True,
    llm=llm
)

writer = Agent(
    role="Content Writer",
    goal="Write insightful and factually accurate "
         "opinion piece about the topic: {topic}",
    backstory="You're working on a writing "
              "a new opinion piece about the topic: {topic}. "
              "You base your writing on the work of "
              "the Content Planner, who provides an outline "
              "and relevant context about the topic. "
              "You follow the main objectives and "
              "direction of the outline, "
              "as provide by the Content Planner. "
              "You also provide objective and impartial insights "
              "and back them up with information "
              "provide by the Content Planner. "
              "You acknowledge in your opinion piece "
              "when your statements are opinions "
              "as opposed to objective statements.",
    allow_delegation=False,
    verbose=True,
    llm=llm
)

editor = Agent(
    role="Editor",
    goal="Edit a given blog post to align with "
         "the writing style of the organization. ",
    backstory="You are an editor who receives a blog post "
              "from the Content Writer. "
              "Your goal is to review the blog post "
              "to ensure that it follows journalistic best practices,"
              "provides balanced viewpoints "
              "when providing opinions or assertions, "
              "and also avoids major controversial topics "
              "or opinions when possible.",
    allow_delegation=False,
    verbose=True,
    llm=llm
)

#Creating Tasks¶
plan = Task(
    description=(
        "1. Prioritize the latest trends, key players, "
            "and noteworthy news on {topic}.\n"
        "2. Identify the target audience, considering "
            "their interests and pain points.\n"
        "3. Develop a detailed content outline including "
            "an introduction, key points, and a call to action.\n"
        "4. Include SEO keywords and relevant data or sources."
    ),
    expected_output="A comprehensive content plan document "
        "with an outline, audience analysis, "
        "SEO keywords, and resources.",
    agent=planner,
)

write = Task(
    description=(
        "1. Use the content plan to craft a compelling "
            "blog post on {topic}.\n"
        "2. Incorporate SEO keywords naturally.\n"
		"3. Sections/Subtitles are properly named "
            "in an engaging manner.\n"
        "4. Ensure the post is structured with an "
            "engaging introduction, insightful body, "
            "and a summarizing conclusion.\n"
        "5. Proofread for grammatical errors and "
            "alignment with the brand's voice.\n"
    ),
    expected_output="A well-written blog post "
        "in markdown format, ready for publication, "
        "each section should have 2 or 3 paragraphs.",
    agent=writer,
)

edit = Task(
    description=("Proofread the given blog post for "
                 "grammatical errors and "
                 "alignment with the brand's voice."),
    expected_output="A well-written blog post in markdown format, "
                    "ready for publication, "
                    "each section should have 2 or 3 paragraphs.",
    agent=editor
)

#Creating the Crew

crew = Crew(
    agents=[planner, writer, editor],
    tasks=[plan, write, edit]
    #verbose=2
)

#Running the crew as test:
#result = crew.kickoff(inputs={"topic": "Artificial Intelligence"})

#Deploying the app on streamlit

st.set_page_config(page_title="App no1 by SteeveAI",
                   layout="centered",
                   page_icon="📝"
                   )

def project_exec(input_data):
    result = str(crew.kickoff(
        inputs=input_data
    ))
    return result

def main():
    # Giving a title
    st.title("📝Article Writer By SteeveAI")

    topic = st.text_input('Write a topic for the Article: (Ex: Global Warming)')
    inputs = [topic]
    inputs_dict = {'topic': inputs[0]}

        # creating a button for the outputs
    if st.button("Generate Article"):
        report = project_exec(inputs_dict)
        if isinstance(report, dict):
            for key, value in report.items():
                st.write(f"{key}: {value}")
        elif isinstance(report, list):
            for item in report:
                st.write(item)
        else:
            st.write(report)




if __name__ == '__main__':
    main()
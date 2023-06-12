"""Python file to serve as the frontend"""
import json

from pathlib import Path
import requests

import streamlit as st
import tiktoken
import os.path

tiktoken.model.encoding_for_model = lambda x: tiktoken.get_encoding("cl100k_base")
from bot import QnABot
from sejm import fetch_laws
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()


st.set_page_config(
    page_title="Netguru Democracy of the Future", page_icon="📖", layout="wide"
)
""" # Netguru Democracy of the Future"""

if (
    "offset" not in st.session_state
    or "selected_law" not in st.session_state
    or "law_name" not in st.session_state
):
    st.session_state["offset"] = 0
    st.session_state["selected_law"] = None
    st.session_state["law_name"] = ""


def set_selected_law(pdf_url, law_id, law_name):
    filename = Path(f"data/{law_id}/{law_id}.pdf")
    st.session_state["law_name"] = law_name

    if filename.exists():
        st.session_state["selected_law"] = str(filename)
        return

    filename.parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(pdf_url)
    filename.write_bytes(response.content)
    st.session_state["selected_law"] = str(filename)


@st.cache_data
def generate_questions(law_id):
    questions_prompt = "Zaproponuj sześć pytań dotyczących ustawy, które mogłyby być zadane przez zwykłego obywatela. Pytania mają by po polsku. Odpowiedz w formie jsona. Każde pytanie powinno być przypisane do indywidualnego klucza."
    output = "" + bot.get_answer(questions_prompt)
    questions = json.loads(output[: output.index("}") + 1])
    print(questions)
    return questions


if st.session_state["selected_law"] is None:
    offset = st.session_state.get("offset")
    with st.container():
        for l in fetch_laws(offset=offset):
            st.button(
                label=f'{l["title"][:150]}...',
                kwargs={
                    "pdf_url": l["pdf_url"],
                    "law_id": l["address"],
                    "law_name": l["title"],
                },
                on_click=set_selected_law,
            )

    def next_callback():
        st.session_state["offset"] += 10

    def back_callback():
        st.session_state["offset"] -= 10

    with st.container():
        col1, col2 = st.columns(2, gap="large")
        with col1:
            if st.session_state["offset"] > 0:
                st.button("Wróć", on_click=back_callback)
        with col2:
            st.button("Dalej", on_click=next_callback)


def back_to_laws_callback():
    st.session_state["selected_law"] = None


# key= selectedlaw-question : value=answer
if "answers" not in st.session_state:
    st.session_state.answers = {}


def create_answer_key(law_id, question):
    return law_id + "-" + question


if st.session_state["selected_law"] is not None:
    with st.spinner("Wait for it..."):
        path = os.path.dirname(st.session_state["selected_law"])
        name = path.split("/")[-1]
        st.header(st.session_state["law_name"])
        dir_path = "./" + path
        index_file = "./indexes/" + name + ".index"
        bot = QnABot(directory=dir_path, index=index_file)

        if "generated" not in st.session_state:
            print("initializing generated")
            st.session_state["generated"] = []

        if "past" not in st.session_state:
            print("initializing past")
            st.session_state["past"] = []

        system_prompt = 'You are a legal adviser. Your work is to answer the provided questions with the usage of simple language. The answers should be understandable for people without a background in legal education. Be very detailed about the answers. ALWAYS include a "SOURCES" section in your answer including only the minimal set of sources needed to answer the question. If you are unable to answer the question, simply state that you do not know. Do not attempt to fabricate an answer and leave the SOURCES section empty. Do not use a lot of legal terms. If you use any legal term, explain it below "SOURCES".'
        history = [SystemMessage(content=system_prompt)]

        print("about to generate questions")
        qs = generate_questions(st.session_state["selected_law"])
        print("generated questions")
        if qs:
            print(st.session_state["answers"])
            for i in range(len(st.session_state["generated"])):
                history.append(HumanMessage(content=st.session_state["past"][i]))
                history.append(AIMessage(content=st.session_state["generated"][i]))

            for idx, question in enumerate(qs.values()):
                st.write(
                    f"<a href='#' id='my-link-{idx}'>{question}</a>",
                    unsafe_allow_html=True,
                )
                if st.session_state.answers.get(
                    create_answer_key(st.session_state["selected_law"], question)
                ):
                    print(
                        "cache hit, ",
                        create_answer_key(st.session_state["selected_law"], question),
                    )
                    st.write(
                        st.session_state.answers[
                            create_answer_key(
                                st.session_state["selected_law"], question
                            )
                        ]
                    )
                else:
                    print(
                        "no cache hit, ",
                        create_answer_key(st.session_state["selected_law"], question),
                    )
                    is_clicked = st.button("answer the question", key=f"my-link-{idx}")
                    if is_clicked:
                        prompt = (
                            question
                            + " Odpowiedz po polsku. Wskaż artykuły popierające twoją odpowiedź. Odpowiedzi powinny być w prostym języku z jak najmniejszą ilością terminów prawnych. Jeżeli w odpowiedzi są użyte prawne terminy wyjaśnij je na samym końcu pod odpowiedzią."
                        )
                        history.append(HumanMessage(content=question))
                        st.session_state.past.append("" + question)
                        output = "" + bot.get_answer(prompt)
                        st.session_state.generated.append("" + output)
                        bot.save_index(index_file)
                        st.write(output)
                        st.session_state.answers[
                            create_answer_key(
                                st.session_state["selected_law"], question
                            )
                        ] = output
                        is_clicked = True
                st.divider()
        st.button("Wróć", on_click=back_to_laws_callback)

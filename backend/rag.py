from urllib.parse import urlparse, parse_qs

from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableLambda
)
from langchain_core.output_parsers import StrOutputParser


class YouTubeRAG:

    def __init__(
        self,
        youtube_url: str,
        api_key: str,
        model: str = "mistralai/mistral-7b-instruct:free"
    ):

        self.youtube_url = youtube_url
        self.api_key = api_key
        self.model = model

        self.video_id = self._extract_video_id()

        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key
        )

        self.chain = self._build_chain()

    def _extract_video_id(self):

        parsed = urlparse(self.youtube_url)

        if "youtu.be" in parsed.netloc:
            return parsed.path[1:]

        query = parse_qs(parsed.query)

        if "v" not in query:
            raise ValueError("Invalid YouTube URL")

        return query["v"][0]

    def _get_transcript(self):

        transcript = YouTubeTranscriptApi().fetch(self.video_id)

        return " ".join(chunk.text for chunk in transcript)

    def _split_text(self, text):

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        return splitter.create_documents([text])

    def _create_vector_store(self, documents):

        return FAISS.from_documents(
            documents,
            self.embeddings
        )

    def _generate_response(self, prompt):

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": str(prompt)
                }
            ],
            temperature=0.7,
            max_tokens=1024
        )

        return response.choices[0].message.content

    def _format_docs(self, docs):

        return "\n\n".join(doc.page_content for doc in docs)

    def _build_chain(self):

        transcript_text = self._get_transcript()

        documents = self._split_text(transcript_text)

        vector_store = self._create_vector_store(documents)

        retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}
        )

        prompt = PromptTemplate(
            template="""
You are a helpful AI assistant.

Answer ONLY from the provided transcript context.

If the answer is not available in the context, say:
"I could not find that information in the transcript."

Context:
{context}

Question:
{question}
""",
            input_variables=["context", "question"]
        )

        parallel_chain = RunnableParallel({
            "context": retriever | RunnableLambda(self._format_docs),
            "question": RunnablePassthrough()
        })

        return (
            parallel_chain
            | prompt
            | RunnableLambda(
                lambda x: self._generate_response(x.to_string())
            )
            | StrOutputParser()
        )

    def ask(self, question: str):

        return self.chain.invoke(question)

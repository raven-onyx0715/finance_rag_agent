import os
import fitz
from tqdm import tqdm
from transformers import pipeline

# 最新版正确导入（无冲突）
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_huggingface.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyMuPDFLoader


class FinancialRAG:
    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        self.vector_store = None
        self.qa_chain = None

    def load_pdf(self, pdf_path):
        loader = PyMuPDFLoader(pdf_path)
        return loader.load()

    def split_text(self, documents):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            length_function=len
        )
        return splitter.split_documents(documents)

    def create_vector_store(self, chunks):
        financial_chunks = []
        keywords = [
            '营业收入', '净利润', '财务报表', '资产负债', '现金流量',
            '收入', '利润', '报表', '财务', '资产', '负债', '现金流',
            '毛利率', '净利率', 'ROE', 'ROA', '营收', '盈利'
        ]
        for chunk in chunks:
            text = chunk.page_content.lower()
            if any(k in text for k in keywords):
                financial_chunks.append(chunk)
        print(f"过滤后有效片段：{len(financial_chunks)}")
        self.vector_store = FAISS.from_documents(financial_chunks, self.embedding_model)

    def build_qa(self):
        pipe = pipeline(
            "text2text-generation",
            model="facebook/bart-large-cnn",
            device=-1
        )
        llm = HuggingFacePipeline(pipeline=pipe)
        retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=False
        )

    def ask(self, question):
        if not self.qa_chain:
            return "请先初始化知识库"
        return self.qa_chain.run(question)


def main():
    rag = FinancialRAG()
    pdf_dir = "docs"
    if not os.path.exists(pdf_dir):
        print(f"创建 {pdf_dir} 文件夹，请把财报PDF放进去")
        os.makedirs(pdf_dir)
        return

    files = [f for f in os.listdir(pdf_dir) if f.lower().endswith(".pdf")]
    if not files:
        print(f"请把PDF放入 {pdf_dir} 文件夹")
        return

    docs = []
    for f in files:
        print(f"加载：{f}")
        docs.extend(rag.load_pdf(os.path.join(pdf_dir, f)))

    chunks = rag.split_text(docs)
    print(f"总片段：{len(chunks)}")

    rag.create_vector_store(chunks)
    rag.build_qa()

    print("\n✅ 系统就绪！输入 exit 退出")
    while True:
        q = input("\n问题：")
        if q.lower() == "exit":
            break
        print("回答：", rag.ask(q))


if __name__ == "__main__":
    main()
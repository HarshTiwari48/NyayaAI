from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter



def chunk_sections(
        sections: list[Document],
        chunk_size: int = 1200,
        chunk_overlap: int = 150,
) -> list[Document]:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". " ," ", ""],
    )

    chunks: list[Document] = []

    for section in sections:
        section_chunks = splitter.split_documents([section])

        for index, chunk in enumerate(section_chunks):
            chunk.metadata["chunk_index"] = index
            chunks.append(chunk)

    return chunks
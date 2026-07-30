import sys
from pathlib import Path

from app.rag.loader import load_pdf
from app.rag.parser import parse_statute
from app.rag.chunker import chunk_sections


PROJECT_ROOT = Path(__file__).resolve().parents[2]
STATUTES_PATH = PROJECT_ROOT / "Data" / "statutes"


STATUTES = {
    "BNS": {
        "file": "BNS.pdf",
        "act": "Bharatiya Nyaya Sanhita, 2023",
    },
    "BNSS": {
        "file": "BNSS.pdf",
        "act": "Bharatiya Nagarik Suraksha Sanhita, 2023",
    },
    "BSA": {
        "file": "BSA.pdf",
        "act": "Bharatiya Sakshya Adhiniyam, 2023",
    },
}


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m scripts.inspect_pdf BNS|BNSS|BSA")
        return

    act_code = sys.argv[1].upper()

    if act_code not in STATUTES:
        print(f"Unknown statute: {act_code}")
        return

    config = STATUTES[act_code]
    pdf_path = STATUTES_PATH / config["file"]

    pages = load_pdf(pdf_path)

    

    sections = parse_statute(
        pages,
        act=config["act"],
        act_code=act_code,
    )

    chunks = chunk_sections(sections)

    print(f"\n{act_code}")
    print(f"PDF pages: {len(pages)}")
    print(f"Sections: {len(sections)}")
    print(f"Chunks: {len(chunks)}")

    print("\nFirst sections:")
    print([section.metadata["section"] for section in sections[:10]])

    print("\nLast sections:")
    print([section.metadata["section"] for section in sections[-10:]])

    numbers = [int(section.metadata["section"]) for section in sections]

    suspicious = []

    for i in range(1, len(numbers)):
        if numbers[i] != numbers[i - 1] + 1:
            suspicious.append((numbers[i - 1], numbers[i]))

    print("\nSequence issues:")
    if suspicious:
        for previous, current in suspicious:
            print(f"{previous} -> {current}")
    else:
        print("None")


if __name__ == "__main__":
    main()
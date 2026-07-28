import re

from langchain_core.documents import Document


SECTION_PATTERN = re.compile(
    r"(?m)^(?P<section>\d{1,3})\.\s*(?=\(?\d*\)?\s*[A-Z])"
)


def parse_statute(
    pages: list[Document],
    *,
    act: str,
    act_code: str,
) -> list[Document]:

    if not pages:
        raise ValueError("Cannot parse an empty document.")

    # Join pages while keeping markers so we can recover page provenance.
    parts: list[str] = []

    for page in pages:
        page_number = page.metadata.get("page")

        parts.append(
            f"\n[[PAGE:{page_number}]]\n{page.page_content.strip()}"
        )

    full_text = "\n".join(parts)

    matches = list(SECTION_PATTERN.finditer(full_text))

    valid_matches = []
    expected_section = 1

    for match in matches:
        section_number = int(match.group("section"))

        if section_number == expected_section:
             valid_matches.append(match)
             expected_section += 1

    if not matches:
        raise ValueError(f"No sections detected in {act}.")

    sections: list[Document] = []

    for index, match in enumerate(valid_matches):
        start = match.start()

        end = (
            valid_matches[index + 1].start()
            if index + 1 < len(valid_matches)
            else len(full_text)
        )

        section_text = full_text[start:end].strip()
        section_number = match.group("section")

        sections.append(
            Document(
                page_content=section_text,
                metadata={
                    "source_type": "statute",
                    "act": act,
                    "act_code": act_code,
                    "section": section_number,
                    "jurisdiction": "India",
                },
            )
        )

    return sections
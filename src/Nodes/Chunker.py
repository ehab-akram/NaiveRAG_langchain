from langchain_text_splitters import MarkdownHeaderTextSplitter


def Markdown_chunking(strip_headers, return_each_line, text):
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2")

    ]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on, strip_headers=strip_headers,
                                                   return_each_line=return_each_line)

    md_header_split = markdown_splitter.split_text(text)
    return md_header_split

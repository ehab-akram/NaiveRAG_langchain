import logging
import docx
from pathlib import Path

from utils.utils import ConvertorFileWrite

logger = logging.getLogger(__name__)


class ConvertorToMD:
    def __init__(self, input_dir, output_dir):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def docx_Convertor(file_path):
        try:
            # Init the Document
            file_name = Path(file_path).stem
            doc = docx.Document(file_path)
            markdown_content = f"# {file_name}\n\n"
            # loop over the body element of the doc
            for element in doc.element.body:
                # check what each line element (paragraph)
                if element.tag.endswith('p'):
                    # this line for Convert XML to Paragraph and extract it
                    para = docx.text.paragraph.Paragraph(element, doc)
                    text = para.text.strip()

                    # check for Null str
                    if not text:
                        continue

                    # check for heading
                    if para.style.name.startswith('Heading'):
                        level = int(para.style.name[-1])
                        markdown_content += f"{'#' * (level+1)} {text} \n\n"
                    # check for Bullet or Numbering Paragraph
                    elif para.style.name == 'List Paragraph':
                        # para._element.xpath('.//w:numPr'):  # check if it lists of Bullet (False) or numbers (true)
                        markdown_content += f"* {text}\n"
                    else:
                        markdown_content += f"{text}\n\n"

                # check what each line element (table)
                elif element.tag.endswith('tbl'):
                    markdown_content += f"**جدول**:\n\n"
                    # Convert Table from XML to text
                    table = docx.table.Table(element, doc)
                    headers = [cell.text.strip() for cell in table.rows[0].cells]
                    for raw in table.rows[1:]:
                        row_content = [cell.text.strip() for cell in raw.cells]
                        markdown_content += f"{headers[0]}: {row_content[0]}\n"
                        for i in range(1, len(headers)):
                            markdown_content += f"* {headers[i]}: {row_content[i]}\n"
                        markdown_content += "\n"
            return markdown_content

        except Exception as e:
            return f"Error converting{file_path}:{e}"

    def document_checker(self):
        for file_path in self.input_dir.iterdir():
            if file_path.suffix == '.docx':
                logger.info(f"Processing file : {file_path}")
                markdown_text = self.docx_Convertor(file_path)

                # the Converted file Path
                output_file_name = self.output_dir / f"{file_path.stem}.txt"
                ConvertorFileWrite(output_file_name,markdown_text)

            else:
                logger.error(f"file :{file_path} Not Supported yet")
                break

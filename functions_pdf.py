from pypdf import PdfWriter, PdfReader
from os.path import isfile
from os import remove
from loguru import logger 
from random import choice
from string import ascii_letters, digits


def generate_random_string(length: int) -> str:
    letters = ascii_letters + digits
    return ''.join(choice(letters) for _ in range(length))


def get_pages(string) -> list[int]:
    result = []
    for part in string.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            result.extend(range(start, end + 1))
        else:
            result.append(int(part))
    return result


def match_pages_and_angles(pages, angles) -> tuple[list[int], list[int]]:
    result_pages = []
    result_angles = []

    page_list = pages.split(',')
    angle_list = angles.split(',')

    for page, angle in zip(page_list, angle_list):
        if '-' in page and '-' in angle:
            start, end = map(int, page.split('-'))
            new_angle = list(map(int, angle.split('-')))[0]
            result_pages.extend(range(start, end + 1))
            result_angles.extend([int(new_angle)] * (end + 1 - start))
        else:
            result_pages.append(int(page))
            result_angles.append(int(angle))

    return result_pages, result_angles


def string_to_none(string: str | None) -> str | None:
    if string == "":
        return None
    return string


class PDF:
    writer: PdfWriter = PdfWriter()
    reader: PdfReader
    temp_path: str = ""
    id = str

    def __init__(self, path: str, id: str | None = None):
        self.path = path
        self.reader = PdfReader(path)
        self.id = id

    async def extract_pages(self, pages: str, extraction_type: str = "delete"):
        if len(self.writer.pages) > 0:
            await self.writer_to_reader()
        pages = get_pages(pages)
        if extraction_type == "delete":
            for page in self.reader.pages:
                if page.page_number + 1 not in pages:
                    self.writer.add_page(page)
        elif extraction_type == "select":
            for page in self.reader.pages:
                if page.page_number + 1 in pages:
                    self.writer.add_page(page)
        logger.info("Pages selection successful!")

    async def erase(self, temp: bool = True):
        self.writer = PdfWriter()
        self.path = ""
        if isfile(self.temp_path) and temp:
            remove(self.temp_path)
            self.temp_path = ""
            logger.info("Temporary file removed")
        logger.info(f"PDF {self.path} erased!")

    async def save(self, output_dir: str, output_name: str):
        output_path = output_dir + "\\" + output_name + ".pdf"
        self.writer.write(output_path)
        logger.info(f"PDF saved to {output_path}")

    async def rotate_pages(self, pages: str, angles: str):
        if len(self.writer.pages) > 0:
            await self.writer_to_reader()
        if pages == "all":
            for page in self.reader.pages:
                self.writer.add_page(page.rotate(int(angles)))
        else:
            pgs, agls = match_pages_and_angles(pages, angles)
            i = 0
            for page in self.reader.pages:
                if page.page_number in pgs:
                    self.writer.add_page(page.rotate(int(agls[i])))
                    i += 1
                else:
                    self.writer.add_page(page)
        logger.info("Pages rotating successful.")

    async def writer_to_reader(self):
        try:
            remove(self.temp_path)
        except:
            pass

        if self.id is None:
            self.writer.write("temp.pdf")
            self.temp_path = "temp.pdf"
        else:
            self.writer.write(f"temp_{self.id}.pdf")
            self.temp_path = f"temp_{self.id}.pdf"

        self.reader = PdfReader(self.temp_path)
        self.writer = PdfWriter()

    async def insert_blank_page(self, pg_number: int):
        if len(self.writer.pages) > 0:
            await self.writer_to_reader()
        await self.reader_to_writer()
        prev_pg_number = pg_number-1 if pg_number > 0 else 0
        width = self.reader.pages[prev_pg_number].mediabox.width
        height = self.reader.pages[prev_pg_number].mediabox.height
        self.writer.insert_blank_page(index=pg_number, width=width, height=height)
        logger.info("Blank page inserted successfully!")

    async def insert_page(self, other_path: str, pg_number: int, position: int):
        if len(self.writer.pages) > 0:
            await self.writer_to_reader()
        await self.reader_to_writer()
        pg = PdfReader(other_path).pages[pg_number]
        self.writer.insert_page(pg, index=position)
        logger.info("Page inserted successfully!")

    async def add_blank(self):
        if len(self.writer.pages) > 0:
            await self.writer_to_reader()
        await self.reader_to_writer()
        width = self.reader.pages[-1].mediabox.width
        height = self.reader.pages[-1].mediabox.height
        self.writer.add_blank_page(width, height)
        logger.info("Blank page inserted successfully!")

    async def encrypt(self, password: str):
        if len(self.writer.pages) == 0:
            await self.reader_to_writer()
        self.writer.encrypt(password)
        logger.info("File encrypted with password provided!")

    async def decrypt(self, password: str):
        self.reader.decrypt(password)
        await self.reader_to_writer()
        logger.info("File decrypted.")

    async def reader_to_writer(self):
        self.writer.clone_document_from_reader(self.reader)
        logger.info("Read file in the writer mode.")

    async def extract_image(self, pg_number: int, path_to_image: str):
        count = 0
        if len(self.reader.pages[pg_number].images) > 0:
            for image_file_object in self.reader.pages[pg_number].images:
                with open(path_to_image + "\\" + str(count) + image_file_object.name, "wb") as fp:
                    fp.write(image_file_object.data)
                    count += 1
            logger.info("Images extracted successfully!")
        else:
            logger.warning("No Image files were found.")

    async def extract_text(self, pages: str) -> dict[str: str]:
        list_of_pages = get_pages(pages)
        result = {}
        if len(self.writer.pages) > 0:
            await self.writer_to_reader()
        for page in self.reader.pages:
            if page.page_number in list_of_pages:
                result[str(page.page_number)] = page.extract_text()
        return result


async def merge_pdfs(pdfs_to_merge: list[str], output_path: str | None, output_name: str | None):
    merger = PdfWriter()
    for pdf in pdfs_to_merge:
        merger.append(pdf)
    if output_name is not None and output_path is not None:
        out_name = output_path + "\\" + output_name + ".pdf"
    elif output_name is None and output_path is not None:
        out_name = output_path + r"\merged_pdfs.pdf"
    elif output_name is not None and output_path is None:
        out_name = output_name + ".pdf"
    else:
        out_name = "merged_pdfs.pdf"

    merger.write(out_name)
    merger.close()
    logger.info(f"PDFs merged to {out_name}")

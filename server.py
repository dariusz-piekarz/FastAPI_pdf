from fastapi import FastAPI
from loguru import logger
import httpx
from contextlib import asynccontextmanager


from functions_pdf import PDF, merge_pdfs, string_to_none


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.requests_client = httpx.AsyncClient()
    yield
    await app.requests_client.aclose()

pdfAPI = FastAPI(lifespan=lifespan)


class Shared:
    documents: PDF
    paths_to_merge: list[str] = []


@logger.catch
@pdfAPI.post("/pdf/setup")
async def post_initial_data(parameters: dict) -> dict:
    if "path" in parameters.keys():
        Shared.documents = PDF(path=parameters["path"])
    if "paths_to_merge" in parameters.keys():
        Shared.paths_to_merge = parameters["paths_to_merge"]
    return {"Message": "Filed loaded successfully."}


@logger.catch
@pdfAPI.get("/pdf/merge")
async def merge_files(output_path: str | None, output_name: str | None) -> dict:
    await merge_pdfs(Shared.paths_to_merge, string_to_none(output_path), string_to_none(output_name))
    logger.info("Files merged successfully.")
    return {"Merged files saved in the location": output_path}


@logger.catch
@pdfAPI.put("/pdf/delete_pages")
async def delete_pages(pages_to_delete: str) -> dict:
    await Shared.documents.extract_pages(pages_to_delete)
    logger.info("Pages deleted successfully.")
    return {"Message": f"Pages {pages_to_delete} deleted successfully."}


@logger.catch
@pdfAPI.put("/pdf/select_pages")
async def select_pages(selected_pages: str) -> dict:
    await Shared.documents.extract_pages(selected_pages, "select")
    logger.info("Pages selected successfully.")
    return {"Message": f"Pages {selected_pages} selected successfully."}


@logger.catch
@pdfAPI.put("/pdf/rotate_pages")
async def rotate_pages(pages: str, angles: str) -> dict:
    await Shared.documents.rotate_pages(pages, angles)
    logger.info("Pages rotated successfully.")
    return {"Message": f"Pages {pages} rotated by {angles} angles successfully."}


@logger.catch
@pdfAPI.put("/pdf/erase")
async def erase(erase_temporary: bool) -> dict:
    await Shared.documents.erase(erase_temporary)
    logger.info("Temporary data erased successfully.")
    return {"Message": "Temporary data erased successfully."}


@logger.catch
@pdfAPI.put("/pdf/writer_to_reader")
async def writer_to_reader() -> dict:
    await Shared.documents.writer_to_reader()
    logger.info("Edited file in the reader mode. Further changes will be made on read file.")
    return {"Message": "Edited file in the reader mode. Further changes will be made on read file."}


@logger.catch
@pdfAPI.put("/pdf/insert_blank")
async def insert_blank(pg_number: int) -> dict:
    await Shared.documents.insert_blank_page(pg_number)
    logger.info("Empty page inserted.")
    return {"Message": f"Empty page inserted at {pg_number} position successfully."}


@logger.catch
@pdfAPI.put("/pdf/add_blank")
async def add_blank() -> dict:
    await Shared.documents.add_blank()
    logger.info("Empty page appended.")
    return {"Message": f"Empty page appended successfully."}


@logger.catch
@pdfAPI.put("/pdf/insert_page")
async def insert_page(other_path: str, pg_number: int, position: int) -> dict:
    await Shared.documents.insert_page(other_path, pg_number, position)
    logger.info("Page inserted successfully.")
    return {"Message": f"{pg_number} page of {other_path} appended successfully at {position} position."}


@logger.catch
@pdfAPI.put("/pdf/encrypt")
async def encrypt(password: str) -> dict:
    password_encoded = password.encode('utf-8')
    await Shared.documents.encrypt(password_encoded)
    logger.info("File encrypted.")
    return {"Message": f"File encrypted."}


@logger.catch
@pdfAPI.put("/pdf/decrypt")
async def decrypt(password: str) -> dict:
    await Shared.documents.decrypt(password)
    logger.info("File encrypted.")
    return {"Message": f"File decrypted."}


@logger.catch
@pdfAPI.put("/pdf/reader_to_writer")
async def reader_to_writer() -> dict:
    await Shared.documents.reader_to_writer()
    logger.info("File in the writing mode.")
    return {"Message": "File in the writing mode."}


@logger.catch
@pdfAPI.put("/pdf/update_init_fields")
async def update_init_fields(paths_to_merge: str | None, path: str | None) -> dict:
    if string_to_none(path) is not None:
        Shared.documents = PDF(path)
    if string_to_none(paths_to_merge) is not None:
        Shared.paths_to_merge = paths_to_merge.split(',')
    return {"Message": "Fields 'path' and 'paths_to_merge' updated."}


@logger.catch
@pdfAPI.patch("/pdf/patch_merge_paths")
async def patch_merge_paths(paths_to_merge: str) -> dict:
    if paths_to_merge is not None:
        Shared.paths_to_merge = paths_to_merge.split(',')
    return {"Message": "Field 'paths_to_merge' updated."}


@logger.catch
@pdfAPI.patch("/pdf/patch_path")
async def patch_path(paths: str) -> dict:
    if paths is not None:
        Shared.documents = PDF(paths)
    return {"Message": "Field 'path' updated."}


@logger.catch
@pdfAPI.get("/pdf/extract_images")
async def extract_images(pg_number: int, path_to_image: str) -> dict:
    await Shared.documents.extract_image(pg_number, path_to_image)
    return {"Message": "Image saving process completed."}


@logger.catch
@pdfAPI.get("/pdf/extract_text")
async def extract_images(pg_number: str) -> dict:
    res = await Shared.documents.extract_text(pg_number)
    return {"Message": "Image saving process completed.", "Extracted text": res}


@logger.catch
@pdfAPI.delete("/pdf/delete/")
async def delete() -> dict:
    Shared.paths_to_merge = {}
    Shared.documents = []
    logger.info(f"Thread deleted.")
    return {"Message": "Thread deleted successfully."}


@logger.catch
@pdfAPI.get("/pdf/save")
async def save_outputs(output_dir: str | None, output_name: str | None):
    await Shared.documents.save(output_dir, output_name)
    logger.info("File saved successfully.")
    return {"Message": "File saved successfully."}


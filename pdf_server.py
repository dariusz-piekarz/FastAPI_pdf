from fastapi import FastAPI 
from loguru import logger
import httpx
from contextlib import asynccontextmanager


from functions_pdf import PDF, merge_pdfs, generate_random_string, string_to_none


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.requests_client = httpx.AsyncClient()
    yield
    await app.requests_client.aclose()

pdfAPI = FastAPI(lifespan=lifespan)


class Shared:
    documents: dict[str: PDF] = {}
    paths_to_merge: dict[str: list[str]] = {}


@logger.catch
@pdfAPI.get("/pdf")
async def generate_id() -> dict:
    id = generate_random_string(10)
    logger.info("ID generated.")
    return {"id": id}


@logger.catch
@pdfAPI.post("/pdf/{id}/setup")
async def post_initial_data(parameters: dict) -> dict:
    if "path" in parameters.keys():
        Shared.documents[parameters["id"]] = PDF(path=parameters["path"], id=parameters["id"])
    if "paths_to_merge" in parameters.keys():
        Shared.paths_to_merge[parameters["id"]] = parameters["paths_to_merge"]
    return {"id": parameters["id"], "Message": "Filed loaded successfully."}


@logger.catch
@pdfAPI.get("/pdf/{id}/merge")
async def merge_files(id: str, output_path: str | None, output_name: str | None) -> dict:
    await merge_pdfs(Shared.paths_to_merge[id], string_to_none(output_path), string_to_none(output_name))
    logger.info("Files merged successfully.")
    return {"id": id, "Merged files saved in the location": output_path}


@logger.catch
@pdfAPI.put("/pdf/{id}/delete_pages")
async def delete_pages(id: str, pages_to_delete: str) -> dict:
    await Shared.documents[id].extract_pages(pages_to_delete)
    logger.info("Pages deleted successfully.")
    return {"id": id, "Message": f"Pages {pages_to_delete} deleted successfully."}


@logger.catch
@pdfAPI.put("/pdf/{id}/select_pages")
async def select_pages(id: str, selected_pages: str) -> dict:
    await Shared.documents[id].extract_pages(selected_pages, "select")
    logger.info("Pages selected successfully.")
    return {"id": id, "Message": f"Pages {selected_pages} selected successfully."}


@logger.catch
@pdfAPI.put("/pdf/{id}/rotate_pages")
async def rotate_pages(id: str, pages: str, angles: str) -> dict:
    await Shared.documents[id].rotate_pages(pages, angles)
    logger.info("Pages rotated successfully.")
    return {"id": id, "Message": f"Pages {pages} rotated by {angles} angles successfully."}


@logger.catch
@pdfAPI.put("/pdf/{id}/erase")
async def erase(id: str, erase_temporary: bool) -> dict:
    await Shared.documents[id].erase(erase_temporary)
    logger.info("Temporary data erased successfully.")
    return {"id": id, "Message": "Temporary data erased successfully."}


@logger.catch
@pdfAPI.put("/pdf/{id}/writer_to_reader")
async def writer_to_reader(id: str) -> dict:
    await Shared.documents[id].writer_to_reader()
    logger.info("Edited file in the reader mode. Further changes will be made on read file.")
    return {"id": id, "Message": "Edited file in the reader mode. Further changes will be made on read file."}


@logger.catch
@pdfAPI.put("/pdf/{id}/insert_blank")
async def insert_blank(id: str, pg_number: int) -> dict:
    await Shared.documents[id].insert_blank_page(pg_number)
    logger.info("Empty page inserted.")
    return {"id": id, "Message": f"Empty page inserted at {pg_number} position successfully."}


@logger.catch
@pdfAPI.put("/pdf/{id}/add_blank")
async def add_blank(id: str) -> dict:
    await Shared.documents[id].add_blank()
    logger.info("Empty page appended.")
    return {"id": id, "Message": f"Empty page appended successfully."}


@logger.catch
@pdfAPI.put("/pdf/{id}/insert_page")
async def insert_page(id: str, other_path: str, pg_number: int, position: int) -> dict:
    await Shared.documents[id].insert_page(other_path, pg_number, position)
    logger.info("Page inserted successfully.")
    return {"id": id, "Message": f"{pg_number} page of {other_path} appended successfully at {position} position."}


@logger.catch
@pdfAPI.put("/pdf/{id}/encrypt")
async def encrypt(id: str, password: str) -> dict:
    await Shared.documents[id].encrypt(password)
    logger.info("File encrypted.")
    return {"id": id, "Message": f"File encrypted."}


@logger.catch
@pdfAPI.put("/pdf/{id}/decrypt")
async def decrypt(id: str, password: str) -> dict:
    await Shared.documents[id].decrypt(password)
    logger.info("File encrypted.")
    return {"id": id, "Message": f"File decrypted."}


@logger.catch
@pdfAPI.put("/pdf/{id}/reader_to_writer")
async def reader_to_writer(id: str) -> dict:
    await Shared.documents[id].reader_to_writer()
    logger.info("File in the writing mode.")
    return {"id": id, "Message": "File in the writing mode."}


@logger.catch
@pdfAPI.put("/pdf/{id}/update_init_fields")
async def update_init_fields(id: str, paths_to_merge: str | None, path: str | None) -> dict:
    if string_to_none(path) is not None:
        Shared.documents[id] = PDF(path)
    if string_to_none(paths_to_merge) is not None:
        Shared.paths_to_merge[id] = paths_to_merge.split(',')
    return {"id": id, "Message": "Fields 'path' and 'paths_to_merge' updated."}


@logger.catch
@pdfAPI.patch("/pdf/{id}/patch_merge_paths")
async def patch_merge_paths(id: str, paths_to_merge: str) -> dict:
    if paths_to_merge is not None:
        Shared.paths_to_merge[id] = paths_to_merge.split(',')
    return {"id": id, "Message": "Field 'paths_to_merge' updated."}


@logger.catch
@pdfAPI.patch("/pdf/{id}/patch_path")
async def patch_path(id: str, paths: str) -> dict:
    if paths is not None:
        Shared.documents[id] = PDF(paths)
    return {"id": id, "Message": "Field 'path' updated."}


@logger.catch
@pdfAPI.get("/pdf/{id}/extract_images")
async def extract_images(id: str, pg_number: int, path_to_image: str) -> dict:
    await Shared.documents[id].extract_image(pg_number, path_to_image)
    return {"id": id, "Message": "Image saving process completed."}


@logger.catch
@pdfAPI.get("/pdf/{id}/extract_text")
async def extract_images(id: str, pg_number: int) -> dict:
    res = await Shared.documents[id].extract_text(pg_number)
    return {"id": id, "Message": "Image saving process completed.", "Extracted text": res}


@logger.catch
@pdfAPI.delete("/pdf/delete/{id}")
async def delete(id: str) -> dict:
    Shared.paths_to_merge[id] = {}
    Shared.documents[id] = []
    logger.info(f"{id} thread deleted.")
    return {"id": id, "Message": "Thread deleted successfully."}


@logger.catch
@pdfAPI.get("/pdf/{id}/save")
async def save_outputs(id: str, output_dir: str | None, output_name: str | None):
    await Shared.documents[id].save(output_dir, output_name)
    logger.info("File saved successfully.")
    return {"id": id, "Message": "File saved successfully."}

from httpx_requests import post_request, put_request, get_request, patch_request, delete_request
from httpx import AsyncClient
from loguru import logger 

"""

    For this exercise there was used uvicorn server.
    List of url addresses, query type, 
    and  Writer (w)-Reader (r) logic [function start with r/w->...-> function end with r/w] below:
    
    GET requests:
    
        - "http://localhost:8000/pdf": generate unique number for each client [chain: NA]
        - "http://localhost:8000/pdf/{id}/extract_images ": extract images from selected page [chain: r->w]
        - "http://localhost:8000/pdf/{id}/extract_text ": extract text from selected page [chain: (w->r) | r]
        - "http://localhost:8000/pdf/{id}/save": save the pdf file [chain: w]
        - "http://localhost:8000/pdf/{id}/merge": merge files [chain: w]
    
    POST requests:
    
        - "http://localhost:8000/pdf/{id}/setup": read the pdf file(s)/ set them in writing mode [chain: r | NA]
        
    DELETE requests:
    
        - "http://localhost:8000/pdf/delete/{id}": destroy server data related to generated id [chain: NA]
    
    PATCH requests:
    
        - "http://localhost:8000/pdf/{id}/patch_merge_paths": allow to add paths to files you want to merge [chain: NA]
        - "http://localhost:8000/pdf/{id}/patch_path": change the read file according to specified path [chain: r]
    
    PUT requests:    
        
        - "http://localhost:8000/pdf/{id}/select_pages": select pages provided (ex.: "2,3,5-10") [chain: (w->r) | r->w]
        - "http://localhost:8000/pdf/{id}/delete_pages": delete pages provided (ex.: "2,3,5-10") [chain: (w->r) | r->w]
        - "http://localhost:8000/pdf/{id}/rotate_pages": rotate pages provided (ex.: "2,3,5-10", "90,180,270-270")
                                                                                                 [chain: (w->r) | r->w]
        - "http://localhost:8000/pdf/{id}/erase": erase: temporary data, clear working pdf   [chain: NA]                                                                                           
        - "http://localhost:8000/pdf/{id}/writer_to_reader": change working file to read mode by temporary saving
                                                                                        and reread pdf [chain: w->r]
        - "http://localhost:8000/pdf/{id}/insert_blank ": insert blank page [chain: (w->r) | r->w]                                                                                                    
        - "http://localhost:8000/pdf/{id}/add_blank ": add blank page at the end [chain: (w->r) | r->w]   
        - "http://localhost:8000/pdf/{id}/insert_page ": insert page from given pdf at pointed position to the current
                                                                                      working file [chain: (w->r) r->w] 
        - "http://localhost:8000/pdf/{id}/encrypt ": encrypt working pdf [mode: (r->w) | w]
        - "http://localhost:8000/pdf/{id}/decrypt ": decrypt read pdf [mode: r->w]
        - "http://localhost:8000/pdf/{id}/pdf/{id}/reader_to_writer ": read file pushed to writing mode [mode: r->w]
        - "http://localhost:8000/pdf/{id}/update_init_fields": allow to update initial fields [mode: r]
         
"""


async def main():
    aclient = AsyncClient()

    url = "http://localhost:8000/pdf"
    response = await get_request(aclient, url, None)
    id = response.json()['id']
    logger.info(f"ID : {response.json()}")

    url = f"http://localhost:8000/pdf/{id}/setup"
    parameters = {"id": id, "path": r"C:\Users\DXD\Desktop\Prace_badawcze.pdf"}
    response = await post_request(aclient, url, parameters)
    logger.info(f"Response : {response.json()}")

    url = f"http://localhost:8000/pdf/{id}/select_pages"
    parameters = {"id": id, "selected_pages": "2-5,10"}
    response = await put_request(aclient, url, parameters)
    logger.info(f"Response : {response.json()}")

    url = f"http://localhost:8000/pdf/{id}/save"
    parameters = {"id": id, "output_dir": r"C:\Users\DXD\Desktop", "output_name": "xyz_file"}
    response = await get_request(aclient, url, parameters)
    logger.info(f"Response : {response.json()}")

    url = f"http://localhost:8000/pdf/{id}/patch_merge_paths"
    parameters = {"id": id, "paths_to_merge": ",".join([r"C:\Users\DXD\Desktop\Prace_badawcze.pdf",
                                                        r"C:\Users\DXD\Desktop\Order Confirmation.pdf"])}
    response = await patch_request(aclient, url, parameters)
    logger.info(f"Response : {response.json()}")

    url = f"http://localhost:8000/pdf/{id}/merge"
    parameters = {"id": id, "output_path": r"C:\Users\DXD\Desktop", "output_name": None}
    response = await get_request(aclient, url, parameters)
    logger.info(f"Response : {response.json()}")

    url = f"http://localhost:8000/pdf/delete/{id}"
    parameters = {"id": id}
    response = await delete_request(aclient, url, parameters)
    logger.info(f"Response : {response.json()}")

    await aclient.aclose()

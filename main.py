from example_queryset import main
from asyncio import run 


if __name__ == "__main__":
    run(main())

# cd C:\Users\DXD\PycharmProjects\FastAPI_pdf                 <- path to the working directory
# uvicorn pdf_server:pdfAPI --host 0.0.0.0 --port 8000        <- run server from cmd
# http://127.0.0.1:8000/docs                                  <- service layout provided by

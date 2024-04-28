from example_queryset import main
from asyncio import run
from time import sleep
from subprocess import run as sys_run
from multiprocessing import Process


def run_server(server: list[str], cd: str):
    sys_run(cd, shell=True)
    sys_run(server)


def run_actions():
    sleep(4)
    run(main())


def run_as_processes():
    server = ["uvicorn", "pdf_server:pdfAPI", "--host", "0.0.0.0", "--port", "8000"]
    cd = ["cd", r"C:\Users\DXD\PycharmProjects\FastAPI_pdf"]
    p1 = Process(target=run_server, args=(server, cd))
    p2 = Process(target=run_actions, args=())
    p1.start()
    p2.start()
    p1.join()
    p2.join()


if __name__ == "__main__":
    run_as_processes()

# cd C:\Users\DXD\PycharmProjects\FastAPI_pdf                 <- path to the working directory
# uvicorn pdf_server:pdfAPI --host 0.0.0.0 --port 8000        <- run server from cmd
# http://127.0.0.1:8000/docs                                  <- service layout provided by

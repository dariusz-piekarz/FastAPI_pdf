Repository contains project of pdf service based od `FAST API`, `httpx`, `asyncio` and `pypdf` modules.

Repository Structure
--------------------

### 1\. main.py

The `main.py` file runs asynchronically the *main* function from the `example_queryset.py` file.

### 2\. example\_queryset.py

The `example_queryset.py` file contains an example function and demonstrates the usage of FAST API queries. It also includes documentation related to available methods, such as:

*   Merging PDF files.
*   Page selection/deletion/rotation.
*   Page insertion.
*   Insertion/appending of blank pages.
*   Functions to change the reader mode to the writer mode and vice versa.
*   PDF encryption/decryption.
*   Text extraction.
*   Image extraction.

### 3\. httpx\_reqests.py
The `httpx_requests.py` contains asynchronic queries *PUT*, *GET*, *DELETE*, *PUSH* and *PATCH*, which allow connection client to server.

### 4\. pdf\_server.py

The `pdf_server.py` folder contains the server logic.

### 5\. functions\_pdf.py

The `functions_pdf.py` file contains the `PDF` class, which allows manipulation of PDF files.

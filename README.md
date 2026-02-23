# Lost and Found Application

## Application Introduction
Your university wants a simple desktop application to help manage lost and found items on campus. You should develop an application that allows staff or students to record items that have been found or lost and update their status when claimed.

There are two tasks to complete

### Task 1

Develop an application in Python which meets the following functional requirements:

**Minimum Item Details:**

- Item Name
- Category (e.g., electronics, clothing, books)
- Date Found/Lost
- Location
- Status (e.g., “Found”, “Claimed”)
- Contact Info of Finder or Owner

**Minimum Features:**
- **CRUD Operations:**
    - Add new lost/found items
    - View all items in a list
    - Update item details (e.g., mark as claimed)
    - Delete items
- **Search/Filter:**
    - Filter by category or status
    - Search by keyword
- **Validation:**
    - Ensure required fields are filled
    - Validate date format

The eventual intention is to make the system available via a web page. You must therefore ensure that you can replace the interface without changing the back-end system.

### Task 2:

You should provide **wireframe** designs for a future web interface to the application

**You do *not need* to consider user authentication in this assignment.**

## Implementation

The software must be written in the Python programming language, version 3.11 or later
(3.11 is recommended). The software must not require any additional software
applications or integrated development environment in order to run.
Python is distributed with an extensive library, and your software should make use of this. Tkinter should be used to implement the graphical user interface, and sqlite3 should be
used to implement the database. You can optionally make use of CustomTKinter.

The following additional Python libraries should be used
- pytest - testing framework.
- flake8
- sphinx

***Do not use any other 3rd party or non standard libraries***

## Testing

You should test your application.

Both static code checking, with flake8 and unit-testing with pytest will be carried out.
You should write your own unit tests and place your tests in a sub-directory of your
application code directory - name this directory **\<tests\>**.

There is information on unit-testing, pytest, and mocking in the recommended text book -
**Hunt, J. (2019). Advanced Guide to Python 3 Programming.**

## Documentation

Use Sphinx to document your system. To view the documentation locally:

Open `docs/build/html/index.html` in your web browser.

or if not found:

1. Ensure you have installed the requirements: `pip install -r requirements.txt`
2. Navigate to the docs folder: `cd docs`
3. Build the HTML: `make html` (or `make.bat html` on Windows)
4. Open `docs/build/html/index.html` in your web browser.
# Machine Learning in the Connected World

This project is an ongoing courseware for the course "Machine Learning on Graphs". 
The overall approach and teaching philosophy are inspired by the "Think X" series of books by Allen B. Downey. I studied and have been teaching from his books for years and I am a big fan of his work. 
The courseware infrastructure code is based on the "Think Python" 3rd edition book by Allen B. Downey. 

I extend my gratitude to Allen for his work and hope to contribute to the community with this project.

Boris Gorelik  
[boris@gorelik.net](mailto:boris@gorelik.net)




## To maintainers

This book uses `jupyter-book` to generate the HTML and PDF versions of the book.

To build the HMML version, run `jupyter-book build MLConnectedWorldBook` in the root directory of the project. This will create the HTML version of the book in the `_build` directory.


To build the PDF version, run `jupyter-book build MLConnectedWorldBook --builder pdflatex` in the root directory of the project. This will create the PDF version of the book (`_build/latex/book.pdf`). Note, that you need to have `pdflatex` installed on your system to build the PDF version of the book.

To publish this book, run `ghp-import -n -p -f _build/html` in the root directory of the project. This will publish the HTML version of the book to GitHub Pages.

-n: This argument specifies that the command should not create a commit. By default, ghp-import will create a new commit when pushing the content to GitHub Pages. 

-p: This argument specifies that the content should be pushed to GitHub Pages after it's been imported.

-f: Forces the import, even if the destination directory already exists. 




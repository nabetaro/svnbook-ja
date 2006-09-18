
How to generate single page HTML with text from a specific language (it in this example)
----------------------------------------------------------------------------------------
Required files: src\it\lab\Makefile.base-rules

Step 1 - Prepare environment
Copy Makefile.base-rules in src\tools\tools in your LOCAL copy of src.

Step 2 - Generate HTML with only IT text
cd src/it
export LANG_FILTER=1
make html


How to generate Mchunk-HTML with text from a specific language (it in this example)
----------------------------------------------------------------------------------------
Required files: src\it\lab\chunk-stylesheet.xsl

Step 1 - Prepare environment
..t be completed
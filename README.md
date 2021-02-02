# diagram-parser
 Parse XML export from draw.io and convert arrows to cvs (Source, Description, Target)
 Works only for connected by arrow objects.

 # usage
 
```
python .\draw_io_parser.py -h
usage: draw_io_parser.py [-h] --input INPUT [--output OUTPUT]

Converts draw.io XML to CSV with inerfaces

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT, -I INPUT
                        The path to XML exported from draw.io
  --output OUTPUT, -O OUTPUT
                        The path to output csv file (default path is "draw_io_parser_output.csv")
```
 

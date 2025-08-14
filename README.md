## System Setup
####  from project root install requirements
```bash
pip install -r requirements.txt
```
## Running the script
#### From project root run
```bash
python main.py --display_results
```
### Optional arguments for the script:
`-v`, `--verbose` – Control log level (**INFO** if passed, **ERROR** if not). Default: **ERROR**.  
`-d`, `--debug` – Disable threading if passed (run sequentially). Default: threading enabled.  
`--output_dir` – Path to the output directory. Relative paths are converted to absolute. Default: `tmp`.  
`--display_results` – Display results in the default browser when finished. Default: `False`.  
### Running with args example
```bash
python main.py -v -d --output_dir not_tmp --display_results
```
This example will run the system with log level INFO,
without using multithreading, 
will write the output to /not_tmp inside the project root, 
and will display results in browser at the end of the run
## Submission Author: Isabel Tripp

### Process SLCSP zip codes and write to stdout

All processing is performed via the `script.py` file.
To execute the script, I recommend creating a virtual environment to support the script's `pandas` dependency:

```
python -m venv venv
source venv/bin/activate
pip install pandas
```

The script can then be executed via `python script.py` (and the output will be emitted on `stdout`)

### Testing

While this code wasn't tested exhaustively, it's possible to manually find the SLCSP for a zip code and compare it with the script's output. The `test.py` file provides a super-simple unitest structure for doing this.

### Assumptions

I made one (questionable?) assumption: if multiple plans in a rate area have the same rate, treat them as distinct ie the first- and second-lowest cost plans might have the same rate. It would be simple to readjust this assumption in the code — feel free to bring it up.

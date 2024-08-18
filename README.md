# Finance

Personal project for merging finnancial record files into a single .csv file.

## How to use

### Initial setup

#### 1. Clone repo

#### 2. Create virtual environment and install required pakcages

On MacOS:

```sh
sh init.sh
```

Windows:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

#### 3. Run the script once the create the *paths* file

```sh
python3 script.py
```

### Using the script

#### 1. Check if the paths on `path.json` are correct

You can leave the default paths or change to a specific path.

```json
{
  "input_path": "./input",
  "output_path": "./output.csv"
}
```

#### 2. Move input files to input path

Input files should all be in `.csv` format.

#### 3. Run script

```sh
python3 script.py
```

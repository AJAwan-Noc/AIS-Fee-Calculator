# ATA Martial Arts Fee Calculator

## Project Overview

A desktop program that works out the monthly fee for each member of ATA
Martial Arts. For every athlete the user enters a name, a training plan, a
weight and weight category, the number of competitions entered this month and
the hours of private coaching per week. The program checks each entry, then
shows an itemised bill (training, coaching, competitions and the monthly
total) and adds the athlete to a list on screen.

It was written for the HND Unit 1 programming assignment.

## Features

- Tkinter window with a form for one athlete at a time.
- Drop-down lists for the plan and the weight category.
- Validation of every field. The first problem found is shown in a red
  message and nothing is added until it is fixed.
- Competitions are locked to 0 when the Beginner plan is chosen.
- Itemised breakdown showing how each cost was worked out, with all money
  shown as pounds to 2 decimal places (for example `£218.00`).
- A table listing every athlete added during the session, with their monthly
  total.
- A "Clear Form" button that empties all fields.
- Unit tests for the pricing, validation and athlete code.
- A profiling script that processes 20,000 athletes.

Athletes are held in memory only. They are not saved when the window is
closed.

## Requirements

- Python 3.12
- Standard library only. The program uses `tkinter` for the window and
  `unittest` for the tests, so there is nothing to install to run it.
- Development tools (optional): `flake8` and `black`, listed in
  `requirements-dev.txt`.

## Installation

1. Clone the repository and move into the folder:

   ```
   git clone <repository-url>
   cd AIS-Fee-Calculator
   ```

2. Create a virtual environment:

   ```
   python -m venv .venv
   ```

3. Activate it:

   - Windows: `.venv\Scripts\activate`
   - macOS / Linux: `source .venv/bin/activate`

4. Install the development tools (flake8 and black):

   ```
   pip install -r requirements-dev.txt
   ```

   This step is only needed for checking and formatting the code. It is not
   needed to run the program or the tests.

## Usage

Start the program from the project folder:

```
python app.py
```

To add an athlete:

1. Type the athlete's name in **Name**. Letters, spaces, hyphens and
   apostrophes are allowed, up to 50 characters.
2. Choose a plan in **Plan**: Beginner, Intermediate or Elite. If you choose
   Beginner, the **Competitions this month** box is set to 0 and locked.
3. Type the weight in kilograms in **Weight (kg)**, for example `72.5`.
4. Choose a **Weight category**. The weight must fit the category you choose
   (see the table below).
5. Type the number of competitions in **Competitions this month**
   (Intermediate and Elite only).
6. Type the private coaching hours per week in **Coaching hours per week**
   (0 to 5, decimals allowed).
7. Click **Calculate and Add Athlete**.

If something is wrong, a red message explains the first problem found. Correct
that field and click the button again.

If everything is valid, the breakdown for that athlete appears in the text
area and a new row is added to the athlete table. The form is not cleared
automatically. Click **Clear Form** before entering the next athlete.

## Price List and Business Rules

Plans (price per week):

| Plan         | Per week | Per month (4 weeks) |
|--------------|----------|---------------------|
| Beginner     | £25.00   | £100.00             |
| Intermediate | £30.00   | £120.00             |
| Elite        | £35.00   | £140.00             |

Other charges and rules:

- Private coaching costs £9.50 per hour, with a maximum of 5 hours per week.
  Hours are entered per week.
- Competition entry costs £22.00 each.
- Only Intermediate and Elite members may enter competitions.
- A month is exactly 4 weeks.
- All money is shown as pounds to 2 decimal places.
- Bad input produces a clear message and the user is asked again.

Weight categories:

| Category           | Weight band          |
|--------------------|----------------------|
| Flyweight          | up to 66 kg          |
| Lightweight        | over 66 up to 73 kg  |
| Light-Middleweight | over 73 up to 81 kg  |
| Middleweight       | over 81 up to 90 kg  |
| Light-Heavyweight  | over 90 up to 100 kg |
| Heavyweight        | over 100 kg          |

The upper limit of each band is included. For example, 81 kg fits
Light-Middleweight and 81.5 kg fits Middleweight.

Worked examples (these are used as test cases):

- Intermediate, 1 competition, 2 coaching hours per week:
  £120.00 + £76.00 + £22.00 = £218.00
- Elite, 3 coaching hours per week, 0 competitions:
  £140.00 + £114.00 + £0.00 = £254.00

## Assumptions

- Coaching hours are entered per week and multiplied by 4 to get the monthly
  coaching cost.
- A month is exactly 4 weeks.
- The maximum of 5 competitions per month and the 50-character limit on names
  are sanity limits chosen for this program. They are not client rules, and
  the brief sets no such maximums.
- The weight entered must fit the chosen weight category. The category does
  not change the fee.

## Running Tests

From the project folder:

```
python -m unittest discover -s tests -v
```

The tests are in the `tests` folder:

- `test_pricing.py` checks the cost functions, both worked examples and the
  5-hour coaching boundary.
- `test_validation.py` checks valid and invalid input for every validation
  function, including the weight category edges and the sanity limits.
- `test_athlete.py` checks the itemised breakdown and the `Squad` class.

The window itself (`app.py`) is not covered by automated tests.

## Profiling

`profile_pricing.py` builds a squad of 20,000 athletes with a mix of plans,
coaching hours and competitions, works out every monthly breakdown, and
prints how many athletes were processed and the grand total. To profile it:

```
python -m cProfile -s cumtime profile_pricing.py
```

## Project Structure

```
AIS-Fee-Calculator/
├── app.py                  Tkinter window (form, breakdown, athlete table)
├── athlete.py              Athlete and Squad classes
├── pricing.py              Prices, limits, weight categories, cost functions
├── validation.py           validate_* functions for each form field
├── profile_pricing.py      Script for profiling 20,000 athletes
├── tests/
│   ├── __init__.py
│   ├── test_pricing.py
│   ├── test_validation.py
│   └── test_athlete.py
├── docs/
│   ├── algorithm.md        IPO table, pseudocode, flowchart, test cases
│   ├── flowchart.drawio.png
│   └── screenshots/        Screenshots for the report, with a status table
├── .flake8                 flake8 settings (79 characters)
├── pyproject.toml          black settings (79 characters)
├── requirements-dev.txt    flake8 and black
├── .gitignore
├── LICENSE
└── README.md
```

How the code fits together: `app.py` reads the form and passes each value to
the matching function in `validation.py`. When all values are valid it
creates an `Athlete` (from `athlete.py`) and adds it to a `Squad`. The
`Athlete` gets its costs from the functions in `pricing.py`, and `app.py` only
formats the results for display.

## Coding Standards (PEP 8)

- Python 3, PEP 8, 4-space indents, maximum line length of 79 characters.
- `flake8` and `black` are both set to 79 characters in `.flake8` and
  `pyproject.toml`. Run them from the project folder:

  ```
  flake8
  black .
  ```

- Every function and class has a short docstring.
- Named UPPER_CASE constants are used instead of magic numbers.
- Plain loops and functions are used. No external libraries are used in the
  program itself.

## Licence

This project is released under the MIT Licence. See [LICENSE](LICENSE).

## Author

Ayaan Javaid Awan

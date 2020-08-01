import csv
import sys
from collections import Counter, OrderedDict, namedtuple
from pprint import pprint
from typing import Dict, List

complaint = namedtuple(
    'complaint',
    ['Product', 'Year', 'Company'],
)


def process_input(
    input_file: str,
    verbose: bool = False,
) -> List:
  """Process the input csv file into list of complaints records using complaint
  namedtuple for storing ('Product', 'DateReceived', 'Year', 'Company')

  Args:
      input_file (str): Path for the CSV file
      verbose (bool, optional): Debugging and printing the processed file. Defaults to False.

  Returns:
      List: List of Complaints
  """
  complaints = []
  with open(input_file, 'r') as file:
    complaints_file = csv.DictReader(
        file,
        delimiter=',',
    )
    for record in complaints_file:
      complaints.append(
          complaint(
              Product=record['Product'].strip().lower(),
              Year=record['Date received'].lower().split('-')[0],
              Company=record['Company'].strip().lower(),
          ))

  if verbose:
    pprint(complaints)

  return complaints


def compute(
    complaints: List,
    verbose: bool = False,
) -> Dict:
  """Computing the complaints according to the challenge specifications.

  Args:
      complaints (List): List of processed complaints
      verbose (bool, optional): Debugging and printing the processed file. Defaults to False.

  Returns:
      Dict: Dictionary of Computed Complaints ready for output
  """
  complaints_output = {}

  for record in complaints:
    complaints_output[(record.Product, record.Year)] = [0, 0, Counter()]

  # Total Number of Complaints
  for record in complaints:
    complaints_output[(record.Product, record.Year)][0] += 1
    complaints_output[(record.Product, record.Year)][2].update([record.Company])

  for key in complaints_output.keys():
    companies = complaints_output[key][2]
    complaints_output[key][1] = len(companies)
    complaints_output[key][2] = round(
        max(companies.values()) / complaints_output[key][0] * 100)

  if verbose:
    pprint(complaints_output)

  return complaints_output


def output_report(complaints_output: dict) -> None:
  """Writing the computed complaints to a CSV file.

  Args:
      complaints_output (dict): Dictionary of computed complaints
  """
  complaints_output = OrderedDict(sorted(complaints_output.items()))

  with open(output_file, 'w') as f:
    for key, values in complaints_output.items():
      if "," in key[0]:
        f.write(
            f"\"{key[0]}\",{int(key[1])},{','.join([str(v) for v in values])}\n"
        )
      else:
        f.write(
            f"{key[0]},{int(key[1])},{','.join([str(v) for v in values])}\n")


if __name__ == "__main__":

  input_file, output_file = sys.argv[1], sys.argv[2]

  complaints = process_input(input_file)

  complaints_output = compute(complaints)

  output_report(complaints_output)

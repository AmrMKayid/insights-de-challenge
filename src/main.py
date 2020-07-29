import csv
import sys
from collections import OrderedDict, namedtuple
from pprint import pprint
from typing import Dict, List

complaint = namedtuple(
    'complaint',
    ['Product', 'DateReceived', 'Year', 'Company'],
)


def process_input(
    input_file: str,
    verbose: bool = False,
) -> List:
  complaints = []
  with open(input_file, 'r') as file:
    complaints_file = csv.DictReader(
        file,
        delimiter=',',
    )
    for record in complaints_file:
      complaints.append(
          complaint(
              Product=record['Product'].lower(),
              DateReceived=record['Date received'].lower(),
              Year=record['Date received'].lower().split('-')[0],
              Company=record['Company'].lower(),
          ))

  if verbose:
    pprint(complaints)

  return complaints


def compute(
    complaints: List,
    verbose: bool = False,
) -> Dict:
  complaints_output = {}

  for record in complaints:
    complaints_output[(record.Product, record.Year)] = [0, set(), 0]

  # Total Number of Complaints
  for record in complaints:
    complaints_output[(record.Product, record.Year)][0] += 1
    complaints_output[(record.Product, record.Year)][1].add(str(record.Company))

  for key in complaints_output.keys():
    complaints_output[key][1] = len(complaints_output[key][1])
    complaints_output[key][2] = round(complaints_output[key][1] /
                                      complaints_output[key][0] * 100)

  if verbose:
    pprint(complaints_output)

  return complaints_output


def output_report(complaints_output: dict) -> None:
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

import os
import pandas as pd
import uuid
from file_path import load_paths
from datetime import datetime

class FinancialRecord:
  """
  Class representing a financial record, which could be either a transaction or a purchase.
  """

  def __init__(self, date, amount, description, category=None, trans_id=None):
    """
    Initialize the financial record.
    :param date: Date of the transaction or purchase.
    :param amount: Amount of money involved in the transaction or purchase.
    :param description: Description of the transaction or purchase.
    :param category: Category of the purchase, optional for transactions.
    :param trans_id: Transaction ID if it's a transaction; None for purchases.
    """
    self.date = self._parse_date(date)
    self.amount = amount
    self.description = description
    self.category = category

    # Determine if it's a transaction or purchase
    if trans_id:
      self.id = trans_id
      self.type = "transaction"
    else:
      self.id = str(uuid.uuid4())  # Generate a new UUID for purchases
      self.type = "purchase"

  def _parse_date(self, date_str):
    """
    Parse the date string into a datetime object. Adjust format if needed.
    :param date_str: The date string.
    :return: A datetime object.
    """
    try:
      return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
      # Handle other date formats if necessary
      return datetime.strptime(date_str, '%d/%m/%Y')

  def to_dict(self):
    """
    Convert the financial record to a dictionary format.
    :return: A dictionary representing the financial record.
    """
    return {
      "Data": self.date.strftime('%Y-%m-%d'),
      "Valor": self.amount,
      "Categoria": self.category,
      "ID": self.id,
      "Descrição": self.description,
      "Tipo": self.type
    }

  def __repr__(self):
    """
    Provide a string representation of the object for debugging.
    :return: A string representation of the financial record.
    """
    return f"<FinancialRecord(type={self.type}, date={self.date}, amount={self.amount})>"

def process_file(file_path):
  """
  Process a single CSV file and convert its rows into FinancialRecord objects.
  :param file_path: The path to the CSV file.
  :return: A DataFrame containing the processed financial records.
  """
  try:
    df = pd.read_csv(file_path)
  except Exception as e:
    print(f"Error reading {file_path}: {e}")
    return pd.DataFrame()  # Return an empty DataFrame if there's an error

  records = []

  for index, row in df.iterrows():
    if 'Data' in row and 'Identificador' in row:
      # Handling for transaction files
      record = FinancialRecord(
        date=row['Data'],
        amount=row['Valor'],
        description=row['Descrição'],
        trans_id=row['Identificador']
      )
    elif 'amount' in row and 'title' in row:
      # Handling for purchase files
      record = FinancialRecord(
        date=row['date'],
        amount=row['amount'],
        description=row['title'],
        category=row['category']
      )
    else:
      continue  # Skip rows that do not match the expected structure

    records.append(record)

  return pd.DataFrame([record.to_dict() for record in records])

def merge_files(input_folder, output_file):
  """
  Merge all CSV files in the input folder into a single CSV file.
  :param input_folder: Path to the folder containing the CSV files.
  :param output_file: Path where the merged CSV file will be saved.
  """
  all_data = []

  for filename in os.listdir(input_folder):
    if filename.endswith(".csv"):
      file_path = os.path.join(input_folder, filename)
      processed_df = process_file(file_path)
      if not processed_df.empty:
        all_data.append(processed_df)

  if all_data:
    merged_df = pd.concat(all_data)
    merged_df = merged_df.sort_values(by='Data')
    merged_df.to_csv(output_file, index=False)
    print(f"Merged file saved to {output_file}")
  else:
    print("No valid CSV files found for processing.")

if __name__ == "__main__":
  input_path, output_path = load_paths()

  # Ensure the input directory exists
  if not os.path.exists(input_path):
    os.makedirs(input_path)

  # Merge the files and write the output
  merge_files(input_path, output_path)
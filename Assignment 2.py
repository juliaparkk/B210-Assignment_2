# This script computes the percentage of explicit songs in a CSV file.
# Usage: python "C:\Users\jinas\Downloads\Assignment 2.py" "C:\path\to\taylor_discography.csv"
import os

def detect_explicit_from_row(row, headers):
	"""Return True if the row appears explicit.

	Heuristics used (in order):
	- If there's a column name containing 'explicit' or 'is_explicit', check its value (1/0, true/false, yes/no)
	- If there's no explicit column, check the joined row text for the word 'explicit' or '(explicit)'
	- If still unknown, return False
	"""
	# try to find an explicit-related column
	for i, h in enumerate(headers):
		key = h.strip().lower()
		if 'explicit' in key or 'is_explicit' in key or key == 'explicit':
			val = row[i].strip().lower()
			if val in ('1', 'true', 't', 'yes', 'y'):
				return True
			return False

	# fallback: search in any field for the token explicit
	joined = ','.join(row).lower()
	if '(explicit)' in joined or 'explicit' in joined:
		return True
	return False


def compute_explicit_percentage(csv_path):
	if not os.path.exists(csv_path):
		print(f"CSV file not found: {csv_path}")
		return

	with open(csv_path, 'r', encoding='utf-8') as file:
		lines = [line.rstrip('\n') for line in file]

	if not lines:
		print('CSV file is empty')
		return

	# naive CSV split by comma, but handle quoted fields
	def split_csv_line(line):
		fields = []
		cur = ''
		in_quote = False
		i = 0
		while i < len(line):
			c = line[i]
			if c == '"':
				if in_quote and i+1 < len(line) and line[i+1] == '"':
					cur += '"'  # escaped quote
					i += 1
				else:
					in_quote = not in_quote
			elif c == ',' and not in_quote:
				fields.append(cur)
				cur = ''
			else:
				cur += c
			i += 1
		fields.append(cur)
		return fields

	header = split_csv_line(lines[0])
	rows = [split_csv_line(l) for l in lines[1:] if l.strip() != '']

	total = 0
	explicit_count = 0
	for row in rows:
		# normalize row length to header
		if len(row) < len(header):
			row += [''] * (len(header) - len(row))
		elif len(row) > len(header):
			# keep extra columns but header indices won't match; it's fine for our heuristics
			pass

		is_exp = detect_explicit_from_row(row, header)
		total += 1
		if is_exp:
			explicit_count += 1

	if total == 0:
		print('No song rows found in CSV')
		return

	percentage = (explicit_count / total) * 100
	print(f"Explicit songs: {explicit_count}/{total} ({percentage:.2f}%)")


if __name__ == '__main__':
	csv_path = r'C:\Users\jinas\OneDrive\Documents\taylor_discography.csv'
	compute_explicit_percentage(csv_path)

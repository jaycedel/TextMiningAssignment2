# SPLIT FILENAME AND RETURNS {'GENDER': 'FEMALE', 'AGE': 26, 'INTEREST': 'INTERNET'}
def parse_filename(filename):
    splittedFilename = filename.split(".")
    return {'GENDER': splittedFilename[1].upper(), 'AGE': int(splittedFilename[2]),
            'INTEREST': splittedFilename[3].upper()}

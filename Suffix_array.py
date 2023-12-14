from pathlib import Path
from colorama import Fore, Style, init
from typing import Union



class SuffixArray:
    def __init__(self, text: str):
        self.text = text
        self.suffix_array = self.build_suffix_array()

    def build_suffix_array(self) -> list:

        suffixes = [i for i in range(len(self.text))]
        suffixes.sort(key=lambda i: self.text[i:])

        return suffixes

    def search_pattern(self, pattern: str) -> list:

        low, high = 0, len(self.text)
        loci = []
        while low < high:
            mid = (low + high) // 2
            suffix = self.suffix_array[mid]
            if self.text[suffix:suffix + len(pattern)] == pattern:
                loci.append(suffix + 1)  # Adding 1 to make the output 1-indexed
                # Continue searching for other occurrences
                left, right = mid - 1, mid + 1
                while left >= low and self.text[self.suffix_array[left]:self.suffix_array[left] + len(pattern)] == pattern:
                    loci.append(self.suffix_array[left] + 1)
                    left -= 1
                while right < high and self.text[self.suffix_array[right]:self.suffix_array[right] + len(pattern)] == pattern:
                    loci.append(self.suffix_array[right] + 1)
                    right += 1
                return loci
            elif self.text[suffix:suffix + len(pattern)] < pattern:
                low = mid + 1
            else:
                high = mid


        return loci

def align_sequences(pattern: str, text: str):
    suffix_array = SuffixArray(text)
    loci = suffix_array.search_pattern(pattern)
    return loci

def read_fasta(file_path: Union[str, Path]) -> str:
    with open(file_path, 'r') as file:
        lines = file.readlines()
    sequence = ''.join(line.strip() for line in lines[1:])
    return sequence

def read_output(output_path: Union[str, Path]) -> str:
    with open(output_path, 'r') as file:
        output = file.readlines()[0]
        
    return output

def test(test_path: Union[str, Path]) -> None:
    test_path = Path(test_path)
    passed = []

    for i, test in enumerate(test_path.iterdir()):
        pattern_file_path = test / "P.fa"
        text_file_path = test / "T.fa"
        output_file = test / "output.txt"

        

        pattern = read_fasta(pattern_file_path)
        text = read_fasta(text_file_path)
        alignment_loci = align_sequences(pattern, text)

        result = "Alignment loci:" + " " + str(sorted(alignment_loci))
        output = read_output(output_file)

        print(test.name)
        print('pattern:', pattern)
        print('text:', text)
        print('-'*20)
        print(f'right answer: {output}\nyour answer: {result}')

        if output == result:
            print(Fore.GREEN + f'Test passed!')
            passed.append(True)

        else:
            print(Fore.RED + f'Test failed(') 
            passed.append(False)          

        print('')
    
    if all(passed):
        print(Fore.GREEN + f'ALL TESTS PASSED!!!')
        print('')


    

if __name__ == "__main__":

    init(autoreset=True)
    test_path = './tests'
    test(test_path)

    # Input paths for sequence P and text T
    pattern_file_path = "P.fa"
    text_file_path = "T.fa"

    # Read sequences from files
    pattern = read_fasta(pattern_file_path)
    text = read_fasta(text_file_path)

    # Align sequences and get the result
    alignment_loci = align_sequences(pattern, text)

    # Output the result
    print("Alignment loci:", sorted(alignment_loci))



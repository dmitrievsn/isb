import multiprocessing
from itertools import product
from typing import List, Optional, Generator
import hashlib
import json
import constants
from tqdm import tqdm
import time
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget,
                            QPushButton, QLabel, QLineEdit, QTextEdit, QProgressBar,
                            QSpinBox, QFormLayout, QMessageBox)
from PyQt5.QtCore import QThread, pyqtSignal



class CardNumberFinder:
    def __init__(self, hash_value: str = None, last_four: str = None,
                 bins: List[str] = None, middle_len: int = None, path: str = None):
        self.bins = bins or constants.ALFABANK_VISA_DEBIT_BINS
        self.last_four = last_four or constants.LAST_4_CHARACTERS_CARD
        self.middle_len = middle_len or constants.MIDDLE_LENGTH
        self.hash_value = hash_value or constants.HASH_VALUE
        self.path = path or constants.PATH_TO_SAVE

    def generate_and_check_cards(self, bin_prefix: str) -> List[str]:
        matching = []
        total_possibilities = 10 ** self.middle_len
        with tqdm(product('0123456789', repeat=self.middle_len),
                 total=total_possibilities,
                 desc=f"Processing BIN {bin_prefix}",
                 leave=False) as pbar:
            for middle in pbar:
                card = bin_prefix + ''.join(middle) + self.last_four
                if self.check_hash(card):
                    matching.append(card)
                    pbar.set_postfix({'found': len(matching)})
        return matching

    @staticmethod
    def luhn_check(card_number: str) -> bool:
        total = 0
        for i, digit in enumerate(reversed(card_number)):
            num = int(digit)
            if i % 2 == 1:
                num *= 2
                if num > 9:
                    num = (num // 10) + (num % 10)
            total += num
        return total % 10 == 0

    def check_hash(self, card_number: str) -> bool:
        hashed = hashlib.sha3_224(card_number.encode()).hexdigest()
        return hashed == self.hash_value

    def find_matching_cards(self, num_processes: int) -> Optional[List[str]]:
        matching_cards = []
        with multiprocessing.Pool(processes=num_processes) as pool:
            results = pool.imap_unordered(
                self.generate_and_check_cards,
                self.bins,
                chunksize=1
            )
            for result in tqdm(results, total=len(self.bins), desc="Processing BINs"):
                if result:
                    matching_cards.extend(result)
        return matching_cards or None

    def save_to_json(self, card_numbers: List[str]) -> None:
        try:
            with open(self.path, "w") as f:
                json.dump({"matching_cards": card_numbers}, f, indent=2)
        except IOError as e:
            print(f"Error saving to file: {e}")


def benchmark(hash_value: str, last_four: str, bins: List[str], middle_len: int = 6):
    max_processes = int(multiprocessing.cpu_count() * 1.5)
    process_counts = range(1, max_processes + 1)
    times = []

    finder = CardNumberFinder(hash_value, last_four, bins, middle_len)

    print(f"Benchmarking with process counts from 1 to {max_processes}...")

    for num_processes in process_counts:
        start_time = time.time()
        matching_cards = finder.find_matching_cards(num_processes)
        elapsed = time.time() - start_time
        times.append(elapsed)

        if matching_cards:
            print(f"\nFound {len(matching_cards)} matching card(s) with {num_processes} processes:")
            for i, card in enumerate(matching_cards, 1):
                print(f"{i}. {card[:6]}******{card[-4:]}")
            finder.save_to_json(matching_cards)
            print(f"Results saved to {finder.path}")
            break

    return process_counts, times


def plot_results(process_counts, times):
    min_time = min(times)
    min_index = times.index(min_time)
    optimal_processes = process_counts[min_index]

    plt.figure(figsize=(10, 6))
    plt.plot(process_counts, times, 'b-o', label='Search time')
    plt.plot(optimal_processes, min_time, 'ro', label=f'Optimal ({optimal_processes} processes)')

    plt.title('Card Number Search Performance')
    plt.xlabel('Number of Processes')
    plt.ylabel('Time (seconds)')
    plt.xticks(process_counts)
    plt.grid(True)
    plt.legend()

    plt.savefig('performance_plot.png')
    plt.show()

    return optimal_processes
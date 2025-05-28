import multiprocessing
from itertools import product
from typing import List, Optional, Generator
import hashlib
import json
import constants
from tqdm import tqdm


class CardNumberFinder:
    def __init__(self):
        self.bins = constants.ALFABANK_VISA_DEBIT_BINS
        self.last_four = constants.LAST_4_CHARACTERS_CARD
        self.middle_len = constants.MIDDLE_LENGTH
        self.hash_value = constants.HASH_VALUE
        self.path = constants.PATH_TO_SAVE

    def generate_and_check_cards(self, bin_prefix: str) -> List[str]:
        matching = []
        for middle in product('0123456789', repeat=self.middle_len):
            card = bin_prefix + ''.join(middle) + self.last_four
            if self.check_hash(card):
                matching.append(card)
        return matching

    def check_hash(self, card_number: str) -> bool:
        hashed = hashlib.sha224(card_number.encode()).hexdigest()
        return hashed == self.hash_value

    def find_matching_cards(self) -> Optional[List[str]]:
        matching_cards = []
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
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


def main():
    print("Starting card number search...")
    finder = CardNumberFinder()
    matching_cards = finder.find_matching_cards()
    if matching_cards:
        print(f"Found {len(matching_cards)} matching card(s):")
        for i, card in enumerate(matching_cards, 1):
            print(f"{i}. {card[:6]}******{card[-4:]}")
        finder.save_to_json(matching_cards)
        print(f"Results saved to {finder.path}")
    else:
        print("No matching cards found")


if __name__ == "__main__":
    main()
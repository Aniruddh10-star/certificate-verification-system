import hashlib
import time
import json


class Block:

    def __init__(self, index, data, previous_hash):

        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash

        block_content = (
            str(self.index) +
            str(self.timestamp) +
            self.data +
            self.previous_hash
        )

        self.hash = hashlib.sha256(
            block_content.encode()
        ).hexdigest()


class Blockchain:

    def __init__(self):
        self.chain = []

        try:
            with open("blockchain.json", "r") as file:
                blockchain_data = json.load(file)

            for block_data in blockchain_data:
                block = Block(
                    block_data["index"],
                    block_data["data"],
                    block_data["previous_hash"]
                )

                block.timestamp = block_data["timestamp"]
                block.hash = block_data["hash"]

                self.chain.append(block)

        except FileNotFoundError:
            self.chain = []
    def add_block(self, data):

        if len(self.chain) == 0:
            previous_hash = "0"
        else:
            previous_hash = self.chain[-1].hash

        new_block = Block(
            len(self.chain) + 1,
            data,
            previous_hash
        )

        self.chain.append(new_block)

    def is_valid(self):

        for i in range(len(self.chain)):

            current_block = self.chain[i]

            block_content = (
                str(current_block.index) +
                str(current_block.timestamp) +
                current_block.data +
                current_block.previous_hash
            )

            calculated_hash = hashlib.sha256(
                block_content.encode()
            ).hexdigest()

            if current_block.hash != calculated_hash:
                return False

            if i > 0:

                previous_block = self.chain[i - 1]

                if current_block.previous_hash != previous_block.hash:
                    return False

        return True

    def save_to_file(self):

        blockchain_data = []

        for block in self.chain:

            blockchain_data.append({
                "index": block.index,
                "timestamp": block.timestamp,
                "data": block.data,
                "previous_hash": block.previous_hash,
                "hash": block.hash
            })

        with open("blockchain.json", "w") as file:
            json.dump(blockchain_data, file, indent=4)



from ellipticcurve.privateKey import PrivateKey


class InterfaceHandler:
    DEBUG = True

    def __init__(self):
        self.HEADER = '\033[95m'
        self.OKBLUE = '\033[94m'
        self.OKCYAN = '\033[96m'
        self.OKGREEN = '\033[92m'
        self.WARNING = '\033[93m'
        self.FAIL = '\033[91m'
        self.ENDC = '\033[0m'
        self.BOLD = '\033[1m'
        self.UNDERLINE = '\033[4m'

    def Error(self, *args):
        print("\n=========================================")
        for t in args:
            print(f"{self.FAIL} + ERROR + {self.ENDC}: {t}")

        print("=========================================\n")

    def Block(self, block):
        print("\n=========================================")
        print(f"{self.OKGREEN} + BLOCK: {block.get_number()} + {self.ENDC}")
        print(f"{self.BOLD}SPK: {self.ENDC}{block.get_sender_public_key()}")
        print(f"{self.BOLD}RPK: {self.ENDC}{block.get_reciever_public_key()}\n")
        print(f"{self.BOLD}Value: {self.ENDC}{block.get_value()}")
        print(f"{self.BOLD}Transaction Cost: {self.ENDC}{block.get_transaction_cost()}")
        print(f"{self.BOLD}Message: {self.ENDC}{block.get_message()}\n")
        print(f"{self.BOLD}Hash: {self.ENDC}{block.get_hash()}")
        print(f"{self.BOLD}Previous Hash: {self.ENDC}{block.get_previouis_hash()}")
        print(f"{self.BOLD}Nonce: {self.ENDC}{block.get_nonce()}")
        print(f"{self.BOLD}Time: {self.ENDC}{block.get_time()}")
        if block.is_valid():
            print(
                f"{self.BOLD}Singature {self.OKGREEN}(verified){self.ENDC}{self.BOLD}: {self.ENDC}{block.get_signature()}")
        else:
            print(
                f"{self.BOLD}Singature {self.FAIL}(corrupted){self.ENDC}{self.BOLD}: {self.ENDC}{block.get_signature()}")
        print("=========================================\n")

    def Alert(self, *args):
        print("\n=========================================")
        for t in args:
            print(f"{self.WARNING} + ALERT + {self.ENDC} : {t}")
        print("=========================================\n")

    def Info(self, *args):
        print("\n=========================================")
        for t in args:
            print(f"{self.OKGREEN} + INFO  + {self.ENDC}: {t}")
        print("=========================================\n")

    def Debug(self, *args):
        if self.DEBUG:
            for t in args:
                print(f"{self.OKCYAN} + DEBUG + {self.ENDC}: {t}")

    def new_user_welcoming_message(self, side_wallet):

        self.wallet = side_wallet

        self.Info("Welcome to the Neurocoin Wallet")
        print("\n=========================================")
        print("1. Create a new wallet")
        print("2. Login to an existing wallet")
        print("3. Exit")
        print("=========================================\n")

        choice = int(input("Enter your choice: "))
        if choice == 3:
            exit()

        public_name = input("Enter your public name: ")
        if (choice == 1):
            if (public_name not in [wallet.public_name for wallet in self.wallet.blockchain.wallets]):
                # Public name of the wallet
                self.wallet.public_name = public_name
                # Public key of the wallet
                self.wallet.private_key = PrivateKey()
                self.wallet.public_key = self.wallet.private_key.publicKey()
                self.wallet.public_key_compressed = self.wallet.public_key.toCompressed()
            else:
                self.Error("This public name is already taken")
                self.new_user_welcoming_message(self.wallet)

        if choice == 2:
            if not self.wallet.login(public_name):
                self.Info("Login failed")
                self.new_user_welcoming_message(
                    self.wallet)
            else:
                self.wallet.public_name = public_name
                self.wallet.public_key = self.wallet.blockchain.wallets[[
                    wallet.public_name for wallet in self.wallet.blockchain.wallets].index(public_name)].public_key
                self.wallet.private_key = self.wallet.blockchain.wallets[[
                    wallet.public_name for wallet in self.wallet.blockchain.wallets].index(public_name)].private_key
                self.wallet.public_key_compressed = self.wallet.blockchain.wallets[[
                    wallet.public_name for wallet in self.wallet.blockchain.wallets].index(public_name)].public_key_compressed
                # find and delete the wallet thats been copied from the blockchain
                self.wallet.blockchain.wallets.pop(
                    [wallet.public_name for wallet in self.wallet.blockchain.wallets].index(public_name))
                self.Info("Login successful")

        self.main_menu()

    def main_menu(self):
        self.Info("Welcome to the Neurocoin Wallet")
        print("1. Send money")
        print("2. Check balance")
        if self.DEBUG:
            print("3. ==DEVELOPER MODE==")
        print("4. Exit")
        print("\n=========================================\n")

        choice = int(input("\nEnter your choice: "))

        if choice == 1:
            for wallet in self.wallet.blockchain.wallets:
                self.Info(
                    f"{wallet.public_name} balance: {wallet.get_balance()}", f"public key: {wallet.public_key_compressed}")
            recipient_public_key = input("\n\tEnter recipient public key: ")
            if recipient_public_key not in [wallet.public_key_compressed for wallet in self.wallet.blockchain.wallets]:
                self.Error("This public key doesn't exist")
                self.main_menu()

            value = int(input("\tEnter value: "))
            self.wallet.send_money(recipient_public_key, value)
            self.Info("Transaction successful")
            self.main_menu()

        elif choice == 2:
            self.Info(
                "you have " + str(self.wallet.get_balance()) + " neurocoins", f"Your public key: {self.wallet.public_key_compressed}")
            self.main_menu()
        elif choice == 3:
            if self.DEBUG:
                print("1. Print blockchain")
                print("2. Print wallets")
                print("3. Exit")
                choice = int(input("\nEnter your choice: "))
                if choice == 1:
                    self.Info("Blockchain:")
                    self.wallet.blockchain.print_blockchain_info()
                    self.main_menu()
                elif choice == 2:
                    for wallet in self.wallet.blockchain.wallets:
                        self.Info(
                            f"{wallet.public_name} balance: {wallet.get_balance()}", f"public key: {wallet.public_key_compressed}")
                    self.main_menu()
                elif choice == 3:
                    self.main_menu()
                else:
                    print("Invalid choice")
                    self.main_menu()
            else:
                print("Invalid choice")
                self.main_menu()

        elif choice == 4:
            self.wallet.blockchain.wallets.append(self.wallet)
            self.new_user_welcoming_message(self.wallet)
        else:
            print("Invalid choice")
            self.main_menu()

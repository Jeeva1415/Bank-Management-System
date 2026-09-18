
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Bank Management System",
    page_icon="🏦"
)

st.title("Bank Management System")

# BANK CLASS
class Bank:

    def __init__(self, owner, acc_no, pin, balance=0):

        self.owner = owner
        self.balance = balance
        self.acc_no = acc_no
        self.pin = pin

    def deposit(self, amount):

        if amount > 0:

            self.balance += amount

            st.success(
                f"₹{amount} added to your account !!"
            )

        else:

            st.error(
                "Please enter a positive number !!"
            )

    def withdraw(self, w_amount):

        if w_amount > self.balance:

            st.error("Insufficient Balance !!")

        elif w_amount <= 0:

            st.error(
                "Please enter a positive number !!"
            )

        else:

            self.balance -= w_amount

            st.success(
                f"₹{w_amount} withdrawn."
            )

            st.info(
                f"Current Balance: ₹{self.balance}"
            )

    def transfer(self, t_amount, t_name):

        if t_amount > self.balance:

            st.error("Insufficient Balance !!")

        elif t_amount <= 0:

            st.error(
                "Please enter a positive number !!"
            )

        elif t_name.strip() == "":

            st.error(
                "Please enter the recipient's name !!"
            )

        else:

            self.balance -= t_amount

            st.success(
                f"₹{t_amount} is transferred to {t_name}"
            )

            st.info(
                f"Current Balance: ₹{self.balance}"
            )

    def statement(self):

        st.subheader("Account Statement")

        st.write(
            f"Account Owner: {self.owner}"
        )

        st.write(
            f"Account Number: {self.acc_no}"
        )

        st.write(
            f"Account Balance: ₹{self.balance}"
        )

# SESSION STATE
if "accounts" not in st.session_state:

    st.session_state.accounts = {}


if "my_acc" not in st.session_state:

    st.session_state.my_acc = None

# LOGIN / CREATE ACCOUNT
if st.session_state.my_acc is None:

    st.subheader("Welcome to Banking")

    option = st.radio(
        "Choose an option",
        [
            "New Customer",
            "Existing Customer"
        ]
    )

    # NEW CUSTOMER
    if option == "New Customer":

        st.subheader("Create New Account")

        name = st.text_input(
            "Enter the name"
        )

        acc_no = st.text_input(
            "Enter the 10-digit account number",
            max_chars=10
        )

        pin = st.text_input(
            "Enter 4 digit pin",
            type="password",
            max_chars=4
        )

        if st.button("Create Account"):

            if name.strip() == "":

                st.error("Please enter your name !!")

            elif not (
                len(acc_no) == 10
                and acc_no.isdigit()
            ):

                st.error(
                    "Please enter a valid 10-digit "
                    "account number !!"
                )

            elif not (
                len(pin) == 4
                and pin.isdigit()
            ):

                st.error(
                    "Please enter a valid 4-digit PIN !!"
                )

            elif acc_no in st.session_state.accounts:

                st.error(
                    "Account already exists !! "
                    "Please use another account number."
                )

            else:

                new_account = Bank(
                    name,
                    acc_no,
                    pin
                )

                st.session_state.accounts[
                    acc_no
                ] = new_account

                st.session_state.my_acc = new_account

                st.success(
                    "Account created successfully !!"
                )

                st.rerun()

    # EXISTING CUSTOMER
    elif option == "Existing Customer":

        st.subheader("Login to Your Account")

        acc_no = st.text_input(
            "Enter your account number",
            max_chars=10
        )

        pin = st.text_input(
            "Enter your 4-digit PIN",
            type="password",
            max_chars=4
        )

        if st.button("Login"):

            if acc_no in st.session_state.accounts:

                account = st.session_state.accounts[
                    acc_no
                ]

                if pin == account.pin:

                    st.session_state.my_acc = account

                    st.success(
                        f"Welcome back, {account.owner} !!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Incorrect PIN !!"
                    )

            else:

                st.error(
                    "Account not found !! "
                    "Please create a new account."
                )

# BANKING OPERATIONS
if st.session_state.my_acc is not None:

    my_acc = st.session_state.my_acc

    st.sidebar.title("Bank Menu")

    st.sidebar.success(
        f"Welcome, {my_acc.owner}"
    )

    choice = st.sidebar.selectbox(
        "Select Operation",
        [
            "Deposit",
            "Withdraw",
            "Transfer",
            "Statement"
        ]
    )

    # DEPOSIT
    if choice == "Deposit":

        st.header("Deposit Money")

        amount = st.number_input(
            "Enter an amount to deposit",
            min_value=0,
            step=100
        )

        if st.button("Deposit"):

            my_acc.deposit(amount)

            st.info(
                f"Current Balance: ₹{my_acc.balance}"
            )

    # WITHDRAW
    elif choice == "Withdraw":

        st.header("Withdraw Money")

        w_amount = st.number_input(
            "Enter the amount to withdraw",
            min_value=0,
            step=100
        )

        pin = st.text_input(
            "Enter your 4-digit PIN",
            type="password",
            max_chars=4
        )

        if st.button("Withdraw"):

            if pin == my_acc.pin:

                my_acc.withdraw(w_amount)

            else:

                st.error(
                    "Please enter the correct PIN !!"
                )

    # TRANSFER
    elif choice == "Transfer":

        st.header("Transfer Money")

        t_name = st.text_input(
            "Please enter the recipient's name"
        )

        t_amount = st.number_input(
            "Enter amount to transfer",
            min_value=0,
            step=100
        )

        if st.button("Transfer"):

            my_acc.transfer(
                t_amount,
                t_name
            )

    # STATEMENT
    elif choice == "Statement":

        my_acc.statement()

    # LOGOUT
    st.sidebar.markdown("---")

    st.sidebar.write(
        f"Current Balance: ₹{my_acc.balance}"
    )

    if st.sidebar.button("Logout"):

        st.session_state.my_acc = None

        st.rerun()
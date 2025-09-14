import argparse
import os

from typing import Callable, Any

import sqlite3

from sqlite3 import Connection, Cursor


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Todos:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.db_file: str = f"{os.path.dirname(os.path.realpath(__file__))}/todos.db"
        self.db_exists: bool = False if not os.path.isfile(self.db_file) else True
        self.con: Connection = sqlite3.connect(self.db_file)
        self.cur: Cursor = self.con.cursor()
        self.create_tables()
        self.init_argparser()
        self.parse_and_handle_cli_args()

    def init_argparser(self):
        self.parser.add_argument("list", type=str, nargs="*", help="TODO option")

    def parse_and_handle_cli_args(self):
        self.args = self.parser.parse_args()

        if not self.args.list:
            self.preview()
            exit(0)

        # Auto remove completed TODOs within 2-3 days
        # todo - Outputs a list of current TODOs, and a list of completed TODOs
        # todo <TODO_IDs or all> completed/c - Marks TODOs as completed
        # todo remove <TODO_IDs>
        # todo new <TODO_description> - Creates a new TODO
        # todo update <TODO_ID> <TODO_new_description> - Updates a TODO
        self.handle_cmd_command("<int> completed", self.complete_one)
        self.handle_cmd_command("new <str>", self.create_one)
        self.handle_cmd_command("remove <int>", self.delete_one)
        self.handle_cmd_command("update <int> <str>", self.update_one)
        self.handle_cmd_command("all completed", self.complete_all)
        self.handle_cmd_command("clear", self.delete_all)

    def handle_cmd_command(self, query: str, callback: Callable[[list[Any]], None]):
        # remove <int>
        # callback_data: [12]
        # update <int> <str>
        # callback_data: [12, "New description"]

        query_args = query.split(" ")
        cli_args = self.args.list

        if len(query_args) != len(cli_args): return

        callback_data = []
        
        # Make sure that query string and cli arguments match
        for idx in range(len(query_args)):
            # int placeholder
            if query_args[idx].strip() == "<int>":
                if cli_args[idx].isdigit():
                    callback_data.append(int(cli_args[idx]))
                else:
                    return
            # string placeholder
            elif query_args[idx].strip() == "<str>":
                callback_data.append(cli_args[idx])
            # must match the exact value
            elif query_args[idx].strip() != cli_args[idx]:
                    return

        callback(*callback_data)
        self.preview()
        exit(0)

    def create_tables(self):
        if not self.db_exists:
            self.cur.execute("""
                CREATE TABLE todos(
                    id INTEGER PRIMARY KEY,
                    description VARCHAR(1000) NOT NULL,
                    completed INTEGER NOT NULL,
                    created_at DATETIME NOT NULL
                )
            """)

    def preview(self):
        res = self.cur.execute("SELECT * FROM todos")
        todos = res.fetchall()
        not_completed_arr = []
        completed_arr = []

        # Header
        print(f"===================== {Colors.BOLD}TODO List{Colors.ENDC} ========================")

        # Sort out todos
        for id, desc, completed, created_at in todos:
            if not completed:
                not_completed_arr.append((id, desc, completed, created_at))
            else:
                completed_arr.append((id, desc, completed, created_at))

        # Uncompleted header
        print(f"\n{Colors.FAIL}{Colors.BOLD}Uncompleted:{Colors.ENDC}\n")

        # Uncompleted TODOs
        for id, desc, completed, created_at in not_completed_arr:
            print(f"({id}) {Colors.FAIL}{Colors.BOLD}[ ]{Colors.ENDC} {desc} {Colors.WARNING}({created_at}){Colors.ENDC}")

        # Completed header
        print(f"\n{Colors.OKGREEN}{Colors.BOLD}Completed:{Colors.ENDC}\n")

        # Completed TODOs
        for id, desc, completed, created_at in completed_arr:
            print(f"{Colors.OKGREEN}({id}) {Colors.BOLD}[X]{Colors.ENDC} {desc} {Colors.WARNING}({created_at}){Colors.ENDC}")

        print("\n===========================================================")

    def complete_one(self, id: int):
        self.cur.execute("UPDATE todos SET completed=1 WHERE id=?", [id])
        self.con.commit()

    def complete_all(self):
        self.cur.execute("UPDATE todos SET completed=1")
        self.con.commit()

    def update_one(self, id: int, new_desc: str):
        self.cur.execute("UPDATE todos SET description=? WHERE id=?", [new_desc, id])
        self.con.commit()

    def delete_one(self, id: int):
        self.cur.execute("DELETE FROM todos WHERE id=?", [id])
        self.con.commit()

    def delete_all(self):
        self.cur.execute("DELETE FROM todos")
        self.con.commit()
        
    def create_one(self, desc: str):
        self.cur.execute("""
            INSERT INTO todos(description, completed, created_at) VALUES(?, 0, DATETIME('now'))
        """, [desc])
        self.con.commit()

    def close(self):
        self.con.close()

        
todos = Todos()
todos.close()

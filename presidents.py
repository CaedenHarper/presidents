__all__ = ["ALL_PRESIDENTS", "NUM_PRESIDENTS", "President"]

class President:
    """Represents a U.S. president with name details, order numbers, and start years.

    Attributes:
        AMBIGIOUS_FULL_NAMES (list[str]): Full names requiring disambiguation.
        HALF_AMBIGIOUS_FULL_NAMES (list[str]): Full names ambiguous without middle name.
        AMBIGIOUS_LAST_NAMES (list[str]): Last names shared by multiple presidents.
        first_name (str): President's first name.
        last_name (str): President's last name.
        middle_name (str | None): Middle name or initial, if any.
        nickname (str | None): Nickname, if any.
        order_numbers (list[str]): Presidential order numbers.
        start_year (list[str]): Years presidency started.
    """
    # lists of ambigious names in lowercase
    # both george bushes require middle initials to disambiguate
    AMBIGIOUS_FULL_NAMES = ("george bush",)
    # currently only john adams is half-ambiguous, meaning if no middle name is given,
    # it's 1979 adams
    HALF_AMBIGIOUS_FULL_NAMES = ("john adams",)
    AMBIGIOUS_LAST_NAMES = ("adams", "bush", "roosevelt", "johnson", "harrison")
    # died first year in office
    AMBIGIOUS_YEARS = ("1841", "1881")
    def __init__(self,
                 first_name: str,
                 last_name: str,
                 order_numbers: list[str],
                 start_year: list[str],
                 *,
                 middle_name: str | None = None,
                 nickname: str | None = None) -> None:
        """Initialize a President instance.

        Args:
            first_name (str): President's first name.
            last_name (str): President's last name.
            order_numbers (list[str]): Presidential order numbers.
            start_year (list[str]): Years presidency started.
            middle_name (str, optional): Middle name or initial. Defaults to None.
            nickname (str, optional): Nickname. Defaults to None.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.order_numbers = order_numbers
        self.start_year = start_year
        self.middle_name = middle_name
        self.nickname = nickname

    def __str__(self) -> str:
        """Return a string representation of the president."""
        return self.get_president_name()

    def get_president_name(self) -> str:
        """Return the full name of the president."""
        if self.middle_name is not None:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"

    def is_full_name_ambiguous(self) -> bool:
        """Check if the president's full name is ambiguous.

        Returns:
            bool: True if the full name is ambiguous, False otherwise.
        """
        return self.first_name.lower() + " " + self.last_name.lower() \
            in self.AMBIGIOUS_FULL_NAMES

    def is_last_name_ambiguous(self) -> bool:
        """Check if the president's last name is ambiguous.

        Returns:
            bool: True if the last name is ambiguous, False otherwise.
        """
        return self.last_name.lower() in self.AMBIGIOUS_LAST_NAMES

    def is_year_ambiguous(self) -> bool:
        """Check if the president's start year is ambiguous.

        Returns:
            bool: True if the start year is ambiguous, False otherwise.
        """
        return any(year in self.AMBIGIOUS_YEARS for year in self.start_year)

GEORGE_WASHINGTON = President("George", "Washington", ["1"], ["1789"])
JOHN_ADAMS = President("John", "Adams", ["2"], ["1797"])
THOMAS_JEFFERSON = President("Thomas", "Jefferson", ["3"], ["1801"])
JAMES_MADISON = President("James", "Madison", ["4"], ["1809"])
JAMES_MONROE = President("James", "Monroe", ["5"], ["1817"])
JOHN_QUINCY_ADAMS = President("John", "Adams", ["6"], ["1825"], middle_name="Quincy")
ANDREW_JACKSON = President("Andrew", "Jackson", ["7"], ["1829"])
MARTIN_VANBUREN = President("Martin", "Van Buren", ["8"], ["1837"])
WILLIAM_HENRY_HARRISON = President("William", "Harrison", ["9"], ["1841"], middle_name="Henry")
JOHN_TYLER = President("John", "Tyler", ["10"], ["1841"])
JAMES_K_POLK = President("James", "Polk", ["11"], ["1845"], middle_name="K.")
ZACHARY_TAYLOR = President("Zachary", "Taylor", ["12"], ["1849"])
MILLARD_FILLMORE = President("Millard", "Fillmore", ["13"], ["1850"])
FRANKLIN_PIERCE = President("Franklin", "Pierce", ["14"], ["1853"])
JAMES_BUCHANAN = President("James", "Buchanan", ["15"], ["1857"])
ABRAHAM_LINCOLN = President("Abraham", "Lincoln", ["16"], ["1861"])
ANDREW_JOHNSON = President("Andrew", "Johnson", ["17"], ["1865"])
ULYSSES_S_GRANT = President("Ulysses", "Grant", ["18"], ["1869"], middle_name="S.")
RUTHERFORD_B_HAYES = President("Rutherford", "Hayes", ["19"], ["1877"], middle_name="B.")
JAMES_A_GARFIELD = President("James", "Garfield", ["20"], ["1881"], middle_name="A.")
CHESTER_A_ARTHUR = President("Chester", "Arthur", ["21"], ["1881"], middle_name="A.")
GROVER_CLEVELAND = President("Grover", "Cleveland", ["22", "24"], ["1885", "1893"])
BENJAMIN_HARRISON = President("Benjamin", "Harrison", ["23"], ["1889"])
WILLIAM_MCKINLEY = President("William", "McKinley", ["25"], ["1897"])
THEODORE_ROOSEVELT = President("Theodore", "Roosevelt", ["26"], ["1901"], nickname="Teddy")
WILLIAM_HOWARD_TAFT = President("William", "Taft", ["27"], ["1909"], middle_name="Howard")
WOODROW_WILSON = President("Woodrow", "Wilson", ["28"], ["1913"])
WARREN_G_HARDING = President("Warren", "Harding", ["29"], ["1921"], middle_name="G.")
CALVIN_COOLIDGE = President("Calvin", "Coolidge", ["30"], ["1923"])
HERBERT_HOOVER = President("Herbert", "Hoover", ["31"], ["1929"])
FRANKLIN_D_ROOSEVELT = President("Franklin", "Roosevelt", ["32"], ["1933"], middle_name="D.",
                                 nickname="FDR")
HARRY_S_TRUMAN = President("Harry", "Truman", ["33"], ["1945"], middle_name="S.")
DWIGHT_D_EISENHOWER = President("Dwight", "Eisenhower", ["34"], ["1953"], middle_name="D.")
JOHN_F_KENNEDY = President("John", "Kennedy", ["35"], ["1961"], middle_name="F.", nickname="JFK")
LYNDON_B_JOHNSON = President("Lyndon", "Johnson", ["36"], ["1963"], middle_name="B.")
RICHARD_NIXON = President("Richard", "Nixon", ["37"], ["1969"])
GERALD_FORD = President("Gerald", "Ford", ["38"], ["1974"])
JIMMY_CARTER = President("Jimmy", "Carter", ["39"], ["1977"])
RONALD_REAGAN = President("Ronald", "Reagan", ["40"], ["1981"])
GEORGE_H_W_BUSH = President("George", "Bush", ["41"], ["1989"], middle_name="H. W.")
BILL_CLINTON = President("Bill", "Clinton", ["42"], ["1993"])
GEORGE_W_BUSH = President("George", "Bush", ["43"], ["2001"], middle_name="W.")
BARACK_OBAMA = President("Barack", "Obama", ["44"], ["2009"])
DONALD_TRUMP = President("Donald", "Trump", ["45", "47"], ["2017", "2025"])
JOE_BIDEN = President("Joe", "Biden", ["46"], ["2021"])
ALL_PRESIDENTS = [
    GEORGE_WASHINGTON,
    JOHN_ADAMS,
    THOMAS_JEFFERSON,
    JAMES_MADISON,
    JAMES_MONROE,
    JOHN_QUINCY_ADAMS,
    ANDREW_JACKSON,
    MARTIN_VANBUREN,
    WILLIAM_HENRY_HARRISON,
    JOHN_TYLER,
    JAMES_K_POLK,
    ZACHARY_TAYLOR,
    MILLARD_FILLMORE,
    FRANKLIN_PIERCE,
    JAMES_BUCHANAN,
    ABRAHAM_LINCOLN,
    ANDREW_JOHNSON,
    ULYSSES_S_GRANT,
    RUTHERFORD_B_HAYES,
    JAMES_A_GARFIELD,
    CHESTER_A_ARTHUR,
    GROVER_CLEVELAND,
    BENJAMIN_HARRISON,
    WILLIAM_MCKINLEY,
    THEODORE_ROOSEVELT,
    WILLIAM_HOWARD_TAFT,
    WOODROW_WILSON,
    WARREN_G_HARDING,
    CALVIN_COOLIDGE,
    HERBERT_HOOVER,
    FRANKLIN_D_ROOSEVELT,
    HARRY_S_TRUMAN,
    DWIGHT_D_EISENHOWER,
    JOHN_F_KENNEDY,
    LYNDON_B_JOHNSON,
    RICHARD_NIXON,
    GERALD_FORD,
    JIMMY_CARTER,
    RONALD_REAGAN,
    GEORGE_H_W_BUSH,
    BILL_CLINTON,
    GEORGE_W_BUSH,
    BARACK_OBAMA,
    DONALD_TRUMP,
    JOE_BIDEN,
]
NUM_PRESIDENTS = len(ALL_PRESIDENTS) # 45 distinct presidents

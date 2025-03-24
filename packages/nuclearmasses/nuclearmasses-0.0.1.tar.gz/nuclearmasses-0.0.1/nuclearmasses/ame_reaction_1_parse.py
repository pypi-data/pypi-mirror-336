"""Extract the data from the first reaction file."""
import logging
import pathlib

import pandas as pd

from nuclearmasses.ame_reaction_1_file import AMEReactionFileOne


class AMEReactionParserOne(AMEReactionFileOne):
    """Parse the first AME reaction file.

    The format is known but I don't think python can easily parse it.
    """

    def __init__(self, filename: pathlib.Path, year: int):
        """Set the file to read and table year."""
        self.filename = filename
        self.year = year
        super().__init__(self.year)
        logging.info(f"Reading {self.filename} from {self.year}")

    def _read_line(self, line: str) -> dict:
        """Read a line from the file."""
        # Don't use a '#' as an experimental marker in this file
        # but still need to remove it
        if line.find("#") != -1:
            line = line.replace("#", " ")

        data = {
            "TableYear": self.year,
            "A": self._read_as_int(line, self.START_R1_A, self.END_R1_A),
            "Z": self._read_as_int(line, self.START_R1_Z, self.END_R1_Z),
            "TwoNeutronSeparationEnergy": self._read_as_float(line, self.START_S2N, self.END_S2N),
            "TwoNeutronSeparationEnergyError": self._read_as_float(line, self.START_DS2N, self.END_DS2N),
            "TwoProtonSeparationEnergy": self._read_as_float(line, self.START_S2P, self.END_S2P),
            "TwoProtonSeparationEnergyError": self._read_as_float(line, self.START_DS2P, self.END_DS2P),
            "QAlpha": self._read_as_float(line, self.START_QA, self.END_QA),
            "QAlphaError": self._read_as_float(line, self.START_DQA, self.END_DQA),
            "QTwoBeta": self._read_as_float(line, self.START_Q2B, self.END_Q2B),
            "QTwoBetaError": self._read_as_float(line, self.START_DQ2B, self.END_DQ2B),
            "QEpsilon": self._read_as_float(line, self.START_QEP, self.END_QEP),
            "QEpsilonError": self._read_as_float(line, self.START_DQEP, self.END_DQEP),
            "QBetaNeutron": self._read_as_float(line, self.START_QBN, self.END_QBN),
            "QBetaNeutronError": self._read_as_float(line, self.START_DQBN, self.END_DQBN),
        }

        data["N"] = data["A"] - data["Z"]
        data["Symbol"] = self.z_to_symbol[data["Z"]]

        return data

    def read_file(self) -> pd.DataFrame:
        """Read the file."""
        with open(self.filename, "r") as f:
            lines = [line.rstrip() for line in f]

        # Remove the header lines
        lines = lines[self.HEADER: self.FOOTER]

        return pd.DataFrame([self._read_line(line) for line in lines])

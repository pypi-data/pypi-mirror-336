import os
import sys
from pathlib import Path
from argparse import ArgumentParser
import json
from hashlib import md5
import typing
from dataclasses import dataclass, asdict
from enum import Enum


@dataclass
class PyrightPosition:
    line: int
    character: int


@dataclass
class PyrightRange:
    start: PyrightPosition
    end: PyrightPosition


@dataclass
class PyrightUri:
    _key: str
    _filePath: str


class PyrightSeverityLevel(str, Enum):
    error = "error"
    warning = "warning"
    information = "information"
    unusedcode = "unusedcode"
    unreachablecode = "unreachablecode"
    deprecated = "deprecated"


class GitlabSeverityLevel(str, Enum):
    blocker = "blocker"
    major = "major"
    minor = "minor"
    info = "info"


@dataclass
class PyrightDiagnostic:
    severity: PyrightSeverityLevel
    message: str
    file: str | None = None
    uri: PyrightUri | None = None
    range: PyrightRange | None = None
    rule: str | None = None


@dataclass
class PyrightReport:
    version: str
    time: str
    generalDiagnostics: list[PyrightDiagnostic]
    summary: dict[str, int]

    @classmethod
    def from_file(cls: "PyrightReport", f: typing.TextIO) -> "PyrightReport":
        return cls(**json.load(f))


@dataclass
class CodeClimatePosition:
    line: int
    column: int


@dataclass
class CodeClimateRange:
    begin: CodeClimatePosition
    end: CodeClimatePosition


@dataclass
class GitlabReportLocation:
    path: Path
    positions: CodeClimateRange


@dataclass
class GitlabReport:
    description: str
    fingerprint: str
    severity: GitlabSeverityLevel
    location: GitlabReportLocation


def load_json(fname: str) -> PyrightReport:
    with open(fname, "rt") as f:
        return PyrightReport.from_file(f)


def extract_path(diag: PyrightDiagnostic) -> Path:
    assert not all(e is None for e in (diag.uri, diag.file)), "cannot parse file format"
    if diag.uri is not None:
        return Path(PyrightUri(**diag.uri)._filePath)
    elif diag.file is not None:
        return Path(diag.file)


def range_to_positions(range: PyrightRange) -> CodeClimateRange:
    return CodeClimateRange(
        begin=CodeClimatePosition(line=range.start.line, column=range.start.character),
        end=CodeClimatePosition(line=range.end.line, column=range.end.character),
    )


def convert_diagnostic_category_to_gitlab_severity(
    category: PyrightSeverityLevel,
) -> GitlabSeverityLevel:
    match category:
        case PyrightSeverityLevel.error:
            return GitlabSeverityLevel.blocker
        case PyrightSeverityLevel.warning:
            return GitlabSeverityLevel.major
        case PyrightSeverityLevel.unreachablecode:
            return GitlabSeverityLevel.major
        case PyrightSeverityLevel.deprecated:
            return GitlabSeverityLevel.minor
        case _:
            return GitlabSeverityLevel.info


def fingerprint(diag: PyrightDiagnostic) -> str:
    if diag.file is not None and diag.range is not None:
        with open(diag.file, "rt") as f:
            ls = f.readlines()
            # fingerprint the code in question
            return md5(os.linesep.join(ls[diag.range.start.line : diag.range.end.line + 1]).encode()).hexdigest()
    else:
        # not much to do ...
        return md5(str(diag).encode()).hexdigest()


def main():
    ap = ArgumentParser()
    ap.add_argument("--src", type=load_json)
    ap.add_argument("--output")
    ap.add_argument("--base-path", default=Path("."), type=Path)
    args = ap.parse_args()

    report = args.src if args.src is not None else PyrightReport.from_file(sys.stdin)

    fout = open(args.output, "wt") if args.output is not None else sys.stdout

    response: list[GitlabReport] = []

    for diag_js in report.generalDiagnostics:
        diag = PyrightDiagnostic(**diag_js)
        diag.range = PyrightRange(
            start=PyrightPosition(**diag.range["start"]),
            end=PyrightPosition(**diag.range["end"]),
        )

        response.append(
            asdict(GitlabReport(
                description=diag.message,
                fingerprint=fingerprint(diag),
                severity=convert_diagnostic_category_to_gitlab_severity(diag.severity),
                location=GitlabReportLocation(
                    path=str(extract_path(diag).resolve().relative_to(args.base_path.resolve())),
                    positions=range_to_positions(diag.range),
                ),
            ))
        )

    print(json.dumps(response), file=fout)


if __name__ == "__main__":
    main()

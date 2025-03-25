from dataclasses import dataclass
from pathlib import Path
from typing import Optional

@dataclass
class FooterBoundary:
    top_bottom: Optional[float] = None    # highest point of bottom footer blocks
    top_right: Optional[float] = None     # highest point of right footer blocks
    left_right: Optional[float] = None    # leftmost point of right footer blocks


@dataclass
class ParserConfig:
    generate_boundaries_pdf: bool = True
    generate_json: bool = True
    output_dir: Optional[Path] = None
    parse_to_markdown: bool = True
    grammar_correction: bool = True
from difflib import SequenceMatcher
import re
from spylls.hunspell import Dictionary
import validators

def similarity_ratio(str1: str, str2: str) -> float:
    """Calculate similarity ratio between two strings"""
    return SequenceMatcher(None, str1.strip(), str2.strip()).ratio()

def clean_text_for_comparison(text: str) -> str:
    """Remove everything except letters and numbers"""
    return ''.join(char for char in text if char.isalnum())

def clean_duplicate_lines(text: str, similarity_threshold: float = 0.97) -> str:
    """
    Remove duplicate lines based on text similarity.
    
    Parameters:
    - text: Input text with potential duplicate lines
    - similarity_threshold: Threshold above which lines are considered duplicates (0.0-1.0)
    
    Returns:
    - Text with duplicates removed
    """
    lines = text.split('\n')
    i = 0
    
    # First pass: Mark duplicates for removal
    to_remove = set()
    while i < len(lines):
        current_line = lines[i].strip()
        if not current_line:  # Skip empty lines in comparison
            i += 1
            continue
            
        # Look at all remaining lines for potential duplicates
        for j in range(i + 1, len(lines)):
            next_line = lines[j].strip()
            if not next_line or j in to_remove:
                continue  # Skip empty lines or already marked lines
            
            # we ignore tables and lines without letters
            has_letter = re.search('[a-zA-Z]', current_line)
            number_of_words = min(len(current_line.split()), len(next_line.split()))
            if '|' not in current_line and has_letter and number_of_words >= 3:
                if next_line.startswith(current_line):
                    # print("Current line: ",current_line)
                    # print("Next line: ", next_line)
                    to_remove.add(i)
                    break
                elif current_line.startswith(next_line):
                    # print("Current line: ",current_line)
                    # print("Next line: ", next_line)
                    to_remove.add(j)
                    break

            # Clean both lines for comparison
            clean_current = clean_text_for_comparison(current_line)
            clean_next = clean_text_for_comparison(next_line)
            
            if clean_current and clean_next:
                similarity = similarity_ratio(clean_current, clean_next)
                
                if similarity > similarity_threshold:
                    
                    # print(f"Similarity: {similarity:.4f} for lines:")
                    # print(f"  '{current_line}'")
                    # print(f"  '{next_line}'")
                    
                    # Choose whether to keep current or next line
                    if len(next_line) > len(current_line):
                        # If next line is longer/better, mark current for removal and use next as new reference
                        to_remove.add(i)
                        # i = j  # Move reference to this better line
                        # current_line = next_line  # Update current line
                        break
                    else:
                        # Mark the duplicate for removal
                        to_remove.add(j)
                else:
                    break
        
        i += 1
    
    # Second pass: Rebuild text without duplicates
    cleaned_lines = [line for idx, line in enumerate(lines) if idx not in to_remove]
    return '\n'.join(cleaned_lines)

def remove_bold(text):
    # Remove italic markers but keep the text inside, avoiding italic markers in links
    result = re.sub(r'(?<![\(\[])\b_(.+?)_\b(?![\]\)])', r'\1', text)
    # Remove bold markers but keep the text inside
    result = re.sub(r'\*\*(.+?)\*\*', r'\1', result)
    # Remove newlines in patterns like "–\n05" to become "–05"
    result = re.sub(r'–\n(\d+)', r'–\1', result)
    return result


def is_nonsense_text(text: str, threshold: float = 0.67) -> bool:
    letters = set('qwertyuiopasdfghjklñzxcvbnmáéíóúäëïöü')
    words = text.split()
    if not words:
        return False
    if len(words) == 1 and words[0] in letters:
        return True
    if "..." in words:
        return False
    # Count single letters, excluding numbers
    single_letters = sum(1 for word in words if len(word) == 1 and not word.isdigit())
    
    # Count short words, excluding numbers
    short_words = sum(1 for word in words if len(word) <= 2 and not word.isdigit())
    
    # Calculate ratios based on non-numeric words only
    non_numeric_words = sum(1 for word in words if not word.isdigit())
    if non_numeric_words == 0 or len(words) == sum(1 for word in words if not word.isalpha()):
        return False
        
    single_letter_ratio = single_letters / non_numeric_words
    short_word_ratio = short_words / non_numeric_words
    return single_letter_ratio > threshold or short_word_ratio > threshold

def remove_nonsense_text(text: str, dictionary: Dictionary) -> str:
    """Remove nonsense parts while preserving meaningful words"""
    # dictionary = Dictionary.from_zip('es.zip')
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            cleaned_lines.append(line)
            continue
            
        # Check if line contains nonsense
        if is_nonsense_text(stripped):
            words = stripped.split()
            # Keep words that are either longer than 2 chars, or a word in the dictionary
            good_words = [word for word in words if len(word) > 3]
            good_words = [word for word in good_words if dictionary.lookup(word)]
            
            if good_words:
                # print(f"Original line: '{stripped}'")
                # print(f"Keeping only: '{' '.join(good_words)}'")
                cleaned_lines.append(' '.join(good_words))
            # else:
            #     print(f"Removing entire line: '{stripped}'")
        else:
            cleaned_lines.append(line)
        
    cleaned_text = '\n'.join(cleaned_lines)
    
    # if cleaned_text != text:
    #     print("Original text:", repr(text))
    #     print("Cleaned text: ", repr(cleaned_text))
    #     print("---------------------------------")
    
    return cleaned_text

def replace_multiple_dots(text: str) -> str:
    """
    Replace any sequence of multiple dots with exactly 5 dots.
    """
    # First replace multiple dots with 5 dots
    text = re.sub(r'\.{3,}+\s*(\d+)', r'.....\1', text)
    
    # Then ensure one newline after .....{number} pattern
    # This regex matches: 5 dots + number + optional newlines + (optional next character)
    return re.sub(r'\.{5}(\d+)[\n]*(?=.|\n|$)', r'.....\1\n', text)

def remove_col_numbers(text: str) -> str:
    """Replace 'Col' followed by any number with an empty string"""
        
    # Use regular expression to find 'Col' followed by one or more digits
    return re.sub(r'Col\d+', '', text)

def find_urls(text):
    # Initial URL pattern - strict matching for http/https URLs
    url_pattern = r'https?://[^\s|\n|<|\]|\)|\}|\|]+'
    
    # Find all potential URLs
    potential_urls = re.finditer(url_pattern, text)
    
    validated_urls = []
    for match in potential_urls:
        url = match.group(0)
        # Remove any trailing characters that shouldn't be part of the URL
        url = url.rstrip('|,.:;]})')
        if validators.url(url):
            validated_urls.append(url)
    
    return validated_urls

def format_links_with_newlines(text):
    # Find all valid URLs in the text
    urls = find_urls(text)
    result = text
    
    # For each URL, check if it has newlines before/after
    for url in urls:
        # Look for the URL with potential surrounding newlines
        pattern = fr'\n\s*{re.escape(url)}|{re.escape(url)}\s*\n'
        match = re.search(pattern, result)
        
        if match and match.group(0):
            # If URL has newlines, replace it with bracketed version
            result = result.replace(match.group(0), f' []({url})')
    
    return result

def standardize_bullets(text):
    # Convert various bullet points to standardized format
    # Handle bullet points with # or other characters before them
    text = re.sub(r'#{1,}\s*[•*◦]\s', '- ', text, flags=re.MULTILINE)  # Handle "# •" case
    text = re.sub(r'^\s*#?\s*[•*◦]\s', '- ', text, flags=re.MULTILINE)  # Handle other cases with #
    # Handle `o` bullet points
    text = re.sub(r'^\s*```\s+', '- ', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*`●`\s+', '- ', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*`o`\s+', '- ', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*`◦`\s+', '- ', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*`•`\s+', '- ', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*✔\s+', '- ', text, flags=re.MULTILINE)
    # Ensure exactly one space after the bullet point
    text = re.sub(r'^\s*-\s+', '- ', text, flags=re.MULTILINE)
    return text

def fix_table_spacing_and_newlines(text: str) -> str:
    """
    Fix table spacing and newlines:
    1. Tables at start: exactly two \n before
    2. Tables in middle: exactly two \n before
    3. Leave table content as is
    4. Exactly two \n after each table
    """
    if not text:
        return ""
    # First remove spaces after newlines
    text = re.sub(r'\n\s+', '\n', text)
    # First split mixed content lines and normalize line endings
    processed_lines = []
    for line in text.splitlines(keepends=True):
        if '|' in line:
            before_table, after_table = line.split('|', 1)
            if before_table.strip():
                processed_lines.append(before_table)
                processed_lines.append('|' + after_table)
            else:
                processed_lines.append(line)
        else:
            processed_lines.append(line)
            
    # Now identify table blocks
    tables = []  # List of (start_idx, end_idx) for each table
    current_table = None
    
    for i, line in enumerate(processed_lines):
        has_table = '|' in line
        
        if has_table:
            if current_table is None:
                current_table = i
        else:
            if current_table is not None:
                tables.append((current_table, i-1))
                current_table = None
    
    if current_table is not None:
        tables.append((current_table, len(processed_lines)-1))
    
    if not tables:
        return text
        
    # Now fix spacing for each table
    result = []
    last_end = 0
    
    for start_idx, end_idx in tables:
        # Add content before table
        if start_idx > 0:
            content_before = ''.join(processed_lines[last_end:start_idx])
            result.append(content_before.rstrip('\n'))  # Remove all trailing newlines
            result.extend(['\n', '\n'])  # Add exactly two
        else:
            result.extend(['\n', '\n'])
            
        # Add table content
        table_content = ''.join(processed_lines[start_idx:end_idx+1])
        result.append(table_content.rstrip('\n'))  # Remove trailing newlines from table
        result.extend(['\n', '\n'])  # Add exactly two
        
        last_end = end_idx + 1
    
    # Add any remaining content
    if last_end < len(processed_lines):
        remaining = ''.join(processed_lines[last_end:])
        result.append(remaining.rstrip('\n'))
    
    return ''.join(result)

def format_figure_lines(text: str) -> str:
    """
    Format figure references that appear at the start of lines.
    Put brackets around figures and handle spacing according to what comes before/after.
    Special case: if line starts with #, remove it when formatting the figure
    """
    if not isinstance(text, str):
        raise TypeError('Input must be a string')
    
    if 'Figura' not in text:
        return text
    
    result = text
    current_pos = 0
    
    while True:
        # Find next figure
        figura_pos = result.find('Figura', current_pos)
        if figura_pos == -1:
            break
            
        # Check if figure is at start of line or after #
        line_start = figura_pos
        while line_start > 0 and result[line_start-1] != '\n':
            line_start -= 1
            
        line_prefix = result[line_start:figura_pos].strip()
        
        # If not at start of line and not after #, skip it
        if line_prefix and line_prefix != '#':
            current_pos = figura_pos + 1
            continue
        
        # Find end of figure text
        end_pos = figura_pos
        while end_pos < len(result) and not (result[end_pos] == '\n' or result[end_pos:].startswith(' Figura')):
            end_pos += 1
            
        figura_text = result[figura_pos:end_pos]
        if line_prefix == '#':
            figura_text = figura_text.strip()
            
        # Look back to find content before
        prev_content_end = line_start - 1
        while prev_content_end >= 0 and result[prev_content_end] in '\n':
            prev_content_end -= 1
        
        # Get the previous content line
        prev_content_start = prev_content_end
        while prev_content_start >= 0 and result[prev_content_start] != '\n':
            prev_content_start -= 1
        prev_content = result[prev_content_start + 1:prev_content_end + 1] if prev_content_end >= 0 else ''
        
        # Look after figure to find next content
        after_pos = end_pos
        next_line = ''
        if after_pos < len(result):
            # Skip blank lines
            while after_pos < len(result) and result[after_pos] in '\n':
                after_pos += 1
            if after_pos < len(result):
                next_end = after_pos
                while next_end < len(result) and result[next_end] != '\n':
                    next_end += 1
                next_line = result[after_pos:next_end].strip()
        
        # Get the remaining text after all we've processed
        remaining_text = result[after_pos:] if not next_line else result[after_pos + len(next_line):]
        if remaining_text.startswith('\n'):
            remaining_text = remaining_text[1:]
        
        # Determine spacing based on rules
        if prev_content.endswith('|'):
            spacing_before = '\n\n'
        elif prev_content.lstrip().startswith(('# ', '## ', '### ', '#### ', '##### ', '###### ')):
            spacing_before = '\n'
        else:
            spacing_before = ' ' if prev_content else ''
        
        if next_line.startswith('Figura'):
            spacing_after = ' '  # Just a space between consecutive figures
        elif next_line.startswith('# ') or next_line.startswith('## '):
            spacing_after = '\n\n'
        elif next_line.startswith('### ') or next_line.startswith('#### ') or next_line.startswith('##### ') or next_line.startswith('###### '):
            spacing_after = '\n'
        elif next_line.startswith('|'):
            spacing_after = '\n\n'
        elif next_line:
            spacing_after = '\n'
        else:
            spacing_after = ''
        
        # Create replacement
        first_part = result[:prev_content_start + 1] if prev_content_start >= 0 else ''
        if next_line.startswith('Figura'):
            middle_part = f'{prev_content}{spacing_before}[{figura_text}]{spacing_after}[{next_line}]'
        else:
            middle_part = f'{prev_content}{spacing_before}[{figura_text}]{spacing_after}{next_line}'
        
        # Add final newline if there was one
        if remaining_text:
            middle_part += '\n'
        
        # Combine all parts
        result = first_part + middle_part + remaining_text
        current_pos = len(first_part) + len(middle_part)
    
    return result

def fix_text_borders(text: str) -> str:
    """
    Fix text borders according to specific rules:
    1. Remove all newlines at start and end
    2. Process each line for proper spacing:
        - Ensure exactly two newlines before any line starting with #, EXCEPT:
          - If the previous line also starts with #, use only one newline
        - Add two newlines after text ending with |
        - Add one newline after text not ending with |
    """
    # Remove all newlines at start and end
    text = text.strip()
    
    # Split into lines for processing
    lines = text.split('\n')
    result_text = ""
    prev_line_starts_with_hash = False
    
    for i, line in enumerate(lines):
        if line.startswith('#'):
            # Check if the previous line also started with #
            if prev_line_starts_with_hash:
                # Previous line was a heading, use only one newline
                result_text = result_text.rstrip('\n')  # Remove any trailing newlines
                result_text += '\n' + line + '\n'  # Add exactly one newline
            else:
                # Normal case, ensure exactly two newlines before heading
                result_text = result_text.rstrip('\n')  # Remove any trailing newlines
                result_text += '\n\n' + line + '\n'  # Add exactly two newlines
            
            prev_line_starts_with_hash = True
        else:
            # For other lines, just add them with a newline
            result_text += line + '\n'
            prev_line_starts_with_hash = False
    
    # Handle special cases for | characters
    if result_text.endswith('|\n'):
        result_text += '\n'  # Add one more newline (total of two)
    
    if result_text.startswith('|'):
        result_text = '\n\n' + result_text  # Add two newlines at start
    
    return result_text
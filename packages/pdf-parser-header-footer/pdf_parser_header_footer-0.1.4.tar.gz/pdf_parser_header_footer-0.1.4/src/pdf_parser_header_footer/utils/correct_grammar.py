import Levenshtein
import json
import re
import time
import signal
from contextlib import contextmanager

class TimeoutException(Exception):
    pass

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    
    # Register a function to raise a TimeoutException on the signal
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    
    try:
        yield
    finally:
        # Disable the alarm
        signal.alarm(0)

def get_suggestions_with_timeout(dictionary, word, timeout=3):
    print(f"\nSearching suggestions for: '{word}'")
    start_time = time.time()
    
    try:
        with time_limit(timeout):
            suggestions = list(dictionary.suggest(word))
            elapsed_time = time.time() - start_time
            print(f"Search took {elapsed_time:.2f} seconds")
            return suggestions
    except TimeoutException:
        print(f"Search timed out after {timeout} seconds")
        return None
    except Exception as e:
        print(f"Error getting suggestions: {e}")
        return None

def correct_grammar(text, dictionary, dictionary_path):
    # dictionary = Dictionary.from_zip('es.zip')
    corrections_cache = {}
    
    # Load cache
    try:
        with open(dictionary_path, 'r', encoding='utf-8') as f:
            corrections_cache = json.load(f)
    except FileNotFoundError:
        corrections_cache = {}
    
    letters = set('qwertyuiopasdfghjklñzxcvbnmáéíóúäëïöü')
    
    # Allow hyphens in words for validation purposes
    def word_is_valid(element):
        return all(c.lower() in letters or c == '-' for c in element)
    
    # Check if a word without hyphens contains valid characters
    def word_without_hyphen_is_valid(element):
        return all(c.lower() in letters for c in element if c != '-')
    
    def split_line_into_elements(line):
        result = re.split(r'(\||\ )', line)
        return [x for x in result if x]
    
    # Function to detect and fix hyphenated words like "word- next" or "word -next"
    def fix_hyphenated_words(elements, i, is_line_start=False):
        # Skip if this is a list item (hyphen at beginning of line)
        if is_line_start and elements[i].startswith('-'):
            return False, i
            
        # Check for patterns like "word- " followed by another word (e.g., "trastor- nos")
        if (i + 2 < len(elements) and 
            word_without_hyphen_is_valid(elements[i]) and 
            elements[i].endswith('-') and 
            elements[i+1] == ' ' and 
            i+2 < len(elements) and
            word_without_hyphen_is_valid(elements[i+2])):
            
            first_part = elements[i][:-1]  # Remove trailing hyphen
            second_part = elements[i+2]
            combined = first_part + second_part
            
            combined_key = f"{first_part}-{second_part}"
            
            if combined_key in corrections_cache:
                elements[i] = corrections_cache[combined_key]
                elements.pop(i+2)  # Remove second word
                elements.pop(i+1)  # Remove space
                return True, i
            
            # Check if combined word is valid or has good suggestions
            if dictionary.lookup(combined):
                corrections_cache[combined_key] = combined
                elements[i] = combined
                elements.pop(i+2)  # Remove second word
                elements.pop(i+1)  # Remove space
                return True, i
            
            # Get suggestions for combined word
            suggestions = get_suggestions_with_timeout(dictionary, combined)
            
            if suggestions is None:
                # Timeout occurred, cache original form
                corrections_cache[combined_key] = f"{first_part} {second_part}"
                return False, i
            
            if suggestions:
                first_suggestion = suggestions[0]
                distance = Levenshtein.distance(combined.lower(), first_suggestion.lower())
                if distance <= 3:
                    corrections_cache[combined_key] = first_suggestion
                    elements[i] = first_suggestion
                    elements.pop(i+2)  # Remove second word
                    elements.pop(i+1)  # Remove space
                    return True, i
                else:
                    # Cache without hyphen if suggestion distance is too high
                    corrections_cache[combined_key] = f"{first_part} {second_part}"
                    elements[i] = first_part
                    return False, i
        
        # Check for reversed pattern: "word " followed by "-word" (e.g., "throm -boembolism")
        # Skip if the second element might be a list item
        if (i + 2 < len(elements) and 
            word_without_hyphen_is_valid(elements[i]) and 
            elements[i+1] == ' ' and 
            i+2 < len(elements) and
            elements[i+2].startswith('-') and
            word_without_hyphen_is_valid(elements[i+2][1:]) and
            # Make sure this isn't a list item (would have space before the -)
            not (i == 0 or (i >= 2 and elements[i-1] == ' ' and 
                (elements[i-2] == '\n' or elements[i-2].endswith('\n'))))):
            
            first_part = elements[i]
            second_part = elements[i+2][1:]  # Remove leading hyphen
            combined = first_part + second_part
            
            combined_key = f"{first_part}-{second_part}"
            
            if combined_key in corrections_cache:
                elements[i] = corrections_cache[combined_key]
                elements.pop(i+2)  # Remove second word
                elements.pop(i+1)  # Remove space
                return True, i
            
            # Check if combined word is valid or has good suggestions
            if dictionary.lookup(combined):
                corrections_cache[combined_key] = combined
                elements[i] = combined
                elements.pop(i+2)  # Remove second word
                elements.pop(i+1)  # Remove space
                return True, i
            
            # Get suggestions for combined word
            suggestions = get_suggestions_with_timeout(dictionary, combined)
            
            if suggestions is None:
                # Timeout occurred, cache original form
                corrections_cache[combined_key] = f"{first_part} {second_part}"
                return False, i
            
            if suggestions:
                first_suggestion = suggestions[0]
                distance = Levenshtein.distance(combined.lower(), first_suggestion.lower())
                if distance <= 3:
                    corrections_cache[combined_key] = first_suggestion
                    elements[i] = first_suggestion
                    elements.pop(i+2)  # Remove second word
                    elements.pop(i+1)  # Remove space
                    return True, i
                else:
                    # Cache without hyphen if suggestion distance is too high
                    corrections_cache[combined_key] = f"{first_part} {second_part}"
                    return False, i
        
        return False, i
    
    lines = text.split('\n')
    corrected_lines = []
    
    for line in lines:
        if not line:
            corrected_lines.append('')
            continue
            
        elements = split_line_into_elements(line)
        i = 0
        
        while i < len(elements):
            # Skip non-word elements, but allow hyphenated words to be processed
            if len(elements[i]) == 0 or (not word_is_valid(elements[i]) and not (
                    '-' in elements[i] and word_without_hyphen_is_valid(elements[i].replace('-', ''))
                )):
                i += 1
                continue
            
            # Check if this is the start of a line
            is_line_start = (i == 0 or 
                            (i >= 2 and elements[i-1] == ' ' and 
                             (elements[i-2] == '\n' or (isinstance(elements[i-2], str) and elements[i-2].endswith('\n')))))
            
            # Check for hyphenated words first
            fixed, i = fix_hyphenated_words(elements, i, is_line_start)
            if fixed:
                continue
                
            current_word = elements[i]
            
            # 1. Check cache first
            if current_word in corrections_cache:
                elements[i] = corrections_cache[current_word]
                i += 1
                continue
            
            # 2. Check dictionary for current word
            current_word_valid = dictionary.lookup(current_word)
            
            # If current word is valid, continue to next word
            if current_word_valid:
                i += 1
                continue
                
            next_word_valid = True
            next_word = None
            
            if i + 2 < len(elements) and word_is_valid(elements[i + 2]):
                next_word = elements[i + 2]
                next_word_valid = dictionary.lookup(next_word)
            
            # 3. If next word exists and either word is invalid, try combining
            if next_word and (not current_word_valid or not next_word_valid):
                separator = elements[i + 1]
                combined_key = f"{current_word}{separator}{next_word}"
                
                if combined_key in corrections_cache:
                    elements[i] = corrections_cache[combined_key]
                    elements.pop(i + 2)
                    elements.pop(i + 1)
                    continue
                
                combined = current_word + next_word
                suggestions = get_suggestions_with_timeout(dictionary, combined)
                
                if suggestions is None:
                    # Timeout occurred, cache original form
                    corrections_cache[combined_key] = current_word + separator + next_word
                    i += 1
                    continue
                
                if suggestions:
                    first_suggestion = suggestions[0]
                    distance = Levenshtein.distance(combined.lower(), first_suggestion.lower())
                    if distance <= 3:
                        corrections_cache[combined_key] = first_suggestion
                        elements[i] = first_suggestion
                        elements.pop(i + 2)
                        elements.pop(i + 1)
                        continue
                    else:
                        # Cache the original words if suggestion distance is too high
                        corrections_cache[combined_key] = current_word + separator + next_word
            
            # 4. If combining didn't work and current word is invalid, try single suggestions
            suggestions = get_suggestions_with_timeout(dictionary, current_word)
            
            if suggestions is None:
                # Timeout occurred, cache original form
                corrections_cache[current_word] = current_word
                i += 1
                continue
            
            if suggestions:
                first_suggestion = suggestions[0]
                distance = Levenshtein.distance(current_word.lower(), first_suggestion.lower())
                if distance <= 3:
                    corrections_cache[current_word] = first_suggestion
                    elements[i] = first_suggestion
                else:
                    # Cache the original word if suggestion distance is too high
                    corrections_cache[current_word] = current_word
            else:
                # If no suggestions found, cache the original word
                corrections_cache[current_word] = current_word
            
            i += 1
        
        corrected_lines.append(''.join(elements))
    
    # Save cache
    with open(dictionary_path, 'w', encoding='utf-8') as f:
        json.dump(corrections_cache, f, ensure_ascii=False, indent=2)
    
    return '\n'.join(line for line in corrected_lines)
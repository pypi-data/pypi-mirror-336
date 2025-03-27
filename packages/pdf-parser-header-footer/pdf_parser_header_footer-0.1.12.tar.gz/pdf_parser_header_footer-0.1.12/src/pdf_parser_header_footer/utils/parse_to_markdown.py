import json
import re
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, precision_score
from sklearn.ensemble import RandomForestClassifier
import pickle
from spylls.hunspell import Dictionary
import spacy

from pdf_parser_header_footer.utils.parse_to_markdown_utils import clean_duplicate_lines, fix_table_spacing_and_newlines, fix_text_borders, format_figure_lines, format_links_with_newlines, remove_bold, remove_col_numbers, remove_nonsense_text, replace_multiple_dots, standardize_bullets

def clean_page_content(text: str, dictionary: Dictionary, classifier) -> str:
    """Apply all cleaning steps to a piece of text"""
    if not isinstance(text, str):
        return text
    
    # Clean duplicate lines from text extraction
    clean_text = clean_duplicate_lines(text)
    
    # Detect title sections
    clean_text = format_markdown_with_ml(clean_text, classifier)
    
    # Remove bold text
    clean_text = remove_bold(clean_text)
    
    # Remove nonsense text from text extraction
    clean_text = remove_nonsense_text(clean_text, dictionary)
    
    # Replace multiple dots
    clean_text = replace_multiple_dots(clean_text)
    
    # Remove col numbers
    clean_text = remove_col_numbers(clean_text)

    # Format links 
    clean_text = format_links_with_newlines(clean_text)
    
    # Standardize bullets
    clean_text = standardize_bullets(clean_text)
    
    # Fix table spacing and newlines
    clean_text = fix_table_spacing_and_newlines(clean_text)
    
    # Format figure lines
    clean_text = format_figure_lines(clean_text)
    
    # Fix text borders
    clean_text = fix_text_borders(clean_text)

    # Clean duplicate lines again
    clean_text = clean_duplicate_lines(clean_text)
    return clean_text

class TitleClassifier:
    def __init__(self):
        self.model = None
        self.doc_stats = {}
        self.threshold = 0.5  # Default threshold, can be adjusted

    def set_threshold(self, threshold):
        """Set the probability threshold for title classification."""
        self.threshold = threshold

    def extract_features(self, text_lines, is_training=False, has_newlines_before=None, has_newlines_after=None):
        """Extract features from text lines."""
        features = []
        
        # Calculate document-level statistics for normalization if training
        if is_training:
            line_lengths = [len(line) for line in text_lines]
            word_counts = [len(line.split()) for line in text_lines]
            
            self.doc_stats = {
                'avg_line_length': np.mean(line_lengths) if line_lengths else 1,
                'avg_word_count': np.mean(word_counts) if word_counts else 1,
            }
        
        
        for i, line in enumerate(text_lines):
            
            # Basic features
            line_length = len(line)
            words = line.split()
            word_count = len(words)
            
            # Average word length
            avg_word_length = np.mean([len(word) for word in words]) if words else 0
            
            # Capitalization features
            capital_count = sum(1 for c in line if c.isupper())
            capital_ratio = capital_count / max(len(line), 1)
            
            # Title indicators
            starts_with_hash = bool(re.match(r'^#+\s', line))
            hash_count = len(re.match(r'^(#+)\s', line).group(1)) if starts_with_hash else 0
            
            surrounded_by_asterisks = bool(re.match(r'^\*\*.*\*\*$', line))

            # Numbering patterns (strong indicators of section titles)
            # text_content = re.sub(r'^\s*#+\s*|\s*\*\*', '', line)  # Remove # or ** prefix
            starts_with_number = bool(re.match(r'(^\s*#+\s*|^\s*\*\*)(_?)(\d+([\.\d]*))', line))
            # has_hierarchical_numbering = bool(re.match(r'(\d+([\.\d]*))', text_content))
            # has_section_numbering = bool(re.search(r'\s+\d+', text_content.lower()))
            
            # Context features
            followed_by_empty = has_newlines_after[i]
            preceded_by_empty = has_newlines_before[i]
            
            # Normalize features by document averages
            norm_line_length = line_length / self.doc_stats.get('avg_line_length', 1)
            norm_word_count = word_count / self.doc_stats.get('avg_word_count', 1)
            
            # Title case detection (First letter of each major word is capitalized)
            title_case = False
            if words:
                # Check if all remaining words start with uppercase
                title_case = all(word[0].isupper() if len(word) > 0 and word[0].isalpha() else True 
                                for word in words)
            
            feature_dict = {
                'line_length': line_length,
                'norm_line_length': norm_line_length,
                'word_count': word_count,
                'norm_word_count': norm_word_count,
                'avg_word_length': avg_word_length,
                'capital_ratio': capital_ratio,
                'starts_with_hash': int(starts_with_hash),
                'hash_count': hash_count,
                'surrounded_by_asterisks': int(surrounded_by_asterisks),
                'starts_with_number': int(starts_with_number),
                'followed_by_empty': int(followed_by_empty),
                'preceded_by_empty': int(preceded_by_empty),
                'title_case': int(title_case),
                'ends_with_punctuation': int(line.rstrip()[-1] in '.!?:;') if line.strip() else 0,
            }
            
            features.append(feature_dict)
            
        
        return pd.DataFrame(features)

    def train(self, training_data_path):
        """Train the title classifier model."""
        # Load training data
        with open(training_data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract text and labels
        text_lines = [item['text'] for item in data]
        labels = [item['is_title'] for item in data]
        has_newlines_before = [item['has_newlines_before'] for item in data]
        has_newlines_after = [item['has_newlines_after'] for item in data]
        
        # Extract features
        X = self.extract_features(text_lines, is_training=True, has_newlines_before=has_newlines_before, has_newlines_after=has_newlines_after)
        y = np.array(labels)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Calculate class weights (for imbalanced data)
        pos_weight = (len(y_train) - sum(y_train)) / sum(y_train) if sum(y_train) > 0 else 1
        class_weight = {0: 1.0, 1: pos_weight}
        
        # Train model
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=2,
            class_weight=class_weight,
            random_state=42
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        y_pred = (y_pred_proba >= self.threshold).astype(int)
        
        # print("Model Performance:")
        # print(classification_report(y_test, y_pred))
        # print(f"Precision at threshold {self.threshold}: {precision_score(y_test, y_pred):.4f}")
        
        # Feature importance
        feature_importance = self.model.feature_importances_
        feature_names = X.columns
        importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': feature_importance})
        importance_df = importance_df.sort_values('Importance', ascending=False)
        # print("\nFeature Importance:")
        # print(importance_df)
        
        return self
    
    def save(self, model_path):
        """Save the trained model to disk."""
        if self.model is None:
            raise ValueError("Model has not been trained yet")
        
        model_data = {
            'model': self.model,
            'doc_stats': self.doc_stats,
            'threshold': self.threshold
        }
        
        with open(model_path, 'wb') as f:
            pickle.dump(model_data, f)
            
        # print(f"Model saved to {model_path}")
    
    def load(self, model_path):
        """Load a trained model from disk."""
        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
        
        self.model = model_data['model']
        self.doc_stats = model_data['doc_stats']
        self.threshold = model_data['threshold']
        
        # print(f"Model loaded from {model_path}")
        return self
    
    def predict(self, text_lines, has_newlines_before, has_newlines_after):
        """Predict if each line is a title and return probabilities."""
        if self.model is None:
            raise ValueError("Model has not been trained or loaded yet")
        
        # Extract features
        X = self.extract_features(text_lines, has_newlines_before=has_newlines_before, has_newlines_after=has_newlines_after)
        
        # Predict
        probabilities = self.model.predict_proba(X)[:, 1]
        predictions = (probabilities >= self.threshold).astype(int)
        
        # Get title levels
        title_levels = []
        for i, line in enumerate(text_lines):
            if predictions[i] == 1 and line.strip() !="":
                # Check if it starts with hash
                match = re.match(r'^(#+)\s', line)
                if match:
                    title_levels.append(len(match.group(1)))
                else:
                    title_levels.append(0)  # Title but not with hash
            else:
                title_levels.append(-1)  # Not a title
        
        return predictions, probabilities, title_levels

def format_markdown_with_ml(text, classifier, min_probability=0.5):
    """Format text by detecting and formatting titles using ML classifier."""
    if not text:
        return ""
    
    lines = text.split('\n')
     # Calculate newlines before and after each line
    has_newlines_before = []
    has_newlines_after = []
    
    # Process the text to detect multiple consecutive newlines
    raw_lines = text.split('\n')
    empty_line_indices = [i for i, line in enumerate(raw_lines) if not line.strip()]
    
    for i in range(len(lines)):
        # Check if there are empty lines before this line
        has_empty_before = False
        if i > 0:
            # Check if there are at least 2 consecutive empty lines before this one
            if i - 1 in empty_line_indices and i - 2 in empty_line_indices:
                has_empty_before = True
        
        # Check if there are empty lines after this line
        has_empty_after = False
        if i < len(lines) - 1:
            # Check if there are at least 2 consecutive empty lines after this one
            if i + 1 in empty_line_indices and i + 2 in empty_line_indices:
                has_empty_after = True
                
        has_newlines_before.append(int(has_empty_before))
        has_newlines_after.append(int(has_empty_after))
    predictions, probabilities, title_levels = classifier.predict(lines, has_newlines_before, has_newlines_after)
    
    formatted_lines = []
    for i, (line, is_title, prob, level) in enumerate(zip(lines, predictions, probabilities, title_levels)):
        # if is_title:
        #     print("--------------------------------")
        #     print("Line: ", line)
        #     print("Is title: ", is_title)
        #     print("Probability: ", prob)
        #     print("Level of the title: ", level)
        #     print("---------------------------------")
        if is_title and prob >= min_probability:
            # If it's already formatted with #, keep it
            if re.match(r'^#+\s', line):
                formatted_lines.append(line)
            # Otherwise, format based on title level (if available)
            elif level > 0:
                # This shouldn't happen in normal flow, but just in case
                formatted_lines.append('#' * level + ' ' + line)
            else:
                # Default to level 2 for detected titles without explicit level
                formatted_lines.append('## ' + line)
        else:
            # If not a title but starts with #, remove the hashtags
            if re.match(r'^#+\s', line):
                # Strip leading hashtags and any space immediately after them
                cleaned_line = re.sub(r'^#+\s+', '', line)
                formatted_lines.append(cleaned_line)
            else:
                formatted_lines.append(line)
    
    return '\n'.join(formatted_lines)


class LineJoinerClassifier:
    def __init__(self):
        self.model = None
        self.doc_stats = {}
        self.threshold = 0.5 
        self.nlp = spacy.load("es_core_news_sm")

    def set_threshold(self, threshold):
        """Set the probability threshold for line joining classification."""
        self.threshold = threshold

    def extract_features(self, line_pairs, is_training=False):
        """
        Extract features from line pairs to determine if they should be joined.
        
        Args:
            line_pairs: List of tuples (line1, line2) for which to extract features
            is_training: Whether this is for training (to calculate document statistics)
            
        Returns:
            DataFrame of features for each line pair
        """
        features = []
        
        # Calculate document-level statistics for normalization if training
        if is_training:
            all_lines = [line for pair in line_pairs for line in pair]
            line_lengths = [len(line) for line in all_lines]
            word_counts = [len(line.split()) for line in all_lines]
            
            self.doc_stats = {
                'avg_line_length': np.mean(line_lengths) if line_lengths else 1,
                'avg_word_count': np.mean(word_counts) if word_counts else 1,
                'max_line_length': max(line_lengths) if line_lengths else 1,
            }
        
        
        for line1, line2 in line_pairs:
            # Basic line features
            line1_length = len(line1)
            line2_length = len(line2)

            line1_words = line1.split()
            line2_words = line2.split()

            line1_word_count = len(line1_words)
            line2_word_count = len(line2_words)
            
            # Length difference
            length_diff = abs(line1_length - line2_length)
            
            #Is a title
            line1_is_title = int(line1.startswith('#'))
            
            #Is a list
            line2_is_list = int(line2.startswith('-') or bool(re.match(r'^\d+\.\s*[a-zA-Z]', line2)) or bool(re.match(r'^([a-zA-Z])\)', line2)))
            
            # Ending and starting patterns
            line1_ends_with_fullstop = int(line1.endswith('.'))
            letters = set('qwertyuiopasdfghjklñzxcvbnmáéíóúäëïöü')
            line2_starts_with_lowercase = int(bool(line2[0].lower() in letters) and line2[0].islower())
            line2_starts_with_uppercase = int(bool(line2[0].lower() in letters) and line2[0].isupper())
                        
            
            feature_dict = {
                'line1_length': line1_length,
                'line2_length': line2_length,
                'line1_word_count': line1_word_count,
                'line2_word_count': line2_word_count,
                'length_diff': length_diff,
                'line1_is_title': line1_is_title,
                'line2_is_list': line2_is_list,
                'line1_ends_with_fullstop': line1_ends_with_fullstop,
                'line2_starts_with_lowercase': line2_starts_with_lowercase,
                'line2_starts_with_uppercase': line2_starts_with_uppercase,
            }
            
            features.append(feature_dict)
        
        return pd.DataFrame(features)

    def train(self, training_data_path):
        """Train the line joining classifier model."""
        # Load training data
        with open(training_data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract line pairs and labels
        line_pairs = [(item['line1'], item['line2']) for item in data]
        labels = [item['should_join'] for item in data]
        
        # Extract features
        X = self.extract_features(line_pairs, is_training=True)
        y = np.array(labels)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Calculate class weights (for imbalanced data)
        pos_weight = (len(y_train) - sum(y_train)) / sum(y_train) if sum(y_train) > 0 else 1
        class_weight = {0: 1.0, 1: pos_weight}
        
        # Train model
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=2,
            class_weight=class_weight,
            random_state=42
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        y_pred = (y_pred_proba >= self.threshold).astype(int)
        
        # print("Model Performance:")
        # print(classification_report(y_test, y_pred))
        # print(f"Precision at threshold {self.threshold}: {precision_score(y_test, y_pred):.4f}")
        # print(f"Recall at threshold {self.threshold}: {recall_score(y_test, y_pred):.4f}")
        # print(f"F1 score at threshold {self.threshold}: {f1_score(y_test, y_pred):.4f}")
        
        # Feature importance
        feature_importance = self.model.feature_importances_
        feature_names = X.columns
        importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': feature_importance})
        importance_df = importance_df.sort_values('Importance', ascending=False)
        # print("\nFeature Importance:")
        # print(importance_df)
        
        return self
    
    def save(self, model_path):
        """Save the trained model to disk."""
        if self.model is None:
            raise ValueError("Model has not been trained yet")
        
        model_data = {
            'model': self.model,
            'doc_stats': self.doc_stats,
            'threshold': self.threshold
        }
        
        with open(model_path, 'wb') as f:
            pickle.dump(model_data, f)
            
        # print(f"Model saved to {model_path}")
    
    def load(self, model_path):
        """Load a trained model from disk."""
        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
        
        self.model = model_data['model']
        self.doc_stats = model_data['doc_stats']
        self.threshold = model_data['threshold']
        
        # print(f"Model loaded from {model_path}")
        return self
    
    def predict(self, line_pairs):
        """
        Predict if each line pair should be joined.
        
        Args:
            line_pairs: List of tuples (line1, line2) to predict on
            
        Returns:
            Tuple of (predictions, probabilities) where:
                - predictions: 1 if lines should be joined, 0 if they should stay separate
                - probabilities: Probability of joining
        """
        if self.model is None:
            raise ValueError("Model has not been trained or loaded yet")
        
        # Extract features
        X = self.extract_features(line_pairs)
        
        # Predict
        probabilities = self.model.predict_proba(X)[:, 1]
        predictions = (probabilities >= self.threshold).astype(int)
        
        return predictions, probabilities


def format_text_with_line_joiner(text, classifier, min_probability=0.5):
    """
    Format text by joining or separating lines based on ML classifier predictions.
    
    Args:
        text: Input text to format
        classifier: Trained LineJoinerClassifier
        min_probability: Minimum probability to join lines
        
    Returns:
        Formatted text with lines properly joined or separated
    """
    if not text:
        return ""
    
    lines = text.split('\n')
    
    # If there's only one line, return as is
    if len(lines) <= 1:
        return text
    
    # Initialize the result with the first line
    result = [lines[0]]
    # The current index in the original lines list
    current_idx = 1
    
    # Process lines sequentially
    while current_idx < len(lines):
        # Get the current line to process
        current_line = lines[current_idx]
        
        # Skip if current line is empty (we'll keep the newline)
        if not current_line.strip():
            result.append("")
            current_idx += 1
            continue
        
        # Get the last part of our result so far (could be a joined line)
        last_part = result[-1]
        
        # Skip if last part is empty
        if not last_part.strip():
            result.append(current_line)
            current_idx += 1
            continue
        
        # Check if we should join these lines
        line_pair = [(last_part, current_line)]
        predictions, probabilities = classifier.predict(line_pair)
        should_join = predictions[0] == 1 and probabilities[0] >= min_probability
        # print("-------------------------")
        # print("Current: ", last_part)
        # print("Next: ", current_line)
        # print("Predictions: ", predictions)
        # print("Probabilities: ", probabilities)
        # print("Should join: ", should_join)
        # print("-------------------------")
        
        if ("....." in last_part and "....." in current_line) or (last_part.startswith('|') or current_line.startswith('|')):
            result.append(current_line)
        elif should_join:
            # Normal joining with a space
            result[-1] = last_part + " " + current_line
        else:
            # Keep separate
            result.append(current_line)
        
        # Move to the next line
        current_idx += 1
    
    return '\n'.join(result)

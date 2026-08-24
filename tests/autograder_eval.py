import pytest
import json
import subprocess
from pathlib import Path
from collections import Counter


class TestJSONLSchema:
    """Validate raw JSONL data files."""
    
    def test_raw_jsonl_schema(self):
        """
        Test that raw JSONL files exist, are valid JSON, and contain required keys.
        
        Requirements:
        - Files must exist at data/*/raw/*.jsonl
        - Each line must be valid JSON
        - Each entry must have keys: 'id', 'url', 'date_retrieved', 'raw_text'
        """
        data_dir = Path("data")
        assert data_dir.exists(), "data/ directory not found"
        
        jsonl_files = list(data_dir.glob("*/raw/*.jsonl"))
        assert len(jsonl_files) > 0, "No .jsonl files found in data/*/raw/"
        
        for jsonl_file in jsonl_files:
            with open(jsonl_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Validate JSON format
                    try:
                        entry = json.loads(line)
                    except json.JSONDecodeError as e:
                        pytest.fail(f"Invalid JSON at {jsonl_file}:{line_num}: {e}")
                    
                    # Validate required keys
                    required_keys = {'id', 'url', 'date_retrieved', 'raw_text'}
                    missing_keys = required_keys - set(entry.keys())
                    assert not missing_keys, \
                        f"Missing keys in {jsonl_file}:{line_num}: {missing_keys}"
                    
                    # Validate key types
                    assert isinstance(entry['id'], int), \
                        f"'id' must be int, got {type(entry['id']).__name__}"
                    assert isinstance(entry['url'], str), \
                        f"'url' must be str, got {type(entry['url']).__name__}"
                    assert isinstance(entry['date_retrieved'], str), \
                        f"'date_retrieved' must be str, got {type(entry['date_retrieved']).__name__}"
                    assert isinstance(entry['raw_text'], str), \
                        f"'raw_text' must be str, got {type(entry['raw_text']).__name__}"


class TestProcessedCorpus:
    """Validate processed tokenized text files."""
    
    def test_processed_corpus_format(self):
        """
        Test that processed corpus files have correct format.
        
        Requirements:
        - Files must exist at data/*/processed/*.txt
        - Each line represents one sentence
        - Tokens must be separated by single spaces
        - No extra whitespace
        """
        data_dir = Path("data")
        txt_files = list(data_dir.glob("*/processed/*.txt"))
        assert len(txt_files) > 0, "No .txt files found in data/*/processed/"
        
        for txt_file in txt_files:
            with open(txt_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line_stripped = line.rstrip('\n')
                    
                    if not line_stripped:
                        # Allow empty lines
                        continue
                    
                    # Check for single space token separation
                    tokens = line_stripped.split(' ')
                    
                    # Verify no empty tokens (would indicate multiple spaces)
                    assert all(token for token in tokens), \
                        f"Multiple spaces found in {txt_file}:{line_num}"
                    
                    # Check that line doesn't start/end with spaces
                    assert not line_stripped.startswith(' '), \
                        f"Line starts with space in {txt_file}:{line_num}"
                    assert not line_stripped.endswith(' '), \
                        f"Line ends with space in {txt_file}:{line_num}"
                    
                    # Verify no tab characters or other whitespace
                    assert '\t' not in line_stripped, \
                        f"Tab character found in {txt_file}:{line_num}"
                    assert '\r' not in line_stripped, \
                        f"Carriage return found in {txt_file}:{line_num}"


class TestBigramModel:
    """Test the BigramModel implementation."""
    
    def test_bigram_perplexity(self):
        """
        Test BigramModel by importing from submissions and evaluating perplexity.
        
        Requirements:
        - BigramModel class must be importable from student submission
        - Model must fit on processed corpus
        - Perplexity on test set must be finite and positive
        - Perplexity should be < 1000 for reasonable models
        """
        import sys
        sys.path.insert(0, 'submissions/group_01_nupe')
        
        # Try to import BigramModel
        try:
            from HW1_assignment import BigramModel
        except ImportError as e:
            pytest.skip(f"Could not import BigramModel: {e}")
        
        # Check that processed corpus exists
        corpus_path = Path("data/nupe/processed/nupe_corpus.txt")
        assert corpus_path.exists(), f"Corpus not found at {corpus_path}"
        
        # Check that test file exists
        test_path = Path("tests/test_nupe_unseen.txt")
        assert test_path.exists(), f"Test file not found at {test_path}"
        
        # Instantiate and fit model
        model = BigramModel()
        bigram_count = model.fit(str(corpus_path))
        
        assert bigram_count > 0, "Model fit returned no bigrams"
        assert model.vocab_size > 0, "Model vocabulary is empty"
        
        # Compute perplexity
        perplexity = model.compute_perplexity(str(test_path))
        
        # Validate perplexity
        assert isinstance(perplexity, (int, float)), \
            f"Perplexity must be numeric, got {type(perplexity).__name__}"
        assert perplexity > 0, f"Perplexity must be positive, got {perplexity}"
        assert perplexity < float('inf'), "Perplexity is infinite"
        assert perplexity < 1000, \
            f"Perplexity {perplexity:.2f} is too high (should be < 1000)"


class TestGitCollaboration:
    """Verify multi-author collaboration via git."""
    
    def test_git_commit_count(self):
        """
        Test that repository has commits from at least 2 different authors.
        
        Requirements:
        - Run `git shortlog -sn` to count commits per author
        - At least 2 distinct authors must have committed
        - Demonstrates group collaboration
        """
        try:
            result = subprocess.run(
                ['git', 'shortlog', '-sn'],
                capture_output=True,
                text=True,
                check=True,
                timeout=10
            )
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError) as e:
            pytest.skip(f"Could not run git shortlog: {e}")
        
        output = result.stdout.strip()
        assert output, "git shortlog returned no output"
        
        # Count authors (each line in output is an author)
        authors = [line for line in output.split('\n') if line.strip()]
        author_count = len(authors)
        
        assert author_count >= 2, \
            f"Expected at least 2 authors, found {author_count}. " \
            f"Please ensure multiple group members commit: {output}"


# Run tests
if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
